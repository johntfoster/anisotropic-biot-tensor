# Simulated JMPS review — reviewer 1, round 1

**Overall verdict: ACCEPT**

This is an independent simulated peer review, not a journal decision. ACCEPT here means that I found no substantive change necessary within the manuscript's stated theoretical scope. The optional comments below are not conditions of acceptance.

## Scope and assessment

I reviewed `main.tex`, `sections/experiments.tex`, both example scripts, `VISION.md`, the repository instructions, and `references/notes/novelty-evidence.md`, against the snapshot recorded in `reviews/round-1/source-sha256.txt`. I applied the derivation-auditor and manuscript-narrative-review guidance. My emphasis was thermodynamic conjugacy, the constrained energy, unjacketed compatibility, stability qualifications, and the distinction between pressure tangents and finite pressure changes. I did not independently repeat the historical full-text citation audit or conduct a comprehensive priority search. In particular, the evidence note's full-text access gap for Foster–Xu remains a limitation of my literature assessment. No manuscript or code was edited.

The paper is mathematically sound under its explicit assumptions. Its strongest contribution is a coherent constitutive compatibility analysis: a law that reproduces a familiar Biot stress coefficient can still have an incorrect mineral-volume response, and the paper identifies precisely which reduced curvature has been misidentified. The finite-deformation examples then demonstrate the consequences of retaining the equilibrated volume coordinate, using a fully specified objective potential and independently checked derivatives. The analysis is appropriately limited to an elastic one-solid/one-fluid system with isotropic distention for the daughter-energy specialization.

The novelty is incremental and constitutive. Neither finite-strain volume conjugacy nor anisotropic effective stress is a new principle here; the introduction, comparison table, and discussion explicitly acknowledge this. I regard the explicit constrained-mineral decomposition, its compatibility diagnosis, and its reproducible finite-state realization as a useful theoretical contribution. The manuscript should continue to be judged on those narrower results, rather than on the mere existence of a tensor Biot coefficient.

## Independently checked mathematical results

1. **Pressure conjugacy and stress.** At fixed skeleton deformation, the stationary function is `W(F,q) + phi_s0 p exp(q)`. Its envelope has pressure derivative `phi_s0 exp(q)`, while subtracting `p J` gives the total fixed-pressure potential. Consequently its mixed derivative gives `P_p = phi_s0 (Jbar)_F - J F^{-T}`, and pushing forward at fixed F gives precisely `sigma_p = -B`. This checks the signs, reference normalization, and distinction between the two effective stresses in `main.tex:197–356`. In particular, the identity `sigma''_p = p B_p` is consistent with the decomposition; the paper does not incorrectly identify `sigma''` with a pressure-independent drained stress.

2. **Objectivity and symmetry.** An objective scalar equilibrated mineral volume has zero variation under `delta F = Omega F` for skew Omega. Thus `(Jbar)_F F^T` is symmetric, and its rotation covariance follows directly. The proof in `main.tex:352–386` is sufficient under the stated objective-energy and selected-branch assumptions. Material anisotropy does not invalidate this argument.

3. **Constrained daughter-energy reduction.** Direct substitution of `eta = Pdev:e + q I/3` into the bilinear energy gives `Cc = C + D:Pdev + Pdev:D^T + Pdev:H:Pdev`, `g = (D:I + Pdev:H:I)/3`, and `h = I:H:I/9`. These are the manuscript's formulas in `main.tex:517–535`; no major symmetry of D was silently used. Eliminating q gives the stated Schur complement and `B0 = I + phi_s0 g/h`. The stability statement requires the positive condensed stiffness and positive h, and correctly avoids claiming that separately positive daughter blocks suffice (`main.tex:547–570`).

4. **Mineral anisotropy.** Holding the specified daughter decomposition fixed, the mineral contribution to the mixed tangent is exactly its volumetric–deviatoric block. Purely deviatoric anisotropy therefore cannot alter B0 when that block, h, and D are held fixed. This is a conditional statement, not a general homogenization theorem, and the manuscript preserves that qualification (`main.tex:596–635`, `809–817`; `sections/experiments.tex:4–43`).

5. **Unjacketed compatibility.** Substituting `e = -p a` into `sigma = Cd:e - p B0` yields `B0 = I - Cd:a`. Substitution of both `e = -p a` and `q = -p tr(a)` into mineral equilibrium yields `g:a + h tr(a) = phi_s0`. Combining these independently recovers `h = phi_s0^2/[phi_s0 tr(a) - a:Cd:a]`, including its strict positivity condition. In the isotropic limit this is `phi_s0^2 Ks^2/(phi_s0 Ks-K)`. The stress-only calibration instead yields exactly the extra factor in the predicted q shown in `main.tex:729–734`. I found no missing factor of three or solid fraction in `main.tex:669–756`.

6. **Storage consistency.** Linearizing `Phi = J - phi_s0 exp(q)` and eliminating q gives `delta Phi = B0:e + phi_s0^2 p/h`. The fluid compressibility term then gives the stated fluid-content increment. Under compatible isotropic tangents, the solid storage is `(phi_s0 - K/Ks)/Ks`, equivalently `(B-phi_f0)/Ks`. This independent check supports the physical interpretation of the compatibility correction (`main.tex:777–794`).

7. **Finite realization and limits.** For the example energy, the q residual has derivative `h + phi_s0 p exp(q) > 0` for nonnegative p and has opposite signs at the two infinite limits. The unique scalar equilibrium and condensed logarithmic Hessian follow as stated. On coaxial paths the stress includes `phi_s0 exp(q) r/J`, whereas its pressure tangent includes the additional `1/(1+z)` factor. Differentiating the equilibrium explicitly recovers that factor. The reference parameters satisfy both compatibility conditions. The confined-layer small-pressure slopes follow directly from its traction condition (`sections/experiments.tex:45–119`, `190–220`).

## Numerical verification

I ran `.agent-runtime/venvs/numerics/bin/python examples/verify_tensor.py` successfully. Maximum absolute discrepancies were 7.0061e-8 for the pressure derivative, 2.6911e-9 for the volume derivative, 2.6077e-10 for the potential gradient, 3.9746e-14 for rotation, 7.8469e-17 for symmetry, 5.6843e-14 for daughter-energy reduction, zero for the reference compatibility residual, and 9.4591e-14 for coaxial agreement. The smallest sampled acoustic eigenvalue was 2.10654 in the stated stress unit across 28 states and 103 directions per state.

I inspected the implementation: the general tensor verification uses the spectral derivative of the matrix logarithm and finite differences of the condensed potential, rather than merely evaluating the coaxial expression twice. It shares material constants and the scalar root solver with the example generator, so “independent” means an independent tensor/derivative evaluation, not an entirely separate implementation. This is adequate for the claimed verification scope. The sampled acoustic test is not a proof of ellipticity over every state or direction, and the paper explicitly says so.

## Blocking findings

None found. I do not require experiments or a complete pore-scale homogenization for acceptance of this expressly theoretical constitutive paper. Neither should its synthetic examples be interpreted as establishing material accuracy.

## Optional editorial suggestions and limitations

- At `main.tex:789–792`, writing the compatible solid storage also as `(B-phi_f0)/Ks` would make its relationship to familiar linear poroelastic notation immediately recognizable. This would clarify that the compatibility equation represents the required classical storage response in the mineral-volume coordinate, not an additional universal poroelastic principle.
- At `sections/experiments.tex:290`, omit “corrected” from “corrected daughter-energy reduction”; a reader of the published paper does not need a reference to development history.
- The finite model is calibrated for compatibility at the reference state only. Its large finite-pressure paths are constitutive predictions, not a demonstration of exact finite-pressure homogeneous-mineral equivalence. The section title and discussion already make this limitation clear; it must not be lost in later revisions.
- The restricted daughter model and the compatible extended model have different interpretations of h. The paper explains this at `main.tex:736–756`; maintaining that distinction is essential. Likewise, no inference that isolated mineral anisotropy is uniquely identifiable from B0 is warranted, and the discussion correctly rules it out.
