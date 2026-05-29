#!/usr/bin/env python3
"""Audit all company HTML pages for blank sections."""
import os, re

website_dir = "/Users/lok/Project/MarketUnderstanding/outputs/website"
issues = []

for fname in sorted(os.listdir(website_dir)):
    if fname == "index.html" or fname == "summary.html" or not fname.endswith(".html"):
        continue
    
    path = os.path.join(website_dir, fname)
    with open(path) as f:
        html = f.read()
    
    name = fname.replace(".html", "").replace("_", " ").title()
    size = len(html)
    
    # Check for very small pages (likely incomplete)
    if size < 3000:
        issues.append(f"  ✗ {name}: Very small page ({size} bytes)")
    
    # Check pain points
    if "No detailed pain point analysis" in html:
        issues.append(f"  ✗ {name}: Pain Points — placeholder text")
    
    # Check solution fit section is not empty
    fit_start = html.find('<h2 class="section-title">WeExpand Solution Fit</h2>')
    if fit_start > 0:
        fit_end = html.find('</section>', fit_start)
        fit_html = html[fit_start:fit_end]
        fit_text = re.sub(r'<[^>]+>', '', fit_html).strip()
        if len(fit_text) < 30:
            issues.append(f"  ✗ {name}: Solution Fit — empty ({len(fit_text)} chars)")
    
    # Check key sections for content
    sections_to_check = [
        "Business Model", "Target Customers", "Events Conducted",
        "Event Scale", "Digital Transformation Maturity", "Tech Stack",
        "Hiring Signals", "Geographic Presence", "Expansion Signals"
    ]
    
    for section in sections_to_check:
        # Find the section
        idx = html.find(f"<h3>{section}</h3>")
        if idx < 0:
            issues.append(f"  ✗ {name}: '{section}' — section missing")
            continue
        
        # Extract content until next h3 or closing div
        next_h3 = html.find("<h3>", idx + len(section) + 10)
        end_div = html.find("</div>", idx)
        end = min(next_h3, end_div) if next_h3 > 0 else end_div
        if end < 0:
            end = idx + 500
        
        content = html[idx:end]
        text = re.sub(r'<[^>]+>', '', content).strip()
        # Remove the section title itself
        text = text.replace(section, "").strip()
        
        # Very short content = effectively blank
        if len(text) < 15:
            issues.append(f"  ✗ {name}: '{section}' — nearly empty ({len(text)} chars)")

print(f"=== AUDIT: {len(issues)} issues found ===\n")
for issue in sorted(issues):
    print(issue)

# Count unique companies
affected = set()
for i in issues:
    name = i.split(":")[0].replace("  ✗ ", "").strip()
    affected.add(name)

print(f"\n{len(affected)} unique companies affected")
print(f"{46 - len(affected)} companies are complete ✓")
