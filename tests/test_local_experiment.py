from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from src.local_experiment import (
    ManifestError,
    ORDERING_RULE,
    generate,
    load_corpus,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def source_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class LocalExperimentTests(unittest.TestCase):
    def test_generation_is_deterministic_and_preserves_sources(self) -> None:
        before = source_hashes(FIXTURES)
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first"
            second = Path(temporary) / "second"
            generate(FIXTURES, first)
            generate(FIXTURES, second)
            self.assertEqual(tree_bytes(first), tree_bytes(second))
        self.assertEqual(before, source_hashes(FIXTURES))

    def test_json_exposes_same_relationships_and_lossless_markdown(self) -> None:
        artifacts = load_corpus(FIXTURES)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            index = generate(FIXTURES, output)
            disk_index = json.loads((output / "index.json").read_text())
        self.assertEqual(index, disk_index)
        by_id = {item["artifact_id"]: item for item in disk_index["artifacts"]}
        for artifact in artifacts:
            exported = by_id[artifact.artifact_id]
            self.assertEqual(exported["raw_markdown"], artifact.markdown)
            self.assertEqual(exported["supersedes"], artifact.manifest["supersedes"])
            self.assertEqual(
                {item["claim_id"] for item in exported["claims"]},
                {item["claim_id"] for item in artifact.manifest["claims"]},
            )
            self.assertEqual(
                {
                    (item["target_claim_id"], tuple(item["citation_ids"]))
                    for item in exported["disagreements"]
                },
                {
                    (item["target_claim_id"], tuple(item["citation_ids"]))
                    for item in artifact.manifest["disagreements"]
                },
            )

    def test_views_disclose_ordering_sources_and_missing_support(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            generate(FIXTURES, output)
            for html_path in output.rglob("*.html"):
                html = html_path.read_text()
                self.assertIn(ORDERING_RULE, html)
                self.assertIn("source: fixtures/", html)
                self.assertIn("not been verified", html)
            claims = (
                output / "synthetic-review-v1" / "claims.html"
            ).read_text()
            self.assertIn("Missing support:", claims)
            self.assertIn("disagreement-identity", claims)

    def test_fixture_discovery_needs_no_hand_maintained_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            shutil.copytree(FIXTURES, fixtures)
            added = fixtures / "synthetic-review-v3"
            shutil.copytree(fixtures / "synthetic-review-v2", added)
            manifest_path = added / "artifact.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["artifact_id"] = "synthetic-review-v3"
            manifest["version"] = "3"
            manifest["supersedes"] = "synthetic-review-v2"
            manifest_path.write_text(json.dumps(manifest))
            output = Path(temporary) / "output"
            index = generate(fixtures, output)
            self.assertEqual(
                [item["artifact_id"] for item in index["artifacts"]],
                [
                    "synthetic-review-v1",
                    "synthetic-review-v2",
                    "synthetic-review-v3",
                ],
            )

    def test_unknown_fields_and_unresolved_relationships_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            shutil.copytree(FIXTURES, fixtures)
            manifest_path = fixtures / "synthetic-review-v1" / "artifact.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["claims"][0]["citation_ids"] = ["missing-citation"]
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ManifestError, "unresolved citations"):
                generate(fixtures, Path(temporary) / "output")

    def test_manifest_and_markdown_html_are_escaped(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            shutil.copytree(FIXTURES, fixtures)
            fixture = fixtures / "synthetic-review-v1"
            manifest_path = fixture / "artifact.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["title"] = "<script>manifest()</script>"
            manifest_path.write_text(json.dumps(manifest))
            (fixture / "artifact.md").write_text("# <script>markdown()</script>\n")
            output = Path(temporary) / "output"
            generate(fixtures, output)
            html = (output / "synthetic-review-v1" / "artifact.html").read_text()
            self.assertNotIn("<script>manifest()</script>", html)
            self.assertNotIn("<script>markdown()</script>", html)
            self.assertIn("&lt;script&gt;manifest()&lt;/script&gt;", html)
            self.assertIn("&lt;script&gt;markdown()&lt;/script&gt;", html)


if __name__ == "__main__":
    unittest.main()
