#!/usr/bin/env python3
"""Fail-closed gate for the three scoped ski-rental claims."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "repro/src/cumulative_science_gate.py")],
        cwd=ROOT,
        check=True,
    )
    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "repro/tests"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(tests.returncode == 0, tests.stdout + tests.stderr)
    subprocess.run(
        [sys.executable, str(ROOT / "repro/src/build_evidence_bundle.py")],
        cwd=ROOT,
        check=True,
    )

    cumulative = json.loads((ROOT / "outputs/CUMULATIVE_SCIENCE_GATE.json").read_text())
    bundle = ROOT / "outputs/evidence_bundle.jsonl"
    rows = [json.loads(line) for line in bundle.read_text().splitlines() if line]
    expected = {
        "README.md",
        "STATUS.md",
        "sources.json",
        "repro/requirements.txt",
        "repro/src/verify_ski_rental.py",
        "repro/src/build_evidence_bundle.py",
        "repro/src/cumulative_science_gate.py",
        "repro/src/publication_gate.py",
        "repro/tests/test_verifier.py",
        "source/arxiv/main.tex",
        "source/arxiv/main_algorithm.tex",
        "source/arxiv/consistency_robustness.tex",
        "source/arxiv/base_algorithm_with_proof.tex",
        "outputs/independent_verification.json",
        "docs/CLAIM_AUDIT.md",
        "docs/BRANCH_AUDIT.md",
        "docs/PUBLICATION_GATE.md",
        "docs/SOURCE_AUDIT.md",
        "outputs/README.md",
    }
    require({row["path"] for row in rows} == expected, "evidence bundle paths changed")
    for row in rows:
        path = ROOT / row["path"]
        require(path.is_file() and path.stat().st_size == row["bytes"], f"bad bundle record: {row['path']}")
        require(digest(path) == row["sha256"], f"bundle hash mismatch: {row['path']}")
    require(cumulative["status"] == "SCOPED_PASS", "cumulative gate failed")
    require(cumulative["strict_status"] == "SCOPED_PASS", "strict scoped status changed")
    for relative in ("README.md", "STATUS.md", "docs/PUBLICATION_GATE.md", "outputs/CUMULATIVE_SCIENCE_GATE.json"):
        require("FULL_GATE_READY" not in (ROOT / relative).read_text(), f"stale full-ready marker: {relative}")

    payload = {
        "paper": "h8NydU966G",
        "gate_version": "scoped-v2",
        "status": "SCOPED_PASS",
        "strict_status": "SCOPED_PASS",
        "overall_status": "VERIFIED_SCOPED",
        "tests_passed": True,
        "publication_gate_passed": True,
        "claims": cumulative["claims"],
        "evidence_bundle_sha256": digest(bundle),
        "source_anchor_sha256": cumulative["source_anchor_sha256"],
        "score_forecast": None,
    }
    for relative in ("publication_gate.json", "outputs/publication_gate.json"):
        (ROOT / relative).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
