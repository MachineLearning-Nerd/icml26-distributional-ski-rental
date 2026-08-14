#!/usr/bin/env python3
"""Validate the committed exact evidence for Claims 1–3."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = "h8NydU966G"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    report = json.loads((ROOT / "outputs/independent_verification.json").read_text())
    source = json.loads((ROOT / "sources.json").read_text())
    require(report["paper"] == PAPER, "wrong verification paper")
    require(source["paper"]["openreview_id"] == PAPER, "wrong source paper")
    require("clean-room" in source["implementation"], "implementation provenance changed")
    for relative, expected in source["anchors"].items():
        actual = digest(ROOT / "source/arxiv" / relative)
        require(actual == expected, f"source hash mismatch: {relative}")

    claims = {claim["id"]: claim for claim in report["claims"]}
    require(set(claims) == {"C1", "C2", "C3"}, "claim inventory changed")
    require(all(claim["outcome"] == "verified" for claim in claims.values()), "claim outcome changed")

    c1 = claims["C1"]
    require(c1["finite_tail_lemma"]["distribution_pairs"] == 15876, "tail distribution count changed")
    require(c1["finite_tail_lemma"]["cells"] == 238140, "tail cell count changed")
    require(c1["finite_tail_lemma"]["violations"] == 0, "tail lemma violation")
    require(c1["finite_algorithm_sweep"]["cells"] == 79380, "algorithm sweep count changed")
    require(c1["finite_algorithm_sweep"]["truncation_inequality_failures"] == 0, "truncation inequality failure")
    require(c1["finite_algorithm_sweep"]["tail_chain_failures"] == 0, "transported-tail failure")

    c2 = claims["C2"]["hard_family"]
    expected_b = [16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576]
    require([row["b"] for row in c2["rows"]] == expected_b, "hard-family scales changed")
    require(c2["all_quantiles_valid"], "hard-family quantile failure")
    require(0.45 < c2["consistency_exponent_last_five"] < 0.55, "consistency exponent failed")
    require(0.95 < c2["robustness_exponent_vs_b_log_b_last_five"] < 1.05, "robustness exponent failed")

    c3 = claims["C3"]["prediction_error_independence"]
    require(c3["source_khat_is_infinity"] and c3["source_u"] == 0, "source threshold setup changed")
    require(c3["source_threshold"] == 16 and c3["strict_u"] == 255, "boundary control changed")
    require(len(set(c3["thresholds_by_truth"].values())) == 1, "source threshold depends on truth")
    require(len(set(c3["eta_aware_mutation_thresholds"].values())) > 1, "eta mutation control failed")

    payload = {
        "paper": PAPER,
        "gate_version": "scoped-v2",
        "status": "SCOPED_PASS",
        "strict_status": "SCOPED_PASS",
        "claims": {
            "C1": {
                "status": "VERIFIED_SCOPED",
                "evidence": "238,140 tail cells and 79,380 exact algorithm cells",
            },
            "C2": {
                "status": "VERIFIED_SCOPED",
                "evidence": "nine-scale exact hard-family audit",
            },
            "C3": {
                "status": "VERIFIED_SCOPED",
                "evidence": "truth-invariance and illegal eta-aware mutation controls",
            },
        },
        "controls": {
            "strict_tail_boundary": True,
            "truth_independence": True,
            "eta_aware_mutation_detected": True,
        },
        "source_anchor_sha256": source["anchors"],
        "score_forecast": None,
    }
    (ROOT / "outputs/CUMULATIVE_SCIENCE_GATE.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
