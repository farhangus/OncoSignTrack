import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

def main():
    # Check for arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file> [--annotate] [--normalize]")
        sys.exit(1)

    file_path = sys.argv[1]
    annotate = "--annotate" in sys.argv  # Check if --annotate flag is passed
    normalize_data = "--normalize" in sys.argv  # Check if --normalize flag is passed

    # Read CSV file
    data = pd.read_csv(file_path, index_col=0)
    print(data.round(0).astype(int))

    # Normalize the data if --normalize is used
    if normalize_data:
        data = pd.DataFrame(
            normalize(data, axis=1, norm="l2"),  # Normalize each row
            index=data.index, 
            columns=data.columns
        )
        print("Data has been normalized using L2 normalization.")
        print(data)

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(data.T)
    similarity_df = pd.DataFrame(similarity_matrix, index=data.columns, columns=data.columns)

    # Generate cluster map
    g = sns.clustermap(
        similarity_df, 
        cmap="coolwarm", 
        method="ward", 
        figsize=(12, 12), 
        annot=annotate,  # Enable annotation if --annotate is used
        fmt=".2f" if annotate else None,  # Format annotation values if enabled
        annot_kws={"size": 8} if annotate else None  # Set annotation text size
    )

    # Save the clustered heatmap
    plt.savefig("clustered_cosine_similarity_heatmap_samples.png", dpi=800)
    print("Clustered heatmap saved as clustered_cosine_similarity_heatmap.png")


if __name__ == "__main__":
    main()

