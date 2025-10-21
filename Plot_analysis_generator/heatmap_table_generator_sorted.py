import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import argparse

# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description="Plot a circle heatmap with optional threshold, SBS sorting, color scheme, exclusions, and log scale."
)
parser.add_argument("input_file", help="CSV input file")
parser.add_argument("--threshold", type=float, default=0.0, help="Minimum value to include (default: 0)")
parser.add_argument("--cell_size", type=float, default=5, help="Circle Size 1-10")
parser.add_argument("--sbs", type=str, default=None, help="Signature row to sort samples (columns) by")
parser.add_argument("--sep", type=int, default=22, help="Column index to separate groups (1-based index)")
parser.add_argument("--scheme", type=str, default="plasma", help="Matplotlib colormap name (e.g. plasma, viridis, bwr)")
parser.add_argument("--exclude", type=str, default="", help="Comma-separated SBS names to exclude (e.g., SBS5,SBS40 or 5,40)")
parser.add_argument("--log", action="store_true", help="If set, apply log10(value+1) to data before plotting")
parser.add_argument("--report", type=int, default=0, help="Report the SBS count per sample (0 = hide, 1 = show)")
args = parser.parse_args()

# --- Parameters ---
input_file = args.input_file
threshold = args.threshold
sort_sbs = args.sbs
cell_size = args.cell_size * 100.0  # scale to scatter 's' units
sep = args.sep - 0.5                # for plotting vline between groups
colormap = plt.get_cmap(args.scheme)
show_report = args.report == 1

# --- File and Output Setup ---
output_dir = os.path.dirname(os.path.abspath(input_file))

# --- Load data ---
data = pd.read_csv(input_file, index_col=0)

# --- Apply exclusions (accept '5' or 'SBS5') ---
if args.exclude:
    raw_excludes = [x.strip() for x in args.exclude.split(",") if x.strip()]
    excluded_sbs = [s if s.upper().startswith("SBS") else f"SBS{s}" for s in raw_excludes]
    data = data[~data.index.isin(excluded_sbs)]
    print(f"ℹ️ Excluded SBS rows: {excluded_sbs}")

# --- Optionally sort columns by a given SBS row ---
if sort_sbs is not None and sort_sbs in data.index:
    data = data.loc[:, data.loc[sort_sbs].sort_values(ascending=False).index]
else:
    print("ℹ️ No SBS sorting applied." if sort_sbs is None else f"⚠️ SBS '{sort_sbs}' not found; no sorting applied.")

# --- Keep only first 88 columns (as per original script) ---
data = data.iloc[:, :88]

# --- Clean & convert ---
data = data.sort_index()
data = data.replace("X", 1).replace("", 0).astype(float)

# --- Threshold & drop all-zero rows ---
data[data < threshold] = 0
data = data[(data != 0).any(axis=1)]

# --- Optional log transform ---
if args.log:
    print("ℹ️ Applying log10(value + 1) transformation.")
    data = np.log10(data + 1)

# --- Counts for the top margin labels ---
occurrence_counts = (data > 0).sum(axis=0)

# --- Min/max for color & size normalization ---
if not (data > 0).any().any():
    print("❌ No values above threshold to plot.")
    sys.exit(1)

min_value = data[data > 0].min().min()
max_value = data.max().max()

if pd.isna(min_value) or pd.isna(max_value) or max_value == 0:
    print("❌ No plottable values after preprocessing.")
    sys.exit(1)

# --- Legend tick values for circle sizes ---
size_values = np.linspace(min_value, max_value, 5)
size_labels = [f"{v:.2f}" for v in size_values]

# --- Plot Heatmap ---
fig, ax = plt.subplots(figsize=(20, 12))

# shaded group backgrounds
ax.axvspan(-0.5, sep, facecolor='lightcoral', alpha=0.15)
ax.axvspan(sep, data.shape[1] - 0.5, facecolor='lightblue', alpha=0.15)

# grid
ax.set_xticks(np.arange(-0.5, data.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, data.shape[0], 1), minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
ax.tick_params(which="minor", bottom=False, left=False)

# circles
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        value = data.iat[i, j]
        if value > 0:
            frac = value / max_value
            ax.scatter(
                j, i,
                s=frac * cell_size,
                c=colormap(frac),
                alpha=0.8,
                edgecolors="black",
                linewidths=0.3
            )

# split line
ax.axvline(x=sep, color='black', linestyle='--', linewidth=2)

# axes labels/ticks
ax.set_xticks(range(data.shape[1]))
ax.set_xticklabels(data.columns, rotation=90, fontsize=8)
ax.set_yticks(range(data.shape[0]))
ax.set_yticklabels(data.index, fontsize=8)
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")
ax.set_ylabel("Mutational Signatures (SBS)", fontsize=14)

# --- Optional SBS counts at the top ---
if show_report:
    print("ℹ️ Reporting SBS counts per sample above heatmap.")
    for j, count in enumerate(occurrence_counts):
        ax.text(j, data.shape[0], f"{count}", ha="center", va="center", fontsize=8, color="black", rotation=90)

ax.set_xlim(-0.5, data.shape[1] - 0.5)
ax.set_ylim(-0.5, data.shape[0] + (0.5 if show_report else 0))

# colorbar
label = "Proportion Value (log10+1)" if args.log else "Proportion Value"
sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=min_value, vmax=max_value))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="vertical", label=label, pad=0.05)

plt.tight_layout()
heatmap_path = os.path.join(output_dir, "heatmap_samples_with_counts.png")
plt.savefig(heatmap_path, dpi=300)
print(f"✅ Heatmap saved to: {heatmap_path}")

# --- Save circle-size legend as a separate image ---
fig_legend, ax_legend = plt.subplots(figsize=(3, 3))
handles = []
for size in size_values:
    frac = size / max_value
    h = ax_legend.scatter([], [], s=frac * cell_size  *.5, c=colormap(frac),
                          alpha=0.8, edgecolors="black", linewidths=0.3)
    handles.append(h)

legend = ax_legend.legend(
    handles,
    size_labels,
    title="Circle Size\n(Value)",
    frameon=True,
    loc="center",
    scatterpoints=1,
    labelspacing=0.5,   # tighten vertical space
    handletextpad=0.8,  # tighten text spacing
    borderpad=0.5,      # reduce padding inside box
    prop={'size': 8},   # smaller font
    title_fontsize=9    # smaller title font
)
ax_legend.set_axis_off()
legend_path = os.path.join(output_dir, "circle_size_legend.png")
fig_legend.savefig(legend_path, bbox_inches="tight", dpi=300)
plt.close(fig_legend)
print(f"✅ Circle size legend saved to: {legend_path}")
