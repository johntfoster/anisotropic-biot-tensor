# Round 20 — author response and revision matrix

Snapshot reviewed: `.agent-runtime/review-snapshots/round-20`
(`SNAPSHOT_ID 542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b`, 534 files).

Verdicts: Reviewer 1 MINOR REVISION · Reviewer 2 MINOR REVISION · Reviewer 3 **ACCEPT**.

Stop criterion (**>=2 exact ACCEPT**) is **not met**; this round produced one ACCEPT.
All three reports confirmed snapshot integrity (534/534 digests) and found the physics,
mathematics and evidence sound. Two required items remain, both confined to one reported
quantity's sign convention and to figure provenance. A revised snapshot must be reviewed in a
new round (round 21); votes are not carried across.

## Required findings (all accepted; none rebutted)

| ID | Reviewers | Location | Issue | Disposition |
| --- | --- | --- | --- | --- |
| B1 | R1-required-1 | `moose_app/include/utils/FabricLaw.h:599`; `FabricMaterial.C:67,105` | Reported `ln_h = xi/√1.5 = −ln h`; the manuscript's `E_d` equations fix `ln h` uniquely (`½I − 3/2 m⊗m = −√(3/2)e₁`), so the reported scalar has the opposite sign to the paper's `ln h` | TO APPLY — flip the sign at the source so the reported `ln_h` equals the paper's `ln h`, align `examples/verify_fabric.py` to the paper convention, then re-run and regenerate every `ln_h`-bearing artifact |
| B2 | R1-required-2, R2-required-1 | `figures/fe_fabric_probe.pdf` panel (c); `fe-evidence/runs`; `sections/experiments.tex` availability ¶ | Panel (c) and `figures/fe_fabric_probe.csv` draw `fabric_probe_a0/a45/a90`, whose run histories are absent from `fe-evidence/runs`, `fe-evidence/manifest.json` and the supplement archive; the documented regeneration reports "Shape-response probes absent" and yields a different figure | TO APPLY — materialize and register the three shape-probe run histories, ship them in the archive, and regenerate the figure and CSV from the shipped evidence tree |

## Optional findings

| ID | Reviewer | Disposition |
| --- | --- | --- |
| O1 | R1-optional-1 | TO APPLY — state explicitly which symmetric-tensor modes the five-modulus `D` leaves frozen (in-plane shear mode) so "full-rank `D`" phrasing agrees |
| O2 | R1-optional-2 | TO APPLY — note in `sec:fe-fabric` that `verify_fabric.py` is an implementation check sharing the modeling conventions |
| O3 | R1-optional-3 | TO APPLY — align the `3.2e-3` attribution wording between `main.tex` and `site/evidence.json` |
| R2-opt-1 | R2 | TO APPLY — refresh `site/reports/tensor-verification.json` so recorded NumPy versions agree |
| R2-opt-2 | R2 | TO APPLY — default `--runs` for the fabric scripts points at the shipped evidence tree |
| R2-opt-3 | R2 | TO CHECK — confirm the `dehghanipentamerodio2019` issue year against Crossref |
| R2-opt-4 | R2 | TO CHECK — confirm the Drumheller §8.9 and Gajo (3.27)/(3.32)/(3.34) anchors against the source papers |

## Verification

The revision pass rebuilds the application, re-runs the fabric decks so recorded evidence matches
the corrected source, re-materializes and registers the shape-probe runs, regenerates figures,
site manifests, and the supplement archive, rebuilds the manuscript, and records per-item
`file:line` confirmation plus the build and reproduction results. The next review round is frozen
from that rebuilt tree.

The next review round (round 21) is frozen from that rebuilt tree.
