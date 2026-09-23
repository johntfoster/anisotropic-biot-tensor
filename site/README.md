# Scientific verification companion

The companion publishes evidence for the MOOSE implementation and finite-element
examples. Scientific claims come from the versioned `site/evidence.json`, not
from the infrastructure status in `research-project.yml`. The existing shared
metadata site is rebuilt under `infrastructure/` and remains linked from the
scientific page.

`site/evidence.json` records the current status of each category exactly:
`passed` where the check is recorded and backed by the listed artifacts,
`pending` where a claim is not yet made, and `not_performed` where no work was
done. Publishing a site does not itself run or review a check.

## Build and inspect

From the repository root, using Python 3.10 or newer:

```sh
python3 -m pip install -r examples/requirements.txt
python3 tools/build_site_downloads.py
python3 tools/build_verification_site.py --manifest .agent-runtime/site-build-evidence.json --validate-only
python3 tools/build_verification_site.py --manifest .agent-runtime/site-build-evidence.json
python3 .agent/shared/tools/research_project.py links .agent-runtime/site
python3 -m unittest discover -s site -p 'test_*.py'
python3 -m http.server 8000 --directory .agent-runtime/site
```

Open `http://localhost:8000` for a local preview. This is not a deployment or an
embedded simulator. The site renderer uses only the Python standard library. The download builder
requires NumPy, SciPy, Matplotlib, latexmk, and a complete LuaLaTeX installation.
It regenerates constitutive calculations and figures from shipped source and
recorded finite-element histories, packages the numerical supplement, and builds
the manuscript PDF. It does not run MOOSE. Generated outputs remain ignored.

The Pages workflow runs both builders on a clean checkout, checks publication
boundaries and local links, and deploys only successful main-branch builds.
Pull requests build and validate the same site without deploying. The download
builder writes `.agent-runtime/site-build-evidence.json`, updating only the PDF
and ZIP hashes for that build; recorded evidence and scientific-source hashes
are still checked against the versioned manifest. PDF and archive bytes can
vary with the build environment, so the published checksums identify the actual
downloads. Site generation does not change the recorded scientific claims.

The default manifest is `site/evidence.json`; `--manifest` selects another
repository-relative JSON file. Generated output must be a subdirectory of
`.agent-runtime`; `--output` defaults to `.agent-runtime/site`. Each successful
rebuild preserves the previous output beside it as `site.previous-<UTC time>`.
Validation and link checks complete in a temporary directory before replacing
the previous site. The shared workflow uploads only `.agent-runtime/site`, not
its backups.

## Integrate the actual scientific results

1. Finish the runs, inspect their reports, and establish the scope of each
   scientific claim. Keep failed or missing checks visible.
2. Stage the selected, publishable files in `validation/publication/` or
   `site/publication/`, or reference explicit source files in the allowed roots
   below. Do not point the site at a runtime directory. Copying a report does
   not make it passing evidence.
3. Create a scientific source snapshot with an explicit `files` array of
   repository-relative `path` and `sha256` values. Include the manuscript,
   constitutive implementation, kernels, input decks, reference solution,
   postprocessing scripts, and any other sources needed to identify the
   reported calculation. A full Git commit hash records the base revision;
   the scientific snapshot records working-file bytes that may not yet be in
   that commit. Do not describe the base commit as the complete scientific
   source if there are additional working files.
4. Add every public source, deck, plot, CSV, run report, PDF, supplement, and
   provenance file to `artifacts` with its SHA-256 digest. These entries are
   the publication allowlist. They must be reviewed for public disclosure.
5. Reference the appropriate artifact IDs from categories, examples, and
   figure captions. Record environment requirements and exact reproduction
   commands under `reproduction`. State the measurement, units, comparison,
   mesh/time-step settings, and interpretation in each figure caption.
6. Run validation, build, and local link checks. Inspect the page and the
   downloadable files. Only then update the authorized deployment workflow.
   After deployment, fetch the live page and representative assets, compare
   their checksums, and record the deployed URL and workflow conclusion.

The site builder checks file identity and link integrity. It does not execute
the displayed commands, determine whether a numerical tolerance is justified,
or infer success from a report filename. The person preparing the evidence
manifest must verify that the report supports the claimed status. In
particular, a finite-load anisotropic example is not an analytical Mandel
verification, and neither is experimental validation.

## Evidence schema, version 1

`site/evidence.json` is the complete manifest. Required top-level fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1`. |
| `version` | Scientific artifact version, changed when evidence changes. |
| `title`, `summary` | Escaped reader-facing text. |
| `provenance.source_revision` | Full 40-character base commit hash of the recorded revision. |
| `provenance.scientific_snapshot` | Artifact ID of the source-hash snapshot the categories rest on. |
| `provenance.note` | Scope and provenance explanation. |
| `categories` | All five categories listed below. |
| `artifacts` | Explicit publication allowlist. |
| `limitations` | Nonempty list of scientific limitations. |

The required categories are `analytical`, `implementation`, `convergence`,
`finite_deformation`, and `physical_validation`. Each has `status`, `summary`,
and `evidence` (artifact IDs). Status is exactly `pending`, `passed`, `failed`,
or `not_performed`. A `passed` category requires at least one report artifact
and verified scientific provenance. Synthetic examples leave
`physical_validation` as `not_performed`.

An artifact entry has this form, with an actual digest replacing the placeholder:

```json
{
  "id": "mandel-report",
  "path": "validation/publication/mandel-report.json",
  "destination": "reports/mandel-report.json",
  "sha256": "<64 lowercase hexadecimal characters>",
  "kind": "report",
  "label": "Mandel comparison: tolerances and measured errors"
}
```

The destination is relative to the site's `artifacts/` directory. `kind` is
one of `report`, `source`, `deck`, `data`, `figure`, `paper`, `provenance`, or
`supplement`. Every ID and destination must be unique. Use
`sha256sum validation/publication/mandel-report.json` to inspect its digest.
Hashes must describe the final bytes; the builder rejects stale hashes.

The source snapshot is itself a checksummed artifact of kind `provenance`.
Its JSON content must include a nonempty array:

```json
{
  "schema_version": 1,
  "files": [
    {"path": "main.tex", "sha256": "<actual source digest>"},
    {"path": "moose_app/test/tests/mandel/mandel.i", "sha256": "<actual deck digest>"}
  ]
}
```

The paths above illustrate the shape, not a claim that this deck exists. The
builder checks all listed source hashes against the checkout. Do not include
the snapshot itself in its own `files` list. Archive the explicit scientific
sources as a `supplement` when a downloadable source package is desired; a
snapshot lists hashes but is not itself a source archive.

Optional `cases` entries contain `title`, `description`, `status`, and
`artifacts` (IDs). A passed case also requires a report and scientific
provenance. Optional `figures` entries contain `artifact`, `caption`, and
`alt`. PNG and JPEG figures display inline; PDF figures are download links.
Optional `reproduction` entries contain `title`, `description` (including
environment requirements), and `command` (a literal command block).

## Publication boundary

Only individual files explicitly named and hashed in `artifacts` are copied.
Allowed source roots are `site`, `validation`, `examples`, `figures`, `build`,
`moose_app`, `provenance`, and `sections`, plus root `main.tex`,
`references.bib`, and `LICENSES.md`. Supported extensions are enumerated in
the builder. Hidden paths, credential-related names, escaping paths,
symlinks, and recursive directory copies are rejected. ZIP contents are
checked for hidden/credential paths, traversal, and symlinks. The builder
never copies `.agent-runtime`, logs, caches, or Git metadata recursively.
These mechanical checks do not replace content review of explicit artifacts.

The output contains the scientific page, CSS, allowlisted artifacts,
`evidence.json`, `build-provenance.json`, `checksums.json`, and the separate
shared infrastructure page. `checksums.json` covers every generated file
except itself. Build provenance records the builder hash, manifest hash,
build commit, and scientific provenance references. It explicitly states
that the build does not run scientific checks.

## Companion design

`site/style.css` is copied without changes from `docs/assets/style.css` in
[the finite-strain companion](https://github.com/johntfoster/finite-strain-biot-poromechanics/blob/13fea4f7d3dc6ffb01d9a76e384750f0b7e78bb3/docs/assets/style.css).
The header, hero, containers, cards, file lists, and footer use its established
classes. `site/companion.css` adds evidence-status colors, keyboard focus, and
small-screen overflow handling. The independent checks formerly detailed in
manuscript section 8.5 live in `verification_details` in the evidence manifest.
