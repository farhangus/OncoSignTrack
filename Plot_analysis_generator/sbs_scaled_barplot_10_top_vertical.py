import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Check for command-line arguments
if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

# Read file path
file_path = sys.argv[1]

# Load CSV file
try:
    data = pd.read_csv(file_path, usecols=[0, 1, 2])
    data.columns = ['Sample', 'Signature', 'Contribution']
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Ensure 'Contribution' is numeric
data['Contribution'] = pd.to_numeric(data['Contribution'], errors='coerce')
data.dropna(subset=['Contribution'], inplace=True)

# Normalize contributions within each sample
data['Contribution'] = data.groupby('Sample')['Contribution'].transform(lambda x: (x / x.sum()) * 100)

# Find top 10 signatures per sample
top_10_per_sample = (
    data.groupby('Sample')
    .apply(lambda group: group.nlargest(10, 'Contribution'))
    .reset_index(drop=True)
)

# Normalize again to 100% within top 10
top_10_per_sample['Contribution'] = top_10_per_sample.groupby('Sample')['Contribution'].transform(lambda x: (x / x.sum()) * 100)

# Save top 10 to CSV
output_dir = os.path.dirname(file_path)
csv_output_file = os.path.join(output_dir, "top_10_sbs_scaled_percent.csv")
top_10_per_sample.to_csv(csv_output_file, index=False)
print(f"✅ CSV file saved at: {csv_output_file}")

# Pivot for plot
pivot_data = top_10_per_sample.pivot(index='Sample', columns='Signature', values='Contribution').fillna(0)

# === Save plot without legend ===
fig, ax = plt.subplots(figsize=(25, 10.8))
bars = pivot_data.plot(kind='bar', stacked=True, colormap='tab20b', edgecolor='none', ax=ax, width=0.9)

# Annotate SBS names inside the bars if the height is sufficient
for i, patch_list in enumerate(bars.containers):
    signature_name = pivot_data.columns[i]
    for bar in patch_list:
        height = bar.get_height()
        if height > 5:  # Only annotate if height is significant
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_y() + height / 2,
                signature_name,
                ha='center',
                va='center',
                fontsize=6,
                rotation='vertical',
                color='white'
            )

ax.set_title("Scaled Contribution of Top 10 SBS Signatures per Sample (100% Scaled)", fontsize=14, pad=20)
ax.set_xlabel("Samples", fontsize=18)
ax.set_ylabel("Contribution to Mutations (%)", fontsize=12)
ax.tick_params(axis='x', rotation=90, labelsize=14)
ax.tick_params(axis='y', labelsize=10)
ax.legend_.remove()
plt.tight_layout()

plot_output_file = os.path.join(output_dir, "top_10_sbs.png")
plt.savefig(plot_output_file, dpi=300, bbox_inches='tight')
print(f"✅ Plot saved at: {plot_output_file}")

# === Save legend as separate file ===
fig_legend = plt.figure(figsize=(6, 10))
handles, labels = bars.get_legend_handles_labels()
fig_legend.legend(handles, labels, loc='center', frameon=False, fontsize=12, title="SBS Signature", title_fontsize=14)
legend_output_file = os.path.join(output_dir, "top_10_sbs_legend.png")
fig_legend.savefig(legend_output_file, dpi=300, bbox_inches='tight')
print(f"✅ Legend saved at: {legend_output_file}")
