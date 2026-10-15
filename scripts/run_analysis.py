from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.portfolio_analysis import load_data, validate_data
from src.visualization import create_portfolio_figure


def main() -> None:
    data_path = ROOT / "data" / "processed" / "ecosystem_values_2018_2023.csv"
    output_base = ROOT / "outputs" / "charts" / "portfolio_overview"
    data = load_data(data_path)
    checks = validate_data(data)
    outputs = create_portfolio_figure(data, output_base)
    print("Validation passed:")
    for key, value in checks.items():
        print(f"  {key}: {value}")
    print("Created:")
    for output in outputs:
        print(f"  {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
