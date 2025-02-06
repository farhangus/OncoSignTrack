import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import os

def plot_horizontal_bar(file_path, sample_name):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, sep=',')

    # Filter rows where Contribution is greater than 0
    df = df[df['Contribution'] > 0]
    df = df.sort_values(by='Contribution', ascending=False).reset_index(drop=True)

    # Extract relevant columns after filtering
    signatures = df['Signature']
    contributions = df['Contribution']

    # Calculate the total contribution
    total_contribution = contributions.sum()

    # Generate unique colors for each bar
    colors = plt.cm.tab20(np.linspace(0, 1, len(signatures)))

    # Plot horizontal bars
    plt.figure(figsize=(10, len(signatures) * 0.5))
    y_positions = range(len(signatures))

    # Plot each bar in a unique color
    for y, contribution, color in zip(y_positions, contributions, colors):
        plt.barh(y, contribution, color=color, edgecolor='black')

    # Annotate only the top 10 contributions
    for i, (y, contribution) in enumerate(zip(y_positions, contributions)):
        if i < 10:  # Annotate only the top 10
            plt.text(contribution + max(contributions) * 0.01, y, f"{int(contribution)}", va='center', fontsize=9)

    # Add a legend to display the total contribution and sample name
    plt.legend([f"Sample: {sample_name}\nTotal Contribution: {int(total_contribution)}"],
               loc="upper right", frameon=True, fontsize=10)

    # Add labels and title
    plt.yticks(y_positions, signatures)
    plt.xlabel('Contribution')
    plt.ylabel('Signatures')
    plt.title('Signatures and Contribution')
    plt.tight_layout()

    # Save the plot in the same directory as the input file
    output_file = os.path.join(os.path.dirname(file_path), f'{sample_name}_contribution_plot.png')
    plt.savefig(output_file, dpi=300)
    print(f"Plot saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot horizontal bar plot of signatures and contributions.")
    parser.add_argument("file", help="Path to the input file")
    parser.add_argument("sample", help="Sample name to include in the legend")
    args = parser.parse_args()

    plot_horizontal_bar(args.file, args.sample)
