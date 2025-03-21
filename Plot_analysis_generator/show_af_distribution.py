import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Check if file name is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <input_file.csv>")
    sys.exit(1)

# Read the input file
input_file = sys.argv[1]
data = pd.read_csv(input_file, header=None)  # Assuming a single-column CSV

# Convert data to numeric values
data = data.iloc[:, 0].dropna().astype(float)

# Define the number of bins
num_bins = 10

# Create histogram data
hist, bins = np.histogram(data, bins=num_bins, range=(data.min(), data.max()))

# Generate bar plot
plt.figure(figsize=(8, 6))
plt.bar(bins[:-1], hist, width=(bins[1] - bins[0]), edgecolor='black', align='edge')

# Set y-axis to normal numbers (not scientific notation)
plt.ticklabel_format(style='plain', axis='y')

# Label axes and title
plt.xlabel("Value Range")
plt.ylabel("Frequency")
plt.title("Bar Plot of Data Distribution")
plt.xticks(bins, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save and show plot
plt.savefig("bar_plot.png")
plt.show()

