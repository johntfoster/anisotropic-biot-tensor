#!/usr/bin/env python3
"""Spherical-distention model: generate diagonal-state manuscript data.

All moduli and pressures use a common arbitrary stress unit. Only the Python
standard library is needed for tables. Full tensor tests are separate.
"""
from pathlib import Path
import json
import math

PHI = 0.6
K = 7.0
CS = [[50.,12.,10.],[12.,60.,14.],[10.,14.,70.]]
SHEAR = [20.,24.,28.]  # Mandel shear entries, ordered yz, xz, xy.
KS = sum(map(sum, CS))/9
KA = K/(1-K/(PHI*KS))
H = KA+PHI*KS
ROW = list(map(sum, CS))
R = [1-PHI*x/(3*H) for x in ROW]
CD = [[PHI*CS[i][j]-PHI**2*ROW[i]*ROW[j]/(9*H) for j in range(3)] for i in range(3)]


def root(f,lo,hi):
    flo,fhi=f(lo),f(hi)
    if flo*fhi>0: raise ValueError('Root is not bracketed')
    for _ in range(100):
        mid=(lo+hi)/2; fm=f(mid)
        if abs(fm)<1e-14:return mid
        if flo*fm<=0:hi=mid
        else:lo=mid;flo=fm
    return (lo+hi)/2


def state(e,p):
    t=sum(e); target=sum(x*y for x,y in zip(R,e))
    q=root(lambda q:H*(q-target)+PHI*p*math.exp(q),target-2,target+2)
    y=math.exp(q);J=math.exp(t);ps=PHI*y/J
    eb=[x-(t-q)/3 for x in e]
    ts=[sum(CS[i][j]*eb[j] for j in range(3)) for i in range(3)]
    stress=[PHI*x/J-(1-ps)*p for x in ts]
    B=[1-PHI*y*x/(J*(1+PHI*p*y/H)) for x in R]
    W=KA*(t-q)**2/2+PHI*sum(x*y for x,y in zip(eb,ts))/2
    return dict(J=J,mineral_volume=y,solid_fraction=ps,q=q,sigma=stress,B=B,W=W)


def layer(p):
    if p == 0:
        return 0.,state([0.,0.,0.],0.)
    ez=root(lambda e:state([0,0,e],p)['sigma'][2],-.3,.6)
    return ez,state([0,0,ez],p)


def main():
    dest=Path('build/weighted-stress');dest.mkdir(parents=True,exist_ok=True)
    records=[]
    for e in ([0.,0.,0.],[0.,0.,-.2],[0.,0.,.2]):
        for p in (0.,.5,2.):
            v=state(e,p);records.append(dict(e=e,p=p,**v))
    rows=[]
    for row in records:
        rows.append(' & '.join(f'{x:.4f}' for x in [row['e'][2],row['p'],row['mineral_volume'],*row['B']])+r' \\')
    (dest/'states.tex').write_text('\n'.join(rows)+'\n')
    rows=[]
    for p in (0.,.5,1.,2.):
        e,v=layer(p)
        rows.append(' & '.join(f'{x:.5f}' for x in [p,e,v['sigma'][0],v['sigma'][1],v['mineral_volume']])+r' \\')
    (dest/'layer.tex').write_text('\n'.join(rows)+'\n')
    lines=['p B11 B22 B33']
    for i in range(101):
        p=i*.02;v=state([0.,0.,0.],p)
        lines.append(' '.join(str(x) for x in [p,*v['B']]))
    (dest/'pressure.dat').write_text('\n'.join(lines)+'\n')
    (dest/'results.json').write_text(json.dumps(dict(phi=PHI,K=K,Ks=KS,Ka=KA,mineral=CS,drained=CD,states=records),indent=2)+'\n')
    print('Generated diagonal-state data in',dest)

if __name__=='__main__':main()
