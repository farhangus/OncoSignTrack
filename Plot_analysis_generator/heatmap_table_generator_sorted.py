import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Read the input file from the command line
input_file = sys.argv[1]

# Get the directory where the input file is located
output_dir = os.path.dirname(os.path.abspath(input_file))

# Load your data into a DataFrame
data = pd.read_csv(input_file, index_col=0)

# Sort rows alphabetically by the index
data = data.sort_index()

# Convert data to numeric for plotting
data = data.replace("X", 1).replace("", 0).astype(float)

# Calculate occurrence counts for each column
occurrence_counts = (data > 0).sum(axis=0)

# Calculate the min and max values for scaling
min_value = data[data > 0].min().min()
max_value = data.max().max()

# Create proportional sizes for legend
size_values = np.linspace(min_value, max_value, 5)
size_labels = [f"{round(size)}" for size in size_values]

# Create heatmap figure
fig, ax = plt.subplots(figsize=(20, 12))

# Add background shading for sample groups
ax.axvspan(-0.5, 21.5, facecolor='lightcoral', alpha=0.15)  # First group: samples 0-21
ax.axvspan(21.5, data.shape[1] - 0.5, facecolor='lightblue', alpha=0.15)  # Second group: samples 22+

# Add minor grid lines
ax.set_xticks(np.arange(-0.5, data.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, data.shape[0], 1), minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
ax.tick_params(which="minor", bottom=False, left=False)

# Plot each non-zero cell as a circle
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        value = data.iloc[i, j]
        if value > 0:
            circle_size = (value / max_value) * 650
            ax.scatter(
                j, i, s=circle_size, c=plt.cm.coolwarm(value / max_value),
                alpha=0.8, edgecolors="black"
            )

# Add vertical separator line after 22nd sample
ax.axvline(x=21.5, color='black', linestyle='--', linewidth=2)

# Customize axis labels
ax.set_xticks(range(data.shape[1]))
ax.set_xticklabels(data.columns, rotation=90, fontsize=8)
ax.set_yticks(range(data.shape[0]))
ax.set_yticklabels(data.index, fontsize=8)

# Move x-axis labels to top
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")
ax.set_ylabel("Mutational Signatures (SBS)", fontsize=14)

# Add SBS occurrence counts below x-axis
for j, count in enumerate(occurrence_counts):
    ax.text(j, data.shape[0], f"{count}", ha="center", va="center", fontsize=8, color="black", rotation=90)

# Adjust plot limits
ax.set_xlim(-0.5, data.shape[1] - 0.5)
ax.set_ylim(-0.5, data.shape[0] + 0.5)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=plt.Normalize(vmin=0, vmax=max_value))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="vertical", label="Proportion Value", pad=0.05)

plt.tight_layout()

# Save main heatmap
heatmap_path = os.path.join(output_dir, 'heatmap_samples_with_counts.png')
plt.savefig(heatmap_path)
print(f"✅ Heatmap saved to: {heatmap_path}")

# Create circle size legend
fig_legend, ax_legend = plt.subplots(figsize=(2, 4))
size_handles = [
    ax_legend.scatter([], [], s=(size / max_value) * 350,
                      color=plt.cm.coolwarm(size / max_value),
                      alpha=0.8, edgecolors="black")
    for size in size_values
]
ax_legend.legend(
    size_handles, size_labels,
    loc="center", title="Circle Size\n(Value)",
    fontsize=10, title_fontsize=10,
    frameon=True, shadow=False,
    labelspacing=.7, handletextpad=.01
)
ax_legend.axis("off")

# Save legend
legend_path = os.path.join(output_dir, 'circle_size_legend_with_colors.png')
plt.tight_layout()
plt.savefig(legend_path)
print(f"✅ Legend saved to: {legend_path}")
