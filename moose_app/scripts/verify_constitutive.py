#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent NumPy spectral oracle versus the compiled C++ AD law."""
from pathlib import Path
import sys,subprocess,io,json
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'examples'))
from conformal_model import Model,shear_gradient,rotation_z
OUT=ROOT/'.agent-runtime/moose-fe-goal-2026-09-20/implementation/constitutive'
OUT.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(415)
states=[(np.eye(3)*v,p) for v in [.7,1.,1.3] for p in [0,2,6]]
states += [(shear_gradient(g),p) for g in [-.8,-.2,0,.4,.8] for p in [-3,0,6]]
for n in range(20):
    f=np.eye(3)+rng.normal(scale=.12,size=(3,3));states.append((f,float(rng.uniform(-2,6))))
valid=[]
for f,p in states:
    try: Model().state(f,p);valid.append((f,p))
    except ValueError: pass
rejected=len(states)-len(valid);states=valid
np.savetxt(OUT/'states.txt',np.array([np.r_[f.ravel(),p] for f,p in states]))
exe=ROOT/'moose_app/anisotropic_biot-opt'
def run(order):
    proc=subprocess.run([str(exe),'--constitutive-table',str(OUT/'states.txt'),str(order)],capture_output=True,text=True,check=True)
    return np.loadtxt(io.StringIO(proc.stdout))
def oracle(f,p):
    s=Model().state(f,p);return np.r_[s['J'],s['y'],np.exp(p/8)*(s['J']-.6*s['y']),s['W'],s['stability'],s['solid_fraction'],s['sigma'].ravel(),s['B'].ravel(),(s['J']*s['sigma']@np.linalg.inv(f).T).ravel()]
a=run(24);ref=np.array([oracle(f,p) for f,p in states]);value_error=float(np.max(abs(a[:,:33]-ref)))
der=a[:,33:].reshape(-1,33,10)
steps=[1e-4,5e-5,2.5e-5,1e-5]
errors=[]
for step in steps:
    err=0
    for n,(f,p) in enumerate(states):
        for j in range(10):
            fp=f.copy();fm=f.copy();pp=p;pm=p
            if j<9:fp.flat[j]+=step;fm.flat[j]-=step
            else:pp+=step;pm-=step
            fd=(oracle(fp,pp)-oracle(fm,pm))/(2*step)
            inds=list(range(33))
            err=max(err,float(np.max(abs(fd[inds]-der[n,inds,j]))))
    errors.append(err)
orders={str(order):float(np.max(abs(run(order)[:,:33]-ref))) for order in [8,12,16,24,32]}
report=dict(states=len(states), inadmissible_states_excluded=rejected,value_absolute_error=value_error,jacobian_step_sizes=steps,jacobian_absolute_errors=errors,quadrature_order_errors=orders,metric_eigenvalue_range=[min(np.linalg.eigvalsh(f.T@f).min() for f,p in states),max(np.linalg.eigvalsh(f.T@f).max() for f,p in states)],pass_values=value_error<1e-8,pass_derivatives=errors[-1]<1e-6)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert report['pass_values'] and report['pass_derivatives']
