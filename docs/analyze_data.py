#!/usr/bin/env python3
"""Analyze all pain point data and generate summary.json for the dashboard."""
import os, re, json
from collections import Counter

reports_dir = "/Users/lok/Project/MarketUnderstanding/outputs/reports"
searched_dir = "/Users/lok/Project/MarketUnderstanding/outputs/searched"

all_companies = []
pain_themes = Counter()
urgency_counts = Counter()

categories = {
    "Manual Sales & Client Acquisition": ["sales", "client acquisition", "lead generation", "manual", "network", "referral", "outreach", "business development", "pipeline", "sponsor", "delegate acquisition", "exhibitor sales", "BD"],
    "No Digital Platform": ["digital platform", "no digital", "digital gap", "online", "app", "portal", "self-service", "digital presence", "e-commerce", "digital event", "digital tools", "digital marketing"],
    "Year-Round Engagement Gap": ["year-round", "annual", "biennial", "11-month", "2-year", "between event", "community platform", "365", "episodic", "engagement gap", "dormant", "community monetization"],
    "Team Scalability Crisis": ["small team", "micro", "lean", "scalability", "headcount", "capacity", "growth bottleneck", "cannot scale", "team size", "bandwidth", "stretched", "cannot handle"],
    "No AI & Automation": ["AI", "automation", "manual process", "no AI", "machine learning", "smart", "chatbot", "AI-driven", "AI-powered"],
    "Data Monetization Gap": ["data", "analytics", "insight", "monetiz", "attendee data", "post-event", "CRM", "visitor data", "lead capture"],
    "Competitive Pressure": ["competition", "competitor", "rival", "market share", "disruption", "threat", "encroach", "competitive"],
    "Revenue Model Risk": ["revenue", "project-based", "recurring", "one-off", "cash flow", "margin", "capital intensive", "rental", "predictab"],
    "Geographic Concentration": ["Hong Kong", "single location", "geographic", "regional", "one city", "China-centric", "concentration", "local market", "one venue"],
    "Operational Risk": ["single point of failure", "key person", "dependency", "operational risk", "vulnerab", "continuity", "burnout", "key people"],
    "Policy & Regulatory Dependency": ["policy", "regulation", "government", "compliance", "geopolitical", "trade", "political"],
    "Brand & Marketing Gap": ["brand", "marketing", "visibility", "social media", "credentials", "certification", "reputation", "amplified"],
}

for fname in sorted(os.listdir(reports_dir)):
    if not fname.endswith("_report.md"):
        continue
    path = os.path.join(reports_dir, fname)
    with open(path) as f:
        text = f.read()
    
    slug = fname.replace("_report.md", "")
    name = slug.replace("_", " ").title()
    
    # Extract pain points with details
    pain_sections = re.split(r'### Pain Point \d+:', text)
    pains = []
    for sec in pain_sections[1:]:
        title = sec.strip().split('\n')[0].strip()
        ev_m = re.search(r'\*\*Evidence:\*\*\s*(.+?)(?:\n|$)', sec)
        imp_m = re.search(r'\*\*Impact:\*\*\s*(.+?)(?:\n|$)', sec)
        urg_m = re.search(r'\*\*Urgency:\*\*\s*(.+?)(?:\s*[—\-–]|\s*\n|\s*\.)', sec)
        
        urgency = urg_m.group(1).strip() if urg_m else "Medium"
        if "High" in urgency: urgency = "High"
        elif "Medium" in urgency: urgency = "Medium"
        elif "Low" in urgency: urgency = "Low"
        else: urgency = "Medium"
        
        urgency_counts[urgency] += 1
        
        pain_lower = title.lower()
        pain_cat = "Other"
        for cat, keywords in categories.items():
            if any(kw.lower() in pain_lower for kw in keywords):
                pain_cat = cat
                break
        pain_themes[pain_cat] += 1
        
        pains.append({
            "title": title,
            "evidence": ev_m.group(1).strip() if ev_m else "",
            "impact": imp_m.group(1).strip() if imp_m else "",
            "urgency": urgency,
            "category": pain_cat
        })
    
    # Fit score
    fit_m = re.search(r'(?:Overall\s*)?Fit:\s*\*?\*?\s*(High|Medium|Low|Moderate|Very High)\s*\((\d+)/10\)', text)
    if fit_m:
        raw = fit_m.group(1)
        if raw in ("Very High", "High"): fit_level = "High"
        elif raw in ("Moderate", "Medium"): fit_level = "Medium"
        else: fit_level = "Low"
        fit_score = int(fit_m.group(2))
    else:
        fit_level = "N/A"
        fit_score = 0
    
    # Employee count
    emp = 0
    searched_path = os.path.join(searched_dir, f"{slug}_searched.md")
    if not os.path.exists(searched_path):
        # Try alternate names
        for f2 in os.listdir(searched_dir):
            if f2.startswith(slug.split("_")[0]) and f2.endswith("_searched.md"):
                searched_path = os.path.join(searched_dir, f2)
                break
    if os.path.exists(searched_path):
        with open(searched_path) as sf:
            stext = sf.read()[:500]
        emp_m = re.search(r'(\d[\d,]*)\s*employees', stext)
        if emp_m:
            emp = int(emp_m.group(1).replace(",", ""))
    
    # Company type
    if "venue" in fname or "hotel" in fname or "sports park" in fname or "exhibition centre" in fname or "convention" in fname:
        comp_type = "Venue Operator"
    elif any(kw in fname for kw in ["production", "staging", "showtex", "syma", "milton", "exr", "expomobilia", "chunky", "serious"]):
        comp_type = "Event Production/Fabrication"
    elif any(kw in fname for kw in ["1000meetings", "keys", "pyjama"]):
        comp_type = "Platform/Marketplace"
    elif any(kw in fname for kw in ["informa", "rx_global", "clarion", "gl_events", "closerstill", "comasia", "adsale", "messe", "oliver"]):
        comp_type = "Large Exhibition Organizer"
    elif any(kw in fname for kw in ["beacon", "leader", "marintec", "jec", "rethink", "beyond", "token", "superai", "121", "aplf", "branded", "beauty", "infocomm", "mykar"]):
        comp_type = "Conference/Niche Event Organizer"
    elif any(kw in fname for kw in ["eventist", "filament", "teamrite", "noah", "fuel", "artcom", "branded"]):
        comp_type = "Creative/Marketing Agency"
    else:
        comp_type = "Event Services"
    
    all_companies.append({
        "name": name,
        "slug": slug,
        "employees": emp,
        "fit_level": fit_level,
        "fit_score": fit_score,
        "pain_count": len(pains),
        "pains": pains,
        "type": comp_type
    })

# Build summary
high_fit = [c for c in all_companies if c["fit_level"] == "High"]
medium_fit = [c for c in all_companies if c["fit_level"] == "Medium"]
total_pains = sum(c["pain_count"] for c in all_companies)
total_emp = sum(c["employees"] for c in all_companies)

# Employee groups
emp_groups = {"Micro (1-20)": 0, "Small (21-100)": 0, "Medium (101-500)": 0, "Large (501+)": 0}
for c in all_companies:
    if c["employees"] <= 0: emp_groups["Micro (1-20)"] += 1
    elif c["employees"] <= 20: emp_groups["Micro (1-20)"] += 1
    elif c["employees"] <= 100: emp_groups["Small (21-100)"] += 1
    elif c["employees"] <= 500: emp_groups["Medium (101-500)"] += 1
    else: emp_groups["Large (501+)"] += 1

# Market opportunity tiers
tier1 = [c for c in all_companies if c["fit_score"] >= 8]  # Prime targets
tier2 = [c for c in all_companies if 6 <= c["fit_score"] <= 7]  # Strong prospects
tier3 = [c for c in all_companies if c["fit_score"] <= 5]  # Niche plays

summary = {
    "total_companies": len(all_companies),
    "total_employees": total_emp,
    "total_pain_points": total_pains,
    "avg_pains_per_company": round(total_pains / len(all_companies), 1),
    "fit_distribution": {"High": len(high_fit), "Medium": len(medium_fit), "Low/N/A": len(all_companies) - len(high_fit) - len(medium_fit)},
    "urgency_distribution": dict(urgency_counts.most_common()),
    "pain_categories": dict(pain_themes.most_common()),
    "employee_groups": emp_groups,
    "tier1_prime": [{"name": c["name"], "slug": c["slug"], "score": c["fit_score"], "employees": c["employees"], "type": c["type"], "pains": c["pain_count"]} for c in tier1],
    "tier2_strong": [{"name": c["name"], "slug": c["slug"], "score": c["fit_score"], "employees": c["employees"], "type": c["type"], "pains": c["pain_count"]} for c in tier2],
    "tier3_niche": [{"name": c["name"], "slug": c["slug"], "score": c["fit_score"], "employees": c["employees"], "type": c["type"], "pains": c["pain_count"]} for c in tier3],
    "top_pains": [{"company": c["name"], "slug": c["slug"], "count": c["pain_count"], "fit": c["fit_level"]} for c in sorted(all_companies, key=lambda x: x["pain_count"], reverse=True)[:10]],
    "companies": all_companies
}

out = "/Users/lok/Project/MarketUnderstanding/outputs/website/summary_data.json"
with open(out, "w") as f:
    json.dump(summary, f, indent=2)

print(f"✅ Summary data generated: {out}")
print(f"   {summary['total_companies']} companies, {summary['total_pain_points']} pain points")
print(f"   High fit: {summary['fit_distribution']['High']}, Medium: {summary['fit_distribution']['Medium']}")
print(f"   Tier 1 (Prime): {len(tier1)}, Tier 2 (Strong): {len(tier2)}, Tier 3 (Niche): {len(tier3)}")
