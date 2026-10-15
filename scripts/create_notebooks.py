from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


SETUP = """from pathlib import Path
import sys

ROOT = Path.cwd()
if ROOT.name == 'notebooks':
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from src.portfolio_analysis import load_data

DATA_PATH = ROOT / 'data' / 'processed' / 'ecosystem_values_2018_2023.csv'
data = load_data(DATA_PATH)
data.head()
"""


def write_notebook(path: Path, title: str, introduction: str, cells: list) -> None:
    notebook = nbf.v4.new_notebook()
    notebook["cells"] = [
        nbf.v4.new_markdown_cell(f"# {title}\n\n{introduction}"),
        nbf.v4.new_code_cell(SETUP),
        *cells,
    ]
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.12"},
    }
    nbf.write(notebook, path)


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)

    write_notebook(
        NOTEBOOKS / "01_data_validation.ipynb",
        "01 Data validation",
        "Validate the public processed table before any analysis. The checks deliberately recompute totals from county-service records rather than trusting source summary cells.",
        [
            nbf.v4.new_code_cell(
                """from src.portfolio_analysis import regional_totals, validate_data

checks = validate_data(data)
checks
"""
            ),
            nbf.v4.new_code_cell(
                """key_counts = {
    'years': data['year'].nunique(),
    'counties': data['county'].nunique(),
    'services': data['service'].nunique(),
    'duplicate_keys': int(data.duplicated(['year', 'county', 'service']).sum()),
    'missing_values': int(data.isna().sum().sum()),
}
key_counts
"""
            ),
            nbf.v4.new_code_cell(
                """totals = regional_totals(data)
totals.assign(
    rounded_cny_100m=totals['total_cny_100m'].round(2),
    rounded_cny_billion=totals['total_cny_billion'].round(2),
)
"""
            ),
            nbf.v4.new_markdown_cell(
                "The corrected 2023 total is 2,696.03 CNY 100 million (CNY 269.60 billion). All structural and unit checks must pass before the next notebooks run."
            ),
        ],
    )

    write_notebook(
        NOTEBOOKS / "02_temporal_comparison.ipynb",
        "02 Temporal comparison",
        "Compare regional totals and service composition between 2018 and 2023. Only two observations are available, so this is a two-point comparison rather than a trend model.",
        [
            nbf.v4.new_code_cell(
                """from src.portfolio_analysis import regional_totals, service_summary, validate_data

validate_data(data)
totals = regional_totals(data)
services = service_summary(data)

regional_change = (totals.loc[totals['year'].eq(2023), 'total_cny_100m'].iloc[0] /
                   totals.loc[totals['year'].eq(2018), 'total_cny_100m'].iloc[0] - 1) * 100
print(f'Regional change: {regional_change:.2f}%')
"""
            ),
            nbf.v4.new_code_cell(
                """service_wide = services.pivot(index='service', columns='year', values='value_cny_100m')
service_wide['change_pct'] = (service_wide[2023] / service_wide[2018] - 1) * 100
service_wide['share_2023_pct'] = services.loc[services['year'].eq(2023)].set_index('service')['share_pct']
service_wide.round(2)
"""
            ),
            nbf.v4.new_code_cell(
                """from IPython.display import Image, display
from src.visualization import create_portfolio_figure

output_base = ROOT / 'outputs' / 'charts' / 'portfolio_overview'
create_portfolio_figure(data, output_base)
display(Image(filename=str(output_base.with_suffix('.png'))))
"""
            ),
        ],
    )

    write_notebook(
        NOTEBOOKS / "03_county_comparison.ipynb",
        "03 County comparison",
        "Examine variation across the 11 county units. The heatmap compares county-service change but is intentionally not presented as a geographic map.",
        [
            nbf.v4.new_code_cell(
                """from src.portfolio_analysis import county_service_change, county_summary, validate_data

validate_data(data)
counties = county_summary(data)
heat = county_service_change(data)
counties.round(2)
"""
            ),
            nbf.v4.new_code_cell(
                """import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from src.visualization import PALETTE, apply_style

apply_style()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5.2), gridspec_kw={'width_ratios': [0.85, 1.25]})

y = np.arange(len(counties))
ax1.barh(y, counties['change_pct'], color=PALETTE['navy'])
ax1.set_yticks(y, counties.index)
ax1.set_xlabel('Change from 2018 to 2023 (%)')
ax1.set_title('County total', loc='left', fontweight='bold')
ax1.grid(axis='x', color='#E6E6E6', linewidth=0.7)
ax1.set_axisbelow(True)

matrix = heat.to_numpy()
cmap = mcolors.LinearSegmentedColormap.from_list('change', ['#D7E5F5', '#FFFFFF', '#F3C4C0', '#B64342'])
norm = mcolors.TwoSlopeNorm(vmin=min(-40, float(matrix.min())), vcenter=0, vmax=max(90, float(matrix.max())))
image = ax2.imshow(matrix, aspect='auto', cmap=cmap, norm=norm)
ax2.set_xticks(np.arange(matrix.shape[1]), heat.columns, rotation=35, ha='right')
ax2.set_yticks(np.arange(matrix.shape[0]), heat.index)
ax2.set_title('Service change', loc='left', fontweight='bold')
ax2.tick_params(length=0)
colorbar = fig.colorbar(image, ax=ax2, location='bottom', shrink=0.75, pad=0.18)
colorbar.set_label('Change (%)')
colorbar.outline.set_visible(False)

fig.tight_layout()
output_base = ROOT / 'outputs' / 'charts' / 'county_comparison'
fig.savefig(output_base.with_suffix('.png'), dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig(output_base.with_suffix('.svg'), bbox_inches='tight', facecolor='white')
plt.close(fig)

from IPython.display import Image, display
display(Image(filename=str(output_base.with_suffix('.png'))))
"""
            ),
            nbf.v4.new_markdown_cell(
                "Luanchuan, Lushi, and Neixiang record the largest total increases. Lushan records the smallest aggregate increase, while some of its individual services decline."
            ),
        ],
    )

    print(f"Created three notebooks in {NOTEBOOKS}")


if __name__ == "__main__":
    main()
