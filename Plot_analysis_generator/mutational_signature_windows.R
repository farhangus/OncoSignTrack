# Function to check and install missing packages
check_install <- function(package) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package)
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

# Install and load the genome package if not installed
bioc_check_install("BSgenome.Hsapiens.NCBI.GRCh38")
library(BSgenome.Hsapiens.NCBI.GRCh38)

# Check and install MutationalPatterns, vcfR, and VariantAnnotation if not installed
bioc_check_install("MutationalPatterns")
library(MutationalPatterns)

check_install("vcfR")
library(vcfR)

bioc_check_install("VariantAnnotation")
library(VariantAnnotation)

# Set the working directory to the folder containing VCF files
setwd("C:/Project/aff_heatmaps/WGS") # Replace with the actual path to your folder

# List all VCF files in the folder
vcf_files <- list.files(pattern = "*.vcf.gz")

# Initialize a results data frame for summary
results <- data.frame(
  File = character(),
  Signature = character(),
  Contribution = numeric(),
  stringsAsFactors = FALSE
)

# Loop through each VCF file and perform mutational signature analysis
for (vcf_file in vcf_files) {
  print(paste("Processing:", vcf_file))
  
  # Read the VCF file using the vcfR package
  vcf <- read.vcfR(vcf_file)
  
  # Extract the AF field from the INFO column and filter for AF > 0
  af_values <- extract.info(vcf, element = "AF")
  af_values <- as.numeric(af_values)
  
  # Filter VCF rows where AF > 0
  vcf <- vcf[which(af_values > 0), ]
  
  # Extract the sample names from the VCF file
  vcf_meta <- colnames(vcf@gt)[-1]  # The first column is usually FORMAT, so skip it
  
  # Use the first sample name from the VCF file
  sample_names <- vcf_meta[1]
  print(paste("Using sample name:", sample_names))
  
  # Use read_vcfs_as_granges from MutationalPatterns to read the VCF file
  vcf_granges <- read_vcfs_as_granges(vcf_file, sample_names, genome = BSgenome.Hsapiens.NCBI.GRCh38, predefined_dbs_mbs = TRUE)
  
  # Extract the mutational contexts (trinucleotide context)
  mut_context <- mut_matrix(vcf_granges, ref_genome = BSgenome.Hsapiens.NCBI.GRCh38)
  
  # Compare your sample against known COSMIC signatures
  cosmic_signatures <- get_known_signatures()
  
  # Fit your data to the COSMIC signatures
  fit_res <- fit_to_signatures(mut_context, cosmic_signatures)
  
  # Save contributions to the results data frame
  contributions <- as.data.frame(t(fit_res$contribution))
  contributions$File <- vcf_file
  contributions <- reshape2::melt(contributions, id.vars = "File", variable.name = "Signature", value.name = "Contribution")
  results <- rbind(results, contributions)
  
  # Visualize the contribution of signatures and save the plot
  base_name <- gsub(".vcf.gz$", "", vcf_file)
  output_plot_file <- paste0(base_name, "_mutational_signatures.png")
  output_csv_file <- paste0(base_name, "_mutational_signatures.csv")
  
  contribution_plot <- plot_contribution(fit_res$contribution, cosmic_signatures, mode = "absolute") +
    labs(y = "Contribution (WGS)")  
  
  # Save the plot
  ggsave(output_plot_file, plot = contribution_plot, width = 10, height = 7, dpi = 300)
  print(paste("Plot saved to:", output_plot_file))
  
  # Save the contributions as a CSV file
  write.csv(contributions, output_csv_file, row.names = FALSE)
  print(paste("CSV report saved to:", output_csv_file))
}

# Save the cumulative results for all VCF files as a separate summary CSV
write.csv(results, "mutational_signatures_summary.csv", row.names = FALSE)
print("Summary report saved to: mutational_signatures_summary.csv")

print("Processing completed for all VCF files.")

