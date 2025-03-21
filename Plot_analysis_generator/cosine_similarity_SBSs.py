import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage

def cosine_similarity(matrix):
    """Compute the cosine similarity between rows of the given matrix."""
    norm_matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    return np.dot(norm_matrix, norm_matrix.T)

def plot_standard_heatmap(data, filename="standard_heatmap_sbs.png"):
    """Plot and save the standard heatmap."""
    plt.figure(figsize=(12, 12))
    sns.heatmap(data, cmap="coolwarm", xticklabels=True, yticklabels=True)
    plt.title("Standard Heatmap (SBSs)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Standard heatmap saved as {filename}")

def plot_clustered_heatmap(data, filename="clustered_cosine_similarity_heatmap.png"):
    """Plot and save the clustered heatmap with hierarchical clustering."""
    row_linkage = linkage(pdist(data, metric='euclidean'), method='ward')
    col_linkage = linkage(pdist(data.T, metric='euclidean'), method='ward')

    g = sns.clustermap(data, row_linkage=row_linkage, col_linkage=col_linkage,
                       cmap="coolwarm", figsize=(12, 12), xticklabels=True, yticklabels=True)

    g.ax_heatmap.set_xticklabels(g.ax_heatmap.get_xmajorticklabels(), rotation=90)
    plt.savefig(filename, dpi=300)
    print(f"Clustered heatmap saved as {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file> [--normalize]")
        sys.exit(1)

    file_path = sys.argv[1]
    normalize_data = "--normalize" in sys.argv  # Check if --normalize flag is passed

    # Read CSV file
    data = pd.read_csv(file_path, index_col=0)

    # Normalize the data if --normalize is used
    if normalize_data:
        data = pd.DataFrame(
            data.div(np.linalg.norm(data, axis=1, keepdims=True)),  # Normalize each row
            index=data.index, 
            columns=data.columns
        )
        print("Data has been normalized using L2 normalization.")
        print(data)

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(data)
    similarity_df = pd.DataFrame(similarity_matrix, index=data.index, columns=data.index)

    # Plot heatmaps
    plot_standard_heatmap(similarity_df)
    plot_clustered_heatmap(similarity_df)

if __name__ == "__main__":
    main()

