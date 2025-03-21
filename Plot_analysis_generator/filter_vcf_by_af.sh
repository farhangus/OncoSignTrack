#!/bin/bash
# Script for filtering VCF files based on allele frequency (AF)
# Author: Farhang Jaryani
# Postdoctoral Fellow at Baylor College of Medicine
# Contact: farhang.jaryani@bcm.edu, fxjaryan@texaschildrens.org
# The Gallo Brain Tumor Research Lab, Department of Pediatrics, Section of Hematology-Oncology, Baylor College of Medicine

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_vcf_file> <AF_threshold>"
    exit 1
fi

# Input VCF file
input_vcf="$1"
af_threshold="$2"

# Validate AF threshold (ensure it's a number between 0 and 1)
if ! [[ "$af_threshold" =~ ^0(\.[0-9]+)?$ || "$af_threshold" =~ ^1(\.0+)?$ ]]; then
    echo "Error: AF_threshold must be a number between 0 and 1."
    exit 1
fi

input_dir=$(dirname "$input_vcf")
input_base=$(basename "$input_vcf")

# Use a unique temporary file for storing positions
temp_positions_file=$(mktemp --tmpdir="$input_dir" positions_XXXXXX.txt)

# Extract necessary fields using bcftools query
bcftools query -f '%CHROM\t%POS\t%ID\t%REF\t%ALT\t[%SAMPLE\t%AD\t]\n' "$input_vcf" | \
awk -v af_threshold="$af_threshold" 'BEGIN { OFS="\t" }
{
    keep = 0
    for (i=7; i<=NF; i+=2) {
        if ($i ~ /^[0-9]+,[0-9]+$/) {
            split($i, ad, ",");
            ref_count = ad[1];
            alt_count = ad[2];
            if (ref_count + alt_count > 0) {  # Avoid division by zero
                af = alt_count / (ref_count + alt_count);
                if (af <= af_threshold && af > 0) {  # Filter based on AF range
                    keep = 1
                    break
                }
            }
        }
    }
    if (keep) {
        print $1, $2
    }
}' > "$temp_positions_file"

# Define filtered VCF output file name
output_vcf="$input_dir/AF_${af_threshold}_${input_base}"

# Use the extracted positions to filter the original VCF
if [ -s "$temp_positions_file" ]; then
    bcftools view -T "$temp_positions_file" "$input_vcf" -Oz -o "$output_vcf"
    
    # Index the new filtered VCF file
    #bcftools index "$output_vcf"
    
    echo "Filtering complete. Filtered VCF: $output_vcf"
else
    echo "No variants passed the filtering criteria."
fi

# Clean up temporary file
rm -f "$temp_positions_file"
