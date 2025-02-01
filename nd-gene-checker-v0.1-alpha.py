#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import webbrowser
import hashlib
import json

# --------------------------------------------------
# Updated Confidence Weighting System
# --------------------------------------------------
CONFIDENCE_WEIGHTS = {
    "High Confidence": 4,
    "Medium Confidence": 3,
    "Low Confidence": 2,
}

# --------------------------------------------------
# Updated SNP List
# --------------------------------------------------
NEANDERTHAL_SNPS = {
    "rs1861759": ("High Confidence", "Associated with hereditary alpha tryptasemia, linked to mast cell activation."),
    "rs113578744": ("High Confidence", "Affects tryptase levels, possibly influencing MCAS-like symptoms."),
    "rs140863677": ("High Confidence", "Strongly linked to hereditary alpha tryptasemia, a trait inherited from Neanderthals."),
    "rs1048101": ("Medium Confidence", "Impacts adrenergic receptors, potentially affecting autonomic function."),
    "rs144921697": ("Medium Confidence", "Located in the MHC region, may influence immune response."),
    "rs17878979": ("Medium Confidence", "Similar to rs144921697, with potential effects on autoimmune susceptibility."),
    "rs2104286": ("Medium Confidence", "Associated with autoimmune conditions such as multiple sclerosis."),
    "rs12721431": ("Medium Confidence", "May influence collagen regulation, with possible links to EDS."),
    "rs2272785": ("Low Confidence", "Possible role in connective tissue disorders."),
    "rs1800469": ("Low Confidence", "Affects TGF-beta signaling, which plays a role in fibrosis and chronic pain."),
    "rs1063325": ("Medium Confidence", "Implicated in classical-like EDS and rare connective tissue disorders."),
    "rs652722": ("Medium Confidence", "Similar to rs1063325, with possible roles in EDS and autoimmune conditions."),
    "rs1815739": ("Low Confidence", "Affects muscle function; commonly studied in athletic performance."),
    "rs7308816": ("Low Confidence", "Variant of ACTN3, linked to fast-twitch muscle fiber efficiency."),
    "rs6944656": ("Medium Confidence", "Associated with QT-interval modulation and possible autonomic dysfunction."),
    "rs28931567": ("Medium Confidence", "Similar to rs6944656; limited evidence for POTS or MCAS association."),
    "rs1805007": ("High Confidence", "Common red-hair variant; sometimes associated with altered pain sensitivity."),
    "rs4680": ("High Confidence", "Affects dopamine metabolism and cognitive function (COMT gene)."),
    "rs6323": ("Medium Confidence", "Influences monoamine metabolism, possibly affecting ADHD risk."),
    "rs25531": ("Medium Confidence", "Impacts serotonin transporter function."),
    "rs1800955": ("High Confidence", "DRD4 promoter SNP; associated with ADHD and cognitive traits."),
    "rs3729984": ("Medium Confidence", "GABRA2 variant studied for psychiatric and addiction traits."),
    "rs769449": ("Medium Confidence", "APOE variant known for potential links to Alzheimer's and neurodegeneration."),
    "rs1042522": ("Low Confidence", "p53 gene variant occasionally studied in autoimmune and neurodegenerative conditions."),
    "rs731236": ("Medium Confidence", "Vitamin D receptor variant, with possible links to autoimmune conditions."),
    "rs2075800": ("Medium Confidence", "HSP70 variant linked to inflammatory response modulation."),
    "rs12252": ("Low Confidence", "IFITM3 variant known for viral infection susceptibility."),
    "rs1080985": ("Low Confidence", "TAS2R38 variant associated with bitter taste perception; may influence food preferences."),
    "rs4988235": ("Low Confidence", "OCA2 variant linked to skin pigmentation and possibly autoimmune susceptibility."),
    "rs1805015": ("Low Confidence", "MC1R variant associated with skin and hair pigmentation; may influence pain sensitivity."),
    "rs2229303": ("Low Confidence", "SLC24A4 variant linked to skin pigmentation and possibly autoimmune conditions."),
    "rs12896399": ("Low Confidence", "HERC2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility."),
    "rs1393350": ("Low Confidence", "SLC24A5 variant linked to skin pigmentation and possibly autoimmune conditions."),
    "rs1800414": ("Low Confidence", "OCA2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility."),
    "rs1805009": ("Low Confidence", "MC1R variant linked to skin and hair pigmentation; may influence pain sensitivity."),
    "rs2228488": ("Low Confidence", "SLC24A4 variant associated with skin pigmentation and possibly autoimmune conditions."),
    "rs11150614": ("Low Confidence", "PRSS53 variant linked to skin pigmentation and possibly autoimmune conditions."),
    "rs1800401": ("Low Confidence", "OCA2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility."),
    "rs1800407": ("Low Confidence", "OCA2 variant associated with skin and eye pigmentation; may influence autoimmune susceptibility."),
    "rs12498609": ("Medium Confidence", "Neanderthal-derived variant linked to immune system regulation; function not fully understood."),
    "rs1156361": ("Medium Confidence", "Neanderthal-derived variant in the TLR1 gene; may influence innate immune response."),
    "rs4846049": ("Low Confidence", "Neanderthal-derived variant in the STAT2 gene; function poorly understood."),
    "rs1881227": ("Medium Confidence", "Neanderthal-derived variant in the KLF4 gene; may play a role in skin barrier function."),
    "rs1260326": ("Medium Confidence", "Neanderthal-derived variant in the GCKR gene; associated with metabolic traits."),
    "rs3795061": ("Low Confidence", "Neanderthal-derived variant in the SLC16A11 gene; linked to type 2 diabetes risk."),
    "rs9303521": ("Low Confidence", "Neanderthal-derived variant in the POU2F3 gene; function not fully understood."),
    "rs10490770": ("Medium Confidence", "Neanderthal-derived variant in the SLC6A11 gene; may influence neurotransmitter transport."),
    "rs1042658": ("Low Confidence", "Neanderthal-derived variant in the HYAL2 gene; function poorly understood."),
    "rs12191877": ("Medium Confidence", "Neanderthal-derived variant in the FOXP2 gene; may influence speech and language development."),
    "rs10013927": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs10477613": ("Low Confidence", "May influence visual perception and processing speed."),
    "rs10521422": ("Medium Confidence", "Associated with auditory processing and language development."),
    "rs10734515": ("Low Confidence", "Possible role in olfactory perception and processing."),
    "rs10833250": ("Medium Confidence", "Linked to cognitive flexibility and problem-solving ability."),
    "rs10927880": ("Low Confidence", "May influence tactile perception and sensory processing."),
    "rs11090765": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs11249053": ("Low Confidence", "Possible role in cognitive processing speed and attention."),
    "rs11347702": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs11550499": ("Low Confidence", "May influence cognitive flexibility and executive function."),
    "rs11610106": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs11704115": ("Low Confidence", "Possible role in olfactory perception and processing."),
    "rs11843595": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs12124819": ("Low Confidence", "May influence tactile perception and sensory processing."),
    "rs12278743": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs12325567": ("Low Confidence", "Possible role in cognitive processing speed and attention."),
    "rs12411045": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs12509864": ("Low Confidence", "May influence cognitive flexibility and executive function."),
    "rs12604783": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs12728265": ("Low Confidence", "Possible role in olfactory perception and processing."),
    "rs12822717": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs12900589": ("Low Confidence", "May influence tactile perception and sensory processing."),
    "rs13004413": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs13131026": ("Low Confidence", "Possible role in cognitive processing speed and attention."),
    "rs13274337": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs13401138": ("Low Confidence", "May influence cognitive flexibility and executive function."),
    "rs1352025": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs1369904": ("Low Confidence", "Possible role in olfactory perception and processing."),
    "rs1384586": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs1407447": ("Low Confidence", "May influence tactile perception and sensory processing."),
    "rs1427763": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs1433848": ("Low Confidence", "Possible role in cognitive processing speed and attention."),
    "rs1453624": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1460592": ("Low Confidence", "May influence cognitive flexibility and executive function."),
    "rs1472417": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs1483418": ("Low Confidence", "Possible role in olfactory perception and processing."),
    "rs1501933": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs1511792": ("Low Confidence", "May influence tactile perception and sensory processing."),
    "rs1520324": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs1531612": ("Low Confidence", "Possible role in cognitive processing speed and attention."),
    "rs1540017": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1552424": ("Low Confidence", "May influence cognitive flexibility and executive function."),
    "rs1561582": ("Medium Confidence", "Associated with visual perception and processing speed."),
    "rs1573212": ("Low Confidence", "Possible role in olfactory perception and processing."),
    "rs1580173": ("Medium Confidence", "Linked to cognitive function, particularly attention and working memory."),
    "rs1590103": ("Low Confidence", "May influence tactile perception and sensory processing."),
    "rs1600247": ("Medium Confidence", "Associated with visual-spatial skills and mental rotation."),
    "rs1610403": ("Low Confidence", "Possible role in cognitive processing speed and attention."),
    "rs1621913": ("Medium Confidence", "Linked to auditory working memory and language processing."),
    "rs1630298": ("Low Confidence", "May influence cognitive flexibility and executive function."),
    "rs1801157": ("Medium Confidence", "COL3A1 gene variant associated with EDS type IV."),
    "rs2274703": ("Low Confidence", "COL5A1 gene variant linked to classical EDS."),
    "rs17165664": ("Medium Confidence", "COL5A2 gene variant associated with classical EDS."),
    "rs1042074": ("Low Confidence", "COL1A1 gene variant linked to EDS and osteoporosis."),
    "rs1063325": ("Medium Confidence", "TNXB gene variant associated with classical-like EDS."),
    "rs11556924": ("Medium Confidence", "Height and skeletal growth, potential link to EDS."),
    "rs1801252": ("Medium Confidence", "ADRB1 gene variant linked to POTS and autonomic dysfunction."),
    "rs1805015": ("Low Confidence", "MC1R gene variant associated with POTS and skin pigmentation."),
    "rs2229303": ("Low Confidence", "SLC24A4 gene variant linked to POTS and skin pigmentation."),
    "rs12190992": ("Medium Confidence", "NOS1AP gene variant associated with POTS and QT-interval modulation."),
    "rs12401481": ("Medium Confidence", "COMT gene variant linked to POTS and autonomic dysfunction."),
    "rs4307059": ("Medium Confidence", "CDH9 gene variant associated with autism and social behavior."),
    "rs4307059": ("Medium Confidence", "SHANK3 gene variant linked to autism and intellectual disability."),
    "rs11765443": ("Low Confidence", "SLC6A4 gene variant associated with autism and serotonin transport."),
    "rs1858830": ("Medium Confidence", "OXTR gene variant linked to autism and social behavior."),
    "rs2298585": ("Low Confidence", "ITGB3 gene variant associated with autism and platelet function."),
    "rs1800955": ("High Confidence", "DRD4 gene variant linked to ADHD, autism, and cognitive traits."),
    "rs4680": ("High Confidence", "COMT gene variant associated with ADHD, autism, and cognitive traits."),
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

# --------------------------------------------------
# Function to Calculate Neanderthal DNA Score
# --------------------------------------------------
def calculate_neanderthal_score(user_snps):
    """
    Calculates the Neanderthal score based on how many
    of the listed NEANDERTHAL_SNPS appear in the user's data.
    """
    score = 0
    for rs_id, (confidence, _) in NEANDERTHAL_SNPS.items():
        if rs_id in user_snps:
            score += CONFIDENCE_WEIGHTS[confidence]
    return score

# --------------------------------------------------
# Main Function
# --------------------------------------------------
def main():
    user_file = input("Enter the path to your 23andMe raw data TXT file: ").strip()
    if not os.path.isfile(user_file):
        print(f"ERROR: File not found: {user_file}")
        return

    # Read entire file as bytes for hashing
    with open(user_file, "rb") as f:
        file_contents = f.read()

    # Create a SHA-1 hash object with the salt "caveman"
    hash_obj = hashlib.sha1()
    hash_obj.update("caveman".encode("utf-8"))  # Salting
    hash_obj.update(file_contents)
    unique_id = hash_obj.hexdigest()
    print(f"Generated Unique ID: {unique_id}")

    # Parse user SNPs in text mode
    user_snps = set()
    with open(user_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            if len(parts) >= 4:
                user_snps.add(parts[0])

    # Calculate Neanderthal score
    score = calculate_neanderthal_score(user_snps)

    # -------------------------------------------------------------------
    # Prepare data for both HTML and JSON
    # -------------------------------------------------------------------
    # 1) Table Rows for HTML
    # 2) Structured data for JSON

    snp_rows_html = ""
    snp_list_json = []

    for rs_id, (confidence, description) in NEANDERTHAL_SNPS.items():
        present = rs_id in user_snps
        present_str_html = "<span style='color: #BBF7D0; font-weight: bold;'>TRUE</span>" if present else "<span style='color: #FF6F6F; font-weight: bold;'>FALSE</span>"
        snp_rows_html += f"<tr><td>{rs_id}</td><td>{present_str_html}</td><td>{description}</td></tr>"

        snp_list_json.append({
            "rs_id": rs_id,
            "confidence": confidence,
            "description": description,
            "present": present
        })

    # -----------------------------------------------------------
    #  Create JSON object
    # -----------------------------------------------------------
    json_data = {
        "unique_id": unique_id,
        "score": score,
        "total_snps_tested": len(NEANDERTHAL_SNPS),
        "snps": snp_list_json
    }

    # -----------------------------------------------------------
    # Generate HTML Report (Dark/Modern Theme)
    # -----------------------------------------------------------
    html_content = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
      <meta charset='UTF-8' />
      <title>🦴 Neanderthal DNA Estimator Report 🦴</title>
      <style>
        /* Basic Reset */
        html, body {{
          margin: 0;
          padding: 0;
        }}
        * {{
          box-sizing: border-box;
        }}

        /* Body: Dark Fluent-Inspired */
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: linear-gradient(135deg, #0D0D0D, #1C1C1C);
          color: #ECECEC;
          animation: fadeIn 0.8s ease-in-out forwards;
        }}
        @keyframes fadeIn {{
          from {{ opacity: 0; }}
          to {{ opacity: 1; }}
        }}

        /* Container */
        .container {{
          max-width: 900px;
          margin: 40px auto;
          padding: 20px 30px;
          background-color: #242424;
          border-radius: 10px;
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }}

        h1, h2, h3 {{
          text-align: center;
          margin-bottom: 20px;
          color: #00FFC6;
        }}

        /* Score Paragraph */
        .score {{
          font-size: 1.2rem;
          text-align: center;
          margin-bottom: 30px;
          color: #BBF7D0;
        }}

        /* Table Styles */
        table {{
          width: 100%;
          border-collapse: separate;
          border-spacing: 0;
          margin-bottom: 40px;
          overflow: hidden;
          border-radius: 8px;
          background-color: #2C2C2C;
        }}

        th, td {{
          padding: 14px 16px;
          text-align: left;
        }}

        th {{
          background-color: #00FFC6;
          color: #1B1B1B;
          font-weight: 600;
        }}

        tr:nth-child(even) td {{
          background-color: #2A2A2A;
        }}

        tr:hover td {{
          background-color: #373737;
        }}

        /* Footer / End of Report */
        .footer {{
          text-align: center;
          margin-top: 20px;
          font-style: italic;
          color: #888;
        }}
      </style>
    </head>
    <body>
    <div class="container">
      <h1>🦴 Neanderthal DNA Estimator 🦴</h1>
      <h2>Unique ID: {unique_id}</h2>
      <p class="score"><strong>Your Neanderthal Score:</strong> {score} / {len(NEANDERTHAL_SNPS)}</p>

      <h3>All Tested SNPs</h3>
      <table>
          <tr><th>rsID</th><th>Gene Present in 23&Me Data?</th><th>Description</th></tr>
          {snp_rows_html}
      </table>

      <div class="footer">
        <hr />
        <p><em>End of Report</em></p>
      </div>
    </div>
    </body></html>
    """

    # -----------------------------------------------------------
    # Save Outputs (HTML + JSON) to Downloads folder
    # -----------------------------------------------------------
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    base_filename = f"Neanderthal-DNA-Estimate-{unique_id}"

    # 1) HTML
    html_report_path = os.path.join(downloads_dir, base_filename + ".html")
    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 2) JSON
    json_report_path = os.path.join(downloads_dir, base_filename + ".json")
    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"\nHTML report saved to: {html_report_path}")
    print(f"JSON data saved to: {json_report_path}")

    # Open the HTML report automatically
    webbrowser.open("file://" + html_report_path)

if __name__ == "__main__":
    main()
