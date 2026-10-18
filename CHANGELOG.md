# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-18

### Added

- **Catalog Expansion (`README.md`)**: Expanded catalog from 351 to **629 verified open-source Compliance-as-Code tools, specifications, and policy packs** (+278 entries) across all 9 engineering domains and 30 subsections:
  - `1. Machine-Readable Formats & Data Protocols` (57 entries: added OCSF Schema, OpenSSF Gemara, NIST Metaschema, SPIFFE Spec, OTLP Proto, OpenTelemetry Spec, OpenAPI Spec, AsyncAPI Spec, JSON Schema Spec/Store, TAXII 2.1, Croissant ML, `vers` Spec, `packageurl-go`, CISA Vulnrichment, CSAF Go Tools (`gocsaf`), Secvisogram, GitHub/PyPA/Go OSV Databases, C2PA, CoRIM, EAR, Notary Project Specs, and TUF Spec).
  - `2. Policy-as-Code (PaC) Engines & Domain Languages` (60 entries: added KCL, Crossplane, Dhall, Jsonnet, Starlark-Go, Buf CLI, `cedar-java`, `cel-rust`, Wasmtime, Z3, `cvc5`, Capsule, `cert-manager csi-driver`, Connaisseur, Pepr, OPA Envoy Plugin, Policy Reporter, Authelia, Casbin-RS, PyCasbin, jCasbin, `node-casbin`, OpenFGA CLI/Language, OAuth2 Proxy, Ory Hydra/Kratos, Pomerium, and AuthZed `zed`).
  - `3. Infrastructure-as-Code (IaC) & Static Config Auditing` (83 entries: added OpenTofu, Atlantis, Digger, Burrito, Flux Tofu Controller, Azure Bicep, Terragrunt, Terramate, TFLint AWS/Azure/GCP rulesets, Argo CD, Flux, Kustomize, Carvel `ytt`/`kbld`/`kapp`, Skopeo, `crane`, `chart-testing`, `helm-unittest`, `helm-docs`, Container Structure Test, Dive, SlimToolkit, ShellCheck, MegaLinter, Cppcheck, PMD, Find Security Bugs, MobSF, `nodejsscan`, `bundler-audit`, Secretlint, `ripsecrets`, `slopless`, and StepSecurity Harden-Runner).
  - `4. Software Supply Chain & Artifact Integrity` (134 entries: added `cyclonedx-go`, `cyclonedx-php-composer`, `cyclonedx-ruby-gem`, `cyclonedx-cocoapods`, `spdx-maven-plugin`, `spdx-gradle-plugin`, Eclipse SW360, ScanCode.io, Tejolote, `govulncheck`, OSV-SCALIBR, OSV.dev, OWASP `dep-scan`, `pip-audit`, Retire.js, `trivy-db`, Trustify, VulnerableCode, Vuls, `go-cve-dictionary`, `goval-dictionary`, `gost`, GoReleaser, JReleaser, `notation-core-go`, `oras-go`, Rekor Tiles, Sunlight, Sigstore Root Signing/Scaffolding, Armored Witness, Transparency-Dev Distributor/Formats, RSTUF CLI, TUF Conformance, Renovate, Dependabot Core, ClearlyDefined Crawler/Service, Apache SkyWalking Eyes, `addlicense`, Licensed, Conforma CLI, Konflux Build Definitions, ORT Server, OpenSSF Alpha-Omega, Tekton Chains, and OpenSSF Criticality Score).
  - `5. Host, Kernel & Runtime Hardening` (96 entries: added ClamAV, Docker Bench for Security, `linux-bench`, Serverspec, `pytest-testinfra`, Test Kitchen, Chaos Mesh, LitmusChaos, Velero, `kube-vip`, Descheduler, Network Policy API, K8sGPT, Kubeshark, Hydrophone, Fairwinds Astro/Insights Plugins, `bpfman`, Falco Libs/Plugins/Rules/Talon/Falcosidekick/Event Generator, Firecracker, gVisor, Kata Containers, Cilium Hubble, Inspektor Gadget, `oci-seccomp-bpf-hook`, Vector, Fluent Bit, OTel Collector/Contrib, Prometheus, Grafana Loki, OpenSearch, Caddy, Certbot, `acme.sh`, Boulder CA, cert-manager `trust-manager`/`approver-policy`, Headscale, Nebula, and Tornjak).
  - `6. Automated Evidence Gathering & Cloud Posture` (56 entries: added StackQL, Apache Atlas, OpenLineage, Marquez, Steampipe AWS/Azure/GCP/Kubernetes/GitHub/Terraform/Docker/Okta plugins, Steampipe GitHub Compliance and AWS Tags Mods, AWS Automated Security Helper, Azure Quick Review, CloudFox, Stratus Red Team, Chainsaw, `pySigma`, YARA-X, OSCAL Compass `compliance-to-policy` (`c2p` and `c2p-go`), Defense Unicorns UDS Core, and Zarf).
  - `7. AI/ML Compliance & Model Governance` (53 entries: added Augustus, DeepTeam, BAML, Outlines, Guidance, Instructor, Mozilla `any-guardrail`, DSPy, GuideLLM, MLCommons ModelBench, OpenInference, UK AISI Inspect Evals, OpenLLMetry, AI Explainability 360, Diffprivlib, Holistic AI, InterpretML, SHAP, OpenDP, Google Differential Privacy, Safetensors, and Sigstore Model Transparency).
  - `8. Pre-Built Policy Packs & Mappings` (61 entries: added CISA CSET, OWASP Top 10/API Security Top 10/DefectDojo/MASVS/SAMM/WSTG/secureCodeBox, MITRE ATT&CK Navigator, Azure Policy Built-in Definitions, Google Cloud Config Validator, Kubewarden Policy Monorepo, OPA Control Plane/Contrib, MITRE RHEL 9 STIG Baseline, Ansible Lockdown CIS/STIG roles for RHEL 8/9, Ubuntu 22.04/24.04, Debian 11, Amazon Linux 2, and Windows Server 2019/2022, Konstruktoid Hardening, OVHcloud Debian CIS, and Neo23x0 Auditd ruleset).
  - `9. Educational & Reference Architectures` (29 entries: added Google OSS-Fuzz, OpenSSF Memory Safety and SBOM Everywhere SIGs, AWS Control Tower AFT, AWS Landing Zone Accelerator, Google Cloud Foundation Fabric, Google Cloud PBMM Landing Zone, Microsoft Sentinel As-Code, FINOS AI Governance Framework, Stanford Foundation Model Transparency Index, MITRE ATLAS, and OWASP ML Security Top 10).
- **Validator Threshold (`scripts/validate_readme.py`)**: Raised minimum catalog entry floor from `340` to `620`.

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

[1.1.0]: https://github.com/fabriziosalmi/awesome-compliance-as-code/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/fabriziosalmi/awesome-compliance-as-code/compare/v0.0.1...v1.0.0
[0.0.1]: https://github.com/fabriziosalmi/awesome-compliance-as-code/releases/tag/v0.0.1
