#!/usr/bin/env python3
import os
import re
import hashlib
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt

# Directory where the uncompressed genome text files are located.
GENOME_DIR = os.path.expanduser("~/genomes")

# Define SNP info (only high and medium confidence entries)
snp_info = {
    "rs1861759": ("High Confidence", "Associated with hereditary alpha tryptasemia, linked to mast cell activation."),
    "rs5030858": ("High Confidence", "Located in the PAH gene; associated with Phenylketonuria (PKU)."),
    "rs7247424": ("High Confidence", "PAH gene variant; linked to PKU and hyperphenylalaninemia."),
    "rs17176012": ("Medium Confidence", "Located in the PAH gene; possibly associated with PKU and related disorders."),
    "rs17176014": ("Medium Confidence", "PAH gene variant; may contribute to PKU susceptibility."),
    "rs199475200": ("High Confidence", "Located in the PAH gene; pathogenic variant associated with PKU."),
    "rs121918202": ("High Confidence", "PAH gene variant; linked to classic PKU."),
    "rs199475201": ("High Confidence", "Located in the PAH gene; associated with PKU and hyperphenylalaninemia."),
    "rs199475203": ("High Confidence", "PAH gene variant; pathogenic variant associated with PKU."),
    "rs199475204": ("High Confidence", "Located in the PAH gene; linked to PKU and related disorders."),
    "rs199475205": ("High Confidence", "PAH gene variant; associated with classic PKU."),
    "rs113578744": ("High Confidence", "Affects tryptase levels, possibly influencing MCAS-like symptoms."),
    "rs140863677": ("High Confidence", "Strongly linked to hereditary alpha tryptasemia, a trait inherited from Neanderthals."),
    "rs1048101": ("Medium Confidence", "Impacts adrenergic receptors, potentially affecting autonomic function."),
    "rs144921697": ("Medium Confidence", "Located in the MHC region, may influence immune response."),
    "rs17878979": ("Medium Confidence", "Similar to rs144921697, with potential effects on autoimmune susceptibility."),
    "rs2104286": ("Medium Confidence", "Associated with autoimmune conditions such as multiple sclerosis."),
    "rs12721431": ("Medium Confidence", "May influence collagen regulation, with possible links to EDS."),
    "rs1063325": ("Medium Confidence", "Implicated in classical-like EDS and rare connective tissue disorders."),
    "rs652722": ("Medium Confidence", "Similar to rs1063325, with possible roles in EDS and autoimmune conditions."),
    "rs6944656": ("Medium Confidence", "Associated with QT-interval modulation and possible autonomic dysfunction."),
    "rs28931567": ("Medium Confidence", "Similar to rs6944656; limited evidence for POTS or MCAS association."),
    "rs1805007": ("High Confidence", "Common red-hair variant; sometimes associated with altered pain sensitivity."),
    "rs4680": ("High Confidence", "Affects dopamine metabolism and cognitive function (COMT gene)."),
    "rs6323": ("Medium Confidence", "Influences monoamine metabolism, possibly affecting ADHD risk."),
    "rs25531": ("Medium Confidence", "Impacts serotonin transporter function."),
    "rs1800955": ("High Confidence", "DRD4 promoter SNP; associated with ADHD and cognitive traits."),
    "rs3729984": ("Medium Confidence", "GABRA2 variant studied for psychiatric and addiction traits."),
    "rs769449": ("Medium Confidence", "APOE variant known for potential links to Alzheimer's and neurodegeneration."),
    "rs731236": ("Medium Confidence", "Vitamin D receptor variant, with possible links to autoimmune conditions."),
    "rs2075800": ("Medium Confidence", "HSP70 variant linked to inflammatory response modulation."),
    "rs12498609": ("Medium Confidence", "Neanderthal-derived variant linked to immune system regulation; function not fully understood."),
    "rs1156361": ("Medium Confidence", "Neanderthal-derived variant in the TLR1 gene; may influence innate immune response."),
    "rs1881227": ("Medium Confidence", "Neanderthal-derived variant in the KLF4 gene; may play a role in skin barrier function."),
    "rs1260326": ("Medium Confidence", "Neanderthal-derived variant in the GCKR gene; associated with metabolic traits."),
    "rs10490770": ("Medium Confidence", "Neanderthal-derived variant in the SLC6A11 gene; may influence neurotransmitter transport."),
    "rs12191877": ("Medium Confidence", "Neanderthal-derived variant in the FOXP2 gene; may influence speech and language development."),
    "rs10013927": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs10521422": ("Medium Confidence", "Associated with auditory processing and language development."),
    "rs10833250": ("Medium Confidence", "Linked to cognitive flexibility and problem-solving ability."),
    "rs11090765": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs11610106": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs11843595": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs12278743": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs12411045": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs12604783": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs12822717": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs13004413": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs13274337": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1352025": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs1384586": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs1427763": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs1453624": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1520324": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs1540017": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1561582": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs1580173": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs1600247": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs1621913": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1801157": ("Medium Confidence", "COL3A1 gene variant associated with EDS type IV."),
    "rs17165664": ("Medium Confidence", "COL5A2 gene variant associated with classical EDS."),
    "rs1063325": ("Medium Confidence", "TNXB gene variant associated with classical-like EDS."),  # duplicate key: latter overrides
    "rs11556924": ("Medium Confidence", "Height and skeletal growth, potential link to EDS."),
    "rs1801252": ("Medium Confidence", "ADRB1 gene variant linked to POTS and autonomic dysfunction."),
    "rs12190992": ("Medium Confidence", "NOS1AP gene variant associated with POTS and QT-interval modulation."),
    "rs12401481": ("Medium Confidence", "COMT gene variant linked to POTS and autonomic dysfunction."),
    "rs4307059": ("Medium Confidence", "SHANK3 gene variant linked to autism and intellectual disability."),
    "rs1858830": ("Medium Confidence", "OXTR gene variant linked to autism and social behavior."),
    "rs2104286": ("High Confidence", "Located near the IL2RA gene; associated with multiple sclerosis and type 1 diabetes."),
    "rs11209026": ("High Confidence", "A non-synonymous variant in the IL23R gene; robustly linked to Crohn's disease, psoriasis, and related inflammatory conditions."),
    "rs12927355": ("High Confidence", "Located near the STAT4 gene; linked with rheumatoid arthritis and systemic lupus erythematosus."),
    "rs3087243": ("High Confidence", "Located in the CTLA4 gene; associated with autoimmune thyroid disease, type 1 diabetes, and other autoimmune disorders."),
    "rs6822844": ("High Confidence", "Found in the IL2/IL21 region; associated with rheumatoid arthritis, celiac disease, and type 1 diabetes."),
    "rs763361": ("High Confidence", "Located in the CD226 gene; linked with several autoimmune diseases, including type 1 diabetes and multiple sclerosis."),
    "rs6457617": ("High Confidence", "Located in the HLA region; associated with multiple autoimmune conditions such as rheumatoid arthritis and type 1 diabetes."),
    "rs9271366": ("High Confidence", "Located in the HLA-DQA1 region; associated with type 1 diabetes and celiac disease."),
    "rs2187668": ("High Confidence", "Also in the HLA-DQA1 region; strongly associated with celiac disease and type 1 diabetes."),
    "rs6323": ("Medium Confidence", "SLC6A3 gene variant linked to ADHD and autism risk."),
    "rs25531": ("Medium Confidence", "SLC6A4 gene variant associated with serotonin transport and autism risk."),
    "rs1048101": ("Medium Confidence", "ADRA1A gene variant linked to autonomic dysfunction and ADHD risk."),
    "rs35044562": ("Medium Confidence", "Neanderthal-derived SNP within the risk haplotype on chromosome 3 associated with increased risk for severe COVID-19; further studies are needed to clarify its functional role."),
    "rs10774671": ("Medium Confidence", "Neanderthal-derived variant in the OAS1 gene that influences alternative splicing and antiviral responses; has been linked in some studies to COVID-19 outcomes, pending further validation."),
    "rs5743810": ("Medium Confidence", "Neanderthal-derived variant in the TLR6 gene; may contribute to modulation of innate immune responses against pathogens; functional effects remain under investigation."),
    "rs4129009": ("Low Confidence", "Putative Neanderthal-derived variant in the TLR10 gene; preliminary data suggest it might affect inflammatory signaling, but more research is required."),
    "rs1868092": ("High Confidence", "Denisovan-derived variant in the EPAS1 gene associated with high-altitude adaptation in Tibetan populations."),
    "rs6754295": ("Medium Confidence", "Candidate Denisovan-derived SNP in the EPAS1 region; may influence hypoxia response in high-altitude environments, pending further studies."),
    "rs4953354": ("Medium Confidence", "Putative Denisovan-derived variant in the EPAS1 region; its functional impact on oxygen homeostasis is under investigation."),
    "rs2293607": ("Medium Confidence", "Candidate Denisovan-derived SNP in the TBX15/WARS2 region; potential role in body fat distribution and cold adaptation, subject to further validation.")
}

# Keep only High and Medium confidence entries
filtered_snp_info = {snp: info for snp, info in snp_info.items() if info[0] in ("High Confidence", "Medium Confidence")}
snp_set = set(filtered_snp_info.keys())

def compute_hash(file_path, block_size=65536):
    """Compute SHA256 hash for a given file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def process_file(file_path):
    """Process a genome file by scanning for SNPs based on the first token of each line."""
    found_snps = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.strip().split()
                if not parts:
                    continue
                rs_id = parts[0]
                if rs_id in snp_set:
                    found_snps.add(rs_id)
                # Optional early break if all SNPs are found
                if len(found_snps) == len(snp_set):
                    break
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return found_snps

def main():
    # List all .txt files in the genome directory
    file_paths = [os.path.join(GENOME_DIR, f) for f in os.listdir(GENOME_DIR) if f.endswith('.txt')]
    total_files = len(file_paths)
    
    unique_hashes = {}
    duplicate_files = []
    snp_counts = defaultdict(int)
    unique_file_count = 0

    # Process each file with a progress bar
    for file_path in tqdm(file_paths, desc="Processing genome files"):
        file_hash = compute_hash(file_path)
        if file_hash in unique_hashes:
            duplicate_files.append(file_path)
            continue
        unique_hashes[file_hash] = file_path
        unique_file_count += 1
        found_snps = process_file(file_path)
        for snp in found_snps:
            snp_counts[snp] += 1

    # Build a results DataFrame
    data = []
    for snp, (confidence, description) in filtered_snp_info.items():
        count = snp_counts[snp]
        frequency = count / unique_file_count if unique_file_count > 0 else 0
        data.append({
            "SNP ID": snp,
            "Confidence": confidence,
            "Description": description,
            "Count": count,
            "Frequency": frequency
        })
    df = pd.DataFrame(data)
    df.sort_values(by=["Confidence", "SNP ID"], inplace=True)
    
    # Save CSV output in the genome directory
    csv_output = os.path.join(GENOME_DIR, "snp_frequency_results.csv")
    df.to_csv(csv_output, index=False)
    
    # Create a Markdown report with duplicate statistics and a table of results
    report_lines = [
        "# Scientific Report: Prevalence of Selected SNPs in the Genome Dataset",
        f"**Total files processed:** {total_files}",
        f"**Unique genome profiles:** {unique_file_count}",
        f"**Duplicate files skipped:** {len(duplicate_files)}",
        "",
        "This report summarizes the occurrence of high and medium confidence SNPs in the genome dataset. "
        "Each SNP’s prevalence is given as the count and as a frequency based on the number of unique genome profiles analyzed.",
        "",
        "## Methods",
        "1. The dataset was uncompressed to `~/genomes/` and all text files (*.txt) were processed.",
        "2. A SHA256 hash was computed for each file to detect duplicates; duplicate files were skipped.",
        "3. Each unique file was read line-by-line (ignoring comment lines), assuming the first token on each line is the SNP identifier.",
        "4. The occurrences of SNPs of interest (High and Medium Confidence) were counted.",
        "",
        "## Results",
        "### SNP Frequency Table",
        df.to_markdown(index=False),
        "",
        "## Visualizations",
        "The bar chart below shows the frequency of each SNP in the unique genome profiles:",
        "![SNP Frequency Bar Chart](snp_bar_chart.png)",
        "",
        "## Discussion and Conclusion",
        "The data presented here provide an overview of the prevalence of several important genetic variants. "
        "Further analysis and validation with additional datasets is recommended.",
        "",
        "## References",
        "- openSNP dataset (unzipped files in `~/genomes/`)",
        "- SNP annotations provided by the research list."
    ]
    report_output = os.path.join(GENOME_DIR, "SNP_Prevalence_Report.md")
    with open(report_output, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    # Generate a bar chart visualization of SNP frequencies
    plt.figure(figsize=(12, 6))
    plt.bar(df["SNP ID"], df["Frequency"], color='skyblue')
    plt.xlabel("SNP ID")
    plt.ylabel("Frequency")
    plt.title("Frequency of Selected SNPs in Unique Genome Profiles")
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    chart_output = os.path.join(GENOME_DIR, "snp_bar_chart.png")
    plt.savefig(chart_output)
    plt.close()
    
    print("Report generated:", report_output)
    print("CSV file saved:", csv_output)
    print("Bar chart saved:", chart_output)

if __name__ == "__main__":
    main()
