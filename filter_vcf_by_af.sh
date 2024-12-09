#!/bin/bash
# Script for filtering VCF files based on allele frequency (AF)
# Author: Farhang Jaryani
# Postdoctoral Fellow at Baylor College of Medicine
# Contact: farhang.jaryani@bcm.edu, fxjaryan@texaschildrens.org
# The Gallo Brain Tumor Research Lab, Department of Pediatrics, Section of Hematology-Oncology, Baylor College of Medicine

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_vcf_file>"
    exit 1
fi

# Input VCF file
input_vcf="$1"
input_dir=$(dirname "$input_vcf")
input_base=$(basename "$input_vcf")

# Extract necessary fields using bcftools query
bcftools query -f '%CHROM\t%POS\t%ID\t%REF\t%ALT\t[%SAMPLE\t%AD\t]\n' "$input_vcf" | \
awk 'BEGIN { OFS="\t" }
{
    keep = 0
    for (i=7; i<=NF; i+=2) {
        if ($i ~ /^[0-9]+,[0-9]+$/) {
            split($i, ad, ",");
            ref_count = ad[1];
            alt_count = ad[2];
            if (ref_count + alt_count > 0) {  # Avoid division by zero
                af = alt_count / (ref_count + alt_count);
                if (af < 0.30 && af > 0) {    # Filter based on AF range
                    keep = 1
                    break
                }
            }
        }
    }
    if (keep) {
        print $1, $2
    }
}' > "$input_dir/positions.txt"

# Use the extracted positions to filter the original VCF
if [ -s "$input_dir/positions.txt" ]; then
    bcftools view -T "$input_dir/positions.txt" "$input_vcf" -Oz -o "$input_dir/filtered_$input_base"
    # Index the new filtered VCF file
    bcftools index "$input_dir/filtered_$input_base"
    echo "Filtering complete. Filtered VCF: $input_dir/filtered_$input_base"
else
    echo "No variants passed the filtering criteria."
fi

