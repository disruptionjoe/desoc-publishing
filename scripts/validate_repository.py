#!/usr/bin/env python3
"""Dependency-free founding and continuity checks."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "CONSTITUTION.md",
    "DECISIONS.md",
    "GOVERNANCE.md",
    "STATUS.md",
    "ROADMAP.md",
    "RESEARCH.md",
    "LANES.yaml",
    "LANE-STATE.yaml",
    "LICENSE",
]

errors: list[str] = []

for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        errors.append(f"missing required file: {relative}")

markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for target in markdown_link.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            errors.append(f"broken local link: {path.relative_to(ROOT)} -> {target}")

expected_fragments = {
    "CONSTITUTION.md": [
        "orthodox and heterodox ideas compete on evidence",
        "Joe alone may:",
        "user-interactive or editable launch",
    ],
    "STATUS.md": [
        "Phase 0 — product definition and local proving",
        "not yet implemented",
        "not authorized",
    ],
    "AGENTS.md": [
        "consider",
        "try",
        "do",
        "read-only idea sources",
    ],
    "LANE-STATE.yaml": [
        "owner_id: desoc-publishing",
        "lane_id: \"1\"",
        "lane_id: A",
    ],
}

for relative, fragments in expected_fragments.items():
    text = (ROOT / relative).read_text(encoding="utf-8")
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{relative} missing consistency marker: {fragment}")

public_text = "\n".join(
    path.read_text(encoding="utf-8", errors="replace")
    for path in ROOT.rglob("*")
    if path.is_file() and ".git" not in path.parts
)
prohibited_patterns = {
    "credential-shaped private key": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
    "GitHub token": r"\bgh[opsu]_[A-Za-z0-9]{20,}\b",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
}
for label, pattern in prohibited_patterns.items():
    if re.search(pattern, public_text):
        errors.append(f"prohibited-content marker found: {label}")

if errors:
    print("desoc-publishing validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"desoc-publishing founding package valid ({len(REQUIRED)} required files).")

