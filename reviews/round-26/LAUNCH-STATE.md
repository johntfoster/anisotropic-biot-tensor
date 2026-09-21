# Round 26 — launched (fresh independent re-review after the round-25 revision pass)

Snapshot: `.agent-runtime/review-snapshots/round-26`
SNAPSHOT_ID: `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907`
Files: 591

## Why round 25 does not count here

Round 25 (SNAPSHOT_ID `5035dd19…`) returned 1 exact ACCEPT + 2 MINOR REVISION (three
required items), so the >=2 threshold was not met and a revision pass followed
(`reviews/round-25/response.md`). The tree changed, so no round-25 vote carries forward.
Counting only exact ACCEPT verdicts on the round-26 snapshot; >=2 required.

## What changed since round 25

| Item | Fix |
|------|-----|
| R25-2-1 | `tools/register_fabric_evidence.py` limitation string rewritten and made idempotent (drops the stale entry instead of only not re-adding it); `site/evidence.json` and `site/scientific-snapshot.json` regenerated. "eigenvalue ratio" now occurs 0 times in either file. |
| R25-3-1 | `sections/pore_fabric.tex` (`sec:fabric-biot`): `\mathbf m` is now defined at first use — "…and the axial (degree-two) direction \(\mathbf e_2=\sqrt{3/2}(\mathbf m\otimes\mathbf m-\mathbf I/3)\), where \(\mathbf m\) is the unit material fabric axis". |
| R25-3-2 | `sections/pore_fabric.tex` (`sec:fabric-transverse`): the claim attached to `eq:fabric-transverse-strain` now reads "twice whose exponential, \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\), reconstructs \eqref{eq:fabric-transverse-h}, whose unimodular eigenvalues are \(h^{-2},h,h\)." (Reviewer 1 of round 25 independently verified \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G\) to 6.7e-16.) |

The optional items recorded by round-25 reviewers (three from reviewer 1, two from
reviewer 2, nine from reviewer 3) were deliberately **not** applied — none was a required
correction and applying them would add churn; they are listed in
`reviews/round-25/response.md` for a future editorial pass.

## Rebuild after the fixes

- `build/main.pdf` rebuilt: 33 pages, 0 undefined references, 0 undefined citations,
  0 overfull boxes; sha256 `db90490c04a7af322087e841dd01eac194de27f46a8baf49305859f5a57fe0c1`.
- `site/evidence.json`, `site/scientific-snapshot.json` regenerated; site rebuilt with
  `tools/build_verification_site.py` (exit 0, link check passed).
- `build/anisotropic-biot-2026-09-20-v2.zip` unchanged (69 files, sha256
  `46ef65aa…c54`) — it is the numerical supplement and contains no manuscript sources; it
  is embedded into `main.pdf` as an attachment.

## Watcher pre-launch verification (read-only)

- `sha256(source-manifest.json)` = `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907`,
  identical to the declared SNAPSHOT_ID; 591 entries; `missing []`.
- No other writer process active in the repository at launch time (checked `ps`).
- Snapshot frozen immediately after the rebuild, with zero writer activity between the
  rebuild and the freeze.

## Rules for this round

- Prior rounds (18–25) reviewed earlier snapshots and do not carry forward.
- Counting only exact ACCEPT verdicts on the round-26 snapshot; >=2 required.
- Three fresh independent reviewers, complementary emphasis:
  (1) mathematics/correctness; (2) physics/source fidelity/packaging;
  (3) prose/notation/significance.
- Reviewers must not read other reviewers' reports or prior-round verdicts, and must not
  modify the snapshot or the working tree (work from a temporary copy).
- Reports: `reviews/round-26/reviewer-{1,2,3}.md`, each ending with a `VERDICT:` line.

## Specific focus for this round

Confirm independently that (a) the round-26 snapshot re-hashes clean; (b) the three
round-25 required fixes are present, correct, and remain prose/documentation-only with no
change to any equation, number, or claim; (c) no statement about `ln h`, the fabric tensor
`H`, or the distention strain contradicts any equation in the paper; (d) every quoted
number still reproduces from the frozen artifacts. Note that the previously cited
"eigenvalue ratio" phrasing must be absent from the manuscript **and** from the shipped
`site/evidence.json`.
