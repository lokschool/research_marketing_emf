#!/usr/bin/env python3
"""Redefine solution fit scoring with objective, data-driven criteria."""
import os, re, json, csv

REPORTS_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/reports"
SEARCHED_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/searched"
CSV_PATH = "/Users/lok/Project/MarketUnderstanding/df_company.csv"
SUMMARY_JSON = "/Users/lok/Project/MarketUnderstanding/outputs/website/summary_data.json"

# Load CSV
csv_data = {}
with open(CSV_PATH) as f:
    for row in csv.DictReader(f):
        csv_data[row["Company Name"].strip()] = row

# Load existing summary
with open(SUMMARY_JSON) as f:
    old_summary = json.load(f)

def score_company(name, emp, keywords, searched_text, report_text):
    """
    Score company fit for WeExpand based on 4 objective dimensions.
    Each dimension contributes 0-3 points. Max = 10.
    
    DIMENSION 1: EVENT DATA SCALE (0-3)
    How much attendee/exhibitor data flows through this company?
    """
    kw = keywords.lower()
    e = int(emp) if emp and emp.replace(",", "").isdigit() else 0
    st = searched_text.lower()[:3000]
    rt = report_text.lower()
    
    data_scale = 0
    
    # High data volume keywords
    if any(w in kw for w in ["visitor", "attendee", "exhibitor", "buyer", "delegate", "audience", "visitors"]):
        data_scale += 1
    if any(w in kw for w in ["trade show", "exhibition", "expo", "conference", "summit", "fair"]):
        data_scale += 1
    if any(w in kw for w in ["global", "international", "worldwide", "asia", "europe"]):
        data_scale += 1
    if e >= 100:  # larger company = more data
        data_scale += 1
    data_scale = min(data_scale, 3)
    
    # DIMENSION 2: AUTOMATION OPPORTUNITY (0-4)
    # How much would AI/automation transform their operations?
    auto_opp = 0
    
    # Manual/traditional indicators
    manual_indicators = ["manual", "traditional", "conventional", "network", "referral", "personal"]
    if any(w in kw for w in manual_indicators):
        auto_opp += 1
    if not any(w in kw for w in ["ai ", "artificial intelligence", "machine learning", "automation", "automated", "bot", "chatbot"]):
        auto_opp += 1  # no AI evidence
    
    # Long event gaps (annual/biennial = big automation win for year-round)
    if any(w in kw for w in ["annual", "biennial", "yearly"]):
        auto_opp += 1
    
    # Sales/marketing keywords (automation target)
    if any(w in kw for w in ["sales", "marketing", "lead generation", "sponsor", "outreach", "business development", "bd"]):
        auto_opp += 1
    auto_opp = min(auto_opp, 4)
    
    # DIMENSION 3: TEAM LEVERAGE (0-3)
    # How much would AI multiply the team's output?
    leverage = 0
    if 0 < e <= 15:
        leverage += 3  # micro team, massive multiplier
    elif 15 < e <= 50:
        leverage += 2  # small team, big multiplier
    elif 50 < e <= 200:
        leverage += 1  # mid team, good multiplier
    elif e > 200:
        leverage += 2  # large team, enterprise-scale opportunity
    
    # Multi-event/multi-client operations
    if any(w in kw for w in ["multiple", "portfolio", "series", "various", "diverse"]):
        leverage += 1
    leverage = min(leverage, 3)
    
    # DIMENSION 4: TECH RECEPTIVITY (0-1)
    # Would they be receptive to AI adoption?
    tech_rec = 0
    if any(w in kw for w in ["technology", "digital", "tech", "innovation", "platform", "software", "app", "online"]):
        tech_rec += 1
    # Penalty for pure hardware/rental (limited software play)
    if any(w in kw for w in ["manufacturing", "fabrication", "equipment rental", "tent", "marquee"]) and \
       not any(w in kw for w in ["software", "platform", "digital", "saas", "technology"]):
        tech_rec -= 1
    
    total = data_scale + auto_opp + leverage + max(tech_rec, 0)
    return min(max(total, 0), 10)

# Re-score all companies
results = []
for fname in sorted(os.listdir(REPORTS_DIR)):
    if not fname.endswith("_report.md"): continue
    path = os.path.join(REPORTS_DIR, fname)
    with open(path) as f: rtext = f.read()
    
    # Get company name
    nm = re.search(r'# (.+?) —', rtext)
    name = nm.group(1) if nm else fname.replace("_report.md","")
    
    # Find CSV row
    csv_row = None
    for cn, row in csv_data.items():
        sn = name.lower().replace(" ","_").replace("(","").replace(")","")
        cn_s = cn.lower().replace(" ","_").replace("(","").replace(")","")
        if sn in cn_s or cn_s in sn or sn.split("_")[0] == cn_s.split("_")[0]:
            csv_row = row; break
    
    emp = csv_row.get("# Employees", "0") if csv_row else "0"
    kw = csv_row.get("Keywords", "") if csv_row else ""
    
    # Get searched file text
    slug = fname.replace("_report.md", "")
    stext = ""
    for sf in os.listdir(SEARCHED_DIR):
        if slug in sf or slug.split("_")[0] in sf:
            with open(os.path.join(SEARCHED_DIR, sf)) as f:
                stext = f.read()
            break
    
    new_score = score_company(name, emp, kw, stext, rtext)
    
    # Determine level
    if new_score >= 8: level = "High"
    elif new_score >= 5: level = "Medium"
    else: level = "Low"
    
    results.append((name, new_score, level, emp))

# Print distribution
print("=== NEW FIT SCORE DISTRIBUTION ===\n")
scores = [r[1] for r in results]
for s in sorted(set(scores)):
    count = scores.count(s)
    names = [r[0][:25] for r in results if r[1] == s]
    print(f"  {s}/10: {count:2d} companies — {', '.join(names[:5])}{'...' if len(names)>5 else ''}")

print(f"\n  High (8-10):  {sum(1 for s in scores if s >= 8)}")
print(f"  Medium (5-7): {sum(1 for s in scores if 5 <= s <= 7)}")  
print(f"  Low (0-4):    {sum(1 for s in scores if s <= 4)}")

# Update all reports with new scores
updated = 0
for name, score, level, emp in results:
    for fname in os.listdir(REPORTS_DIR):
        if not fname.endswith("_report.md"): continue
        sn = name.lower().replace(" ","_").replace("(","").replace(")","")
        fn = fname.replace("_report.md","")
        if sn in fn or fn in sn or sn.split("_")[0] == fn.split("_")[0]:
            path = os.path.join(REPORTS_DIR, fname)
            with open(path) as f: text = f.read()
            
            # Update first-line fit score
            text = re.sub(r'\*\*Fit:.*?\*\*', f'**Fit: {level} ({score}/10)**', text, count=1)
            # Update Overall Fit in strategy section
            text = re.sub(r'\*\*Overall Fit:\*\*\s*\*?\*?.*?\*?\*?', f'**Overall Fit:** **{level} ({score}/10)**', text)
            
            with open(path, "w") as f: f.write(text)
            updated += 1
            break

print(f"\n✅ Updated {updated} reports with new objective scores")
