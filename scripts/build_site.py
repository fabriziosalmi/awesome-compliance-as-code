#!/usr/bin/env python3
"""Deterministic static site, JSON API, and AI/SEO discovery generator for awesome-compliance-as-code.

Parses README.md (single source of truth) and examples/ to produce:
  - _site/index.html (SSR-prerendered monochrome technical index with airgapped SVG icons & JSON-LD)
  - _site/catalog.json (machine-readable JSON catalog and regulatory matrix)
  - _site/llms.txt (concise agent index following llmstxt.org specification)
  - _site/llms-full.txt (complete plain-text/Markdown catalog + reference implementations for LLM context)
  - _site/robots.txt (crawler directives + Sitemap & llms.txt discovery)
  - _site/sitemap.xml (XML sitemap validated as well-formed XML)
  - _site/assets/compliance-lifecycle.svg
  - _site/examples/... (executable OPA, Kyverno, Steampipe, and OSCAL artifacts)
  - _site/.nojekyll
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import pathlib
import shutil
import sys
import urllib.parse
from typing import Any

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_readme import (  # noqa: E402
    CATALOG_SECTION_PREFIXES,
    ENTRY_REGEX,
    EXAMPLES_DIR,
    README_PATH,
    TAG_EXTRACT_REGEX,
    github_slug,
    validate_markdown_text,
)

DEFAULT_OUTPUT_DIR = ROOT_DIR / "_site"
SITE_BASE_URL = "https://fabriziosalmi.github.io/awesome-compliance-as-code"
REPO_URL = "https://github.com/fabriziosalmi/awesome-compliance-as-code"

PERMISSIVE_LICENSES = frozenset(
    {"Apache-2.0", "MIT", "MIT-0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "UPL-1.0"}
)
WEAK_COPYLEFT_LICENSES = frozenset({"MPL-2.0", "EPL-2.0", "LGPL-2.1", "LGPL-3.0", "CPAL-1.0"})
STRONG_COPYLEFT_LICENSES = frozenset({"GPL-2.0", "GPL-3.0", "AGPL-3.0"})
OPEN_SPEC_LICENSES = frozenset(
    {"CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0", "Community-Spec-1.0", "Public-Domain"}
)


def classify_license_family(spdx_id: str) -> str:
    """Return high-level license category for filtering."""
    if spdx_id in PERMISSIVE_LICENSES:
        return "permissive"
    if spdx_id in WEAK_COPYLEFT_LICENSES:
        return "weak-copyleft"
    if spdx_id in STRONG_COPYLEFT_LICENSES:
        return "strong-copyleft"
    if spdx_id in OPEN_SPEC_LICENSES:
        return "open-spec"
    return "other"


def extract_repo_coord(url: str) -> str:
    """Extract concise 'owner/repo' or 'host/path' coordinate for visual provenance."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = parsed.path.strip("/")
    if host == "github.com":
        parts = path.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    return f"{host}/{path}" if path else host


def parse_catalog_data(readme_text: str, examples_dir: pathlib.Path = EXAMPLES_DIR) -> dict[str, Any]:
    """Parse validated README.md content into a structured dictionary."""
    lines = readme_text.splitlines()
    sections: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    matrix_rows: list[dict[str, str]] = []

    current_sec: dict[str, Any] | None = None
    current_sub: dict[str, Any] | None = None
    in_catalog = False
    in_matrix = False
    in_code_block = False

    tag_counts: dict[str, int] = {}
    license_counts: dict[str, int] = {}

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if line.startswith("## "):
            heading = line[3:].strip()
            in_catalog = any(line.startswith(prefix) for prefix in CATALOG_SECTION_PREFIXES)
            in_matrix = heading == "Regulatory-to-Code Mapping Matrix"
            current_sub = None
            if in_catalog:
                sec_slug = github_slug(heading)
                sec_num = heading.split(".", 1)[0].strip()
                current_sec = {
                    "id": sec_slug,
                    "number": int(sec_num),
                    "title": heading,
                    "description": "",
                    "subsections": [],
                    "count": 0,
                }
                sections.append(current_sec)
            else:
                current_sec = None
            continue

        if in_catalog and current_sec is not None:
            if line.startswith("### "):
                sub_title = line[4:].strip()
                sub_slug = github_slug(sub_title)
                current_sub = {
                    "id": sub_slug,
                    "title": sub_title,
                    "count": 0,
                }
                current_sec["subsections"].append(current_sub)
                continue

            if not line.startswith("- ") and current_sub is None and stripped and not current_sec["description"]:
                current_sec["description"] = stripped
                continue

            if line.startswith("- "):
                match = ENTRY_REGEX.match(line)
                if not match:
                    continue
                name = match.group("name").strip()
                url = match.group("url").strip()
                desc = match.group("desc").strip()
                raw_tags = TAG_EXTRACT_REGEX.findall(match.group("tags"))
                clean_tags = [t.strip("[]") for t in raw_tags]
                license_id = match.group("license").strip()
                license_family = classify_license_family(license_id)
                repo_coord = extract_repo_coord(url)

                for t in clean_tags:
                    tag_counts[t] = tag_counts.get(t, 0) + 1
                license_counts[license_id] = license_counts.get(license_id, 0) + 1

                current_sec["count"] += 1
                if current_sub is not None:
                    current_sub["count"] += 1

                entries.append(
                    {
                        "id": len(entries) + 1,
                        "name": name,
                        "url": url,
                        "repo": repo_coord,
                        "description": desc,
                        "section": current_sec["title"],
                        "section_id": current_sec["id"],
                        "section_num": current_sec["number"],
                        "subsection": current_sub["title"] if current_sub else "",
                        "subsection_id": current_sub["id"] if current_sub else "",
                        "tags": clean_tags,
                        "license": license_id,
                        "license_family": license_family,
                        "line": idx,
                    }
                )
            continue

        if in_matrix and stripped.startswith("|") and not stripped.startswith("| :---") and "Regulation / Standard" not in stripped:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) == 5:
                matrix_rows.append(
                    {
                        "regulation": cells[0].replace("**", ""),
                        "article": cells[1],
                        "requirement": cells[2],
                        "control": cells[3],
                        "tooling": cells[4],
                    }
                )

    reference_examples: list[dict[str, str]] = []
    example_specs = [
        (
            "OPA Rego v1: EU CRA & NIS2 Workload Hardening",
            "examples/opa/cra_workloads.rego",
            "rego",
            "Enforces non-root container execution (UID != 0) and requires a verified SBOM attestation annotation at Kubernetes admission.",
        ),
        (
            "Kyverno ClusterPolicy: DORA Art. 9 Keyless Signature & Privilege Gate",
            "examples/kyverno/dora_signed_images.yaml",
            "yaml",
            "Verifies keyless Sigstore Cosign OIDC image signatures against Rekor and blocks privileged containers.",
        ),
        (
            "Steampipe SQL: DORA Art. 10 & SOC 2 Encryption at Rest Audit",
            "examples/steampipe/dora_s3_encryption.sql",
            "sql",
            "Queries live AWS S3 buckets via PostgreSQL foreign tables to detect missing default server-side encryption.",
        ),
        (
            "NIST OSCAL 1.1.2 Component Definition",
            "examples/oscal/cra_component_definition.json",
            "json",
            "Maps NIST SP 800-53 Rev. 5 control AC-6 (Least Privilege) directly to automated OPA policy evaluation.",
        ),
    ]
    for title, rel_path, lang, summary in example_specs:
        full_path = examples_dir.parent / rel_path
        if full_path.exists():
            reference_examples.append(
                {
                    "title": title,
                    "path": rel_path,
                    "language": lang,
                    "summary": summary,
                    "code": full_path.read_text(encoding="utf-8").strip(),
                }
            )

    return {
        "schema_version": "1.1.0",
        "site_url": SITE_BASE_URL,
        "repository": REPO_URL,
        "license": "CC0-1.0",
        "total_entries": len(entries),
        "total_sections": len(sections),
        "total_subsections": sum(len(s["subsections"]) for s in sections),
        "regulatory_tags": dict(sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))),
        "licenses": dict(sorted(license_counts.items(), key=lambda x: (-x[1], x[0]))),
        "sections": sections,
        "matrix": matrix_rows,
        "examples": reference_examples,
        "entries": entries,
    }


def render_llms_txt(catalog: dict[str, Any]) -> str:
    """Render concise llmstxt.org discovery file for AI agents."""
    total = catalog["total_entries"]
    lines = [
        "# Awesome Compliance-as-Code",
        "",
        f"> Curated, deterministically validated catalog of {total} open-source Compliance-as-Code (CaC) specifications, policy engines, SBOM/VEX verifiers, runtime auditors, and regulatory-to-code mappings for CI/CD pipelines and production infrastructure.",
        "",
        "All entries in this catalog satisfy three automated verification gates:",
        "1. Executable tool, formal machine-readable schema, or policy ruleset (no slide-ware or commercial SaaS).",
        "2. Distributed under an approved OSI open-source or open-specification license.",
        "3. Unarchived repository with active commit history within the last 540 days.",
        "",
        "## Machine-Readable Endpoints",
        "",
        f"- [Complete Catalog JSON API]({SITE_BASE_URL}/catalog.json): Full structured dataset ({total} entries, regulatory tags, SPDX licenses, and mapping matrix).",
        f"- [Full Plain-Text Catalog for LLMs]({SITE_BASE_URL}/llms-full.txt): Single-file plain-text export of all {total} entries, the regulatory matrix, and reference policies.",
        f"- [Interactive Technical Index]({SITE_BASE_URL}/): Monochrome web interface supporting URL query-string filtering (`?tags=DORA,NIS2&mode=all&license=Apache-2.0`).",
        f"- [Source Repository]({REPO_URL}): Canonical GitHub repository, validation scripts, and CI workflows.",
        "",
        "## Executable Reference Policies",
        "",
    ]
    for ex in catalog["examples"]:
        lines.append(f"- [{ex['title']}]({SITE_BASE_URL}/{ex['path']}): {ex['summary']}")

    lines.extend(["", "## Engineering Domains & Subsections", ""])
    for sec in catalog["sections"]:
        sub_names = ", ".join(f"{sub['title']} ({sub['count']})" for sub in sec["subsections"])
        lines.append(
            f"- [{sec['title']}]({SITE_BASE_URL}/?section={sec['id']}) ({sec['count']} entries): {sec['description']} Subsections: {sub_names}."
        )

    lines.extend(["", "## Regulatory Tag Distribution", ""])
    for tag, count in catalog["regulatory_tags"].items():
        lines.append(f"- `[{tag}]`: {count} entries ({SITE_BASE_URL}/?tags={tag})")

    lines.extend(["", "## SPDX License Distribution", ""])
    for lic, count in catalog["licenses"].items():
        lines.append(f"- `{lic}`: {count} entries ({SITE_BASE_URL}/?license={lic})")

    return "\n".join(lines) + "\n"


def render_llms_full_txt(readme_text: str) -> str:
    """Render complete plain-text/Markdown catalog for deep LLM ingestion."""
    header = (
        "# Awesome Compliance-as-Code - Full Agent Context (llms-full.txt)\n"
        f"# Canonical URL: {SITE_BASE_URL}/llms-full.txt\n"
        f"# JSON API: {SITE_BASE_URL}/catalog.json\n"
        f"# Repository: {REPO_URL}\n"
        "# License: CC0-1.0\n\n"
    )
    return header + readme_text.strip() + "\n"


def render_robots_txt() -> str:
    """Render robots.txt with Sitemap and LLM discovery pointers."""
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {SITE_BASE_URL}/sitemap.xml\n"
        f"# AI / LLM Discovery:\n"
        f"# llms.txt: {SITE_BASE_URL}/llms.txt\n"
        f"# llms-full.txt: {SITE_BASE_URL}/llms-full.txt\n"
        f"# JSON API: {SITE_BASE_URL}/catalog.json\n"
    )


def render_sitemap_xml(catalog: dict[str, Any]) -> str:
    """Render valid XML sitemap for search engines."""
    today = datetime.date.today().isoformat()
    urls = [
        f"{SITE_BASE_URL}/",
        f"{SITE_BASE_URL}/catalog.json",
        f"{SITE_BASE_URL}/llms.txt",
        f"{SITE_BASE_URL}/llms-full.txt",
    ]
    for ex in catalog["examples"]:
        urls.append(f"{SITE_BASE_URL}/{ex['path']}")

    url_entries = "\n".join(
        f"  <url>\n    <loc>{html.escape(u)}</loc>\n    <lastmod>{today}</lastmod>\n  </url>"
        for u in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{url_entries}\n"
        "</urlset>\n"
    )


def _prerender_catalog_html(catalog: dict[str, Any]) -> str:
    """Pre-render all sections and entries as static 4-column Swiss-grid HTML so crawlers and curl see the full catalog."""
    by_sec: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for entry in catalog["entries"]:
        by_sec.setdefault(entry["section_id"], {}).setdefault(entry["subsection_id"], []).append(entry)

    blocks: list[str] = []
    for sec in catalog["sections"]:
        sub_map = by_sec.get(sec["id"], {})
        if not sub_map:
            continue
        sub_pills_html = "".join(
            f'<button class="sub-jump-btn" type="button" data-sub-jump="{html.escape(sub["id"])}">'
            f'{html.escape(sub["title"])} <span class="cnt">{sub["count"]}</span></button>'
            for sub in sec["subsections"]
        )
        sec_parts = [
            '<div class="sec-block">',
            '  <div class="sec-head">',
            '    <div class="sec-head-left">',
            f'      <svg class="ic"><use href="#sec-{sec["number"]}"/></svg>',
            f'      <span>{html.escape(sec["title"])}</span>',
            "    </div>",
            f'    <span class="sec-count">{sec["count"]} entries</span>',
            "  </div>",
            f'  <p class="sec-desc">{html.escape(sec["description"])}</p>',
            f'  <div class="sub-jump-strip">{sub_pills_html}</div>',
        ]
        for sub in sec["subsections"]:
            items = sub_map.get(sub["id"], [])
            if not items:
                continue
            sec_parts.append('  <div class="sub-block">')
            sec_parts.append(
                f'    <div class="sub-head"><span>{html.escape(sub["title"])}</span><span class="sub-head-cnt">{len(items)}</span></div>'
            )
            sec_parts.append(
                '    <div class="col-head">'
                "<span>Artifact / Repository</span>"
                "<span>Technical Specification</span>"
                "<span>Frameworks</span>"
                '<span class="col-right">License</span>'
                "</div>"
            )
            sec_parts.append('    <div class="entry-table">')
            for item in items:
                tags_html = "".join(
                    f'<span class="chip-tag" data-click-tag="{html.escape(t)}" title="Filter by [{html.escape(t)}]">[{html.escape(t)}]</span>'
                    for t in item["tags"]
                )
                sec_parts.append(
                    '      <div class="entry-row">'
                    '<div class="entry-name-cell">'
                    f'<a class="entry-link" href="{html.escape(item["url"])}" target="_blank" rel="noopener">'
                    f'{html.escape(item["name"])}<svg class="ic ic-ext"><use href="#i-ext"/></svg>'
                    "</a>"
                    f'<span class="entry-slug">{html.escape(item["repo"])}</span>'
                    "</div>"
                    f'<div class="entry-desc-cell">{html.escape(item["description"])}</div>'
                    f'<div class="entry-tags-cell">{tags_html}</div>'
                    '<div class="entry-lic-cell">'
                    f'<span class="chip-lic" data-click-lic="{html.escape(item["license"])}" title="Filter by license {html.escape(item["license"])}">{html.escape(item["license"])}</span>'
                    "</div></div>"
                )
            sec_parts.append("    </div>")
            sec_parts.append("  </div>")
        sec_parts.append("</div>")
        blocks.append("\n".join(sec_parts))
    return "\n".join(blocks)


def _prerender_matrix_html(catalog: dict[str, Any]) -> str:
    """Pre-render Regulatory-to-Code Mapping Matrix rows as static HTML."""
    reg_to_tag = {
        "EU Cyber Resilience Act (CRA)": "EU-CRA",
        "EU NIS2 Directive": "NIS2",
        "EU DORA": "DORA",
        "EU AI Act": "EU-AI-Act",
        "GDPR": "GDPR",
        "PCI-DSS v4.0": "PCI-DSS",
        "NIST SP 800-53 Rev. 5": "NIST-800-53",
        "ISO/IEC 42001": "ISO-42001",
    }
    rows: list[str] = []
    for row in catalog["matrix"]:
        tag = reg_to_tag.get(row["regulation"], "")
        tag_btn = (
            f'<div style="margin-top:6px"><button class="btn matrix-filter-btn" type="button" data-matrix-tag="{html.escape(tag)}">'
            f'Filter [{html.escape(tag)}] ({catalog["regulatory_tags"].get(tag, 0)}) &rarr;</button></div>'
            if tag
            else ""
        )
        rows.append(
            "<tr>"
            f"<td><strong>{html.escape(row['regulation'])}</strong>{tag_btn}</td>"
            f"<td><code>{html.escape(row['article'])}</code></td>"
            f"<td>{html.escape(row['requirement'])}</td>"
            f"<td>{html.escape(row['control'])}</td>"
            f"<td>{html.escape(row['tooling'])}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _prerender_examples_html(catalog: dict[str, Any]) -> str:
    """Pre-render Reference Code blocks as static HTML."""
    cards: list[str] = []
    for idx, ex in enumerate(catalog["examples"]):
        cards.append(
            '<div class="code-card">'
            '<div class="code-card-head">'
            f'<span><strong>{html.escape(ex["title"])}</strong> &middot; <a href="{html.escape(ex["path"])}">{html.escape(ex["path"])}</a></span>'
            f'<button class="btn copy-btn" data-ex-idx="{idx}" type="button"><svg class="ic ic-sm"><use href="#i-copy"/></svg><span>Copy</span></button>'
            "</div>"
            f'<div class="code-card-desc">{html.escape(ex["summary"])}</div>'
            f'<pre><code>{html.escape(ex["code"])}</code></pre>'
            "</div>"
        )
    return "\n".join(cards)


def _build_json_ld(catalog: dict[str, Any]) -> str:
    """Construct Schema.org Dataset and ItemList JSON-LD for search and agent indexing."""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Dataset",
                "@id": f"{SITE_BASE_URL}/#dataset",
                "name": "Awesome Compliance-as-Code",
                "description": (
                    f"Curated catalog of {catalog['total_entries']} open-source Compliance-as-Code specifications, "
                    "policy engines, SBOM/VEX verifiers, runtime auditors, and regulatory-to-code mappings."
                ),
                "url": f"{SITE_BASE_URL}/",
                "sameAs": REPO_URL,
                "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                "isAccessibleForFree": True,
                "version": catalog["schema_version"],
                "keywords": list(catalog["regulatory_tags"].keys()) + ["Compliance-as-Code", "Policy-as-Code", "SBOM", "OSCAL", "VEX"],
                "creator": {
                    "@type": "Person",
                    "name": "Fabrizio Salmi",
                    "url": "https://github.com/fabriziosalmi",
                },
                "distribution": [
                    {
                        "@type": "DataDownload",
                        "encodingFormat": "application/json",
                        "contentUrl": f"{SITE_BASE_URL}/catalog.json",
                    },
                    {
                        "@type": "DataDownload",
                        "encodingFormat": "text/plain",
                        "contentUrl": f"{SITE_BASE_URL}/llms-full.txt",
                    },
                ],
            },
            {
                "@type": "ItemList",
                "@id": f"{SITE_BASE_URL}/#domains",
                "name": "Compliance-as-Code Engineering Domains",
                "numberOfItems": catalog["total_sections"],
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": sec["number"],
                        "name": sec["title"],
                        "description": sec["description"],
                        "url": f"{SITE_BASE_URL}/?section={sec['id']}",
                    }
                    for sec in catalog["sections"]
                ],
            },
        ],
    }
    return json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_html(catalog: dict[str, Any]) -> str:
    """Render monochrome, airgapped-SVG, SSR-prerendered technical index in index.html."""
    embedded_json = json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    json_ld = _build_json_ld(catalog)
    prerendered_catalog = _prerender_catalog_html(catalog)
    prerendered_matrix = _prerender_matrix_html(catalog)
    prerendered_examples = _prerender_examples_html(catalog)

    total_entries = catalog["total_entries"]
    total_sections = catalog["total_sections"]
    total_subsections = catalog["total_subsections"]
    total_tags = len(catalog["regulatory_tags"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Awesome Compliance-as-Code ({total_entries} Verified Open-Source Entries)</title>
  <meta name="description" content="Curated technical index of {total_entries} open-source Compliance-as-Code specifications, policy engines, SBOM/VEX verifiers, runtime auditors, and regulatory mappings for EU CRA, NIS2, DORA, EU AI Act, GDPR, PCI-DSS, and NIST 800-53.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_BASE_URL}/">
  <link rel="alternate" type="application/json" title="Compliance-as-Code JSON API" href="catalog.json">
  <link rel="alternate" type="text/plain" title="LLMs.txt Agent Index" href="llms.txt">
  <link rel="alternate" type="text/plain" title="LLMs-Full.txt Complete Catalog" href="llms-full.txt">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Awesome Compliance-as-Code ({total_entries} Verified Entries)">
  <meta property="og:description" content="Machine-readable specifications, policy engines, supply-chain verifiers, runtime auditors, and regulatory-to-code mappings for CI/CD and production infrastructure.">
  <meta property="og:url" content="{SITE_BASE_URL}/">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Awesome Compliance-as-Code ({total_entries} Verified Entries)">
  <meta name="twitter:description" content="Filterable index and JSON API of {total_entries} open-source Compliance-as-Code tools, schemas, and policy packs.">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23111' stroke-width='2'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3Cpath d='m9 12 2 2 4-4'/%3E%3C/svg%3E">
  <script type="application/ld+json">{json_ld}</script>
  <style>
    :root {{
      --bg: #ffffff;
      --bg-subtle: #f6f6f6;
      --bg-muted: #ededed;
      --bg-invert: #111111;
      --fg: #111111;
      --fg-secondary: #383838;
      --fg-muted: #6e6e6e;
      --fg-dim: #9a9a9a;
      --fg-invert: #ffffff;
      --border: #dfdfdf;
      --border-mid: #b0b0b0;
      --border-strong: #111111;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, "Helvetica Neue", Arial, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: auto; }}
    body {{
      background: var(--bg);
      color: var(--fg);
      font-family: var(--font-sans);
      font-size: 13.5px;
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
      font-variant-numeric: tabular-nums;
    }}
    a {{ color: var(--fg); text-decoration: none; }}
    button, input, select {{ font: inherit; color: inherit; }}
    mark {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      padding: 0 2px;
      font-weight: 600;
    }}
    .ic {{
      width: 14px;
      height: 14px;
      stroke: currentColor;
      stroke-width: 1.9;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
      flex-shrink: 0;
      vertical-align: -2px;
    }}
    .ic-sm {{ width: 11.5px; height: 11.5px; stroke-width: 2; }}
    .wrap {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Compact Technical Masthead */
    header {{
      border-bottom: 1px solid var(--border);
      padding: 14px 0 12px;
      background: var(--bg);
    }}
    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand-group {{
      display: flex;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .brand {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .brand-mark {{
      width: 19px;
      height: 19px;
      stroke: var(--fg);
      stroke-width: 2.1;
      fill: none;
      position: relative;
      top: 2px;
    }}
    h1 {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.025em;
    }}
    .ver-pill {{
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 600;
      padding: 1px 5px;
      border: 1px solid var(--border-mid);
      background: var(--bg-subtle);
      color: var(--fg-secondary);
    }}
    .subtitle {{
      color: var(--fg-secondary);
      font-size: 12.5px;
      margin-top: 4px;
    }}
    .header-links {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: var(--bg);
      color: var(--fg);
      border: 1px solid var(--border-mid);
      padding: 4px 9px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 500;
      cursor: pointer;
      white-space: nowrap;
      user-select: none;
    }}
    .btn:hover {{
      border-color: var(--border-strong);
      background: var(--bg-subtle);
    }}
    .btn:active, .btn.active, .btn-invert {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      border-color: var(--border-strong);
    }}

    /* Sticky View & Telemetry Bar */
    .nav-strip {{
      border-bottom: 2px solid var(--border-strong);
      background: var(--bg);
      position: sticky;
      top: 0;
      z-index: 30;
    }}
    .nav-strip-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      height: 38px;
    }}
    .tabs {{
      display: flex;
      height: 100%;
    }}
    .tab-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: transparent;
      color: var(--fg-secondary);
      border: none;
      border-right: 1px solid var(--border);
      padding: 0 14px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      cursor: pointer;
      white-space: nowrap;
      height: 100%;
    }}
    .tab-btn:first-child {{ border-left: 1px solid var(--border); }}
    .tab-btn:hover {{
      color: var(--fg);
      background: var(--bg-subtle);
    }}
    .tab-btn.active {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      font-weight: 600;
    }}
    .telemetry-bar {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--fg-muted);
      display: flex;
      align-items: center;
      gap: 14px;
      white-space: nowrap;
    }}
    .kbd-legend {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .kbd {{
      display: inline-block;
      border: 1px solid var(--border-mid);
      background: var(--bg-subtle);
      color: var(--fg);
      padding: 0 4px;
      font-family: var(--font-mono);
      font-size: 10px;
      line-height: 1.4;
    }}
    @media (max-width: 1040px) {{
      .telemetry-bar {{ display: none; }}
    }}

    main {{ padding: 16px 0 56px; }}
    .pane {{ display: none; }}
    .pane.active {{ display: block; }}

    /* Two-column Swiss grid workspace */
    .workspace {{
      display: grid;
      grid-template-columns: 236px minmax(0, 1fr);
      gap: 20px;
      align-items: start;
    }}
    @media (max-width: 980px) {{
      .workspace {{ grid-template-columns: 1fr; }}
      .domain-rail {{ display: none; }}
    }}

    /* Left Sticky Domain Rail */
    .domain-rail {{
      position: sticky;
      top: 52px;
      border: 1px solid var(--border-strong);
      background: var(--bg);
    }}
    .rail-title {{
      padding: 7px 10px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: var(--bg-subtle);
      border-bottom: 1px solid var(--border-strong);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .rail-list {{ list-style: none; }}
    .rail-item {{
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      padding: 6.5px 10px;
      border: none;
      border-bottom: 1px solid var(--border);
      background: var(--bg);
      color: var(--fg-secondary);
      font-size: 12.5px;
      text-align: left;
      cursor: pointer;
    }}
    .rail-item:last-child {{ border-bottom: none; }}
    .rail-item:hover {{
      background: var(--bg-subtle);
      color: var(--fg);
    }}
    .rail-item.active {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      font-weight: 600;
    }}
    .rail-item.dim {{
      opacity: 0.38;
    }}
    .rail-item-left {{
      display: flex;
      align-items: center;
      gap: 7px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .rail-cnt {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--fg-muted);
      flex-shrink: 0;
    }}
    .rail-item.active .rail-cnt {{ color: #d0d0d0; }}

    /* Command & Filter Console */
    .filter-box {{
      border: 1px solid var(--border-strong);
      background: var(--bg);
      margin-bottom: 12px;
    }}
    .filter-top {{
      display: grid;
      grid-template-columns: 2.2fr 1.1fr 1.1fr;
      border-bottom: 1px solid var(--border);
    }}
    @media (max-width: 780px) {{
      .filter-top {{ grid-template-columns: 1fr; }}
    }}
    .search-wrap {{
      position: relative;
      display: flex;
      align-items: center;
      border-right: 1px solid var(--border);
    }}
    .search-wrap .ic-search {{
      position: absolute;
      left: 10px;
      color: var(--fg-muted);
      pointer-events: none;
    }}
    .search-clear {{
      position: absolute;
      right: 8px;
      background: var(--bg-invert);
      color: var(--fg-invert);
      border: none;
      font-family: var(--font-mono);
      font-size: 10.5px;
      padding: 1px 5px;
      cursor: pointer;
      display: none;
    }}
    .search-wrap .kbd-hint {{
      position: absolute;
      right: 9px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: var(--fg-muted);
      border: 1px solid var(--border);
      background: var(--bg-subtle);
      padding: 0 5px;
      pointer-events: none;
    }}
    .select-wrap {{
      position: relative;
      display: flex;
      align-items: center;
      border-right: 1px solid var(--border);
    }}
    .select-wrap:last-child {{ border-right: none; }}
    .select-wrap .ic-chev {{
      position: absolute;
      right: 9px;
      width: 12px;
      height: 12px;
      color: var(--fg-muted);
      pointer-events: none;
    }}
    .control {{
      width: 100%;
      background: var(--bg);
      color: var(--fg);
      border: none;
      padding: 0 10px;
      font-size: 12.5px;
      font-family: var(--font-mono);
      border-radius: 0;
      height: 34px;
      -webkit-appearance: none;
      appearance: none;
    }}
    select.control {{
      padding-right: 26px;
      cursor: pointer;
    }}
    #search-input {{
      font-family: var(--font-sans);
      font-size: 13px;
      padding-left: 31px;
      padding-right: 48px;
    }}
    .control:focus {{
      outline: none;
      background: var(--bg-subtle);
      box-shadow: inset 0 -2px 0 0 var(--border-strong);
    }}

    /* Faceted Regulatory Tag Bar */
    .tag-strip {{
      padding: 8px 10px;
      background: var(--bg-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
       gap: 10px;
      flex-wrap: wrap;
    }}
    .tag-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      flex: 1;
    }}
    .tag-btn {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--bg);
      color: var(--fg);
      border: 1px solid var(--border);
      padding: 2px 6px;
      font-family: var(--font-mono);
      font-size: 11px;
      cursor: pointer;
      user-select: none;
    }}
    .tag-btn:hover {{
      border-color: var(--border-strong);
    }}
    .tag-btn.active {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      border-color: var(--border-strong);
    }}
    .tag-btn.zero {{
      opacity: 0.35;
    }}
    .tag-btn .cnt {{
      color: var(--fg-muted);
      font-size: 10px;
    }}
    .tag-btn.active .cnt {{ color: #cccccc; }}

    .mode-switch {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: var(--fg-muted);
      flex-shrink: 0;
    }}
    .mode-btn {{
      background: var(--bg);
      color: var(--fg-secondary);
      border: 1px solid var(--border);
      padding: 2px 6px;
      font-family: var(--font-mono);
      font-size: 10px;
      cursor: pointer;
    }}
    .mode-btn.active {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      border-color: var(--border-strong);
    }}

    /* Status & Active Filter Breadcrumb Bar */
    .toolbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 4px 0 10px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 14px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--fg-secondary);
      flex-wrap: wrap;
      gap: 8px;
    }}
    .toolbar-left {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .perf-badge {{
      color: var(--fg-muted);
      font-size: 10.5px;
    }}
    .active-chip {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--bg-invert);
      color: var(--fg-invert);
      padding: 1px 6px;
      font-size: 10.5px;
      cursor: pointer;
      border: 1px solid var(--border-strong);
    }}
    .active-chip:hover {{
      background: #333333;
    }}
    .toolbar-actions {{
      display: flex;
      gap: 6px;
    }}

    /* Sections, Subsection Quick-Jump & 4-Column Datasheet Rows */
    .sec-block {{
      margin-bottom: 28px;
    }}
    .sec-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 7px 10px;
      background: var(--bg-invert);
      color: var(--fg-invert);
    }}
    .sec-head-left {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }}
    .sec-count {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: #cccccc;
    }}
    .sec-desc {{
      color: var(--fg-secondary);
      font-size: 12.5px;
      padding: 7px 10px 6px;
      background: var(--bg-subtle);
      border-left: 1px solid var(--border);
      border-right: 1px solid var(--border);
    }}
    .sub-jump-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      padding: 4px 10px 8px;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-top: none;
      margin-bottom: 12px;
    }}
    .sub-jump-btn {{
      background: var(--bg);
      color: var(--fg-secondary);
      border: 1px solid var(--border);
      padding: 2px 7px;
      font-family: var(--font-mono);
      font-size: 11px;
      cursor: pointer;
    }}
    .sub-jump-btn:hover {{
      border-color: var(--border-strong);
      color: var(--fg);
    }}
    .sub-jump-btn.active {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      border-color: var(--border-strong);
    }}
    .sub-jump-btn .cnt {{
      color: var(--fg-muted);
      font-size: 10px;
    }}
    .sub-jump-btn.active .cnt {{ color: #cccccc; }}

    .sub-block {{
      margin-bottom: 16px;
      border: 1px solid var(--border);
    }}
    .sub-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 6px 10px;
      background: var(--bg-subtle);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--fg);
      border-bottom: 1px solid var(--border);
    }}
    .sub-head-cnt {{
      font-size: 11px;
      color: var(--fg-muted);
      font-weight: 500;
    }}
    .col-head {{
      display: grid;
      grid-template-columns: 235px minmax(0, 1fr) 196px 108px;
      gap: 14px;
      padding: 4px 10px;
      border-bottom: 1px solid var(--border);
      background: #fafafa;
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--fg-muted);
    }}
    .col-right {{ text-align: right; }}
    .entry-table {{ width: 100%; }}
    .entry-row {{
      border-bottom: 1px solid #ebebeb;
      display: grid;
      grid-template-columns: 235px minmax(0, 1fr) 196px 108px;
      gap: 14px;
      padding: 7.5px 10px;
      align-items: start;
      position: relative;
    }}
    .entry-row:last-child {{ border-bottom: none; }}
    .entry-row:hover {{
      background: var(--bg-subtle);
    }}
    .entry-row.kb-focus {{
      background: var(--bg-subtle);
      box-shadow: inset 3px 0 0 0 var(--border-strong);
    }}
    @media (max-width: 860px) {{
      .col-head {{ display: none; }}
      .entry-row {{
        grid-template-columns: 1fr;
        gap: 6px;
      }}
      .entry-lic-cell {{ text-align: left !important; }}
    }}
    .entry-name-cell {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }}
    .entry-link {{
      display: inline;
      font-weight: 700;
      font-size: 13px;
      line-height: 1.35;
      color: var(--fg);
      text-decoration: underline;
      text-decoration-color: var(--border-mid);
      text-underline-offset: 2px;
      word-break: break-word;
    }}
    .entry-link:hover {{
      text-decoration-color: var(--border-strong);
    }}
    .entry-link .ic-ext {{
      width: 11px;
      height: 11px;
      color: var(--fg-muted);
      margin-left: 3px;
      vertical-align: -1px;
    }}
    .entry-slug {{
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: var(--fg-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .entry-desc-cell {{
      color: var(--fg-secondary);
      font-size: 13px;
      line-height: 1.48;
      padding-right: 6px;
    }}
    .entry-tags-cell {{
      display: flex;
      flex-wrap: wrap;
      gap: 3px;
      align-items: flex-start;
      font-family: var(--font-mono);
      font-size: 10.5px;
    }}
    .entry-lic-cell {{
      text-align: right;
      font-family: var(--font-mono);
      font-size: 10.5px;
      white-space: nowrap;
    }}
    .chip-tag, .chip-lic {{
      display: inline-block;
      padding: 1px 5px;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--fg-secondary);
      cursor: pointer;
      line-height: 1.35;
    }}
    .chip-lic {{
      background: var(--bg-subtle);
      color: var(--fg);
      font-weight: 600;
    }}
    .chip-tag:hover, .chip-lic:hover {{
      border-color: var(--border-strong);
      color: var(--fg);
    }}
    .chip-tag.active, .chip-lic.active {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      border-color: var(--border-strong);
    }}
    .empty-box {{
      border: 1px solid var(--border-strong);
      padding: 36px;
      text-align: center;
      font-family: var(--font-mono);
      color: var(--fg-muted);
    }}

    /* Matrix & Code tabs */
    table.matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    table.matrix-table th, table.matrix-table td {{
      border: 1px solid var(--border);
      padding: 9px 11px;
      text-align: left;
      vertical-align: top;
    }}
    table.matrix-table th {{
      background: var(--bg-invert);
      color: var(--fg-invert);
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    code {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      background: var(--bg-subtle);
      padding: 1px 4px;
      border: 1px solid var(--border);
    }}
    .code-card {{
      border: 1px solid var(--border-strong);
      margin-bottom: 16px;
    }}
    .code-card-head {{
      background: var(--bg-subtle);
      border-bottom: 1px solid var(--border);
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 12px;
    }}
    .code-card-head a {{ text-decoration: underline; }}
    .code-card-desc {{
      padding: 7px 12px;
      border-bottom: 1px solid var(--border);
      color: var(--fg-secondary);
      font-size: 12.5px;
    }}
    pre {{
      padding: 12px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 12px;
      line-height: 1.5;
      background: var(--bg);
      color: var(--fg);
    }}
    pre code {{ border: none; background: none; padding: 0; }}
    .arch-box {{
      border: 1px solid var(--border-strong);
      padding: 16px;
      margin-bottom: 16px;
      background: var(--bg);
      text-align: center;
    }}
    .arch-box img {{
      max-width: 100%;
      height: auto;
    }}
    footer {{
      border-top: 1px solid var(--border);
      padding: 16px 0 32px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--fg-muted);
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }}
    footer a {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <!-- Airgapped inline SVG sprite sheet -->
  <svg xmlns="http://www.w3.org/2000/svg" style="display:none">
    <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
    <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></symbol>
    <symbol id="i-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></symbol>
    <symbol id="i-list" viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></symbol>
    <symbol id="i-table" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="1"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="9" x2="9" y2="21"/></symbol>
    <symbol id="i-code" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></symbol>
    <symbol id="i-braces" viewBox="0 0 24 24"><path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></symbol>
    <symbol id="i-reset" viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></symbol>
    <symbol id="i-copy" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="1"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></symbol>
    <symbol id="i-link" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></symbol>
    <symbol id="i-ext" viewBox="0 0 24 24"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></symbol>
    <symbol id="sec-1" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/></symbol>
    <symbol id="sec-2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
    <symbol id="sec-3" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></symbol>
    <symbol id="sec-4" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></symbol>
    <symbol id="sec-5" viewBox="0 0 24 24"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/><rect x="2" y="3" width="20" height="18" rx="1"/></symbol>
    <symbol id="sec-6" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></symbol>
    <symbol id="sec-7" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="1"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></symbol>
    <symbol id="sec-8" viewBox="0 0 24 24"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></symbol>
    <symbol id="sec-9" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></symbol>
  </svg>

  <header>
    <div class="wrap">
      <div class="header-top">
        <div>
          <div class="brand-group">
            <a class="brand" href="./">
              <svg class="brand-mark"><use href="#i-shield"/></svg>
              <h1>Awesome Compliance-as-Code</h1>
            </a>
            <span class="ver-pill">v{catalog["schema_version"]}</span>
          </div>
          <p class="subtitle">
            Machine-readable specifications, policy engines, supply-chain verifiers, runtime auditors, and regulatory-to-code mappings.
          </p>
        </div>
        <div class="header-links">
          <a class="btn" href="llms.txt" title="Concise agent index (llmstxt.org)"><svg class="ic ic-sm"><use href="#sec-1"/></svg>llms.txt</a>
          <a class="btn" href="llms-full.txt" title="Full plain-text catalog for LLM context"><svg class="ic ic-sm"><use href="#sec-1"/></svg>llms-full.txt</a>
          <a class="btn" href="catalog.json" title="Machine-readable JSON API"><svg class="ic ic-sm"><use href="#i-braces"/></svg>catalog.json</a>
          <a class="btn" href="{REPO_URL}" target="_blank" rel="noopener"><svg class="ic ic-sm"><use href="#i-ext"/></svg>GitHub</a>
        </div>
      </div>
    </div>
  </header>

  <div class="nav-strip">
    <div class="wrap nav-strip-inner">
      <nav class="tabs" aria-label="Views">
        <button class="tab-btn active" data-tab="catalog" type="button"><svg class="ic"><use href="#i-list"/></svg>Catalog ({total_entries})</button>
        <button class="tab-btn" data-tab="matrix" type="button"><svg class="ic"><use href="#i-table"/></svg>Regulatory Matrix (8)</button>
        <button class="tab-btn" data-tab="examples" type="button"><svg class="ic"><use href="#i-code"/></svg>Reference Policies (4)</button>
        <button class="tab-btn" data-tab="api" type="button"><svg class="ic"><use href="#i-braces"/></svg>Architecture &amp; API</button>
      </nav>
      <div class="telemetry-bar">
        <span>{total_entries} VERIFIED &middot; {total_sections} DOMAINS &middot; {total_tags} FRAMEWORKS</span>
        <span class="kbd-legend">
          <span><kbd class="kbd">/</kbd> Search</span>
          <span><kbd class="kbd">1-9</kbd> Domain</span>
          <span><kbd class="kbd">j/k</kbd> Row</span>
          <span><kbd class="kbd">Esc</kbd> Reset</span>
        </span>
      </div>
    </div>
  </div>

  <main class="wrap">
    <section id="tab-catalog" class="pane active">
      <div class="workspace">
        <aside class="domain-rail" aria-label="Domain filter">
          <div class="rail-title">
            <span>Domains</span>
            <span>0&ndash;9</span>
          </div>
          <ul id="domain-rail-list" class="rail-list"></ul>
        </aside>

        <div>
          <div class="filter-box">
            <div class="filter-top">
              <div class="search-wrap">
                <svg class="ic ic-search"><use href="#i-search"/></svg>
                <input id="search-input" class="control" type="search" autocomplete="off" spellcheck="false" placeholder="Filter by tool, repo owner, eBPF, SBOM, OSCAL, Rego, Sigstore..." aria-label="Search catalog">
                <button id="search-clear" class="search-clear" type="button" title="Clear search (Esc)">CLEAR</button>
                <span id="search-kbd" class="kbd-hint">/</span>
              </div>
              <div class="select-wrap">
                <select id="subsection-select" class="control" aria-label="Subsection filter">
                  <option value="">All subsections ({total_subsections})</option>
                </select>
                <svg class="ic ic-chev"><use href="#i-chevron"/></svg>
              </div>
              <div class="select-wrap">
                <select id="license-select" class="control" aria-label="License filter">
                  <option value="">All SPDX licenses ({len(catalog["licenses"])})</option>
                  <optgroup label="License Family">
                    <option value="family:permissive">Permissive (Apache-2.0, MIT, BSD, ISC, UPL)</option>
                    <option value="family:weak-copyleft">Weak Copyleft (MPL-2.0, EPL-2.0, LGPL, CPAL)</option>
                    <option value="family:strong-copyleft">Strong Copyleft (GPL-2.0, GPL-3.0, AGPL-3.0)</option>
                    <option value="family:open-spec">Open Spec / Public Domain (CC, Community-Spec)</option>
                  </optgroup>
                  <optgroup id="license-spdx-group" label="SPDX Identifier"></optgroup>
                </select>
                <svg class="ic ic-chev"><use href="#i-chevron"/></svg>
              </div>
            </div>

            <div class="tag-strip">
              <div id="tag-pills" class="tag-pills"></div>
              <div class="mode-switch">
                <span>LOGIC:</span>
                <button id="mode-any" class="mode-btn active" type="button" title="Match ANY selected tag">OR</button>
                <button id="mode-all" class="mode-btn" type="button" title="Match ALL selected tags">AND</button>
              </div>
            </div>
          </div>

          <div class="toolbar">
            <div class="toolbar-left">
              <strong id="results-summary">Showing {total_entries} of {total_entries} entries</strong>
              <span id="perf-readout" class="perf-badge"></span>
              <div id="active-chips" class="toolbar-left"></div>
            </div>
            <div class="toolbar-actions">
              <button id="share-url-btn" class="btn" type="button" title="Copy deep link to current view"><svg class="ic ic-sm"><use href="#i-link"/></svg><span>Copy View URL</span></button>
              <button id="export-json-btn" class="btn" type="button" title="Download filtered entries as JSON"><svg class="ic ic-sm"><use href="#i-download"/></svg>Export JSON</button>
              <button id="reset-filters-btn" class="btn" type="button" title="Reset all filters (Esc)"><svg class="ic ic-sm"><use href="#i-reset"/></svg>Reset</button>
            </div>
          </div>

          <div id="catalog-container">{prerendered_catalog}</div>
        </div>
      </div>
    </section>

    <section id="tab-matrix" class="pane">
      <table class="matrix-table">
        <thead>
          <tr>
            <th>Regulation / Standard</th>
            <th>Article / Control</th>
            <th>Legal / Technical Requirement</th>
            <th>Deterministic Engineering Control (CaC)</th>
            <th>Open-Source Tooling &amp; Artifact</th>
          </tr>
        </thead>
        <tbody id="matrix-tbody">{prerendered_matrix}</tbody>
      </table>
    </section>

    <section id="tab-examples" class="pane">
      <div id="examples-container">{prerendered_examples}</div>
    </section>

    <section id="tab-api" class="pane">
      <div class="arch-box">
        <img src="assets/compliance-lifecycle.svg" alt="Compliance-as-Code Pipeline Lifecycle">
      </div>
      <div class="code-card">
        <div class="code-card-head">
          <strong>AI Agent &amp; LLM Discovery (llms.txt / llms-full.txt)</strong>
          <div>
            <a class="btn" href="llms.txt">llms.txt</a>
            <a class="btn" href="llms-full.txt">llms-full.txt</a>
          </div>
        </div>
        <div class="code-card-desc">
          Standardized plain-text endpoints following the llmstxt.org specification for low-token agent indexing and full-context retrieval:
        </div>
        <pre><code># Concise index (~10 KB): domain map, tag counts, license counts, and query deep links
curl -sSfL {SITE_BASE_URL}/llms.txt

# Complete plain-text catalog ({total_entries} entries + Regulatory Matrix + Reference Code)
curl -sSfL {SITE_BASE_URL}/llms-full.txt</code></pre>
      </div>

      <div class="code-card">
        <div class="code-card-head">
          <strong>Structured JSON API (catalog.json)</strong>
          <a class="btn" href="catalog.json">catalog.json</a>
        </div>
        <div class="code-card-desc">
          Compiled deterministically from README.md on every commit. Query directly with curl and jq:
        </div>
        <pre><code># 1. Filter DORA + Apache-2.0 tools
curl -sSfL {SITE_BASE_URL}/catalog.json \\
  | jq '.entries[] | select((.tags | index("DORA")) and .license == "Apache-2.0") | {{name, repo, url, subsection}}'

# 2. Count entries per regulatory framework
curl -sSfL {SITE_BASE_URL}/catalog.json \\
  | jq '.regulatory_tags'</code></pre>
      </div>
    </section>
  </main>

  <div class="wrap">
    <footer>
      <div>CC0-1.0 Public Domain &middot; <a href="llms.txt">llms.txt</a> &middot; <a href="llms-full.txt">llms-full.txt</a> &middot; <a href="catalog.json">catalog.json</a> &middot; <a href="sitemap.xml">sitemap.xml</a> &middot; <a href="robots.txt">robots.txt</a></div>
      <div><a href="{REPO_URL}">github.com/fabriziosalmi/awesome-compliance-as-code</a></div>
    </footer>
  </div>

  <script id="catalog-data" type="application/json">{embedded_json}</script>
  <script>
    (() => {{
      const t0 = performance.now();
      const DATA = JSON.parse(document.getElementById("catalog-data").textContent);

      // Pre-index entries once at startup (< 0.8ms) for sub-millisecond filtering
      DATA.entries.forEach(item => {{
        item._tagSet = new Set(item.tags);
        item._hay = `${{item.name}} ${{item.repo}} ${{item.description}} ${{item.tags.join(" ")}} ${{item.license}} ${{item.subsection}}`.toLowerCase();
      }});

      const searchInput = document.getElementById("search-input");
      const searchClear = document.getElementById("search-clear");
      const searchKbd = document.getElementById("search-kbd");
      const subsectionSelect = document.getElementById("subsection-select");
      const licenseSelect = document.getElementById("license-select");
      const licenseSpdxGroup = document.getElementById("license-spdx-group");
      const tagPillsContainer = document.getElementById("tag-pills");
      const domainRailList = document.getElementById("domain-rail-list");
      const catalogContainer = document.getElementById("catalog-container");
      const examplesContainer = document.getElementById("examples-container");
      const matrixTbody = document.getElementById("matrix-tbody");
      const resultsSummary = document.getElementById("results-summary");
      const perfReadout = document.getElementById("perf-readout");
      const activeChips = document.getElementById("active-chips");
      const modeAnyBtn = document.getElementById("mode-any");
      const modeAllBtn = document.getElementById("mode-all");
      const resetBtn = document.getElementById("reset-filters-btn");
      const exportBtn = document.getElementById("export-json-btn");
      const shareUrlBtn = document.getElementById("share-url-btn");

      const SHORT_SECTION_NAMES = {{
        1: "1. Formats & Schemas",
        2: "2. Policy Engines",
        3: "3. IaC & SAST Auditing",
        4: "4. Supply Chain & SBOM",
        5: "5. Host & Kernel Runtime",
        6: "6. Cloud & OSCAL Evidence",
        7: "7. AI/ML Governance",
        8: "8. Policy Packs & Baselines",
        9: "9. Reference Blueprints"
      }};

      let selectedSection = "";
      let selectedTags = new Set();
      let tagMode = "any";
      let currentFiltered = DATA.entries;
      let kbFocusIdx = -1;

      function escapeHtml(str) {{
        return String(str)
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;");
      }}

      function highlightText(text, query) {{
        const safe = escapeHtml(text);
        if (!query || query.length < 2) return safe;
        const escapedQ = escapeHtml(query).replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&");
        try {{
          const re = new RegExp(`(${{escapedQ}})`, "gi");
          return safe.replace(re, "<mark>$1</mark>");
        }} catch (_) {{
          return safe;
        }}
      }}

      // Populate SPDX license dropdown
      Object.entries(DATA.licenses).forEach(([lic, count]) => {{
        const opt = document.createElement("option");
        opt.value = lic;
        opt.textContent = `${{lic}} (${{count}})`;
        licenseSpdxGroup.appendChild(opt);
      }});

      // Populate regulatory tag buttons
      Object.entries(DATA.regulatory_tags).forEach(([tag, count]) => {{
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tag-btn";
        btn.dataset.tag = tag;
        btn.innerHTML = `<span>[${{escapeHtml(tag)}}]</span><span class="cnt" data-tag-cnt="${{escapeHtml(tag)}}">${{count}}</span>`;
        btn.addEventListener("click", () => {{
          if (selectedTags.has(tag)) selectedTags.delete(tag);
          else selectedTags.add(tag);
          applyFilters();
        }});
        tagPillsContainer.appendChild(btn);
      }});

      function populateSubsections(secId) {{
        const currentVal = subsectionSelect.value;
        let totalSubs = 0;
        DATA.sections.forEach(sec => {{
          if (!secId || sec.id === secId) totalSubs += sec.subsections.length;
        }});
        subsectionSelect.innerHTML = `<option value="">All subsections (${{totalSubs}})</option>`;
        DATA.sections.forEach(sec => {{
          if (secId && sec.id !== secId) return;
          sec.subsections.forEach(sub => {{
            const opt = document.createElement("option");
            opt.value = sub.id;
            opt.textContent = secId ? `${{sub.title}} (${{sub.count}})` : `${{sec.number}}. ${{sub.title}} (${{sub.count}})`;
            subsectionSelect.appendChild(opt);
          }});
        }});
        if ([...subsectionSelect.options].some(o => o.value === currentVal)) {{
          subsectionSelect.value = currentVal;
        }}
      }}

      function matchesBaseWithout(item, ignoreField, q, sub, lic) {{
        if (ignoreField !== "section" && selectedSection && item.section_id !== selectedSection) return false;
        if (ignoreField !== "subsection" && sub && item.subsection_id !== sub) return false;
        if (ignoreField !== "license" && lic) {{
          if (lic.startsWith("family:")) {{
            if (item.license_family !== lic.slice(7)) return false;
          }} else if (item.license !== lic) {{
            return false;
          }}
        }}
        if (ignoreField !== "tags" && selectedTags.size > 0) {{
          if (tagMode === "all") {{
            for (const t of selectedTags) {{
              if (!item._tagSet.has(t)) return false;
            }}
          }} else {{
            let ok = false;
            for (const t of selectedTags) {{
              if (item._tagSet.has(t)) {{ ok = true; break; }}
            }}
            if (!ok) return false;
          }}
        }}
        if (q && !item._hay.includes(q)) return false;
        return true;
      }}

      function updateFacetedNavigation(q, sub, lic) {{
        // 1. Compute live counts per domain ignoring 'section' filter
        const secCounts = new Map();
        let allDomainCount = 0;
        DATA.entries.forEach(item => {{
          if (matchesBaseWithout(item, "section", q, "", lic)) {{
            allDomainCount++;
            secCounts.set(item.section_id, (secCounts.get(item.section_id) || 0) + 1);
          }}
        }});

        domainRailList.innerHTML = "";
        const allLi = document.createElement("li");
        const allBtn = document.createElement("button");
        allBtn.type = "button";
        allBtn.className = "rail-item" + (selectedSection === "" ? " active" : "");
        allBtn.innerHTML = `<span class="rail-item-left"><svg class="ic"><use href="#i-list"/></svg><span>All Domains</span></span><span class="rail-cnt">${{allDomainCount}}</span>`;
        allBtn.addEventListener("click", () => {{
          selectedSection = "";
          populateSubsections("");
          subsectionSelect.value = "";
          applyFilters();
        }});
        allLi.appendChild(allBtn);
        domainRailList.appendChild(allLi);

        DATA.sections.forEach(sec => {{
          const cnt = secCounts.get(sec.id) || 0;
          const li = document.createElement("li");
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "rail-item" + (selectedSection === sec.id ? " active" : "") + (cnt === 0 ? " dim" : "");
          const shortTitle = SHORT_SECTION_NAMES[sec.number] || sec.title;
          btn.innerHTML = `
            <span class="rail-item-left">
              <svg class="ic"><use href="#sec-${{sec.number}}"/></svg>
              <span>${{escapeHtml(shortTitle)}}</span>
            </span>
            <span class="rail-cnt">${{cnt}}</span>
          `;
          btn.addEventListener("click", () => {{
            selectedSection = (selectedSection === sec.id) ? "" : sec.id;
            populateSubsections(selectedSection);
            subsectionSelect.value = "";
            applyFilters();
          }});
          li.appendChild(btn);
          domainRailList.appendChild(li);
        }});

        // 2. Compute live counts per regulatory tag
        const tagFacetCounts = new Map();
        DATA.entries.forEach(item => {{
          if (matchesBaseWithout(item, tagMode === "any" ? "tags" : "none", q, sub, lic)) {{
            item.tags.forEach(t => {{
              tagFacetCounts.set(t, (tagFacetCounts.get(t) || 0) + 1);
            }});
          }}
        }});

        tagPillsContainer.querySelectorAll(".tag-btn").forEach(btn => {{
          const t = btn.dataset.tag;
          const cnt = tagFacetCounts.get(t) || 0;
          const isAct = selectedTags.has(t);
          btn.classList.toggle("active", isAct);
          btn.classList.toggle("zero", cnt === 0 && !isAct);
          const cntEl = btn.querySelector(".cnt");
          if (cntEl) cntEl.textContent = cnt;
        }});

        modeAnyBtn.classList.toggle("active", tagMode === "any");
        modeAllBtn.classList.toggle("active", tagMode === "all");
      }}

      function renderActiveChips(q, sub, lic) {{
        activeChips.innerHTML = "";
        if (selectedSection) {{
          const secObj = DATA.sections.find(s => s.id === selectedSection);
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "active-chip";
          chip.innerHTML = `<span>Domain: ${{escapeHtml(secObj ? SHORT_SECTION_NAMES[secObj.number] : selectedSection)}}</span><span>&times;</span>`;
          chip.addEventListener("click", () => {{
            selectedSection = "";
            populateSubsections("");
            subsectionSelect.value = "";
            applyFilters();
          }});
          activeChips.appendChild(chip);
        }}
        if (sub) {{
          let subTitle = sub;
          DATA.sections.forEach(s => s.subsections.forEach(sb => {{ if (sb.id === sub) subTitle = sb.title; }}));
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "active-chip";
          chip.innerHTML = `<span>Sub: ${{escapeHtml(subTitle)}}</span><span>&times;</span>`;
          chip.addEventListener("click", () => {{
            subsectionSelect.value = "";
            applyFilters();
          }});
          activeChips.appendChild(chip);
        }}
        if (lic) {{
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "active-chip";
          chip.innerHTML = `<span>License: ${{escapeHtml(lic)}}</span><span>&times;</span>`;
          chip.addEventListener("click", () => {{
            licenseSelect.value = "";
            applyFilters();
          }});
          activeChips.appendChild(chip);
        }}
        selectedTags.forEach(t => {{
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "active-chip";
          chip.innerHTML = `<span>[${{escapeHtml(t)}}]</span><span>&times;</span>`;
          chip.addEventListener("click", () => {{
            selectedTags.delete(t);
            applyFilters();
          }});
          activeChips.appendChild(chip);
        }});
        if (q) {{
          const chip = document.createElement("button");
          chip.type = "button";
          chip.className = "active-chip";
          chip.innerHTML = `<span>Query: "${{escapeHtml(q)}}"</span><span>&times;</span>`;
          chip.addEventListener("click", () => {{
            searchInput.value = "";
            applyFilters();
          }});
          activeChips.appendChild(chip);
        }}
      }}

      function applyFilters() {{
        const startMs = performance.now();
        const q = searchInput.value.trim().toLowerCase();
        const sub = subsectionSelect.value;
        const lic = licenseSelect.value;

        searchClear.style.display = q ? "block" : "none";
        searchKbd.style.display = q ? "none" : "block";

        currentFiltered = DATA.entries.filter(item => matchesBaseWithout(item, "none", q, sub, lic));
        kbFocusIdx = -1;

        updateFacetedNavigation(q, sub, lic);
        renderActiveChips(q, sub, lic);
        renderCatalog(currentFiltered, q, sub, lic);
        syncUrlState();

        const elapsed = (performance.now() - startMs).toFixed(1);
        perfReadout.textContent = `\u00b7 ${{elapsed}}ms`;
      }}

      function renderCatalog(entries, q, activeSub, activeLic) {{
        resultsSummary.textContent = `Showing ${{entries.length}} of ${{DATA.total_entries}} entries`;
        if (entries.length === 0) {{
          catalogContainer.innerHTML = `<div class="empty-box">No entries match the active filters. Press Esc or click Reset to restore all ${{DATA.total_entries}} entries.</div>`;
          return;
        }}

        const bySec = new Map();
        entries.forEach(e => {{
          if (!bySec.has(e.section_id)) bySec.set(e.section_id, new Map());
          const subMap = bySec.get(e.section_id);
          if (!subMap.has(e.subsection_id)) subMap.set(e.subsection_id, []);
          subMap.get(e.subsection_id).push(e);
        }});

        const frag = document.createDocumentFragment();
        DATA.sections.forEach(sec => {{
          if (!bySec.has(sec.id)) return;
          const subMap = bySec.get(sec.id);
          const secBlock = document.createElement("div");
          secBlock.className = "sec-block";

          let secTotal = 0;
          subMap.forEach(arr => {{ secTotal += arr.length; }});

          const subPillsHtml = sec.subsections.map(sub => {{
            const cnt = (subMap.get(sub.id) || []).length;
            if (cnt === 0 && activeSub !== sub.id) return "";
            const isAct = activeSub === sub.id ? " active" : "";
            return `<button class="sub-jump-btn${{isAct}}" type="button" data-sub-jump="${{escapeHtml(sub.id)}}">${{escapeHtml(sub.title)}} <span class="cnt">${{cnt}}</span></button>`;
          }}).join("");

          secBlock.innerHTML = `
            <div class="sec-head">
              <div class="sec-head-left">
                <svg class="ic"><use href="#sec-${{sec.number}}"/></svg>
                <span>${{escapeHtml(sec.title)}}</span>
              </div>
              <span class="sec-count">${{secTotal}} entries</span>
            </div>
            <p class="sec-desc">${{escapeHtml(sec.description)}}</p>
            <div class="sub-jump-strip">${{subPillsHtml}}</div>
          `;

          sec.subsections.forEach(sub => {{
            const items = subMap.get(sub.id);
            if (!items || items.length === 0) return;
            const subBlock = document.createElement("div");
            subBlock.className = "sub-block";
            subBlock.innerHTML = `
              <div class="sub-head">
                <span>${{escapeHtml(sub.title)}}</span>
                <span class="sub-head-cnt">${{items.length}}</span>
              </div>
              <div class="col-head">
                <span>Artifact / Repository</span>
                <span>Technical Specification</span>
                <span>Frameworks</span>
                <span class="col-right">License</span>
              </div>
            `;
            const listDiv = document.createElement("div");
            listDiv.className = "entry-table";

            items.forEach(item => {{
              const row = document.createElement("div");
              row.className = "entry-row";
              const tagsHtml = item.tags.map(t => {{
                const act = selectedTags.has(t) ? " active" : "";
                return `<span class="chip-tag${{act}}" data-click-tag="${{escapeHtml(t)}}" title="Filter by [${{escapeHtml(t)}}]">[${{escapeHtml(t)}}]</span>`;
              }}).join("");
              const licAct = activeLic === item.license ? " active" : "";
              row.innerHTML = `
                <div class="entry-name-cell">
                  <a class="entry-link" href="${{escapeHtml(item.url)}}" target="_blank" rel="noopener">${{highlightText(item.name, q)}}<svg class="ic ic-ext"><use href="#i-ext"/></svg></a>
                  <span class="entry-slug">${{highlightText(item.repo, q)}}</span>
                </div>
                <div class="entry-desc-cell">${{highlightText(item.description, q)}}</div>
                <div class="entry-tags-cell">${{tagsHtml}}</div>
                <div class="entry-lic-cell">
                  <span class="chip-lic${{licAct}}" data-click-lic="${{escapeHtml(item.license)}}" title="Filter by license ${{escapeHtml(item.license)}}">${{escapeHtml(item.license)}}</span>
                </div>
              `;
              listDiv.appendChild(row);
            }});

            subBlock.appendChild(listDiv);
            secBlock.appendChild(subBlock);
          }});

          frag.appendChild(secBlock);
        }});

        catalogContainer.innerHTML = "";
        catalogContainer.appendChild(frag);
      }}

      // Delegated clicks inside catalog
      catalogContainer.addEventListener("click", (e) => {{
        const subJump = e.target.closest("[data-sub-jump]");
        if (subJump) {{
          const subId = subJump.dataset.subJump;
          subsectionSelect.value = (subsectionSelect.value === subId) ? "" : subId;
          applyFilters();
          return;
        }}
        const tagEl = e.target.closest("[data-click-tag]");
        if (tagEl) {{
          const t = tagEl.dataset.clickTag;
          if (selectedTags.has(t)) selectedTags.delete(t);
          else selectedTags.add(t);
          applyFilters();
          return;
        }}
        const licEl = e.target.closest("[data-click-lic]");
        if (licEl) {{
          const l = licEl.dataset.clickLic;
          licenseSelect.value = (licenseSelect.value === l) ? "" : l;
          applyFilters();
        }}
      }});

      // Matrix -> Catalog filter jump
      matrixTbody.addEventListener("click", (e) => {{
        const btn = e.target.closest("[data-matrix-tag]");
        if (!btn) return;
        const tag = btn.dataset.matrixTag;
        selectedTags.clear();
        selectedTags.add(tag);
        activateTab("catalog");
        applyFilters();
        window.scrollTo({{ top: 0, behavior: "instant" }});
      }});

      // Copy code examples
      examplesContainer.addEventListener("click", (e) => {{
        const btn = e.target.closest(".copy-btn");
        if (!btn) return;
        const idx = Number(btn.dataset.exIdx);
        const ex = DATA.examples[idx];
        if (!ex) return;
        const labelSpan = btn.querySelector("span");
        navigator.clipboard.writeText(ex.code);
        labelSpan.textContent = "Copied";
        setTimeout(() => {{ labelSpan.textContent = "Copy"; }}, 1200);
      }});

      // Tabs
      const tabBtns = document.querySelectorAll(".tab-btn");
      const tabPanes = document.querySelectorAll(".pane");
      function activateTab(tabName) {{
        tabBtns.forEach(b => b.classList.toggle("active", b.dataset.tab === tabName));
        tabPanes.forEach(p => p.classList.toggle("active", p.id === `tab-${{tabName}}`));
      }}
      tabBtns.forEach(btn => {{
        btn.addEventListener("click", () => {{
          activateTab(btn.dataset.tab);
          syncUrlState();
        }});
      }});

      function loadStateFromUrl() {{
        const params = new URLSearchParams(window.location.search);
        if (params.get("q")) searchInput.value = params.get("q");
        if (params.get("section")) {{
          selectedSection = params.get("section");
          populateSubsections(selectedSection);
        }} else {{
          populateSubsections("");
        }}
        if (params.get("subsection")) subsectionSelect.value = params.get("subsection");
        if (params.get("license")) licenseSelect.value = params.get("license");
        if (params.get("mode") === "all") tagMode = "all";
        if (params.get("tags")) {{
          params.get("tags").split(",").filter(Boolean).forEach(t => selectedTags.add(t));
        }}
        if (params.get("tab")) activateTab(params.get("tab"));
      }}

      function syncUrlState() {{
        const params = new URLSearchParams();
        const q = searchInput.value.trim();
        const sub = subsectionSelect.value;
        const lic = licenseSelect.value;
        const activeTab = document.querySelector(".tab-btn.active")?.dataset.tab;
        if (q) params.set("q", q);
        if (selectedSection) params.set("section", selectedSection);
        if (sub) params.set("subsection", sub);
        if (lic) params.set("license", lic);
        if (selectedTags.size > 0) params.set("tags", [...selectedTags].join(","));
        if (tagMode === "all" && selectedTags.size > 0) params.set("mode", "all");
        if (activeTab && activeTab !== "catalog") params.set("tab", activeTab);
        const qs = params.toString();
        const newUrl = qs ? `${{window.location.pathname}}?${{qs}}` : window.location.pathname;
        window.history.replaceState(null, "", newUrl);
      }}

      function resetAll() {{
        searchInput.value = "";
        selectedSection = "";
        populateSubsections("");
        subsectionSelect.value = "";
        licenseSelect.value = "";
        selectedTags.clear();
        tagMode = "any";
        applyFilters();
      }}

      searchInput.addEventListener("input", applyFilters);
      searchClear.addEventListener("click", () => {{
        searchInput.value = "";
        searchInput.focus();
        applyFilters();
      }});
      subsectionSelect.addEventListener("change", applyFilters);
      licenseSelect.addEventListener("change", applyFilters);

      modeAnyBtn.addEventListener("click", () => {{ tagMode = "any"; applyFilters(); }});
      modeAllBtn.addEventListener("click", () => {{ tagMode = "all"; applyFilters(); }});
      resetBtn.addEventListener("click", resetAll);

      shareUrlBtn.addEventListener("click", () => {{
        navigator.clipboard.writeText(window.location.href);
        const span = shareUrlBtn.querySelector("span");
        span.textContent = "Copied URL";
        setTimeout(() => {{ span.textContent = "Copy View URL"; }}, 1200);
      }});

      exportBtn.addEventListener("click", () => {{
        const cleanExport = currentFiltered.map(({{_tagSet, _hay, ...rest}}) => rest);
        const blob = new Blob([JSON.stringify(cleanExport, null, 2)], {{ type: "application/json" }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `compliance-as-code-filtered-${{cleanExport.length}}.json`;
        a.click();
        URL.revokeObjectURL(url);
      }});

      // Precision keyboard navigation: /, Esc, 0-9, j/k, Enter
      window.addEventListener("keydown", (e) => {{
        const inInput = ["INPUT", "SELECT", "TEXTAREA"].includes(document.activeElement?.tagName);
        if (e.key === "/" && !inInput) {{
          e.preventDefault();
          searchInput.focus();
          searchInput.select();
          return;
        }}
        if (e.key === "Escape") {{
          if (document.activeElement === searchInput && searchInput.value) {{
            searchInput.value = "";
            applyFilters();
            return;
          }}
          if (inInput) {{
            document.activeElement.blur();
            return;
          }}
          resetAll();
          return;
        }}
        if (inInput || e.metaKey || e.ctrlKey || e.altKey) return;

        if (e.key >= "0" && e.key <= "9") {{
          const num = Number(e.key);
          if (num === 0) {{
            selectedSection = "";
          }} else {{
            const sec = DATA.sections.find(s => s.number === num);
            if (sec) selectedSection = (selectedSection === sec.id) ? "" : sec.id;
          }}
          populateSubsections(selectedSection);
          subsectionSelect.value = "";
          applyFilters();
          return;
        }}

        if (e.key === "j" || e.key === "k") {{
          const rows = catalogContainer.querySelectorAll(".entry-row");
          if (!rows.length) return;
          e.preventDefault();
          if (kbFocusIdx >= 0 && kbFocusIdx < rows.length) {{
            rows[kbFocusIdx].classList.remove("kb-focus");
          }}
          if (e.key === "j") {{
            kbFocusIdx = Math.min(rows.length - 1, kbFocusIdx + 1);
          }} else {{
            kbFocusIdx = Math.max(0, kbFocusIdx <= 0 ? 0 : kbFocusIdx - 1);
          }}
          const target = rows[kbFocusIdx];
          target.classList.add("kb-focus");
          target.scrollIntoView({{ block: "nearest" }});
          return;
        }}

        if (e.key === "Enter" && kbFocusIdx >= 0) {{
          const rows = catalogContainer.querySelectorAll(".entry-row");
          const link = rows[kbFocusIdx]?.querySelector(".entry-link");
          if (link) window.open(link.href, "_blank", "noopener");
        }}
      }});

      loadStateFromUrl();
      const hasUrlFilters = Boolean(
        searchInput.value || selectedSection || subsectionSelect.value || licenseSelect.value || selectedTags.size > 0
      );
      if (hasUrlFilters) {{
        applyFilters();
      }} else {{
        // Hydrate faceted rail and tag counts without destroying SSR DOM
        updateFacetedNavigation("", "", "");
        perfReadout.textContent = `\u00b7 ${{(performance.now() - t0).toFixed(1)}}ms`;
      }}
    }})();
  </script>
</body>
</html>
"""


def build_site(
    readme_path: pathlib.Path = README_PATH,
    output_dir: pathlib.Path = DEFAULT_OUTPUT_DIR,
    examples_dir: pathlib.Path = EXAMPLES_DIR,
) -> dict[str, Any]:
    """Validate README.md and build static site, JSON API, and agent/SEO discovery files into output_dir."""
    content = readme_path.read_text(encoding="utf-8")
    errors = validate_markdown_text(content, examples_dir=examples_dir)
    if errors:
        msg = "; ".join(str(e) for e in errors)
        raise ValueError(f"Cannot build site from invalid README.md: {msg}")

    catalog = parse_catalog_data(content, examples_dir=examples_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    assets_out = output_dir / "assets"
    assets_out.mkdir(parents=True, exist_ok=True)

    svg_src = readme_path.parent / "assets" / "compliance-lifecycle.svg"
    if svg_src.exists():
        shutil.copy2(svg_src, assets_out / "compliance-lifecycle.svg")

    if examples_dir is not None and examples_dir.exists():
        examples_out = output_dir / "examples"
        if examples_out.exists():
            shutil.rmtree(examples_out)
        shutil.copytree(examples_dir, examples_out)

    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "llms.txt").write_text(render_llms_txt(catalog), encoding="utf-8")
    (output_dir / "llms-full.txt").write_text(render_llms_full_txt(content), encoding="utf-8")
    (output_dir / "robots.txt").write_text(render_robots_txt(), encoding="utf-8")
    (output_dir / "sitemap.xml").write_text(render_sitemap_xml(catalog), encoding="utf-8")
    (output_dir / "index.html").write_text(render_html(catalog), encoding="utf-8")
    return catalog


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build awesome-compliance-as-code static site, JSON API, and llms.txt/SEO artifacts."
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for generated static files (default: _site)",
    )
    args = parser.parse_args()

    try:
        catalog = build_site(output_dir=args.output)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        f"OK: built {args.output}/ (index.html, catalog.json, llms.txt, llms-full.txt, robots.txt, sitemap.xml) "
        f"for {catalog['total_entries']} entries."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
