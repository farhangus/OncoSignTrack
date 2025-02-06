#!/bin/bash

# Loop through all CSV files starting with '7316' and ending in '.csv'
for file in 7316*.csv; do
    
    base=$(echo $file| cut -d '.' -f 1 )
    
    echo -n "$base,"
    
    # Extract the base name (remove everything after the first dot)
    base=$(echo "$file" | cut -d '.' -f 1)
    
    # Construct the filtered file name
    filtered="filtered_${base}_mutational_signatures.csv"
    
    # Check if the filtered file exists
    if [[ -f "$filtered" ]]; then
        # Run the Python script to calculate cosine similarity
        python3 generate_cosine_sim.py "$file" "$filtered"
    else
        echo "Filtered file not found: $filtered. Skipping..."
    fi
done

echo "Processing completed for all files."

