#!/usr/bin/env python3
"""Post-process all company HTML pages to inject teammate collaboration data."""
import os, json, re

WEBSITE_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/website"
MERGED_JSON = os.path.join(WEBSITE_DIR, "merged_data.json")

with open(MERGED_JSON) as f:
    md = json.load(f)

# Map company names to slugs using name matching
def slug_match(name, html_files):
    name_lower = name.lower().replace("(", "").replace(")", "").replace("-", " ")
    for hf in html_files:
        hf_name = hf.replace(".html", "").replace("_", " ").replace("-", " ")
        if name_lower in hf_name or hf_name in name_lower:
            return hf
        # Try first 3 words
        nw = " ".join(name_lower.split()[:3])
        hw = " ".join(hf_name.split()[:3])
        if nw == hw:
            return hf
    return None

html_files = [f for f in os.listdir(WEBSITE_DIR) if f.endswith(".html") and f not in ("index.html", "summary.html", "merged_report.html")]

injected = 0
for c in md["companies"]:
    tm_data = c
    match = slug_match(c["name"], html_files)
    if not match:
        continue
    
    has_contact = tm_data.get("contacts") and len(tm_data.get("contacts", [])) > 0
    has_outreach = tm_data.get("outreach") and len(tm_data["outreach"]) > 20
    has_insights = tm_data.get("insights_t2") and len(tm_data.get("insights_t2", [])) > 0
    
    if not (has_contact or has_outreach or has_insights):
        continue
    
    path = os.path.join(WEBSITE_DIR, match)
    with open(path) as f:
        html = f.read()
    
    # Build teammate section HTML
    section = '\n<section id="team" class="section">\n<div class="container" style="max-width:1100px;margin:0 auto;padding:0 20px;">\n<h2 class="section-title">Teammate Collaboration Data</h2>\n<div class="card">\n<p style="color:#888;margin-bottom:16px;">Additional intelligence contributed by team members during collaborative research phase.</p>\n'
    
    if has_contact:
        section += '<h3>📇 Key Contacts (Teamate 1)</h3><div style="display:grid;gap:8px;">\n'
        for contact in tm_data["contacts"][:5]:
            name = contact.get("name", "")
            role = contact.get("role", "")
            if name:
                section += f'<div style="padding:8px 12px;background:#f8fafc;border-radius:6px;border:1px solid #e9ecef;"><strong>{name}</strong><br><small style="color:#888;">{role}</small></div>\n'
        section += '</div>\n'
    
    if has_outreach:
        outreach = tm_data["outreach"][:400].replace("<", "&lt;").replace(">", "&gt;")
        section += f'<h3 style="margin-top:16px;">🎯 Suggested Outreach Angle (Teamate 1)</h3><p style="font-size:0.9rem;">{outreach}</p>\n'
    
    if has_insights:
        section += '<h3 style="margin-top:16px;">💡 Strategic Insights (Teamate 2)</h3><ul style="font-size:0.9rem;">\n'
        for insight in tm_data["insights_t2"][:5]:
            if len(insight) > 20:
                clean = insight[:200].replace("<", "&lt;").replace(">", "&gt;")
                section += f'<li>{clean}</li>\n'
        section += '</ul>\n'
    
    section += '</div>\n</div>\n</section>\n'
    
    # Inject before </body>
    if "</body>" in html:
        html = html.replace("</body>", section + "\n</body>")
        with open(path, "w") as f:
            f.write(html)
        injected += 1
        print(f"  ✓ {c['name']}: injected teammate data")

print(f"\n✅ Injected teammate data into {injected} company pages")
