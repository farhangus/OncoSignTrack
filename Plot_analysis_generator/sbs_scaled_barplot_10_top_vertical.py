import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os  # For handling file paths

# Check for command-line arguments
if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

# Read file path
file_path = sys.argv[1]

# Load CSV file
try:
    # Read only the first 3 columns of the input file
    data = pd.read_csv(file_path, usecols=[0, 1, 2])
    data.columns = ['Sample', 'Signature', 'Contribution']  # Assign proper labels
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Ensure 'Contribution' is numeric
data['Contribution'] = pd.to_numeric(data['Contribution'], errors='coerce')
data.dropna(subset=['Contribution'], inplace=True)

# Normalize contributions within each sample
data['Contribution'] = data.groupby('Sample')['Contribution'].transform(lambda x: (x / x.sum()) * 100)

# Find the top 10 signatures per sample
top_10_per_sample = (
    data.groupby('Sample')
    .apply(lambda group: group.nlargest(10, 'Contribution'))
    .reset_index(drop=True)
)

# Normalize contributions for the top 10 signatures to sum to 100% within each sample
top_10_per_sample['Contribution'] = top_10_per_sample.groupby('Sample')['Contribution'].transform(lambda x: (x / x.sum()) * 100)

# Pivot the data for the stacked bar plot
pivot_data = top_10_per_sample.pivot(index='Sample', columns='Signature', values='Contribution').fillna(0)

# Set figure size
plt.figure(figsize=(50, 10.8))

# Plot the 100% stacked barplot
ax = pivot_data.plot(
    kind='bar',
    stacked=True,
    colormap='tab20b',
    edgecolor='none',
    width=0.9,
    figsize=(25, 10.8)
)

# Customize the plot
plt.title("Scaled Contribution of Top 10 SBS Signatures per Sample (100% Scaled)", fontsize=14, pad=20)
plt.xlabel("Samples", fontsize=18, labelpad=10)
plt.ylabel("Contribution to Mutations (%)", fontsize=12, labelpad=10)
plt.xticks(rotation=90, fontsize=14, ha='center')
plt.yticks(fontsize=10)

# Customize legend: Smaller size
plt.legend(
    title="SBS Signature",
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    fontsize=14,
    title_fontsize=8,
    frameon=False
)

# Adjust layout to ensure everything fits
plt.tight_layout()

# Save the image in the same directory as the input file
output_dir = os.path.dirname(file_path)
output_file = os.path.join(output_dir, "top_10_sbs.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')

print(f"Plot saved at: {output_file}")
