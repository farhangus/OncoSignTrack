import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Function to generate the heatmap
def generate_heatmap(file_path):
    # Load the data from the specified file
    df = pd.read_csv(file_path, header=None, names=["Sample", "Signature", "Value"])

    # Disable scientific notation in pandas
    pd.options.display.float_format = '{:.0f}'.format

    # Pivot the data to create a matrix for the heatmap
    heatmap_data = df.pivot(index="Signature", columns="Sample", values="Value")

    # Fill missing values with 0
    heatmap_data.fillna(0, inplace=True)

    # Calculate row-wise sums (Signature-wise sums)
    row_sums = heatmap_data.sum(axis=1)

    # Add a row for the column sums at the bottom
    column_sums = heatmap_data.sum(axis=0)
    column_sums_df = pd.DataFrame(column_sums).T  # Convert to DataFrame and transpose

    # Concatenate the column_sums row to the heatmap_data
    heatmap_data = pd.concat([heatmap_data, column_sums_df], ignore_index=False)

    # Sort heatmap_data by row sums (including the new 'Column Sums' row)
    heatmap_data = heatmap_data.loc[row_sums.sort_values(ascending=False).index]
    
    # Plot and save the heatmap
    plt.figure(figsize=(18, 12))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar=True, linewidths=0.5)
    plt.title("Heatmap of Signatures Across Samples (Sorted by Row Sum)")
    plt.ylabel("Signature")
    plt.xlabel("Samples")
    plt.tight_layout()
    plt.savefig("heatmap.png")  # Save the heatmap as an image
    plt.close()

    # Plot and save the row sums bar plot
    plt.figure(figsize=(8, 8))
    sns.barplot(y=row_sums.loc[heatmap_data.index[:-1]].index, x=row_sums.loc[heatmap_data.index[:-1]].values, orient='h', palette="RdYlBu")
    plt.title("Row Sums")
    plt.xlabel("Sum")
    plt.ylabel("")  # No need for a label as it corresponds to the same y-axis
    plt.tight_layout()
    plt.savefig("row_sums.png")  # Save the row sums plot as an image
    plt.close()

    # Plot and save the column sums bar plot
    plt.figure(figsize=(24, 12))
    sns.barplot(x=column_sums.index, y=column_sums.values, palette="YlGnBu")
    plt.title("Column Sums")
    plt.xlabel("Samples")
    plt.ylabel("Sum")
    # Add annotations to the column sums bars
    for p in plt.gca().patches:
        plt.gca().annotate(f'{p.get_height():.0f}', 
                           (p.get_x() + p.get_width() / 2., p.get_height()), 
                           ha='center', va='center', fontsize=8, color='black', 
                           xytext=(0, 10), textcoords='offset points', rotation=90)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("column_sums.png")  # Save the column sums plot as an image
    plt.close()

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Generate a heatmap with row and column sums from a CSV file.")
    parser.add_argument("file", type=str, help="Path to the CSV file containing the data.")
    args = parser.parse_args()

    # Generate the heatmap
    generate_heatmap(args.file)

if __name__ == "__main__":
    main()
