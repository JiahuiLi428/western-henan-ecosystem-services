from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

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


def create_readme_hero(data, output_base: str | Path) -> list[Path]:
    """Create an English, data-driven water-retention comparison for GitHub."""
    apply_style()
    output_base = Path(output_base)
    output_base.parent.mkdir(parents=True, exist_ok=True)

    water = data.loc[data["service"].astype(str).eq("water_retention")]
    wide = water.pivot(index="county", columns="year", values="value_cny_100m")
    wide["change_pct"] = (wide[2023] / wide[2018] - 1) * 100
    wide = wide.sort_values(2023, ascending=False)

    total_2018 = float(wide[2018].sum())
    total_2023 = float(wide[2023].sum())
    regional_change = (total_2023 / total_2018 - 1) * 100
    increased = int(wide["change_pct"].gt(0).sum())
    growth_leaders = wide.sort_values("change_pct", ascending=False).head(3)

    navy = "#17324D"
    blue = "#247BA0"
    aqua = "#52A9B5"
    slate = "#8D99A6"
    pale = "#E7EEF2"

    fig = plt.figure(figsize=(14.2, 7.4), facecolor="white")
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=[3.2, 1.15],
        left=0.08,
        right=0.96,
        bottom=0.14,
        top=0.76,
        wspace=0.13,
    )

    ax = fig.add_subplot(grid[0, 0])
    positions = np.arange(len(wide))
    for y, (_, row) in zip(positions, wide.iterrows()):
        ax.plot([row[2018], row[2023]], [y, y], color=aqua, linewidth=3.4, alpha=0.78, solid_capstyle="round")
        ax.scatter(row[2018], y, s=70, facecolor="white", edgecolor=slate, linewidth=1.8, zorder=3)
        ax.scatter(row[2023], y, s=80, facecolor=blue, edgecolor="white", linewidth=0.9, zorder=4)
        ax.text(row[2023] + 0.10, y, f"+{row['change_pct']:.1f}%", va="center", color=blue, fontsize=8.2, fontweight="bold")

    county_labels = [county.replace(" County", "") for county in wide.index]
    ax.set_yticks(positions, labels=county_labels)
    ax.invert_yaxis()
    ax.set_xlim(0.25, 4.15)
    ax.set_xticks(np.arange(0.5, 4.1, 0.5))
    ax.set_xlabel("Estimated water-retention value (RMB 100 million)", color="#4F5B66", labelpad=10)
    ax.grid(axis="x", color=pale, linewidth=1)
    ax.tick_params(axis="y", length=0, pad=8, labelcolor=navy)
    ax.tick_params(axis="x", colors="#65727E")
    for spine in ax.spines.values():
        spine.set_visible(False)

    legend = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor=slate, markeredgewidth=1.7, markersize=7, label="2018"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=blue, markeredgecolor="white", markersize=8, label="2023"),
    ]
    ax.legend(handles=legend, loc="lower left", bbox_to_anchor=(0, 1.03), ncol=2, handletextpad=0.5, columnspacing=1.5)

    info = fig.add_subplot(grid[0, 1])
    info.set_xlim(0, 1)
    info.set_ylim(0, 1)
    info.axis("off")
    info.axvline(0.02, color=pale, linewidth=1.2)
    info.text(0.12, 0.97, "AT A GLANCE", color="#6B7782", fontsize=9, fontweight="bold", va="top")
    info.text(0.12, 0.80, f"{increased} / 11", color=blue, fontsize=31, fontweight="bold", va="center")
    info.text(0.12, 0.72, "counties increased", color=navy, fontsize=11, fontweight="bold")

    info.text(0.12, 0.54, f"{total_2018 / 10:.2f}", color=slate, fontsize=18, fontweight="bold")
    info.text(0.50, 0.54, "→", color="#87929C", fontsize=18, ha="center", fontweight="bold")
    info.text(0.88, 0.54, f"{total_2023 / 10:.2f}", color=blue, fontsize=18, ha="right", fontweight="bold")
    info.text(0.12, 0.47, "regional total (RMB billion)", color="#6B7782", fontsize=9)
    info.text(0.12, 0.36, f"+{regional_change:.1f}%", color=aqua, fontsize=23, fontweight="bold")
    info.text(0.12, 0.29, "overall change", color=navy, fontsize=9.5, fontweight="bold")

    info.text(0.12, 0.205, "FASTEST GROWTH", color="#6B7782", fontsize=8.5, fontweight="bold")
    leader_lines = [
        f"{county.replace(' County', '')}  +{row['change_pct']:.1f}%"
        for county, row in growth_leaders.iterrows()
    ]
    info.text(0.12, 0.145, "\n".join(leader_lines), color=navy, fontsize=8.7, linespacing=1.45, va="top")

    fig.text(0.08, 0.925, "Water-retention value increased across all 11 counties", color=navy, fontsize=24, fontweight="bold")
    fig.text(0.08, 0.865, "Model-estimated values for mountainous western Henan, 2018–2023", color="#5F6B75", fontsize=12)
    fig.text(
        0.08,
        0.04,
        "Each line links the same county across time; percentages show relative change. Values are model-derived, not market transactions.",
        color="#6B7782",
        fontsize=8.5,
    )

    outputs = [output_base.with_suffix(".png"), output_base.with_suffix(".svg")]
    fig.savefig(outputs[0], dpi=220, bbox_inches="tight", facecolor="white", metadata={"Software": "matplotlib"})
    fig.savefig(outputs[1], bbox_inches="tight", facecolor="white", metadata={"Date": None})
    plt.close(fig)
    return outputs


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
