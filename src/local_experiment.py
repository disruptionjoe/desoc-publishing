"""Dependency-free loader and renderer for the first local experiment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
import json
from pathlib import Path
import re
import shutil
from typing import Any


ORDERING_RULE = (
    "Ordering: artifacts use stable artifact ID; claims use stable claim ID. "
    "This deterministic order is not a quality ranking."
)
SYNTHETIC_NOTICE = (
    "Synthetic fixture: producer identity, authorship, and declared priority "
    "have not been verified."
)
MANIFEST_FIELDS = {
    "schema_version",
    "artifact_id",
    "title",
    "producer_display",
    "created_at",
    "version",
    "supersedes",
    "claims",
    "citations",
    "disagreements",
}
CLAIM_FIELDS = {"claim_id", "text", "citation_ids"}
CITATION_FIELDS = {"citation_id", "text", "locator"}
DISAGREEMENT_FIELDS = {
    "disagreement_id",
    "target_claim_id",
    "position",
    "rationale",
    "citation_ids",
}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ManifestError(ValueError):
    """Raised when a portable artifact does not satisfy the experiment contract."""


@dataclass(frozen=True)
class Artifact:
    root: Path
    manifest: dict[str, Any]
    markdown: str

    @property
    def artifact_id(self) -> str:
        return self.manifest["artifact_id"]


def _require_exact_fields(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        raise ManifestError(f"{label} fields mismatch; missing={missing}, unknown={unknown}")


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{label} must be a non-empty string")
    return value


def _require_id(value: Any, label: str) -> str:
    identifier = _require_string(value, label)
    if not ID_PATTERN.fullmatch(identifier):
        raise ManifestError(f"{label} must be a portable identifier")
    return identifier


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ManifestError(f"{label} must be a list")
    result = [_require_id(item, f"{label} item") for item in value]
    if len(result) != len(set(result)):
        raise ManifestError(f"{label} contains duplicates")
    return result


def _require_object_list(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ManifestError(f"{label} must be a list")
    if not all(isinstance(item, dict) for item in value):
        raise ManifestError(f"{label} items must be objects")
    return value


def load_artifact(directory: Path) -> Artifact:
    """Load and validate one portable artifact directory."""

    directory = directory.resolve()
    manifest_path = directory / "artifact.json"
    markdown_path = directory / "artifact.md"
    if directory.is_symlink() or manifest_path.is_symlink() or markdown_path.is_symlink():
        raise ManifestError(f"{directory.name}: symbolic links are not accepted")
    if not manifest_path.is_file() or not markdown_path.is_file():
        raise ManifestError(f"{directory.name}: artifact.json and artifact.md are required")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{directory.name}: invalid UTF-8 JSON manifest") from exc
    if not isinstance(manifest, dict):
        raise ManifestError(f"{directory.name}: manifest root must be an object")
    _require_exact_fields(manifest, MANIFEST_FIELDS, directory.name)

    if manifest["schema_version"] != "1.0":
        raise ManifestError(f"{directory.name}: unsupported schema_version")
    artifact_id = _require_id(manifest["artifact_id"], "artifact_id")
    if artifact_id != directory.name:
        raise ManifestError(f"{directory.name}: artifact_id must match directory name")
    for field in ("title", "producer_display", "version"):
        _require_string(manifest[field], field)
    created_at = _require_string(manifest["created_at"], "created_at")
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ManifestError(f"{directory.name}: created_at must be ISO 8601") from exc
    supersedes = manifest["supersedes"]
    if supersedes is not None:
        _require_id(supersedes, "supersedes")
        if supersedes == artifact_id:
            raise ManifestError(f"{directory.name}: artifact cannot supersede itself")

    claims = _require_object_list(manifest["claims"], "claims")
    citations = _require_object_list(manifest["citations"], "citations")
    disagreements = _require_object_list(manifest["disagreements"], "disagreements")
    if not claims:
        raise ManifestError(f"{directory.name}: at least one claim is required")

    claim_ids: set[str] = set()
    for claim in claims:
        _require_exact_fields(claim, CLAIM_FIELDS, "claim")
        claim_id = _require_id(claim["claim_id"], "claim_id")
        if claim_id in claim_ids:
            raise ManifestError(f"{directory.name}: duplicate claim_id {claim_id}")
        claim_ids.add(claim_id)
        _require_string(claim["text"], f"{claim_id}.text")
        _require_string_list(claim["citation_ids"], f"{claim_id}.citation_ids")

    citation_ids: set[str] = set()
    for citation in citations:
        _require_exact_fields(citation, CITATION_FIELDS, "citation")
        citation_id = _require_id(citation["citation_id"], "citation_id")
        if citation_id in citation_ids:
            raise ManifestError(f"{directory.name}: duplicate citation_id {citation_id}")
        citation_ids.add(citation_id)
        _require_string(citation["text"], f"{citation_id}.text")
        _require_string(citation["locator"], f"{citation_id}.locator")

    disagreement_ids: set[str] = set()
    for disagreement in disagreements:
        _require_exact_fields(disagreement, DISAGREEMENT_FIELDS, "disagreement")
        disagreement_id = _require_id(
            disagreement["disagreement_id"], "disagreement_id"
        )
        if disagreement_id in disagreement_ids:
            raise ManifestError(
                f"{directory.name}: duplicate disagreement_id {disagreement_id}"
            )
        disagreement_ids.add(disagreement_id)
        target = _require_id(disagreement["target_claim_id"], "target_claim_id")
        if target not in claim_ids:
            raise ManifestError(
                f"{directory.name}: disagreement target {target} is not a local claim"
            )
        _require_string(disagreement["position"], f"{disagreement_id}.position")
        _require_string(disagreement["rationale"], f"{disagreement_id}.rationale")
        _require_string_list(
            disagreement["citation_ids"], f"{disagreement_id}.citation_ids"
        )

    referenced_citations = {
        citation_id
        for item in [*claims, *disagreements]
        for citation_id in item["citation_ids"]
    }
    unresolved = sorted(referenced_citations - citation_ids)
    if unresolved:
        raise ManifestError(f"{directory.name}: unresolved citations {unresolved}")

    try:
        markdown = markdown_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ManifestError(f"{directory.name}: artifact.md must be UTF-8") from exc
    if not markdown.strip():
        raise ManifestError(f"{directory.name}: artifact.md must not be empty")
    return Artifact(root=directory, manifest=manifest, markdown=markdown)


def load_corpus(fixtures_root: Path) -> list[Artifact]:
    """Discover portable artifact directories without a hand-maintained index."""

    fixtures_root = fixtures_root.resolve()
    if not fixtures_root.is_dir():
        raise ManifestError(f"fixtures root does not exist: {fixtures_root}")
    artifacts = [
        load_artifact(path)
        for path in sorted(fixtures_root.iterdir(), key=lambda item: item.name)
        if path.is_dir() and not path.name.startswith(".")
    ]
    if not artifacts:
        raise ManifestError("fixtures root contains no artifacts")
    artifact_ids = {artifact.artifact_id for artifact in artifacts}
    for artifact in artifacts:
        supersedes = artifact.manifest["supersedes"]
        if supersedes is not None and supersedes not in artifact_ids:
            raise ManifestError(
                f"{artifact.artifact_id}: unresolved supersedes target {supersedes}"
            )
    return artifacts


def render_markdown(markdown: str) -> str:
    """Render a deliberately small, escaped Markdown subset."""

    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{escape(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{escape(item)}</li>" for item in list_items)
            blocks.append(f"<ul>{items}</ul>")
            list_items.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if not line:
            flush_paragraph()
            flush_list()
        elif line.startswith("# "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h2>{escape(line[2:].strip())}</h2>")
        elif line.startswith("## "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h3>{escape(line[3:].strip())}</h3>")
        elif line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
        else:
            flush_list()
            paragraph.append(line.strip())
    flush_paragraph()
    flush_list()
    return "\n".join(blocks)


def _page(title: str, content: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{escape(title)}</title>"
        "<style>"
        "body{font:16px/1.5 system-ui,sans-serif;max-width:68rem;margin:2rem auto;"
        "padding:0 1rem;color:#182026}nav a{margin-right:1rem}"
        ".notice{border-left:.3rem solid #b7791f;padding:.6rem 1rem;background:#fffaf0}"
        ".claim,.citation,.disagreement{border:1px solid #ccd6dd;padding:1rem;"
        "margin:1rem 0;border-radius:.3rem}code{overflow-wrap:anywhere}"
        "</style></head><body>"
        f"{content}</body></html>\n"
    )


def _navigation(artifact_id: str) -> str:
    return (
        "<nav>"
        '<a href="artifact.html">Artifact</a>'
        '<a href="claims.html">Claims and support</a>'
        '<a href="versions.html">Versions and disagreements</a>'
        "</nav>"
        f"<p><code>source: fixtures/{escape(artifact_id)}/artifact.json + "
        f"artifact.md</code></p>"
    )


def _citation_lookup(artifact: Artifact) -> dict[str, dict[str, Any]]:
    return {
        citation["citation_id"]: citation
        for citation in artifact.manifest["citations"]
    }


def render_artifact_view(artifact: Artifact) -> str:
    manifest = artifact.manifest
    citations = "".join(
        '<section class="citation">'
        f"<h3>{escape(item['citation_id'])}</h3>"
        f"<p>{escape(item['text'])}</p>"
        f"<p><code>{escape(item['locator'])}</code></p></section>"
        for item in sorted(manifest["citations"], key=lambda item: item["citation_id"])
    )
    lineage = manifest["supersedes"] or "none (first declared version)"
    content = (
        f"{_navigation(artifact.artifact_id)}"
        f"<h1>{escape(manifest['title'])}</h1>"
        f'<p class="notice">{escape(SYNTHETIC_NOTICE)}</p>'
        f"<dl><dt>Producer display</dt><dd>{escape(manifest['producer_display'])}</dd>"
        f"<dt>Declared time</dt><dd>{escape(manifest['created_at'])}</dd>"
        f"<dt>Version</dt><dd>{escape(manifest['version'])}</dd>"
        f"<dt>Supersedes</dt><dd>{escape(lineage)}</dd></dl>"
        f"<p>{escape(ORDERING_RULE)}</p>"
        f"<article>{render_markdown(artifact.markdown)}</article>"
        f"<h2>Citations</h2>{citations or '<p>No citations declared.</p>'}"
    )
    return _page(f"{manifest['title']} — artifact", content)


def render_claims_view(artifact: Artifact) -> str:
    manifest = artifact.manifest
    citations = _citation_lookup(artifact)
    disagreements_by_claim: dict[str, list[dict[str, Any]]] = {}
    for disagreement in manifest["disagreements"]:
        disagreements_by_claim.setdefault(
            disagreement["target_claim_id"], []
        ).append(disagreement)
    claim_sections: list[str] = []
    for claim in sorted(manifest["claims"], key=lambda item: item["claim_id"]):
        support = claim["citation_ids"]
        support_html = (
            "<ul>"
            + "".join(
                f"<li><strong>{escape(cid)}</strong>: "
                f"{escape(citations[cid]['text'])}</li>"
                for cid in support
            )
            + "</ul>"
            if support
            else '<p class="notice"><strong>Missing support:</strong> '
            "the producer declared no citation for this claim.</p>"
        )
        contests = disagreements_by_claim.get(claim["claim_id"], [])
        contest_html = (
            "".join(
                '<div class="disagreement">'
                f"<strong>{escape(item['disagreement_id'])} — "
                f"{escape(item['position'])}</strong>: "
                f"{escape(item['rationale'])}"
                f"<br>Citations: {escape(', '.join(item['citation_ids']) or 'none')}"
                "</div>"
                for item in sorted(
                    contests, key=lambda item: item["disagreement_id"]
                )
            )
            or "<p>No disagreement declared.</p>"
        )
        claim_sections.append(
            '<section class="claim">'
            f"<h2>{escape(claim['claim_id'])}</h2>"
            f"<p>{escape(claim['text'])}</p>"
            f"<h3>Declared support</h3>{support_html}"
            f"<h3>Contesting disagreements</h3>{contest_html}</section>"
        )
    content = (
        f"{_navigation(artifact.artifact_id)}"
        f"<h1>{escape(manifest['title'])}: claims and support</h1>"
        f'<p class="notice">{escape(SYNTHETIC_NOTICE)}</p>'
        f"<p>{escape(ORDERING_RULE)}</p>{''.join(claim_sections)}"
    )
    return _page(f"{manifest['title']} — claims", content)


def render_versions_view(artifact: Artifact) -> str:
    manifest = artifact.manifest
    grouped: dict[str, list[dict[str, Any]]] = {}
    for disagreement in manifest["disagreements"]:
        grouped.setdefault(disagreement["target_claim_id"], []).append(disagreement)
    sections = []
    for claim_id in sorted(grouped):
        items = "".join(
            '<div class="disagreement">'
            f"<h3>{escape(item['disagreement_id'])}: {escape(item['position'])}</h3>"
            f"<p>{escape(item['rationale'])}</p>"
            f"<p>Citations: {escape(', '.join(item['citation_ids']) or 'none')}</p>"
            "</div>"
            for item in sorted(grouped[claim_id], key=lambda item: item["disagreement_id"])
        )
        sections.append(f"<section><h2>Target claim {escape(claim_id)}</h2>{items}</section>")
    lineage = manifest["supersedes"] or "none (first declared version)"
    content = (
        f"{_navigation(artifact.artifact_id)}"
        f"<h1>{escape(manifest['title'])}: versions and disagreements</h1>"
        f'<p class="notice">{escape(SYNTHETIC_NOTICE)}</p>'
        f"<p>Version {escape(manifest['version'])}; supersedes: {escape(lineage)}.</p>"
        f"<p>{escape(ORDERING_RULE)}</p>"
        f"{''.join(sections) or '<p>No disagreements declared.</p>'}"
    )
    return _page(f"{manifest['title']} — versions", content)


def build_index(artifacts: list[Artifact]) -> dict[str, Any]:
    """Return the machine-readable form of every visible relationship."""

    return {
        "schema_version": "1.0",
        "notice": SYNTHETIC_NOTICE,
        "ordering_rule": ORDERING_RULE,
        "artifacts": [
            {
                **artifact.manifest,
                "claims": sorted(
                    artifact.manifest["claims"], key=lambda item: item["claim_id"]
                ),
                "citations": sorted(
                    artifact.manifest["citations"],
                    key=lambda item: item["citation_id"],
                ),
                "disagreements": sorted(
                    artifact.manifest["disagreements"],
                    key=lambda item: (
                        item["target_claim_id"],
                        item["disagreement_id"],
                    ),
                ),
                "source_files": {
                    "manifest": f"fixtures/{artifact.artifact_id}/artifact.json",
                    "markdown": f"fixtures/{artifact.artifact_id}/artifact.md",
                },
                "raw_markdown": artifact.markdown,
                "views": {
                    "artifact": f"{artifact.artifact_id}/artifact.html",
                    "claims": f"{artifact.artifact_id}/claims.html",
                    "versions": f"{artifact.artifact_id}/versions.html",
                },
            }
            for artifact in artifacts
        ],
    }


def generate(fixtures_root: Path, output_root: Path) -> dict[str, Any]:
    """Generate a complete deterministic output tree."""

    artifacts = load_corpus(fixtures_root)
    output_root = output_root.resolve()
    if output_root.exists():
        if output_root.is_symlink() or not output_root.is_dir():
            raise ManifestError("output must be a real directory")
        if not (output_root / ".desoc-experiment-output").is_file():
            raise ManifestError(
                "refusing to replace a directory not created by this experiment"
            )
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    (output_root / ".desoc-experiment-output").write_text(
        "generated; safe to replace\n", encoding="utf-8", newline="\n"
    )

    for artifact in artifacts:
        artifact_output = output_root / artifact.artifact_id
        artifact_output.mkdir()
        (artifact_output / "artifact.html").write_text(
            render_artifact_view(artifact), encoding="utf-8", newline="\n"
        )
        (artifact_output / "claims.html").write_text(
            render_claims_view(artifact), encoding="utf-8", newline="\n"
        )
        (artifact_output / "versions.html").write_text(
            render_versions_view(artifact), encoding="utf-8", newline="\n"
        )

    index = build_index(artifacts)
    (output_root / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return index
