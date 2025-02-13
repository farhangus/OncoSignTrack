# Function to check and install missing packages
check_install <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package, repos = "http://cran.us.r-project.org")
  }
}

library(ggplot2)

# Check if BiocManager is installed
check_install("BiocManager")

# Load BiocManager
library(BiocManager)

# Function to install Bioconductor packages if not installed
bioc_check_install <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    BiocManager::install(package)
  }
}

# Install and load required Bioconductor packages
bioc_check_install("BSgenome.Hsapiens.NCBI.GRCh38")
library(BSgenome.Hsapiens.NCBI.GRCh38)

bioc_check_install("MutationalPatterns")
library(MutationalPatterns)

check_install("vcfR")
library(vcfR)

bioc_check_install("VariantAnnotation")
library(VariantAnnotation)

# Get the directory from command line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("Error: Please provide the folder path containing VCF files as an argument.")
}

folder_path <- args[1]  # Take the first argument as folder path

# Set the working directory to the user-provided folder
setwd(folder_path)
print(paste("Working directory set to:", folder_path))

# List all VCF files in the folder
vcf_files <- list.files(pattern = "\\.vcf(\\.gz)?$")
if (length(vcf_files) == 0) {
  stop("Error: No VCF files found in the specified directory.")
}

# Initialize a data frame to store results for all files
all_results <- data.frame(
  File = character(),
  Signature = character(),
  Contribution = numeric(),
  stringsAsFactors = FALSE
)

# Loop through each VCF file and perform mutational signature analysis
for (vcf_file in vcf_files) {
  print(paste("Processing:", vcf_file))
  
  tryCatch({
    # Read the VCF file
    vcf <- read.vcfR(vcf_file)
    
    # Extract the AF field from the INFO column and filter for AF > 0
    af_values <- extract.info(vcf, element = "AF")
    af_values <- as.numeric(af_values)
    if (any(is.na(af_values))) {
      af_values <- af_values[!is.na(af_values)] # Remove NA values
    }
    
    # Filter VCF rows where AF > 0
    vcf <- vcf[which(af_values > 0), ]
    
    # Extract the sample names from the VCF file
    vcf_meta <- colnames(vcf@gt)[-1]  # The first column is FORMAT, so skip it
    
    # Use the first sample name from the VCF file
    sample_names <- vcf_meta[1]
    print(paste("Using sample name:", sample_names))
    
    # Use read_vcfs_as_granges from MutationalPatterns to read the VCF file
    vcf_granges <- read_vcfs_as_granges(vcf_file, sample_names, genome = BSgenome.Hsapiens.NCBI.GRCh38, predefined_dbs_mbs = TRUE)
    
    # Extract the mutational contexts (trinucleotide context)
    mut_context <- mut_matrix(vcf_granges, ref_genome = BSgenome.Hsapiens.NCBI.GRCh38)
    
    # Compare sample against known COSMIC signatures
    cosmic_signatures <- get_known_signatures()
    
    # Fit data to COSMIC signatures
    fit_res <- fit_to_signatures(mut_context, cosmic_signatures)
    
    # Save the contribution data as a CSV
    contributions <- as.data.frame(t(fit_res$contribution))
    contributions$File <- vcf_file
    contributions <- reshape2::melt(contributions, id.vars = "File", variable.name = "Signature", value.name = "Contribution")
    
    # Add to cumulative results
    all_results <- rbind(all_results, contributions)
    
    # Save contributions as a CSV file for the current VCF file
    csv_output_file <- gsub("\\.vcf(\\.gz)?$", "_mutational_signatures.csv", vcf_file)
    write.csv(contributions, csv_output_file, row.names = FALSE)
    print(paste("CSV saved to:", csv_output_file))
    
    # Visualize the contribution of signatures and save the plot
    output_plot_file <- gsub("\\.vcf(\\.gz)?$", "_mutational_signatures.png", vcf_file)
    contribution_plot <- plot_contribution(fit_res$contribution, cosmic_signatures, mode = "absolute")
    
    # Save the plot
    ggsave(output_plot_file, plot = contribution_plot, width = 10, height = 7, dpi = 300)
    print(paste("Plot saved to:", output_plot_file))
  }, error = function(e) {
    # Handle errors gracefully
    print(paste("Error processing file:", vcf_file))
    print(e)
  })
}

# Save all results in a summary CSV
summary_csv <- "all_mutational_signatures_summary.csv"
write.csv(all_results, summary_csv, row.names = FALSE)
print(paste("Summary CSV saved to:", summary_csv))

