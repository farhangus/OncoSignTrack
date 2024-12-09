import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from matplotlib.ticker import ScalarFormatter

# Check for command-line arguments
if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

# Read the file path from the command line
file_path = sys.argv[1]

# Load the CSV file
try:
    data = pd.read_csv(file_path, delimiter=",")  # Use delimiter if necessary
    # Ensure column names are correct
    data.columns = ['Signature', 'Contribution']
except Exception as e:
    print(f"Error reading the file: {e}")
    sys.exit(1)

# Sort the data by mean contribution for better readability
data['Signature'] = pd.Categorical(
    data['Signature'],
    categories=data.groupby('Signature')['Contribution'].mean().sort_values(ascending=False).index
)
data.sort_values('Signature', inplace=True)

# Create the figure
plt.figure(figsize=(14, 7))

# Set the y-axis explicitly to linear scale
plt.yscale('linear')

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

# Add number of samples above each box
sample_counts = data['Signature'].value_counts()
positions = range(len(sample_counts))
for pos, count in zip(positions, sample_counts):
    plt.text(pos, data['Contribution'].max() * 1.2, f'n={count}', ha='center', fontsize=8, color='blue')

# Customize the plot
plt.title('Box Plot of Contributions by Mutational Signature \n', fontsize=16)
plt.xlabel('Mutational Signatures (Sorted by Mean Contribution)', fontsize=12)
plt.ylabel('Contribution', fontsize=12)

# Add horizontal and vertical grids
plt.grid(axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Add median line to highlight the overall median contribution
overall_median = data['Contribution'].median()
plt.axhline(overall_median, color='green', linestyle='--', linewidth=1, label=f'Median: {overall_median:.2f}')
plt.axhline(overall_median, color='green', linestyle='', linewidth=1, label=f'Total Number of Samples: {sample_counts.sum()}')
plt.legend()

# Customize the y-axis formatting to avoid scientific notation
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis='y', style='plain')

# Adjust layout
plt.tight_layout()

# Save the plot as an image
plt.savefig('box_plot.png', dpi=800)
