import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
    heatmap_data.fillna(0, inplace=False)

    # Calculate row-wise sums (Signature-wise sums)
    row_sums = heatmap_data.sum(axis=1)

    # Add a row for the column sums at the bottom
    column_sums = heatmap_data.sum(axis=0)
    column_sums_df = pd.DataFrame(column_sums).T  # Convert to DataFrame and transpose

    # Concatenate the column_sums row to the heatmap_data
    heatmap_data = pd.concat([heatmap_data, column_sums_df], ignore_index=False)

    # Sort heatmap_data by row sums (including the new 'Column Sums' row)
    heatmap_data = heatmap_data.loc[row_sums.sort_values(ascending=False).index]

    # Custom colormap: Set 0 values to black
    cmap = sns.color_palette("YlGnBu", as_cmap=True)
    cmap.set_under("black")

    # Plot the heatmap and the row sums
    fig, ax = plt.subplots(figsize=(36,12), ncols=3, gridspec_kw={'width_ratios': [4, 1, 1]})

    # Heatmap on the left
    sns.heatmap(heatmap_data, annot=False, fmt=".0f", cmap=cmap, cbar=True, linewidths=0.5, ax=ax[0], vmin=0.1)
    ax[0].set_title("Heatmap of Signatures Across Samples (Sorted by Row Sum)  AF <.30")
    ax[0].set_ylabel("Signature")
    ax[0].set_xlabel("Samples")

    # Row sums bar plot in the middle
    sns.barplot(y=row_sums.loc[heatmap_data.index[:-1]].index, x=row_sums.loc[heatmap_data.index[:-1]].values, orient='h', ax=ax[1], palette="RdYlBu")
    ax[1].set_title("Row Sums")
    ax[1].set_xlabel("Sum")
    ax[1].set_ylabel("")  # No need for a label as it corresponds to the same y-axis
# Ensure x-axis tick labels display normal values and are horizontal
    ax[1].set_xticklabels(ax[1].get_xticks(), rotation=90, fontsize=10)

    # Optional: Manually adjust padding for better spacing
    plt.subplots_adjust(right=0.85)  # Increase this to create more space on the right side

    # Column sums bar plot on the right
    sns.barplot(x=column_sums.index, y=column_sums.values, ax=ax[2], palette="YlGnBu")
    ax[2].set_title("Column Sums")
    ax[2].set_xlabel("Samples")
    ax[2].set_ylabel("Sum")

    # Add annotations to the column sums bars
    # for p in ax[2].patches:
    #     ax[2].annotate(f'{p.get_height():.0f}', 
    #                    (p.get_x() + p.get_width() / 2., p.get_height()), 
    #                    ha='center', va='center', fontsize=8, color='black', 
    #                    xytext=(0, 10), textcoords='offset points', rotation=90)

    # Rotate x-axis labels to make them vertical
    ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=90, fontsize=4)

    # Save the figure
    plt.tight_layout()
    plt.savefig("heatmap_with_black_cells.jpg", dpi=300)
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
