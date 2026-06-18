#!/usr/bin/env python3
"""Redraw the HMM-gated PLM benchmark bar charts for the replicater.xyz site.

Renders on the site's cream canvas with the Monet accent palette so the
diagrams match the page background and read more colourfully than the
black/grey print versions. Data are the published benchmark numbers.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))

# replicater.xyz site palette (Monet)
CREAM = "#f4ecde"
SKY = "#b8c9d8"
LAVENDER = "#c2b6cf"
ROSE = "#e6b9ae"
SAGE = "#9bb29a"
DEEP = "#3a4a5c"
SLATE2 = "#5b7184"
TERRA = "#cf8a63"
INK = "#2a2f3a"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 12,
    "axes.titlesize": 12,
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
})

EDGE = "#7d7363"


def hbar(ax, labels, vals, colors, fmt, xlim, hatched=None):
    """labels/vals given top-to-bottom; plotted with the top row highest."""
    n = len(labels)
    y = np.arange(n)[::-1]  # row 0 at top
    bars = ax.barh(y, vals, color=colors, edgecolor=EDGE, linewidth=1.0,
                   height=0.62, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(*xlim)
    ax.grid(axis="y", visible=False)
    for yi, v, lab in zip(y, vals, labels):
        if hatched and lab in hatched:
            continue
        ax.text(v + (xlim[1] - xlim[0]) * 0.012, yi, fmt(v),
                va="center", ha="left", fontsize=10.5, color=INK)
    return bars


def fig_temperature():
    labels = ["This work (+PTPE)", "This work (pre-PTPE)",
              "Koblitz 2025", "GenomeSPOT"]
    vals = [2.67, 2.74, 2.94, 4.39]
    colors = [DEEP, SLATE2, SKY, LAVENDER]
    fig, ax = plt.subplots(figsize=(8.2, 3.1))
    hbar(ax, labels, vals, colors, lambda v: f"{v:.2f} \u00b0C", (0, 5.0))
    ax.set_xlabel("Optimum temperature MAE (\u00b0C), lower is better")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "hmm-gated-fig2-temperature.png"),
                bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)


def fig_oxygen():
    labels = ["This work, LoRA", "This work, tabular", "This work, pre-PTPE",
              "GenomeSPOT", "Koblitz 2025"]
    vals = [0.945, 0.402, 0.412, 0.0, 0.0]
    colors = [DEEP, SLATE2, SAGE, "none", "none"]
    hatched = {"GenomeSPOT", "Koblitz 2025"}
    notes = {"GenomeSPOT": "binary tolerant / not-tolerant, different label space",
             "Koblitz 2025": "binary aerobe / anaerobe, different label space"}
    fig, ax = plt.subplots(figsize=(8.2, 3.4))
    n = len(labels)
    y = np.arange(n)[::-1]
    for yi, v, c, lab in zip(y, vals, colors, labels):
        if lab in hatched:
            ax.barh(yi, 0.06, color="none", edgecolor="#9a8f7c",
                    hatch="////", linewidth=1.0, height=0.62, zorder=3)
            ax.text(0.09, yi, notes[lab], va="center", ha="left",
                    fontsize=10, color="#6f6657", style="italic")
        else:
            ax.barh(yi, v, color=c, edgecolor=EDGE, linewidth=1.0,
                    height=0.62, zorder=3)
            ax.text(v + 0.012, yi, f"{v:.3f}", va="center", ha="left",
                    fontsize=10.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, 1.05)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Oxygen requirement macro-F1 (4-class), higher is better")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "hmm-gated-fig3-oxygen.png"),
                bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)


def fig_medium():
    labels = ["XGBoost recommender (this work)", "Taxonomic popularity",
              "Global popularity"]
    vals = [0.775, 0.372, 0.366]
    colors = [DEEP, SKY, LAVENDER]
    fig, ax = plt.subplots(figsize=(8.2, 2.7))
    hbar(ax, labels, vals, colors, lambda v: f"{v*100:.1f}%", (0, 1.0))
    ax.set_xlabel("Medium recommender Hit@5, 5-fold family-heldout, higher is better")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "hmm-gated-fig4-medium.png"),
                bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)


if __name__ == "__main__":
    fig_temperature()
    fig_oxygen()
    fig_medium()
    print("HMM web figures written to", HERE)
