#!/usr/bin/env python3
"""Cross-check HTML pages vs summary data vs searched files for consistency."""
import os, re, json

website_dir = "/Users/lok/Project/MarketUnderstanding/outputs/website"
searched_dir = "/Users/lok/Project/MarketUnderstanding/outputs/searched"
reports_dir = "/Users/lok/Project/MarketUnderstanding/outputs/reports"

mismatches = []
noda_sections = []
total_checked = 0

with open(os.path.join(website_dir, "summary_data.json")) as f:
    summary = json.load(f)

for fname in sorted(os.listdir(website_dir)):
    if fname in ("index.html", "summary.html") or not fname.endswith(".html"):
        continue
    total_checked += 1
    
    path = os.path.join(website_dir, fname)
    with open(path) as f:
        html = f.read()
    
    slug = fname.replace(".html", "")
    
    emp_m = re.search(r'Employees</div>\s*<div[^>]*>(\d[\d,]*)<', html)
    fit_m = re.search(r'Solution Fit</div>\s*<div[^>]*>([^<]+)<', html)
    pain_m = re.search(r'Pain Points</div>\s*<div[^>]*>(\d+)<', html)
    
    html_emp = emp_m.group(1) if emp_m else "?"
    html_fit = fit_m.group(1) if fit_m else "?"
    html_pain = pain_m.group(1) if pain_m else "?"
    
    summary_match = None
    for c in summary["companies"]:
        if c["slug"] == slug:
            summary_match = c
            break
    
    issues = []
    
    if summary_match:
        sum_emp = str(summary_match["employees"])
        sum_pain = str(summary_match["pain_count"])
        html_fl = html_fit.split(" ")[0] if html_fit != "?" else "?"
        sum_fl = summary_match["fit_level"]
        
        if html_emp != sum_emp:
            issues.append(f"Emp: HTML={html_emp} vs JSON={sum_emp}")
        if html_pain != sum_pain:
            issues.append(f"Pain: HTML={html_pain} vs JSON={sum_pain}")
        if html_fl != sum_fl and html_fl != "N/A" and sum_fl != "N/A":
            issues.append(f"Fit: HTML={html_fl} vs JSON={sum_fl}")
    
    # Check "No public data found" sections
    ndf_sections = []
    for section in ["Business Model", "Events Conducted", "Tech Stack", "Hiring Signals", "Geographic Presence", "Expansion Signals"]:
        idx = html.find(f"<h3>{section}</h3>")
        if idx > 0:
            end = html.find("</div>", idx)
            if end < 0:
                end = html.find("<h3>", idx + 20)
            chunk = html[idx:end] if end > 0 else ""
            if "No public data found" in chunk:
                ndf_sections.append(section)
    
    if ndf_sections:
        issues.append(f"NoData sections: {', '.join(ndf_sections)}")
        noda_sections.extend([f"{slug}: {s}" for s in ndf_sections])
    
    # Check for raw markdown artifacts in strategic assessment
    strat_idx = html.find("Strategic Opportunity Assessment")
    if strat_idx > 0:
        strat_end = html.find("</div>", strat_idx)
        strat_chunk = html[strat_idx:strat_end] if strat_end > 0 else ""
        # Count ** that aren't converted to <strong>
        raw_bold = len(re.findall(r'\*\*[^*]+\*\*', strat_chunk))
        if raw_bold > 2:
            issues.append(f"Markdown in Strategy: {raw_bold} ** artifacts")
    
    if issues:
        company_name = slug.replace("_", " ").title()
        mismatches.append((company_name, issues))

print(f"=== CROSS-CHECK: {total_checked} companies ===")
print(f"Clean: {total_checked - len(mismatches)} | Issues: {len(mismatches)}")
print()

if mismatches:
    print("=== DATA MISMATCHES ===")
    for name, issues in mismatches:
        print(f"\n  {name}:")
        for i in issues:
            print(f"    - {i}")

if noda_sections:
    print(f"\n=== 'NO DATA FOUND' SECTIONS ({len(noda_sections)}) ===")
    for ns in noda_sections:
        print(f"  - {ns}")

# Summary vs Index check
print()
with open(os.path.join(website_dir, "index.html")) as f:
    idx_html = f.read()
idx_nums = re.findall(r'stat-num[^>]*>(\d+)<', idx_html)
print(f"=== INDEX vs SUMMARY ===")
print(f"Index: companies={idx_nums[1]}, high={idx_nums[2]}, med={idx_nums[3]}, pains={idx_nums[4]}")
print(f"Summary: companies={summary['total_companies']}, high={summary['fit_distribution']['High']}, med={summary['fit_distribution']['Medium']}, pains={summary['total_pain_points']}")
