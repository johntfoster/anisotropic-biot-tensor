# Round 26 — response to the three independent reviews

Snapshot reviewed: `.agent-runtime/review-snapshots/round-26`
SNAPSHOT_ID: `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907` (591 files;
591/591 re-hashed OK by all three reviewers).

## Verdicts (read from the report files on disk)

| Reviewer | Emphasis | Verdict | Required |
|----------|----------|---------|----------|
| 1 | mathematics / correctness | **ACCEPT** | 0 |
| 2 | physics / source fidelity / packaging | MINOR REVISION | 1 |
| 3 | prose / notation / significance | **ACCEPT** | 0 |

Accept count = **2**; the >=2 threshold is **met** on the round-26 snapshot.

Reviewers 1 and 3 independently confirmed the three round-25 fixes:
- R25-3-1: `\mathbf m` is defined at first use in `sec:fabric-biot` (`pore_fabric.tex:282–283`).
- R25-3-2: the distention-strain sentence is exactly right — with
  \(\mathbf E_{\mathrm{dis}}=(\ln a/3)\mathbf I+\ln h(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m)\),
  spectral exponentiation gives \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\)
  (a bare exponential would give \(\mathbf G^{1/2}\)), so the factor-of-two claim is correct.
- R25-2-1: "eigenvalue ratio" occurs 0 times in `main.tex` + `sections/`, 0 in
  `site/evidence.json`, 0 in `site/scientific-snapshot.json`.

Reviewer 1 also reproduced every quoted FE number from the frozen artifacts and found no
wrong sign, factor error, or failing identity; reviewer 3 found no genuine notation
collision in the fabric/distention symbol family.

## Required item and disposition

| # | Source | Item | Disposition |
|---|--------|------|-------------|
| F1 | reviewer-2 | The shipped `site/evidence.json` (23 artifacts / 7 figures / 3 cases / 0 "fabric" hits) and `site/scientific-snapshot.json` (45 files) were **not** the output of the shipped `tools/register_fabric_evidence.py` (41 / 13 / 5 / 78 hits / 47 files). 21 `figures/*` files plus `site/reports/fabric-verification.json` were unregistered against the allowlist `site/README.md` declares authoritative, so the companion site published none of the paper's pore-fabric evidence while the PDF-embedded supplement shipped all of it. Root cause: `tools/populate_site_manifest.py` wholesale replaces `manifest['artifacts']` and `manifest['figures']`, so running it *after* the fabric registration silently discards that registration. | **CLOSED.** Established and executed the correct order: `populate_site_manifest.py` → `register_fabric_evidence.py` → `build_verification_site.py`. Post-fix state on disk: `site/evidence.json` **41 artifacts / 13 figures / 5 cases**, `site/scientific-snapshot.json` **47 files**, **0 digest mismatches** in both, `build_verification_site.py` exit 0 with **41 artifacts** and **link check passed**. The four fabric figure artifacts (`fe_fabric_probe.png`, `fe_fabric_mandel.png`, `fe_fabric_contours.png`, `fe_fabric_diffusion.png`) plus `site/reports/fabric-verification.json` are registered, and "eigenvalue ratio" occurs 0 times in either manifest. |

No manuscript source (`.tex`, code, numbers, figures) was changed by this repair: F1 is a
companion-site manifest registration defect only.

## Optional items

Reviewer 1 recorded three OPTIONAL items (panel-(b) count/range wording; one over-strong
justification sentence about the frozen complementary modes; one cross-check note).
Reviewer 2 recorded two OPTIONAL items (a superseded limitation wording; the legacy key
name `H_eigenvalue_ratio_expected`). Reviewer 3 recorded eleven OPTIONAL editorial items
(duplicated implementation-check caveat; "shape of the mineral" vs "pore shape"; the
tautological `h=e^{\ln h}`; "unimodular eigenvalues" phrasing; implicit `e_4,e_5`;
intermediate-vs-mixture frame wording for `\bar{\mathbf S}_{\mathrm{dis}}`; residual
`H_eigenvalue_ratio_expected` field names; stiffness/compliance wording at
`pore_fabric.tex:297–300`; and others). None was a required correction; they are recorded
here for a future editorial pass and were not applied, to avoid churn on an otherwise
accepted tree.

## Note on the round-26 snapshot

The frozen round-26 snapshot captured the pre-fix companion-site manifests (23 artifacts),
because the site tooling had been run in the wrong order immediately before the freeze.
The F1 repair changed `site/evidence.json` and `site/scientific-snapshot.json`, so the tree
no longer matches the round-26 snapshot; the corrected tree is re-frozen as **round-27**
and receives one fresh independent re-review before delivery. The manuscript sources and
`build/main.pdf` (sha256 `db90490c…f0c1`, 33 pages, 0 undefined, 0 overfull) are unchanged
between round-26 and round-27.
