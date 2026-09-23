"""Check publication boundaries and evidence requirements, without running MOOSE."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verification_site", ROOT / "tools/build_verification_site.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class PublicationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "validation").mkdir()
        self.manifest = json.loads((ROOT / "site/evidence.json").read_text())
        self.manifest["artifacts"] = []
        self.manifest["figures"] = []
        self.manifest["cases"] = []
        self.manifest["verification_details"] = []
        self.manifest["provenance"]["scientific_snapshot"] = None
        self.manifest["provenance"]["source_revision"] = None
        for item in self.manifest["categories"].values():
            item["status"] = "pending"
            item["evidence"] = []

    def artifact(self, name="result.json", content='{"status": "pending"}', kind="report"):
        path = self.root / "validation" / name
        path.write_text(content)
        item = {"id": "result", "path": "validation/" + name, "destination": name,
                "sha256": builder.digest(path), "kind": kind, "label": "Result"}
        self.manifest["artifacts"].append(item)
        return item

    def test_pending_has_no_scientific_pass(self):
        self.assertEqual(builder.check_manifest(self.root, self.manifest), {})

    def test_checksum_mismatch_rejected(self):
        self.artifact()["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            builder.check_manifest(self.root, self.manifest)

    def test_missing_artifact_rejected(self):
        self.artifact()
        (self.root / "validation/result.json").unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            builder.check_manifest(self.root, self.manifest)

    def test_traversal_and_hidden_paths_rejected(self):
        for value in ("../secret.json", "/tmp/a.json", "validation/../../a.json", ".agent-runtime/run.json", "validation/.env", "validation/api-token.json", "validation\\a.json"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                builder.relative_path(value)

    def test_symlink_rejected(self):
        self.artifact()
        path = self.root / "validation/result.json"
        actual = self.root / "validation/actual.json"
        path.rename(actual)
        path.symlink_to(actual)
        with self.assertRaisesRegex(ValueError, "symlink"):
            builder.check_manifest(self.root, self.manifest)

    def test_duplicate_destinations_rejected(self):
        item = self.artifact()
        duplicate = dict(item, id="another")
        self.manifest["artifacts"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            builder.check_manifest(self.root, self.manifest)

    def test_pass_requires_report(self):
        self.manifest["categories"]["implementation"]["status"] = "passed"
        with self.assertRaisesRegex(ValueError, "report"):
            builder.check_manifest(self.root, self.manifest)

    def test_pass_requires_scientific_snapshot(self):
        self.artifact()
        self.manifest["categories"]["implementation"].update(status="passed", evidence=["result"])
        with self.assertRaisesRegex(ValueError, "snapshot"):
            builder.check_manifest(self.root, self.manifest)

    def test_current_scientific_snapshot_required(self):
        self.artifact()
        source = self.root / "main.tex"
        source.write_text("Scientific source")
        snapshot = self.root / "validation/snapshot.json"
        snapshot.write_text(json.dumps({"files": [{"path": "main.tex", "sha256": builder.digest(source)}]}))
        self.manifest["artifacts"].append({"id": "snapshot", "path": "validation/snapshot.json", "destination": "snapshot.json", "kind": "provenance", "label": "Source hashes", "sha256": builder.digest(snapshot)})
        self.manifest["provenance"].update(source_revision="a" * 40, scientific_snapshot="snapshot")
        self.manifest["categories"]["implementation"].update(status="passed", evidence=["result"])
        self.assertEqual(len(builder.check_manifest(self.root, self.manifest)), 2)
        source.write_text("Different source")
        with self.assertRaisesRegex(ValueError, "snapshot mismatch"):
            builder.check_manifest(self.root, self.manifest)

    def test_zip_escape_rejected(self):
        archive = self.root / "validation/source.zip"
        with zipfile.ZipFile(archive, "w") as out:
            out.writestr("../outside.json", "{}")
        with self.assertRaises(ValueError):
            builder.check_zip(archive)

    def test_unknown_evidence_rejected(self):
        self.manifest["categories"]["analytical"]["evidence"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "Unknown"):
            builder.check_manifest(self.root, self.manifest)

    def test_html_text_is_escaped(self):
        self.manifest["title"] = "<script>alert(1)</script>"
        page = builder.render(self.manifest, {"repository": "https://example.org/paper", "default_branch": "main"}, {})
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("No finite-element result figures", page)


if __name__ == "__main__":
    unittest.main()
