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

    def test_corpus_entry_and_derived_predecessor_comparison_are_navigable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            index = generate(FIXTURES, output)
            entrypoint = (output / "index.html").read_text()
            self.assertEqual("index.html", index["entrypoint"])
            self.assertIn('href="synthetic-review-v1/artifact.html"', entrypoint)
            self.assertIn('href="synthetic-review-v2/versions.html"', entrypoint)
            artifact = (output / "synthetic-review-v2" / "artifact.html").read_text()
            versions = (output / "synthetic-review-v2" / "versions.html").read_text()
            self.assertIn('../synthetic-review-v1/artifact.html', artifact)
            self.assertIn('../index.html', artifact)
            self.assertIn("Derived immediate-predecessor comparison", versions)
            self.assertIn("claim-trust", versions)
            self.assertIn("citation-identity", versions)
            self.assertIn("added disagreement-strength", versions)

    def test_independent_artifact_is_discoverable_without_false_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            index = generate(FIXTURES, output)
            self.assertEqual(
                [item["artifact_id"] for item in index["artifacts"]],
                [
                    "synthetic-independent-brief",
                    "synthetic-review-branch-a",
                    "synthetic-review-v1",
                    "synthetic-review-v2",
                ],
            )
            independent = next(
                item
                for item in index["artifacts"]
                if item["artifact_id"] == "synthetic-independent-brief"
            )
            self.assertIsNone(independent["supersedes"])
            entrypoint = (output / "index.html").read_text()
            artifact = (output / "synthetic-independent-brief" / "artifact.html").read_text()
            versions = (output / "synthetic-independent-brief" / "versions.html").read_text()
            self.assertIn('href="synthetic-independent-brief/artifact.html"', entrypoint)
            self.assertIn("not a quality ranking", entrypoint)
            self.assertIn("No predecessor is declared", artifact)
            self.assertIn("No predecessor is declared", versions)
            self.assertNotIn("synthetic-review-v1", artifact)
            self.assertNotIn("synthetic-review-v2", artifact)

    def test_declared_successors_are_navigable_without_canonicality(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            index = generate(FIXTURES, output)
            by_id = {item["artifact_id"]: item for item in index["artifacts"]}
            predecessor = by_id["synthetic-review-v1"]
            self.assertEqual(
                [item["artifact_id"] for item in predecessor["declared_successors"]],
                ["synthetic-review-branch-a", "synthetic-review-v2"],
            )
            artifact = (output / "synthetic-review-v1" / "artifact.html").read_text()
            versions = (output / "synthetic-review-v1" / "versions.html").read_text()
            self.assertIn('../synthetic-review-branch-a/artifact.html', artifact)
            self.assertIn('../synthetic-review-v2/artifact.html', artifact)
            self.assertLess(
                artifact.index("synthetic-review-branch-a"),
                artifact.index("synthetic-review-v2"),
            )
            self.assertIn("do not identify a canonical", artifact)
            self.assertIn("do not identify a canonical", versions)
            self.assertIn("No declared successors.", (output / "synthetic-review-v2" / "artifact.html").read_text())

    def test_successor_traversal_exposes_declared_siblings_without_ranking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            index = generate(FIXTURES, output)
            by_id = {item["artifact_id"]: item for item in index["artifacts"]}
            branch = by_id["synthetic-review-branch-a"]
            self.assertEqual(branch["declared_lineage_context"]["predecessor"], "synthetic-review-v1")
            self.assertEqual(branch["declared_lineage_context"]["sibling_continuations"], ["synthetic-review-v2"])
            self.assertIn("no continuation is compared, ranked, or selected", branch["declared_lineage_context"]["notice"])
            artifact = (output / "synthetic-review-branch-a" / "artifact.html").read_text()
            versions = (output / "synthetic-review-branch-a" / "versions.html").read_text()
            for view in (artifact, versions):
                self.assertIn("Declared lineage context", view)
                self.assertIn('../synthetic-review-v2/artifact.html', view)
                self.assertIn("does not compare, rank, or select", view)

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
                    "synthetic-independent-brief",
                    "synthetic-review-branch-a",
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
