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

# Create the boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(x='Signature', y='Contribution', data=data)

# Customize the plot
plt.title('Box Plot of Contributions by Mutational Signature HGG AF<0.30', fontsize=16)
plt.xlabel('Signature', fontsize=12)
plt.ylabel('Contribution', fontsize=12)
plt.xticks(rotation=90)

# Show the plot
plt.tight_layout()
plt.show()

