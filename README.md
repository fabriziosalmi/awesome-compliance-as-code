# Awesome Compliance-as-Code [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of open-source Compliance-as-Code (CaC) specifications, policy engines, supply-chain verifiers, runtime auditors, and regulatory-to-code mappings for automating technical compliance across CI/CD pipelines and production infrastructure.

Compliance-as-Code translates statutory regulations, security baselines, and industry standards into machine-readable specifications, declarative policies, and automated verification gates. If a requirement cannot be validated via CLI, queried via API, or enforced in a deployment pipeline, it does not belong in this catalog.

## Contents

- [1. Machine-Readable Formats & Data Protocols](#1-machine-readable-formats--data-protocols)
  - [Control & Assessment Schemas](#control--assessment-schemas)
  - [Software Bill of Materials (SBOM, CBOM, SaaSBOM, HBOM)](#software-bill-of-materials-sbom-cbom-saasbom-hbom)
  - [Vulnerability, Advisory & Exploitability Formats](#vulnerability-advisory--exploitability-formats)
  - [Provenance & Attestation Specifications](#provenance--attestation-specifications)
- [2. Policy-as-Code (PaC) Engines & Domain Languages](#2-policy-as-code-pac-engines--domain-languages)
  - [General-Purpose Policy & Constraint Engines](#general-purpose-policy--constraint-engines)
  - [Kubernetes Admission & Policy Controllers](#kubernetes-admission--policy-controllers)
  - [Fine-Grained Authorization & Access Control Engines](#fine-grained-authorization--access-control-engines)
- [3. Infrastructure-as-Code (IaC) & Static Config Auditing](#3-infrastructure-as-code-iac--static-config-auditing)
  - [Multi-Cloud & Terraform Scanners](#multi-cloud--terraform-scanners)
  - [Kubernetes Manifest, Helm & Container Linters](#kubernetes-manifest-helm--container-linters)
  - [Source Code, Secrets & Privacy Static Analyzers](#source-code-secrets--privacy-static-analyzers)
- [4. Software Supply Chain & Artifact Integrity](#4-software-supply-chain--artifact-integrity)
  - [SBOM Generation & Manipulation](#sbom-generation--manipulation)
  - [Vulnerability Correlation & VEX Tooling](#vulnerability-correlation--vex-tooling)
  - [Cryptographic Signing, Provenance & Transparency Logs](#cryptographic-signing-provenance--transparency-logs)
  - [License Compliance & Dependency Governance](#license-compliance--dependency-governance)
  - [Supply-Chain Graph & Policy Aggregators](#supply-chain-graph--policy-aggregators)
- [5. Host, Kernel & Runtime Hardening](#5-host-kernel--runtime-hardening)
  - [SCAP, CIS & STIG Host Auditing](#scap-cis--stig-host-auditing)
  - [Kubernetes Node & Cluster Runtime Benchmarks](#kubernetes-node--cluster-runtime-benchmarks)
  - [eBPF & Kernel Runtime Policy Enforcement](#ebpf--kernel-runtime-policy-enforcement)
  - [Fleet Telemetry, Cryptography & Log Integrity](#fleet-telemetry-cryptography--log-integrity)
- [6. Automated Evidence Gathering & Cloud Posture](#6-automated-evidence-gathering--cloud-posture)
  - [SQL-Over-Infrastructure & Asset Graph Engines](#sql-over-infrastructure--asset-graph-engines)
  - [Continuous Cloud Security Posture & Drift Engines](#continuous-cloud-security-posture--drift-engines)
  - [OSCAL Automation & Evidence-as-Code Frameworks](#oscal-automation--evidence-as-code-frameworks)
- [7. AI/ML Compliance & Model Governance](#7-aiml-compliance--model-governance)
  - [LLM Red-Teaming, Guardrails & Safety Gates](#llm-red-teaming-guardrails--safety-gates)
  - [RAG Faithfulness, Hallucination & Benchmark Evaluation](#rag-faithfulness-hallucination--benchmark-evaluation)
  - [Algorithmic Fairness, Differential Privacy & Artifact Integrity](#algorithmic-fairness-differential-privacy--artifact-integrity)
- [8. Pre-Built Policy Packs & Mappings](#8-pre-built-policy-packs--mappings)
  - [Machine-Readable Control Catalogs & Requirements](#machine-readable-control-catalogs--requirements)
  - [Kubernetes, OPA & Kyverno Policy Libraries](#kubernetes-opa--kyverno-policy-libraries)
  - [Host, Edge & Cloud Hardening Baselines](#host-edge--cloud-hardening-baselines)
- [9. Educational & Reference Architectures](#9-educational--reference-architectures)
- [Regulatory-to-Code Mapping Matrix](#regulatory-to-code-mapping-matrix)
- [Reference Implementations](#reference-implementations)
- [Contributing](#contributing)
- [License](#license)

## 1. Machine-Readable Formats & Data Protocols

Serializable schemas (JSON, YAML, XML, Protobuf) that replace ambiguous natural-language compliance requirements with deterministic data structures.

### Control & Assessment Schemas

- [Common Cloud Controls (FINOS CCC)](https://github.com/finos/common-cloud-controls) - Open standard maintained by FINOS describing consistent cyber, operational, and resiliency controls for financial-sector cloud deployments. `[DORA]` `[SOC2/ISO27001]` `CC-BY-4.0`
- [NIST OSCAL (Open Security Controls Assessment Language)](https://github.com/usnistgov/OSCAL) - Standardized XML, JSON, and YAML schemas developed by NIST for expressing control catalogs, baselines, System Security Plans (SSP), and assessment results. `[NIST-800-53]` `[Multi-Framework]` `Public-Domain`
- [OCI Image Specification](https://github.com/opencontainers/image-spec) - Open Container Initiative schema defining interoperable container image manifests, filesystem layers, and cryptographic configuration annotations. `[EU-CRA]` `[CIS]` `Apache-2.0`
- [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec) - Open Container Initiative specification governing container execution state, Linux namespaces, cgroups, and seccomp security boundaries. `[CIS]` `[NIS2]` `Apache-2.0`

### Software Bill of Materials (SBOM, CBOM, SaaSBOM, HBOM)

- [CycloneDX Specification](https://github.com/CycloneDX/specification) - OWASP standard for Software, Hardware, Cryptography, and SaaS Bills of Materials (SBOM, HBOM, CBOM, SaaSBOM) with formal vulnerability and compliance attestations. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [OmniBOR Specification](https://github.com/omnibor/spec) - Minimalist artifact identity specification constructing reproducible content-addressable dependency graphs across software build trees. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Package URL (purl) Specification](https://github.com/package-url/purl-spec) - Universal, URI-based identifier standard for referencing software packages reliably across package managers, SBOM formats, and vulnerability databases. `[EU-CRA]` `[Multi-Framework]` `MIT`
- [SPDX (Software Package Data Exchange)](https://github.com/spdx/spdx-spec) - ISO/IEC 5962:2021 open standard for communicating software bill of materials components, licenses, copyrights, and security references. `[EU-CRA]` `[NIS2]` `CC-BY-4.0`

### Vulnerability, Advisory & Exploitability Formats

- [CSAF (Common Security Advisory Framework)](https://github.com/oasis-tcs/csaf) - OASIS standard for publishing and consuming machine-readable security advisories and vulnerability disclosures across software supply chains. `[EU-CRA]` `[NIS2]` `BSD-3-Clause`
- [CVE JSON Record Format Schema](https://github.com/CVEProject/cve-schema) - Official JSON Schema specification for Common Vulnerabilities and Exposures (CVE) v5 records, CVSS vectors, and CWE problem types. `[EU-CRA]` `[NIS2]` `CC0-1.0`
- [OpenVEX](https://github.com/openvex/spec) - Minimal, interoperable Vulnerability Exploitability eXchange specification for attesting whether a vulnerability listed in an SBOM is exploitable in practice. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [OSV Schema (Open Source Vulnerability)](https://github.com/ossf/osv-schema) - OpenSSF JSON schema for describing vulnerabilities precisely across open-source ecosystems and commit ranges. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [SARIF (Static Analysis Results Interchange Format)](https://github.com/oasis-tcs/sarif-spec) - OASIS JSON standard unifying the output of static analysis and compliance scanners across CI/CD systems. `[Multi-Framework]` `BSD-3-Clause`

### Provenance & Attestation Specifications

- [DSSE (Dead Simple Signing Envelope)](https://github.com/secure-systems-lab/dsse) - Cryptographic signature envelope specification designed to sign arbitrary supply-chain metadata and in-toto predicates without canonicalization bugs. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [IETF SCITT Architecture](https://github.com/ietf-wg-scitt/draft-ietf-scitt-architecture) - IETF Supply Chain Integrity, Transparency, and Trust working group specification for append-only transparency services and signed receipts. `[EU-CRA]` `[SLSA]` `BSD-2-Clause`
- [in-toto Attestation Framework](https://github.com/in-toto/attestation) - Vendor-neutral specifications and schemas for cryptographically verifiable software supply-chain step metadata and predicates. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [SLSA (Supply-chain Levels for Software Artifacts)](https://github.com/slsa-framework/slsa) - Security framework and provenance specification defining verifiable build integrity levels for software artifacts. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [Uptane Standard](https://github.com/uptane/uptane-standard) - Compromise-resilient software update security framework designed for automotive, embedded, and IoT systems subject to statutory safety rules. `[EU-CRA]` `[NIS2]` `Apache-2.0`

## 2. Policy-as-Code (PaC) Engines & Domain Languages

Evaluation engines that process structured inputs (ASTs, JSON, admission requests, infrastructure plans) and emit deterministic allow/deny decisions.

### General-Purpose Policy & Constraint Engines

- [Cedar](https://github.com/cedar-policy/cedar) - Formally verified policy language and evaluation engine developed for fine-grained permissions and automated mathematical reasoning over authorization policies. `[NIST-800-53]` `[SOC2/ISO27001]` `Apache-2.0`
- [CEL (Common Expression Language) Spec](https://github.com/cel-expr/cel-spec) - Non-Turing-complete expression language specification designed for fast, safe, embedded policy evaluation inside Kubernetes and RPC gateways. `[Multi-Framework]` `Apache-2.0`
- [cel-go](https://github.com/cel-expr/cel-go) - Reference Go implementation of the Common Expression Language for evaluating linear-time compliance and admission expressions. `[Multi-Framework]` `Apache-2.0`
- [CUE](https://github.com/cue-lang/cue) - Strongly typed constraint and data validation language based on lattice logic for unifying schemas, configurations, and compliance rules. `[Multi-Framework]` `Apache-2.0`
- [Nickel](https://github.com/nickel-lang/nickel) - Configuration and policy language with gradual typing and contract verification for generating validated infrastructure manifests. `[Multi-Framework]` `MIT`
- [Open Policy Agent (OPA)](https://github.com/open-policy-agent/opa) - General-purpose policy engine using the declarative Rego language to decouple policy evaluation from application and infrastructure services. `[Multi-Framework]` `Apache-2.0`
- [Pkl](https://github.com/apple/pkl) - Configuration-as-code language with rich type and constraint validation capable of rendering verified JSON, YAML, XML, and property files. `[Multi-Framework]` `Apache-2.0`
- [Regal](https://github.com/open-policy-agent/regal) - Linter and language server for Open Policy Agent Rego policies that enforces correctness, performance, and style rules across policy repositories. `[Multi-Framework]` `Apache-2.0`
- [Regorus](https://github.com/microsoft/regorus) - Fast, lightweight Rust implementation of the Open Policy Agent Rego evaluation engine suitable for embedded and WebAssembly environments. `[Multi-Framework]` `MIT`

### Kubernetes Admission & Policy Controllers

- [Chainsaw](https://github.com/kyverno/chainsaw) - Declarative end-to-end testing tool for Kubernetes operators and admission controllers to verify that compliance policies reject non-conformant workloads. `[NIS2]` `[DORA]` `Apache-2.0`
- [Gatekeeper (OPA)](https://github.com/open-policy-agent/gatekeeper) - Customizable Kubernetes admission webhook and audit controller that enforces CRD-based OPA policies across clusters. `[NIS2]` `[DORA]` `Apache-2.0`
- [Kubewarden Admission Controller](https://github.com/kubewarden/adm-controller) - Kubernetes policy controller that manages and executes WebAssembly (Wasm) admission policies written in Rust, Go, Rego, or CEL. `[NIS2]` `[CIS]` `Apache-2.0`
- [Kyverno](https://github.com/kyverno/kyverno) - Cloud-native policy engine designed for Kubernetes that validates, mutates, generates, and verifies resource configurations and image signatures using declarative YAML. `[NIS2]` `[DORA]` `Apache-2.0`
- [Sigstore Policy Controller](https://github.com/sigstore/policy-controller) - Kubernetes admission controller that enforces Cosign container image signatures, Fulcio identities, and attested SBOM policies before pod scheduling. `[EU-CRA]` `[SLSA]` `Apache-2.0`

### Fine-Grained Authorization & Access Control Engines

- [Apache Casbin](https://github.com/apache/casbin) - Authorization library supporting ACL, RBAC, ABAC, and ReBAC access control models across Go, Python, Java, Rust, and Node.js. `[NIST-800-53]` `[SOC2/ISO27001]` `Apache-2.0`
- [Apache Ranger](https://github.com/apache/ranger) - Centralized security framework for defining, administering, and auditing fine-grained data access policies across Hadoop, SQL, and lakehouse platforms. `[GDPR]` `[DORA]` `Apache-2.0`
- [Cerbos](https://github.com/cerbos/cerbos) - Stateless, cloud-native access control decision engine that evaluates context-aware YAML authorization policies via gRPC and REST APIs. `[SOC2/ISO27001]` `[NIST-800-53]` `Apache-2.0`
- [OPAL (Open Policy Administration Layer)](https://github.com/permitio/opal) - Event-driven administration layer for Open Policy Agent and Cedar that synchronizes real-time policy and authorization data updates to edge engines. `[SOC2/ISO27001]` `[Multi-Framework]` `Apache-2.0`
- [OpenFGA](https://github.com/openfga/openfga) - Relationship-based access control (ReBAC) and authorization engine inspired by Google Zanzibar with auditable authorization modeling. `[SOC2/ISO27001]` `[NIST-800-53]` `Apache-2.0`
- [SpiceDB](https://github.com/authzed/spicedb) - Open-source, Zanzibar-inspired database and policy engine for storing and evaluating fine-grained permissions across distributed applications. `[SOC2/ISO27001]` `[NIST-800-53]` `Apache-2.0`
- [Topaz](https://github.com/aserto-dev/topaz) - Fine-grained authorization service combining Open Policy Agent policy evaluation with a Zanzibar directory graph. `[SOC2/ISO27001]` `[NIST-800-53]` `Apache-2.0`

## 3. Infrastructure-as-Code (IaC) & Static Config Auditing

Static analyzers that inspect declarative infrastructure templates, container manifests, and source code before provisioning.

### Multi-Cloud & Terraform Scanners

- [cfn-lint (CloudFormation Linter)](https://github.com/aws-cloudformation/cfn-lint) - Static validator for AWS CloudFormation JSON and YAML templates checking resource properties against the AWS specification and custom policy rules. `[CIS]` `[SOC2/ISO27001]` `MIT`
- [Checkov](https://github.com/bridgecrewio/checkov) - Graph-based static analysis scanner for Terraform, OpenTofu, CloudFormation, Kubernetes, Helm, and Bicep with built-in CIS and regulatory control mappings. `[CIS]` `[SOC2/ISO27001]` `Apache-2.0`
- [CloudFormation Guard (cfn-guard)](https://github.com/aws-cloudformation/cloudformation-guard) - Rust-based Policy-as-Code DSL and CLI validator for checking CloudFormation templates, Terraform JSON plans, and Kubernetes manifests against compliance rules. `[CIS]` `[NIST-800-53]` `Apache-2.0`
- [KICS (Keeping Infrastructure as Code Secure)](https://github.com/Checkmarx/kics) - Open-source static scanner powered by OPA Rego queries to detect security misconfigurations across IaC providers. `[CIS]` `[NIST-800-53]` `Apache-2.0`
- [TFLint](https://github.com/terraform-linters/tflint) - Pluggable Terraform linter that enforces provider-specific validity rules, naming conventions, and deprecated resource checks in CI. `[CIS]` `[Multi-Framework]` `MPL-2.0`
- [tfsec](https://github.com/aquasecurity/tfsec) - Static analysis security scanner for Terraform code that evaluates HCL templates locally and in CI pipelines against cloud security baselines. `[CIS]` `[SOC2/ISO27001]` `MIT`
- [Trivy](https://github.com/aquasecurity/trivy) - Unified security scanner for container images, filesystems, Git repositories, IaC misconfigurations, Kubernetes clusters, and SBOM generation. `[EU-CRA]` `[NIS2]` `Apache-2.0`

### Kubernetes Manifest, Helm & Container Linters

- [Conftest](https://github.com/open-policy-agent/conftest) - CLI utility built on Open Policy Agent for writing unit tests against structured configuration files including Terraform, Kubernetes, and Dockerfiles. `[Multi-Framework]` `Apache-2.0`
- [Dockle](https://github.com/goodwithtech/dockle) - Container image linter for security and compliance auditing that checks images against CIS Docker Benchmark controls. `[CIS]` `[NIS2]` `Apache-2.0`
- [Goldilocks](https://github.com/FairwindsOps/goldilocks) - Kubernetes utility that audits workload resource requests and limits against VerticalPodAutoscaler baselines to support availability controls. `[DORA]` `[NIS2]` `Apache-2.0`
- [Hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter written in Haskell that parses container build instructions into an AST and validates inline shell scripts via ShellCheck. `[CIS]` `[EU-CRA]` `GPL-3.0`
- [Kube-linter](https://github.com/stackrox/kube-linter) - Static analysis CLI tool that checks Kubernetes YAML manifests and Helm charts against production security and privilege baselines. `[CIS]` `[NIS2]` `Apache-2.0`
- [kube-no-trouble (kubent)](https://github.com/doitintl/kube-no-trouble) - CLI tool that detects Kubernetes cluster resources using deprecated or removed API versions prior to control-plane upgrades. `[DORA]` `[NIS2]` `MIT`
- [Kube-score](https://github.com/zegl/kube-score) - Static code analysis tool for Kubernetes object definitions that evaluates network policies, security contexts, and pod disruption budgets. `[CIS]` `[DORA]` `MIT`
- [Kubeconform](https://github.com/yannh/kubeconform) - Fast Kubernetes manifest validator with support for Custom Resource Definitions (CRDs) and offline JSON schema verification in CI. `[Multi-Framework]` `Apache-2.0`
- [Kubescape](https://github.com/kubescape/kubescape) - Kubernetes security platform for scanning clusters, YAML manifests, and Helm charts against NSA-CISA, MITRE ATT&CK, CIS, and SOC 2 frameworks. `[CIS]` `[SOC2/ISO27001]` `Apache-2.0`
- [Kubesec](https://github.com/controlplaneio/kubesec) - Security risk analysis tool for Kubernetes resources that produces deterministic numeric scores for Pod specifications. `[CIS]` `[NIS2]` `Apache-2.0`
- [Pluto](https://github.com/FairwindsOps/pluto) - CLI utility that scans Kubernetes repositories, Helm releases, and live clusters for deprecated API versions. `[DORA]` `[NIS2]` `Apache-2.0`
- [Polaris](https://github.com/FairwindsOps/polaris) - Validation engine and dashboard for auditing Kubernetes workloads against security, reliability, and resource isolation rules. `[CIS]` `[SOC2/ISO27001]` `Apache-2.0`
- [Popeye](https://github.com/derailed/popeye) - Live Kubernetes cluster sanitizer that scans deployed resources and reports misconfigurations, dead ports, and RBAC over-permissions. `[CIS]` `[NIS2]` `Apache-2.0`

### Source Code, Secrets & Privacy Static Analyzers

- [Bandit](https://github.com/PyCQA/bandit) - AST-based static security analyzer designed to locate common security and cryptographic defects in Python codebases. `[PCI-DSS]` `[EU-CRA]` `Apache-2.0`
- [Bearer CLI](https://github.com/Bearer/bearer) - Static application security and data-flow scanner that discovers sensitive PII/PHI data types and maps how applications process them. `[GDPR]` `[PCI-DSS]` `ELv2`
- [cargo-deny](https://github.com/EmbarkStudios/cargo-deny) - Cargo plugin for linting Rust dependency graphs against license compliance policies, banned crates, security advisories, and source registry rules. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Gitleaks](https://github.com/gitleaks/gitleaks) - Fast static scanner for detecting hardcoded secrets, API tokens, and private keys across Git repositories, files, and commit histories. `[NIS2]` `[PCI-DSS]` `MIT`
- [Gosec](https://github.com/securego/gosec) - Go security checker that inspects Go ASTs for unsafe cryptographic primitives, SQL injection vectors, and file permission weaknesses. `[PCI-DSS]` `[EU-CRA]` `Apache-2.0`
- [l0-git](https://github.com/fabriziosalmi/l0-git) - Deterministic project-hygiene gate runner that scans repositories for leaked secrets, connection strings, missing governance files, and CI defects. `[NIS2]` `[EU-CRA]` `MIT`
- [Privado CLI](https://github.com/Privado-Inc/privado) - Static privacy code scanner that discovers personal data elements in source code and traces data flows to third-party APIs, logs, and databases. `[GDPR]` `[SOC2/ISO27001]` `LGPL-3.0`
- [RustSec Advisory Database & cargo-audit](https://github.com/rustsec/rustsec) - Vulnerability advisory repository and CLI auditing toolchain for Rust crates and Cargo.lock dependency trees. `[EU-CRA]` `[NIS2]` `MIT`
- [Semgrep](https://github.com/semgrep/semgrep) - Polyglot static analysis tool with semantic pattern matching for enforcing secure coding standards, secrets prevention, and data-handling rules in CI. `[PCI-DSS]` `[GDPR]` `LGPL-2.1`
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - Secret discovery and verification engine that scans Git history, container images, S3 buckets, and filesystems for live credentials. `[NIS2]` `[SOC2/ISO27001]` `AGPL-3.0`

## 4. Software Supply Chain & Artifact Integrity

Technical enforcement tooling for SBOM generation, cryptographic signing, provenance attestation, and vulnerability correlation under the EU CRA and NIS2.

### SBOM Generation & Manipulation

- [apko](https://github.com/chainguard-dev/apko) - Declarative container image builder based on APK packages that produces reproducible OCI images and emits build-time SPDX SBOMs automatically. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [bom (Kubernetes SIGs)](https://github.com/kubernetes-sigs/bom) - CLI utility developed by Kubernetes SIG Release to generate standards-compliant SPDX Bills of Materials from images, tarballs, and source trees. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [bomctl](https://github.com/bomctl/bomctl) - Format-agnostic SBOM management CLI built on Protobom for fetching, merging, linking, and pushing CycloneDX and SPDX documents. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [cdxgen](https://github.com/cdxgen/cdxgen) - Polyglot CLI tool and library that generates CycloneDX SBOMs, CBOMs, SaaSBOMs, and OBOMs across dozens of package managers and languages. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli) - Official tool for validating, converting, merging, diffing, and cryptographically signing CycloneDX SBOM documents. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [cyclonedx-gomod](https://github.com/CycloneDX/cyclonedx-gomod) - CLI generator that produces accurate CycloneDX SBOMs with module hashes and license metadata directly from Go module repositories. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [cyclonedx-node-npm](https://github.com/CycloneDX/cyclonedx-node-npm) - Official CycloneDX SBOM generator for Node.js and npm projects producing deterministic package dependency graphs. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python) - Python library and CLI tool for generating CycloneDX SBOMs from Python virtual environments, Poetry, Pipenv, and requirements files. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [melange](https://github.com/chainguard-dev/melange) - Declarative APK package builder using YAML pipelines to produce reproducible packages and attestable software supply-chain metadata. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Microsoft SBOM Tool](https://github.com/microsoft/sbom-tool) - Scalable, enterprise CLI generator for creating SPDX 2.2 compliant SBOMs across build artifacts and container images. `[EU-CRA]` `[NIS2]` `MIT`
- [Protobom](https://github.com/protobom/protobom) - Protocol Buffer intermediary representation library enabling lossless translation and manipulation between SPDX and CycloneDX SBOM formats. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [sbom-action (Anchore)](https://github.com/anchore/sbom-action) - GitHub Action that invokes Syft during workflow builds to generate and attach SPDX or CycloneDX SBOM artifacts to releases. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [spdx-tools-golang](https://github.com/spdx/tools-golang) - Official Go library and command-line utilities for parsing, validating, converting, and manipulating SPDX documents. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [spdx-tools-python](https://github.com/spdx/tools-python) - Official Python library and CLI for parsing, validating, and converting SPDX Bills of Materials across tag-value, JSON, YAML, and XML formats. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [Syft](https://github.com/anchore/syft) - CLI tool and Go library for generating CycloneDX and SPDX Software Bills of Materials from container images and filesystems. `[EU-CRA]` `[NIS2]` `Apache-2.0`

### Vulnerability Correlation & VEX Tooling

- [CVE Binary Tool (cve-bin-tool)](https://github.com/ossf/cve-bin-tool) - OpenSSF scanner that inspects compiled binaries, firmware images, and SBOM files to detect vulnerable open-source library versions. `[EU-CRA]` `[NIS2]` `GPL-3.0`
- [Dependency-Track](https://github.com/DependencyTrack/dependency-track) - Continuous SBOM analysis platform by OWASP that ingests CycloneDX documents to monitor component vulnerabilities, license risks, and VEX statuses. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [Grype](https://github.com/anchore/grype) - Vulnerability scanner for container images, filesystems, and CycloneDX/SPDX SBOM documents with OpenVEX filtering support. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [OSV-Scanner](https://github.com/google/osv-scanner) - Vulnerability scanner written in Go that matches project lockfiles, SBOMs, and container packages against the distributed Open Source Vulnerability database. `[EU-CRA]` `[NIS2]` `Apache-2.0`
- [vexctl](https://github.com/openvex/vexctl) - CLI tool for creating, merging, attesting, and applying OpenVEX exploitability documents to filter scanner vulnerability reports. `[EU-CRA]` `[NIS2]` `Apache-2.0`

### Cryptographic Signing, Provenance & Transparency Logs

- [Archivista](https://github.com/in-toto/archivista) - Graph and storage service for archiving, indexing, and querying cryptographically signed in-toto supply-chain attestations. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Cosign](https://github.com/sigstore/cosign) - Sigstore CLI for container signing, verification, keyless OIDC attestation, and OCI registry storage of SBOMs and provenance predicates. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Fulcio](https://github.com/sigstore/fulcio) - Sigstore Root-CA for issuing short-lived code-signing X.509 certificates bound to OpenID Connect (OIDC) workload or developer identities. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Gitsign](https://github.com/sigstore/gitsign) - Keyless Git commit and tag signing CLI using Sigstore OIDC identities and the Rekor transparency log instead of long-lived GPG keys. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [Gittuf](https://github.com/gittuf/gittuf) - Security layer for Git repositories providing cryptographic policy enforcement over branches, tags, and developer signing keys. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [go-tuf](https://github.com/theupdateframework/go-tuf) - Go implementation of The Update Framework (TUF) specification for securing software repository metadata and artifact updates against key compromise. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [in-toto (Reference Implementation)](https://github.com/in-toto/in-toto) - Reference Python framework and CLI for defining software supply-chain layouts and verifying cryptographic step link metadata. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [in-toto-golang](https://github.com/in-toto/in-toto-golang) - Go library implementing the in-toto layout, link metadata, and attestation specifications for build systems and admission controllers. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [Notation (Notary Project)](https://github.com/notaryproject/notation) - CLI tool and library for signing and verifying OCI artifacts and container images using X.509 PKI trust stores. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [python-tuf](https://github.com/theupdateframework/python-tuf) - Reference Python implementation of The Update Framework (TUF) for compromise-resilient software distribution. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Rekor](https://github.com/sigstore/rekor) - Immutable, tamper-resistant cryptographic transparency log for storing signed software supply-chain metadata and attestations. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator) - Isolated, reusable GitHub Actions workflows for generating unforgeable SLSA Level 3 provenance attestations across artifacts and containers. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [SLSA Verifier](https://github.com/slsa-framework/slsa-verifier) - CLI tool to verify cryptographic SLSA provenance attestations generated by trusted CI/CD builders before deployment. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [Witness](https://github.com/in-toto/witness) - Pluggable framework for generating and verifying in-toto attestations during CI/CD build and test execution steps. `[SLSA]` `[EU-CRA]` `Apache-2.0`

### License Compliance & Dependency Governance

- [cargo-about](https://github.com/EmbarkStudios/cargo-about) - Cargo plugin for generating complete third-party license attribution bundles and verifying license policies across Rust dependencies. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [FOSSA CLI](https://github.com/fossas/fossa-cli) - Zero-configuration polyglot command-line analyzer for dependency discovery, license compliance auditing, and SBOM export. `[EU-CRA]` `[Multi-Framework]` `MPL-2.0`
- [go-licenses](https://github.com/google/go-licenses) - CLI tool that analyzes Go package dependency trees to report license classifications and block forbidden license categories in CI. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [Grant](https://github.com/anchore/grant) - CLI tool for verifying open-source license compliance across container images, SBOMs, and filesystems against configurable allow/deny rules. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [Licensee](https://github.com/licensee/licensee) - Ruby library and CLI used by GitHub to detect and match open-source repository LICENSE files against the SPDX license list. `[EU-CRA]` `[Multi-Framework]` `MIT`
- [ORT (OSS Review Toolkit)](https://github.com/oss-review-toolkit/ort) - Suite of tools to automate software dependency analysis, license compliance verification, vulnerability checks, and SBOM generation. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`
- [pip-licenses](https://github.com/raimon49/pip-licenses) - CLI tool that dumps and validates software licenses of installed Python packages in JSON, Markdown, CSV, or CycloneDX formats. `[EU-CRA]` `[Multi-Framework]` `MIT`
- [reuse-tool (FSFE)](https://github.com/fsfe/reuse-tool) - Command-line linter verifying that source repositories adhere to the FSFE REUSE specification with machine-readable SPDX copyright and license headers. `[EU-CRA]` `[Multi-Framework]` `GPL-3.0`
- [ScanCode Toolkit](https://github.com/aboutcode-org/scancode-toolkit) - Deep code scanner that detects licenses, copyright notices, package manifests, and dependencies across source files and binaries. `[EU-CRA]` `[Multi-Framework]` `Apache-2.0`

### Supply-Chain Graph & Policy Aggregators

- [Allstar](https://github.com/ossf/allstar) - GitHub App developed by OpenSSF that continuously enforces repository security settings, branch protections, and security policies across organizations. `[SLSA]` `[NIS2]` `Apache-2.0`
- [Chainloop](https://github.com/chainloop-dev/chainloop) - Open-source software supply-chain control plane for collecting, attesting, and evaluating SBOMs, SARIF reports, and CSAF advisories against declarative contracts. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [GUAC (Graph for Understanding Artifact Composition)](https://github.com/guacsec/guac) - Graph database aggregator that ingests SBOMs, SLSA attestations, and VEX documents to answer complex supply-chain compliance queries. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [Macaron](https://github.com/oracle/macaron) - Supply-chain security analyzer developed by Oracle Labs that inspects CI build pipelines and provenance against SLSA requirements. `[SLSA]` `[EU-CRA]` `UPL-1.0`
- [Minder](https://github.com/mindersec/minder) - Supply-chain security platform that enrolls repositories and artifacts to continuously enforce declarative security and provenance rules. `[SLSA]` `[EU-CRA]` `Apache-2.0`
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - Automated security health tool that evaluates open-source repositories against supply-chain checks including pinned dependencies, signed releases, and SAST gates. `[EU-CRA]` `[SLSA]` `Apache-2.0`

## 5. Host, Kernel & Runtime Hardening

Agents, eBPF sensors, and auditing frameworks that verify and enforce compliance baselines on operating systems, nodes, and container runtimes.

### SCAP, CIS & STIG Host Auditing

- [AIDE (Advanced Intrusion Detection Environment)](https://github.com/aide/aide) - File and directory integrity checker for POSIX systems that verifies cryptographic hashes and permissions to satisfy file-integrity monitoring (FIM) controls. `[PCI-DSS]` `[NIS2]` `GPL-2.0`
- [ComplianceAsCode (SCAP Security Guide)](https://github.com/ComplianceAsCode/content) - Security policy content written in SCAP, Ansible, Bash, and Ignition formats covering DISA STIG, CIS, HIPAA, PCI-DSS, and ANSSI baselines. `[CIS]` `[PCI-DSS]` `BSD-3-Clause`
- [Goss](https://github.com/goss-org/goss) - YAML-based serverspec alternative for validating Linux host state, running services, listening ports, permissions, and sysctl parameters in milliseconds. `[CIS]` `[NIS2]` `Apache-2.0`
- [InSpec](https://github.com/inspec/inspec) - Auditable testing framework that expresses operating system, network, and cloud compliance controls as executable Ruby DSL tests. `[CIS]` `[PCI-DSS]` `Apache-2.0`
- [Linux Audit Userspace (auditd)](https://github.com/linux-audit/audit-userspace) - Userspace daemon and tools (`auditctl`, `ausearch`, `aureport`) for collecting Linux kernel security audit events under CAPP, PCI-DSS, and STIG rules. `[PCI-DSS]` `[NIST-800-53]` `GPL-2.0`
- [Lynis](https://github.com/CISOfy/lynis) - Host-based security auditing and system hardening scanner for Linux, macOS, and Unix derivatives mapped to ISO 27001, PCI-DSS, and NIS2. `[SOC2/ISO27001]` `[PCI-DSS]` `GPL-3.0`
- [OpenSCAP](https://github.com/OpenSCAP/openscap) - NIST-certified SCAP command-line scanner and library for evaluating XCCDF security baselines and OVAL vulnerability definitions on Linux hosts. `[NIST-800-53]` `[CIS]` `LGPL-2.1`
- [OSSEC](https://github.com/ossec/ossec-hids) - Host-based intrusion detection system performing log analysis, file integrity checking, Windows registry monitoring, and rootkit detection. `[PCI-DSS]` `[NIS2]` `GPL-2.0`

### Kubernetes Node & Cluster Runtime Benchmarks

- [Kube-bench](https://github.com/aquasecurity/kube-bench) - Go tool that checks whether Kubernetes cluster nodes are deployed in accordance with the CIS Kubernetes Benchmark specifications. `[CIS]` `[NIS2]` `Apache-2.0`
- [Security Profiles Operator](https://github.com/kubernetes-sigs/security-profiles-operator) - Kubernetes operator that manages cluster-wide seccomp, SELinux, and AppArmor profiles with audit-log recording for workload hardening. `[CIS]` `[NIS2]` `Apache-2.0`
- [Sonobuoy](https://github.com/vmware-tanzu/sonobuoy) - Diagnostic tool that runs Kubernetes conformance tests and custom security plugins across cluster nodes to generate auditable archive reports. `[CIS]` `[Multi-Framework]` `Apache-2.0`
- [Trivy Operator](https://github.com/aquasecurity/trivy-operator) - Kubernetes-native security operator that continuously scans workloads and cluster nodes to produce CIS Benchmark, NSA, and SBOM compliance CRDs. `[CIS]` `[EU-CRA]` `Apache-2.0`

### eBPF & Kernel Runtime Policy Enforcement

- [Falco](https://github.com/falcosecurity/falco) - Cloud-native runtime security engine using eBPF to detect anomalous system calls, privilege escalations, and policy violations in real time. `[NIS2]` `[DORA]` `Apache-2.0`
- [KubeArmor](https://github.com/kubearmor/KubeArmor) - Cloud-native runtime security enforcement system that uses Linux Security Modules (AppArmor, BPF-LSM, SELinux) to restrict container process and file behavior. `[NIS2]` `[NIST-800-53]` `Apache-2.0`
- [libseccomp](https://github.com/seccomp/libseccomp) - Platform-independent library providing a high-level interface to the Linux kernel syscall filtering (seccomp-bpf) mechanism. `[CIS]` `[EU-CRA]` `LGPL-2.1`
- [Tetragon](https://github.com/cilium/tetragon) - Kernel-level eBPF security observability and synchronous runtime enforcement agent for Kubernetes workloads, system calls, and file access controls. `[NIS2]` `[DORA]` `Apache-2.0`
- [Tracee](https://github.com/aquasecurity/tracee) - Linux runtime security and forensics tool using eBPF to capture kernel events and evaluate behavioral signatures. `[NIS2]` `[SOC2/ISO27001]` `Apache-2.0`

### Fleet Telemetry, Cryptography & Log Integrity

- [cert-manager](https://github.com/cert-manager/cert-manager) - Kubernetes add-on that automates X.509 certificate issuance, renewal, and mTLS rotation from ACME, Vault, and private PKI issuers. `[NIS2]` `[DORA]` `Apache-2.0`
- [CertMate](https://github.com/fabriziosalmi/certmate) - Self-hosted TLS certificate lifecycle platform with REST API, CLI, and Helm chart for automating discovery, renewal, and deployment across infrastructure. `[NIS2]` `[DORA]` `MIT`
- [External Secrets Operator](https://github.com/external-secrets/external-secrets) - Kubernetes operator that synchronizes secrets from external secret managers into Kubernetes with auditable refresh policies. `[DORA]` `[SOC2/ISO27001]` `Apache-2.0`
- [Fleet](https://github.com/fleetdm/fleet) - Open-source device management and osquery telemetry platform for enforcing endpoint compliance policies across Linux, macOS, and Windows fleets. `[SOC2/ISO27001]` `[NIS2]` `MIT`
- [OpenBao](https://github.com/openbao/openbao) - Linux Foundation open-source identity-based secrets and encryption management system providing dynamic credentials and cryptographic audit logs. `[DORA]` `[PCI-DSS]` `MPL-2.0`
- [osquery](https://github.com/osquery/osquery) - SQL-powered operating system instrumentation and analytics agent that exposes Linux, macOS, and Windows state as relational tables. `[SOC2/ISO27001]` `[NIS2]` `Apache-2.0`
- [Rainlogs](https://github.com/fabriziosalmi/rainlogs) - Deterministic log archiving and tamper-evident retention toolkit designed for NIS2 directive log preservation compliance. `[NIS2]` `[DORA]` `Apache-2.0`
- [Sealed Secrets](https://github.com/bitnami/sealed-secrets) - Kubernetes controller and CLI for one-way asymmetric encryption of secrets so credentials can be stored safely in GitOps repositories. `[NIS2]` `[SOC2/ISO27001]` `Apache-2.0`
- [SOPS (Secrets OPerationS)](https://github.com/getsops/sops) - CNCF encrypted file editor supporting YAML, JSON, ENV, and INI formats backed by age, PGP, AWS KMS, GCP KMS, and Azure Key Vault. `[NIS2]` `[DORA]` `MPL-2.0`
- [SPIRE](https://github.com/spiffe/spire) - Production runtime environment for SPIFFE that issues cryptographic workload identities (SVIDs) for zero-trust authentication across heterogeneous infrastructure. `[DORA]` `[NIST-800-53]` `Apache-2.0`
- [Velociraptor](https://github.com/Velocidex/velociraptor) - Endpoint visibility, digital forensics, and continuous incident-response query platform powered by the Velociraptor Query Language (VQL). `[NIS2]` `[DORA]` `AGPL-3.0`
- [Wazuh](https://github.com/wazuh/wazuh) - Open-source XDR and SIEM platform providing continuous configuration assessment, file integrity monitoring, and regulatory dashboards for PCI-DSS, GDPR, and NIS2. `[PCI-DSS]` `[NIS2]` `GPL-2.0`

## 6. Automated Evidence Gathering & Cloud Posture

Tools that query live cloud APIs, identity providers, and infrastructure state to generate continuous, verifiable audit evidence and OSCAL artifacts.

### SQL-Over-Infrastructure & Asset Graph Engines

- [Cartography](https://github.com/cartography-cncf/cartography) - CNCF Python tool that consolidates infrastructure assets, IAM permissions, and network topology into a Neo4j graph database for exposure analysis. `[SOC2/ISO27001]` `[DORA]` `Apache-2.0`
- [CloudQuery](https://github.com/cloudquery/cloudquery) - High-performance open-source ELT framework that extracts configuration state from cloud APIs into SQL databases for historical posture auditing. `[DORA]` `[SOC2/ISO27001]` `Apache-2.0`
- [DataHub](https://github.com/datahub-project/datahub) - Extensible metadata and data governance platform providing fine-grained lineage, PII classification tags, and compliance audit trails across data stacks. `[GDPR]` `[EU-AI-Act]` `Apache-2.0`
- [MQL (Mondoo Query Language / cnquery)](https://github.com/mondoohq/mql) - Graph-based query engine and CLI for inspecting live configuration data across cloud accounts, Kubernetes clusters, containers, and OS hosts. `[CIS]` `[Multi-Framework]` `Apache-2.0`
- [OpenMetadata](https://github.com/open-metadata/OpenMetadata) - Unified metadata, data quality, and data governance platform for cataloging schemas, tracking lineage, and enforcing data privacy policies. `[GDPR]` `[EU-AI-Act]` `Apache-2.0`
- [Powerpipe](https://github.com/turbot/powerpipe) - Declarative HCL dashboard and benchmark runner for executing SQL-based compliance packs (CIS, NIST, SOC 2, PCI-DSS, DORA) over Steampipe or PostgreSQL. `[DORA]` `[CIS]` `Apache-2.0`
- [Steampipe](https://github.com/turbot/steampipe) - Zero-ETL SQL engine that exposes cloud APIs, Kubernetes clusters, and SaaS platforms as foreign tables in PostgreSQL for live compliance querying. `[DORA]` `[SOC2/ISO27001]` `Apache-2.0`
- [Tailpipe](https://github.com/turbot/tailpipe) - DuckDB-powered CLI tool for collecting and querying cloud audit logs, flow logs, and security events locally using standard SQL. `[DORA]` `[NIS2]` `Apache-2.0`

### Continuous Cloud Security Posture & Drift Engines

- [Cloud Custodian](https://github.com/cloud-custodian/cloud-custodian) - Rules engine for managing public cloud accounts and resources with YAML policies for real-time compliance enforcement, tagging, and encryption remediation. `[DORA]` `[SOC2/ISO27001]` `Apache-2.0`
- [cloud-nuke](https://github.com/gruntwork-io/cloud-nuke) - CLI tool for identifying and cleaning up orphaned or non-compliant cloud resources across AWS accounts to enforce environment hygiene. `[SOC2/ISO27001]` `[DORA]` `MIT`
- [CloudSploit](https://github.com/aquasecurity/cloudsploit) - Open-source cloud security posture scanner that detects misconfigurations across AWS, Azure, Google Cloud, and Oracle Cloud Infrastructure. `[CIS]` `[SOC2/ISO27001]` `Apache-2.0`
- [cnspec](https://github.com/mondoohq/cnspec) - Policy-as-code security and compliance scanner built on MQL for evaluating cloud accounts, Kubernetes, and hosts against CIS and regulatory baselines. `[CIS]` `[SOC2/ISO27001]` `Apache-2.0`
- [nis2-public](https://github.com/fabriziosalmi/nis2-public) - Self-hosted NIS2 posture management and domain security scanner that evaluates external attack surfaces, DNSSEC, TLS, and HTTP security headers. `[NIS2]` `[DORA]` `AGPL-3.0`
- [Prowler](https://github.com/prowler-cloud/prowler) - Cloud security posture and continuous compliance CLI covering AWS, Azure, GCP, and Kubernetes with native mappings for NIS2, DORA, ENS, CIS, and PCI-DSS v4.0. `[NIS2]` `[DORA]` `Apache-2.0`
- [ScoutSuite](https://github.com/nccgroup/ScoutSuite) - Multi-cloud security auditing tool that queries cloud provider APIs and generates offline HTML posture reports for AWS, Azure, and GCP. `[CIS]` `[SOC2/ISO27001]` `GPL-2.0`
- [ScubaGear](https://github.com/cisagov/ScubaGear) - CISA automation tool that assesses Microsoft 365 tenant configurations against Secure Cloud Business Applications (SCuBA) security baselines using OPA Rego. `[NIST-800-53]` `[CIS]` `CC0-1.0`
- [ScubaGoggles](https://github.com/cisagov/ScubaGoggles) - CISA assessment tool that verifies Google Workspace tenant settings against federal SCuBA security baselines using Open Policy Agent. `[NIST-800-53]` `[CIS]` `CC0-1.0`

### OSCAL Automation & Evidence-as-Code Frameworks

- [Compliance Masonry](https://github.com/opencontrol/compliance-masonry) - CLI tool that constructs System Security Plans (SSP) and gitbook compliance documentation from machine-readable OpenControl YAML files. `[NIST-800-53]` `[Multi-Framework]` `CC0-1.0`
- [Compliance Trestle](https://github.com/oscal-compass/compliance-trestle) - Python SDK and CLI managed under the OSCAL Compass project for authoring, transforming, and validating NIST OSCAL documents in Git workflows. `[NIST-800-53]` `[Multi-Framework]` `Apache-2.0`
- [go-oscal](https://github.com/defenseunicorns/go-oscal) - Go library and CLI for generating, validating, and converting NIST OSCAL types across versioned JSON and YAML schemas. `[NIST-800-53]` `[Multi-Framework]` `Apache-2.0`
- [Heimdall2](https://github.com/mitre/heimdall2) - Web-based and CLI security test result visualizer that aggregates InSpec, SARIF, SonarQube, and OWASP ZAP outputs mapped to NIST SP 800-53 controls. `[NIST-800-53]` `[Multi-Framework]` `Apache-2.0`
- [Lula](https://github.com/defenseunicorns/lula) - Kubernetes and infrastructure compliance validator that evaluates live system state and converts evidence directly into NIST OSCAL Assessment Results. `[NIST-800-53]` `[Multi-Framework]` `Apache-2.0`
- [oscal-cli](https://github.com/usnistgov/oscal-cli) - Official Java command-line tool developed by NIST for validating OSCAL catalogs, profiles, SSPs, and resolving profile imports. `[NIST-800-53]` `[Multi-Framework]` `Public-Domain`
- [oscal-sdk-go](https://github.com/oscal-compass/oscal-sdk-go) - Go SDK maintained by the Linux Foundation OSCAL Compass project for building pluggable OSCAL assessment and evidence pipelines. `[NIST-800-53]` `[Multi-Framework]` `Apache-2.0`

## 7. AI/ML Compliance & Model Governance

Testing frameworks, red-teaming scanners, and documentation generators for translating EU AI Act and ISO/IEC 42001 requirements into automated CI gates.

### LLM Red-Teaming, Guardrails & Safety Gates

- [aidlp](https://github.com/fabriziosalmi/aidlp) - Data Loss Prevention (DLP) middleware and policy proxy for LLM endpoints that intercepts and masks PII, secrets, and regulated data before external transmission. `[EU-AI-Act]` `[GDPR]` `MIT`
- [Garak](https://github.com/NVIDIA/garak) - LLM vulnerability scanner that probes generative models for prompt injection, data leakage, jailbreaks, toxicity, and hallucination weaknesses. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [Giskard OSS](https://github.com/Giskard-AI/giskard-oss) - Open-source testing and quality assurance framework for tabular ML models and LLM pipelines covering bias, robustness, and security scans. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) - Python framework for attaching input and output validators to LLM calls to enforce structural schemas, PII redaction, and topic boundaries. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [llmproxy](https://github.com/fabriziosalmi/llmproxy) - Security-first LLM gateway with tamper-evident audit logging, rate controls, and policy enforcement for regulated AI workloads. `[EU-AI-Act]` `[DORA]` `MIT`
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) - Programmable toolkit for adding conversational safety rails, fact-checking flows, and jailbreak prevention to LLM applications. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [Promptfoo](https://github.com/promptfoo/promptfoo) - CLI and CI/CD evaluation suite for deterministic LLM testing, automated red-teaming, prompt injection checks, and OWASP LLM Top 10 compliance reporting. `[EU-AI-Act]` `[ISO-42001]` `MIT`
- [Purple Llama](https://github.com/meta-llama/PurpleLlama) - Suite of open trust and safety tools including CyberSecEval benchmarks and Llama Guard classifiers for defensive generative AI deployment. `[EU-AI-Act]` `[ISO-42001]` `MIT`

### RAG Faithfulness, Hallucination & Benchmark Evaluation

- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - OpenTelemetry-based AI observability and evaluation platform for tracing LLM calls, quantifying RAG hallucination rates, and auditing model drift. `[EU-AI-Act]` `[ISO-42001]` `ELv2`
- [DeepEval](https://github.com/confident-ai/deepeval) - Unit-testing framework for LLM systems that evaluates hallucination rates, factual faithfulness, toxicity, and PII leakage inside CI pipelines. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [HELM (Holistic Evaluation of Language Models)](https://github.com/stanford-crfm/helm) - Reproducible benchmark framework by Stanford CRFM measuring accuracy, calibration, robustness, fairness, bias, and toxicity across language models. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [Hugging Face Evaluate](https://github.com/huggingface/evaluate) - Python library for standardized evaluation of machine learning models and datasets across accuracy, bias, toxicity, and statistical parity metrics. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) - Framework developed by the UK AI Safety Institute for evaluating frontier language model capabilities, autonomous agent safety, and robustness. `[EU-AI-Act]` `[ISO-42001]` `MIT`
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) - Unified benchmarking framework by EleutherAI for reproducible few-shot evaluation of causal and instruction-tuned language models. `[EU-AI-Act]` `[ISO-42001]` `MIT`
- [Ragas](https://github.com/vibrantlabsai/ragas) - Evaluation framework for Retrieval-Augmented Generation (RAG) pipelines quantifying context precision, recall, and answer faithfulness. `[EU-AI-Act]` `[ISO-42001]` `Apache-2.0`
- [TruLens](https://github.com/truera/trulens) - Instrumentation and evaluation library for tracking LLM experiments and computing groundedness, relevance, and safety feedback functions. `[EU-AI-Act]` `[ISO-42001]` `MIT`

### Algorithmic Fairness, Differential Privacy & Artifact Integrity

- [AI Fairness 360 (AIF360)](https://github.com/Trusted-AI/AIF360) - LF AI & Data toolkit of metrics and algorithms to test datasets and machine learning models for demographic bias and discrimination. `[EU-AI-Act]` `[GDPR]` `Apache-2.0`
- [ai-dependency-guard](https://github.com/fabriziosalmi/ai-dependency-guard) - Supply-chain verifier for AI and Python projects that detects hallucinated package names, slopsquatting risks, and untrusted model dependencies. `[EU-AI-Act]` `[EU-CRA]` `MIT`
- [Fairlearn](https://github.com/fairlearn/fairlearn) - Python toolkit for assessing and mitigating algorithmic bias and statistical disparity across machine learning models. `[EU-AI-Act]` `[GDPR]` `MIT`
- [ModelScan](https://github.com/protectai/modelscan) - Security scanner for serialized ML model files (Pickle, PyTorch, TensorFlow, Keras, ONNX) that detects embedded arbitrary code execution payloads. `[EU-AI-Act]` `[EU-CRA]` `Apache-2.0`
- [Opacus](https://github.com/meta-pytorch/opacus) - High-speed library for training PyTorch models with formal differential privacy guarantees and mathematical privacy budget accounting. `[GDPR]` `[EU-AI-Act]` `Apache-2.0`
- [Picklescan](https://github.com/mmaitre314/picklescan) - Security scanner that inspects Python Pickle files and Hugging Face PyTorch model archives for malicious opcode imports before loading weights. `[EU-AI-Act]` `[EU-CRA]` `MIT`
- [TensorFlow Privacy](https://github.com/tensorflow/privacy) - Library implementing differentially private stochastic gradient descent optimizers and membership-inference privacy attack tests. `[GDPR]` `[EU-AI-Act]` `Apache-2.0`

## 8. Pre-Built Policy Packs & Mappings

Ready-to-run policy rulesets, control catalogs, and hardening baselines mapped to specific regulatory standards.

### Machine-Readable Control Catalogs & Requirements

- [MITRE ATT&CK Decider](https://github.com/cisagov/decider) - CISA web application and structured catalog mapping adversary behaviors to MITRE ATT&CK techniques and defensive controls. `[NIS2]` `[NIST-800-53]` `CC0-1.0`
- [MITRE Vulcan](https://github.com/mitre/vulcan) - Application for authoring and exporting Security Technical Implementation Guides (STIGs) and InSpec compliance profiles mapped to NIST SP 800-53. `[NIST-800-53]` `[CIS]` `Apache-2.0`
- [NIST OSCAL Content Repository](https://github.com/usnistgov/oscal-content) - Official machine-readable JSON, YAML, and XML control catalogs and baselines for NIST SP 800-53 Rev. 5, FedRAMP, and NIST Cybersecurity Framework. `[NIST-800-53]` `[Multi-Framework]` `Public-Domain`
- [OWASP ASVS (Application Security Verification Standard)](https://github.com/OWASP/ASVS) - Community-maintained catalog of application security requirements published in JSON, CSV, XML, and Markdown formats for automated verification mapping. `[PCI-DSS]` `[EU-CRA]` `CC-BY-4.0`
- [OWASP OpenCRE (Common Requirements Enumeration)](https://github.com/OWASP/OpenCRE) - Interactive knowledge graph and API linking security standards (NIST 800-53, ISO 27001, OWASP ASVS, CWE, CAPEC) to unified technical controls. `[Multi-Framework]` `Apache-2.0`

### Kubernetes, OPA & Kyverno Policy Libraries

- [Gatekeeper Library](https://github.com/open-policy-agent/gatekeeper-library) - Community-owned library of OPA Gatekeeper ConstraintTemplates and Rego policies enforcing Kubernetes Pod Security Standards and network isolation. `[CIS]` `[NIS2]` `Apache-2.0`
- [Kyverno Policy Library](https://github.com/kyverno/policies) - Official repository of Kubernetes Pod Security Standards (PSS), supply-chain attestation rules, and multi-tenancy isolation policies for Kyverno. `[CIS]` `[NIS2]` `Apache-2.0`
- [Red Hat CoP Rego Policies](https://github.com/redhat-cop/rego-policies) - Collection of Open Policy Agent Rego policies tested with Conftest for validating OpenShift, Kubernetes, and Tekton supply-chain resources. `[CIS]` `[NIS2]` `Apache-2.0`

### Host, Edge & Cloud Hardening Baselines

- [Ansible Collection Hardening (DevSec)](https://github.com/dev-sec/ansible-collection-hardening) - Ansible collection hardening Linux OS, SSH, Nginx, MySQL, and PostgreSQL nodes against CIS and DevSec baselines. `[CIS]` `[NIS2]` `Apache-2.0`
- [Ansible Lockdown RHEL 9 CIS](https://github.com/ansible-lockdown/RHEL9-CIS) - Automated Ansible role implementing CIS Red Hat Enterprise Linux 9 Benchmark controls with configurable audit and remediation tags. `[CIS]` `[NIST-800-53]` `MIT`
- [caddy-waf](https://github.com/fabriziosalmi/caddy-waf) - Web Application Firewall middleware for Caddy enforcing OWASP anomaly detection, rate limiting, GeoIP, and bad-bot rules at the HTTP edge. `[NIS2]` `[PCI-DSS]` `AGPL-3.0`
- [Coraza WAF](https://github.com/corazawaf/coraza) - OWASP enterprise-grade Go Web Application Firewall library compatible with ModSecurity SecLang and the OWASP Core Rule Set. `[PCI-DSS]` `[NIS2]` `Apache-2.0`
- [DevSec Linux Baseline](https://github.com/dev-sec/linux-baseline) - InSpec compliance profile verifying Linux kernel parameters, filesystem mounts, and package configurations against production security baselines. `[CIS]` `[NIS2]` `Apache-2.0`
- [MITRE SAF (Security Automation Framework) CLI & Profiles](https://github.com/mitre/saf) - CLI toolkit and curated InSpec profiles for validating cloud, container, and OS deployments against NIST SP 800-53 and DISA STIG controls. `[NIST-800-53]` `[CIS]` `Apache-2.0`
- [ModSecurity](https://github.com/owasp-modsecurity/ModSecurity) - Cross-platform open-source Web Application Firewall engine for Apache, Nginx, and IIS supporting real-time HTTP traffic inspection. `[PCI-DSS]` `[NIS2]` `Apache-2.0`
- [Nuclei](https://github.com/projectdiscovery/nuclei) - YAML-templated vulnerability and misconfiguration scanner for continuous verification of exposed services, TLS posture, and CVE remediations. `[NIS2]` `[DORA]` `MIT`
- [OWASP Core Rule Set (CRS)](https://github.com/coreruleset/coreruleset) - Generic attack detection rule set for ModSecurity and Coraza protecting web applications against OWASP Top 10 risks for PCI-DSS 6.4 compliance. `[PCI-DSS]` `[NIS2]` `Apache-2.0`
- [OWASP ZAP (Zed Attack Proxy)](https://github.com/zaproxy/zaproxy) - Dynamic Application Security Testing (DAST) proxy with GitHub Actions and CLI automation for verifying web application security controls in CI. `[PCI-DSS]` `[NIS2]` `Apache-2.0`
- [patterns (Multi-Engine WAF & Bot Rules)](https://github.com/fabriziosalmi/patterns) - Automated security rule generator translating OWASP CRS and threat patterns into configurations for Nginx, Apache, Traefik, and HAProxy. `[NIS2]` `[PCI-DSS]` `MIT`
- [SIMP (System Integrity Management Platform)](https://github.com/simp/simp-core) - Puppet-based compliance automation framework designed for operating systems regulated under NIST SP 800-53, DISA STIG, and CIS benchmarks. `[NIST-800-53]` `[CIS]` `Apache-2.0`
- [wafcontrol](https://github.com/fabriziosalmi/wafcontrol) - Declarative GitOps toolkit for managing and auditing Cloudflare Web Application Firewall rulesets as versioned YAML in CI pipelines. `[NIS2]` `[DORA]` `MIT`
- [zonecontrol](https://github.com/fabriziosalmi/zonecontrol) - GitOps configuration and drift-detection tool for enforcing DNS, TLS, and perimeter security settings as YAML across Cloudflare zones. `[NIS2]` `[DORA]` `AGPL-3.0`

## 9. Educational & Reference Architectures

Technical specifications, working groups, and engineering blueprints for designing continuous compliance pipelines.

- [OpenGitOps Documents](https://github.com/open-gitops/documents) - CNCF OpenGitOps principles and reference specifications for declarative, immutable, and continuously reconciled system state. `[DORA]` `[Multi-Framework]` `CC-BY-4.0`
- [OpenSSF Best Practices for Open Source Developers](https://github.com/ossf/wg-best-practices-os-developers) - OpenSSF working group guides covering compiler hardening flags, secure software development lifecycles, and dependency hygiene. `[EU-CRA]` `[SLSA]` `CC-BY-4.0`
- [OpenSSF OSPS Baseline (Open Source Project Security Baseline)](https://github.com/ossf/security-baseline) - Catalog of machine-mappable security controls for open-source projects aligned with the EU Cyber Resilience Act and NIST SSDF. `[EU-CRA]` `[NIST-800-53]` `Apache-2.0`
- [OpenSSF S2C2F (Secure Supply Chain Consumption Framework)](https://github.com/ossf/s2c2f) - Engineering framework governing how enterprises ingest, scan, rebuild, and audit third-party open-source dependencies. `[EU-CRA]` `[NIS2]` `CC-BY-4.0`
- [OpenSSF Supply Chain Integrity Working Group](https://github.com/ossf/wg-supply-chain-integrity) - Working group repository maintaining supply-chain threat models, SLSA governance, and software provenance reference architectures. `[EU-CRA]` `[SLSA]` `Apache-2.0`
- [OWASP AI Security and Privacy Guide](https://github.com/OWASP/www-project-ai-security-and-privacy-guide) - Technical engineering guide detailing adversarial robustness controls, model provenance, and data minimization under GDPR and the EU AI Act. `[EU-AI-Act]` `[GDPR]` `CC-BY-4.0`
- [OWASP CycloneDX Authoritative Guide to SBOM](https://github.com/CycloneDX/bom-examples) - Official repository of machine-readable SBOM, CBOM, VEX, and attestation examples for software supply-chain compliance. `[EU-CRA]` `[NIS2]` `CC0-1.0`
- [OWASP Top 10 for Large Language Model Applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications) - Reference taxonomy of security and governance failure modes in generative AI applications including prompt injection and training data poisoning. `[EU-AI-Act]` `[ISO-42001]` `CC-BY-4.0`

## Regulatory-to-Code Mapping Matrix

The matrix below maps statutory and industry compliance articles to deterministic engineering controls and open-source enforcement tooling.

| Regulation / Standard | Article / Control | Legal / Standard Requirement | Engineering Control (CaC) | Tooling & Verification Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **EU Cyber Resilience Act (CRA)** | Art. 13(5), Art. 13(23) & Annex I Part II | Identify and document vulnerabilities and components via a machine-readable SBOM; ensure artifact integrity. | Generate CycloneDX/SPDX SBOM at build time, scan against CVE/OpenVEX feeds, and sign OCI artifacts before release. | `syft` + `grype` + `cosign` in CI; admission check via OPA or Kyverno. |
| **EU NIS2 Directive** | Art. 21(2)(d) & Art. 21(2)(e) | Supply-chain security and security in network and information systems acquisition, development, and maintenance. | Reject container workloads running as root (`UID 0`) or missing verified provenance annotations at cluster admission. | `trivy` in CI/CD + OPA Rego (`examples/opa/cra_workloads.rego`) or Kyverno policy. |
| **EU DORA** | Art. 9(2) & Art. 10(1) | Continuous protection of ICT systems, cryptographic key/data protection at rest and in transit, and configuration drift detection. | Enforce keyless image signature verification on production pods and run continuous SQL queries over cloud storage encryption state. | Kyverno (`examples/kyverno/dora_signed_images.yaml`) + Steampipe (`examples/steampipe/dora_s3_encryption.sql`). |
| **EU AI Act** | Art. 10, Art. 14 & Art. 15 | Data governance, bias detection, accuracy measurement, and resilience against adversarial manipulation (prompt injection) for high-risk AI systems. | Execute automated red-teaming, bias disparity metrics, and hallucination thresholds as blocking pull-request gates. | `promptfoo`, `garak`, `giskard-oss`, and `fairlearn` in ML CI workflows. |
| **GDPR** | Art. 25 & Art. 32 | Data protection by design and by default; pseudonymisation, encryption, and prevention of unauthorized PII logging. | Static AST rules blocking unmasked PII fields in log sinks and verifying column-level encryption on data stores. | `semgrep` / `bearer` / `privado` + `checkov` / `steampipe` database encryption audits. |
| **PCI-DSS v4.0** | Req. 6.3.2 & Req. 6.4.3 | Maintain bespoke and third-party software inventory; authorize and assure integrity of all payment page scripts. | Automated SBOM generation on every release plus static verification of Content Security Policy (CSP) and Subresource Integrity (SRI). | `cdxgen` / `ort` + `semgrep` + `inspec` host baseline checks. |
| **NIST SP 800-53 Rev. 5** | AC-6 (Least Privilege) & CM-2 (Baseline Config) | Enforce least privilege across identities and workloads; maintain automated baseline configurations and system security plans. | Validate IAM policies for wildcard absence and emit machine-readable OSCAL Component Definitions and Assessment Results. | `cedar` / `checkov` + `lula` / `compliance-trestle` (`examples/oscal/cra_component_definition.json`). |
| **ISO/IEC 42001** | Annex A.6.2 & A.8.4 | Document AI system lifecycle, training data provenance, model limitations, and continuous runtime evaluation metrics. | Verify model weight safety, track evaluation benchmarks, and evaluate RAG faithfulness in CI. | `modelscan` + `deepeval` / `ragas` / `promptfoo`. |

## Reference Implementations

All code snippets below are synchronized with and tested against the files under [`examples/`](examples/) in CI.

### 1. OPA Rego v1: EU CRA & NIS2 Workload Hardening (`examples/opa/cra_workloads.rego`)

Tested in CI via `opa check --strict` and `opa test examples/opa/ -v` ([`examples/opa/cra_workloads_test.rego`](examples/opa/cra_workloads_test.rego)).

```rego
# METADATA
# title: Enforce CRA and NIS2 Container Hardening
# description: Requires non-root execution and a verified SBOM attestation annotation
package compliance.cra.workloads

import rego.v1

default allow := false

allow if {
	count(violation) == 0
}

has_root_containers if {
	input.request.kind.kind == "Pod"
	some container in input.request.object.spec.containers
	not container.securityContext.runAsNonRoot == true
}

has_sbom_annotation if {
	input.request.kind.kind == "Pod"
	input.request.object.metadata.annotations["compliance.example.org/sbom-verified"] == "true"
}

violation contains msg if {
	has_root_containers
	msg := "NIS2/CRA violation: every container must set securityContext.runAsNonRoot to true"
}

violation contains msg if {
	input.request.kind.kind == "Pod"
	not has_sbom_annotation
	msg := "CRA violation: Pod metadata must include annotation compliance.example.org/sbom-verified=true"
}
```

### 2. Kyverno ClusterPolicy: DORA Art. 9 Keyless Signature & Privilege Gate (`examples/kyverno/dora_signed_images.yaml`)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: dora-require-signed-images-and-non-privileged
  annotations:
    policies.kyverno.io/title: DORA ICT Artifact and Runtime Integrity Gate
    policies.kyverno.io/category: Regulatory Compliance
    policies.kyverno.io/severity: high
    policies.kyverno.io/subject: Pod
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: verify-sigstore-keyless-attestation
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "ghcr.io/enterprise-org/*"
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"
                    subject: "https://github.com/enterprise-org/*"
                    rekor:
                      url: "https://rekor.sigstore.dev"
    - name: forbid-privileged-containers
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "DORA Art. 9 violation: privileged containers are prohibited in production namespaces."
        pattern:
          spec:
            containers:
              - =(securityContext):
                  =(privileged): false
```

### 3. Steampipe SQL: DORA Art. 10 & SOC 2 Encryption at Rest Audit (`examples/steampipe/dora_s3_encryption.sql`)

```sql
-- Query AWS S3 buckets lacking default server-side encryption at rest (DORA Art. 10 / SOC 2 CC6.1)
select
  name as bucket_name,
  region,
  server_side_encryption_configuration -> 'Rules' as encryption_rules,
  case
    when server_side_encryption_configuration is null then 'NON_COMPLIANT'
    else 'COMPLIANT'
  end as compliance_status,
  'DORA Art. 10 / SOC 2 CC6.1 - Encryption at Rest' as control_reference
from
  aws_s3_bucket
where
  server_side_encryption_configuration is null;
```

### 4. NIST OSCAL 1.1.2 Component Definition (`examples/oscal/cra_component_definition.json`)

```json
{
  "component-definition": {
    "uuid": "8c504b8e-4f1a-4b0c-9a6d-12e4f8c90123",
    "metadata": {
      "title": "Payments API Service Component Definition",
      "last-modified": "2026-10-17T12:00:00Z",
      "version": "1.0.0",
      "oscal-version": "1.1.2"
    },
    "components": [
      {
        "uuid": "d2f9a110-7c4b-4e89-8f12-9b0012345678",
        "type": "software",
        "title": "payments-api",
        "description": "Core payment processing service with automated SBOM and non-root execution gates.",
        "control-implementations": [
          {
            "uuid": "f1a2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c",
            "source": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
            "description": "NIST SP 800-53 Rev. 5 and EU CRA technical control mappings.",
            "implemented-requirements": [
              {
                "uuid": "a0b1c2d3-e4f5-4a6b-8c7d-9e0f1a2b3c4d",
                "control-id": "ac-6",
                "description": "Enforces least privilege via non-root container execution validated by OPA policy compliance.cra.workloads."
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and run `python3 scripts/validate_readme.py` before submitting a pull request.

## License

[![CC0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, the maintainers have waived all copyright and related or neighboring rights to this work under the [CC0 1.0 Universal Public Domain Dedication](LICENSE).
