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

To run OncoSignTrack, install the required dependencies:

```bash
pip install numpy pandas matplotlib seaborn
conda install -c bioconda bedtools
R -e "install.packages(c('ggplot2', 'BiocManager', 'vcfR', 'VariantAnnotation'))"
R -e "BiocManager::install(c('BSgenome.Hsapiens.NCBI.GRCh38', 'MutationalPatterns'))"

```
## License

OncoSignTrack is licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, without warranties or conditions of any kind, either express or implied. See the License for the specific language governing permissions and limitations under the License.
