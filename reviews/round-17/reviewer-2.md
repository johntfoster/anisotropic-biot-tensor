# Round 17 — Reviewer 2 (physics / source fidelity + packaging completeness)

Independent AI-agent review of the frozen snapshot
`.agent-runtime/review-snapshots/round-17`
(SNAPSHOT_ID `faa3a2f488c5f117474072bb2de41b8de8e78a7cffbc8b51b449edec76292959`).
Prior-round verdicts were not consulted and carry no weight. All checks were
run against the frozen snapshot contents only.

## 1. Snapshot integrity

- `sha256(source-manifest.json)` =
  `faa3a2f488c5f117474072bb2de41b8de8e78a7cffbc8b51b449edec76292959`,
  identical to `SNAPSHOT_ID`. **PASS.**
- Re-hashed every file declared in `source-manifest.json`:
  **438 declared, 438 present and matching, 0 missing, 0 mismatch.**
  The only files not listed in the manifest are `SNAPSHOT_ID` and
  `source-manifest.json` themselves (self-referential, expected).

## 2. Referenced-artifact resolution

Every artifact a shipped document references was checked for presence and
digest:

- `fe-evidence/manifest.json` — **202/202** declared files resolve with
  matching SHA-256 (and matching declared byte counts). All 38 cases have a
  matching `runs/<case>/` directory; the 28 `not_applicable` entries are
  correctly absent from disk.
- `site/evidence.json` — **23/23** artifact `path`+`sha256` entries resolve;
  all referenced artifact IDs resolve; the five category blocks and
  `reproduction`/`limitations` arrays are present.
- `site/scientific-snapshot.json` — **33/33** listed source hashes resolve and
  are byte-for-byte consistent with the same paths in `source-manifest.json`
  (0 cross-manifest mismatches).
- Embedded supplement archive — see §3.

## 3. Supplement archive, packager, and PDF attachment

- Shipped `build/conformal-2026-09-20-v1.zip` SHA-256 =
  `b635be7667231fc2077fa7542663ddec1eee126fcd7290c2309222768649f981`,
  matching the `source-manifest.json` declaration.
- Re-ran `tools/package_numerical_supplement.py` on a writable copy of the
  snapshot: it reproduced the shipped archive **byte-for-byte**
  (`b635be76…f981`, 34 files). **Deterministic reproducibility PASS.**
- The PDF `build/main.pdf` embeds exactly one attachment
  (`conformal-2026-09-20-v1.zip`); the extracted attachment bytes hash to
  `b635be76…f981`, i.e. **identical to the shipped archive**. The packager
  README's `pdfdetach -saveall` claim is accurate.

## 4. Force / mass / platen balance claims vs raw run data

I recomputed the per-run diagnostics directly from each
`fe-evidence/runs/<case>/solution.csv` (using the same conventions encoded in
`moose_app/scripts/analyze_mandel.py`) and compared against the shipped
`analysis.json` and `site/reports/finite-deformation-summary.json`.

For every non-Mandel demonstration run (anisotropic 0/30/45/90, isotropic
comparison, partial 0/30), the recomputed values agree to machine precision
with the shipped records. Representative results:

| run | force_relative (recomputed) | discrete_mass_abs | mass_mobilized_rel | platen_equality |
|---|---|---|---|---|
| anisotropic_0 | 4.0001e-12 | 2.1824e-14 | 3.4965e-12 | 7.0e-16 |
| anisotropic_90 | 1.6430e-12 | 2.6449e-14 | 7.8647e-12 | 1.1e-15 |
| anisotropic_30_coarse | 1.2764e-10 | 3.5123e-13 | 2.4699e-10 | 3.2e-14 |
| isotropic | 3.2144e-12 | 2.6714e-14 | 7.5870e-12 | 9.0e-16 |
| partial_0 | 5.8571e-12 | 2.9007e-13 | 3.5611e-11 | 3.1e-14 |
| partial_30 | 2.0521e-10 | 3.2327e-13 | 4.6363e-10 | 2.4e-14 |

These exactly match the corresponding `analysis.json` fields and the family
aggregates in `finite-deformation-summary.json`
(anisotropic force_relative_max 1.2764e-10, partial 2.0521e-10, isotropic
3.2144e-12; partial mass_mobilized_rel max 4.6363e-10). **PASS.**

**Corrected force diagnostic.** The force convention is stated explicitly:
`expected_force = -a*q_L` (quarter, a=1) or `-2*a*q_L` (full domain, a=1).
For the full-domain demonstrations with `load=0.7`, `expected_force = -1.4`,
and `force_relative = max|top_reaction − applied_resultant| / |expected_force|`
is ≤ 1.3e-10 across all anisotropic runs and ≤ 2.1e-10 across partial runs.
The plate resultant is treated as an equilibrium residual of a
force-controlled rigid-platen problem, not as a "force-balance failure" —
this matches the wording in `site/evidence.json` ("the corrected plate
resultant is −2·a·q_L … an equilibrium residual, not a force-balance
failure"). **Corrected diagnostic is present and consistent.**

**Partial-drainage family marked not comparable.** Every
`partial_*` run's `analysis.json` carries `"reference_comparable": false` and
a `reference_note` stating the square domain `[-1,1]×[-1,1]` differs from the
slender Mandel reference `[-1,1]×[-0.1,0.1]`, so no Mandel-normalized field is
emitted. All 11 non-comparable demonstration runs (6 anisotropic + isotropic +
4 partial) correctly have **no** `reference_comparison.csv` on disk; only the
quarter-domain `mandel`-case runs carry one. The manuscript
`sections/finite_elements.tex` "Scope of these results" paragraph states the
same exclusion. **PASS.**

## 5. Acceptance-evidence internal consistency

- `mandel-reference.json`: **38** self-checks, all passed;
  `central_overshoot.ratio = 1.0546586069998425` (= 5.4659%) at
  `t = 0.01516535` — matches `site/evidence.json` (38 checks, 5.4659%).
- `fluid-coupling-verification.json`: `count = 110`,
  `maximum_scaled_error = 8.0867e-09` — matches "110 checks, max 8.09e-09".
- `cpp-python-constitutive.json`: `states = 41`,
  `value_absolute_error = 6.3949e-14` — matches "6.4e-14 over 41 states".
- `conformal-verification.json`: 186 checks, max constitutive-identity error
  2.455e-09; observed orders near 2.0 — internally consistent.
- `mms-convergence.json` spatial/temporal orders match the site summary
  (spatial ux/uy ≈ 2.99/3.00, p ≈ 2.00; temporal difference-orders bounded
  near one, with the mesh-step cross-term explanation).
- `figures/fe_load_limit.csv`: minimum normalized pressure error 3.2209e-3 at
  nx=20, dt=1e-3 — matches the stated ~3.2e-3 floor (a discretization floor,
  not decaying to the linear reference).

## 6. Overclaim / non-comparable-as-verification scan

- The finite-deformation category is correctly labelled `pending`; the
  physical-validation category `not_performed`; parameters synthetic. The
  rotated-anisotropy and partial-drainage cases are explicitly labelled
  "demonstrations," not quantitative verification.
- No non-comparable comparison is presented as verification: the only
  reference-normalized discrepancies emitted are for `case='mandel'` decks
  (the reference-modulus quarter-domain problem), and those are framed in the
  manuscript as an implementation check of the weak balances/constant tangent
  that "need not reproduce [the analytical] series at a finite load."
- No artifact digest fails to resolve; every shipped digest that a document
  cites was matched against bytes.

## Findings (non-blocking)

1. **NOTE** — `site/reports/mms-convergence.json` (and the identical
   `fe-evidence/mms-convergence.json`) records `runs_dir` as an absolute,
   host-specific path
   (`/home/jfoster/projects/…/.agent-runtime/moose-fe-goal-2026-09-20/…/runs`).
   Non-portable in a published artifact; no scientific or digest consequence.
2. **NOTE** — `site/evidence.json` lists seven `fe-*-data` /
   `mandel-reference-mandel-*` / `scientific-snapshot` artifacts that are
   allowlisted but not referenced by any category or figure. Permitted by the
   explicit allowlist design; cross-linking would improve auditability.
3. **NOTE** — The supplement archive version namespace
   (`conformal-2026-09-20-v1`) differs from the evidence-site namespace
   (`moose-fe-pending-2026-09-20`); both are dated consistently and describe
   different deliverables — not a contradiction.

No overclaim, no non-comparable comparison presented as verification, and no
unresolved artifact digest were found.

## Verdict

Zero required corrections; three NOTE items, all cosmetic/auditability-only.

VERDICT: ACCEPT
