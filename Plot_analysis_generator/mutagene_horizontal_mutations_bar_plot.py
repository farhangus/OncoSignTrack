import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import os

def plot_horizontal_bar(file_path, sample_name):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, sep='\t')

    # Sort by mutations in descending order
    df = df.sort_values(by='mutations', ascending=False)

    # Extract relevant columns
    signatures = df['signature']
    mutations = df['mutations']
    mutations_low = df['mutations_low']
    mutations_high = df['mutations_high']

    # Calculate the total number of mutations
    total_mutations = mutations.sum()

    # Generate unique colors for each bar
    colors = plt.cm.tab20(np.linspace(0, 1, len(signatures)))

    # Plot horizontal bars
    plt.figure(figsize=(10, len(signatures) * 0.5))
    y_positions = range(len(signatures))

    # Plot each bar in a unique color
    for y, mutation, low, high, color in zip(y_positions, mutations, mutations_low, mutations_high, colors):
        plt.barh(y, mutation, color=color, edgecolor='black')
        # Plot the mutation range as a line
        plt.plot([low, high], [y, y], color='red')

    # Annotate only the top 10 mutations
    for i, (y, mutation) in enumerate(zip(y_positions, mutations)):
        if i < 10:  # Annotate only the top 10
            plt.text(mutation + max(mutations) * 0.01, y, f"{mutation}", va='center', fontsize=9)

    # Add a legend to display the total number of mutations and sample name
    plt.legend([f"Sample: {sample_name}\nTotal Number of Signature Mutations: {int(total_mutations)}"],
               loc="upper right", frameon=True, fontsize=10)

    # Add labels and title
    plt.yticks(y_positions, signatures)
    plt.xlabel('Number of Mutations')
    plt.ylabel('Signatures')
    plt.title('Signatures and Mutation Ranges')
    plt.tight_layout()

    # Save the plot in the same directory as the input file
    output_file = os.path.join(os.path.dirname(file_path), f'{sample_name}_signatures_plot.png')
    plt.savefig(output_file, dpi=300)
    print(f"Plot saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot horizontal bar plot of signatures and mutations.")
    parser.add_argument("file", help="Path to the input file")
    parser.add_argument("sample", help="Sample name to include in the legend")
    args = parser.parse_args()

    plot_horizontal_bar(args.file, args.sample)
