#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import json
import webbrowser
import hashlib
from collections import defaultdict

# --------------------------------------------------
# Embedded CSV data for the relevant SNPs:
# --------------------------------------------------
CSV_DATA = """Condition(s),Gene,rsID,Evidence/Status,Ancestry Note,Notes/References
"MCAS, Autism/ADHD","TPSAB1","rs1861759","Preliminary/unconfirmed; alpha tryptase CNV is main known factor","Claimed Neanderthal","User-cited duplication variant. Main evidence is for hereditary alpha tryptasemia rather than autism/ADHD. Minimal mainstream support."
"MCAS, Autism/ADHD","TPSAB1","rs113578744","Preliminary/unconfirmed; alpha tryptase CNV is main known factor","Claimed Neanderthal","Same gene duplication rationale as rs1861759. MCAS-like symptoms can result from extra copies of alpha tryptase; data on ADHD/autism link are speculative."
"MCAS, Autism/ADHD","TPSAB1","rs140863677","Strong association with hereditary alpha tryptasemia","Claimed Neanderthal","Found in individuals with elevated tryptase levels; associated with MCAS-like symptoms."
"MCAS, Autism/ADHD, POTS","ADRA1A","rs1048101","Preliminary; alpha-adrenergic receptor SNP linked to autonomic dysfunction","Claimed Neanderthal","Weakly associated with POTS and autonomic dysregulation."
"POTS, MCAS, Lupus, RA","HLA-B","rs144921697","Preliminary/unconfirmed; MHC region well known in autoimmunity","Claimed Neanderthal","HLA-B is implicated in autoimmune disease, but specific SNP evidence is less established for POTS/MCAS."
"POTS, MCAS, Lupus, RA","HLA-B","rs17878979","Preliminary/unconfirmed; MHC region well known in autoimmunity","Claimed Neanderthal","Similar commentary as rs144921697. MHC variants can influence broad autoimmunity risk."
"MCAS, Autism/ADHD, MS","IL2RA","rs2104286","Known association with autoimmune conditions (e.g., T1D, MS)","Claimed Neanderthal","IL2RA (CD25) is crucial in immune regulation. Clear link with MS; MCAS/autism associations are not well established."
"EDS/hEDS","COL5A1","rs12721431","Preliminary/unconfirmed; possible collagen regulation SNP","Claimed Neanderthal","COL5A1 is central in classical EDS; hEDS genetics remain elusive. Minimal data on this specific rs."
"EDS/hEDS, Fibromyalgia","TGFB2","rs2272785","Preliminary/unconfirmed","Claimed Neanderthal","TGFB2 variants known in some connective tissue disorders (e.g., Loeys-Dietz), but data for hEDS/fibromyalgia are sparse."
"EDS/hEDS, Fibromyalgia","TGFB1","rs1800469","Preliminary/unconfirmed","Claimed Neanderthal","Promoter polymorphism C-509T in TGFB1; some small studies tie it to fibrosis or chronic pain. Not definitively validated for hEDS."
"EDS/hEDS, RA, Lupus","TNXB","rs1063325","Preliminary/unconfirmed","Claimed Neanderthal","Biallelic TNXB deficiency can mimic classical-like EDS. Specific SNP association with RA/Lupus is not well replicated."
"EDS/hEDS, RA, Lupus","TNXB","rs652722","Preliminary/unconfirmed","Claimed Neanderthal","Similar to rs1063325. TNXB implicated in rare forms of EDS; broader autoimmune overlap not strongly established."
"EDS/hEDS, POTS, Autism/ADHD","ACTN3","rs1815739","Well-known ‘R577X’ athlete variant, minimal EDS/POTS evidence","Claimed Viking","ACTN3 influences fast-twitch muscle fibers. No strong mainstream data linking it to EDS, POTS, or neurodevelopmental disorders."
"EDS/hEDS, POTS, Autism/ADHD","ACTN3","rs7308816","Preliminary/unconfirmed","Claimed Viking","Less-studied ACTN3 SNP. ‘Viking origin’ is speculative, primarily associated with athletic performance studies."
"EDS/hEDS, POTS, MCAS","NOS1AP","rs6944656","Preliminary/unconfirmed","Claimed Viking","NOS1AP studied mostly in QT-interval and diabetic neuropathy. ‘Viking Disease’ typically refers to Dupuytren’s contracture; tenuous link here."
"EDS/hEDS, POTS, MCAS","NOS1AP","rs28931567","Preliminary/unconfirmed","Claimed Viking","Same gene as rs6944656, limited mainstream evidence for EDS, POTS, MCAS association."
"Autism/ADHD, MCAS, Fibromyalgia","MC1R","rs1805007","Common red-hair variant, minimal direct link to these disorders","Claimed Neanderthal","MC1R variants sometimes associated with altered pain sensitivity. ‘Neanderthal origin’ is a popular myth, not firmly established."
"Autism/ADHD, MCAS, Fibromyalgia","COMT","rs4680","Widely studied in psychiatric/pain contexts","Claimed Neanderthal","Val158Met influences dopamine metabolism, pain, cognition. Some archaic haplotypes in COMT, but details remain unclear."
"Autism/ADHD, MCAS, Fibromyalgia","MAOA","rs6323","Preliminary/unconfirmed","Claimed Neanderthal","MAOA influences monoamine metabolism. Evidence for direct link to MCAS/fibromyalgia is marginal."
"Autism/ADHD, MCAS, Fibromyalgia","SLC6A4","rs25531","Promoter polymorphism near 5-HTTLPR","Claimed Neanderthal","Involved in serotonin transporter function. Many inconsistent links to neuropsychiatric or pain disorders."
"Autism/ADHD, MCAS, Fibromyalgia","DRD4","rs1800955","Promoter SNP, ADHD association replicated","Claimed Neanderthal","DRD4 is a well-known ADHD gene (especially 7R VNTR). Direct MCAS/fibro link is not widely established."
"Autism/ADHD, MCAS, Fibromyalgia","GABRA2","rs3729984","Preliminary/unconfirmed","Claimed Neanderthal","GABRA2 variants studied in addiction/psychiatric traits. Limited data for MCAS/fibro."
"ALS, MS, Lupus, RA","APOE","rs769449","Preliminary/unconfirmed for these autoimmune/ALS contexts","Claimed Neanderthal","APOE ε4 is well known for Alzheimer’s risk, some small association signals in MS/ALS, not firmly validated."
"ALS, MS, Lupus, RA","TP53","rs1042522","Arg72Pro variant with cancer relevance, minimal direct link here","Claimed Neanderthal","Occasionally studied in neurodegeneration or autoimmune, but data are not conclusive."
"MS, Lupus, RA, Fibromyalgia","VDR","rs731236","‘BsmI’ variant in vitamin D receptor","Claimed Neanderthal","Vitamin D pathways widely studied in autoimmune disorders. Conflicting or modest results across diseases."
"MS, Lupus, RA, Fibromyalgia","HSP70 (HSPA1A)","rs2075800","Preliminary/unconfirmed","Claimed Neanderthal","Heat shock proteins can modulate inflammation. Some studies link HSP70 SNPs to autoimmune severity."
"MS, Lupus, RA, Fibromyalgia","IFITM3","rs12252","Preliminary/unconfirmed; known for infection susceptibility","Claimed Neanderthal","IFITM3 primarily studied for viral infections (influenza/COVID-19). Autoimmune/fibro links are less established."
"""

# Function to parse the CSV data
def parse_snp_csv(csv_data):
    snp_dict = {}
    reader = csv.DictReader(csv_data.strip().splitlines())
    for row in reader:
        rs_id = row["rsID"].strip()
        snp_dict[rs_id] = {
            "Conditions": row["Condition(s)"].strip(),
            "Gene": row["Gene"].strip(),
            "Evidence": row["Evidence/Status"].strip(),
            "Ancestry": row["Ancestry Note"].strip(),
            "Notes": row["Notes/References"].strip()
        }
    return snp_dict

# Function to generate a unique ID based on file hash and salt
def generate_unique_id(file_path, salt):
    sha1 = hashlib.sha1()
    sha1.update(salt.encode('utf-8'))
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha1.update(chunk)
    return sha1.hexdigest()

def main():
    user_file = input("Enter the path to your 23andMe raw data TXT file: ").strip()
    if not os.path.isfile(user_file):
        print(f"ERROR: File not found: {user_file}")
        return
    
    unique_id = generate_unique_id(user_file, "caveman")
    print(f"Generated Unique ID: {unique_id}")
    
    snps_of_interest = parse_snp_csv(CSV_DATA)
    
    user_snps = {}
    with open(user_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            rs_id = parts[0]
            genotype = parts[3]
            user_snps[rs_id] = genotype
    
    gene_map = defaultdict(list)
    for rs_id, info in snps_of_interest.items():
        gene_map[info["Gene"]].append((rs_id, info))
    
    sorted_genes = sorted(gene_map.keys())
    
    # HTML Report
    html_lines = []
    html_lines.append("<!DOCTYPE html>")
    html_lines.append("<html lang='en'>")
    html_lines.append("<head>")
    html_lines.append("  <meta charset='UTF-8' />")
    html_lines.append(f"  <title>🧬Modern Neanderthal Sensitivity Report - {unique_id}🧬</title>")
    html_lines.append("""  
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      h1, h2 {
        text-align: center;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 40px;
      }
      th, td {
        border: 1px solid #ccc;
        padding: 8px;
      }
      th {
        background-color: #f0f0f0;
        text-align: left;
      }
      .present {
        color: green;
        font-weight: bold;
      }
      .missing {
        color: red;
        font-weight: bold;
      }
    </style>
    """)
    html_lines.append("</head>")
    html_lines.append("<body>")
    html_lines.append(f"<h1>🧬Modern Neanderthal Sensitivity Report🧬</h1>")
    html_lines.append(f"<h2>Unique ID: {unique_id}</h2>")
    html_lines.append("<p>This report examines selected SNPs (Single Nucleotide Polymorphisms) in your 23andMe data. Each SNP has a unique identifier (rsID) and corresponds to a specific location in your genome. Your <strong>genotype</strong> shows the two variants of DNA you inherited at that location.</p>")
    html_lines.append("<p><strong>Important:</strong> This report is for educational purposes only. It is not a substitute for professional genomic testing or medical advice. Consult a qualified healthcare professional for interpretation and guidance.</p>")
    
    for gene in sorted_genes:
        html_lines.append(f"<h3>Gene: {gene}</h3>")
        html_lines.append("<table>")
        html_lines.append("""
          <tr>
            <th>rsID</th>
            <th>Conditions</th>
            <th>Present?</th>
            <th>Genotype</th>
            <th>Evidence/Status</th>
            <th>Ancestry Note</th>
            <th>Notes</th>
          </tr>
        """)
        gene_map[gene].sort(key=lambda x: x[0])
        for rs_id, info in gene_map[gene]:
            present = rs_id in user_snps
            genotype = user_snps[rs_id] if present else "NOT FOUND"
            presence_str = "<span class='present'>Present</span>" if present else "<span class='missing'>Missing</span>"
            row_html = f"""
              <tr>
                <td>{rs_id}</td>
                <td>{info['Conditions']}</td>
                <td>{presence_str}</td>
                <td>{genotype}</td>
                <td>{info['Evidence']}</td>
                <td>{info['Ancestry']}</td>
                <td>{info['Notes']}</td>
              </tr>
            """
            html_lines.append(row_html)
        html_lines.append("</table>")
    
    html_lines.append("<hr />")
    html_lines.append("<p><em>End of Report</em></p>")
    html_lines.append("</body></html>")
    
    report_html = "\n".join(html_lines)
    
    # JSON Report
    json_report = {"UniqueID": unique_id}
    for gene in sorted_genes:
        gene_map[gene].sort(key=lambda x: x[0])
        snp_list = []
        for rs_id, info in gene_map[gene]:
            present = rs_id in user_snps
            genotype = user_snps[rs_id] if present else "NOT FOUND"
            record = {
                "rsID": rs_id,
                "Conditions": info["Conditions"],
                "PresentIn23andMe": present,
                "Genotype": genotype,
                "EvidenceStatus": info["Evidence"],
                "AncestryNote": info["Ancestry"],
                "Notes": info["Notes"],
            }
            snp_list.append(record)
        json_report[gene] = snp_list
    
    # Save reports
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    html_report_path = os.path.join(downloads_dir, f"ND-Sensitivity-Report-{unique_id}.html")
    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(report_html)
    
    json_report_path = os.path.join(downloads_dir, f"ND-Sensitivity-Report-{unique_id}.json")
    with open(json_report_path, "w", encoding="utf-8") as jf:
        json.dump(json_report, jf, indent=2)
    
    print(f"\nHTML report saved to: {html_report_path}")
    print(f"JSON report saved to: {json_report_path}")
    
    webbrowser.open("file://" + html_report_path)

if __name__ == "__main__":
    main()
