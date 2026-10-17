#!/usr/bin/env python3
"""Deterministic structural and content validator for awesome-compliance-as-code."""

from __future__ import annotations

import json
import pathlib
import re
import sys
from dataclasses import dataclass

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
README_PATH = ROOT_DIR / "README.md"
EXAMPLES_DIR = ROOT_DIR / "examples"

EXPECTED_HEADER = "# Awesome Compliance-as-Code [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)"

ALLOWED_REGULATORY_TAGS = frozenset(
    {
        "[EU-CRA]",
        "[NIS2]",
        "[DORA]",
        "[EU-AI-Act]",
        "[GDPR]",
        "[PCI-DSS]",
        "[SOC2/ISO27001]",
        "[ISO-42001]",
        "[NIST-800-53]",
        "[CIS]",
        "[SLSA]",
        "[Multi-Framework]",
    }
)

ALLOWED_LICENSES = frozenset(
    {
        "Apache-2.0",
        "MIT",
        "GPL-2.0",
        "GPL-3.0",
        "AGPL-3.0",
        "LGPL-2.1",
        "LGPL-3.0",
        "MPL-2.0",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "CC0-1.0",
        "CC-BY-4.0",
        "CC-BY-SA-4.0",
        "ISC",
        "EPL-2.0",
        "UPL-1.0",
        "Public-Domain",
        "BUSL-1.1",
        "ELv2",
    }
)

BANNED_WORDS = (
    "revolutionary",
    "world-leading",
    "best-in-class",
    "next-generation",
    "cutting-edge",
    "effortless",
    "effortlessly",
    "seamless",
    "seamlessly",
    "game-changing",
    "game-changer",
    "ultimate",
    "supercharge",
    "skyrocket",
)

CATALOG_SECTION_PREFIXES = (
    "## 1. ",
    "## 2. ",
    "## 3. ",
    "## 4. ",
    "## 5. ",
    "## 6. ",
    "## 7. ",
    "## 8. ",
    "## 9. ",
)

ENTRY_REGEX = re.compile(
    r"^- \[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\) - (?P<desc>.+?)\s+(?P<tags>(?:`\[[^\]]+\]`\s+)+)`(?P<license>[^`]+)`$"
)

TAG_EXTRACT_REGEX = re.compile(r"`(\[[^\]]+\])`")
TOC_LINK_REGEX = re.compile(r"^\s*- \[(?P<title>[^\]]+)\]\(#(?P<anchor>[a-z0-9-]+)\)$")

EMOJI_REGEX = re.compile(
    "["
    "\U0001F300-\U0001F9FF"
    "\U00002600-\U000027BF"
    "\U0001FA00-\U0001FAFF"
    "]+",
    flags=re.UNICODE,
)


@dataclass(frozen=True)
class ValidationError:
    line: int
    message: str

    def __str__(self) -> str:
        if self.line > 0:
            return f"line {self.line}: {self.message}"
        return self.message


def github_slug(heading_text: str) -> str:
    """Compute GitHub Markdown anchor slug for a heading title."""
    slug = heading_text.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s", "-", slug)
    return slug


def count_sentences(text: str) -> int:
    """Count sentences in a technical description while ignoring common abbreviations."""
    normalized = re.sub(r"\b(e\.g|i\.e|vs|etc|Art|Req|Rev|SP|v\d+)\.", r"\1", text)
    parts = [segment.strip() for segment in re.split(r"\.(?:\s+|$)", normalized) if segment.strip()]
    return len(parts)


def validate_markdown_text(
    content: str,
    *,
    examples_dir: pathlib.Path | None = EXAMPLES_DIR,
    min_entries: int = 300,
) -> list[ValidationError]:
    """Validate README.md content and return a list of structural or policy errors."""
    errors: list[ValidationError] = []
    lines = content.splitlines()

    if not lines or lines[0].strip() != EXPECTED_HEADER:
        errors.append(
            ValidationError(1, f"first line must match Awesome header '{EXPECTED_HEADER}'")
        )

    for idx, line in enumerate(lines, start=1):
        if "\u2014" in line:
            errors.append(ValidationError(idx, "em dash (U+2014) is not allowed; use a hyphen or colon"))
        if EMOJI_REGEX.search(line):
            errors.append(ValidationError(idx, "emojis are not allowed in repository documentation"))

    current_h2: str | None = None
    current_group: str | None = None
    in_catalog_section = False
    in_toc_section = False
    in_code_block = False

    h2_sections_seen: set[str] = set()
    group_entry_names: dict[str, list[tuple[int, str]]] = {}
    toc_anchors: list[tuple[int, str, str]] = []
    actual_headings: dict[str, str] = {}
    seen_urls: dict[str, int] = {}
    seen_names: dict[str, int] = {}
    total_entries = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if line.startswith("## "):
            heading_title = line[3:].strip()
            actual_headings[github_slug(heading_title)] = heading_title
            current_h2 = line.strip()
            in_toc_section = current_h2 == "## Contents"
            in_catalog_section = any(current_h2.startswith(prefix) for prefix in CATALOG_SECTION_PREFIXES)
            if in_catalog_section:
                h2_sections_seen.add(current_h2)
                current_group = current_h2
                group_entry_names.setdefault(current_group, [])
            else:
                current_group = None
            continue

        if line.startswith("### "):
            heading_title = line[4:].strip()
            actual_headings[github_slug(heading_title)] = heading_title
            if in_catalog_section and current_h2 is not None:
                current_group = f"{current_h2} > {line.strip()}"
                group_entry_names.setdefault(current_group, [])
            continue

        if in_toc_section and stripped.startswith("- ["):
            toc_match = TOC_LINK_REGEX.match(line)
            if not toc_match:
                errors.append(ValidationError(idx, f"invalid Table of Contents line: '{line}'"))
            else:
                toc_anchors.append((idx, toc_match.group("title"), toc_match.group("anchor")))
            continue

        if not in_catalog_section or not line.startswith("- "):
            continue

        match = ENTRY_REGEX.match(line)
        if not match:
            errors.append(
                ValidationError(
                    idx,
                    "invalid catalog entry format; expected '- [Name](https://...) - Description. `[TAG]` `License`'",
                )
            )
            continue

        total_entries += 1
        name = match.group("name").strip()
        url = match.group("url").strip()
        desc = match.group("desc").strip()
        tags_raw = match.group("tags")
        license_id = match.group("license").strip()

        if not url.startswith("https://"):
            errors.append(ValidationError(idx, f"URL for '{name}' must use https:// (got '{url}')"))

        if url.endswith("/"):
            errors.append(
                ValidationError(idx, f"URL for '{name}' must not have a trailing slash ('{url}')")
            )

        normalized_url = url.rstrip("/").lower()
        if normalized_url in seen_urls:
            first_line = seen_urls[normalized_url]
            errors.append(
                ValidationError(idx, f"duplicate URL '{url}' for '{name}' (already listed on line {first_line})")
            )
        else:
            seen_urls[normalized_url] = idx

        normalized_name = name.casefold()
        if normalized_name in seen_names:
            first_line = seen_names[normalized_name]
            errors.append(
                ValidationError(idx, f"duplicate project name '{name}' (already listed on line {first_line})")
            )
        else:
            seen_names[normalized_name] = idx

        if not desc[0].isupper() and not desc[0].isdigit():
            errors.append(
                ValidationError(idx, f"description for '{name}' must start with an uppercase letter")
            )

        if not desc.endswith("."):
            errors.append(ValidationError(idx, f"description for '{name}' must end with a period"))

        sentence_count = count_sentences(desc)
        if sentence_count > 2:
            errors.append(
                ValidationError(
                    idx,
                    f"description for '{name}' exceeds maximum of 2 sentences (counted {sentence_count})",
                )
            )

        lower_desc = desc.lower()
        for word in BANNED_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", lower_desc):
                errors.append(
                    ValidationError(idx, f"description for '{name}' contains promotional word '{word}'")
                )

        tags = TAG_EXTRACT_REGEX.findall(tags_raw)
        if not tags:
            errors.append(ValidationError(idx, f"entry '{name}' must include at least one regulatory tag"))
        for tag in tags:
            if tag not in ALLOWED_REGULATORY_TAGS:
                errors.append(
                    ValidationError(
                        idx,
                        f"entry '{name}' uses unknown regulatory tag '{tag}'; allowed: {sorted(ALLOWED_REGULATORY_TAGS)}",
                    )
                )

        if license_id not in ALLOWED_LICENSES:
            errors.append(
                ValidationError(
                    idx,
                    f"entry '{name}' uses unapproved or malformed license identifier '{license_id}'",
                )
            )

        assert current_group is not None
        group_entry_names[current_group].append((idx, name))

    for toc_line, toc_title, toc_anchor in toc_anchors:
        if toc_anchor not in actual_headings:
            errors.append(
                ValidationError(
                    toc_line,
                    f"TOC anchor '#{toc_anchor}' for '{toc_title}' does not match any heading slug",
                )
            )

    for prefix in CATALOG_SECTION_PREFIXES:
        matching = [sec for sec in h2_sections_seen if sec.startswith(prefix)]
        if not matching:
            errors.append(ValidationError(0, f"missing required catalog section starting with '{prefix}'"))

    for group, entries in group_entry_names.items():
        if not entries:
            if " > ### " in group or not any(k.startswith(f"{group} > ### ") for k in group_entry_names):
                errors.append(ValidationError(0, f"catalog group '{group}' contains no entries"))
            continue
        for i in range(1, len(entries)):
            prev_line, prev_name = entries[i - 1]
            curr_line, curr_name = entries[i]
            if prev_name.casefold() > curr_name.casefold():
                errors.append(
                    ValidationError(
                        curr_line,
                        f"alphabetical order violation in '{group}': '{curr_name}' must appear before '{prev_name}' (line {prev_line})",
                    )
                )

    if total_entries < min_entries:
        errors.append(
            ValidationError(
                0,
                f"catalog contains {total_entries} entries, which is below the minimum threshold of {min_entries}",
            )
        )

    if examples_dir is not None and examples_dir.exists():
        expected_files = [
            examples_dir / "opa" / "cra_workloads.rego",
            examples_dir / "kyverno" / "dora_signed_images.yaml",
            examples_dir / "steampipe" / "dora_s3_encryption.sql",
            examples_dir / "oscal" / "cra_component_definition.json",
        ]
        for ex_file in expected_files:
            if not ex_file.exists():
                errors.append(ValidationError(0, f"missing reference example file: {ex_file.relative_to(ROOT_DIR)}"))
                continue
            snippet = ex_file.read_text(encoding="utf-8").strip()
            if snippet not in content:
                errors.append(
                    ValidationError(
                        0,
                        f"reference example '{ex_file.relative_to(ROOT_DIR)}' is out of sync with README.md code block",
                    )
                )
            if ex_file.suffix == ".json":
                try:
                    parsed = json.loads(snippet)
                    if "component-definition" not in parsed:
                        errors.append(
                            ValidationError(0, f"OSCAL JSON '{ex_file.name}' missing top-level 'component-definition'")
                        )
                except json.JSONDecodeError as exc:
                    errors.append(ValidationError(0, f"invalid JSON in '{ex_file.name}': {exc}"))

        svg_path = ROOT_DIR / "assets" / "compliance-lifecycle.svg"
        if not svg_path.exists():
            errors.append(ValidationError(0, "missing architectural diagram: assets/compliance-lifecycle.svg"))
        else:
            import xml.etree.ElementTree as ET

            try:
                ET.fromstring(svg_path.read_text(encoding="utf-8"))
            except ET.ParseError as exc:
                errors.append(ValidationError(0, f"invalid XML in assets/compliance-lifecycle.svg: {exc}"))
            if "assets/compliance-lifecycle.svg" not in content:
                errors.append(ValidationError(0, "README.md must embed assets/compliance-lifecycle.svg"))

    return errors


def main() -> int:
    if not README_PATH.exists():
        print(f"ERROR: {README_PATH} does not exist", file=sys.stderr)
        return 1

    content = README_PATH.read_text(encoding="utf-8")
    errors = validate_markdown_text(content)
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    entry_count = sum(1 for line in content.splitlines() if ENTRY_REGEX.match(line))
    print(f"OK: README.md validated cleanly ({entry_count} catalog entries, 9 sections, examples synchronized).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
