#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file="$1"

# Extract unique sample names and print the header
samples=$(tail -n +2 "$input_file" | awk -F',' '{print $1}' | sort -u | tr '\n' ',' | sed 's/,$//')
echo "Signature,$samples"

# Generate the table with integer values from the Contribution column
tail -n +2 "$input_file" | gawk -F',' '
BEGIN {
    split("'"$samples"'", sample_array, ",");
    for (i in sample_array) {
        samples[sample_array[i]] = sample_array[i];
    }
}
{
    # Convert Contribution to integer using int()
    table[$2][$1] = int($3);
    signatures[$2] = $2;
}
END {
    for (sig in signatures) {
        printf "%s", sig;
        for (i in sample_array) {
            sample = sample_array[i];
            printf ",%s", (table[sig][sample] ? table[sig][sample] : "0");
        }
        print "";
    }
}'
