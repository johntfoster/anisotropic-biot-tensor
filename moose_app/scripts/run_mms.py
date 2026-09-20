#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import tempfile,json,re
from concurrent.futures import ThreadPoolExecutor
from decks import ROOT,make,section
from run_case import run_input
import numpy as np
REF=ROOT/'.agent-runtime/moose-fe-goal-2026-09-20/reference'
def replace(text,section_name,new):
    return re.sub(r'^\['+section_name+r'\]\n.*?^\[\]\n',new,text,flags=re.M|re.S)
def mms(name,n,dt,end):
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'input.i';make(path,nx=n,ny=n,dt=dt,end=end,linear=True,case='anisotropic',angle=30);text=path.read_text()
    text=replace(text,'Mesh',section('Mesh',{'base':dict(type='GeneratedMeshGenerator',dim=2,nx=n,ny=n,xmin=0,xmax=1,ymin=0,ymax=1,elem_type='QUAD9')}))
    text=replace(text,'Functions',(REF/'mms-functions.i').read_text())
    text=replace(text,'ICs',section('ICs',{v:dict(type='ConstantIC',variable=v,value=0) for v in ['ux','uy','p']}))
    text=replace(text,'BCs',section('BCs',{v:dict(type='FunctionDirichletBC',variable=v,boundary="'left right top bottom'",function='exact_'+v) for v in ['ux','uy','p']}))
    text=replace(text,'Constraints','')
    kernels={'mx':dict(type='ReferenceMomentum',variable='ux',component=0),'my':dict(type='ReferenceMomentum',variable='uy',component=1),'mass':dict(type='ReferenceFluidMass',variable='p')}
    for v,f in [('ux','body_x'),('uy','body_y'),('p','mass_source')]:kernels['source_'+v]=dict(type='BodyForce',variable=v,function=f)
    text=replace(text,'Kernels',section('Kernels',kernels))
    text=replace(text,'Postprocessors',section('Postprocessors',{v+'_l2':dict(type='ElementL2Error',variable=v,function='exact_'+v,execute_on="'INITIAL TIMESTEP_END'") for v in ['ux','uy','p']}))
    text=replace(text,'VectorPostprocessors','')
    text=text.replace('solve_type = PJFNK','solve_type = NEWTON')
    out=run_input(name,text,dict(case='manufactured',nx=n,ny=n,dt=dt,end=end,linear=True,angle=30))
    data=np.genfromtxt(out/'solution.csv',delimiter=',',names=True)[-1];report={v+'_l2':float(data[v+'_l2']) for v in ['ux','uy','p']};report.update(nx=n,dt=dt,end=end)
    (out/'analysis.json').write_text(json.dumps(report,indent=2)+'\n');print(name,report,flush=True)
    return report
if __name__=='__main__':
    jobs=[(f'mms_space_{n}',n,.0001,.01) for n in [4,8,16]]+[(f'mms_time_{dt:g}',16,dt,.2) for dt in [.02,.01,.005]]
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda x:mms(*x),jobs))
