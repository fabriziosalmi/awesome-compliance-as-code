# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-17

### Added

- Curated Compliance-as-Code catalog of 323 verified open-source specifications, policy engines, static IaC scanners, supply-chain verifiers, runtime eBPF/SCAP hardening tools, cloud posture engines, AI/ML governance toolkits, and pre-built policy packs across 9 engineering domains and 25 subsections.
- Regulatory-to-Code Mapping Matrix linking EU Cyber Resilience Act (CRA), NIS2, DORA, EU AI Act, GDPR, PCI-DSS v4.0, NIST SP 800-53 Rev. 5, and ISO/IEC 42001 articles to concrete engineering controls and verification artifacts.
- Closed-loop architectural diagram (`assets/compliance-lifecycle.svg`) illustrating the 4-stage Compliance-as-Code lifecycle from machine-readable schemas to continuous runtime evidence.
- Tested, synchronized reference implementations under `examples/` (OPA Rego v1 with unit tests, Kyverno ClusterPolicy YAML with keyless Sigstore verification, Steampipe SQL query, and NIST OSCAL 1.1.2 Component Definition JSON).
- Zero-dependency validation and maintenance suite (`scripts/validate_readme.py`, `scripts/check_links.py`, `scripts/check_repo_health.py`) with unit and negative break-tests (`tests/test_validator.py`).
- SHA-pinned GitHub Actions workflows (`ci.yml`, `slopless.yml`, `links.yml`, `health-check.yml`) and repository governance documents (`LICENSE` CC0-1.0, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`).

## [0.0.1] - 2026-10-17

### Added

- Initial private bootstrap, catalog verification, and GitHub Actions CI setup.
