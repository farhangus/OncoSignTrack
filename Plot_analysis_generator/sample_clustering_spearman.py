import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage
import numpy as np
import os

def spearman_sample_clustering(input_file, output_prefix="sample_spearman"):
    # Load and transpose the data
    df = pd.read_csv(input_file, index_col=0)
    df = df.T  # Now samples are rows

    # Compute Spearman correlation matrix
    corr, _ = spearmanr(df, axis=1)
    corr_df = pd.DataFrame(corr, index=df.index, columns=df.index)

    # Save the correlation matrix
    corr_df.to_csv(f"{output_prefix}_correlation_matrix.csv")
    print(f"✅ Correlation matrix saved as {output_prefix}_correlation_matrix.csv")

    # Convert correlation to distance for clustering
    distance = 1 - corr_df
    row_linkage = linkage(squareform(distance, checks=False), method='ward')

    # Create clustered heatmap
    sns.set(style="white")
    g = sns.clustermap(
        corr_df,
        row_linkage=row_linkage,
        col_linkage=row_linkage,
        cmap="coolwarm",
        figsize=(15, 15),
        xticklabels=True,
        yticklabels=True,
        linewidths=0.5,
        annot=False
    )

    g.ax_heatmap.set_xticklabels(g.ax_heatmap.get_xmajorticklabels(), rotation=90)
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), rotation=0)
    
    output_img = f"{output_prefix}_heatmap.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"✅ Heatmap saved as {output_img}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample clustering using Spearman correlation.")
    parser.add_argument("--input", required=True, help="CSV file with SBSs as rows and samples as columns.")
    args = parser.parse_args()

    spearman_sample_clustering(args.input)

