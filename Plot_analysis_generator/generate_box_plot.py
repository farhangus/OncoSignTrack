import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os  # For handling file paths
from matplotlib.ticker import ScalarFormatter

# Check for command-line arguments
if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

# Read the file path from the command line
file_path = sys.argv[1]

# Extract the directory of the input file
output_dir = os.path.dirname(file_path)

# Prompt the user for the dataset name
data_set_name = input("Enter the dataset name: ").strip()

# Load the CSV file
try:
    data = pd.read_csv(file_path, delimiter=",")  # Use delimiter if necessary
    data = pd.read_csv(file_path, usecols=[0, 1, 2])

    
    # Check the number of columns
    if data.shape[1] == 3:
        # Use only columns 2 and 3
        data = data.iloc[:, 1:3]
        data.columns = ['Signature', 'Contribution']
    elif data.shape[1] == 2:
        data.columns = ['Signature', 'Contribution']
    else:
        raise ValueError("The input file must have either 2 or 3 columns.")
    
except Exception as e:
    print(f"Error reading the file: {e}")
    sys.exit(1)

# Ensure 'Contribution' is numeric
data['Contribution'] = pd.to_numeric(data['Contribution'], errors='coerce')
data.dropna(subset=['Contribution'], inplace=True)

# Sort the data by mean contribution for better readability
data['Signature'] = pd.Categorical(
    data['Signature'],
    categories=data.groupby('Signature')['Contribution'].mean().sort_values(ascending=False).index
)
data.sort_values('Signature', inplace=True)

# Create the figure
plt.figure(figsize=(14, 7))

# Boxplot with color coding for contributions
sns.boxplot(
    x='Signature', 
    y='Contribution', 
    data=data, 
    palette='Set2', 
    showfliers=False
)  # Hide outliers for cleaner visualization

# Overlay a stripplot to show individual data points
sns.stripplot(
    x='Signature', 
    y='Contribution', 
    data=data, 
    color='black', 
    size=1.5, 
    jitter=True
)

# Add number of samples above each box (corrected sample count)
sample_counts = data.groupby('Signature')['Contribution'].count()
positions = range(len(sample_counts))

for pos, (signature, count) in zip(positions, sample_counts.items()):
    plt.text(
        pos, 
        data['Contribution'].max() * 1.05, 
        f'n={count}', 
        ha='center', 
        fontsize=8, 
        color='blue'
    )

# Customize the plot
plt.title(f'Box Plot of Contributions by Mutational Signature ({data_set_name} Samples)\n', fontsize=16)
plt.xlabel('Mutational Signatures (Sorted by Mean Contribution)', fontsize=12)
plt.ylabel('Contribution', fontsize=12)

# Add horizontal and vertical grids
plt.grid(axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Add median line to highlight the overall median contribution
overall_median = data['Contribution'].median()
plt.axhline(overall_median, color='green', linestyle='--', linewidth=1, label=f'Median: {overall_median:.2f}')
plt.legend()

# Customize the y-axis formatting to avoid scientific notation
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis='y', style='plain')

# Adjust layout
plt.tight_layout()

# Save the plot as an image in the same folder as the input file
output_file = os.path.join(output_dir, f'box_plot_{data_set_name.replace(" ", "_")}.png')
plt.savefig(output_file, dpi=800)

print(f"Plot saved at: {output_file}")
