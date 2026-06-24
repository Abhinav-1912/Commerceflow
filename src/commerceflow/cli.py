from __future__ import annotations

import argparse
import json

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CommerceFlow transaction pipeline")
    parser.add_argument(
        "--config",
        default="config/local.example.json",
        help="Path to pipeline config JSON",
    )
    args = parser.parse_args()

    result = run_pipeline(args.config, create_sample_if_missing=True)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
