#!/usr/bin/env python3
"""Clean-room exact-rational audit of the three h8NydU966G claims."""
import argparse
import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "main_algorithm.tex": "47c36490f628d8028364a8bee3c80862af4ed69ad680b921ddc0f0edafaa7a54",
    "consistency_robustness.tex": "4df60b9cecc995fc2d639f914809c31bd0b44146300ef1a9551632162ab1822f",
    "base_algorithm_with_proof.tex": "5a084a4919de80641caf48268e18f6d2a2cc78c2f7ff9742ad2ebdcd1f458a73",
}


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def tail(dist, time):
    return sum((p for day, p in dist.items() if day > time), Fraction())


def cost(dist, buy_after, buy_cost):
    if buy_after is None:
        return sum((day * p for day, p in dist.items()), Fraction())
    return sum((p * (day if day <= buy_after else buy_after + buy_cost) for day, p in dist.items()), Fraction())


def optimum(dist, buy_cost):
    infinite = cost(dist, None, buy_cost)
    finite = [(cost(dist, threshold, buy_cost), threshold) for threshold in range(max(dist) + 1)]
    best = min([infinite] + [value for value, _ in finite])
    if infinite == best and not any(value < infinite for value, _ in finite):
        return None, infinite
    return min((entry for entry in finite if entry[0] == best), key=lambda entry: entry[1])[1], best


def emd(left, right):
    return sum((abs(tail(left, t) - tail(right, t)) for t in range(max(max(left), max(right)))), Fraction())


def source_algorithm(prediction, buy_cost):
    root = math.isqrt(buy_cost)
    assert root * root == buy_cost
    khat, _ = optimum(prediction, buy_cost)
    u = next(t for t in range(max(prediction) + 1) if tail(prediction, t) <= Fraction(1, root))
    return (u + root if khat is None else min(khat + root, u + root)), khat, u


def hard_tail(buy_cost, cutoff, time):
    fast = Decimal(buy_cost - 2) / Decimal(buy_cost)
    if time <= cutoff:
        return fast ** time
    slow = Decimal(2 * buy_cost - 1) / Decimal(2 * buy_cost)
    return fast ** cutoff * slow ** (time - cutoff)


def hard_quantile(buy_cost, cutoff):
    root = math.isqrt(buy_cost)
    target = Decimal(1) / root
    # The tail is monotone. A binary search is exact while avoiding a
    # potentially enormous linear correction from a floating-point log guess.
    low, high = 0, cutoff
    while low < high:
        middle = (low + high) // 2
        if hard_tail(buy_cost, cutoff, middle) <= target:
            high = middle
        else:
            low = middle + 1
    return low


def slope(xs, ys):
    x, y = [math.log(float(v)) for v in xs], [math.log(float(v)) for v in ys]
    xbar, ybar = sum(x) / len(x), sum(y) / len(y)
    return sum((a - xbar) * (b - ybar) for a, b in zip(x, y)) / sum((a - xbar) ** 2 for a in x)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", default="outputs/independent_verification.json"); args = parser.parse_args()
    for relative, expected in PINS.items():
        actual = hashlib.sha256((ROOT / "source/arxiv" / relative).read_bytes()).hexdigest()
        assert actual == expected, (relative, actual)
    support, denominator = tuple(range(6)), 4
    distributions = [{day: Fraction(count, denominator) for day, count in zip(support, counts) if count} for counts in compositions(denominator, len(support))]
    tail_audit = {"distribution_pairs": len(distributions) ** 2, "cells": 0, "violations": 0, "minimum_slack": None}
    for predicted in distributions:
        for truth in distributions:
            distance = emd(predicted, truth)
            for start in range(5):
                for shift in range(1, 4):
                    slack = tail(predicted, start) + distance / shift - tail(truth, start + shift)
                    tail_audit["cells"] += 1; tail_audit["violations"] += int(slack < 0)
                    tail_audit["minimum_slack"] = slack if tail_audit["minimum_slack"] is None else min(tail_audit["minimum_slack"], slack)
    upper = {"cells": 0, "prediction_sensitive_max_ratio": 0., "robust_max_ratio": 0., "truncation_inequality_failures": 0, "tail_chain_failures": 0, "maximum_loss": 0.}
    for buy_cost in (4, 9, 16, 25, 36):
        root = math.isqrt(buy_cost)
        for predicted in distributions:
            threshold, khat, u = source_algorithm(predicted, buy_cost)
            base_threshold = u + root if khat is None else khat + root
            for truth in distributions:
                _, optimal_cost = optimum(truth, buy_cost)
                result_cost, distance = cost(truth, threshold, buy_cost), emd(predicted, truth)
                loss = result_cost - optimal_cost
                truncation = result_cost - cost(truth, base_threshold, buy_cost)
                truncation_bound = buy_cost * tail(truth, u + root)
                transported_bound = buy_cost * (tail(predicted, u) + distance / root)
                upper["cells"] += 1
                upper["prediction_sensitive_max_ratio"] = max(upper["prediction_sensitive_max_ratio"], float(loss / (root * max(distance, Fraction(1)))))
                upper["robust_max_ratio"] = max(upper["robust_max_ratio"], float(loss) / (buy_cost * math.log(buy_cost)))
                upper["truncation_inequality_failures"] += int(truncation > truncation_bound)
                upper["tail_chain_failures"] += int(truncation_bound > transported_bound)
                upper["maximum_loss"] = max(upper["maximum_loss"], float(loss))
    getcontext().prec = 90
    hard_rows = []
    for exponent in range(4, 21, 2):
        buy_cost, root = 2 ** exponent, 2 ** (exponent // 2)
        cutoff = math.ceil(Decimal(buy_cost) * Decimal(buy_cost).ln() / 2)
        quantile = hard_quantile(buy_cost, cutoff)
        threshold = min(cutoff + root, quantile + root)
        fast = Decimal(buy_cost - 2) / Decimal(buy_cost)
        threshold_cost = Decimal(buy_cost) / 2 + Decimal(buy_cost) * fast ** threshold / 2
        optimal_cost = Decimal(buy_cost) / 2 + Decimal(buy_cost) * fast ** cutoff / 2
        hard_rows.append({"b": buy_cost, "cutoff": cutoff, "u": quantile, "threshold": threshold, "consistency_loss": float(threshold_cost - optimal_cost), "consistency_over_sqrt_b": float((threshold_cost - optimal_cost) / root), "robustness_loss": float(threshold), "robustness_over_b_log_b": float(Decimal(threshold) / (Decimal(buy_cost) * Decimal(buy_cost).ln())), "quantile_valid": hard_tail(buy_cost, cutoff, quantile) <= Decimal(1) / root and (quantile == 0 or hard_tail(buy_cost, cutoff, quantile - 1) > Decimal(1) / root)})
    final_rows = hard_rows[-5:]
    hard = {"rows": hard_rows, "all_quantiles_valid": all(row["quantile_valid"] for row in hard_rows), "consistency_exponent_last_five": slope([row["b"] for row in final_rows], [row["consistency_loss"] for row in final_rows]), "robustness_exponent_vs_b_log_b_last_five": slope([row["b"] * math.log(row["b"]) for row in final_rows], [row["robustness_loss"] for row in final_rows])}
    # Strict-tail mutation and illegal eta-aware threshold mutation expose the two key interfaces.
    buy_cost, root = 256, 16
    prediction = {0: Fraction(root - 1, root), buy_cost - 1: Fraction(1, root)}
    threshold, khat, u = source_algorithm(prediction, buy_cost)
    strict_u = next(t for t in range(max(prediction) + 1) if tail(prediction, t) < Fraction(1, root))
    strict_threshold = strict_u + root if khat is None else min(khat + root, strict_u + root)
    truths = {"same": prediction, "short": {0: Fraction(1)}, "boundary": {buy_cost - 1: Fraction(1)}, "far": {buy_cost ** 3: Fraction(1)}}
    interface = {"source_khat_is_infinity": khat is None, "source_u": u, "strict_u": strict_u, "source_threshold": threshold, "strict_mutation_threshold": strict_threshold, "thresholds_by_truth": {}, "eta_aware_mutation_thresholds": {}}
    for name, truth in truths.items():
        interface["thresholds_by_truth"][name] = source_algorithm(prediction, buy_cost)[0]
        interface["eta_aware_mutation_thresholds"][name] = threshold + math.ceil(float(emd(prediction, truth)))
    assert tail_audit["violations"] == 0
    assert upper["truncation_inequality_failures"] == upper["tail_chain_failures"] == 0
    assert hard["all_quantiles_valid"] and .45 < hard["consistency_exponent_last_five"] < .55 and .95 < hard["robustness_exponent_vs_b_log_b_last_five"] < 1.05
    assert interface["source_khat_is_infinity"] and interface["source_u"] == 0 and interface["strict_u"] == 255 and interface["strict_mutation_threshold"] > 100
    assert len(set(interface["thresholds_by_truth"].values())) == 1 and len(set(interface["eta_aware_mutation_thresholds"].values())) > 1
    report = {"paper": "h8NydU966G", "claims": [{"id": "C1", "outcome": "verified", "finite_tail_lemma": tail_audit, "finite_algorithm_sweep": upper}, {"id": "C2", "outcome": "verified", "hard_family": hard}, {"id": "C3", "outcome": "verified", "prediction_error_independence": interface}]}
    path = ROOT / args.output; path.parent.mkdir(exist_ok=True); path.write_text(json.dumps(report, indent=2, default=str) + "\n"); print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
