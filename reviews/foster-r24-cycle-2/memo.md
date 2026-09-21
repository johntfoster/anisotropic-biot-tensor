Foster reviewer/editor cycle 2 (round-24) — memo (findings)

Manuscript: anisotropic Biot tensor from mineral stress and distention work
Repository: /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor
Base snapshot: round-24 `1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423`

## Concurrent-writer condition (report, not a normal cycle)

This cycle made **zero manuscript edits** and did not complete a normal
prose pass, because a second writer modified two of the seven manuscript
sources while this cycle was running.

At start (22:36 CT) the single-writer check passed: `pgrep -af 'opencode run'`
returned no `opencode run` process. During the cycle, `sections/pore_fabric.tex`
(mtime 22:37:37) and `sections/finite_elements.tex` (mtime 22:37:38) changed on
disk with no edit from this writer. The change is exactly the R24-3-1 fix that
this cycle was instructed NOT to make and to leave for the parent:

- `sections/pore_fabric.tex`: "the reported shape scalar is the unimodular
  fabric eigenvalue ratio \(\ln h\), not a projection of it." was rewritten to
  "…the reported shape scalar is the logarithm of the unimodular transverse
  fabric eigenvalue \(h=\mathrm{e}^{\ln h}\), not a projection of it," and the
  sentence now carries the explicit reconstruction
  \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\) with
  "whose unimodular eigenvalues are \(h^{-2},h,h\)".
- `sections/finite_elements.tex`: the `fig:fe-fabric-probe` caption now reads
  "…exactly the logarithm of the unimodular transverse fabric eigenvalue
  \(h=\mathrm{e}^{\ln h}\) of \eqref{eq:fabric-transverse-h}."

Concurrently a round-25 launch appeared on disk:
`.agent-runtime/review-snapshots/round-25/` (SNAPSHOT_ID
`5035dd198266c12544140e47381da3e9390c7d1e68c00a06009e85ba6052f9dd`, 591 files)
and `reviews/round-25/{LAUNCH-STATE.md,reviewer-2.md,reviewer-3.md}` (written
22:38–22:45). The launch document describes "Round 25 — fresh independent
re-review" of the "revised post-Foster-cycle tree," i.e. the parent has moved
the manuscript past the round-24 snapshot this cycle targets.

Per the standing instruction ("if another writer is active, stop and report
rather than becoming a second writer"), this cycle stopped before making any
source edit. No equation, symbol, label, citation, number, or claim was
changed by this cycle, because nothing was changed by this cycle.

## Prose findings (recorded, zero edits applied)

A read-only prose scan found no high-value authorial/editorial improvement to
make, independent of the concurrent-writer stop. Confirmed clean:

- No repeated words, no non-leading double spaces, no `its`/`it's` errors,
  no "in order to / the fact that / it should be noted / due to the fact",
  no development-note phrasing, no "principal/principle" or
  "distention/distension" inconsistency (uniformly "distention").
- The known terminology fix from cycle 1 ("transversely isotropic") is
  retained and not reversed.
- R24-3-1 (the description of \(\ln h\) as the "unimodular fabric eigenvalue
  ratio" versus the equation's eigenvalues \(h^{-2},h,h\), so the log
  eigenvalue ratio is \(-3\ln h\)) is RECORDED here as the known open item.
  This cycle left the text alone, per instruction; the parent's round-25
  revision has since changed that wording in both files.

## Integrity note

counts-before.txt was captured on the round-24+cycle-1 state. The two fabric
files changed between the before and after verifier runs, but the change is
the concurrent writer's R24-3-1 wording edit, not this cycle. The seven
fixed-string count columns and the digit-literal multisets are identical
before and after (the R24-3-1 rewrite adds no label/ref/cite/equation and no
digit literal). See counts-after.txt and cycle-report.md for the programmatic
proof.
