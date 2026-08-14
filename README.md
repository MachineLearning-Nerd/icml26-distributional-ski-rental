# Ski Rental with Distributional Predictions of Unknown Quality

Clean-room, exact-rational reproduction for:

- OpenReview: [`h8NydU966G`](https://openreview.net/forum?id=h8NydU966G)
- arXiv: [`2602.21104v1`](https://arxiv.org/abs/2602.21104)
- Authors: Qiming Cui and Michael Dinitz

## Current status

`VERIFIED_SCOPED`

The three source-anchored claims in the current audit scope pass the exact
finite-distribution, hard-family, and interface checks. The scoped publication
gate is `SCOPED_PASS`; no numerical score forecast is made. The source archive
does not advertise author code, so this is an independent clean-room audit and
not an author-code parity claim.

## What the paper studies

The paper treats ski rental when the prediction is a distribution `p-hat` over
the number of ski days rather than a single point prediction. The main policy
computes the optimal predicted-distribution buy threshold `K-hat`, computes a
tail quantile `U` at mass `1/sqrt(b)`, and runs at
`K* = min(K-hat + sqrt(b), U + sqrt(b))`. Its loss is bounded both by a
prediction-sensitive `O(sqrt(b) max(EMD(p-hat, p), 1))` term and by a robust
`O(b log b)` term.

## Claim-to-evidence ledger

| Claim | Status | Evidence producer | Independent checker | Recorded result |
| --- | --- | --- | --- | --- |
| Distribution-sensitive upper bound and transported-tail proof chain | `VERIFIED_SCOPED` | `repro/src/verify_ski_rental.py` reconstructs `tail`, `emd`, `optimum`, the source threshold rule, and both upper-bound routes | `repro/src/cumulative_science_gate.py` plus the focused tests | 238,140 exact tail cells; 79,380 algorithm cells; zero violations/failures |
| Consistency/robustness trade-off is tight | `VERIFIED_SCOPED` | `hard_tail()` and `hard_quantile()` audit `b=2^4,...,2^20` | Exact quantile certificates and exponent checks | All quantiles valid; consistency exponent `0.507758`; robustness exponent `0.998898` against `b log b` |
| The policy does not need the unknown prediction-error bound | `VERIFIED_SCOPED` | `source_algorithm()` and the boundary/interface mutation audit | Truth-invariance and illegal eta-aware mutation controls | Source threshold remains `16` for four truths; an eta-aware mutation changes thresholds |

The exact producer-to-checker paths are expanded in
[`docs/CLAIM_AUDIT.md`](docs/CLAIM_AUDIT.md).

## Reproduction protocol

The audit uses Python `Fraction` for finite distributions and 90-digit decimal
arithmetic for the hard family. It exhausts all 4-unit rational distributions
over support `{0,1,2,3,4,5}`, five buy-cost scales for the finite algorithm
sweep, and nine powers `b=2^4` through `2^20` for the hard family. No sampled
proxy or learned model is substituted.

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements.txt
.venv/bin/python repro/src/verify_ski_rental.py --output outputs/independent_verification.json
.venv/bin/python -m pytest -q repro/tests
.venv/bin/python repro/src/publication_gate.py
```

The generator writes the committed verification report. The publication gate
checks the report, source hashes, exact output manifest, focused tests, and
canonical gate copies without relying on private Trackio paths or a hidden
publication service.

## Branch map

The original repository had only `main`; there were no `orx/*` experiment
branches to preserve or rename. The branch audit and release identity are in
[`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md).

## Citation

```bibtex
@article{cui2026distributionalskirental,
  title         = {Ski Rental with Distributional Predictions of Unknown Quality},
  author        = {Cui, Qiming and Dinitz, Michael},
  journal       = {arXiv preprint arXiv:2602.21104},
  year          = {2026},
  url           = {https://arxiv.org/abs/2602.21104}
}
```

## Thank you

Thank you to Qiming Cui and Michael Dinitz for making the paper and its source
available. The source made it possible to reconstruct the threshold policy and
test its prediction sensitivity, robustness, and consistency trade-offs with
exact arithmetic while preserving the proof boundaries.

## Provenance and limits

- The vendored source archive is `2602.21104v1`; active source hashes are
  recorded in [`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md) and `sources.json`.
- No author implementation was advertised in the primary source; the verifier
  is independent exact arithmetic.
- The evidence covers the three current source-anchored claims listed above,
  not an unbounded numerical survey of every distribution or buy cost.
- `outputs/PUBLICATION_GATE_PASSED.json` is retained as a historical marker;
  the current canonical result is `publication_gate.json`.
