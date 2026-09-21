#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent check of the MOOSE fabric law against the manuscript equations.

This script re-implements the reference-state axisymmetric distention model of
``sections/pore_fabric.tex`` from scratch with NumPy (kinematics, the
volumetric--axial distention basis, the constrained distention equilibrium, the
compliance restriction, the Biot tensor) and compares the result with the
compiled ``FabricMaterial`` output recorded under ``fe-evidence/runs``. The
distention strain is restricted to the fabric's retained invariant subspace
``span(e1, e2)`` (the volumetric and axial-deviatoric directions), exactly as
the compiled law reduces it: the complementary four symmetric modes carry no
distention energy and are frozen into the mineral. That recorded
run tree ships both with the repository and inside the numerical supplement
archive, so the script runs unchanged from an extracted archive root; pass
``--runs`` to read another recorded tree.

This is an implementation check: it verifies the compiled material against
re-derived formulas, but it shares the modeling conventions (basis, equilibrium,
and the reported `ln_h = ln h` sign convention) with the implementation.

It also checks the two required limits:
  * the conformal (spherical distention) limit reproduces the reviewed
    ``ConformalMaterial`` at the same prescribed state, and
  * a vanishing volume-axial distention coupling leaves the Biot tensor
    isotropic, so any B_par != B_per must come from that coupling or from an
    anisotropic mineral.

Nothing here is fitted: every number comes from the equations and the
recorded runs.
"""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS = ROOT / "fe-evidence/runs"
OUT = ROOT / "build/fabric"

PHI = 0.9
KF = 8.0
RHO0 = 1.0
CS_ENTRIES = [
    3.6111111111111116, 1.9444444444444444, 1.9444444444444444, 0.0, 0.0, 0.0,
    1.9444444444444444, 3.6111111111111116, 1.9444444444444444, 0.0, 0.0, 0.0,
    1.9444444444444444, 1.9444444444444444, 3.6111111111111116, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.6666666666666667, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 1.6666666666666667, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 1.6666666666666667,
]
CS = np.array(CS_ENTRIES).reshape(6, 6)
KS = CS[:3, :3].sum() / 9.0

# Prescribed uniform state of the probe decks.
E11, E22, P0 = 0.01, -0.005, 0.02


def mandel(T):
    return np.array([T[0, 0], T[1, 1], T[2, 2],
                     np.sqrt(2) * T[1, 2], np.sqrt(2) * T[0, 2], np.sqrt(2) * T[0, 1]])


def tensor(v):
    T = np.zeros((3, 3))
    T[0, 0], T[1, 1], T[2, 2] = v[0], v[1], v[2]
    T[1, 2] = T[2, 1] = v[3] / np.sqrt(2)
    T[0, 2] = T[2, 0] = v[4] / np.sqrt(2)
    T[0, 1] = T[1, 0] = v[5] / np.sqrt(2)
    return T


def basis(angle_deg):
    a = np.radians(angle_deg)
    m = np.array([np.cos(a), np.sin(a), 0.0])

    def sym(a1, a2):
        return 0.5 * (np.outer(a1, a2) + np.outer(a2, a1))

    I3 = np.eye(3)
    dirs = [
        I3 / np.sqrt(3.0),          # e1, volumetric
        sym(m, m) - I3 / 3.0,       # e2, axial (degree-2)
    ]
    out = []
    for T in dirs:
        v = mandel(T)
        out.append(v / np.linalg.norm(v))
    return m, out


def solve_probe(params):
    """Retained-subspace equilibrium coefficients x for the probe state."""
    angle = params.get("angle", 0.0)
    kv = params.get("volume", 1.0)
    ka = params.get("axial", 1.0)
    kc = params.get("coupling", 0.0)
    if params.get("conformal", False):
        ka, kc = 1.0e12, 0.0
    _, e = basis(angle)
    Dd = np.array([[kv, kc], [kc, ka]])
    G = np.array([[float(e[i] @ CS @ e[j]) for j in range(2)] for i in range(2)])
    solve = np.linalg.inv(Dd + PHI * G)
    eps = np.diag([E11, E22, 0.0])
    ev = mandel(eps)
    g = np.array([float(e[i] @ CS @ ev) for i in range(2)])
    rhs = PHI * g
    rhs[0] += PHI * np.sqrt(3.0) * P0
    return solve @ rhs


def run_case(params):
    angle = params.get("angle", 0.0)
    conformal = params.get("conformal", False)
    kv = params.get("volume", 1.0)
    ka = params.get("axial", 1.0)
    kc = params.get("coupling", 0.0)
    if conformal:
        ka = 1.0e12
        kc = 0.0

    m, e = basis(angle)
    Dd = np.array([[kv, kc], [kc, ka]])
    assert np.all(np.linalg.eigvalsh(Dd) > 0)

    Dplus = np.zeros((6, 6))
    dinv = np.linalg.inv(Dd)
    for i in range(2):
        for j in range(2):
            Dplus += dinv[i, j] * np.outer(e[i], e[j])

    Cd = np.linalg.inv(np.linalg.inv(PHI * CS) + Dplus)
    eI = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    Bv = eI - Cd @ (np.linalg.inv(CS) @ eI)
    B = tensor(Bv)
    mm = np.outer(m, m)
    b_par = float(mm.ravel() @ B.ravel())
    b_per = 0.5 * (float(np.trace(B)) - b_par)
    Kd = Cd[:3, :3].sum() / 9.0
    storage = (1 - PHI) / KF + (PHI / KS) * (1.0 - Kd / (PHI * KS))

    G = np.array([[float(e[i] @ CS @ e[j]) for j in range(2)] for i in range(2)])
    solve = np.linalg.inv(Dd + PHI * G)

    eps = np.diag([E11, E22, 0.0])
    ev = mandel(eps)
    g = np.array([float(e[i] @ CS @ ev) for i in range(2)])
    rhs = PHI * g
    rhs[0] += PHI * np.sqrt(3.0) * P0
    x = solve @ rhs

    edv = sum(x[i] * e[i] for i in range(2))
    ebv = ev - edv
    epsbar = tensor(ebv)
    sig = PHI * CS @ ebv - (1 - PHI) * P0 * eI

    J = 1.0 + np.trace(eps)
    y = 1.0 + np.trace(epsbar)
    b_dot_e = float(Bv @ ev)
    return {
        "B_par": b_par,
        "B_per": b_per,
        "B_anisotropy": b_par - b_per,
        "ln_a": float(np.sqrt(3.0) * x[0]),
        "ln_h": float(-x[1] / np.sqrt(1.5)),
        "J": float(J),
        "Jbar": float(y),
        "solid_fraction": float(PHI * y / J),
        "sigma11": float(sig[0]),
        "sigma22": float(sig[1]),
        "mass": float(RHO0 * ((1 - PHI) + b_dot_e + storage * P0)),
    }


def last_row(runs, name):
    path = runs / name / "solution.csv"
    if not path.is_file():
        raise SystemExit("recorded run history not found: " + str(path))
    with open(path) as f:
        return list(csv.DictReader(f))[-1]


CASES = {
    "fabric_probe_iso": dict(coupling=0.0),
    "fabric_probe_coup_a0": dict(angle=0.0, coupling=0.4),
    "fabric_probe_coup_a45": dict(angle=45.0, coupling=0.4),
    "fabric_probe_coup_a90": dict(angle=90.0, coupling=0.4),
    "fabric_probe_conformal": dict(conformal=True, volume=5.4),
    "fabric_probe_stiffaxial": dict(axial=1.0e6),
    "fabric_probe_softaxial": dict(axial=0.1),
    # Shape-response probes behind panel (c) of fig:fe-fabric-probe.
    "fabric_probe_a0": dict(angle=0.0, coupling=0.0),
    "fabric_probe_a45": dict(angle=45.0, coupling=0.0),
    "fabric_probe_a90": dict(angle=90.0, coupling=0.0),
}

FIELDS = ["B_par", "B_per", "ln_a", "ln_h", "J", "Jbar", "solid_fraction", "sigma11", "sigma22", "mass"]


def d4_matrix(angle_deg, kv, ka, kc):
    """Distention stiffness in the Mandel basis of the retained subspace."""
    _, e = basis(angle_deg)
    Dd = np.array([[kv, kc], [kc, ka]])
    D4 = np.zeros((6, 6))
    for i in range(2):
        for j in range(2):
            D4 += Dd[i, j] * np.outer(e[i], e[j])
    return D4


def orthonormal_mandel_basis(angle_deg):
    """Full orthonormal Mandel basis of symmetric tensors for the fabric triad."""
    a = np.radians(angle_deg)
    m = np.array([np.cos(a), np.sin(a), 0.0])
    p1 = np.array([-np.sin(a), np.cos(a), 0.0])
    p2 = np.array([0.0, 0.0, 1.0])

    def sym(x, y):
        return 0.5 * (np.outer(x, y) + np.outer(y, x))

    tensors = [np.eye(3) / np.sqrt(3.0), sym(m, m) - np.eye(3) / 3.0,
               sym(p1, p1) - sym(p2, p2), sym(p1, m), sym(p2, m), sym(p1, p2)]
    columns = [mandel(T) / np.linalg.norm(mandel(T)) for T in tensors]
    return m, np.column_stack(columns)


def symmetry_checks():
    """Decisive checks of the reduced (axisymmetric) distention stiffness.

    Transverse isotropy about m requires D:e3 = D:e6 on the coupled
    (p1-p2) Mandel pair; the reduction sets both to zero because the
    in-plane modes are frozen out. The checks are exact algebraic
    identities, evaluated numerically here.
    """
    angle, kv, ka, kc = 30.0, 1.0, 1.0, 0.4
    m, B = orthonormal_mandel_basis(angle)
    D4 = d4_matrix(angle, kv, ka, kc)
    e3, e6 = B[:, 2], B[:, 5]
    # 30 degree rotation about the fabric axis, as an orthogonal map on Mandel coords
    # expressed in the orthonormal basis B. Unit basis tensors are rebuilt from B so
    # that the induced map is orthogonal.
    phi = np.radians(30.0)
    K = np.array([[0.0, -m[2], m[1]], [m[2], 0.0, -m[0]], [-m[1], m[0], 0.0]])
    Q = np.eye(3) + np.sin(phi) * K + (1 - np.cos(phi)) * (K @ K)
    Rm = np.column_stack([mandel(Q @ tensor(np.eye(6)[k]) @ Q.T) for k in range(6)])
    # Fabric reconstruction for the coupled 45 degree probe. E_d = ln(a)/3 I + (1/2) ln H,
    # so H = a^{-2/3} exp(2 E_d).
    x = solve_probe(dict(angle=45.0, coupling=0.4))
    _, e = basis(45.0)
    edv = sum(x[i] * e[i] for i in range(2))
    Ed = tensor(edv)
    ln_a = float(np.sqrt(3.0) * x[0])
    values, vectors = np.linalg.eigh(Ed - (ln_a / 3.0) * np.eye(3))
    H = vectors @ np.diag(np.exp(2.0 * values)) @ vectors.T
    ln_h = -x[1] / np.sqrt(1.5)
    h = float(np.exp(ln_h))
    mt = np.array([np.cos(np.radians(45.0)), np.sin(np.radians(45.0)), 0.0])
    H_expected = h ** -2 * np.outer(mt, mt) + h * (np.eye(3) - np.outer(mt, mt))
    eigenvalues = np.sort(np.linalg.eigvalsh(H))
    return {
        "fabric_angle_deg": angle,
        "D4_e3_norm": float(np.linalg.norm(D4 @ e3)),
        "D4_e6_norm": float(np.linalg.norm(D4 @ e6)),
        "rotation_invariance_norm": float(np.linalg.norm(Rm @ D4 @ Rm.T - D4)),
        "reconstruction_case": "fabric_probe_coup_a45",
        "H_reconstruction_max_abs_diff": float(np.max(np.abs(H - H_expected))),
        "H_det_minus_one": float(np.linalg.det(H) - 1.0),
        "H_eigenvalues": [float(v) for v in eigenvalues],
        "H_eigenvalues_expected": [float(np.exp(-2.0 * ln_h)), h, h],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=DEFAULT_RUNS,
                        help="recorded MOOSE run tree (default: fe-evidence/runs)")
    args = parser.parse_args()
    runs = args.runs
    if not (runs / "fabric_probe_iso" / "solution.csv").is_file():
        raise SystemExit("no recorded pore-fabric runs under " + str(runs)
                         + "; pass --runs <recorded-run-tree>")

    report = {"cases": {}, "limits": {}, "conformal_cross_check": {}}
    report["tensor_checks"] = symmetry_checks()
    worst = 0.0
    for name, params in CASES.items():
        ref = run_case(params)
        row = last_row(runs, name)
        diff = {}
        for f in FIELDS:
            a, b = ref[f], float(row[f])
            diff[f] = abs(a - b)
            worst = max(worst, abs(a - b))
        report["cases"][name] = {"moose": {f: float(row[f]) for f in FIELDS},
                                 "independent": {f: ref[f] for f in FIELDS},
                                 "abs_diff": diff}

    # Limit 1: no coupling => isotropic Biot tensor with an isotropic mineral.
    n_iso = run_case(dict(coupling=0.0))
    report["limits"]["no_coupling_isotropic_biot"] = {
        "B_par": n_iso["B_par"], "B_per": n_iso["B_per"],
        "anisotropy": n_iso["B_par"] - n_iso["B_per"]}
    # Limit 2: coupling => transversely isotropic Biot tensor.
    c_an = run_case(dict(coupling=0.4))
    report["limits"]["coupling_gives_anisotropy"] = {
        "B_par": c_an["B_par"], "B_per": c_an["B_per"],
        "anisotropy": c_an["B_par"] - c_an["B_per"]}
    # Limit 3: frozen shape reproduces the isotropic Biot tensor.
    s_ax = run_case(dict(axial=1.0e6))
    report["limits"]["frozen_shape_isotropic_biot"] = {
        "B_par": s_ax["B_par"], "B_per": s_ax["B_per"],
        "anisotropy": s_ax["B_par"] - s_ax["B_per"]}

    # Limit 4: conformal reduction against the reviewed ConformalMaterial.
    ref = run_case(dict(conformal=True, volume=5.4))
    cm = last_row(runs, "conformal_probe_ref")
    rows = {}
    for f in ("J", "Jbar", "sigma11", "sigma22", "solid_fraction"):
        rows[f] = {"independent": ref[f], "ConformalMaterial": float(cm[f]),
                   "abs_diff": abs(ref[f] - float(cm[f]))}
    report["conformal_cross_check"] = rows

    report["worst_probe_abs_diff"] = worst
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "fabric-verification.json").write_text(json.dumps(report, indent=2) + "\n")

    print(f"{'case':26s} " + " ".join(f"{f:>12s}" for f in ("B_par", "B_per", "ln_h", "Jbar", "sigma22")))
    for name in CASES:
        r = report["cases"][name]
        print(f"{name:26s} " + " ".join(f"{r['independent'][f]:12.6g}" for f in ("B_par", "B_per", "ln_h", "Jbar", "sigma22")))
    print()
    print("limits:")
    for k, v in report["limits"].items():
        print(f"  {k}: anisotropy = {v['anisotropy']:.6e}")
    print("conformal reduction vs reviewed ConformalMaterial:")
    for f, v in report["conformal_cross_check"].items():
        print(f"  {f:14s} {v['independent']:20.12f} vs {v['ConformalMaterial']:20.12f}  diff {v['abs_diff']:.3e}")
    print()
    print("reduced-distention tensor checks:")
    for key, value in report["tensor_checks"].items():
        print(f"  {key:32s} {value}")
    print(f"\nworst probe-field absolute difference = {worst:.3e}")


if __name__ == "__main__":
    main()
