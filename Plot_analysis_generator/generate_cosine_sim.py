import sys
import pandas as pd
import numpy as np
from numpy.linalg import norm

# Function to calculate cosine similarity
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    magnitude = norm(vector1) * norm(vector2)
    return dot_product / magnitude if magnitude != 0 else 0

# Ensure two file paths are provided as command-line arguments
if len(sys.argv) != 3:
    print("Usage: python script_name.py <file1.csv> <file2.csv>")
    sys.exit(1)

# Read file paths from command-line arguments
file1_path = sys.argv[1]
file2_path = sys.argv[2]

# Load the CSV files into dataframes
data1 = pd.read_csv(file1_path)
data2 = pd.read_csv(file2_path)

# Ensure both files have the same set of signatures
data1 = data1.set_index("Signature").sort_index()
data2 = data2.set_index("Signature").sort_index()

if not data1.index.equals(data2.index):
    print("Error: Signature sets in the two files do not match.")
    sys.exit(1)

# Extract contribution values as vectors
vector1 = data1["Contribution"].values
vector2 = data2["Contribution"].values

# Calculate cosine similarity
similarity = cosine_similarity(vector1, vector2)

# Print the result
print(f"{similarity:.4f}")
