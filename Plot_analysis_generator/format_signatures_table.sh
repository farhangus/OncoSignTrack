#!/bin/bash

# Check if an argument (input filename) is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Read input file from command-line argument
input_file="$1"
output_file="sbs_signatures.txt"

# Check if the file exists
if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found!"
    exit 1
fi

# Process each line of the input file
declare -A signature_map

while IFS= read -r line; do
    # Remove "Associated Signatures:" from the line
    line=$(echo "$line" | sed 's/Associated Signatures: //g')

    # Extract the prefix before the colon (the main SBS entry)
    prefix=$(echo "$line" | cut -d':' -f1 | xargs)

    # Extract the text after the colon (associated signatures)
    content=$(echo "$line" | cut -d':' -f2- | xargs)

    # Extract only SBS signatures (removing DBS, ID, CN, SV)
    sbs_list=$(echo "$content" | grep -oE 'SBS[0-9]+[a-zA-Z]?' | sort -u | tr '\n' ' ')

    # Remove the SBS prefix from the right side if it appears in the left column
    filtered_sbs_list=""
    for sbs in $sbs_list; do
        if [[ "$sbs" != "$prefix" ]]; then
            filtered_sbs_list+="$sbs "
        fi
    done

    # Remove trailing spaces and replace spaces with commas
    filtered_sbs_list=$(echo "$filtered_sbs_list" | xargs | tr ' ' ',')

    # Store unique SBS values only (remove empty lines)
    if [[ ! -z "$filtered_sbs_list" ]]; then
        signature_map["$prefix,$filtered_sbs_list"]=1
    fi
done < "$input_file"

# Save unique results to output file
> "$output_file"
for key in "${!signature_map[@]}"; do
    echo "$key" >> "$output_file"
done

echo "Formatted SBS output saved to $output_file"

