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
    data = pd.read_csv(file_path)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Ensure columns are correct
data.columns = ['Sample', 'Signature', 'Contribution']

# Remove ".vcf.gz" from Sample names
data['Sample'] = data['Sample'].str.replace(r'\.vcf\.gz$', '', regex=True)

# Calculate total contribution for each sample to normalize contributions
data['Contribution'] = data.groupby('Sample')['Contribution'].transform(lambda x: (x / x.sum()) * 100)

# Pivot the data to create a table for stacked bar plot
pivot_data = data.pivot(index='Sample', columns='Signature', values='Contribution').fillna(0)

# Manually set figure size (close to 1920x1080 resolution or adjust as needed)
plt.figure(figsize=(25, 10.8))  # Figure size in inches (width, height)

# Plot the 100% stacked barplot
pivot_data.plot(
    kind='bar', 
    stacked=True, 
    colormap='tab20b', 
    edgecolor='none',
    width=0.9,

)

# Customize the plot
plt.title("Scaled Contribution of Each SBS Signature per Sample", fontsize=14, pad=20)
plt.xlabel("Samples", fontsize=7, labelpad=10)
plt.ylabel("Contribution to Mutations (%)", fontsize=12, labelpad=10)
plt.xticks(rotation=90, fontsize=4, ha='center')
plt.yticks(fontsize=10)

# Customize legend: Smaller size
plt.legend(
    title="SBS Signature", 
    bbox_to_anchor=(1.05, 1), 
    loc='upper left', 
    fontsize=6, 
    title_fontsize=8, 
    frameon=False
)

# Adjust layout to ensure everything fits
plt.tight_layout()

# Save the image in the same directory as the input file
output_dir = os.path.dirname(file_path)
output_file = os.path.join(output_dir, "sbs_stacked_percentage_barplot_adjusted.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')

print(f"Plot saved at: {output_file}")

