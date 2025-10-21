import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from matplotlib.ticker import ScalarFormatter

# --- Check for command-line arguments ---
if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

# --- Read the file path ---
file_path = sys.argv[1]
output_dir = os.path.dirname(file_path)
data_set_name = ""

# --- Load the CSV file ---
try:
    data = pd.read_csv(file_path, usecols=[0, 1, 2])
    data.columns = ['File', 'Signature', 'Contribution']
except Exception as e:
    print(f"Error reading the file: {e}")
    sys.exit(1)

# --- Ensure 'Contribution' is numeric ---
data['Contribution'] = pd.to_numeric(data['Contribution'], errors='coerce')
data.dropna(subset=['Contribution'], inplace=True)

# --- ✅ Remove signatures with all-zero contributions ---
data = data.groupby('Signature').filter(lambda x: (x['Contribution'] > 0).any())

# --- Sort signatures by mean contribution ---
data['Signature'] = pd.Categorical(
    data['Signature'],
    categories=data.groupby('Signature')['Contribution'].mean().sort_values(ascending=False).index
)
data.sort_values('Signature', inplace=True)

# --- Create the figure ---
plt.figure(figsize=(14, 7))

# --- Boxplot ---
sns.boxplot(
    x='Signature',
    y='Contribution',
    data=data,
    palette='Set2',
    showfliers=False
)

# --- Overlay data points ---
sns.stripplot(
    x='Signature',
    y='Contribution',
    data=data,
    color='black',
    size=1.5,
    jitter=True
)

# --- Count unique samples with nonzero contribution per signature ---
nonzero_data = data[data['Contribution'] > 0]
sample_counts = nonzero_data.groupby('Signature')['File'].nunique()
positions = range(len(sample_counts))

# --- Display counts vertically above boxes ---
y_offset = data['Contribution'].max() * 1.05
for pos, (signature, count) in zip(positions, sample_counts.items()):
    plt.text(
        pos,
        y_offset,
        f'n={count}',
        ha='center',
        va='bottom',
        fontsize=8,
        color='blue',
        rotation=90
    )

# --- Customize the plot ---
plt.title(f'Box Plot of Contributions by Mutational Signature ({data_set_name} Samples)\n', fontsize=16)
plt.xlabel('Mutational Signatures (Sorted by Mean Contribution)', fontsize=12)
plt.ylabel('Contribution', fontsize=12)
plt.grid(axis='both', linestyle='--', linewidth=0.7, alpha=0.7)
plt.xticks(rotation=90)

# --- Add overall median line ---
overall_median = data['Contribution'].median()
plt.axhline(overall_median, color='green', linestyle='--', linewidth=1, label=f'Median: {overall_median:.2f}')
plt.legend()

# --- Format y-axis ---
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(axis='y', style='plain')

plt.tight_layout()

# --- Save plot ---
output_file = os.path.join(output_dir, f'box_plot_{data_set_name.replace(" ", "_")}.png')
plt.savefig(output_file, dpi=800)

print(f"✅ Plot saved at: {output_file}")
