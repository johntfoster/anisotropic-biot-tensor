#!/usr/bin/env python3
"""Build a companion site from an explicit, checksummed publication manifest."""
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlparse
import zipfile

CATEGORIES = ("analytical", "implementation", "convergence", "finite_deformation", "physical_validation")
STATUSES = {"pending", "passed", "failed", "not_performed"}
KINDS = {"report", "source", "deck", "data", "figure", "paper", "provenance", "supplement"}
ROOTS = {"site", "validation", "examples", "figures", "build", "moose_app", "provenance", "sections"}
EXTENSIONS = {".json", ".csv", ".txt", ".md", ".pdf", ".pgf", ".png", ".jpg", ".jpeg", ".i", ".C", ".h", ".py", ".tex", ".bib", ".yml", ".yaml", ".toml", ".zip", ".sha256"}
SECRET_WORDS = {"credentials", "credential", "secrets", "secret", "token", "tokens", "passwd", "password", "id_rsa", "id_ed25519"}
esc = html.escape


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("Artifact paths must be nonempty POSIX relative paths")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in {".", ".."} for part in value.split("/")):
        raise ValueError("Absolute paths and path traversal are forbidden")
    if any(part.startswith(".") or part.lower() in SECRET_WORDS for part in p.parts):
        raise ValueError("Hidden and credential-related paths are not publication artifacts")
    if any(word in SECRET_WORDS for part in p.parts for word in re.split(r"[._-]", part.lower())):
        raise ValueError("Credential-related paths are not publication artifacts")
    return p


def check_zip(path):
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            relative_path(info.filename.rstrip("/"))
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Publication archives cannot contain symlinks")


def check_artifacts(root, manifest):
    artifacts = {}
    destinations = set()
    for item in manifest["artifacts"]:
        ident = item["id"]
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", ident) or ident in artifacts:
            raise ValueError("Artifact IDs must be unique lowercase identifiers")
        source = relative_path(item["path"])
        destination = relative_path(item["destination"])
        if source.parts[0] not in ROOTS and str(source) not in {"main.tex", "references.bib", "LICENSES.md"}:
            raise ValueError(f"Source outside publication roots: {source}")
        if source.suffix not in EXTENSIONS or destination.suffix != source.suffix:
            raise ValueError(f"Unsupported or renamed artifact type: {source}")
        if str(destination) in destinations:
            raise ValueError("Duplicate publication destination")
        destinations.add(str(destination))
        path = root / source
        if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f"Missing or escaping source: {source}")
        if any(part.is_symlink() for part in [path, *path.parents] if part != root.parent):
            raise ValueError(f"Publication source cannot be a symlink: {source}")
        if item["kind"] not in KINDS or not item.get("label"):
            raise ValueError("Artifact kind and label are required")
        if not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) or digest(path) != item["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {source}")
        if path.suffix == ".zip":
            check_zip(path)
        artifacts[ident] = item
    return artifacts


def check_manifest(root, manifest):
    if manifest.get("schema_version") != 1:
        raise ValueError("Expected evidence schema_version 1")
    for field in ("version", "title", "summary"):
        if not isinstance(manifest.get(field), str) or not manifest[field]:
            raise ValueError(f"Missing {field}")
    if set(manifest["categories"]) != set(CATEGORIES):
        raise ValueError("All five distinct verification categories are required")
    artifacts = check_artifacts(root, manifest)
    provenance = manifest["provenance"]
    if provenance["source_revision"] is not None and not re.fullmatch(r"[0-9a-f]{40}", provenance["source_revision"]):
        raise ValueError("source_revision must be a full commit hash or null")
    snapshot = provenance["scientific_snapshot"]
    if snapshot is not None:
        if snapshot not in artifacts or artifacts[snapshot]["kind"] != "provenance":
            raise ValueError("scientific_snapshot must reference an allowlisted provenance artifact")
        payload = json.loads((root / artifacts[snapshot]["path"]).read_text())
        if not isinstance(payload.get("files"), list) or not payload["files"]:
            raise ValueError("Scientific snapshot requires a nonempty files list")
        for entry in payload["files"]:
            source = root / relative_path(entry["path"])
            if not source.resolve().is_relative_to(root.resolve()) or not source.is_file() or digest(source) != entry["sha256"]:
                raise ValueError(f"Scientific snapshot mismatch: {entry['path']}")
    has_pass = False
    for name, item in manifest["categories"].items():
        if item["status"] not in STATUSES or not item.get("summary"):
            raise ValueError(f"Invalid status or missing summary: {name}")
        evidence = item.get("evidence", [])
        if any(ident not in artifacts for ident in evidence):
            raise ValueError(f"Unknown evidence artifact: {name}")
        if item["status"] == "passed":
            has_pass = True
            if not evidence or not any(artifacts[ident]["kind"] == "report" for ident in evidence):
                raise ValueError(f"Passed category requires a report artifact: {name}")
    if has_pass and (snapshot is None or provenance["source_revision"] is None):
        raise ValueError("Passed claims require the base commit AND a verified scientific source snapshot")
    for case in manifest.get("cases", []):
        if case["status"] not in STATUSES or not case.get("title") or not case.get("description"):
            raise ValueError("Cases require title, description, and explicit status")
        if any(ident not in artifacts for ident in case.get("artifacts", [])):
            raise ValueError("Unknown case artifact")
        if case["status"] == "passed" and not any(artifacts[ident]["kind"] == "report" for ident in case.get("artifacts", [])):
            raise ValueError("Passed case requires a report artifact")
        if case["status"] == "passed" and (snapshot is None or provenance["source_revision"] is None):
            raise ValueError("Passed cases require source provenance")
    for detail in manifest.get("verification_details", []):
        if not detail.get("title") or not detail.get("paragraphs"):
            raise ValueError("Verification details require a title and paragraphs")
        if any(key not in artifacts for key in detail.get("evidence", [])):
            raise ValueError("Unknown verification-detail evidence")
    for figure in manifest.get("figures", []):
        item = artifacts.get(figure["artifact"])
        if not item or item["kind"] != "figure" or not figure.get("caption") or not figure.get("alt"):
            raise ValueError("Figures require a figure artifact, caption, and alternative text")
    if not manifest.get("limitations"):
        raise ValueError("Scientific limitations must be stated")
    return artifacts


def artifact_link(item):
    return '<a href="artifacts/' + quote(item["destination"], safe="/") + '">' + esc(item["label"]) + "</a>"


def render(manifest, metadata, artifacts):
    repo = metadata["repository"]
    if urlparse(repo).scheme != "https":
        raise ValueError("Repository URL must use HTTPS")
    categories = []
    for name in CATEGORIES:
        item = manifest["categories"][name]
        evidence = ", ".join(artifact_link(artifacts[key]) for key in item.get("evidence", [])) or "No report published."
        categories.append(f'<article class="card category"><h3>{esc(name.replace("_", " ").capitalize())}</h3><p class="status {item["status"]}">{esc(item["status"].replace("_", " "))}</p><p>{esc(item["summary"])}</p><p>{evidence}</p></article>')
    details = "".join(
        "<article><h3>" + esc(item["title"]) + "</h3>"
        + "".join("<p>" + esc(paragraph) + "</p>" for paragraph in item["paragraphs"])
        + "<p>" + " · ".join(artifact_link(artifacts[key]) for key in item.get("evidence", []))
        + "</p></article>" for item in manifest.get("verification_details", [])
    )
    cases = []
    for item in manifest.get("cases", []):
        links = " · ".join(artifact_link(artifacts[key]) for key in item.get("artifacts", []))
        cases.append(f'<article class="card"><h3>{esc(item["title"])}</h3><p class="status {item["status"]}">{esc(item["status"].replace("_", " "))}</p><p>{esc(item["description"])}</p><p>{links}</p></article>')
    figures = []
    for item in manifest.get("figures", []):
        art = artifacts[item["artifact"]]
        visual = ""
        if Path(art["destination"]).suffix in {".png", ".jpg", ".jpeg"}:
            visual = f'<img loading="lazy" src="artifacts/{quote(art["destination"], safe="/")}" alt="{esc(item["alt"], quote=True)}">'
        figures.append(f'<figure>{visual}<figcaption>{esc(item["caption"])} {artifact_link(art)}</figcaption></figure>')
    downloads = "".join(f'<li>{artifact_link(item)} <span class="kind">{esc(item["kind"])}</span><br><code>SHA-256 {item["sha256"]}</code></li>' for item in artifacts.values()) or "<li>No scientific artifacts published in this pending version.</li>"
    reproduction = "".join(f'<h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p><pre><code>{esc(item["command"])}</code></pre>' for item in manifest.get("reproduction", [])) or "<p>Scientific reproduction commands will accompany the reviewed run reports.</p>"
    limits = "".join(f"<li>{esc(item)}</li>" for item in manifest["limitations"])
    snapshot_id = manifest["provenance"]["scientific_snapshot"]
    snapshot = artifact_link(artifacts[snapshot_id]) if snapshot_id else "Pending; no scientific snapshot published."
    commit = esc(manifest["provenance"]["source_revision"] or "Pending")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(manifest["title"])}</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="companion.css"></head>
<body><a class="skip" href="#main">Skip to scientific evidence</a>
<header class="site-header"><div class="container"><a class="brand" href="index.html">Anisotropic Biot tensor<span class="tag">Mineral stress · distention work</span></a>
<nav aria-label="Companion navigation"><a class="active" href="index.html">Home</a><a href="#verification">Verification</a><a href="#cases">Examples</a><a href="#reproduce">Reproduce</a><a href="#downloads">Downloads</a></nav></div></header>
<section class="hero"><div class="container"><h1>{esc(manifest["title"])}</h1><p>{esc(manifest["summary"])}</p><div class="cta"><a class="btn primary" href="#reproduce">Full reproduction commands</a><a class="btn ghost" href="#downloads">Manuscript and data</a><a class="btn ghost" href="{esc(repo, quote=True)}">Repository</a></div></div></section>
<main id="main"><div class="container"><section class="section" id="verification"><h2>What has been checked?</h2><p>These categories describe different kinds of evidence. A successful site build or hosted development environment does not establish scientific correctness.</p><div class="grid">{"".join(categories)}</div></section>
<section class="section" id="constitutive-checks"><h2>Independent constitutive verification</h2>{details}</section>
<section class="section" id="cases"><h2>Finite-element examples</h2>{"".join(cases) or "<p>Examples pending.</p>"}</section>
<section class="section" id="figures"><h2>Results and figures</h2>{"".join(figures) or "<p>No finite-element result figures have been published in this version.</p>"}</section>
<section class="section" id="reproduce"><h2>Reproduce the calculations</h2>{reproduction}<p>Commands are documentation, not browser-executed code. Follow the stated environment requirements before running them.</p></section>
<section class="section" id="limits"><h2>Scope and limitations</h2><ul>{limits}</ul></section>
<section class="section" id="downloads"><h2>Scientific artifacts</h2><ul class="file-list downloads">{downloads}</ul></section>
<section class="section" id="provenance"><h2>Provenance</h2><p>Base repository commit: <code>{commit}</code>. The base commit alone may not contain the scientific working files. Their exact content is identified by the separately hashed scientific snapshot.</p><p>{snapshot}</p><p>{esc(manifest["provenance"].get("note", ""))}</p><p><a href="evidence.json">Scientific evidence manifest</a> · <a href="checksums.json">Published file checksums</a> · <a href="build-provenance.json">Site build provenance</a></p></section>
</div></main><footer class="site-footer"><div class="container"><p>Code: Apache-2.0. Manuscript: CC BY 4.0. See <a href="{esc(repo, quote=True)}/blob/{esc(metadata["default_branch"], quote=True)}/LICENSES.md">license scope and third-party notices</a>.</p><p><a href="infrastructure/index.html">Infrastructure record</a> · <a href="https://johntfoster.github.io/finite-strain-biot-poromechanics/">Companion paper</a></p></div></footer></body></html>'''


def build(root, manifest_path, output):
    root = root.resolve()
    output = output.resolve()
    if not output.is_relative_to(root / ".agent-runtime") or output == root / ".agent-runtime":
        raise ValueError("Generated site must be a subdirectory of .agent-runtime")
    manifest = json.loads(manifest_path.read_text())
    artifacts = check_manifest(root, manifest)
    metadata = json.loads((root / "research-project.yml").read_text())
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".verification-site-", dir=output.parent))
    try:
        subprocess.run(["python3", str(root / ".agent/shared/tools/research_project.py"), "site", "--output", str(temporary / "infrastructure")], cwd=root, check=True, capture_output=True, text=True)
        for item in artifacts.values():
            destination = temporary / "artifacts" / item["destination"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / item["path"], destination)
            if digest(destination) != item["sha256"]:
                raise ValueError("Artifact changed during build")
        (temporary / "index.html").write_text(render(manifest, metadata, artifacts))
        for name in ("style.css", "companion.css"):
            shutil.copyfile(root / "site" / name, temporary / name)
        (temporary / "evidence.json").write_text(json.dumps(manifest, indent=2) + "\n")
        git_revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
        provenance = {"schema_version": 1, "built_at_utc": datetime.now(timezone.utc).isoformat(), "builder_sha256": digest(root / "tools/build_verification_site.py"), "evidence_sha256": digest(temporary / "evidence.json"), "site_build_commit": git_revision, "scientific_source_revision": manifest["provenance"]["source_revision"], "scientific_snapshot_artifact": manifest["provenance"]["scientific_snapshot"], "claim": "Build and artifact-integrity record only; no scientific checks are executed by this builder."}
        (temporary / "build-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        checksums = {str(path.relative_to(temporary)): digest(path) for path in sorted(temporary.rglob("*")) if path.is_file()}
        (temporary / "checksums.json").write_text(json.dumps({"algorithm": "sha256", "files": checksums, "excludes": ["checksums.json"]}, indent=2) + "\n")
        subprocess.run(["python3", str(root / ".agent/shared/tools/research_project.py"), "links", str(temporary)], cwd=root, check=True, capture_output=True, text=True)
        backup = None
        if output.exists():
            backup = output.with_name(output.name + ".previous-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
            output.rename(backup)
        temporary.rename(output)
        return {"output": str(output.relative_to(root)), "artifacts": len(artifacts), "previous_output": str(backup.relative_to(root)) if backup else None, "link_check": "passed", "scientific_checks_executed": False}
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("site/evidence.json"))
    parser.add_argument("--output", type=Path, default=Path(".agent-runtime/site"))
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = root / args.manifest
    try:
        if args.validate_only:
            artifacts = check_manifest(root, json.loads(manifest.read_text()))
            print(json.dumps({"manifest": "valid", "artifacts": len(artifacts), "scientific_checks_executed": False}))
        else:
            print(json.dumps(build(root, manifest, root / args.output), indent=2))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Site build failed: {exc}\n")


if __name__ == "__main__":
    main()
