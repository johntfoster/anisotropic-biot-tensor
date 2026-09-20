#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build reproducible Q2/Q1, total-Lagrangian input decks."""
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import root
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'examples'))
from conformal_model import Model,isotropic_stiffness,DEFAULT_CS

def block(name,values):
    return f'  [{name}]\n'+''.join(f'    {k} = {v}\n' for k,v in values.items())+'  []\n'
def section(name,items): return f'[{name}]\n'+''.join(block(k,v) for k,v in items.items())+'[]\n'
def initial_mandel(load,linear):
    model=Model(isotropic_stiffness(2.5,5/6),.9,1)
    if linear:
        sys.path.insert(0,str(ROOT/'validation'))
        from mandel_reference import MandelSolution,MandelParameters
        d=MandelSolution(MandelParameters()).evaluate(1.,.1,0.,load=load)
        return float(d['eps_xx']),float(d['eps_yy']),float(d['pressure'])
    def residual(z):
        f=np.diag([1+z[0],1+z[1],1]);s=model.state(f,z[2]);P=s['J']*s['sigma']@np.linalg.inv(f).T
        return [P[0,0],P[1,1]+load,np.exp(z[2]/8)*(s['J']-.9*s['y'])-.1]
    guess=initial_mandel(load,True);sol=root(residual,guess,tol=1e-11)
    if np.linalg.norm(residual(sol.x))>1e-10:raise RuntimeError(sol.message)
    return tuple(sol.x)
def make(path,nx=10,ny=2,dt=.001,end=.2,load=1e-4,linear=False,case='mandel',angle=0,order=12):
    quarter=case=='mandel';partial=case=='partial';a=1;h=.1 if not partial else 1
    xmin=0 if quarter else -a;ymin=0 if quarter else -h
    cs=isotropic_stiffness(2.5,5/6) if quarter else isotropic_stiffness(28,16.8) if case=='isotropic' else DEFAULT_CS
    phi=.9 if quarter else .6;k=1 if quarter else 7
    ex,ey,p0=initial_mandel(load,linear) if quarter else (0,0,0)
    mesh={'base':dict(type='GeneratedMeshGenerator',dim=2,nx=nx,ny=ny,xmin=xmin,xmax=a,ymin=ymin,ymax=h,elem_type='QUAD9')}
    if partial:
        mesh['drain']=dict(type='ParsedGenerateSideset',input='base',combinatorial_geometry="'x > 0.99999 & y > -0.25 & y < 0.25'",new_sideset_name='drain')
    mesh['anchor']=dict(type='ExtraNodesetGenerator',input='drain' if partial else 'base',new_boundary='anchor',coord=f"'{xmin} {ymin} 0'")
    text=section('Mesh',mesh)
    text+=section('Variables',{'ux':dict(order='SECOND',family='LAGRANGE'),'uy':dict(order='SECOND',family='LAGRANGE'),'p':dict(order='FIRST',family='LAGRANGE')})
    text+=section('Functions',{'ix':dict(type='ParsedFunction',expression=f"'{ex:.17g}*x'"),'iy':dict(type='ParsedFunction',expression=f"'{ey:.17g}*y'"),'load':dict(type='ParsedFunction',expression=f"'{load:.17g}'" if quarter else f"'{load:.17g}*min(t/0.002,1)'" )})
    text+=section('ICs',{'ix':dict(type='FunctionIC',variable='ux',function='ix'),'iy':dict(type='FunctionIC',variable='uy',function='iy'),'p':dict(type='ConstantIC',variable='p',value=f'{p0:.17g}')})
    aux={n:dict(family='MONOMIAL',order='CONSTANT') for n in ['J','Jbar','solid_fraction','stability','energy','B12','sigma11','sigma22','sigma12']}
    aux['mass_reaction']=dict(family='LAGRANGE',order='FIRST');aux['force_reaction']=dict(family='LAGRANGE',order='SECOND')
    text+=section('AuxVariables',aux)
    text+=section('AuxKernels',{n:dict(type='MaterialRealAux',variable=n,property=n,execute_on="'INITIAL TIMESTEP_END'") for n in aux if n not in ['mass_reaction','force_reaction']})
    text+=section('Materials',{'law':dict(type='ConformalMaterial',ux='ux',uy='uy',pressure='p',mineral_stiffness="'"+' '.join(f'{v:.17g}' for v in cs.flat)+"'",solid_fraction=phi,drained_bulk=k,fluid_bulk=8,mobility=1.5,angle=angle,linear_reference=str(linear).lower(),log_quadrature=order)})
    text+=section('Kernels',{'mx':dict(type='ReferenceMomentum',variable='ux',component=0),'my':dict(type='ReferenceMomentum',variable='uy',component=1,save_in='force_reaction'),'mass':dict(type='ReferenceFluidMass',variable='p',save_in='mass_reaction')})
    drain='right' if quarter else 'drain' if partial else 'left right'
    bcs={'x':dict(type='DirichletBC',variable='ux',boundary='left' if quarter else 'anchor',value=0),'bottom':dict(type='DirichletBC',variable='uy',boundary='bottom',value=0 if not quarter else 0),'pressure':dict(type='DirichletBC',variable='p',boundary=f"'{drain}'",value=0,preset='false'),'force':dict(type='FunctionNeumannBC',variable='uy',boundary='top',function='load')}
    # FunctionNeumannBC residual is -test*function; compression needs negative function.
    text=text.replace(f"expression = '{load:.17g}'",f"expression = '{-load:.17g}'").replace(f"expression = '{load:.17g}*min",f"expression = '{-load:.17g}*min")
    text+=section('BCs',bcs)
    text+=section('Constraints',{'platen':dict(type='EqualValueBoundaryConstraint',variable='uy',secondary='top',formulation='kinematic',penalty=1)})
    pp={'mass':dict(type='ADElementIntegralMaterialProperty',mat_prop='fluid_mass'),'outflow_gradient':dict(type='ReferenceOutflow',boundary=f"'{drain}'"),'mass_reaction':dict(type='DofReactionSum',variable='mass_reaction',boundary=f"'{drain}'"),'top_reaction':dict(type='DofReactionSum',variable='force_reaction',boundary='top'),'platen_min':dict(type='NodalExtremeValue',variable='uy',boundary='top',value_type='min'),'platen_max':dict(type='NodalExtremeValue',variable='uy',boundary='top',value_type='max'),'center_pressure':dict(type='PointValue',variable='p',point="'0 0 0'"),'edge_ux':dict(type='PointValue',variable='ux',point=f"'{a} 0 0'")}
    for prop in ['J','Jbar','solid_fraction','stability']:
        for side in ['min','max']:pp[f'{prop}_{side}']=dict(type='ElementExtremeMaterialProperty',mat_prop=prop,value_type=side)
    for values in pp.values(): values['execute_on']="'INITIAL TIMESTEP_END'"
    text+=section('Postprocessors',pp)
    text+=section('VectorPostprocessors',{'profile':dict(type='LineValueSampler',variable="'p ux uy'",start_point=f"'{xmin} 0 0'",end_point=f"'{a} 0 0'",num_points=101,sort_by='x')})
    text+='[Preconditioning]\n  [full]\n    type = SMP\n    full = true\n  []\n[]\n'
    text+=f"[Executioner]\n  type = Transient\n  solve_type = PJFNK\n  line_search = basic\n  dt = {dt}\n  end_time = {end}\n  scheme = implicit-euler\n  nl_rel_tol = 1e-9\n  nl_abs_tol = 1e-12\n  nl_max_its = 15\n  l_tol = 1e-9\n  l_max_its = 200\n  petsc_options_iname = '-pc_type -pc_factor_mat_solver_type'\n  petsc_options_value = 'lu mumps'\n[]\n"
    text+='[Outputs]\n  csv = true\n  exodus = true\n  execute_on = \'INITIAL TIMESTEP_END\'\n[]\n'
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    return dict(nx=nx,ny=ny,dt=dt,end=end,load=load,linear=linear,case=case,angle=angle,initial=[ex,ey,p0])
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('path');ap.add_argument('--nx',type=int,default=10);ap.add_argument('--ny',type=int,default=2);ap.add_argument('--dt',type=float,default=.001);ap.add_argument('--end',type=float,default=.2);ap.add_argument('--load',type=float,default=1e-4);ap.add_argument('--linear',action='store_true');ap.add_argument('--case',default='mandel');ap.add_argument('--angle',type=float,default=0);a=vars(ap.parse_args());print(make(**a))
