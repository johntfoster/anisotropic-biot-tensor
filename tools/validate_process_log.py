#!/usr/bin/env python3
"""Validate the six-section process log and AI provenance required in commit messages."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


SECTIONS = (
    "Summary",
    "What changed & why",
    "Alternatives considered",
    "Dead ends & backtracks",
    "Open questions",
    "Next steps",
)
HEADING = re.compile(r"^(?:##\s+)?(" + "|".join(re.escape(item) for item in SECTIONS) + r")\s*$")
AI_PROVENANCE_FIELDS = (
    "AI model(s)",
    "AI session(s)",
)
AI_PROVENANCE = {
    field: re.compile(r"^" + re.escape(field) + r"\s*:\s*(.+?)\s*$", re.IGNORECASE)
    for field in AI_PROVENANCE_FIELDS
}
UNACCEPTABLE_PROVENANCE = {"unknown", "unavailable", "not recorded", "n/a", "none", "todo", "tbd"}


def validate(message: str) -> list[str]:
    errors: list[str] = []
    lines = message.splitlines()
    if not lines or not lines[0].strip():
        return ["commit subject is empty"]

    found: list[tuple[str, int]] = []
    for index, line in enumerate(lines[1:], start=1):
        match = HEADING.match(line.strip())
        if match:
            found.append((match.group(1), index))

    names = [name for name, _ in found]
    for section in SECTIONS:
        count = names.count(section)
        if count == 0:
            errors.append(f"missing section: {section}")
        elif count > 1:
            errors.append(f"duplicate section: {section}")

    if names != list(SECTIONS):
        errors.append("sections must appear once and in the required order")
        return errors

    for position, (name, line_index) in enumerate(found):
        end = found[position + 1][1] if position + 1 < len(found) else len(lines)
        content = [line.strip() for line in lines[line_index + 1 : end] if line.strip()]
        if not content:
            errors.append(f"empty section: {name}")

        if name == "Summary":
            for field, pattern in AI_PROVENANCE.items():
                values = [match.group(1) for line in content if (match := pattern.match(line))]
                if not values:
                    errors.append(f"missing {field} in Summary")
                elif len(values) > 1:
                    errors.append(f"duplicate {field} in Summary")
                elif values[0].casefold() in UNACCEPTABLE_PROVENANCE:
                    errors.append(f"unrecorded {field} in Summary")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message_file", type=Path)
    args = parser.parse_args()
    try:
        message = args.message_file.read_text(encoding="utf-8")
    except OSError as error:
        print(f"process-log validation failed: {error}", file=sys.stderr)
        return 2

    errors = validate(message)
    if errors:
        print("process-log validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print("required body sections: " + " / ".join(SECTIONS), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
