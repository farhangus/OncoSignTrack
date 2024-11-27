import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Check for command-line arguments
if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

# Read the file path from the command line
file_path = sys.argv[1]

# Load the CSV file
try:
    data = pd.read_csv(file_path, delimiter="\t")  # Use delimiter if necessary
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

# Boxplot with color coding for contributions
sns.boxplot(
    x='Signature', 
    y='Contribution', 
    data=data, 
    palette='coolwarm', 
    showfliers=False
)  # Hide outliers for cleaner visualization

# Overlay a stripplot to show individual data points
sns.stripplot(
    x='Signature', 
    y='Contribution', 
    data=data, 
    color='black', 
    size=3, 
    jitter=True
)

# Add number of samples above each box
sample_counts = data['Signature'].value_counts()
positions = range(len(sample_counts))
for pos, count in zip(positions, sample_counts):
    plt.text(pos, data['Contribution'].max() * 1.2, f'n={count}', ha='center', fontsize=8, color='blue')

# #Add annotations for the top 3 signatures
# top_signatures = data.groupby('Signature')['Contribution'].mean().nlargest(3)
# for pos, (signature, mean_value) in enumerate(top_signatures.items()):
#     plt.annotate(
#         f"Top: {mean_value:.1f}",
#         xy=(pos, mean_value),
#         xytext=(0, 15),
#         textcoords='offset points',
#         arrowprops=dict(arrowstyle="->", color='red'),
#         fontsize=9,
#         color='red',
#         ha='center'
#     )

# Customize the plot
plt.title('Box Plot of Contributions by Mutational Signature HGG AF<0.30\n', fontsize=16)
plt.xlabel('Mutational Signatures (Sorted by Mean Contribution)', fontsize=12)
plt.ylabel('Contribution (Log Scale)', fontsize=12)

# Add horizontal and vertical grids
plt.grid(axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

# Set the y-axis to a logarithmic scale for better visualization

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Add median line to highlight the overall median contribution
overall_median = data['Contribution'].median()
plt.axhline(overall_median, color='green', linestyle='--', linewidth=1, label=f'Median: {overall_median:.2f}')
plt.legend()

# Adjust layout
plt.tight_layout()

# Show the plot
plt.savefig('box_plot.png')

