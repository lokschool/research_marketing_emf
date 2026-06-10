#!/usr/bin/env python3
"""Proper audit - check for actual content (li/p tags), not text-stripped length."""
import os, re

website_dir = "/Users/lok/Project/MarketUnderstanding/outputs/website"
truly_empty = []

for fname in sorted(os.listdir(website_dir)):
    if fname == "index.html" or fname == "summary.html" or not fname.endswith(".html"):
        continue
    
    path = os.path.join(website_dir, fname)
    with open(path) as f:
        html = f.read()
    
    name = fname.replace(".html", "").replace("_", " ").title()
    issues_for_company = []
    
    # Check each major section for actual HTML content
    sections = [
        "Business Model", "Target Customers", "Events Conducted",
        "Event Scale", "Event Types", "Event Themes",
        "Digital Transformation Maturity", "Tech Stack",
        "Hiring Signals", "Reviews &amp; Media", 
        "Geographic Presence", "Expansion Signals"
    ]
    
    for section in sections:
        idx = html.find(f"<h3>{section}</h3>")
        if idx < 0:
            continue
        end = html.find("</div>", idx)
        if end < 0:
            end = html.find("<h3>", idx + len(section) + 10)
        if end < 0:
            end = idx + 500
        
        snippet = html[idx:end]
        # Count actual content elements
        li_count = len(re.findall(r'<li>', snippet))
        p_count = len(re.findall(r'<p>', snippet))
        strong_count = len(re.findall(r'<strong>', snippet))
        em_count = len(re.findall(r'<em>', snippet))
        
        total_elements = li_count + p_count
        if total_elements == 0:
            # Truly empty - no visible content
            issues_for_company.append(section)
    
    # Check pain points
    if "No detailed pain point analysis" in html:
        issues_for_company.append("Pain Points (placeholder)")
    
    # Check solution fit
    fit_start = html.find('WeExpand Solution Fit</h2>')
    if fit_start > 0:
        fit_end = html.find('</section>', fit_start)
        fit_html = html[fit_start:fit_end]
        has_table = '<table' in fit_html
        has_strategy = 'Strategic Opportunity' in fit_html
        has_opportunity = 'opportunity-card' in fit_html
        if not has_table and not has_strategy:
            issues_for_company.append("Solution Fit (no table or strategy)")
    
    if issues_for_company:
        truly_empty.append((name, fname, issues_for_company))

if truly_empty:
    print(f"=== {len(truly_empty)} COMPANIES WITH TRULY EMPTY SECTIONS ===\n")
    for name, fname, issues in truly_empty:
        print(f"✗ {name} ({len(issues)} empty sections):")
        for i in issues:
            print(f"    - {i}")
else:
    print("✓ All companies have content in all sections!")

print(f"\n{len(truly_empty)} companies need fixes")
