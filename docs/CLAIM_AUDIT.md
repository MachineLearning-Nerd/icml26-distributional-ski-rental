# Claim audit — h8NydU966G

The current evaluation scope contains three source-anchored claims. Each
status below means the declared finite/exact contract passed; it does not claim
that every possible distribution or parameter value was exhaustively tested.

## Claim 1 — distribution-sensitive upper bound

Source anchors: the main algorithm in `source/arxiv/main_algorithm.tex`, the
transported-tail lemma, and the proof of the two bounds
`O(sqrt(b) max(EMD,1))` and `O(b log b)`.

Producer path:

1. `compositions()` enumerates all distributions with denominator 4 over six
   support points.
2. `tail()`, `emd()`, `cost()`, and `optimum()` reconstruct the source
   quantities with `Fraction`.
3. `source_algorithm()` reconstructs `K-hat`, `U`, and `K*`.
4. The verifier checks the transported-tail inequality, truncation inequality,
   and both loss normalizations over five buy-cost scales.

Checker path: `repro/src/cumulative_science_gate.py` checks the exact cell
counts and requires zero violations/failures. The focused tests independently
exercise EMD, the non-strict tail boundary, prediction-only behavior, and the
committed full audit report.

Recorded result: 238,140 tail cells and 79,380 algorithm cells; zero failures;
maximum observed normalized ratios `1.5` and `0.7213475`.

Status: `VERIFIED_SCOPED`.

## Claim 2 — tight consistency/robustness trade-off

Source anchor: `source/arxiv/consistency_robustness.tex` and the hard-family
construction in the appendix.

Producer path: `hard_tail()` and `hard_quantile()` use 90-digit decimal
arithmetic to certify the quantile and policy threshold for `b=2^4` through
`2^20`. The verifier computes the consistency loss and robustness threshold,
then fits slopes on the final five scales.

Checker path: the cumulative gate requires all nine quantile certificates and
requires the final-five consistency exponent to lie in `(0.45,0.55)` and the
robustness exponent against `b log b` to lie in `(0.95,1.05)`.

Recorded result: all quantiles valid; consistency exponent `0.5077583`;
robustness exponent `0.9988981`.

Status: `VERIFIED_SCOPED`.

## Claim 3 — no prediction-error bound is required

Source anchor: the `K*` rule in `main_algorithm.tex`, which uses only the
prediction distribution, its optimal threshold, and its `1/sqrt(b)` tail
quantile.

Producer path: the verifier fixes a boundary prediction at `b=256`, compares
the source non-strict tail rule with a strict-tail mutation, and evaluates four
truth distributions. It also runs an illegal eta-aware mutation as a negative
control.

Checker path: the cumulative gate requires the source threshold to remain `16`
for all four truths, while the eta-aware mutation must vary across truths. It
also requires the strict boundary mutation to move the quantile from `0` to
`255` and the threshold from `16` to `271`.

Status: `VERIFIED_SCOPED`.

## Boundary

The source also contains a further robustification appendix and auxiliary lower
bounds. They remain available under the pinned source, but this repository does
not promote them to separate claims without dedicated evidence contracts.
