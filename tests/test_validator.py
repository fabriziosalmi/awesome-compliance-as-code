"""Unit and break tests for scripts/validate_readme.py."""

from __future__ import annotations

import unittest

from scripts.validate_readme import (
    CATALOG_SECTION_PREFIXES,
    EXPECTED_HEADER,
    README_PATH,
    validate_markdown_text,
)


def _build_minimal_valid_readme() -> str:
    sections = []
    for idx, prefix in enumerate(CATALOG_SECTION_PREFIXES, start=1):
        sections.append(
            f"{prefix}Section {idx}\n\n"
            f"- [Alpha Tool {idx}](https://example.com/alpha-{idx}) - Static verifier for control {idx}. `[EU-CRA]` `Apache-2.0`\n"
            f"- [Beta Tool {idx}](https://example.com/beta-{idx}) - Runtime policy engine for control {idx}. `[NIS2]` `MIT`\n"
        )
    return f"{EXPECTED_HEADER}\n\n" + "\n".join(sections)


class ValidatorTestSuite(unittest.TestCase):
    def test_minimal_valid_catalog_passes(self) -> None:
        md = _build_minimal_valid_readme()
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertEqual(errors, [])

    def test_break_alphabetical_order_fails(self) -> None:
        md = _build_minimal_valid_readme().replace(
            "- [Alpha Tool 1](https://example.com/alpha-1) - Static verifier for control 1. `[EU-CRA]` `Apache-2.0`\n"
            "- [Beta Tool 1](https://example.com/beta-1) - Runtime policy engine for control 1. `[NIS2]` `MIT`",
            "- [Zulu Tool 1](https://example.com/zulu-1) - Static verifier for control 1. `[EU-CRA]` `Apache-2.0`\n"
            "- [Alpha Tool 1](https://example.com/alpha-1) - Runtime policy engine for control 1. `[NIS2]` `MIT`",
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("alphabetical order violation" in e.message for e in errors))

    def test_break_non_https_url_fails(self) -> None:
        md = _build_minimal_valid_readme().replace(
            "https://example.com/alpha-1",
            "http://example.com/alpha-1",
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("must use https://" in e.message for e in errors))

    def test_break_trailing_slash_url_fails(self) -> None:
        md = _build_minimal_valid_readme().replace(
            "https://example.com/alpha-1",
            "https://example.com/alpha-1/",
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("trailing slash" in e.message for e in errors))

    def test_break_duplicate_url_fails(self) -> None:
        md = _build_minimal_valid_readme().replace(
            "https://example.com/beta-1",
            "https://example.com/alpha-1",
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("duplicate URL" in e.message for e in errors))

    def test_break_broken_toc_anchor_fails(self) -> None:
        md = (
            f"{EXPECTED_HEADER}\n\n"
            "## Contents\n\n"
            "- [1. Section 1](#non-existent-anchor)\n\n"
            + _build_minimal_valid_readme().split("\n\n", 1)[1]
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("does not match any heading slug" in e.message for e in errors))

    def test_break_unknown_regulatory_tag_fails(self) -> None:
        md = _build_minimal_valid_readme().replace("[EU-CRA]", "[FAKE-LAW-99]", 1)
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("unknown regulatory tag" in e.message for e in errors))

    def test_break_promotional_word_fails(self) -> None:
        md = _build_minimal_valid_readme().replace(
            "Static verifier for control 1.",
            "A revolutionary verifier for control 1.",
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("promotional word 'revolutionary'" in e.message for e in errors))

    def test_break_more_than_two_sentences_fails(self) -> None:
        md = _build_minimal_valid_readme().replace(
            "Static verifier for control 1.",
            "First sentence here. Second sentence here. Third sentence is forbidden.",
        )
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("exceeds maximum of 2 sentences" in e.message for e in errors))

    def test_break_em_dash_fails(self) -> None:
        md = _build_minimal_valid_readme() + "\nThis line has an em dash \u2014 which is banned.\n"
        errors = validate_markdown_text(md, examples_dir=None, min_entries=18)
        self.assertTrue(any("em dash" in e.message for e in errors))

    def test_real_repository_readme_passes(self) -> None:
        self.assertTrue(README_PATH.exists(), "README.md must exist at repository root")
        content = README_PATH.read_text(encoding="utf-8")
        errors = validate_markdown_text(content)
        self.assertEqual(errors, [], f"README.md validation failed: {[str(e) for e in errors]}")


if __name__ == "__main__":
    unittest.main()
