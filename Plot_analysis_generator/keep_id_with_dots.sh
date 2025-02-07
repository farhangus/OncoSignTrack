#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 input.vcf.gz"
  exit 1
fi

# Input VCF file from command line argument
input_vcf="$1"
output_vcf="filtered_${input_vcf}"

# Use bcftools to filter and compress the output
bcftools view -h "$input_vcf" > header.tmp                     # Extract the header
bcftools view "$input_vcf" | awk '$3 == "." {print}' > body.tmp  # Extract lines where the 3rd column is "."

# Combine header and body, then compress and index the output
cat header.tmp body.tmp | bcftools view -Oz -o "$output_vcf"   # Compress into gzipped VCF
bcftools index "$output_vcf"                                  # Create the index file

# Clean up temporary files
rm header.tmp body.tmp

echo "Filtered VCF file saved as $output_vcf"



