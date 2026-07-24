#!/usr/bin/env python3
"""Build the dependency-free offline publishing experiment."""

from argparse import ArgumentParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.local_experiment import ManifestError, generate  # noqa: E402


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=ROOT / "fixtures")
    parser.add_argument("--output", type=Path, default=ROOT / "_local/experiment")
    args = parser.parse_args()
    try:
        index = generate(args.fixtures, args.output)
    except ManifestError as exc:
        parser.error(str(exc))
    print(f"generated {len(index['artifacts'])} artifacts at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
