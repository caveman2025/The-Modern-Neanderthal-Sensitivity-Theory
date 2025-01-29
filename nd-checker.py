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
    "High Confidence": 5,
    "Medium Confidence": 3,
    "Low Confidence": 1,
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
