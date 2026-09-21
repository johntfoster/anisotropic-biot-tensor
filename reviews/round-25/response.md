# Round 25 — response to the three independent reviews

Snapshot reviewed: `.agent-runtime/review-snapshots/round-25`
SNAPSHOT_ID: `5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd` (591 files;
591/591 re-hashed OK by all three reviewers).

## Verdicts (read from the report files on disk)

| Reviewer | Emphasis | Verdict | Required |
|----------|----------|---------|----------|
| 1 | mathematics / correctness | **ACCEPT** | 0 |
| 2 | physics / source fidelity / packaging | MINOR REVISION | 1 |
| 3 | prose / notation / significance | MINOR REVISION | 2 |

Accept count = **1**; the >=2 threshold is **not met**. Both reviewers who withheld
acceptance said explicitly that the required items are one-line fixes with no effect on
any equation, number, or claim. A revision pass was therefore run on the three items and
the tree was re-frozen as **round-26** for a fresh independent re-review.

## Required items and disposition

| # | Source | Item | Disposition |
|---|--------|------|-------------|
| R25-2-1 | reviewer-2 | The superseded `R24-3-1` wording still shipped in `site/evidence.json` (limitations[5]) and was still emitted by `tools/register_fabric_evidence.py`, so the launch-state claim that the phrase "no longer occurs" was false. | **CLOSED.** Rewrote the limitation string in `tools/register_fabric_evidence.py` ("…the reported shape scalar is the logarithm of the unimodular transverse fabric eigenvalue.") and made the append **idempotent** so the stale entry is dropped rather than merely not re-added. Regenerated `site/evidence.json` and `site/scientific-snapshot.json`; the string "eigenvalue ratio" now occurs **0 times** in either file. |
| R25-3-1 | reviewer-3 | `\mathbf m` is used in `sec:fabric-biot` (in `\mathbf e_2` and in "the plane normal to `\mathbf m`") but only defined a subsection later in `sec:fabric-transverse`. | **CLOSED.** Defined at first use in `sec:fabric-biot`: the axial direction is now "…and the axial (degree-two) direction \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\), where \(\mathbf m\) is the unit material fabric axis". The later definition in `sec:fabric-transverse` remains as the formal setup of that subsection. |
| R25-3-2 | reviewer-3 | The sentence attached to `eq:fabric-transverse-strain` said "whose exponential reconstructs \eqref{eq:fabric-transverse-h}", but with \(\mathbf E_{\mathrm{dis}}=\tfrac12\ln\mathbf G\) only \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\) reproduces the quoted eigenvalues. | **CLOSED.** The sentence now reads "twice whose exponential, \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\), reconstructs \eqref{eq:fabric-transverse-h}, whose unimodular eigenvalues are \(h^{-2},h,h\)." Reviewer 1 had independently verified \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G\) to 6.7e-16, so the corrected statement matches the verified identity. |

## Optional items

Reviewer 1 recorded three OPTIONAL items (the "one above one" wording vs several temporal
orders above unity; `FabricLaw.h` reporting a constant `stability` diagnostic where
`ConformalLaw.h` reports the pressure-dependent branch derivative; `FabricLaw.h`'s
small-strain `\mathbf P=\boldsymbol\sigma` convention worth a one-line comment).
Reviewer 2 recorded two OPTIONAL nits (`H_eigenvalue_ratio_expected` key name in
`fabric-verification.json`; `fe-evidence/README.md` not listed in `fe-evidence/manifest.json`).
Reviewer 3 recorded nine OPTIONAL prose/notation observations. These are **not** applied in
this pass: none is a required correction, they were not carried as accepted-work items, and
applying five-to-twelve further edits would add churn and require another full re-freeze.
They are recorded here for a future editorial pass.

## Rebuild and re-verification after the three fixes

| Check | Result |
|-------|--------|
| `latexmk -lualatex … -outdir=build main.tex` | exit 0; **33 pages**; 0 undefined references; 0 undefined citations; 0 overfull boxes |
| `build/main.pdf` sha256 | `db90490c04a7af322087e841dd01eac194de27f46a8baf49305859f5a57fe0c1` |
| `site/evidence.json`, `site/scientific-snapshot.json` | regenerated; "eigenvalue ratio" **0** occurrences |
| `tools/populate_site_manifest.py` | exit 0 |
| `tools/build_verification_site.py` | exit 0; 23 artifacts; **link_check passed** |
| `build/anisotropic-biot-2026-09-20-v2.zip` | 69 files, sha256 `46ef65aad77df01de64054108c5a0b0ec4a91718a73123f620f1793f6cba2c54` — unchanged, as expected: it is the numerical supplement (no manuscript sources), and it is embedded into `main.pdf` as an attachment rather than containing the manuscript |
| residual search `unimodular fabric eigenvalue ratio` outside `reviews/` and `.agent-runtime/` | none |

## Next step

Freeze **round-26** on this revised tree and run a fresh three-reviewer independent round
(>=2 exact ACCEPT required) before delivering the accepted PDF.
