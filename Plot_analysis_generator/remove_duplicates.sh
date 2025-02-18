#!/bin/bash

# Check if a filename is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Check if the file exists
if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found!"
    exit 1
fi

# Process the file to remove duplicate words, handling spaces and commas
awk '
{
    seen = "";   # Variable to keep track of seen words
    gsub(/,/, " ", $0);  # Replace commas with spaces
    split($0, words, " ");

    output = "";
    for (i in words) {
        if (words[i] != "" && !match(seen, "\\<" words[i] "\\>")) {  # Check if word is not already seen
            output = output (output ? " " : "") words[i];
            seen = seen words[i] " ";
        }
    }
    print output;
}' "$1"

