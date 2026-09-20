#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Parent-owned analysis helper (not part of moose_app/ or validation/ source).
# Reproduces the MMS observed-order measurement from run analysis.json files.
#
# Why the difference method: each run's ElementL2Error is measured against the
# exact manufactured solution, so the reported norm contains a mesh-dependent
# floor E_h (identical for a fixed h) plus a time-step contribution E_t(dt).
# Refining dt alone therefore leaves the naive ratio E(dt)/E(dt/2) near 1.
# E(dt)-E(dt/2) cancels E_h to leading order and isolates the temporal part,
# so the observed temporal order is log2(D(dt)/D(dt/2)) with D the successive
# norm deficits. The naive ratios are reported alongside for contrast.
#
# Run resolution: the runs live in the distributed layout
#   <runtime>/implementation/runs/<run>/analysis.json
# in the live repository, but the frozen review snapshot copies them to
#   fe-evidence/runs/<run>/analysis.json
# so this script searches several known roots (plus --runs / $MMS_RUNS) and
# FAILS LOUDLY (exit 2) when any required run is missing. It never silently
# emits a partial convergence table.
import argparse, json, math, os, sys
from pathlib import Path

VARS = ("ux_l2", "uy_l2", "p_l2")
SPACE_NX = (4, 8, 16)
TIME_SERIES = ((16, "mms_time"), (32, "mms_time_fine32"), (64, "mms_time_fine64"))
TIME_DTS = (0.02, 0.01, 0.005)

REQUIRED = [f"mms_space_{n}" for n in SPACE_NX] + [
    f"{prefix}_{dt:g}" for _, prefix in TIME_SERIES for dt in TIME_DTS
]
SENTINEL = REQUIRED[0]


def candidate_roots(explicit):
    here = Path(__file__).resolve()
    roots = []
    if explicit:
        roots.append(Path(explicit))
    env = os.environ.get("MMS_RUNS")
    if env:
        roots.append(Path(env))
    for base in [here.parent, here.parent.parent, here.parent.parent.parent, Path.cwd()]:
        for rel in ("implementation/runs", "fe-evidence/runs", "runs",
                    "examples/runs", "moose_app/runs"):
            roots.append(base / rel)
    seen, uniq = set(), []
    for r in roots:
        k = str(r)
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    return uniq


def resolve_runs(explicit):
    tried = []
    for root in candidate_roots(explicit):
        tried.append(str(root))
        if (root / SENTINEL).is_dir():
            return root, tried
        if explicit and str(root) == str(Path(explicit)):
            sys.stderr.write(
                f"ERROR: --runs {explicit} does not contain the sentinel run "
                f"'{SENTINEL}'. Refusing to fall back to another location.\n")
            sys.exit(2)
    sys.stderr.write(
        "ERROR: could not locate MMS runs.\n"
        f"       No candidate root contained the sentinel run '{SENTINEL}'.\n"
        "       Roots tried:\n" + "".join(f"         - {t}\n" for t in tried) +
        "       Pass --runs <dir> or set $MMS_RUNS to the directory holding the\n"
        "       run subdirectories\n")
    sys.exit(2)


def load(runs, name):
    p = runs / name / "analysis.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def order(pairs):
    # pairs: list of (level, data) ordered from coarsest to finest
    out = {}
    for v in VARS:
        e = [p[1][v] for p in pairs]
        rec = {"levels": [p[0] for p in pairs], "norms": e}
        rec["naive_orders"] = [math.log2(e[i] / e[i + 1]) for i in range(len(e) - 1)]
        d = [e[i] - e[i + 1] for i in range(len(e) - 1)]
        rec["norm_deficits"] = d
        rec["difference_orders"] = (
            [math.log2(d[i] / d[i + 1]) for i in range(len(d) - 1)] if len(d) > 1 else []
        )
        out[v] = rec
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Reproduce the MMS observed-order measurement from run analysis.json files.")
    ap.add_argument("--runs", help="directory holding the mms_* run subdirectories")
    ap.add_argument("--out", help="output JSON path (default: alongside this script)")
    args = ap.parse_args()

    runs, tried = resolve_runs(args.runs)
    missing = [n for n in REQUIRED if not (runs / n / "analysis.json").exists()]
    if missing:
        sys.stderr.write(
            f"ERROR: runs directory resolved to {runs}, but {len(missing)} required run(s) "
            "are missing or have no analysis.json:\n" + "".join(f"         - {m}\n" for m in missing) +
            "       Refusing to emit a partial convergence table.\n")
        sys.exit(2)

    result = {
        "method": "successive differences of exact-solution L2 error norms at fixed mesh",
        "runs_dir": str(runs),
        "required_runs": REQUIRED,
        "space": {},
        "time": {},
    }
    space_pairs = [(n, load(runs, f"mms_space_{n}")) for n in SPACE_NX]
    result["space"]["configs"] = [(n, d["nx"], d["dt"], d["end"]) for n, d in space_pairs]
    result["space"]["orders"] = order(space_pairs)

    for nx, prefix in TIME_SERIES:
        pairs = [(dt, load(runs, f"{prefix}_{dt:g}")) for dt in TIME_DTS]
        result["time"][f"nx{nx}"] = {
            "configs": [(d["dt"], d["end"]) for _, d in pairs],
            "levels": len(pairs),
            "orders": order(pairs),
        }

    outp = Path(args.out) if args.out else Path(__file__).resolve().parent / "mms-convergence.json"
    outp.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"\nwrote {outp}", file=sys.stderr)


if __name__ == "__main__":
    main()
