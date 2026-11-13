#!/usr/bin/env python
"""Test wrapper to run evaluation via pytest."""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate import evaluate


def test_evaluation():
    """Run the full evaluation and assert minimum metrics."""
    evaluate()


if __name__ == "__main__":
    test_evaluation()
