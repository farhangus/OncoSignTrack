import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 your_script.py somatic_sbs_raw.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = os.path.dirname(os.path.abspath(input_file))

    # Load your data
    data = pd.read_csv(input_file, index_col=0)
    data = data.sort_index()
    data = data.replace("X", 1).replace("", 0).astype(float)

    # Apply log(1+x) transformation
    data = np.log1p(data)

    # ➡️ Save the log-transformed data to CSV
    log_csv_path = os.path.join(output_dir, 'log_transformed_data.csv')
    data.to_csv(log_csv_path)
    print(f"✅ Log-transformed CSV saved to: {log_csv_path}")

    # Count how many SBS are present in each sample
    occurrence_counts = (data > 0).sum(axis=0)

    # Determine color and size scaling
    min_value = data[data > 0].min().min()
    max_value = data.max().max()
    size_values = np.linspace(min_value, max_value, 10)
    size_labels = [f"{round(v, 2)}" for v in size_values]

    # Create main heatmap
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_xticks(np.arange(-0.5, data.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, data.shape[0], 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data.iloc[i, j]
            if value > 0:
                circle_size = (value / max_value) * 250
                ax.scatter(
                    j, i,
                    s=circle_size,
                    c=plt.cm.coolwarm(value / max_value),
                    alpha=0.8,
                    edgecolors="black"
                )

    ax.set_xticks(range(data.shape[1]))
    ax.set_xticklabels(data.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(data.shape[0]))
    ax.set_yticklabels(data.index, fontsize=8)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("Mutational Signatures (SBS)", fontsize=14)

    for j, count in enumerate(occurrence_counts):
        ax.text(
            j, data.shape[0], f"{count}",
            ha="center", va="center",
            fontsize=8, color="black", rotation=90
        )

    ax.set_xlim(-0.5, data.shape[1] - 0.5)
    ax.set_ylim(-0.5, data.shape[0] + 0.5)

    sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=plt.Normalize(vmin=0, vmax=max_value))
    sm.set_array([])
    fig.colorbar(sm, ax=ax, orientation="vertical", label="Log-Transformed Value", pad=0.05)

    plt.tight_layout()
    heatmap_path = os.path.join(output_dir, 'log_heatmap_samples_with_counts.png')
    plt.savefig(heatmap_path)
    print(f"✅ Heatmap saved to: {heatmap_path}")

    # Create the legend separately
    fig_legend, ax_legend = plt.subplots(figsize=(4, 4))
    size_handles = [
        ax_legend.scatter(
            [], [],
            s=(s / max_value) * 200,
            color=plt.cm.coolwarm(s / max_value),
            alpha=0.8,
            edgecolors="black"
        )
        for s in size_values
    ]
    ax_legend.legend(
        size_handles, size_labels,
        loc="center", title="Circle Size\n(Log Value)",
        fontsize=10, title_fontsize=10, frameon=True
    )
    ax_legend.axis("off")

    legend_path = os.path.join(output_dir, 'log_circle_size_legend_with_colors.png')
    plt.tight_layout()
    plt.savefig(legend_path)
    print(f"✅ Legend saved to: {legend_path}")

if __name__ == "__main__":
    main()
