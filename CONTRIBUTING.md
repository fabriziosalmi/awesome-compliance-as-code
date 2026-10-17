# Contributing Guidelines

Contributions to `awesome-compliance-as-code` are welcome and enforced through automated CI checks (`scripts/validate_readme.py`, `scripts/check_links.py`, and `scripts/check_repo_health.py`). Please read these criteria before opening an issue or pull request.

## Inclusion Criteria

1. **Executable Code or Formal Specification Only (No Slide-Ware)**
   Every entry must be an executable software tool (CLI, library, policy engine, Kubernetes operator, runtime sensor), a machine-readable specification (JSON, YAML, XML, or Protobuf schema), or an open-source technical reference containing executable artifacts. Links to consultancy websites, gated PDF whitepapers, webinars, marketing landing pages, or manual spreadsheet checklists are rejected.

2. **Open Source or Open Standard Only**
   Resources must be distributed under an approved OSI open-source license, Creative Commons / Community Specification license, or public-domain dedication. Proprietary, closed-box SaaS products and source-available licenses (`BUSL-1.1`, `ELv2`, `SSPL-1.0`) are excluded.

3. **Project Maturity and Maintenance**
   - Public source repository with documented installation and quickstart instructions.
   - Active maintenance with commits within the last **540 days (18 months)**, verified automatically via `scripts/check_repo_health.py`.
   - Unarchived repository status on GitHub, GitLab, or equivalent forge.

4. **Neutral, Factual Descriptions**
   - Maximum of **two sentences** per entry, starting with an uppercase letter and ending with a period (`.`).
   - Written in third-person technical English without promotional adjectives. The validator explicitly rejects entries containing: `revolutionary`, `world-leading`, `best-in-class`, `next-generation`, `cutting-edge`, `effortless`, `effortlessly`, `seamless`, `seamlessly`, `game-changing`, `game-changer`, `ultimate`, `supercharge`, or `skyrocket`.
   - No emojis and no em dashes (`U+2014`).

## Entry Format

Every catalog entry inside `README.md` must match the following single-line syntax:

```markdown
- [Project Name](https://example.com/org/repo) - Concise technical description in one or two sentences ending with a period. `[TAG]` `License`
```

Multiple regulatory tags may precede the license tag:

```markdown
- [Syft](https://github.com/anchore/syft) - CLI tool and Go library for generating CycloneDX and SPDX Software Bills of Materials from container images and filesystems. `[EU-CRA]` `[NIS2]` `Apache-2.0`
```

### URL Hygiene Rules

- All URLs must use `https://`.
- URLs must not end with a trailing slash (`/`).
- Use the canonical repository URL (no HTTP 301/302 redirect aliases).
- Duplicate URLs and duplicate project names across the catalog are rejected.

### Allowed Regulatory Tags

Every entry must include at least one regulatory or standard tag from the controlled vocabulary below:

- `[EU-CRA]` - EU Cyber Resilience Act
- `[NIS2]` - EU NIS2 Directive
- `[DORA]` - EU Digital Operational Resilience Act
- `[EU-AI-Act]` - EU Artificial Intelligence Act
- `[GDPR]` - EU General Data Protection Regulation and technical privacy controls
- `[PCI-DSS]` - Payment Card Industry Data Security Standard (v4.0)
- `[SOC2/ISO27001]` - SOC 2 and ISO/IEC 27001 controls
- `[ISO-42001]` - ISO/IEC 42001 AI Management System controls
- `[NIST-800-53]` - NIST SP 800-53, SP 800-171, FedRAMP, and OSCAL ecosystems
- `[CIS]` - CIS Benchmarks and OS/Kubernetes/Cloud hardening baselines
- `[SLSA]` - Supply-chain Levels for Software Artifacts
- `[Multi-Framework]` - General-purpose engines, schemas, or scanners applicable across multiple regulatory frameworks

### Allowed License Identifiers

Every entry must conclude with an approved SPDX license identifier (or `Public-Domain`) wrapped in backticks:

- `Apache-2.0`, `MIT`, `MIT-0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`
- `MPL-2.0`, `EPL-2.0`, `UPL-1.0`, `CPAL-1.0`
- `GPL-2.0`, `GPL-3.0`, `AGPL-3.0`, `LGPL-2.1`, `LGPL-3.0`
- `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, `Community-Spec-1.0`, `Public-Domain`

## Alphabetical Ordering

Entries within each `###` subsection (or `##` section when no subsections exist) must be sorted strictly in case-insensitive alphabetical order by `[Project Name]`.

## Synchronized Reference Examples

Code snippets under `## Reference Implementations` in `README.md` are verified in CI to match the files in `examples/` byte-for-byte. If you update an example under `examples/`, update the corresponding code block in `README.md` and run `opa test examples/opa/ -v`.

## Local Validation Before Submitting a Pull Request

Run the local validation suite before submitting your pull request:

```bash
python3 scripts/validate_readme.py
python3 -m unittest discover -s tests -v
python3 scripts/check_links.py
```

All commands must exit with code `0`.
