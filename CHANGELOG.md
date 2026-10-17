# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-17

### Added

- **Catalog (`README.md`)**: 351 verified open-source Compliance-as-Code tools, formal specifications, and policy packs organized across 9 engineering domains and 27 subsections:
  - `1. Machine-Readable Formats & Data Protocols` (30 entries across Control Schemas, SBOM/CBOM/SaaSBOM, Vulnerability/VEX/Advisory Formats, and Provenance Specifications).
  - `2. Policy-as-Code (PaC) Engines & Domain Languages` (30 entries across General-Purpose Engines, Kubernetes Admission Controllers, and Fine-Grained Authorization Engines).
  - `3. Infrastructure-as-Code (IaC) & Static Config Auditing` (46 entries across Multi-Cloud/Terraform Scanners, Kubernetes/Container Linters, and Source/Secrets/Privacy Static Analyzers).
  - `4. Software Supply Chain & Artifact Integrity` (83 entries across SBOM/CBOM Generation, Vulnerability/VEX Correlation, Cryptographic Signing/Transparency Logs, License Governance, and Supply-Chain Graph Aggregators).
  - `5. Host, Kernel & Runtime Hardening` (50 entries across SCAP/CIS/STIG Auditing, Kubernetes Node Benchmarks, eBPF Runtime Enforcement, and Fleet Telemetry/Cryptography/Log Integrity).
  - `6. Automated Evidence Gathering & Cloud Posture` (31 entries across SQL-Over-Infrastructure Engines, Continuous CSPM/Drift Scanners, and OSCAL Evidence Frameworks).
  - `7. AI/ML Compliance & Model Governance` (31 entries across LLM Red-Teaming/Guardrails, RAG Faithfulness/Benchmark Evaluation, and Fairness/Differential Privacy/Artifact Integrity).
  - `8. Pre-Built Policy Packs & Mappings` (33 entries across Machine-Readable Control Catalogs, Kubernetes/OPA/Kyverno Policy Libraries, and Host/Edge/Cloud Hardening Baselines).
  - `9. Educational & Reference Architectures` (17 entries across Supply-Chain Security Frameworks and Cloud/GitOps/AI Governance Blueprints).
- **Regulatory-to-Code Mapping Matrix**: Cross-reference table mapping statutory articles from the EU Cyber Resilience Act (CRA), EU NIS2 Directive, EU DORA, EU AI Act, GDPR, PCI-DSS v4.0, NIST SP 800-53 Rev. 5, and ISO/IEC 42001 to engineering controls and verification artifacts.
- **Closed-Loop Architecture Diagram (`assets/compliance-lifecycle.svg`)**: Responsive vector diagram illustrating the 4-stage Compliance-as-Code control loop and continuous OSCAL/VEX evidence feedback.
- **Executable Reference Implementations (`examples/`)**:
  - `examples/opa/cra_workloads.rego` and `examples/opa/cra_workloads_test.rego` (OPA Rego v1 policy and unit test suite).
  - `examples/kyverno/dora_signed_images.yaml` (Kyverno `ClusterPolicy` enforcing keyless Sigstore verification and non-privileged execution).
  - `examples/steampipe/dora_s3_encryption.sql` (Steampipe SQL audit query for storage encryption at rest).
  - `examples/oscal/cra_component_definition.json` (NIST OSCAL 1.1.2 Component Definition mapping `AC-6` to OPA policy evaluation).
- **Deterministic Validation & CI Suite (`scripts/`, `tests/`, `.github/workflows/`)**:
  - `scripts/validate_readme.py` and `tests/test_validator.py`: zero-dependency structural validator and break-test suite enforcing `awesome` formatting, TOC anchor slugs, alphabetical ordering per subsection, regulatory/license tags, and byte-level synchronization with `examples/`.
  - `scripts/check_links.py` and `.github/workflows/links.yml`: concurrent HTTPS reachability verifier.
  - `scripts/check_repo_health.py` and `.github/workflows/health-check.yml`: GitHub API monitor detecting archived repositories, canonical slug renames, SPDX license drift, or inactivity exceeding 540 days.
  - `.github/workflows/ci.yml` and `.github/workflows/slopless.yml`: SHA-pinned workflows running catalog validation, OPA Rego tests, and static analysis.

## [0.0.1] - 2026-10-17

### Added

- Initial private repository bootstrap, governance files (`LICENSE` CC0-1.0, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`), and CI workflow setup.

[1.0.0]: https://github.com/fabriziosalmi/awesome-compliance-as-code/compare/v0.0.1...v1.0.0
[0.0.1]: https://github.com/fabriziosalmi/awesome-compliance-as-code/releases/tag/v0.0.1
