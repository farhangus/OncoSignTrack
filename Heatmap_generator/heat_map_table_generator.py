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

# Set up the figure
fig, ax = plt.subplots(figsize=(20, 12))

# Plot grid lines
ax.set_xticks(np.arange(-0.5, data.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-0.5, data.shape[0], 1), minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
ax.tick_params(which="minor", bottom=False, left=False)

# Plot circles representing values
max_value = data.max().max()
scale_factor = 250  # Adjust to control the circle size
min_circle_size = 10  # Set the minimum circle size
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        value = data.iloc[i, j]
        if value > 0:  # Only plot circles for non-zero values
            circle_size = max((value / max_value) * scale_factor, min_circle_size)
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

# Add a second row of labels for occurrence counts below the x-axis labels
for j, count in enumerate(occurrence_counts):
    ax.text(j, data.shape[0], f"{count}", ha="center", va="center", fontsize=8, color="black", rotation=90)

# Adjust the x-axis range to fit the counts below
ax.set_xlim(-0.5, data.shape[1] - 0.5)
ax.set_ylim(-0.5, data.shape[0] + 0.5)

# Add a colorbar for circle colors
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=plt.Normalize(vmin=0, vmax=max_value))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="vertical", label="Proportion Value", pad=0.05)

# Add a smaller legend for circle sizes and connect to paired colors
legend_sizes = np.linspace(0.1, 1.0, 10)  # 10 different proportion values
legend_labels = [f"{val:.1f}" for val in legend_sizes]
for size, label in zip(legend_sizes, legend_labels):
    plt.scatter(
        [],
        [],
        s=max((size / max_value) * scale_factor, min_circle_size),
        c=plt.cm.coolwarm(size),
        alpha=0.8,
        edgecolors="black",
        label=f"Proportion: {label}",
    )

# Tight layout to adjust spacing
plt.tight_layout()

# Show the plot
plt.savefig('heatmap_samples.png')
