from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from src.portfolio_analysis import (
    SERVICE_LABELS,
    SERVICE_ORDER,
    county_service_change,
    county_summary,
    regional_totals,
    service_summary,
)


PALETTE = {
    "navy": "#0F4D92",
    "blue": "#3775BA",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "red": "#B64342",
    "gray": "#CFCECE",
    "dark": "#272727",
}
SERVICE_COLORS = {
    "provisioning": "#8BCF8B",
    "water_retention": "#42949E",
    "carbon_storage": "#7884B4",
    "soil_retention": "#E9A6A1",
    "recreation": "#9A4D8E",
}


def apply_style() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["legend.frameon"] = False


def add_panel_label(ax, label: str) -> None:
    ax.text(
        -0.12,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def create_portfolio_figure(data, output_base: str | Path) -> list[Path]:
    """Create the four-panel portfolio overview and save PNG and editable SVG."""
    apply_style()
    output_base = Path(output_base)
    output_base.parent.mkdir(parents=True, exist_ok=True)

    totals = regional_totals(data)
    services = service_summary(data)
    counties = county_summary(data)
    heat = county_service_change(data)

    fig = plt.figure(figsize=(7.2, 6.4))
    grid = fig.add_gridspec(2, 2, height_ratios=[0.82, 1.18], hspace=0.72, wspace=0.88)
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    # a: headline regional total
    x = np.arange(2)
    values = totals["total_cny_billion"].to_numpy()
    bars = ax_a.bar(x, values, width=0.58, color=[PALETTE["gray"], PALETTE["navy"]])
    ax_a.set_xticks(x, totals["year"].astype(str))
    ax_a.set_ylabel("Estimated value (CNY billion)")
    ax_a.set_title("Regional total", loc="left", fontweight="bold")
    ax_a.set_ylim(0, 310)
    ax_a.grid(axis="y", color="#E6E6E6", linewidth=0.7)
    ax_a.set_axisbelow(True)
    for bar, value in zip(bars, values):
        ax_a.text(bar.get_x() + bar.get_width() / 2, value + 7, f"{value:.1f}", ha="center")
    pct = (values[1] / values[0] - 1) * 100
    ax_a.text(0.5, 292, f"+{pct:.2f}%", ha="center", color=PALETTE["navy"], fontweight="bold")
    add_panel_label(ax_a, "a")

    # b: service composition
    pivot = services.pivot(index="year", columns="service", values="value_cny_100m")
    left = np.zeros(2)
    for service in SERVICE_ORDER:
        vals = pivot[service].to_numpy() / 10
        ax_b.barh([0, 1], vals, left=left, color=SERVICE_COLORS[service], label=SERVICE_LABELS[service])
        left += vals
    ax_b.set_yticks([0, 1], ["2018", "2023"])
    ax_b.set_xlabel("Estimated value (CNY billion)")
    ax_b.set_title("Service composition", loc="left", fontweight="bold")
    ax_b.legend(loc="upper left", bbox_to_anchor=(0.0, -0.20), ncol=2, fontsize=6.2)
    ax_b.spines["left"].set_visible(False)
    ax_b.tick_params(axis="y", length=0)
    add_panel_label(ax_b, "b")

    # c: county change
    y = np.arange(len(counties))
    colors = [PALETTE["blue"] if v < 25 else PALETTE["navy"] for v in counties["change_pct"]]
    ax_c.barh(y, counties["change_pct"], color=colors, height=0.68)
    ax_c.set_yticks(y, counties.index)
    ax_c.set_xlabel("Change from 2018 to 2023 (%)")
    ax_c.set_title("County-level change", loc="left", fontweight="bold")
    ax_c.grid(axis="x", color="#E6E6E6", linewidth=0.7)
    ax_c.set_axisbelow(True)
    for yi, value in enumerate(counties["change_pct"]):
        ax_c.text(value + 0.8, yi, f"{value:.1f}", va="center", fontsize=6.5)
    ax_c.set_xlim(0, 52)
    add_panel_label(ax_c, "c")

    # d: county-service change heatmap
    matrix = heat.to_numpy()
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "change", ["#D7E5F5", "#FFFFFF", "#F3C4C0", "#B64342"]
    )
    norm = mcolors.TwoSlopeNorm(vmin=min(-40, float(matrix.min())), vcenter=0, vmax=max(90, float(matrix.max())))
    im = ax_d.imshow(matrix, aspect="auto", cmap=cmap, norm=norm)
    ax_d.set_xticks(np.arange(matrix.shape[1]), heat.columns, rotation=35, ha="right")
    ax_d.set_yticks(np.arange(matrix.shape[0]), heat.index)
    ax_d.set_title("Service change by county", loc="left", fontweight="bold")
    ax_d.tick_params(length=0)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            rgba = cmap(norm(value))
            luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
            label = "0" if abs(value) < 0.5 else f"{value:.0f}"
            ax_d.text(j, i, label, ha="center", va="center", fontsize=5.5, color="white" if luminance < 0.52 else PALETTE["dark"])
    cbar = fig.colorbar(im, ax=ax_d, location="right", shrink=0.68, pad=0.04, aspect=24)
    cbar.set_label("Change (%)")
    cbar.outline.set_visible(False)
    add_panel_label(ax_d, "d")

    fig.suptitle(
        "Ecosystem-service value increased, with uneven county gains",
        x=0.02,
        ha="left",
        fontsize=12,
        fontweight="bold",
    )
    fig.subplots_adjust(top=0.89, bottom=0.15, left=0.11, right=0.98)

    outputs = [output_base.with_suffix(".png"), output_base.with_suffix(".svg")]
    fig.savefig(outputs[0], dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(outputs[1], bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return outputs
