# Source audit — h8NydU966G

## Identity

- Title: *Ski Rental with Distributional Predictions of Unknown Quality*
- Authors: Qiming Cui and Michael Dinitz
- OpenReview: `h8NydU966G`
- arXiv: `2602.21104v1`
- Source archive SHA-256: `f4332df2005da57a5d0dc409e5b321813868878a04d00ad303962dd9755b6864`
- Main source: `source/arxiv/main.tex`, SHA-256 `5b5eeec7386bd0f7ffa00c0a34280911ea18438cc6bef09a95edcf54da39d07d`

## Hash-pinned anchors

| Source file | SHA-256 | Role |
| --- | --- | --- |
| `source/arxiv/main_algorithm.tex` | `47c36490f628d8028364a8bee3c80862af4ed69ad680b921ddc0f0edafaa7a54` | `K*` policy and prediction-sensitive/robust upper bounds |
| `source/arxiv/consistency_robustness.tex` | `4df60b9cecc995fc2d639f914809c31bd0b44146300ef1a9551632162ab1822f` | consistency/robustness lower-bound trade-off |
| `source/arxiv/base_algorithm_with_proof.tex` | `5a084a4919de80641caf48268e18f6d2a2cc78c2f7ff9742ad2ebdcd1f458a73` | base algorithm and transported-tail proof |

The cumulative gate checks every anchor in `sources.json` before accepting the
committed evidence.

## Provenance boundary

The repository records that no author implementation is advertised in the
primary source. `repro/src/verify_ski_rental.py` is a clean-room reconstruction
of the definitions and proof interfaces, using exact rational and high-
precision decimal arithmetic.
