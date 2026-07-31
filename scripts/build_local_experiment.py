#!/usr/bin/env python3
"""Build the dependency-free offline publishing experiment."""

from argparse import ArgumentParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.local_experiment import ManifestError, generate, preflight  # noqa: E402


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=ROOT / "fixtures")
    parser.add_argument("--output", type=Path, default=ROOT / "_local/experiment")
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="print a structural, non-admission report without writing output",
    )
    args = parser.parse_args()
    try:
        if args.preflight:
            report = preflight(args.fixtures)
            print(json.dumps(report, indent=2, ensure_ascii=True, sort_keys=True))
            return 0 if report["ready"] else 1
        index = generate(args.fixtures, args.output)
    except ManifestError as exc:
        parser.error(str(exc))
    print(f"generated {len(index['artifacts'])} artifacts at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
