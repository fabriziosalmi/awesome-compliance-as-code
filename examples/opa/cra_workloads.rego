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
