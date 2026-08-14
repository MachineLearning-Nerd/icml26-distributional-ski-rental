# Publication gate

The current gate is a self-contained `SCOPED_PASS` for the three claims in the
README ledger.

## Checks

`repro/src/cumulative_science_gate.py` validates the committed verification
report, all four source hashes, exact finite cell counts, zero proof-chain
failures, nine hard-family scales, exponent ranges, and the boundary/interface
controls.

`repro/src/publication_gate.py` then runs the focused tests, rebuilds and
validates the public evidence manifest, rejects stale full-ready markers, and
writes identical canonical summaries to:

- `publication_gate.json`
- `outputs/publication_gate.json`

The gate does not depend on `.trackio/metadata.json`, absolute local paths, a
private Space, or a queue handoff.

## Status semantics

`publication_gate_passed: true` means the three declared source-anchored claims
passed their exact contracts. It does not mean that every auxiliary appendix
has been turned into a separate claim. `score_forecast` remains `null` because
the current evidence is a reproduction audit, not a prediction of an external
evaluation score.
