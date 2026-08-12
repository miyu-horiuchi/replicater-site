#!/usr/bin/env python3
"""Redraw the Taxonomy Ceiling cosine-geometry figure for the replicater.xyz site.

Renders on the site's cream canvas with the Monet accent palette so the diagram
matches the page background and the other taxonomy-ceiling figures. Data are the
published cosine-kNN macro-F1 values by cosine-support tercile (Figure 6).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# replicater.xyz site palette (Monet)
CREAM = "#f4ecde"
SAGE = "#9bb29a"
DEEP = "#3a4a5c"
TERRA = "#cf8a63"
INK = "#2a2f3a"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#dccdb6",
    "grid.linewidth": 0.8,
    "figure.dpi": 200,
    "figure.facecolor": CREAM,
    "axes.facecolor": CREAM,
    "savefig.facecolor": CREAM,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.edgecolor": "#9a8f7c",
    "xtick.color": INK,
    "ytick.color": INK,
    "legend.frameon": False,
})


def fig_cosine_coverage():
    x = np.arange(3)
    bins = ["low\n(far)", "mid", "high\n(near)"]
    series = [
        ("catalase", [0.598, 0.685, 0.786], DEEP, "o"),
        ("motility", [0.580, 0.604, 0.687], TERRA, "s"),
        ("sporulation", [0.808, 0.787, 0.877], SAGE, "^"),
    ]
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    for name, vals, color, marker in series:
        ax.plot(x, vals, color=color, marker=marker, markersize=9,
                linewidth=2.4, markeredgecolor=INK, markeredgewidth=0.7,
                label=name, zorder=3, clip_on=False)
    ax.set_xticks(x)
    ax.set_xticklabels(bins)
    ax.set_xlim(-0.25, 2.25)
    ax.set_ylim(0.50, 0.92)
    ax.set_ylabel("Cosine kNN macro-F1, higher is better")
    ax.set_xlabel("Cosine support of held-out family (nearest training-family centroid)")
    ax.set_title("Family transfer improves with geometric coverage",
                 fontweight="bold")
    ax.grid(axis="x", visible=False)
    ax.legend(title="Trait", loc="lower right", fontsize=11, title_fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "taxonomy-ceiling-fig6-cosine-coverage.png"),
                bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)


if __name__ == "__main__":
    fig_cosine_coverage()
    print("Taxonomy web figure written to", HERE)
