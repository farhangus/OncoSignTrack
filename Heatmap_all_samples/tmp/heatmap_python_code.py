import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Function to generate the heatmap
def generate_heatmap(file_path):
    # Load the data from the specified file
    df = pd.read_csv(file_path, header=None, names=["Sample", "Signature", "Value"])

    # Pivot the data to create a matrix for the heatmap
    heatmap_data = df.pivot(index="Signature", columns="Sample", values="Value")

    # Fill missing values with 0
    heatmap_data.fillna(0, inplace=True)

    # Normalize each column by dividing by the column sum
    normalized_data = heatmap_data.div(heatmap_data.sum(axis=0), axis=1)

    # Calculate row-wise sums (Signature-wise sums)
    row_sums = heatmap_data.sum(axis=1)

    # Plot the heatmap and the row sums
    fig, ax = plt.subplots(figsize=(12, 6), ncols=2, gridspec_kw={'width_ratios': [4, 1]})

    # Heatmap on the left
    sns.heatmap(normalized_data, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True, linewidths=0.5, ax=ax[0])
    ax[0].set_title("Normalized Heatmap (Column-wise)")
    ax[0].set_ylabel("Signature")
    ax[0].set_xlabel("Sample")

    # Row sums bar plot on the right
    sns.barplot(y=row_sums.index, x=row_sums.values, orient='h', ax=ax[1], palette="YlGnBu")
    ax[1].set_title("Row Sums")
    ax[1].set_xlabel("Sum")
    ax[1].set_ylabel("")  # No need for a label as it corresponds to the same y-axis

    # Adjust layout
    plt.tight_layout()
    plt.savefig('sample_heatmap.png')

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Generate a normalized heatmap with row sums from a CSV file.")
    parser.add_argument("file", type=str, help="Path to the CSV file containing the data.")
    args = parser.parse_args()

    # Generate the heatmap
    generate_heatmap(args.file)

if __name__ == "__main__":
    main()

