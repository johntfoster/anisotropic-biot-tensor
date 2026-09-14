#!/usr/bin/env python3
"""Independent tensor and finite-difference checks for finite_pressure.py.

Run with NumPy and SciPy installed. All diagnostics go to build/examples/.
"""
import json
import platform
import numpy as np
import scipy
from scipy.linalg import expm
import finite_pressure as model

I = np.eye(3)
BASIS = [np.diag(I[i]) for i in range(3)]
for i,j in ((1,2),(0,2),(0,1)):
    x = np.zeros((3,3)); x[i,j] = x[j,i] = 1/np.sqrt(2)
    BASIS.append(x)
BASIS = np.array(BASIS)
CD = np.zeros((6,6)); CD[:3,:3] = model.CD
CD[3:,3:] = np.diag([6.,6.,8.])
r = np.array([*model.R,0,0,0])
phi,h = model.PHI,model.H


def vec(x): return np.einsum('aij,ij->a',BASIS,x)
def mat(x): return np.einsum('a,aij->ij',x,BASIS)


def evaluate(F,p,law="log",cd=CD,rr=r,hh=h):
    vals,U = np.linalg.eigh(F.T@F)
    logvals = np.log(vals)
    eps = (U*(logvals/2))@U.T
    v = vec(eps)
    req = rr@v
    if law == "volume":
        q=np.log(np.exp(req)-phi*p/hh)
    else:
        q = req if p == 0 else model.root(lambda q: hh*(q-req)+phi*p*np.exp(q), req-5,req)
    J = np.linalg.det(F)
    z = phi*p*np.exp(q)/hh
    divided = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            divided[i,j] = 2/(vals[i]+vals[j]) if abs(vals[i]-vals[j]) < 1e-10 else (logvals[i]-logvals[j])/(vals[i]-vals[j])
    def L(x): return U@(divided*(U.T@x@U))@U.T
    grad = mat(cd@v+hh*(req-q)*rr)
    if law == "volume":
        grad=mat(cd@v+phi*p*np.exp(req)*rr)
    P = F@L(grad)-p*J*np.linalg.inv(F).T
    sigma = P@F.T/J
    B = I-phi*np.exp(q)/(J*(1+z)) * F@L(mat(rr))@F.T
    V = 0.5*v@cd@v+0.5*hh*(q-req)**2+phi*p*np.exp(q)-p*J
    if law == "volume":
        B=I-phi*np.exp(req)/J*F@L(mat(rr))@F.T
        V=.5*v@cd@v+.5*hh*(np.exp(q)-np.exp(req))**2+phi*p*np.exp(q)-p*J
    return V,P,sigma,B,q


def main():
    rng = np.random.default_rng(87134)
    errors = {k:0. for k in ('pressure','volume','potential','rotation','symmetry','quadratic','unjacketed','diagonal')}
    # Arbitrary daughter tensors: directly compare the two energy evaluations.
    one=np.array([1,1,1,0,0,0.]); dev=np.eye(6)-np.outer(one,one)/3
    for _ in range(30):
        X=rng.normal(size=(6,6)); mineral=X.T@X+np.eye(6)
        D=rng.normal(size=(6,6)); C=np.eye(6)*20
        e=rng.normal(size=6); q=rng.normal()
        eta=dev@e+q*one/3
        cc=C+D@dev+dev@D.T+dev@mineral@dev
        g=(D@one+dev@mineral@one)/3
        hh=one@mineral@one/9
        original=.5*e@C@e+e@D@eta+.5*eta@mineral@eta
        reduced=.5*e@cc@e+q*g@e+.5*hh*q*q
        errors['quadratic']=max(errors['quadratic'],abs(original-reduced))
    # Noncoaxial states and repeated principal stretches test the log derivative.
    states=[(np.diag(np.exp([0,0,s])),p) for s in (-.2,0,.2) for p in (0.,.2,1.,2.)]
    states += [(np.diag([1,1,np.exp(model.layer(p)[0])]),p) for p in (0.,.2,1.,2.)]
    for _ in range(12):
        E=rng.normal(size=(3,3))*.08
        states.append((expm((E+E.T)/2),rng.uniform(.1,2)))
    delta=2e-6
    for F,p in states:
        V,P,sigma,B,q=evaluate(F,p)
        # At p=0 use a forward second-order pressure derivative (no negative-p branch).
        if p==0:
            ds=(-3*sigma+4*evaluate(F,delta)[2]-evaluate(F,2*delta)[2])/(2*delta)
        else:
            ds=(evaluate(F,p+delta)[2]-evaluate(F,p-delta)[2])/(2*delta)
        errors['pressure']=max(errors['pressure'],np.max(np.abs(ds+B)))
        dbar=np.zeros((3,3)); dV=np.zeros((3,3))
        for i in range(3):
            for j in range(3):
                E=np.zeros((3,3)); E[i,j]=delta
                plus,minus=evaluate(F+E,p),evaluate(F-E,p)
                dbar[i,j]=(np.exp(plus[4])-np.exp(minus[4]))/(2*delta)
                dV[i,j]=(plus[0]-minus[0])/(2*delta)
        errors['volume']=max(errors['volume'],np.max(np.abs(B-(I-phi/np.linalg.det(F)*dbar@F.T))))
        errors['potential']=max(errors['potential'],np.max(np.abs(P-dV)))
        omega=rng.normal(size=(3,3)); Q=expm(omega-omega.T)
        rotated=evaluate(Q@F,p)
        errors['rotation']=max(errors['rotation'],np.max(np.abs(rotated[3]-Q@B@Q.T)),abs(V-rotated[0]))
        errors['symmetry']=max(errors['symmetry'],np.max(np.abs(B-B.T)))
        if np.max(abs(F-np.diag(np.diag(F))))<1e-12:
            st=model.state(np.log(np.diag(F)),p)
            errors['diagonal']=max(errors['diagonal'],np.max(abs(np.diag(sigma)-st['sigma'])),np.max(abs(np.diag(B)-st['B'])))
    # Both unjacketed conditions, independently of finite-pressure energy evaluation.
    a=one/(3*model.KS); g=-h*r; b=one+phi*g/h
    errors['unjacketed']=max(np.max(abs(b-(one-CD@a))),abs(g@a+h*sum(a[:3])-phi))
    # Acoustic tensor checks of the condensed total potential, not just W_H convexity.
    directions=rng.normal(size=(100,3)); directions/=np.linalg.norm(directions,axis=1)[:,None]
    directions=np.vstack((I,directions))
    minimum=1e20
    for F,p in states:
        A=np.zeros((3,3,3,3))
        for j in range(3):
            for b in range(3):
                E=np.zeros((3,3)); E[j,b]=delta
                A[:,:,j,b]=(evaluate(F+E,p)[1]-evaluate(F-E,p)[1])/(2*delta)
        for n in directions:
            acoustic=np.einsum('iajb,a,b->ij',A,n,n)
            minimum=min(minimum,np.linalg.eigvalsh((acoustic+acoustic.T)/2)[0])
    assert all(v<2e-6 for v in errors.values()),errors
    assert minimum>0,minimum
    # Compatible anisotropic-mineral reconstruction, including the daughter tensors.
    T=np.array([-1,-1,2,0,0,0])/np.sqrt(6); vv=one/np.sqrt(3)
    compatible=[]
    for c,beta in ((0.,6.),(6.,6.),(6.,18.)):
        mineral=45*np.outer(vv,vv)+12*dev+beta*np.outer(T,T)+c*(np.outer(vv,T)+np.outer(T,vv))
        a=phi*np.linalg.solve(mineral,one)
        hh=phi**2/(phi*sum(a[:3])-a@CD@a)
        gg=-hh/phi*CD@a
        target=3*gg-dev@mineral@one
        D=np.outer(target,one)/3-dev@mineral@dev/2
        C=CD+np.outer(gg,gg)/hh
        cc=C+D@dev+dev@D.T+dev@mineral@dev
        assert np.allclose(cc-np.outer(gg,gg)/hh,CD)
        assert np.allclose((D@one+dev@mineral@one)/3,gg)
        assert abs(gg@a+hh*sum(a[:3])-phi)<1e-13
        assert np.linalg.eigvalsh(mineral)[0]>0 and hh>0
        minimum_phi=1.
        for ss in (-.2,0,.2):
            for pp in (0.,.2,2.):
                F=np.diag(np.exp([0,0,ss]))
                q=evaluate(F,pp,rr=-gg/hh,hh=hh)[4]
                pore=1-phi*np.exp(q)/np.linalg.det(F)
                assert 0<pore<1
                minimum_phi=min(minimum_phi,pore)
        compatible.append(dict(c=c,beta=beta,h=hh,kappa=hh-15,minimum_sampled_porosity=minimum_phi))
    # Verify the alternative hyperelastic continuation against pressure/potential differences.
    alt_error=0.; alt_minimum=1e20; min_record=None
    for F,p in states:
        V,P,sigma,B,q=evaluate(F,p,law="volume")
        ds=(evaluate(F,p+delta,law="volume")[2]-evaluate(F,p-delta,law="volume")[2])/(2*delta)
        alt_error=max(alt_error,np.max(abs(ds+B)))
        A=np.zeros((3,3,3,3))
        for j in range(3):
            for b in range(3):
                E=np.zeros((3,3)); E[j,b]=delta
                plus,minus=evaluate(F+E,p,law="volume"),evaluate(F-E,p,law="volume")
                alt_error=max(alt_error,abs((plus[0]-minus[0])/(2*delta)-P[j,b]))
                A[:,:,j,b]=(plus[1]-minus[1])/(2*delta)
        for n in directions:
            acoustic=np.einsum('iajb,a,b->ij',A,n,n)
            value=np.linalg.eigvalsh((acoustic+acoustic.T)/2)[0]
            if value<alt_minimum:
                alt_minimum=value; min_record=dict(F=F.tolist(),p=p,direction=n.tolist())
    assert alt_error<2e-6 and alt_minimum>0
    pp=1e-5
    slope_s,_,reaction=model.layer(pp)
    assert abs(slope_s/pp-model.B0[2]/model.CD[2][2])<2e-6
    assert abs(reaction/pp-(model.CD[0][2]*model.B0[2]/model.CD[2][2]-model.B0[0]))<2e-6
    report=dict(max_absolute_errors=errors,minimum_sampled_acoustic_eigenvalue=minimum,
                states=len(states),directions_per_state=len(directions),seed=87134,
                compatible_minerals=compatible,
                volume_law_max_error=alt_error,volume_law_minimum_acoustic=alt_minimum,
                volume_law_minimum_state=min_record,
                versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                scope='Sampled local checks, not a proof of global rank-one convexity.')
    model.write(model.OUT/'verification.json',json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
