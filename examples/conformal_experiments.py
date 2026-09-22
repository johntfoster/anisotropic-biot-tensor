#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproducible synthetic conformal-distention material-point experiments.

Run: python3 examples/conformal_experiments.py. CSV data, metadata, and vector
PDF figures are written under build/conformal. All stresses use one arbitrary
unit; these curves are constitutive illustrations, not material calibration.
"""
import csv
import json
import hashlib
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from conformal_model import Model, I, isotropic_stiffness, shear_gradient, rotation_z

DEST = Path(__file__).resolve().parents[1]/'build/conformal'
from figure_style import COLORS, apply_style, publication_size
apply_style()


def write_csv(name, records):
    with (DEST/name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader(); writer.writerows(records)


def save(fig, name):
    publication_size(fig)
    fig.savefig(DEST/(name+'.pdf'))
    fig.savefig(DEST/(name+'.png'), dpi=160)
    plt.close(fig)


def record(state, **extra):
    out = dict(extra, J=state['J'], mineral_volume=state['y'], a=state['a'],
        solid_fraction=state['solid_fraction'], W=state['W'], storage=state['storage'],
        mineral_residual=state['residual'], scalar_stability=state['stability'])
    for field in ('B', 'sigma'):
        for i,j in ((0,0), (1,1), (2,2), (0,1), (0,2), (1,2)):
            out[f'{field}{i+1}{j+1}'] = float(state[field][i,j])
    return out


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    anis = Model(); iso = Model(isotropic_stiffness(anis.ks, anis.mu_average))
    models = [('anisotropic', anis), ('isotropic', iso)]
    all_states = []
    def evaluate(model, f, p, rotation=I):
        value = model.state(f,p,rotation); all_states.append(value)
        return value

    pressures = np.linspace(0,6,121)
    pressure = {name:[evaluate(model,I,p) for p in pressures] for name,model in models}
    write_csv('pressure_response.csv', [record(st, material=name, pressure=p)
        for name,_ in models for p,st in zip(pressures,pressure[name])])
    fig, axes = plt.subplots(2,2,figsize=(7.2,5.6), constrained_layout=True)
    for i,color in enumerate(COLORS):
        axes[0,0].plot(pressures,[st['B'][i,i] for st in pressure['anisotropic']],color=color,label=fr'$B_{{{i+1}{i+1}}}$')
        axes[0,1].plot(pressures,[st['sigma'][i,i] for st in pressure['anisotropic']],color=color,label=fr'$\sigma_{{{i+1}{i+1}}}$')
    axes[0,0].plot(pressures,[st['B'][0,0] for st in pressure['isotropic']], 'k--',label='Isotropic')
    axes[0,1].plot(pressures,[st['sigma'][0,0] for st in pressure['isotropic']], 'k--',label='Isotropic')
    axes[1,0].plot(pressures,[st['y'] for st in pressure['anisotropic']], color=COLORS[0],label=r'$\bar J$, both minerals')
    axes[1,0].plot(pressures,[st['solid_fraction'] for st in pressure['anisotropic']], color=COLORS[1],label=r'$\phi_s$, both minerals')
    for i,color in enumerate(COLORS):
        # At F=I the zero-pressure stress is zero.
        error = [st['sigma'][i,i]+p*st['B'][i,i] for p,st in zip(pressures,pressure['anisotropic'])]
        axes[1,1].plot(pressures,error,color=color,label=fr'$i={i+1}$')
    labels = [('(a) Fixed-deformation coupling',r'$B_{ii}$'),
              ('(b) Pressure-induced total stress',r'$\sigma_{ii}$ [stress unit]'),
              ('(c) Mineral volume and solid fraction','Dimensionless'),
              ('(d) Error from using instantaneous $pB$',r'$\sigma_{ii}(p)+pB_{ii}(p)$ [stress unit]')]
    for ax,(title,ylabel) in zip(axes.flat,labels):
        ax.set(title=title,xlabel='$p$ [stress unit]',ylabel=ylabel); ax.legend(); ax.grid(alpha=.2)
    save(fig,'pressure_response')

    gammas = np.linspace(-.8,.8,161)
    shear = {name:[evaluate(model,shear_gradient(g),2.) for g in gammas] for name,model in models}
    write_csv('shear_response.csv',[record(st,material=name,gamma=g,pressure=2.)
        for name,_ in models for g,st in zip(gammas,shear[name])])
    fig,axes = plt.subplots(1,3,figsize=(9.1,2.7),constrained_layout=True)
    for i,color in enumerate(COLORS):
        axes[0].plot(gammas,[st['B'][i,i] for st in shear['anisotropic']],color=color,label=fr'$B_{{{i+1}{i+1}}}$')
    axes[0].plot(gammas,[st['B'][0,0] for st in shear['isotropic']], 'k--',label='Isotropic')
    for name,_ in models:
        style = '-' if name=='anisotropic' else '--'
        color = COLORS[0] if name=='anisotropic' else 'k'
        axes[1].plot(gammas,[st['B'][0,1] for st in shear[name]],style,color=color,label=name.capitalize())
        axes[2].plot(gammas,[st['y'] for st in shear[name]],style,color=color,label=name.capitalize())
    for ax,title,ylabel in zip(axes,['(a) Directional coupling','(b) Shear pressure coupling','(c) Shape-induced mineral volume'],['$B_{ii}$','$B_{12}$',r'$\bar J$']):
        ax.set(title=title,xlabel=r'Shear parameter $\gamma$',ylabel=ylabel); ax.grid(alpha=.2); ax.legend()
    save(fig,'shear_response')

    fstar = shear_gradient(.65); angle = np.linspace(0,2*np.pi,361)
    directional_states = [('Anisotropic, $F=I$', evaluate(anis,I,2.)),
        ('Anisotropic, finite shear',evaluate(anis,fstar,2.)),
        ('Isotropic, finite shear',evaluate(iso,fstar,2.))]
    directional = []
    fig = plt.figure(figsize=(7.2,3.6),layout='constrained')
    ax1 = fig.add_subplot(121,projection='polar'); ax2=fig.add_subplot(122)
    for number,(name,st) in enumerate(directional_states):
        n = np.column_stack([np.cos(angle), np.sin(angle), np.zeros_like(angle)])
        tangent = np.column_stack([-np.sin(angle),np.cos(angle),np.zeros_like(angle)])
        normal = np.einsum('ni,ij,nj->n',n,st['B'],n)
        shear_traction = np.einsum('ni,ij,nj->n',tangent,st['B'],n)
        color = COLORS[number] if number<2 else 'k'; style='-' if number<2 else '--'
        ax1.plot(angle,normal,style,color=color,label=name)
        ax2.plot(np.rad2deg(angle),shear_traction,style,color=color,label=name)
        directional.extend(dict(state=name,theta_deg=float(t),normal_coupling=float(b),
            tangential_coupling=float(bt)) for t,b,bt in zip(np.rad2deg(angle),normal,shear_traction))
    ax1.set(title=r'(a) Normal coupling $\mathbf{n}\cdot\mathbf{B}\mathbf{n}$',ylim=(0,1),yticks=[.25,.5,.75,1.])
    ax2.set(title='(b) Tangential pressure coupling',xlabel=r'Current direction $\theta$ [degrees]',
        ylabel=r'$\mathbf{t}\cdot\mathbf{B}\mathbf{n}$',xlim=(0,360),xticks=[0,90,180,270,360])
    ax2.grid(alpha=.2); ax2.legend(loc='upper center',bbox_to_anchor=(.5,-.22),fontsize=7)
    save(fig,'directional_response'); write_csv('directional_response.csv',directional)

    angles = np.linspace(0,np.pi,121)
    rotations = []
    fig,axes = plt.subplots(1,2,figsize=(7.2,2.8),constrained_layout=True)
    max_gauge_error = 0.; max_objectivity_error=0.
    reference = anis.state(fstar,2.)
    for mode in ('internal frame','physical rotation'):
        values = []
        for theta in angles:
            q=rotation_z(theta)
            st=evaluate(anis,fstar,2.,q) if mode=='internal frame' else evaluate(anis,q@fstar,2.)
            values.append(st)
            expected = reference['B'] if mode=='internal frame' else q@reference['B']@q.T
            error=float(np.linalg.norm(st['B']-expected))
            if mode=='internal frame':
                max_gauge_error=max(max_gauge_error,error,np.linalg.norm(st['sigma']-reference['sigma']),abs(st['W']-reference['W']))
            else:
                max_objectivity_error=max(max_objectivity_error,error,np.linalg.norm(st['sigma']-q@reference['sigma']@q.T),abs(st['W']-reference['W']))
            rotations.append(record(st,mode=mode,theta_deg=float(np.rad2deg(theta)),pressure=2.))
        for ax,(i,j) in zip(axes,[(0,0),(0,1)]):
            ax.plot(np.rad2deg(angles),[st['B'][i,j] for st in values],
                '--' if mode=='internal frame' else '-',label=mode.capitalize())
    for ax,title,ylabel in zip(axes,['(a) Normal component','(b) Off-diagonal component'],['$B_{11}$','$B_{12}$']):
        ax.set(title=title,xlabel='Rotation angle [degrees]',ylabel=ylabel,xlim=(0,180));ax.legend();ax.grid(alpha=.2)
    save(fig,'rotation_response');write_csv('rotation_response.csv',rotations)

    layer = {}; layer_records=[]
    for name,model in models:
        layer[name]=[]
        for p in pressures:
            def axial_residual(e):
                return model.state(np.diag([1.,1.,np.exp(e)]),p)['sigma'][2,2]
            e=brentq(axial_residual,-.2,.8,xtol=5e-15)
            st=evaluate(model,np.diag([1.,1.,np.exp(e)]),p)
            assert abs(st['sigma'][2,2]) < 2e-11
            layer[name].append((e,st))
            layer_records.append(record(st,material=name,pressure=p,axial_log_strain=e,axial_stretch=float(np.exp(e))))
    fig,axes=plt.subplots(1,3,figsize=(9.1,2.7),constrained_layout=True)
    for name,_ in models:
        style='-' if name=='anisotropic' else '--';color=COLORS[0] if name=='anisotropic' else 'k'
        axes[0].plot(pressures,[np.expm1(e) for e,_ in layer[name]],style,color=color,label=name.capitalize())
        axes[2].plot(pressures,[st['y'] for _,st in layer[name]],style,color=color,label=name.capitalize())
    for i,color in enumerate(COLORS[:2]):
        axes[1].plot(pressures,[st['sigma'][i,i] for _,st in layer['anisotropic']],color=color,label=fr'Anisotropic $\sigma_{{{i+1}{i+1}}}$')
    axes[1].plot(pressures,[st['sigma'][0,0] for _,st in layer['isotropic']], 'k--',label='Isotropic, both directions')
    for ax,title,ylabel in zip(axes,['(a) Axial expansion','(b) Lateral reaction stresses','(c) Mineral volume'],[r'$\lambda_3-1$',r'$\sigma_{ii}$ [stress unit]',r'$\bar J$']):
        ax.set(title=title,xlabel='$p$ [stress unit]',ylabel=ylabel);ax.legend();ax.grid(alpha=.2)
    save(fig,'constrained_layer');write_csv('constrained_layer.csv',layer_records)

    if (DEST/'verification.json').exists():
        verify=json.loads((DEST/'verification.json').read_text())
        write_csv('step_refinement.csv',verify['refinement'])
        fig,ax=plt.subplots(figsize=(4.2,3.1),constrained_layout=True)
        for name in ('energy_stress','pore_volume','pressure'):
            ax.loglog([row['step'] for row in verify['refinement']],
                [row[name] for row in verify['refinement']], 'o-',label=name.replace('_',' ').capitalize())
        ax.set(xlabel='Central-difference step',ylabel='Absolute Frobenius error',title='Second-order derivative refinement')
        ax.legend();ax.grid(alpha=.2,which='both');save(fig,'step_refinement')
    assert max(abs(st['residual']) for st in all_states) < 2e-11
    assert max_gauge_error < 2e-10 and max_objectivity_error < 2e-10
    metadata=dict(units='All moduli, stresses, energies per reference volume, and pressure share one arbitrary stress unit; remaining quantities dimensionless.',
        phi_s0=anis.phi,K=anis.k,Ks=anis.ks,alpha=anis.alpha,Ka=anis.ka,
        mineral_Mandel_stiffness=anis.cs.tolist(),drained_Mandel_stiffness=anis.cd.tolist(),
        Mandel_order=['11','22','33','sqrt(2)23','sqrt(2)13','sqrt(2)12'],
        isotropic_comparison=dict(Ks=iso.ks,mu=anis.mu_average,cs=iso.cs.tolist(),
            condition='Same mineral spherical-strain modulus and mean deviatoric stiffness; same K and reference solid fraction.'),
        loading=dict(pressure='F=I, p=0..6, 121 points',
            shear='F=[[exp(.12),gamma,0],[0,exp(-.04),0],[0,0,exp(-.08)]], gamma=-.8.. .8, 161 points, p=2, J=1',
            directional='p=2; F=I or shear F at gamma=.65; n=(cos(theta),sin(theta),0), t=(-sin(theta),cos(theta),0), theta=0..360 deg',
            rotation='shear F at gamma=.65, p=2; R_A=Rz(theta) at fixed F or F=Rz(theta)Fstar at R_A=I, theta=0..180 deg, 121 points',
            layer='F=diag(1,1,exp(e3)); sigma33=0; p=0..6,121 points; homogeneous laterally constrained elastic layer'),
        state_evaluations=len(all_states),max_mineral_residual=max(abs(st['residual']) for st in all_states),
        solid_fraction_range=[min(st['solid_fraction'] for st in all_states),max(st['solid_fraction'] for st in all_states)],
        min_scalar_stability=min(st['stability'] for st in all_states),max_internal_rotation_error=float(max_gauge_error),
        max_physical_rotation_error=float(max_objectivity_error),
        highlights=dict(reference_B=np.diag(pressure['anisotropic'][0]['B']).tolist(),
            pressure6_B=np.diag(pressure['anisotropic'][-1]['B']).tolist(),
            pressure6_mineral_volume=pressure['anisotropic'][-1]['y'],
            shear065_B=reference['B'].tolist(),shear065_mineral_volume=reference['y'],
            layer6={name:dict(e3=values[-1][0],axial_expansion=float(np.expm1(values[-1][0])),
                sigma11=float(values[-1][1]['sigma'][0,0]),sigma22=float(values[-1][1]['sigma'][1,1]),
                mineral_volume=values[-1][1]['y']) for name,values in layer.items()}),
        versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__),
        source_sha256={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                       for name in ('conformal_model.py','conformal_experiments.py','figure_style.py')},
        scope='Synthetic homogeneous constitutive calculations. No finite-element solve, measured material calibration, or physical validation.')
    (DEST/'experiments.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({key:metadata[key] for key in ('state_evaluations','max_mineral_residual',
        'solid_fraction_range','max_internal_rotation_error','max_physical_rotation_error','highlights')},indent=2))


if __name__=='__main__':
    main()
