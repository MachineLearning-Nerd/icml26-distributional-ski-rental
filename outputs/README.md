# Output contract

| File | Producer | Meaning |
| --- | --- | --- |
| `independent_verification.json` | `repro/src/verify_ski_rental.py` | Exact finite-distribution, hard-family, and interface evidence |
| `evidence_bundle.jsonl` | `repro/src/build_evidence_bundle.py` | Hash manifest for public code, source anchors, docs, and evidence |
| `CUMULATIVE_SCIENCE_GATE.json` | `repro/src/cumulative_science_gate.py` | Claim-level validation result |
| `publication_gate.json` | `repro/src/publication_gate.py` | Canonical scoped publication status |
| `PUBLICATION_GATE_PASSED.json` | historical | Retained pre-audit marker; not used by the current gate |

The current gate requires every manifest row to match the committed file's
size and SHA-256. The root and `outputs/` publication-gate copies must also be
identical.
