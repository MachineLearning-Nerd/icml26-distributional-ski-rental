from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from verify_ski_rental import emd, source_algorithm, tail


def test_earth_mover_distance_for_point_shift():
    assert emd({1: Fraction(1)}, {4: Fraction(1)}) == 3


def test_source_threshold_uses_non_strict_tail_boundary():
    b, root = 256, 16
    prediction = {0: Fraction(root - 1, root), b - 1: Fraction(1, root)}
    threshold, khat, u = source_algorithm(prediction, b)
    assert khat is None and u == 0 and threshold == root
    assert tail(prediction, 0) == Fraction(1, root)


def test_prediction_only_threshold_is_truth_independent():
    b, root = 256, 16
    prediction = {0: Fraction(root - 1, root), b - 1: Fraction(1, root)}
    baseline = source_algorithm(prediction, b)[0]
    assert baseline == source_algorithm(prediction, b)[0]
    assert baseline == 16


def test_full_exact_audit_output_is_present():
    import json
    root = Path(__file__).resolve().parents[2]
    result = json.loads((root / "outputs/independent_verification.json").read_text())
    assert [claim["outcome"] for claim in result["claims"]] == ["verified"] * 3
    assert result["claims"][0]["finite_algorithm_sweep"]["cells"] == 79380
