#!/usr/bin/env python3
"""Check work equivalence, drained compatibility, scalar and unjacketed limits."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize_scalar,brentq
from verify_tensor import I,ONE,vec,mat,logarithm,push,parameters,compute,DEFAULT_CS


def main():
    rng=np.random.default_rng(20260920);errors={name:0. for name in
        ('compliance','drained_energy','drained_hooke','minimization','work_equivalence','unjacketed','reference_biot','reference_storage','isotropic_eos','isotropic_biot')}
    minimum=1e6;reject=0
    for _ in range(20):
        X=rng.normal(size=(6,6));cs=X.T@X+12*np.eye(6);phi=rng.uniform(.45,.7)
        ks=ONE@cs@ONE/9;k=rng.uniform(.2,.65)*phi*ks;ks,ka,h,cd=parameters(cs,phi,k)
        extra=np.linalg.inv(cd)-np.linalg.inv(phi*cs)
        expected=np.outer(ONE,ONE)/(9*ka)
        errors['compliance']=max(errors['compliance'],np.max(abs(extra-expected)))
        minimum=min(minimum,min(np.linalg.eigvalsh(cd)))
        wrong=cd+np.diag([0,0,0,.1,.2,.3])
        reject+=int(np.linalg.norm(np.linalg.inv(wrong)-np.linalg.inv(phi*cs)-expected)>1e-5)
        for __ in range(5):
            e=rng.normal(size=6)*.08;F=expm(mat(e));t=ONE@e
            zero=compute(F,0.,cs,phi,k);eb=vec(logarithm(zero['Fbar']))
            errors['drained_energy']=max(errors['drained_energy'],abs(zero['W']-.5*e@cd@e))
            errors['drained_hooke']=max(errors['drained_hooke'],np.max(abs(phi*cs@eb-cd@e)))
            p=.3;value=compute(F,p,cs,phi,k)
            def objective(q):
                eb=e-(t-q)*ONE/3
                return ka*(t-q)**2/2+phi/2*eb@cs@eb+phi*p*np.exp(q)
            m=minimize_scalar(objective,bracket=(value['q']-.1,value['q'],value['q']+.1),method='brent',options={'xtol':1e-12})
            errors['minimization']=max(errors['minimization'],abs(m.x-value['q']))
            # Arbitrary joint virtual change of distention and true mineral F.
            a=np.linalg.det(F)/value['y'];Fb=value['Fbar'];dFb=rng.normal(size=(3,3));dl=.3;step=1e-6
            def energy(l,Fb):
                eb=vec(logarithm(Fb));return ka*l*l/2+phi*eb@cs@eb/2
            numeric=(energy(np.log(a)+step*dl,Fb+step*dFb)-energy(np.log(a)-step*dl,Fb-step*dFb))/(2*step)
            taumin=value['y']*value['mineral_sigma'];tauprime=phi*(taumin+p*value['y']*I)
            work=np.trace(tauprime)/3*dl+phi*np.sum(taumin*(dFb@np.linalg.inv(Fb)))
            errors['work_equivalence']=max(errors['work_equivalence'],abs(numeric-work))
        hydro=np.linalg.solve(cs,ONE)
        for p in (.01,.2):
            q=brentq(lambda q:q+p*np.exp(q)*sum(hydro[:3]),-2,0)
            e=-p*np.exp(q)*hydro;F=expm(mat(e));v=compute(F,p,cs,phi,k)
            errors['unjacketed']=max(errors['unjacketed'],abs(v['y']-np.linalg.det(F)),np.max(abs(v['sigma']+p*I)),np.max(abs(v['mineral_sigma']+p*I)),abs(v['solid_fraction']-phi))
        zero=compute(I,0.,cs,phi,k)
        errors['reference_biot']=max(errors['reference_biot'],np.max(abs(zero['B']-mat(ONE-cd@hydro))))
        dp=1e-5;num=-phi*(compute(I,dp,cs,phi,k)['y']-compute(I,-dp,cs,phi,k)['y'])/(2*dp)
        expected=phi*sum(hydro[:3])-hydro@cd@hydro
        errors['reference_storage']=max(errors['reference_storage'],abs(num-expected))
    dev=np.eye(6)-np.outer(ONE,ONE)/3
    cs=28*np.outer(ONE,ONE)+24*dev;phi=.6;k=7
    for t in (-.2,0.,.2):
        for p in (0.,.5,2.):
            F=np.diag(np.exp([0.,0.,t]));v=compute(F,p,cs,phi,k);q=v['q'];y=v['y'];d=1-k/(phi*28)
            errors['isotropic_eos']=max(errors['isotropic_eos'],abs(28*q+d*p*y-k*t/phi))
            expected=(1-k*y/(np.exp(t)*(28+d*p*y)))*I
            errors['isotropic_biot']=max(errors['isotropic_biot'],np.max(abs(v['B']-expected)))
    assert reject==20
    assert all(x<2e-6 for x in errors.values()),errors
    assert minimum>0
    report=dict(errors=errors,seed=20260920,materials=20,incompatible_pairs_rejected=reject,minimum_drained_eigenvalue=minimum)
    dest=Path('build/weighted-stress');dest.mkdir(parents=True,exist_ok=True)
    (dest/'reconstruction-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
