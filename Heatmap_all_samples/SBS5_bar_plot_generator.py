import pandas as pd
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
import numpy as np

# Function to generate a single sorted boxplot without outliers but with jittered dots
def generate_sorted_combined_boxplot(file_path):
    # Load the data from the file
    df = pd.read_csv(file_path, header=None, names=["Sample", "Signature", "Value"])

    # Convert the Value column to numeric (in case it's read as a string)
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    print(df)
    # Calculate the maximum value for each sample
    max_values = df.groupby("Sample")["Value"].max()

    # Sort the sample names by their maximum value in descending order
    sorted_samples = max_values.sort_values(ascending=False).index

    # Reorder the dataframe based on the sorted sample names
    df["Sample"] = pd.Categorical(df["Sample"], categories=sorted_samples, ordered=True)
    df = df.sort_values("Sample")

    # Set a unique color for each sample
    num_samples = len(sorted_samples)
    colors = sns.color_palette("husl", num_samples)  # Use Seaborn color palette

    # Create the boxplot
    plt.figure(figsize=(16, 10))  # Set the figure size

    # Generate boxplots without outliers and with jittered dots
    for i, sample in enumerate(sorted_samples):
        data = df[df["Sample"] == sample]["Value"]

        # Boxplot without outliers
        plt.boxplot(
            data,
            positions=[i],
            widths=0.6,  # Increase the width of the box
            patch_artist=True,
            boxprops=dict(facecolor=colors[i], edgecolor="black", linewidth=2),
            showfliers=False,  # Remove the outliers
        )

        # Add jittered individual data points as smaller filled black dots
        x_coords = np.random.normal(loc=i, scale=0.05, size=len(data))  # Add jitter for dots
        plt.scatter(x_coords, data, color="black", s=20, alpha=0.8, zorder=3)

    # Customize the plot
    plt.title("Box Plot of Values for All Sample Types SBS5 (Sorted by Max Value)", fontsize=18)
    plt.xlabel("Sample Type", fontsize=14)
    plt.ylabel("Value", fontsize=14)
    plt.xticks(range(num_samples), sorted_samples, rotation=45, fontsize=12)  # Add sample names as x-ticks
    plt.tight_layout()

    # Save the plot
    plt.savefig("sorted_combined_boxplot_without_outliers.png", dpi=300)  # Save the figure
    plt.show()

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Generate a combined sorted boxplot for all sample types without outliers but with jittered black dots.")
    parser.add_argument("file", type=str, help="Path to the CSV file containing the data.")
    args = parser.parse_args()

    # Generate the sorted combined boxplot
    generate_sorted_combined_boxplot(args.file)

if __name__ == "__main__":
    main()
