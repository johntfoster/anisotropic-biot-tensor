# Weighted-stress reconsideration — 2026-09-19

## User correction and source evidence

The user rejected the preceding reconstruction for departing from the
companion's volume-fraction-weighted stress and equivalent volumetric energy
argument, and for excessive notation and unsuitable tensor typography/prose.
Round-4 ACCEPT votes do not validate this reconsideration.

Read the companion's current canonical root, macros, agent instructions,
author profile, elastic derivation, and Gajo equivalence appendix. The source
sequence is: current phase stress sum; single-prime effective stress; multiply
by J and use J phi_s = phi_s0 Jbar; change virtual work from (J,Jbar) to
(a,Jbar); cancel pressure work; integrate mineral work at fixed a; use the
zero-pressure skeleton law to determine distention energy; differentiate at
fixed skeleton deformation. Plastic factors are set to the identity here.
Source identity and labels are recorded in the manifest beside this note.

## Replacement and mathematical scope

The previous assumed logarithmic tensor-spring construction has been
removed from the manuscript. Its independent mineral strain and helper
operators are not used. Current sections 2–4 follow the source's stress/work
sequence, with a = det A and A = a^(1/3) I. Full mineral variations extend
the volume-work calculation using the prescribed anisotropic mineral law.
They give W_s = W_A(a) + phi_s0 Wbar_s(Fbar). The work equality retains the
full spatial stress, not just its trace.

Spherical distention restricts the complete drained compliance difference
to [1-K/(phi_s0 Ks)] I tensor I/(9K). K and Ks denote spherical-strain
stiffnesses in anisotropy; they need not equal hydrostatic-stress bulk
moduli. Compatible examples are reconstructed from that restriction.
An isotropic mineral cannot produce an anisotropic drained skeleton through
this deformation mechanism alone. Additional pore-shape deformation needs
its own law. This is stated as a physical limitation, not bypassed with an
unverified tensor balance.

## Citation update

The companion title is now *Pressure coupling and the Biot coefficient in
finite-strain poroelasticity and poroplasticity*. Its unpublished citation
was updated to the inspected September 19 version.

The original Gajo (2010) PDF was inspected, including pp. 3072–3074,
equations (3.27), (3.28)–(3.34). Its logarithmic constituent law, phase stress
relation, and elimination of the two volume factors support the scalar
correspondence stated here. The PDF is stored locally as
`references/pdfs/gajo-2010-compressible-constituents.pdf`.
The previous 23-entry reference audit remains historical evidence at its
stated access levels; it does not imply access to every original full text.

## Checks before the fresh reviews

Both new numerical suites pass. Across 273 finite tensor states and 13
mineral stiffnesses, the independent phase-stress/energy derivative error
is below 9e-10 and the pressure derivative error below 2e-9. Twenty additional
mineral stiffnesses exercise drained compatibility, virtual-work equivalence,
reference coefficients, and the finite unjacketed path. Incompatible pairs
are explicitly rejected. No numerical trace-only substitute is used.

All active tensor notation uses `\mathbf{}`. LuaLaTeX's unicode-math is
configured to render both Latin and Greek tensors upright and bold.
Five relevant companion skills were recovered from pinned Git objects and
adapted under distinct local names before the derivation was rewritten.
Fresh independent reports are required on this revised manuscript.
