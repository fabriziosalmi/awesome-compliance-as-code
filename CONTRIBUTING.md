# Contributing Guidelines

Contributions to `awesome-compliance-as-code` are welcome and enforced through automated CI checks (`scripts/validate_readme.py`). Please read these criteria before opening an issue or pull request.

## Inclusion Criteria

1. **Executable Code or Formal Specification Only (No Slide-Ware)**
   Every entry must be an executable software tool (CLI, library, policy engine, Kubernetes operator, agent), a machine-readable specification (JSON/YAML/XML schema), or an open-source technical reference with executable artifacts. Links to consultancy websites, gated PDF whitepapers, webinars, marketing landing pages, or manual spreadsheet checklists are rejected.

2. **Open Source or Verifiably Self-Hostable**
   Tools must be distributed under an OSI-approved open-source license (`Apache-2.0`, `MIT`, `GPL-3.0`, `MPL-2.0`, `BSD-3-Clause`, `CC0-1.0`, `Public-Domain`) or a source-available license with a fully functional, free, self-hostable CLI or community edition. Closed-box SaaS products whose primary call to action is "Book a Demo" are excluded.

3. **Project Maturity and Maintenance**
   - Public source repository with documented installation and quickstart instructions.
   - Active maintenance (commits within the last 180 days for tools, or active working group status for formal specifications).
   - Unarchived repository status on GitHub, GitLab, or equivalent forge.

4. **Neutral, Factual Descriptions**
   - Maximum of two sentences per entry.
   - Written in third-person technical English without promotional adjectives ("revolutionary", "world-leading", "best-in-class", "next-generation", "effortless", "seamless").
   - No emojis and no em dashes.

## Entry Format

Every catalog entry inside `README.md` must match the following syntax:

```markdown
- [Project Name](https://example.com) - Concise technical description in one or two sentences ending with a period. `[TAG]` `License`
```

Multiple regulatory tags may precede the license tag:

```markdown
- [Syft](https://github.com/anchore/syft) - CLI tool and Go library for generating Software Bills of Materials (SBOM) from container images and filesystems in CycloneDX and SPDX formats. `[EU-CRA]` `[NIS2]` `Apache-2.0`
```

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

## Alphabetical Ordering

Entries within each `###` or `##` catalog section must be sorted strictly in case-insensitive alphabetical order by `[Project Name]`.

## Local Validation Before Submitting a Pull Request

Run the local validation suite before submitting your pull request:

```bash
python3 scripts/validate_readme.py
python3 -m unittest discover -s tests -v
```

Both commands must exit with code `0`.
