# OncoSignTrack Pipeline

OncoSignTrack is a fully automated and user-friendly computational pipeline designed for high-throughput analysis of mutational signatures. It processes VCF files, extracts mutational signatures, and integrates COSMIC annotations, offering comprehensive insights into tumor aetiology and genomic alterations.

## Implementation

The pipeline is constructed using a **modular design**, allowing components to be added, removed, or replaced without disrupting the workflow. This approach enables **customization** based on research objectives and facilitates seamless **integration** with existing bioinformatics tools.

### **Technology Stack**
OncoSignTrack is implemented using **Python, R, and Bash**, leveraging the strengths of each language for robust and flexible genomic data analysis:

- **Python:** Primary language for **data visualization and mutational signature extraction**.
  - **Libraries used:** `pandas`, `matplotlib`, `seaborn`, `numpy`
- **R:** Used for **genomic data wrangling and analysis**.
  - **Required packages:** `ggplot2`, `BiocManager`, `BSgenome.Hsapiens.NCBI.GRCh38`, `MutationalPatterns`, `vcfR`, `VariantAnnotation`
- **Bash:** Controls the execution of different components.
- **bedtools:** Used to **filter shared variants** and **exclude common variations** based on user-defined allele frequency thresholds.

The pipeline is optimized for **reproducibility** and **scientific rigor**, with built-in **error handling** that detects, logs, and resolves issues at each stage, ensuring streamlined genomic data analysis.

## Command-Line Options

| **Flag** | **Description** | **Required?** |
|---------|-------------|--------------|
| `-d, -D, --directory` | Path to VCF directory | ✅ **Yes** |
| `-f, -F, --allele-frequency` | Allele frequency threshold | ❌ **Optional** |
| `-b, -B, --bed-file` | BED file to exclude shared variants | ❌ **Optional** |
| `-v, -V, --visualize` | Generate visualizations | ❌ **Optional** |
| `-e, -E, --etiology` | Extract COSMIC etiology info | ❌ **Optional** |
| `-h, -H, --help` | Display help message | ❌ **Optional** |

## Features

- **Automated variant filtering**: Identifies non-frequent SNPs using `hg38` or `hg37`.
- **Allele frequency calculation**: Extracts real **allele frequency (AF)** from **allele depth (AD)** values.
- **COSMIC annotation integration**: Retrieves and organizes **mutational signatures** based on **COSMIC database**.
- **Visualization tools**: Generates **heatmaps, stacked bar charts, and boxplots** for easy interpretation.
- **Scalability**: Supports **large-scale genomic studies**, ensuring reproducible analysis.

## Installation

To ensure a smooth installation of **OncoSignTrack**, follow the steps below to set up a dedicated environment and install all required dependencies.

```bash
# 1. Set up a Conda/Mamba environment
# Using Conda:
conda create -n oncosigntrack_env python=3.9 -y
conda activate oncosigntrack_env

# OR Using Mamba (faster alternative to Conda):
mamba create -n oncosigntrack_env python=3.9 -y
mamba activate oncosigntrack_env

# 2. Install Python dependencies
pip install numpy pandas matplotlib seaborn

# 3. Install Bedtools
conda install -c bioconda bedtools

# 4. Install R and required packages
# If R is not installed, install it first using Conda:
conda install -c conda-forge r-base

# Install required R packages
R -e "install.packages(c('ggplot2', 'BiocManager', 'vcfR', 'VariantAnnotation'))"
R -e "BiocManager::install(c('BSgenome.Hsapiens.NCBI.GRCh38', 'MutationalPatterns'))"

```
## Usage

To run OncoSignTrack, use the following command-line options:

```bash
./OncoSignTrack_pipeline.sh -h
 -d, -D, --directory <path>         Specify the destination folder containing VCF files. (Required)
  -f, -F, --allele-frequency <value> Set the allele frequency threshold. (Optional)
  -b, -B, --bed-file <file>          Specify the BED file to exclude shared variants. (Optional)
  -v, -V, --visualize                Generate graphs to compare mutational signatures among samples. (Optional)
  -e, -E, --etiology                 Extract mutational signature etiology from the COSMIC database. (Optional)
  -h, -H, --help                     Display this help message.
```

## Example Visualization

Here is an example of a mutational signature visualization:
![sample of heatmap comapring SBS among samples_1](images/heatmap_samples_with_counts.png)
![sample of barplot for all SBSs](images/sbs_stacked_percentage_barplot_adjusted.png)

![sample of barplot for top10 SBSs](images/top_10_sbs_with_percentages.png)

![sample of boxplot](images/box_plot_.png)

## License

OncoSignTrack is licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, without warranties or conditions of any kind, either express or implied. See the License for the specific language governing permissions and limitations under the License.
