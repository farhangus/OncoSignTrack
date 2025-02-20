#!/bin/bash

# Check if correct arguments are given
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.vcf.gz> <input.bed>"
    exit 1
fi

# Get input VCF and BED file
VCF_FILE="$1"
BED_FILE="$2"

# Get directory and base name of the VCF file
VCF_DIR=$(dirname "$VCF_FILE")
VCF_BASENAME=$(basename "$VCF_FILE" .vcf.gz)

# Define output file name
OUTPUT_VCF="${VCF_DIR}/${VCF_BASENAME}_non_common.vcf.gz"

# Create a temporary header file
HEADER_TMP=$(mktemp)

# Extract header from the VCF file
zgrep "^#" "$VCF_FILE" > "$HEADER_TMP"

# Use bedtools subtract to remove variants present in the BED file 
bedtools subtract -A -a "$VCF_FILE" -b "$BED_FILE" | grep -v "^#" > "${VCF_BASENAME}_filtered_body.vcf"

# Combine header and filtered body into a new VCF file
cat "$HEADER_TMP" "${VCF_BASENAME}_filtered_body.vcf" | bgzip -c > "$OUTPUT_VCF"

# Index the new VCF file
#tabix -p vcf "$OUTPUT_VCF"

# Clean up temporary files
rm -f "$HEADER_TMP" "${VCF_BASENAME}_filtered_body.vcf"

echo "Filtered VCF saved as: $OUTPUT_VCF"

