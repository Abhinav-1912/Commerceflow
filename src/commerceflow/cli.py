from __future__ import annotations

import argparse
import json

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CommerceFlow local pipeline")
    parser.add_argument("--transactions", type=int, default=1000, help="Number of synthetic transactions")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    result = run_pipeline(transaction_count=args.transactions, seed=args.seed)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
