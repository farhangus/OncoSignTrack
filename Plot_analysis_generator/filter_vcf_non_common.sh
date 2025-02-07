#!/bin/bash

# Check if the input VCF file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_vcf.gz>"
    exit 1
fi

# Input VCF file
input_vcf="$1"

# Define the BED file path
bed_file="../../Projects/Gene_AF/CrHG38_common_SNPs_exons_beds/common_SNPs.bed"

# Extract the base name of the input file to create the output file name
base_name=$(basename "$input_vcf" .vcf.gz)
output_vcf="${base_name}_final_filtered.vcf.gz"

# Temporary file for storing intermediate data
temp_body_file="${base_name}_body.tmp"
temp_header_file="${base_name}_header.tmp"

# Step 1: Extract the VCF header
bcftools view -h "$input_vcf" > "$temp_header_file"

# Step 2: Remove variants overlapping with the BED file
bedtools intersect -v -a "$input_vcf" -b "$bed_file" > "$temp_body_file"

# Step 3: Append the extracted variants to the header and compress
cat "$temp_header_file" "$temp_body_file" | bgzip -c > "$output_vcf"

# Step 4: Cleanup intermediate files
rm -f "$temp_header_file" "$temp_body_file"

# Step 5: Notify the user
echo "Filtered VCF file (no overlaps) created: $output_vcf"

