#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'validation'))
from mandel_reference import MandelParameters,MandelSolution

def analyze(path):
    path=Path(path);prov=json.loads((path/'provenance.json').read_text());cfg=prov['configuration'];q=cfg['load']
    d=np.genfromtxt(path/'solution.csv',names=True,delimiter=',');t=d['time']
    # Top-boundary resultant convention. The decks (decks.py) put a uniform
    # compressive traction of magnitude q_L on the top boundary via
    # FunctionNeumannBC. The Mandel quarter domain spans x in [0,1] (width a=1);
    # every full-domain case spans x in [-1,1] (width 2a=2). The applied top
    # resultant is therefore -a*q_L (quarter) or -2*a*q_L (full), with a=1.
    # Non-quarter decks ramp the load over t in [0,0.002]; the quarter deck is a
    # step load. top_reaction is the summed vertical plate reaction, which must
    # balance the instantaneous applied resultant.
    quarter = cfg.get('case') == 'mandel'
    width = 1.0 if quarter else 2.0
    expected_force = -q * width
    ramp_time = 0.0 if quarter else 0.002
    ramp = np.ones_like(t) if quarter else np.minimum(t / ramp_time, 1.0)
    applied_resultant = expected_force * ramp
    m=d['mass'];reaction=d['mass_reaction'];flux=-reaction
    budget=m-m[0]+np.r_[0,np.cumsum(np.diff(t)*flux[1:])]
    mobilized=np.maximum(abs(m-m[0]),np.r_[0,np.cumsum(np.diff(t)*abs(flux[1:]))]);floor=max(abs(m[0])*1e-12,1e-16)
    # A run is comparable with the Mandel series only when its deck solves the same
    # reference-modulus quarter-domain problem (case='mandel').
    comparable = cfg.get('case') == 'mandel'
    report=dict(
        discrete_mass_absolute=float(np.max(abs(budget))),
        discrete_mass_mobilized_relative=float(np.max(abs(budget[1:])/np.maximum(mobilized[1:],floor))),
        force_relative=float(np.max(np.abs(d['top_reaction'][1:]-applied_resultant[1:]))/abs(expected_force)),
        expected_force=float(expected_force),
        force_convention=('top boundary carries a uniform compressive traction of magnitude q_L over '
                          'width a (quarter Mandel, a=1) or 2a (full domain, a=1); expected top resultant '
                          'is -a*q_L (quarter) or -2*a*q_L (full).'),
        platen_equality_absolute=float(np.max(abs(d['platen_min']-d['platen_max']))),
        peak_pressure=float(np.max(d['center_pressure'])),
        peak_time=float(t[np.argmax(d['center_pressure'])]),
        reference_comparable=comparable,
    )
    # The Mandel series is the reference-modulus quarter-domain problem solved by
    # the `mandel` decks (decks.make: phi_s0=0.9, K=1, isotropic_stiffness(2.5,5/6),
    # x,y in [0,1]x[0,0.1]). Every other deck solves a different problem and the
    # reference-normalized discrepancy would divide differences between different
    # materials/domains, so it is not emitted for them.
    if not comparable:
        stale=path/'reference_comparison.csv'
        if stale.exists():
            stale.unlink()
        reason={
            'partial':('The partial-drainage runs use the square domain [-1,1]x[-1,1] '
                '(h=1 in decks.py), while the Mandel analytical reference is the slender domain '
                '[-1,1]x[-0.1,0.1] (a=1, b=0.1).'),
            'anisotropic':('The rotated-anisotropy runs use DEFAULT_CS with phi_s0=0.6 and K=7, '
                'while the Mandel reference is the reference-modulus isotropic problem of the '
                'quarter-domain decks (phi_s0=0.9, K=1, G=0.75, alpha=0.6).'),
            'isotropic':('The isotropic comparison run uses isotropic_stiffness(28,16.8) with '
                'phi_s0=0.6 and K=7, not the reference-modulus problem of the quarter-domain decks '
                '(phi_s0=0.9, K=1, G=0.75).'),
        }.get(cfg.get('case'),'The run does not use the reference-modulus quarter-domain deck.')
        report['reference_note']=(reason+' A Mandel-normalized discrepancy would compare different '
            'problems, so no reference-normalized field is emitted; only the run diagnostics '
            '(mass balance, force balance, platen equality, peak pressure) are reported.')
    else:
        ref=MandelSolution(MandelParameters());v=ref.evaluate(0,.1,t,load=q);vx=ref.evaluate(1,0,t,load=q)
        p0=float(ref.evaluate(0,0,0,load=q)['pressure']);uy_drained=float(ref.evaluate(0,.1,1e5,load=q)['uy']);ux_drained=float(ref.evaluate(1,0,1e5,load=q)['ux'])
        curve=np.c_[t,d['center_pressure'],v['pressure'],d['platen_min'],v['uy'],d['edge_ux'],vx['ux']]
        np.savetxt(path/'reference_comparison.csv',curve,delimiter=',',header='time,pressure,pressure_reference,platen,platen_reference,edge_ux,edge_ux_reference',comments='')
        profile_max=0;profile_l2=[];resolved_max=0;sample_errors={}
        for n,time in enumerate(t):
            pfile=path/f'solution_profile_{n:04d}.csv'
            if not pfile.exists():continue
            line=np.genfromtxt(pfile,delimiter=',',names=True)
            pr=ref.evaluate(line['x'],0,time,load=q)['pressure'];diff=(line['p']-pr)/p0
            if time>0:
                profile_max=max(profile_max,float(np.max(abs(diff))));profile_l2.append(float(np.sqrt(np.sum((diff[1:]**2+diff[:-1]**2)*np.diff(line['x'])/2))))
            if time>=.01-1e-12:resolved_max=max(resolved_max,float(np.max(abs(diff))))
            if any(abs(time-target)<1e-10 for target in [.01,.02,.05,.1,.2]):sample_errors[str(float(time))]=float(np.max(abs(diff)))
        report.update(dict(
            pressure_max_normalized=float(np.max(abs(d['center_pressure'][1:]-v['pressure'][1:]))/p0),
            platen_max_normalized=float(np.max(abs(d['platen_min'][1:]-v['uy'][1:]))/abs(uy_drained)),
            edge_ux_max_normalized=float(np.max(abs(d['edge_ux'][1:]-vx['ux'][1:]))/abs(ux_drained)),
            profile_max_normalized=profile_max,
            profile_max_after_t001=resolved_max,
            profile_fixed_time_errors=sample_errors,
            profile_rms_normalized=float(np.sqrt(np.mean(np.square(profile_l2)))) if profile_l2 else None,
            peak_pressure_normalized=float(np.max(d['center_pressure'])/p0),
        ))
    report['configuration']=cfg
    (path/'analysis.json').write_text(json.dumps(report,indent=2)+'\n');print(path.name,json.dumps(report),flush=True);return report
if __name__=='__main__':
    for arg in sys.argv[1:]:analyze(arg)
