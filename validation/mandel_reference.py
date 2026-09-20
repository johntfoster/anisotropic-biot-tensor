#!/usr/bin/env python3
"""Classical plane-strain Mandel solution, independently evaluated series.

SPDX-License-Identifier: Apache-2.0
Equations: Cheng and Detournay (1988), doi:10.1002/nag.1610120508;
also Appendix D of doi:10.1093/gji/ggad370. No third-party code is copied.

Coordinates span [-a,a] x [-b,b]. ``load`` is positive mean compressive
traction, not resultant force. Full top force is 2*a*load per unit thickness.
The t=0 value is the undrained post-load bulk trace; drainage starts at t>0.
All quantities use one consistent length, stress, and time unit system.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.special import erfc


@dataclass(frozen=True)
class MandelParameters:
    K: float = 1.0
    G: float = 0.75
    alpha: float = 0.6
    M: float = 80.0 / 17.0
    mobility: float = 1.5
    a: float = 1.0
    b: float = 0.1

    def __post_init__(self):
        if min(self.K, self.G, self.M, self.mobility, self.a, self.b) <= 0:
            raise ValueError("Moduli, mobility, and half dimensions must be positive")
        if not 0 < self.alpha <= 1:
            raise ValueError("This series requires 0 < alpha <= 1")

    @property
    def lame(self):
        return self.K - 2 * self.G / 3

    @property
    def Ku(self):
        return self.K + self.alpha**2 * self.M

    @property
    def nu(self):
        return (3 * self.K - 2 * self.G) / (6 * self.K + 2 * self.G)

    @property
    def nu_u(self):
        return (3 * self.Ku - 2 * self.G) / (6 * self.Ku + 2 * self.G)

    @property
    def skempton(self):
        return self.alpha * self.M / self.Ku

    @property
    def c(self):
        return self.mobility / (1 / self.M + self.alpha**2 / (self.K + 4*self.G/3))

    @property
    def root_ratio(self):
        return (1 - self.nu) / (self.nu_u - self.nu)

    @property
    def initial_pressure_per_load(self):
        return self.skempton * (1 + self.nu_u) / 3


class MandelSolution:
    """Adaptive Gaussian-tail-controlled eigenfunction series.

    ``tolerance`` bounds a dimensionless common tail envelope, before field
    prefactors. It is not an FE acceptance threshold. Roots solve
    sin(z)/z - root_ratio*cos(z) = 0 without evaluating tan near its poles.
    """

    def __init__(self, params=None, tolerance=1e-13, max_modes=20000):
        self.params = params or MandelParameters()
        if not 0 < tolerance < 1:
            raise ValueError("tolerance must lie between zero and one")
        self.tolerance = tolerance
        self.max_modes = max_modes
        self.roots = []

    def _roots(self, n):
        ratio = self.params.root_ratio
        while len(self.roots) < n:
            k = len(self.roots)
            lo = k * math.pi if k else 1e-8
            hi = (k + 0.5) * math.pi
            root = brentq(lambda z: math.sin(z)/z - ratio*math.cos(z),
                          lo, hi, xtol=1e-14, rtol=4*np.finfo(float).eps)
            self.roots.append(root)
        return np.asarray(self.roots[:n])

    @staticmethod
    def _tail(n, beta):
        # Omitted roots z_k exceed k*pi (zero-based k >= n). The Gaussian
        # sum is bounded by its first term plus the decreasing-function integral.
        gamma = beta * math.pi**2
        return math.exp(-gamma*n*n) + math.sqrt(math.pi)/(2*math.sqrt(gamma))*erfc(math.sqrt(gamma)*n)

    def _mode_count(self, t):
        beta = self.params.c * t / self.params.a**2
        n = max(8, int(math.sqrt(-math.log(self.tolerance)/beta)/math.pi)+1)
        while self._tail(n, beta) > self.tolerance:
            n += 1
        if n > self.max_modes:
            raise ValueError(f"Series needs {n} modes; increase max_modes or resolve t=0 analytically")
        return n, self._tail(n, beta)

    def evaluate(self, x, y, t, load=1.0):
        """Return broadcast arrays for fields; modes and tail_bound are scalars.

        fluid_content = alpha*div(u)+p/M is fluid-volume change per reference
        volume. qx is outward-positive Darcy volume flux in the +x direction.
        Multiply both by reference fluid density for linearized mass units.
        """
        x, y, t = np.broadcast_arrays(np.asarray(x, float), np.asarray(y, float), np.asarray(t, float))
        p = self.params
        if np.any(~np.isfinite(x)) or np.any(~np.isfinite(y)) or np.any(~np.isfinite(t)):
            raise ValueError("Coordinates and time must be finite")
        if np.any(t < 0) or np.any(np.abs(x) > p.a*(1+1e-14)) or np.any(np.abs(y) > p.b*(1+1e-14)):
            raise ValueError("Use t>=0 and points inside the rectangle")
        fields = {key: np.empty(x.shape) for key in ("pressure", "ux", "uy", "eps_xx", "eps_yy", "qx")}
        initial = t == 0
        fields["pressure"][initial] = load*p.initial_pressure_per_load
        fields["eps_xx"][initial] = load*p.nu_u/(2*p.G)
        fields["eps_yy"][initial] = -load*(1-p.nu_u)/(2*p.G)
        fields["ux"][initial] = fields["eps_xx"][initial]*x[initial]
        fields["uy"][initial] = fields["eps_yy"][initial]*y[initial]
        fields["qx"][initial] = 0  # undrained trace, not the singular t=0+ edge flux
        modes, bound = 0, 0.0
        if np.any(~initial):
            modes, bound = self._mode_count(float(t[~initial].min()))
            roots = self._roots(modes)
            sn, cs = np.sin(roots), np.cos(roots)
            denom = roots - sn*cs
            # Chunk points to avoid a modes-by-entire-mesh allocation.
            flatids = np.flatnonzero(~initial)
            for ids in np.array_split(flatids, max(1, math.ceil(len(flatids)/256))):
                xx, yy, tt = x.flat[ids], y.flat[ids], t.flat[ids]
                decay = np.exp(-roots[:, None]**2*p.c*tt[None, :]/p.a**2)
                angle = roots[:, None]*xx[None, :]/p.a
                cosx, sinx = np.cos(angle), np.sin(angle)
                S = np.sum((sn*cs/denom)[:, None]*decay, axis=0)
                P = 2*load*p.initial_pressure_per_load*np.sum((sn/denom)[:, None]*(cosx-cs[:, None])*decay, axis=0)
                ex = load*p.nu/(2*p.G) - load*p.nu_u/p.G*S + load/p.G*np.sum((roots*cs/denom)[:, None]*cosx*decay, axis=0)
                ey = -load*(1-p.nu)/(2*p.G) + load*(1-p.nu_u)/p.G*S
                ux = (load*p.nu/(2*p.G)-load*p.nu_u/p.G*S)*xx + load*p.a/p.G*np.sum((cs/denom)[:, None]*sinx*decay, axis=0)
                qx = 2*load*p.initial_pressure_per_load*p.mobility/p.a*np.sum((roots*sn/denom)[:, None]*sinx*decay, axis=0)
                for key, value in {"pressure": P,"ux":ux,"uy":ey*yy,"eps_xx":ex,"eps_yy":ey,"qx":qx}.items():
                    fields[key].flat[ids] = value
        volume_strain = fields["eps_xx"] + fields["eps_yy"]
        fields["sigma_xx"] = 2*p.G*fields["eps_xx"] + p.lame*volume_strain - p.alpha*fields["pressure"]
        fields["sigma_yy"] = 2*p.G*fields["eps_yy"] + p.lame*volume_strain - p.alpha*fields["pressure"]
        fields["fluid_content"] = p.alpha*volume_strain + fields["pressure"]/p.M
        fields["modes"] = modes
        fields["tail_bound"] = bound
        return fields


def self_check(solution):
    """Reference-only gates, independent of any FE result."""
    p = solution.params
    checks = {}
    def check(name, error, tol):
        checks[name] = {"error": float(error), "tolerance": tol, "passed": bool(abs(error) <= tol)}
    z = solution._roots(128)
    check("root_equation_scaled_residual", np.max(np.abs(np.sin(z)/z-p.root_ratio*np.cos(z))), 2e-12)
    check("reference_M", p.M-80/17, 1e-14)
    check("reference_Ku", p.Ku-229/85, 1e-14)
    x = np.linspace(-p.a, p.a, 91)
    initial = solution.evaluate(x, p.b, 0)
    check("undrained_fluid_content", np.max(np.abs(initial["fluid_content"])), 1e-14)
    check("undrained_vertical_stress", np.max(np.abs(initial["sigma_yy"]+1)), 1e-14)
    check("undrained_horizontal_stress", np.max(np.abs(initial["sigma_xx"])), 1e-14)
    late = solution.evaluate(x, p.b, 30*p.a*p.a/p.c)
    check("drained_pressure", np.max(np.abs(late["pressure"])), 1e-14)
    check("drained_ux", np.max(np.abs(late["ux"]-p.nu*x/(2*p.G))), 1e-14)
    check("drained_uy", np.max(np.abs(late["uy"]+(1-p.nu)*p.b/(2*p.G))), 1e-14)
    for time in (1e-5, 0.001, 0.03, 0.2):
        state = solution.evaluate(x, p.b, time)
        check(f"horizontal_equilibrium_t{time}", np.max(np.abs(state["sigma_xx"])), 2e-13)
        check(f"drainage_t{time}", np.max(np.abs(state["pressure"][[0,-1]])), 1e-14)
        check(f"rigid_platen_t{time}", np.ptp(state["uy"]), 1e-14)
        integral = quad(lambda xx: float(solution.evaluate(xx, p.b, time)["sigma_yy"]), 0,p.a,epsabs=1e-12,limit=300)[0]
        check(f"platen_resultant_t{time}", integral+p.a, 1e-11)
        fine = MandelSolution(p, tolerance=1e-15).evaluate(x,p.b,time)
        check(f"truncation_pressure_t{time}", np.max(np.abs(state["pressure"]-fine["pressure"])), 1e-12)
        check(f"truncation_displacement_t{time}", np.max(np.abs(state["ux"]-fine["ux"])), 1e-12)
    near = MandelSolution(p, max_modes=40000).evaluate(np.array([0.,.3*p.a,.6*p.a]),p.b,1e-9)
    # The bulk t->0 approach is O(sqrt(t)); the boundary corner is excluded.
    check("initial_interior_pressure_limit", np.max(np.abs(near["pressure"]-p.initial_pressure_per_load)), 2e-5)
    check("initial_displacement_limit", np.max(np.abs(near["ux"]-p.nu_u*np.array([0.,.3*p.a,.6*p.a])/(2*p.G))), 2e-5)
    time=.02
    dt=1e-6
    content = lambda tt: quad(lambda xx: float(solution.evaluate(xx,0,tt)["fluid_content"]),0,p.a,epsabs=1e-12)[0]*p.b
    lossrate = (content(time+dt)-content(time-dt))/(2*dt)
    flux = float(solution.evaluate(p.a,0,time)["qx"])*p.b
    check("integrated_mass_rate", lossrate+flux, 1e-9)
    peak = minimize_scalar(lambda tt: -float(solution.evaluate(0,0,tt)["pressure"]), bounds=(1e-8,.4*p.a*p.a/p.c),method="bounded",options={"xatol":1e-13})
    ratio = -peak.fun/p.initial_pressure_per_load
    checks["central_overshoot"] = {"ratio": ratio, "time": peak.x, "passed":bool(ratio>1.01)}
    checks["series_tail_bound"] = {"value": float(solution.evaluate(0,0,1e-5)["tail_bound"]), "passed":bool(solution.evaluate(0,0,1e-5)["tail_bound"]<=solution.tolerance)}
    return {"category":"analytical-reference-only", "passed":all(c["passed"] for c in checks.values()),"checks": checks}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=Path(".agent-runtime/moose-fe-goal-2026-09-20/reference"))
    parser.add_argument("--load",type=float,default=1.)
    parser.add_argument("--self-check",action="store_true")
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    sol=MandelSolution()
    times=np.unique(np.r_[0., np.geomspace(1e-6,.7,300),.001,.01,.03,.1,.3,.7])
    rows=[]
    for time in times:
        for x in (0.,.3,.8,1.):
            result=sol.evaluate(x,sol.params.b,time,args.load)
            rows.append({"time":time,"x":x,"y":sol.params.b,**{k:float(v) for k,v in result.items()}})
    with (args.output_dir/"mandel-probes.csv").open("w") as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    rows=[]
    for time in (.00001,.001,.01,.03,.1,.3,.7):
        for x in np.linspace(-1.,1.,201):
            result=sol.evaluate(x,sol.params.b,time,args.load)
            rows.append({"time":time,"x":x,"y":sol.params.b,**{k:float(v) for k,v in result.items()}})
    with (args.output_dir/"mandel-profiles.csv").open("w") as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    metadata={"parameters":asdict(sol.params),"derived":{k:getattr(sol.params,k) for k in ("Ku","nu","nu_u","skempton","c","root_ratio","initial_pressure_per_load")},"load":args.load,"force_convention":"load is positive mean traction; full top force=2*a*load per unit thickness","source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"numpy_version":np.__version__,"artifacts":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in args.output_dir.glob("mandel-*.csv")}}
    if args.self_check:
        metadata["verification"]=self_check(sol)
    (args.output_dir/"mandel-reference-report.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print(json.dumps(metadata,indent=2))
    if args.self_check and not metadata["verification"]["passed"]:
        raise SystemExit(1)


if __name__=="__main__":
    main()
