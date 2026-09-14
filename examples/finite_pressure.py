#!/usr/bin/env python3
"""Reproduce the manuscript's dimensionless coaxial pressure experiments.

Uses only the Python standard library. Outputs are regenerated under build/.
All stresses/moduli use one arbitrary common stress unit; strains are logarithmic.
"""
from pathlib import Path
import csv
import io
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "examples"
PHI = 0.75
KS = 20.0
CD = ((12., 4., 3.), (4., 12., 3.), (3., 3., 8.))
ROWS = tuple(sum(row) for row in CD)
H = PHI**2 / (PHI / KS - sum(ROWS) / (9 * KS**2))
R = tuple(v / (3 * PHI * KS) for v in ROWS)
B0 = tuple(1 - PHI * v for v in R)
BS = sum(B0) / 3


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def root(fun, lo, hi, tolerance=2e-14):
    """Bracketed bisection; the reported paths have strictly increasing residuals."""
    flo, fhi = fun(lo), fun(hi)
    if flo > 0 or fhi < 0:
        raise ValueError((lo, hi, flo, fhi))
    for _ in range(160):
        mid = (lo + hi)/2
        value = fun(mid)
        if value > 0:
            hi = mid
        else:
            lo = mid
        if hi-lo < tolerance:
            return (hi+lo)/2
    raise RuntimeError("bisection did not converge")


def state(eps, p):
    """Exact coaxial stress and Biot tensor of W=eps:Cd:eps/2+h(q-r:eps)^2/2."""
    req = dot(R, eps)
    q = req if p == 0 else root(lambda q: H*(q-req)+PHI*p*math.exp(q), req-5, req)
    mineral = math.exp(q)
    jac = math.exp(sum(eps))
    solid = PHI*mineral/jac
    z = PHI*p*mineral/H
    biot = tuple(1-solid*r/(1+z) for r in R)
    drained = tuple(dot(row, eps)/jac for row in CD)
    sigma = tuple(s + p*(solid*r-1) for s, r in zip(drained, R))
    return dict(q=q, mineral=mineral, J=jac, porosity=1-solid,
                hp=H*(1+z), B=biot, sigma=sigma, drained=drained)


def surrogate(eps, p, kind):
    if kind == "volume":
        # W_V = W_d + h/2 (exp(q) - exp(r:eps))^2.
        mineral = math.exp(dot(R, eps))-PHI*p/H
        if mineral <= 0:
            raise ValueError("volume-penalty mineral volume is nonpositive")
        solid = PHI*mineral/math.exp(sum(eps))
        if not 0 < solid < 1:
            raise ValueError("volume-penalty porosity is inadmissible")
        b = tuple(1-PHI*math.exp(dot(R,eps)-sum(eps))*v for v in R)
        return tuple(dot(row,eps)/math.exp(sum(eps))-p*v for row,v in zip(CD,b))
    b = B0 if kind == "tensor" else (BS,)*3
    return tuple(dot(row, eps)/math.exp(sum(eps))-p*v for row, v in zip(CD, b))


def layer(p, kind="full"):
    def stress(s):
        return (state((0, 0, s), p)["sigma"] if kind == "full"
                else surrogate((0, 0, s), p, kind))[2]
    s = root(stress, 0, 0.65)
    eps = (0, 0, s)
    sig = state(eps, p)["sigma"] if kind == "full" else surrogate(eps, p, kind)
    return s, math.expm1(s), sig[0]


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != content:
        path.write_text(content)


def csv_text(rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerows(rows)
    return buf.getvalue()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = dict(phi=PHI, Ks=KS, h=H, r=R, B0=B0, scalar=BS, fixed=[], layer=[])
    rows = [["p_over_Ks", "s", "B1", "B3", "mineral", "porosity", "stress1", "stress3", "tensor_error", "scalar_error"]]
    for s in (-0.2, 0., 0.2):
        path = [["p", "B1", "B3", "porosity", "mineral", "error"]]
        for j in range(81):
            p = KS*0.1*j/80
            st = state((0, 0, s), p)
            inc = tuple(a-b for a, b in zip(st["sigma"], st["drained"]))
            errors = []
            for b in (B0, (BS,)*3):
                errors.append(0. if p == 0 else math.sqrt(sum((a+p*v)**2 for a, v in zip(inc,b)))/math.sqrt(dot(inc,inc)))
            rows.append([p/KS, s, *[st["B"][i] for i in (0,2)], st["mineral"], st["porosity"], inc[0], inc[2], *errors])
            path.append([p/KS, st["B"][0], st["B"][2], st["porosity"], st["mineral"], 100*errors[0]])
            assert st["hp"] > 0 and 0 < st["porosity"] < 1
        write(OUT / f"fixed_{s:+.1f}.csv", csv_text(path))
        summary["fixed"].append(dict(s=s, p=p, **st, tensor_error=errors[0], scalar_error=errors[1]))
    write(OUT/"fixed.csv", csv_text(rows))
    rows = [["p", "full_extension", "tensor_extension", "scalar_extension", "full_reaction", "tensor_reaction", "scalar_reaction"]]
    for j in range(81):
        p = KS*0.1*j/80
        vals = [layer(p, kind) for kind in ("full", "tensor", "scalar")]
        rows.append([p/KS, *[100*v[1] for v in vals], *[v[2]/KS for v in vals]])
        st = state((0,0,vals[0][0]),p)
        assert 0 < st["porosity"] < 1
        if j in (1, 8, 40, 80):
            summary["layer"].append(dict(p=p, full=vals[0], tensor=vals[1], scalar=vals[2], porosity=st["porosity"]))
    write(OUT/"layer.csv", csv_text(rows))
    write(OUT/"summary.json", json.dumps(summary, indent=2)+"\n")
    table = []
    for rec in summary["fixed"]:
        table.append(f"{rec['s']:+.1f} & {rec['B'][0]:.3f} & {rec['B'][2]:.3f} & {rec['mineral']:.3f} & {rec['porosity']:.3f} & {100*rec['tensor_error']:.1f} & {100*rec['scalar_error']:.1f} \\\\")
    write(OUT/"fixed_rows.tex", "\n".join(table)+"\n")
    table = []
    for rec in summary["layer"]:
        table.append(f"{rec['p']/KS:.5f} & {100*rec['full'][1]:.3f} & {100*rec['tensor'][1]:.3f} & {100*rec['scalar'][1]:.3f} & {rec['full'][2]/KS:.4f} & {rec['tensor'][2]/KS:.4f} & {rec['scalar'][2]/KS:.4f} \\\\")
    write(OUT/"layer_rows.tex", "\n".join(table)+"\n")
    # A second hyperelastic continuation with exactly the same reference Hessian
    # and the same condensed energy at every zero-pressure deformation.
    rows = [["p", "log_extension", "volume_extension", "log_reaction", "volume_reaction"]]
    alternative=[]
    for j in range(81):
        p=KS*0.1*j/80
        log,vol=layer(p),layer(p,"volume")
        rows.append([p/KS,100*log[1],100*vol[1],log[2]/KS,vol[2]/KS])
        if j in (8,40,80):
            alternative.append(dict(p=p,log=log,volume=vol))
    write(OUT/"continuations.csv",csv_text(rows))
    summary['continuations']=alternative
    # Compatible anisotropic intrinsic elasticity: same Cd, variable mineral.
    T=(-1/math.sqrt(6),-1/math.sqrt(6),2/math.sqrt(6))
    anisotropic=[];table=[]
    for c,beta in ((0.,6.),(6.,6.),(6.,18.)):
        hd=12+beta
        a=tuple(PHI*math.sqrt(3)/(45-c*c/hd)*(1/math.sqrt(3)-c*t/hd) for t in T)
        cda=tuple(dot(row,a) for row in CD)
        hh=PHI**2/(PHI*sum(a)-dot(a,cda))
        b=tuple(1-v for v in cda)
        rec=dict(c=c,beta=beta,a=a,h=hh,kappa=hh-15,B=b)
        anisotropic.append(rec)
        table.append(f"{c:.0f} & {beta:.0f} & {hh:.3f} & {hh-15:.3f} & {b[0]:.3f} & {b[2]:.3f} \\\\")
    summary['anisotropic']=anisotropic
    write(OUT/"anisotropic_rows.tex","\n".join(table)+"\n")
    write(OUT/"summary.json",json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
