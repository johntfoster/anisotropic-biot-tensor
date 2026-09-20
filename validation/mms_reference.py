#!/usr/bin/env python3
"""Independent symbolic reference for rotated-anisotropic linear poroelasticity.

SPDX-License-Identifier: Apache-2.0
Reference labels: eq:drained-compliance-restriction in stress_reconstruction,
eq:reference-biot-compatibility and eq:reference-storage-compatibility in limits.
No application material, kernel, residual, or AD code is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


def mandel_basis():
    basis=[]
    for i,j in ((0,0),(1,1),(2,2),(1,2),(0,2),(0,1)):
        e=sp.zeros(3)
        e[i,j]=1 if i==j else 1/sp.sqrt(2)
        e[j,i]=e[i,j]
        basis.append(e)
    return basis


def build_reference():
    """Build exact expressions for the declared benchmark, with rational data."""
    basis=mandel_basis()
    eye=sp.eye(3)
    eye6=sp.Matrix([1,1,1,0,0,0])
    cs=sp.Matrix([[50,12,10,0,0,0],[12,60,14,0,0,0],
                  [10,14,70,0,0,0],[0,0,0,20,0,0],
                  [0,0,0,0,24,0],[0,0,0,0,0,28]])
    angle=sp.pi/6
    rotation=sp.Matrix([[sp.cos(angle),-sp.sin(angle),0],
                        [sp.sin(angle),sp.cos(angle),0],[0,0,1]])
    Q=sp.Matrix(6,6,lambda i,j:sp.trace(basis[i].T*rotation*basis[j]*rotation.T))
    cs=sp.simplify(Q*cs*Q.T)
    phi=sp.Rational(3,5)
    K=sp.Integer(7)
    Ks=(eye6.T*cs*eye6)[0]/9
    # Invert the compliance addition (43), rather than reproducing the C++
    # material's rank-one stiffness update, to give an independent reference.
    sd=cs.inv()/phi+(1-K/(phi*Ks))/(9*K)*(eye6*eye6.T)
    cd=sp.simplify(sd.inv())
    B6=sp.simplify(eye6-cd*cs.inv()*eye6)
    B=sum((B6[i]*basis[i] for i in range(6)),sp.zeros(3))
    Ss=sp.simplify((phi*eye6.T*cs.inv()*eye6-eye6.T*cs.inv()*cd*cs.inv()*eye6)[0])
    Kf=sp.Integer(8)
    rho0=sp.Integer(1)
    mobility=sp.Rational(3,2)
    S=Ss+(1-phi)/Kf
    x,y,t=sp.symbols("x y t", real=True)
    amplitude=sp.Rational(1,100)
    ux=amplitude*sp.sin(sp.pi*x)*sp.sin(sp.pi*y)*sp.sin(t)
    uy=amplitude*sp.cos(sp.pi*x)*sp.sin(sp.pi*y)*sp.sin(t)
    pressure=amplitude*sp.cos(sp.pi*x)*sp.cos(sp.pi*y)*sp.sin(t)
    u=sp.Matrix([ux,uy,0])
    grad=sp.zeros(3)
    for i in range(3):
        for j,coord in enumerate((x,y)):
            grad[i,j]=sp.diff(u[i],coord)
    strain=(grad+grad.T)/2
    strain6=sp.Matrix([sp.trace(e.T*strain) for e in basis])
    stress6=cd*strain6-B6*pressure
    stress=sum((stress6[i]*basis[i] for i in range(6)),sp.zeros(3))
    body=sp.Matrix([-sum(sp.diff(stress[i,j],coord) for j,coord in enumerate((x,y))) for i in range(2)])
    # Linear reference mass per reference mixture volume and mass flux.
    mass=rho0*((1-phi)+sp.trace(B.T*strain)+S*pressure)
    flux=sp.Matrix([-rho0*mobility*sp.diff(pressure,c) for c in (x,y)])
    source=sp.diff(mass,t)+sum(sp.diff(flux[j],coord) for j,coord in enumerate((x,y)))
    expressions={"exact_ux":ux,"exact_uy":uy,"exact_p":pressure,
                 "body_x":sp.expand(body[0]),"body_y":sp.expand(body[1]),
                 "mass_source":sp.expand(source)}
    return dict(x=x,y=y,t=t,basis=basis,Cs=cs,Cd=cd,B0=B,Ss=Ss,S=S,
                rho0=rho0,Kf=Kf,mobility=mobility,phi=phi,K=K,Ks=Ks,
                rotation=rotation,strain=strain,stress=stress,mass=mass,flux=flux,
                expressions=expressions)


def parsed_expression(expression):
    """Emit only MOOSE ParsedFunction arithmetic and trigonometric syntax."""
    return str(sp.N(expression.subs(sp.pi,sp.N(sp.pi,17)),17)).replace("**","^")


def evaluate(reference,x,y,t):
    args=(reference["x"],reference["y"],reference["t"])
    fields={key:float(sp.lambdify(args,value,"numpy")(x,y,t))
            for key,value in reference["expressions"].items()}
    for key in ("stress","strain","mass","flux"):
        fields[key]=np.asarray(sp.lambdify(args,reference[key],"numpy")(x,y,t),float).tolist()
    return fields


def verify(reference):
    args=(reference["x"],reference["y"],reference["t"])
    stress=sp.lambdify(args,reference["stress"],"numpy")
    mass=sp.lambdify(args,reference["mass"],"numpy")
    flux=sp.lambdify(args,reference["flux"],"numpy")
    body=sp.lambdify(args,sp.Matrix([reference["expressions"]["body_x"],reference["expressions"]["body_y"]]),"numpy")
    source=sp.lambdify(args,reference["expressions"]["mass_source"],"numpy")
    results=[]
    for point in ((.17,.23,.19),(.43,.61,.7),(.81,.37,1.1)):
        x,y,t=point
        errors=[]
        for h in (1e-3,5e-4,2.5e-4,1e-4):
            divergence=((stress(x+h,y,t)-stress(x-h,y,t))[:,0]
                        +(stress(x,y+h,t)-stress(x,y-h,t))[:,1])/(2*h)
            balance=(mass(x,y,t+h)-mass(x,y,t-h))/(2*h)
            balance+=float((flux(x+h,y,t)[0,0]-flux(x-h,y,t)[0,0]
                           +flux(x,y+h,t)[1,0]-flux(x,y-h,t)[1,0])/(2*h))
            errors.append({"h":h,"body_error":float(np.max(np.abs(divergence[:2]+body(x,y,t).ravel()))),
                           "mass_error":float(abs(balance-source(x,y,t)))})
        passed=(errors[-1]["body_error"]<1e-7 and errors[-1]["mass_error"]<1e-7
                and errors[0]["body_error"]/errors[1]["body_error"]>3.8
                and errors[0]["mass_error"]/errors[1]["mass_error"]>3.8)
        results.append({"point":point,"differences":errors,"passed":bool(passed)})
    # Check emitted decimal ParsedFunction strings against exact symbolic expressions.
    expressions=reference["expressions"]
    parser_error=0.
    for point in ((.17,.23,.19),(.43,.61,.7),(.81,.37,1.1)):
        values=dict(zip(("x","y","t"),point))
        for expr in expressions.values():
            emitted=parsed_expression(expr).replace("^","**")
            emitted_value=eval(emitted,{"__builtins__":{},"sin":math.sin,"cos":math.cos,"sqrt":math.sqrt},values)
            exact_value=float(expr.subs(dict(zip(args,point))))
            parser_error=max(parser_error,abs(emitted_value-exact_value))
    initial_zero=all(sp.simplify(v.subs(reference["t"],0))==0 for key,v in expressions.items() if key.startswith("exact_"))
    # Exact domain L2 norms: each trigonometric product has squared integral 1/4.
    return {"category":"independent-reference-only","passed":all(r["passed"] for r in results) and parser_error<1e-14 and initial_zero,
            "finite_difference_checks":results,"parsed_expression_error":parser_error,
            "zero_initial_fields":bool(initial_zero),"exact_L2_each_field":"abs(sin(t))/200",
            "exact_L2_vector_displacement":"sqrt(2)*abs(sin(t))/200",
            "smallest_Cd_eigenvalue":float(np.linalg.eigvalsh(np.array(reference["Cd"],float)).min()),
            "storage":float(reference["S"]),"solid_storage":float(reference["Ss"])}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=Path(".agent-runtime/moose-fe-goal-2026-09-20/reference"))
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    ref=build_reference()
    expressions={k:parsed_expression(v) for k,v in ref["expressions"].items()}
    (args.output_dir/"mms-expressions.json").write_text(json.dumps(expressions,indent=2)+"\n")
    functions=["# Generated by validation/mms_reference.py; original Apache-2.0 code.","[Functions]"]
    for name,value in expressions.items():
        functions.extend([f"  [{name}]","    type = ParsedFunction",f"    expression = '{value}'","  []"])
    functions.extend(["[]",""])
    (args.output_dir/"mms-functions.i").write_text("\n".join(functions))
    points=[dict(x=x,y=y,t=t,**evaluate(ref,x,y,t)) for x,y,t in ((.17,.23,.19),(.43,.61,.7),(.81,.37,1.1))]
    (args.output_dir/"mms-fixed-points.json").write_text(json.dumps(points,indent=2)+"\n")
    report={"source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "sympy_version":sp.__version__,"numpy_version":np.__version__,
            "parameters":{key:float(ref[key]) for key in ("rho0","Kf","mobility","phi","K","Ks","Ss","S")},
            "orientation_degrees":30,"amplitudes":{"U":.01,"P":.01},
            "Cs_Mandel":np.array(ref["Cs"],float).tolist(),"Cd_Mandel":np.array(ref["Cd"],float).tolist(),
            "B0":np.array(ref["B0"],float).tolist(),"rotation":np.array(ref["rotation"],float).tolist(),
            "verification":verify(ref),
            "artifact_sha256":{name:hashlib.sha256((args.output_dir/name).read_bytes()).hexdigest()
                               for name in ("mms-expressions.json","mms-functions.i","mms-fixed-points.json")}}
    (args.output_dir/"mms-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if not report["verification"]["passed"]:
        raise SystemExit(1)


if __name__=="__main__":
    main()
