# Review of the source manuscript's new references

Date: 2026-09-18. Scope: all **23** bibliography keys present in the source
manuscript's `all.bib` and absent from this paper's bibliography at the start
of this revision. Source bibliography SHA-256:
`47954bac64165fffec0ee9f23dcb8dddef25a542f91b3bf02f9948f85cb1fb90`.
The original inventory and retrieval logs are in
`.agent-runtime/research/stress-reconstruction/`.

This is a relevance and claim-support review of every new entry, not a claim
that every original full text was accessible or that a complete historical
priority search was performed. The evidence level for each item is explicit.
Only full-text-supported claims are added to the manuscript. Unavailable
originals are not used to substantiate new equation claims. No citation
counts or journal metrics were used to choose sources.

## Constitutive and experimental references

| Key | Evidence inspected | Assessment and action |
| --- | --- | --- |
| `zha1996forsterite` | Author-hosted published PDF, `references/pdfs/zha1996.pdf`, abstract, experimental discussion, and Table 3 (printed p.17540). [Full text](https://duffy.princeton.edu/sites/g/files/toruqf616/files/zha_etal_jgr_1996.pdf). | Brillouin measurements establish pressure-dependent mineral elasticity. This supports caution about extrapolating constant logarithmic elastic coefficients, not identification of acoustic moduli at finite pressure with the present material Hessian. Add a qualitative limitation; do not import numerical moduli or claim a forsterite calibration. |
| `hashinshtrikman1963` | Source metadata and [Hashin's 1980 retrospective](https://garfield.library.upenn.edu/classics1980/A1980JC93400001.pdf). Original 1963 full text not obtained. | Relevant to microstructural bounds, but no original equation verified. Do not claim the series ordering is a Hashin–Shtrikman bound or sufficient for pore-geometry realizability. No new citation-backed bound is added. |
| `nurbyerlee1971` | [Original publisher abstract and metadata](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/JB076i026p06414); full-text endpoint returned 403. | Classical scalar effective-stress law under Hooke assumptions; potentially relevant historical context. Does not verify a finite anisotropic logarithmic series law. Preserve current verified classical comparison; no new detailed attribution to this inaccessible original. |
| `biot1973` | [Publisher abstract](https://doi.org/10.1029/JB078i023p04924); original full text unavailable after targeted retrieval. | Prior nonlinear/semilinear porous-solid theory, with grain compression and geometric effects. Confirms that broad finite-deformation or nonlinear coupling novelty would be inappropriate. No new equation comparison or priority claim is made without the full text. |
| `dehghanipentamerodio2019` | `references/pdfs/dehghani2019.pdf`, Glasgow author manuscript; printed pp.4–7, section 2, equations (3)–(10), and cell geometry in section 3. [Full text](https://eprints.gla.ac.uk/213049/13/213049.pdf). | Derives effective elasticity, Biot tensor, and storage from periodic cell problems with linear elastic matrix. Use to distinguish resolved microstructural localization from the present internal-strain assumption. Repository metadata gives online 2018; bibliography uses journal volume 6 (2019), article 035404. |
| `dehghanizilian2021` | `references/pdfs/dehghani-zilian-2021.pdf`, arXiv:2103.06569v1; introduction, sections 2.1–2.2 and conclusions pp.31–32. | Incremental homogenization/localization with ANN-assisted property updates explicitly models micro–macro dependence. Relevant comparison, not evidence for the present series localization. Add a short distinction from evolving microstructure. |
| `chenyangeinav2026` | [Publisher abstract/section preview](https://www.sciencedirect.com/science/article/abs/pii/S002250962500393X); publisher API metadata saved locally. Standard HTML/PDF endpoints returned 403; API supplied metadata only. | Directly relevant alternative energy-based treatment of stresses and pressures, including density dependence and saturation. Original full text remains an explicit access gap. No claim that the present stress distinction or thermodynamic framework is new, and no detailed comparison to its equations is asserted. This is not full-text verification despite the article's open-access metadata. |
| `hongetal2008` | `references/pdfs/hong2008.pdf`, published article; pp.1782–1783 equations (9)–(15), abstract, and molecular incompressibility assumptions. [Author copy](https://imechanica.org/sites/default/files/200%20a%20theory%20of%20coupled%20diffusion%20and%20large%20deformation%20in%20polymeric%20gels.pdf). | Finite deformation, energy derivatives, diffusion, and incompressible molecular constituents; not a compressible-mineral constitutive closure. Relevant gel comparison, but no need to expand the current paper into chemical swelling. |
| `macminnetal2016` | `references/pdfs/macminn-2016-large-deformations.pdf`, arXiv:1510.03455v3; pp.2–3 constituent assumptions and mass/porosity kinematics, p.6 Hencky elasticity. | Prior use of Hencky skeleton elasticity in finite poromechanics with incompressible grains. Add this explicit precedent: logarithmic skeleton elasticity alone is not new; the present construction adds compressible mineral response and a stated series assumption. |
| `bertrandetal2016` | `references/pdfs/bertrand2016.pdf`, published article; pp.064010-2–4, equations (1)–(9), swelling/drying model. [Author copy](https://jorgepeixinho.com/wp-content/uploads/2023/08/bertrandPeixinhoMukhopadyayMacMinn16.pdf). | Network stretching plus mixing energy and a pore-pressure/chemical-potential distinction. Provides dynamic gel context, not the present isolated-mineral law. Reviewed but not added solely to enlarge the bibliography. |
| `ingraham2017evolution` | Published PDF `references/pdfs/ingraham-2017-biot-coefficient-high-mean-stresses-sandstone-published.pdf`, pp.1–3; distinguish from duplicated proof versions in the source library. | Elastic effective-stress coefficient measured along evolving, compacted sandstone states. Supports the need to distinguish reversible elastic response from damage/plastic evolution. Current model does not reproduce that evolution, so do not use it as validation. |
| `makhnenkolabuz2015` | `references/pdfs/2015-makhnenko-labuz-dilatant-hardening.pdf`, abstract and introductory experimental scope. | Drained, undrained, unjacketed testing plus elastoplastic dilatant hardening. Useful broader experimental context but plastic hardening is excluded by the user. The existing Makhnenko–Labuz 2016 citation already supplies the needed elastic-test context. |
| `brantut2020` | `references/pdfs/2020-brantut-dilatancy-pressure-drop.pdf`, abstract and introduction. | Rupture/slip-driven dilatancy and fluid-pressure drops concern irreversible fracture and dynamic faulting. Outside elastic reconstruction; do not use as evidence for the present equilibrium pressure tangent. |
| `yamakawaetal2021` | [Publisher abstract and author contributions](https://onlinelibrary.wiley.com/doi/abs/10.1002/nag.3268). | Finite-strain Cam-Clay, rotational hardening, and plastic multiplicative factors. Exclude plastic constitutive developments from this paper. Full text was not required to support any added claim, since no claim from it is added. |
| `foster2026nonassociated` | `references/pdfs/foster-2026-apparent-non-associative-plasticity.pdf`, abstract and introduction. | Mechanism-resolved plasticity, distention closure, and distinct flow mechanisms. It reinforces the importance of explicitly stating a localization/closure assumption, but does not derive the present elastic tensor series. Do not introduce its plastic equations. |

## Computational and auxiliary references

| Key | Evidence inspected | Assessment and action |
| --- | --- | --- |
| `gastonetal2009moose` | Local `references/pdfs/gaston-2009-moose.pdf`, abstract/introduction; this is a conference version with matching framework subject, not certified as the journal version. | MOOSE/JFNK framework. This paper's independent constitutive scripts do not use MOOSE, so adding the citation would imply an unused dependency. Exclude. |
| `balayetal2026petsc` | [Official PETSc documentation and manual metadata](https://petsc.gitlab.io/petsc/release/), revision 3.25, DOI 10.2172/2998643. | Solver software used in the source implementation, not this constitutive derivation or its NumPy/SciPy checks. Exclude; no PETSc performance or API claim is made. |
| `usstandardatmosphere1976` | Bibliographic entry (NASA-TM-X-74335) and its atmospheric-data subject. | Auxiliary dimensional reference with no role in this synthetic elastic study. No atmospheric pressure/density value is imported. Title/scope screening only, not full-text verification. Exclude. |
| `lindsayetal2021ad` | `references/pdfs/lindsay-2021-automatic-differentiation.pdf`, abstract/introduction. | AD within MOOSE and nested nonlinear calculations. No MOOSE AD implementation is claimed here; finite-difference and direct derivative checks are documented on their own. Exclude. |
| `sunostien2013` | `references/pdfs/sun-ostien-salinger-2013-stabilized-finite-strain-poromechanics.pdf`, templated residual/AD discussion in numerical implementation. | Coupled finite-strain poromechanics and stabilization/AD. This paper does not implement the source's FE scheme. Do not cite it as verification of the new closed-form tensor. |
| `simotaylor1985` | `references/pdfs/simo-taylor-1985.pdf`, opening summary and introduction. | Consistent discrete plastic tangents and Newton convergence. No plastic update exists in this elastic study. Exclude. |
| `miehe1996` | `references/pdfs/miehe-1996-algorithmic-tangents.pdf`, abstract and pp.223–224. | Perturbation-based algorithmic stress derivatives; includes elasticity but primarily supplies a general implementation technique. The current finite-difference diagnostics need no claim that this source verifies them. Reviewed, not added. |
| `chengdetournay1988` | [Publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1002/nag.1610120508), full original unavailable. | Plane-strain BEM and Mandel/borehole validation. The present paper has a homogeneous confined-layer constitutive test, not the source's Mandel transient. Exclude rather than misattribute its test. |

## Consequences for the revision

- Add full-text-supported context for logarithmic skeleton elasticity,
  microstructural localization, and limits of constant mineral coefficients.
- Retain a self-contained proof of the tensor construction. Neither the
  series assumption nor its modulus ordering is attributed to an uninspected
  classical paper.
- Distinguish an effective internal mineral strain from actual phase-average
  Cauchy stress. No retrieved source closes that localization gap for this
  model; it remains an explicit constitutive scope condition.
- Detailed historical comparison with Chen–Yang–Einav, Biot 1973,
  Nur–Byerlee, and Hashin–Shtrikman remains limited by original full-text
  access. This audit reviews those entries at the available evidence level;
  it does not conceal the gap or certify priority.
