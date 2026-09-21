# Round 27 — launched (confirmation round after the F1 companion-site repair)

Snapshot: `.agent-runtime/review-snapshots/round-27`
SNAPSHOT_ID: `c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e`
Files: 591

## Why round 26 does not count here

Round 26 (SNAPSHOT_ID `6e1afd93…`) returned **2 exact ACCEPT + 1 MINOR REVISION**, so the
>=2 threshold was met, but the dissenting reviewer's single required item (F1) was a real
companion-site registration defect: `tools/populate_site_manifest.py` wholesale replaces
`manifest['artifacts']` and `manifest['figures']`, so running it *after*
`tools/register_fabric_evidence.py` silently discarded the pore-fabric registration, and
the frozen round-26 snapshot captured that state (23 artifacts / 7 figures / 0 "fabric"
hits). The repair changed `site/evidence.json` and `site/scientific-snapshot.json`, so the
tree no longer matches the round-26 snapshot and no round-26 vote carries forward.
Counting only exact ACCEPT verdicts on the round-27 snapshot; >=2 required.

## What changed since round 26

**Companion-site registration only — no manuscript source, code, number, or figure changed.**

- Established and executed the correct order: `populate_site_manifest.py` →
  `register_fabric_evidence.py` → `build_verification_site.py`.
- `site/evidence.json`: **41 artifacts / 13 figures / 5 cases**; `site/scientific-snapshot.json`:
  **47 files**; **0 digest mismatches** in both; site rebuilt with **link check passed**.
- The four fabric figure artifacts (`fe_fabric_probe.png`, `fe_fabric_mandel.png`,
  `fe_fabric_contours.png`, `fe_fabric_diffusion.png`) and
  `site/reports/fabric-verification.json` are registered.
- "eigenvalue ratio" / "unimodular fabric eigenvalue ratio" occurs **0** times in the
  manuscript sources **and** in both site manifests.
- `build/main.pdf` is unchanged from round 26: sha256
  `db90490c04a7af322087e841dd01eac194de27f46a8baf49305859f5a57fe0c1`, 33 pages,
  0 undefined references, 0 undefined citations, 0 overfull boxes.

Manuscript sources and `build/main.pdf` are byte-identical to round 26; only
`site/evidence.json`, `site/scientific-snapshot.json`, the rebuilt `.agent-runtime/site`
output, and the F1 tooling/response records differ.

## Standing disposition of earlier items

The three round-25 required items were closed in the round-25 revision pass and
independently confirmed by round-26 reviewers 1 and 3. The optional items recorded in
rounds 25 and 26 (three from round-26 reviewer 1, two from round-26 reviewer 2, eleven
from round-26 reviewer 3) were deliberately not applied (no required correction; churn
avoidance) and are listed in `reviews/round-25/response.md` and
`reviews/round-26/response.md`.

## Rules for this round

- Prior rounds (18–26) reviewed earlier snapshots and do not carry forward.
- Counting only exact ACCEPT verdicts on the round-27 snapshot; >=2 required.
- Three fresh independent reviewers, complementary emphasis:
  (1) mathematics/correctness; (2) physics/source fidelity/packaging;
  (3) prose/notation/significance.
- Reviewers must not read other reviewers' reports or prior-round verdicts, and must not
  modify the snapshot or the working tree (work from a temporary copy).
- Reports: `reviews/round-27/reviewer-{1,2,3}.md`, each ending with a `VERDICT:` line.

## Specific focus for this round

Confirm independently that (a) the round-27 snapshot re-hashes clean; (b) the F1 repair is
real and complete — `site/evidence.json` registers the pore-fabric artifacts and figures
with resolving digests, and `tools/register_fabric_evidence.py` run after
`populate_site_manifest.py` reproduces that state; (c) no statement about `ln h`, the
fabric tensor `H`, or the distention strain contradicts any equation; (d) every quoted
number still reproduces from the frozen artifacts.
