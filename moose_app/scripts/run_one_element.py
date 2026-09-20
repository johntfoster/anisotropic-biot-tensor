#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import tempfile,re,json
from decks import ROOT,make,section,initial_mandel
from run_case import run_input
import numpy as np
from scipy.optimize import root
import sys
sys.path.insert(0,str(ROOT/'examples'))
from conformal_model import Model,isotropic_stiffness

def replace(text,name,new):return re.sub(r'^\['+name+r'\]\n.*?^\[\]\n',new,text,flags=re.M|re.S)
for mode in ['drained','undrained']:
    q=.01
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'input.i';make(path,nx=1,ny=1,dt=.01,end=.01,load=q);text=path.read_text()
    text=replace(text,'ICs',section('ICs',{v:dict(type='ConstantIC',variable=v,value=0) for v in ['ux','uy','p']}))
    if mode=='undrained':
        text=re.sub(r'  \[pressure\]\n.*?  \[\]\n','',text,flags=re.S);text=text.replace('mobility = 1.5','mobility = 0')
        ex,ey,p=initial_mandel(q,False)
    else:
        text=text.replace("boundary = 'right'","boundary = 'left right top bottom'")
        model=Model(isotropic_stiffness(2.5,5/6),.9,1)
        def res(z):
            f=np.diag([1+z[0],1+z[1],1]);s=model.state(f,0);P=s['J']*s['sigma']@np.linalg.inv(f).T;return [P[0,0],P[1,1]+q]
        sol=root(res,[.002,-.005],tol=1e-11);ex,ey=sol.x;p=0
    out=run_input('one_element_'+mode,text,dict(case=mode,load=q))
    data=np.genfromtxt(out/'solution.csv',delimiter=',',names=True);final=data[-1]
    report=dict(expected=dict(edge_ux=ex,platen=.1*ey,p=p),actual=dict(edge_ux=float(final['edge_ux']),platen=float(final['platen_min']),p=float(final['center_pressure'])),mass_change=float(final['mass']-data[0]['mass']))
    report['absolute_error']=max(abs(report['expected'][k]-report['actual'][k]) for k in report['expected']);report['pass']=report['absolute_error']<1e-8 and (mode=='drained' or abs(report['mass_change'])<1e-10)
    (out/'analysis.json').write_text(json.dumps(report,indent=2)+'\n');print(mode,report,flush=True)
    assert report['pass']
