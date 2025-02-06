import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

# Read the input file from the command line
input_file = sys.argv[1]

# Load your data into a DataFrame
data = pd.read_csv(input_file, index_col=0)

# Sort rows alphabetically by the index
data = data.sort_index()

# Convert data to numeric for plotting
data = data.replace("X", 1).replace("", 0).astype(float)

# Calculate occurrence counts for each column
occurrence_counts = (data > 0).sum(axis=0)

# Calculate the minimum and maximum values in the data for scaling
min_value = data[data > 0].min().min()  # Smallest non-zero value
max_value = data.max().max()  # Largest value

# Generate size values for the legend proportionally between min_value and max_value
size_values = np.linspace(min_value, max_value, 5)  # Adjust the number of legend circles (5 here)

# Create labels for the legend (only values)
size_labels = [f"{round(size)}" for size in size_values]

# Set up the figure for the main heatmap
fig, ax = plt.subplots(figsize=(20, 12))

# Plot grid lines
ax.set_xticks(np.arange(-0.5, data.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, data.shape[0], 1), minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
ax.tick_params(which="minor", bottom=False, left=False)

# Plot circles representing values
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        value = data.iloc[i, j]
        if value > 0:  # Only plot for non-zero values
            circle_size = (value / max_value) * 250
            ax.scatter(
                j, i, s=circle_size, c=plt.cm.coolwarm(value / max_value), alpha=0.8, edgecolors="black"
            )

# Customize axis labels
ax.set_xticks(range(data.shape[1]))
ax.set_xticklabels(data.columns, rotation=90, fontsize=8)
ax.set_yticks(range(data.shape[0]))
ax.set_yticklabels(data.index, fontsize=8)

# Move x-axis labels to the top
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")

# Add axis titles
ax.set_ylabel("Mutational Signatures (SBS)", fontsize=14)

# Add the number of SBS occurrences below each sample on the x-axis
for j, count in enumerate(occurrence_counts):
    ax.text(j, data.shape[0], f"{count}", ha="center", va="center", fontsize=8, color="black", rotation=90)

# Adjust the x-axis range to fit the counts below
ax.set_xlim(-0.5, data.shape[1] - 0.5)
ax.set_ylim(-0.5, data.shape[0] + 0.5)

# Add a colorbar for circle colors
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=plt.Normalize(vmin=0, vmax=max_value))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="vertical", label="Proportion Value", pad=0.05)

# Tight layout to adjust spacing
plt.tight_layout()

# Save the main heatmap plot
plt.savefig('heatmap_samples_with_counts.png')

# Create a separate figure for the circle size legend
fig_legend, ax_legend = plt.subplots(figsize=(4, 4))

# Create legend handles with scaled sizes and matching colors
size_handles = [
    ax_legend.scatter(
        [], [],
        s=(size / max_value) * 250,
        color=plt.cm.coolwarm(size / max_value),
        alpha=0.8,
        edgecolors="black"
    )
    for size in size_values
]

# Add the legend to the separate figure
ax_legend.legend(
    size_handles,
    size_labels,
    loc="center",
    title="Circle Size\n(Value)",
    fontsize=10,
    title_fontsize=10,
    frameon=True,
    shadow=False,
)
ax_legend.axis("off")  # Hide axes for the legend figure

# Save the circle size legend as a separate image
plt.tight_layout()
plt.savefig('circle_size_legend_with_colors.png')
