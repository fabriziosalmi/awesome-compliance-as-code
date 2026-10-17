# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial repository structure, governance documents (`LICENSE` CC0-1.0, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`), and GitHub Issue/PR templates.
- Reference Compliance-as-Code policy examples in `examples/` (OPA Rego v1, Kyverno ClusterPolicy, Steampipe SQL, NIST OSCAL Component Definition).
- Automated README and example validator (`scripts/validate_readme.py`) with unit test suite (`tests/test_validator.py`).
- Curated catalog across 8 Compliance-as-Code engineering domains plus Regulatory-to-Code mapping matrix in `README.md`.
- GitHub Actions CI workflows for structural validation, policy testing, link verification, repository health monitoring, and static analysis.
