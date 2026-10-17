# Roadmap

This document tracks the engineering milestones for `awesome-compliance-as-code`, from local structural validation to public release and continuous maintenance.

## Milestone 1: Local Foundation and Deterministic Validation (Done)

- [x] Initialize repository structure (`LICENSE` under CC0-1.0, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`, `.gitattributes`, `.github/CODEOWNERS`).
- [x] Define GitHub Issue Forms (`.github/ISSUE_TEMPLATE/submit-tool.yml`, `.github/ISSUE_TEMPLATE/submit-policy-pack.yml`) and Pull Request template (`.github/PULL_REQUEST_TEMPLATE.md`).
- [x] Create tested, executable Compliance-as-Code reference examples under `examples/` (OPA Rego v1 with unit tests, Kyverno ClusterPolicy YAML, Steampipe SQL, NIST OSCAL component definition JSON).
- [x] Build a zero-dependency Python structural validator (`scripts/validate_readme.py`), HTTP link verifier (`scripts/check_links.py`), GitHub API freshness monitor (`scripts/check_repo_health.py`), and unit/break-test suite (`tests/test_validator.py`).

## Milestone 2: Scoped Catalog Expansion and Regulatory-to-Code Matrix (Done)

- [x] Populate 9 core engineering sections and 25 scoped subsections with **224 verified open-source tools, specifications, and policy packs**.
- [x] Verify all 224 GitHub repositories via the GitHub API (`0` archived, `0` inactive > 540 days, `0` HTTP 404/broken links across all 228 URLs) and confirm exact SPDX license identifiers.
- [x] Build the Regulatory-to-Code Mapping Matrix covering EU Cyber Resilience Act (CRA), NIS2, DORA, EU AI Act, GDPR, PCI-DSS v4.0, NIST SP 800-53 Rev. 5, and ISO/IEC 42001.
- [x] Pass all 11 unit/break tests and all 36 `lgit check .` project-hygiene gates with `0` findings.

## Milestone 3: Private GitHub Repository and Atomic CI (`v0.0.1`)

- [ ] Create private repository `fabriziosalmi/awesome-compliance-as-code` and push `main`.
- [ ] Verify SHA-pinned GitHub Actions workflows on GitHub runners:
  - `ci.yml`: structural validator, unit tests, `examples/` syntax and policy tests (`opa check --strict`, `opa test`), and JSON/YAML validation.
  - `slopless.yml`: static analysis against AI-slop patterns on Markdown and Python files.
  - `links.yml`: scheduled and PR-triggered link verification.
  - `health-check.yml`: quarterly repository freshness and archive monitor via GitHub API.
- [ ] Confirm 100% green CI and tag `v0.0.1`.

## Milestone 4: Visual Assets and Pre-Launch Polish (`v0.1.0`)

- [ ] Add architectural SVG diagram (`assets/compliance-lifecycle.svg`) illustrating the Compliance-as-Code control loop from specification to runtime attestation.
- [ ] Final review of descriptions, regulatory tags, and Table of Contents anchors.

## Milestone 5: Final Audit and Public Launch (`v1.0.0`)

- [ ] Run end-to-end audit (`validate_readme.py`, `unittest`, `lgit`, `slopless`, live HTTP link check).
- [ ] Switch repository visibility to public, configure repository metadata and topics, and cut release `v1.0.0`.
