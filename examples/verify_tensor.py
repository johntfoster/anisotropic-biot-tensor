#!/usr/bin/env python3
"""Independent full spatial stress, energy, and pressure checks.

Uses NumPy/SciPy; results go to build/weighted-stress. The phase stress is
computed from the true mineral deformation, separately from the derivative
of the mixture pressure potential.
"""
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm
from scipy.optimize import brentq
import weighted_stress as data

I=np.eye(3)
BASIS=[np.diag(I[i]) for i in range(3)]
for i,j in ((1,2),(0,2),(0,1)):
    x=np.zeros((3,3));x[i,j]=x[j,i]=1/np.sqrt(2);BASIS.append(x)
BASIS=np.array(BASIS)
ONE=np.array([1.,1.,1.,0.,0.,0.])
DEFAULT_CS=np.zeros((6,6));DEFAULT_CS[:3,:3]=data.CS
DEFAULT_CS[3:,3:]=np.diag(data.SHEAR)


def vec(x):return np.einsum('aij,ij->a',BASIS,x)
def mat(x):return np.einsum('a,aij->ij',x,BASIS)


def logarithm(F):
    vals,Q=np.linalg.eigh(F.T@F)
    if min(vals)<=0 or np.linalg.det(F)<=0:raise ValueError('Nonpositive deformation')
    return (Q*(np.log(vals)/2))@Q.T


def push(F,T):
    vals,Q=np.linalg.eigh(F.T@F);d=np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            # Continuous limit avoids cancellation at repeated eigenvalues.
            if abs(vals[i]-vals[j])<1e-8*max(vals[i],vals[j]):d[i,j]=2/(vals[i]+vals[j])
            else:d[i,j]=(np.log(vals[i])-np.log(vals[j]))/(vals[i]-vals[j])
    return F@Q@(d*(Q.T@T@Q))@Q.T@F.T


def parameters(cs=DEFAULT_CS,phi=data.PHI,k=data.K):
    ks=ONE@cs@ONE/9
    if not (0<phi<1 and 0<k<phi*ks):raise ValueError('Invalid fractions or spherical stiffness')
    if min(np.linalg.eigvalsh(cs))<=0:raise ValueError('Nonpositive mineral stiffness')
    ka=k/(1-k/(phi*ks));h=ka+phi*ks
    cd=phi*cs-phi**2*np.outer(cs@ONE,cs@ONE)/(9*h)
    return ks,ka,h,cd


def compute(F,p,cs=DEFAULT_CS,phi=data.PHI,k=data.K):
    ks,ka,h,cd=parameters(cs,phi,k)
    e=vec(logarithm(F));t=ONE@e;J=np.linalg.det(F)
    r=ONE-phi*(cs@ONE)/(3*h)
    target=r@e
    q=brentq(lambda q:h*(q-target)+phi*p*np.exp(q),target-1,target+1,xtol=5e-15)
    y=np.exp(q);a=J/y;eb=e-np.log(a)*ONE/3
    Fbar=a**(-1/3)*F
    mineral_tau=push(Fbar,mat(cs@eb))
    mineral_sigma=mineral_tau/y
    solid_fraction=phi*y/J
    sigma=solid_fraction*mineral_sigma-(1-solid_fraction)*p*I
    W=ka*np.log(a)**2/2+phi*eb@cs@eb/2
    V=W+phi*p*y-p*J
    B=I-phi*y/(J*(1+phi*p*y/h))*push(F,mat(r))
    P=J*sigma@np.linalg.inv(F).T
    return dict(V=V,W=W,sigma=sigma,P=P,B=B,q=q,y=y,Fbar=Fbar,
                mineral_sigma=mineral_sigma,solid_fraction=solid_fraction,cd=cd)


def main():
    rng=np.random.default_rng(20260919)
    errors={name:0. for name in ('phase_energy','pressure','volume_gradient','rotation','symmetry','diagonal','trace','shape')}
    states=[(expm(np.diag([0.,0.,e])),p) for e in (-.2,0.,.2) for p in (0.,.5,2.)]
    states += [(expm(mat(rng.normal(size=6)*.09)),rng.uniform(0.,2.)) for _ in range(12)]
    materials=[(DEFAULT_CS,data.PHI,data.K)]
    for _ in range(12):
        X=rng.normal(size=(6,6));cs=X.T@X+15*np.eye(6)
        phi=rng.uniform(.45,.7);ks=ONE@cs@ONE/9;k=phi*ks*rng.uniform(.25,.6)
        materials.append((cs,phi,k))
    step=2e-6;noncommuting=0.;count=0
    for cs,phi,k in materials:
        for F,p in states:
            value=compute(F,p,cs,phi,k);count+=1
            assert 0<value['solid_fraction']<1
            grad=np.zeros((3,3));dv=np.zeros((3,3))
            for i in range(3):
                for j in range(3):
                    dF=np.zeros((3,3));dF[i,j]=step
                    plus=compute(F+dF,p,cs,phi,k);minus=compute(F-dF,p,cs,phi,k)
                    grad[i,j]=(plus['V']-minus['V'])/(2*step)
                    dv[i,j]=(plus['y']-minus['y'])/(2*step)
            energy_stress=grad@F.T/np.linalg.det(F)
            errors['phase_energy']=max(errors['phase_energy'],np.max(abs(value['sigma']-energy_stress)))
            errors['volume_gradient']=max(errors['volume_gradient'],np.max(abs(value['B']-(I-phi*dv@F.T/np.linalg.det(F)))))
            ds=(compute(F,p+step,cs,phi,k)['sigma']-compute(F,p-step,cs,phi,k)['sigma'])/(2*step)
            errors['pressure']=max(errors['pressure'],np.max(abs(ds+value['B'])))
            omega=rng.normal(size=(3,3));Q=expm(omega-omega.T)
            rot=compute(Q@F,p,cs,phi,k)
            errors['rotation']=max(errors['rotation'],abs(rot['V']-value['V']),np.max(abs(rot['sigma']-Q@value['sigma']@Q.T)),np.max(abs(rot['B']-Q@value['B']@Q.T)))
            errors['symmetry']=max(errors['symmetry'],np.max(abs(value['B']-value['B'].T)))
            E=logarithm(F);T=mat(cs@vec(logarithm(value['Fbar'])))
            noncommuting=max(noncommuting,np.linalg.norm(E@T-T@E))
            errors['trace']=max(errors['trace'],abs(np.trace(push(value['Fbar'],T))-np.trace(T)))
            errors['shape']=max(errors['shape'],np.max(abs(value['Fbar']/value['y']**(1/3)-F/np.linalg.det(F)**(1/3))))
    for e in (-.2,0.,.2):
        for p in (0.,.5,2.):
            val=compute(np.diag(np.exp([0.,0.,e])),p);ref=data.state([0.,0.,e],p)
            errors['diagonal']=max(errors['diagonal'],np.max(abs(np.diag(val['sigma'])-ref['sigma'])),np.max(abs(np.diag(val['B'])-ref['B'])),abs(val['y']-ref['mineral_volume']))
    assert all(x<2e-6 for x in errors.values()),errors
    assert noncommuting>1e-3,'States must exercise differing stress/strain directions'
    report=dict(errors=errors,materials=len(materials),states_per_material=len(states),total_states=count,
                maximum_stress_strain_commutator=noncommuting,seed=20260919,
                versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    dest=Path('build/weighted-stress');dest.mkdir(parents=True,exist_ok=True)
    (dest/'tensor-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
