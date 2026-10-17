# Security Policy

## Supported Versions

This repository is continuously maintained on the `main` branch.

| Version | Supported |
| :--- | :--- |
| `1.0.x` (`main`) | Yes |
| `< 1.0.0` | No |

## Scope

`awesome-compliance-as-code` maintains a curated catalog of Compliance-as-Code specifications and tools, executable reference policies under `examples/`, and automated verification scripts under `scripts/` and `.github/workflows/`.

Security issues in scope for this repository include:

1. **Reference Policy Defects**: Policy bypasses, insecure defaults, or logic errors in `examples/opa/cra_workloads.rego`, `examples/kyverno/dora_signed_images.yaml`, `examples/steampipe/dora_s3_encryption.sql`, or `examples/oscal/cra_component_definition.json`.
2. **Compromised Catalog Links**: Upstream repository compromises, malicious domain takeovers, typosquatted URLs, or deprecated/abandoned tools listed in `README.md`.
3. **CI/CD and Validator Vulnerabilities**: Command injection, workflow permission escalation, or parsing vulnerabilities in `scripts/*.py` or `.github/workflows/*.yml`.

## Supply-Chain Controls Enforced on This Repository

- **SHA-Pinned Workflows**: Every third-party GitHub Action in `.github/workflows/` is pinned to an immutable 40-character commit SHA rather than a mutable tag.
- **Least-Privilege Token Permissions**: Workflows declare explicit top-level `permissions: contents: read` blocks.
- **Zero External Python Dependencies**: All validation scripts (`scripts/validate_readme.py`, `scripts/check_links.py`, `scripts/check_repo_health.py`) use only the Python standard library.
- **Continuous Link & Repository Health Auditing**: Scheduled workflows verify hyperlink reachability weekly (`links.yml`) and audit GitHub repository archive/activity status quarterly (`health-check.yml`).

## Reporting a Vulnerability or Compromised Link

- **Compromised or Hijacked External Link**: Open an issue or pull request removing the affected catalog entry immediately.
- **Vulnerability in Reference Policies, Scripts, or Workflows**: Do not open a public issue. Report privately via [GitHub Private Vulnerability Reporting](https://github.com/fabriziosalmi/awesome-compliance-as-code/security/advisories/new).

We acknowledge reports within **48 hours** and publish remediations promptly after verification.
