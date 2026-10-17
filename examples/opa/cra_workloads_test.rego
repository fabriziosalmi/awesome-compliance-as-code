package compliance.cra.workloads_test

import data.compliance.cra.workloads
import rego.v1

test_compliant_pod_allowed if {
	workloads.allow with input as {"request": {
		"kind": {"kind": "Pod"},
		"object": {
			"metadata": {"annotations": {"compliance.example.org/sbom-verified": "true"}},
			"spec": {"containers": [{
				"name": "payments-api",
				"securityContext": {"runAsNonRoot": true},
			}]},
		},
	}}
}

test_root_container_rejected if {
	not workloads.allow with input as {"request": {
		"kind": {"kind": "Pod"},
		"object": {
			"metadata": {"annotations": {"compliance.example.org/sbom-verified": "true"}},
			"spec": {"containers": [{
				"name": "payments-api",
				"securityContext": {"runAsNonRoot": false},
			}]},
		},
	}}
}

test_missing_sbom_annotation_rejected if {
	not workloads.allow with input as {"request": {
		"kind": {"kind": "Pod"},
		"object": {
			"metadata": {"annotations": {}},
			"spec": {"containers": [{
				"name": "payments-api",
				"securityContext": {"runAsNonRoot": true},
			}]},
		},
	}}
}
