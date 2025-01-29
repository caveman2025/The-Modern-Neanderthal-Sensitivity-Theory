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
"ALS, MS, Lupus, RA",TP53,rs1042522,"Arg72Pro variant with cancer relevance, minimal direct link here",Claimed Neanderthal,"Occasionally studied in neurodegeneration or autoimmune, but data are not conclusive."
"MCAS, Autism/ADHD, POTS",ADRA1A,rs1048101,Medium Confidence,Claimed Neanderthal,"Impacts adrenergic receptors, potentially affecting autonomic function."
"EDS/hEDS, RA, Lupus",TNXB,rs1063325,Medium Confidence,Claimed Neanderthal,Implicated in classical-like EDS and rare connective tissue disorders.
Taste Perception,TAS2R38,rs1080985,Low Confidence,Claimed Neanderthal,TAS2R38 variant associated with bitter taste perception; may influence food preferences.
Skin Pigmentation,PRSS53,rs11150614,Low Confidence,Claimed Neanderthal,PRSS53 variant linked to skin pigmentation and possibly autoimmune conditions.
"MCAS, Autism/ADHD",TPSAB1,rs113578744,High Confidence,Claimed Neanderthal,"Affects tryptase levels, possibly influencing MCAS-like symptoms."
"MS, Lupus, RA, Fibromyalgia",IFITM3,rs12252,Preliminary/unconfirmed; known for infection susceptibility,Claimed Neanderthal,IFITM3 primarily studied for viral infections (influenza/COVID-19). Autoimmune/fibro links are less established.
EDS/hEDS,COL5A1,rs12721431,Preliminary/unconfirmed; possible collagen regulation SNP,Claimed Neanderthal,"COL5A1 is central in classical EDS; May influence collagen regulation, with possible links to EDS."
Skin/Eye Pigmentation,HERC2,rs12896399,Low Confidence,Claimed Neanderthal,HERC2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility.
Skin Pigmentation,SLC24A5,rs1393350,Low Confidence,Claimed Neanderthal,SLC24A5 variant linked to skin pigmentation and possibly autoimmune conditions.
"MCAS, Autism/ADHD",TPSAB1,rs140863677,Strong association with hereditary alpha tryptasemia,Claimed Neanderthal,"Found in individuals with elevated tryptase levels; associated with MCAS-like symptoms. Strongly linked to hereditary alpha tryptasemia, a trait inherited from Neanderthals."
"POTS, MCAS, Lupus, RA",HLA-B,rs144921697,Preliminary/unconfirmed; MHC region well known in autoimmunity,Claimed Neanderthal,"HLA-B is implicated in autoimmune disease, but specific SNP evidence is less established for POTS/MCAS."
"POTS, MCAS, Lupus, RA",HLA-B,rs17878979,Preliminary/unconfirmed; MHC region well known in autoimmunity,Claimed Neanderthal,Similar commentary as rs144921697. MHC variants can influence broad autoimmunity risk.
Skin/Eye Pigmentation,OCA2,rs1800401,Low Confidence,Claimed Neanderthal,OCA2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility.
Skin/Eye Pigmentation,OCA2,rs1800407,Low Confidence,Claimed Neanderthal,OCA2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility.
Skin/Eye Pigmentation,OCA2,rs1800414,Low Confidence,Claimed Neanderthal,OCA2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility.
"EDS/hEDS, Fibromyalgia",TGFB1,rs1800469,Preliminary/unconfirmed,Claimed Neanderthal,Promoter polymorphism C-509T in TGFB1; some small studies tie it to fibrosis or chronic pain. Not definitively validated for hEDS.
"Autism/ADHD, MCAS, Fibromyalgia",DRD4,rs1800955,"Promoter SNP, ADHD association replicated",Claimed Neanderthal,DRD4 is a well-known ADHD gene shown to influence cognitive traits (especially 7R VNTR). Direct MCAS/fibro link is not widely established.
"Autism/ADHD, MCAS, Fibromyalgia",MC1R,rs1805007,"Common red-hair variant, minimal direct link to these disorders",Claimed Neanderthal,"MC1R variants sometimes associated with altered pain sensitivity. ‘Neanderthal origin’ is a popular myth, not firmly established."
"Skin/Hair Pigmentation, Pain Sensitivity",MC1R,rs1805009,Low Confidence,Claimed Neanderthal,MC1R variant linked to skin and hair pigmentation; may influence pain sensitivity.
"Skin/Hair Pigmentation, Pain Sensitivity",MC1R,rs1805015,Low Confidence,Claimed Neanderthal,MC1R variant associated with skin and hair pigmentation; may influence pain sensitivity.
"EDS/hEDS, POTS, Autism/ADHD",ACTN3,rs1815739,"Well-known ‘R577X’ athlete variant, minimal EDS/POTS evidence",Claimed Viking,"ACTN3 influences fast-twitch muscle fibers. No strong mainstream data linking it to EDS, POTS, or neurodevelopmental disorders."
"MCAS, Autism/ADHD",TPSAB1,rs1861759,High Confidence,Claimed Neanderthal,"Associated with hereditary alpha tryptasemia, linked to mast cell activation."
"MS, Lupus, RA, Fibromyalgia",HSP70 (HSPA1A),rs2075800,Preliminary/unconfirmed,Claimed Neanderthal,Heat shock proteins can modulate inflammation. Some studies link HSP70 SNPs to autoimmune severity. HSP70 variant linked to inflammatory response modulation.
"MCAS, Autism/ADHD, MS",IL2RA,rs2104286,"Known association with autoimmune conditions (e.g., T1D, MS)",Claimed Neanderthal,IL2RA (CD25) is crucial in immune regulation. Clear link with MS; MCAS/autism associations are not well established.
"MCAS, Autism/ADHD, MS",IL2RA,rs2104286,Medium Confidence,Claimed Neanderthal,Associated with autoimmune conditions such as multiple sclerosis.
Skin Pigmentation,SLC24A4,rs2228488,Low Confidence,Claimed Neanderthal,SLC24A4 variant associated with skin pigmentation and possibly autoimmune conditions.
Skin Pigmentation,SLC24A4,rs2229303,Low Confidence,Claimed Neanderthal,SLC24A4 variant linked to skin pigmentation and possibly autoimmune conditions.
"EDS/hEDS, Fibromyalgia",TGFB2,rs2272785,Preliminary/unconfirmed,Claimed Neanderthal,"TGFB2 variants known in some connective tissue disorders (e.g., Loeys-Dietz), but data for hEDS/fibromyalgia are sparse."
"EDS/hEDS, Fibromyalgia",TGFB2,rs2272785,Low Confidence,Claimed Neanderthal,Possible role in connective tissue disorders.
"Autism/ADHD, MCAS, Fibromyalgia",SLC6A4,rs25531,Promoter polymorphism near 5-HTTLPR,Claimed Neanderthal,Involved in serotonin transporter function. Many inconsistent links to neuropsychiatric or pain disorders.
"Autism/ADHD, MCAS, Fibromyalgia",SLC6A4,rs25531,Medium Confidence,Claimed Neanderthal,Impacts serotonin transporter function.
"EDS/hEDS, POTS, MCAS",NOS1AP,rs28931567,Preliminary/unconfirmed,Claimed Viking,"Same gene as rs6944656, limited mainstream evidence for EDS, POTS, MCAS association."
"Autism/ADHD, MCAS, Fibromyalgia",GABRA2,rs3729984,Preliminary/unconfirmed,Claimed Neanderthal,GABRA2 variants studied in addiction/psychiatric traits. Limited data for MCAS/fibro.
"Autism/ADHD, MCAS, Fibromyalgia",GABRA2,rs3729984,Medium Confidence,Claimed Neanderthal,GABRA2 variant studied for psychiatric and addiction traits.
"Autism/ADHD, MCAS, Fibromyalgia",COMT,rs4680,Widely studied in psychiatric/pain contexts,Claimed Neanderthal,"Val158Met influences dopamine metabolism, pain, cognition. Some archaic haplotypes in COMT, but details remain unclear."
"Autism/ADHD, MCAS, Fibromyalgia",COMT,rs4680,High Confidence,Claimed Neanderthal,Affects dopamine metabolism and cognitive function (COMT gene).
Skin Pigmentation,OCA2,rs4988235,Low Confidence,Claimed Neanderthal,OCA2 variant linked to skin pigmentation and possibly autoimmune susceptibility.
"Autism/ADHD, MCAS, Fibromyalgia",MAOA,rs6323,Preliminary/unconfirmed,Claimed Neanderthal,"MAOA Influences monoamine metabolism, possibly affecting ADHD risk. Evidence for direct link to MCAS/fibromyalgia is marginal."
"EDS/hEDS, RA, Lupus",TNXB,rs652722,Preliminary/unconfirmed,Claimed Neanderthal,Similar to rs1063325. TNXB implicated in rare forms of EDS and autoimmune conditions.
"EDS/hEDS, RA, Lupus",TNXB,rs652722,Medium Confidence,Claimed Neanderthal,"Similar to rs1063325, with possible roles in EDS and autoimmune conditions."
"EDS/hEDS, POTS, MCAS",NOS1AP,rs6944656,Preliminary/unconfirmed,Claimed Viking,NOS1AP  ‘Viking Disease’ typically refers to Dupuytren’s contracture. Associated with QT-interval modulation and possible autonomic dysfunction.
"EDS/hEDS, POTS, Autism/ADHD",ACTN3,rs7308816,Preliminary/unconfirmed,Claimed Viking,"Less-studied ACTN3 SNP. ‘Viking origin’ is speculative, primarily associated with athletic performance studies."
"EDS/hEDS, POTS, Autism/ADHD",ACTN3,rs7308816,Low Confidence,Claimed Viking,"Variant of ACTN3, linked to fast-twitch muscle fiber efficiency."
"MS, Lupus, RA, Fibromyalgia",VDR,rs731236,‘BsmI’ variant in vitamin D receptor,Claimed Neanderthal,Vitamin D pathways receptor variant widely studied in autoimmune disorders with possible links found
"MS, Lupus, RA, Fibromyalgia",VDR,rs731236,Medium Confidence,Claimed Neanderthal,"Vitamin D receptor variant, with possible links to autoimmune conditions."
"ALS, MS, Lupus, RA",APOE,rs769449,Preliminary/unconfirmed for these autoimmune/ALS contexts,Claimed Neanderthal,"APOE ε4 is well known for Alzheimer’s risk, some small association signals in MS/ALS, not firmly validated."
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
    
    # Group the SNPs by gene
    gene_map = defaultdict(list)
    for rs_id, info in snps_of_interest.items():
        gene_map[info["Gene"]].append((rs_id, info))
    
    # Sort genes alphabetically for the table
    sorted_genes = sorted(gene_map.keys())
    
    # -----------------------------------------------------------
    # Generate the HTML Report with Dark/Modern styling
    # -----------------------------------------------------------
    html_lines = []
    html_lines.append("<!DOCTYPE html>")
    html_lines.append("<html lang='en'>")
    html_lines.append("<head>")
    html_lines.append("  <meta charset='UTF-8' />")
    html_lines.append(f"  <title>🧬Modern Neanderthal Sensitivity Report - {unique_id}🧬</title>")
    # --- New dark/modern style block:
    html_lines.append("""
    <style>
      /* Basic Reset */
      html, body {
        margin: 0;
        padding: 0;
      }
      * {
        box-sizing: border-box;
      }

      /* Body: Dark Fluent-Inspired */
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #0D0D0D, #1C1C1C);
        color: #ECECEC;
        animation: fadeIn 0.8s ease-in-out forwards;
      }
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      /* Container */
      .container {
        max-width: 900px;
        margin: 40px auto;
        padding: 20px 30px;
        background-color: #242424;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
      }

      h1, h2, h3 {
        text-align: center;
        margin-bottom: 20px;
        color: #00FFC6; /* teal-like color for headings */
      }

      p {
        margin-bottom: 15px;
        line-height: 1.5;
      }

      /* Table Styles */
      table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-bottom: 40px;
        overflow: hidden;
        border-radius: 8px;
        background-color: #2C2C2C;
      }

      th, td {
        padding: 14px 16px;
        text-align: left;
      }

      th {
        background-color: #00FFC6;
        color: #1B1B1B;
        font-weight: 600;
      }

      tr:nth-child(even) td {
        background-color: #2A2A2A;
      }

      tr:hover td {
        background-color: #373737;
      }

      /* "Present"/"Missing" color styles */
      .present {
        color: #BBF7D0;
        font-weight: bold;
      }
      .missing {
        color: #FF6F6F;
        font-weight: bold;
      }

      /* Footer / End of Report */
      .footer {
        text-align: center;
        margin-top: 20px;
        font-style: italic;
        color: #888;
      }
    </style>
    """)
    html_lines.append("</head>")

    html_lines.append("<body>")
    html_lines.append("<div class='container'>")

    html_lines.append(f"<h1>🧬Modern Neanderthal Sensitivity Report🧬</h1>")
    html_lines.append(f"<h2>Unique ID: {unique_id}</h2>")

    html_lines.append("<p>This report examines selected SNPs (Single Nucleotide Polymorphisms) in your 23andMe data. Each SNP has a unique identifier (rsID) and corresponds to a specific location in your genome. Your <strong>genotype</strong> shows the two variants of DNA you inherited at that location.</p>")
    html_lines.append("<p><strong>Important:</strong> This report is for educational purposes only. It is not a substitute for professional genomic testing or medical advice. Consult a qualified healthcare professional for interpretation and guidance.</p>")

    # Build the tables by gene
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
        # Sort by rsID
        gene_map[gene].sort(key=lambda x: x[0])
        for rs_id, info in gene_map[gene]:
            present = rs_id in user_snps
            genotype = user_snps[rs_id] if present else "NOT FOUND"

            # color-coded "Present" / "Missing"
            presence_str = (
                "<span class='present'>Present</span>"
                if present else
                "<span class='missing'>Missing</span>"
            )

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

    html_lines.append("<div class='footer'>")
    html_lines.append("<hr />")
    html_lines.append("<p><em>End of Report</em></p>")
    html_lines.append("</div>")

    html_lines.append("</div>")  # close container
    html_lines.append("</body></html>")

    report_html = "\n".join(html_lines)
    
    # -----------------------------------------------------------
    #  Create JSON object
    # -----------------------------------------------------------
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

    # -----------------------------------------------------------
    # Save the reports
    # -----------------------------------------------------------
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    html_report_path = os.path.join(downloads_dir, f"ND-Sensitivity-Report-{unique_id}.html")
    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    json_report_path = os.path.join(downloads_dir, f"ND-Sensitivity-Report-{unique_id}.json")
    with open(json_report_path, "w", encoding="utf-8") as jf:
        json.dump(json_report, jf, indent=2)

    print(f"\nHTML report saved to: {html_report_path}")
    print(f"JSON report saved to: {json_report_path}")

    # Open HTML report in the default browser
    webbrowser.open("file://" + html_report_path)


if __name__ == "__main__":
    main()
