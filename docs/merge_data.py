#!/usr/bin/env python3
"""Extract data from teammates' HTML files and merge with my work into one unified report."""
import os, re, json

T1_DIR = "/Users/lok/Project/MarketUnderstanding/otherTeamateWork/teamate1"
T2_DIR = "/Users/lok/Project/MarketUnderstanding/otherTeamateWork/teamate2"
MY_JSON = "/Users/lok/Project/MarketUnderstanding/outputs/website/summary_data.json"

with open(MY_JSON) as f:
    my_data = json.load(f)

# Map company names to slug for matching
my_slugs = {c["name"].lower(): c["slug"] for c in my_data["companies"]}
my_by_slug = {c["slug"]: c for c in my_data["companies"]}

def extract_teamate1_data(html):
    """Extract data from teamate1's HTML format"""
    data = {}
    
    # Company name from title
    title_m = re.search(r'<title>(.+?) \| EMF Company Intelligence</title>', html)
    if title_m:
        data["name"] = title_m.group(1).strip()
    
    # Contacts
    contacts = []
    contact_blocks = re.findall(r'<div class="contact">(.*?)</div>', html, re.DOTALL)
    for cb in contact_blocks:
        name_m = re.search(r'<strong>(.+?)</strong>', cb)
        role_m = re.search(r'<span>(.+?)</span>', cb)
        contacts.append({
            "name": name_m.group(1) if name_m else "",
            "role": role_m.group(1) if role_m else ""
        })
    if contacts:
        data["contacts"] = contacts
    
    # Pain points
    pain_section = re.search(r'EMF Workflow Pain Points</h2>(.*?)(?=<h2|</section)', html, re.DOTALL)
    if pain_section:
        pains = re.findall(r'<strong>(.+?)</strong>(.*?)(?=<strong>|</div)', pain_section.group(1), re.DOTALL)
        data["pains_from_t1"] = [{"title": p[0].strip(), "desc": re.sub(r'<[^>]+>', '', p[1]).strip()[:200]} for p in pains[:5]]
    
    # Solution mapping
    sol_section = re.search(r'WeExpand Solution Mapping</h2>(.*?)(?=<h2|</section)', html, re.DOTALL)
    if sol_section:
        maps = re.findall(r'<strong>(.+?)</strong>\s*<span>(.+?)</span>', sol_section.group(1))
        data["solution_from_t1"] = [{"pain": m[0].strip(), "weexpand": m[1].strip()} for m in maps[:5]]
    
    # AI Fit
    fit_m = re.search(r'AI Fit</h2>.*?<div[^>]*>(\d+)/10', html, re.DOTALL)
    if fit_m:
        data["t1_fit_score"] = int(fit_m.group(1))
    
    # Outreach angle
    outreach_m = re.search(r'Suggested First Outreach Angle</h2>(.*?)(?=<h2)', html, re.DOTALL)
    if outreach_m:
        data["outreach"] = re.sub(r'<[^>]+>', '', outreach_m.group(1)).strip()[:300]
    
    # Sources
    sources = re.findall(r'https?://[^\s"\'<>]+', html)
    data["t1_sources"] = list(set([s for s in sources if len(s) > 20 and "google" not in s.lower()]))[:8]
    
    return data

def extract_teamate2_data(html):
    """Extract data from teamate2's HTML format"""
    data = {}
    
    title_m = re.search(r'<title>(.+?) \| Strategic Enterprise Analysis', html)
    if title_m:
        data["name"] = title_m.group(1).strip()
    
    # Pain points / challenges
    pains = re.findall(r'<h3[^>]*>(.+?)</h3>\s*<p[^>]*>(.+?)</p>', html, re.DOTALL)
    data["t2_challenges"] = [{"title": p[0].strip(), "desc": re.sub(r'<[^>]+>', '', p[1]).strip()[:200]} for p in pains[:8]]
    
    # Key data points
    emp_m = re.search(r'(\d[\d,]*)\s*employees', html)
    if emp_m:
        data["t2_employees"] = emp_m.group(1)
    
    # Strategic insights
    insights = re.findall(r'<li>(.+?)</li>', html)
    data["t2_insights"] = [re.sub(r'<[^>]+>', '', i).strip()[:200] for i in insights[:10]]
    
    # Sources
    sources = re.findall(r'https?://[^\s"\'<>]+', html)
    data["t2_sources"] = list(set([s for s in sources if len(s) > 20]))[:8]
    
    return data

# Process Teamate1
t1_companies = []
for entry in os.listdir(T1_DIR):
    entry_path = os.path.join(T1_DIR, entry)
    if os.path.isdir(entry_path):
        html_path = os.path.join(entry_path, "index.html")
    elif entry == "index.html":
        continue  # Skip index
    else:
        continue
    
    if os.path.exists(html_path):
        with open(html_path) as f:
            html = f.read()
        data = extract_teamate1_data(html)
        if data.get("name"):
            t1_companies.append(data)

print(f"Teamate1: {len(t1_companies)} companies extracted")

# Process Teamate2
t2_companies = []
for entry in os.listdir(T2_DIR):
    if entry.endswith(".html"):
        path = os.path.join(T2_DIR, entry)
        with open(path) as f:
            html = f.read()
        data = extract_teamate2_data(html)
        if data.get("name"):
            t2_companies.append(data)

print(f"Teamate2: {len(t2_companies)} companies extracted")

# Build merged data
def fuzzy_match(name, candidates):
    """Fuzzy match company name to my data"""
    name_lower = name.lower().replace("(", "").replace(")", "").replace("-", " ").replace("_", " ")
    # Direct match
    for c in candidates:
        if name_lower == c["name"].lower():
            return c
    # Partial match
    words = set(name_lower.split())
    for c in candidates:
        c_words = set(c["name"].lower().split())
        if len(words & c_words) >= 3:
            return c
    # First word match
    first_word = name_lower.split()[0]
    for c in candidates:
        if c["name"].lower().startswith(first_word):
            return c
    return None

merged = []
for mc in my_data["companies"]:
    entry = {
        "name": mc["name"],
        "slug": mc["slug"],
        "employees": mc["employees"],
        "fit_score": mc["fit_score"],
        "fit_level": mc["fit_level"],
        "pain_count": mc["pain_count"],
        "type": mc["type"],
        "source": "me",
    }
    
    # Match with teamate1
    t1m = fuzzy_match(mc["name"], t1_companies)
    if t1m:
        if "contacts" in t1m:
            entry["contacts"] = t1m["contacts"]
        if "pains_from_t1" in t1m:
            entry["pains_t1"] = t1m["pains_from_t1"]
        if "solution_from_t1" in t1m:
            entry["solution_t1"] = t1m["solution_from_t1"]
        if "outreach" in t1m:
            entry["outreach"] = t1m["outreach"]
        entry["has_t1"] = True
    
    # Match with teamate2
    t2m = fuzzy_match(mc["name"], t2_companies)
    if t2m:
        if "t2_challenges" in t2m:
            entry["challenges_t2"] = t2m["t2_challenges"]
        if "t2_insights" in t2m:
            entry["insights_t2"] = t2m["t2_insights"]
        entry["has_t2"] = True
    
    merged.append(entry)

# Add unique entries not in my CSV
for t1c in t1_companies:
    if not fuzzy_match(t1c["name"], my_data["companies"]):
        merged.append({
            "name": t1c["name"],
            "slug": t1c["name"].lower().replace(" ", "-").replace("(", "").replace(")", ""),
            "employees": 0,
            "fit_score": t1c.get("t1_fit_score", 0),
            "fit_level": "N/A",
            "pain_count": len(t1c.get("pains_from_t1", [])),
            "type": "Unknown",
            "source": "teamate1",
            "has_t1": True,
            "contacts": t1c.get("contacts", []),
            "pains_t1": t1c.get("pains_from_t1", []),
            "outreach": t1c.get("outreach", ""),
        })

for t2c in t2_companies:
    if not fuzzy_match(t2c["name"], my_data["companies"]):
        merged.append({
            "name": t2c["name"],
            "slug": t2c["name"].lower().replace(" ", "-").replace("(", "").replace(")", ""),
            "employees": int(t2c.get("t2_employees", "0").replace(",", "")) if t2c.get("t2_employees") else 0,
            "fit_score": 0,
            "fit_level": "N/A",
            "pain_count": len(t2c.get("t2_challenges", [])),
            "type": "Unknown",
            "source": "teamate2",
            "has_t2": True,
            "challenges_t2": t2c.get("t2_challenges", []),
            "insights_t2": t2c.get("t2_insights", []),
        })

# Save merged data
out = "/Users/lok/Project/MarketUnderstanding/outputs/website/merged_data.json"
with open(out, "w") as f:
    json.dump({"total": len(merged), "companies": merged}, f, indent=2)

print(f"\nMERGED: {len(merged)} total companies ({len(my_data['companies'])} me + {len([c for c in merged if c['source']=='teamate1'])} t1-unique + {len([c for c in merged if c['source']=='teamate2'])} t2-unique)")
print(f"Companies with all 3 sources: {len([c for c in merged if c.get('has_t1') and c.get('has_t2')])}")
print(f"Companies with t1 only: {len([c for c in merged if c.get('has_t1') and not c.get('has_t2')])}")
print(f"Companies with t2 only: {len([c for c in merged if c.get('has_t2') and not c.get('has_t1')])}")
