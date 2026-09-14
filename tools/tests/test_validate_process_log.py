#!/usr/bin/env python3
"""Unit tests for the commit process-log validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "validate_process_log.py"
SPEC = importlib.util.spec_from_file_location("validate_process_log", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


VALID = """Subject

Summary
State transition.

AI model(s): GPT-5
AI session(s): codex-2026-09-14-example

What changed & why
Factual changes and rationale.

Alternatives considered
An alternative was rejected.

Dead ends & backtracks
No dead end was recorded.

Open questions
No unresolved question was recorded.

Next steps
Run the next verification.
"""


class ProcessLogValidationTest(unittest.TestCase):
    def test_accepts_complete_log(self) -> None:
        self.assertEqual(MODULE.validate(VALID), [])

    def test_rejects_subject_only(self) -> None:
        errors = MODULE.validate("Subject only\n")
        self.assertIn("missing section: Summary", errors)

    def test_rejects_empty_section(self) -> None:
        empty_summary = VALID.replace(
            "State transition.\n\nAI model(s): GPT-5\nAI session(s): codex-2026-09-14-example\n",
            "",
        )
        errors = MODULE.validate(empty_summary)
        self.assertIn("empty section: Summary", errors)

    def test_rejects_missing_ai_provenance(self) -> None:
        errors = MODULE.validate(VALID.replace("AI session(s): codex-2026-09-14-example\n", ""))
        self.assertIn("missing AI session(s) in Summary", errors)

    def test_rejects_unrecorded_ai_provenance(self) -> None:
        errors = MODULE.validate(VALID.replace("AI model(s): GPT-5", "AI model(s): unknown"))
        self.assertIn("unrecorded AI model(s) in Summary", errors)

    def test_rejects_reordered_sections(self) -> None:
        changed = VALID.replace("Summary\nState transition.", "TEMP").replace(
            "Next steps\nRun the next verification.", "Summary\nState transition."
        ).replace("TEMP", "Next steps\nRun the next verification.")
        self.assertIn("sections must appear once and in the required order", MODULE.validate(changed))


if __name__ == "__main__":
    unittest.main()
