#!/bin/bash

# Default values
DEST_DIR=""
ALLELE_FREQ=""
BED_FILE=""
VISUALIZE=false
EXTRACT_ETY=false

# Function to display help message
show_help() {
    echo "OncoSignTrack Pipeline: Fully Automated Mutational Signature Analysis"
    echo ""
    echo "Usage: bash OncoSignTrack_pipeline.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -d, -D, --directory <path>         Specify the destination folder containing VCF files. (Required)"
    echo "  -f, -F, --allele-frequency <value> Set the allele frequency threshold. (Optional)"
    echo "  -b, -B, --bed-file <file>          Specify the BED file to exclude shared variants. (Optional)"
    echo "  -v, -V, --visualize                Generate graphs to compare mutational signatures among samples. (Optional)"
    echo "  -e, -E, --etiology                 Extract mutational signature etiology from the COSMIC database. (Optional)"
    echo "  -h, -H, --help                     Display this help message."
    echo ""
    echo "Description:"
    echo "  This pipeline is fully automated to process VCF files, calculate mutational signatures,"
    echo "  and visualize the results. It filters variants, extracts allele frequency (AF) from AD,"
    echo "  removes common SNPs using a BED file, and generates COSMIC signature contributions."
    echo "  The final output includes structured CSV files and visualizations."
    echo ""
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--directory|-D) DEST_DIR="$2"; shift 2;;
        -f|--allele-frequency|-F) ALLELE_FREQ="$2"; shift 2;;
        -b|--bed-file|-B) BED_FILE="$2"; shift 2;;
        -v|--visualize|-V) VISUALIZE=true; shift 1;;
        -e|--etiology|-E) EXTRACT_ETY=true; shift 1;;
        -h|--help|-H) show_help;;
        *) echo "Error: Unknown option: $1"; exit 1;;
    esac
done

# Check if required arguments are provided
if [[ -z "$DEST_DIR" ]]; then
    echo "Error: No directory provided. Use -d, -D, or --directory <path>."
    echo "Run 'bash OncoSignTrack_pipeline.sh --help' for more details."
    exit 1
fi

# Display pipeline start message
echo "Starting OncoSignTrack Pipeline..."
echo "Processing VCF files in: $DEST_DIR"

# Display optional parameters if provided
[[ -n "$ALLELE_FREQ" ]] && echo "Using allele frequency threshold: $ALLELE_FREQ"
[[ -n "$BED_FILE" ]] && echo "Excluding shared variants using BED file: $BED_FILE"
[[ "$VISUALIZE" == true ]] && echo "Visualization enabled: Generating comparison graphs for mutational signatures."
[[ "$EXTRACT_ETY" == true ]] && echo "Etiology extraction enabled: Fetching COSMIC mutation signature details."

# Step 1: Filtering variants
if [[ -n "$BED_FILE" ]]; then
    echo "Filtering variants..."
    for file in "$DEST_DIR"/*.gz;
    do
        echo "$file"
        bash Plot_analysis_generator/filter_vcf_non_common.sh "$file" "$BED_FILE"
    done
fi

if [[ -n "$ALLELE_FREQ" ]]; then
    if [[ -z "$BED_FILE" ]]
    then
    echo "Filtering variants by AF..."
    for file in "$DEST_DIR"/*.gz;
    do
        bash Plot_analysis_generator/filter_vcf_by_af.sh "$file" "$ALLELE_FREQ"
    done
    fi
    if [[ -n "$BED_FILE" ]]
    then
    echo "Filtering variants by AF..."
    for file in "$DEST_DIR"/*non_common*.gz;
    do
        bash Plot_analysis_generator/filter_vcf_by_af.sh "$file" "$ALLELE_FREQ"
    done
    fi
    
fi

# Step 2: Calculating mutational signatures

echo "Calculating mutational signatures..."
if [[ -z "$ALLELE_FREQ" && -z "$BED_FILE" ]]
then 
for file in "$DEST_DIR"/*.gz; do
    echo "Processing: $file"
    Rscript Plot_analysis_generator/mutational_analysis_single_file.R "$file"
done
fi

if [[ -n "$ALLELE_FREQ" && -z "$BED_FILE" ]]
then
for file in "$DEST_DIR"/AF*.gz; do
 echo "Processing: $file"
    Rscript Plot_analysis_generator/mutational_analysis_single_file.R "$file"
done
fi

if [[ -z "$ALLELE_FREQ" && -n "$BED_FILE" ]]
then
for file in "$DEST_DIR"/*non_common*.gz; do
 echo "Processing: $file"
    Rscript Plot_analysis_generator/mutational_analysis_single_file.R "$file"
done
fi

if [[ -n "$ALLELE_FREQ" && -n "$BED_FILE" ]]
then
for file in "$DEST_DIR"/AF*non_common*.gz; do
 echo "Processing: $file"
    Rscript Plot_analysis_generator/mutational_analysis_single_file.R "$file"
done
fi

echo "Mutational signature calculation completed."

# Step 3: Extracting mutational signature etiology
if [[ "$EXTRACT_ETY" == true ]]; then
    echo "Step 3: Extracting etiology from COSMIC..."
    # Add command to extract etiology from COSMIC
fi
# Step 4: Generating visualizations
# Step 4: Generating visualizations
if [[ "$VISUALIZE" == true ]]; then
    tmpfile="$DEST_DIR/all.csv"
    tmp_file_group="$DEST_DIR/group.csv"
    echo "File,Signature,Contribution" > "$tmpfile"
    echo "Step 4: Generating visualizations..."
    
    shopt -s nullglob
    for file in "$DEST_DIR"/*.csv; do
        [[ "$file" == "$tmpfile" ]] && continue  # Skip the output file
        grep -v -e "File" -e ",0" "$file" >> "$tmpfile"
    done
    shopt -u nullglob  # Restore default behavior
    
    if [[ -s "$tmpfile" ]]; then
        python3 Plot_analysis_generator/generate_box_plot.py "$tmpfile"
        python3 Plot_analysis_generator/bar_plot_generator.py "$tmpfile"
        python3 Plot_analysis_generator/sbs_scaled_barplot_10_top.py  "$tmpfile"
        sed -i 's/"//g' "$tmpfile"
        bash Plot_analysis_generator/generate_report_grouped_by_SBS.sh "$tmpfile"> "$tmp_file_group"
        python3 Plot_analysis_generator/heat_map_table_generator.py "$tmp_file_group"
    else
        echo "No data to visualize. Skipping plot generation."
    fi
    rm $tmpfile
    rm "$tmp_file_group"
fi

if [[ "$EXTRACT_ETY" == true ]]; then
    tmpfile="$DEST_DIR/all.csv"
    tmp_sbs_list="$DEST_DIR/sbs.txt"
    sbs_log="$DEST_DIR/sbs_ety.log"
    shopt -s nullglob

    for file in "$DEST_DIR"/*.csv; do
        [[ "$file" == "$tmpfile" ]] && continue  # Skip the output file
        grep -v -e "File" -e ",0" "$file" >> "$tmpfile"
    done

    # Debugging step: Check if the file exists before processing
    if [[ ! -f "$tmpfile" ]]; then
        echo "Error: Expected file $tmpfile not found!" >&2
        exit 1
    fi

    cat "$tmpfile" | cut -d , -f 2 | tr -d '\"' | sort | uniq > "$tmp_sbs_list"
    shopt -u nullglob  # Restore default behavior

    # Run the Python script and save the log
    python3 Plot_analysis_generator/Proposed_Aetiology_extractor.py -l "$tmp_sbs_list" > "$sbs_log"

    # Clean up temporary files safely
    rm "$tmpfile"
    rm "$tmp_sbs_list"
fi

echo "Pipeline completed successfully! Results are stored in: $DEST_DIR"
