import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def cosine_similarity(matrix):
    """Compute cosine similarity between rows of a matrix."""
    norm_matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    similarity_matrix = np.dot(norm_matrix, norm_matrix.T)
    return similarity_matrix

def report_sample_similarity(similarity_df, output_csv="sample_similarity_scores.csv"):
    """Save similarity scores for all sample pairs to a CSV file."""
    similarity_list = []
    
    for i in range(len(similarity_df)):
        for j in range(i + 1, len(similarity_df)):  # Avoid redundant pairs
            sample1 = similarity_df.index[i]
            sample2 = similarity_df.index[j]
            score = similarity_df.iloc[i, j]
            similarity_list.append([sample1, sample2, score])

    # Convert to DataFrame and save
    similarity_df_out = pd.DataFrame(similarity_list, columns=["Sample1", "Sample2", "Cosine_Similarity"])
    similarity_df_out.to_csv(output_csv, index=False)
    
    print(f"\nSimilarity scores saved to: {output_csv}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    # Load data
    file_path = sys.argv[1]
    df = pd.read_csv(file_path, index_col=0)

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(df)
    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

    # Save and report similarity scores
    report_sample_similarity(similarity_df)

if __name__ == "__main__":
    main()

