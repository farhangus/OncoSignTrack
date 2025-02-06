#!/bin/bash

# Input file containing URLs
input_file="download_links"

# Loop through each line in the file
while read -r line; do
  # Extract everything after 'variants/' and before '?'
  filename=$(echo "$line" | sed -n 's/.*variants\/\([^?]*\)?.*/\1/p')
  
  # Generate wget command
  if [[ -n "$filename" ]]; then
    echo "wget \"$line\" -O \"$filename\""
  fi
done < "$input_file"

