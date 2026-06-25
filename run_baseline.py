"""Run the baseline simulation and save the results as a CSV file.

Usage:
    python run_baseline.py

Optional examples:
    python run_baseline.py --steps 100
    python run_baseline.py --steps 100 --output baseline_results.csv
"""

import argparse
import random
from pathlib import Path

import numpy as np

from model import FossilModel


def run_baseline(steps: int = 100, output: str = "baseline_results.csv", seed: int | None = None) -> Path:
    """Run the baseline model and save model-level results to a CSV file."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    model = FossilModel()

    for _ in range(steps):
        model.step()

    output_path = Path(output)
    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    model.df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the baseline coal-transition ABM and save results as CSV."
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100,
        help="Number of simulation steps. Default: 100.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="baseline_results.csv",
        help="Output CSV file path. Default: baseline_results.csv.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducibility.",
    )

    args = parser.parse_args()
    output_path = run_baseline(steps=args.steps, output=args.output, seed=args.seed)
    print(f"Baseline simulation completed. Results saved to: {output_path}")


if __name__ == "__main__":
    main()
