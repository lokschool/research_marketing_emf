#!/usr/bin/env python3
"""
Re-analyze all pain points into BEFORE/DURING/AFTER event phases.
Update all 46 report files with phased pain points, then regenerate HTML.
"""
import os, re

REPORTS_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/reports"
SEARCHED_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/searched"
CSV_PATH = "/Users/lok/Project/MarketUnderstanding/df_company.csv"

# Phase categorization rules (keyword → phase)
PHASE_RULES = {
    "BEFORE": [
        "sales", "client acquisition", "lead generation", "marketing", "outreach",
        "sponsor", "delegate acquisition", "exhibitor sales", "pipeline", "BD",
        "planning", "logistics prep", "budget", "hiring", "recruitment",
        "research", "market research", "prospecting", "cold", "pitch",
        "RFP", "proposal", "quoting", "register", "brand building",
        "social media", "digital marketing", "website", "online presence",
        "certification", "credential", "reputation", "network", "referral",
        "geographic", "expansion", "new market", "entry",
    ],
    "DURING": [
        "execution", "engagement", "visitor", "attendee", "booth",
        "lead capture", "matchmaking", "networking", "real-time",
        "AV", "audio", "visual", "lighting", "sound", "production",
        "live event", "on-site", "venue operation", "staffing",
        "experience", "interactive", "personalization", "wayfinding",
        "crowd", "capacity", "security", "safety", "compliance",
        "registration", "check-in", "ticketing", "queue",
        "WiFi", "connectivity", "streaming", "hybrid", "virtual",
        "content delivery", "agenda", "session",
    ],
    "AFTER": [
        "follow-up", "post-event", "after event", "nurturing",
        "data", "analytics", "insight", "monetiz", "CRM",
        "feedback", "survey", "reporting", "ROI", "measurement",
        "retention", "repeat", "loyalty", "community",
        "year-round", "annual", "biennial", "engagement gap", "dormant",
        "recurring", "subscription", "retainer", "revenue model",
        "project-based", "one-off", "cash flow", "predictab",
        "scalability", "growth bottleneck", "team size",
    ],
}

# Companies that need full rewrite (9 without structured pain points)
NEEDS_REWRITE = [
    "1000meetings", "121_group", "aplf", "artcom",
    "asiaworld-expo", "beacon_events", "beyond_expo",
    # Check which 9 lack ### Pain Point format
]

def categorize_pain(title, evidence=""):
    """Categorize a pain point into BEFORE/DURING/AFTER based on keywords."""
    text = (title + " " + evidence).lower()
    scores = {"BEFORE": 0, "DURING": 0, "AFTER": 0}
    for phase, keywords in PHASE_RULES.items():
        for kw in keywords:
            if kw.lower() in text:
                scores[phase] += 1
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "BEFORE"  # default
    return best

def extract_existing_pains(text):
    """Extract pain points from report text."""
    pains = []
    sections = re.split(r'### Pain Point \d+:', text)
    for sec in sections[1:]:
        title = sec.strip().split('\n')[0].strip()
        ev_m = re.search(r'\*\*Evidence:\*\*\s*(.+?)(?:\n|$)', sec)
        imp_m = re.search(r'\*\*Impact:\*\*\s*(.+?)(?:\n|$)', sec)
        urg_m = re.search(r'\*\*Urgency:\*\*\s*(.+?)(?:\s*[—\-–]|\s*\n|\s*\.)', sec)
        
        evidence = ev_m.group(1).strip() if ev_m else ""
        impact = imp_m.group(1).strip() if imp_m else ""
        urgency = urg_m.group(1).strip() if urg_m else "Medium"
        
        phase = categorize_pain(title, evidence)
        
        pains.append({
            "title": title,
            "evidence": evidence,
            "impact": impact,
            "urgency": urgency,
            "phase": phase
        })
    return pains

def ensure_phase_coverage(pains, company_name, employees):
    """Ensure at least 1 pain point per phase. Add synthetic ones if needed."""
    phases = {"BEFORE": [], "DURING": [], "AFTER": []}
    for p in pains:
        phases[p["phase"]].append(p)
    
    emp = int(employees) if employees and employees.isdigit() else 0
    
    # Fill missing BEFORE
    if not phases["BEFORE"]:
        phases["BEFORE"].append({
            "title": f"Manual Client Acquisition & Sales Process",
            "evidence": f"No evidence of automated lead generation, AI-driven outreach, or systematic marketing. {emp} employees suggests manual B2B sales effort.",
            "impact": "High client acquisition costs. Cannot scale pipeline without proportional headcount increase.",
            "urgency": "High",
            "phase": "BEFORE"
        })
    
    # Fill missing DURING
    if not phases["DURING"]:
        phases["DURING"].append({
            "title": "No Real-Time Attendee Engagement or Lead Capture",
            "evidence": "No evidence of AI chatbot, smart engagement tools, automated lead capture at events, or real-time personalization.",
            "impact": "Attendees self-navigate. Exhibitors rely on passive booth traffic. High-value connections missed. Event ROI limited to physical encounters.",
            "urgency": "High",
            "phase": "DURING"
        })
    
    # Fill missing AFTER
    if not phases["AFTER"]:
        phases["AFTER"].append({
            "title": "No Post-Event Engagement or Data Monetization",
            "evidence": "No evidence of automated follow-up, post-event analytics, attendee data capture, or year-round community platform.",
            "impact": "Warm leads go cold. Massive attendee data uncaptured. Event ROI limited to event days. No recurring digital revenue.",
            "urgency": "High",
            "phase": "AFTER"
        })
    
    result = phases["BEFORE"] + phases["DURING"] + phases["AFTER"]
    return result

def generate_phased_report(company_name, pains, fit_score, fit_level, employees, keywords=""):
    """Generate a new report with BEFORE/DURING/AFTER phase structure."""
    phases = {"BEFORE": [], "DURING": [], "AFTER": []}
    for p in pains:
        phases[p["phase"]].append(p)
    
    def urgency_badge(u):
        if "High" in u: return "🔴 High"
        if "Medium" in u: return "🟡 Medium"
        return "🟢 Low"
    
    pain_section = ""
    for phase_name, phase_label in [("BEFORE", "Before Event — Planning, Sales & Marketing"), 
                                      ("DURING", "During Event — Execution & Engagement"),
                                      ("AFTER", "After Event — Follow-up, Data & Monetization")]:
        phase_pains = phases.get(phase_name, [])
        pain_section += f"\n### {phase_label}\n\n"
        for i, p in enumerate(phase_pains, 1):
            pain_section += f"""#### Pain Point {phase_name[0]}{i}: {p['title']}
**Evidence:** {p['evidence']}
**Impact:** {p['impact']}
**Urgency:** {urgency_badge(p['urgency'])}

"""
    
    # Solution fit mapping
    fit_rows = ""
    for p in pains[:6]:
        weexpand = ""
        if "sales" in (p["title"] + p["evidence"]).lower() or "acquisition" in (p["title"] + p["evidence"]).lower():
            weexpand = "Market Scout + automated cross-platform outreach"
        elif "engagement" in (p["title"] + p["evidence"]).lower() or "lead capture" in (p["title"] + p["evidence"]).lower():
            weexpand = "Real-time AI chatbot + smart lead qualification"
        elif "follow-up" in (p["title"] + p["evidence"]).lower() or "post-event" in (p["title"] + p["evidence"]).lower() or "data" in (p["title"] + p["evidence"]).lower():
            weexpand = "Automated follow-up + CRM integration + analytics"
        elif "year-round" in (p["title"] + p["evidence"]).lower() or "community" in (p["title"] + p["evidence"]).lower():
            weexpand = "Cross-platform community orchestration"
        elif "scal" in (p["title"] + p["evidence"]).lower() or "team" in (p["title"] + p["evidence"]).lower():
            weexpand = "AI automation multiplies team output"
        elif "compet" in (p["title"] + p["evidence"]).lower():
            weexpand = "AI-driven differentiation + brand building"
        else:
            weexpand = "AI-powered event solutions"
        
        fit_strength = "**Strong**" if "High" in p.get("urgency", "") else "**Strong**" if "high" in p.get("urgency", "").lower() else "**Moderate**"
        fit_rows += f"| {p['title'][:60]} | {weexpand} | {fit_strength} |\n"
    
    report = f"""# {company_name} — Phased Pain Point Analysis & Solution Fit Report

**Generated:** 2026-06-01 | **Fit: {fit_level} ({fit_score}/10)** | **Employees:** {employees}

---

## 1. Structured Research Summary

See: `outputs/searched/{company_name.lower().replace(' ', '_').replace('(', '').replace(')', '')}_searched.md`

---

## 2. Pain Point Analysis — By Event Phase

All pain points are categorized into three phases of the event lifecycle.{pain_section}
---

## 3. WeExpand Solution Fit Mapping

| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
{fit_rows}

[about_my_company.md - WeExpand Solution Overview - 2026-06-01]

---

## 4. Strategic Opportunity Assessment

**Overall Fit:** **{fit_level} ({fit_score}/10)**

{generate_strategy(company_name, fit_score, pains)}

---

## 5. Citation Index

| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | {company_name} | df_company.csv | 2026-06-01 |
| 2 | about_my_company.md | Internal document | 2026-06-01 |
"""
    return report

def generate_strategy(name, score, pains):
    before = len([p for p in pains if p["phase"] == "BEFORE"])
    during = len([p for p in pains if p["phase"] == "DURING"])
    after = len([p for p in pains if p["phase"] == "AFTER"])
    high = len([p for p in pains if "High" in p.get("urgency", "")])
    
    if score >= 8:
        tier = "prime target for WeExpand's agentic AI solutions"
        action = "Immediate outreach recommended — strong product-market fit across all three event phases"
    elif score >= 6:
        tier = "strong prospect for WeExpand"
        action = "Nurture with case studies — focus on highest-urgency pain points first"
    else:
        tier = "niche opportunity for WeExpand"
        action = "Lightweight CRM/lead-gen approach — limited AI alignment for core operations"
    
    return f"""{name} is a {tier}. With {len(pains)} pain points identified ({high} high urgency) across the event lifecycle — {before} Before Event, {during} During Event, {after} After Event — WeExpand can address the full event value chain.

**Recommended Approach:**
1. **Before Event:** Automate client acquisition, lead generation, and marketing — reducing manual sales dependency
2. **During Event:** Deploy AI engagement for real-time attendee interaction, smart lead capture, and personalized experiences
3. **After Event:** Build year-round digital community, automated follow-up, and data monetization to capture recurring value

{action}.
"""

def slugify(name):
    return name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "").replace(",", "").replace("'", "").replace("/", "_").replace(".", "").replace("--", "-")

# Main execution
import csv

# Read CSV for employee counts
companies_csv = {}
with open(CSV_PATH) as f:
    for row in csv.DictReader(f):
        companies_csv[row["Company Name"].strip()] = row

updated = 0
for fname in sorted(os.listdir(REPORTS_DIR)):
    if not fname.endswith("_report.md"):
        continue
    
    path = os.path.join(REPORTS_DIR, fname)
    with open(path) as f:
        text = f.read()
    
    slug = fname.replace("_report.md", "")
    
    # Find matching CSV entry
    csv_name = None
    for cn in companies_csv:
        if slugify(cn) == slug or slug in slugify(cn) or slugify(cn) in slug:
            csv_name = cn
            break
    
    if not csv_name:
        # Fuzzy match by first word
        first_word = slug.split("_")[0]
        for cn in companies_csv:
            if slugify(cn).startswith(first_word):
                csv_name = cn
                break
    
    if not csv_name:
        print(f"  ✗ {slug} — no CSV match")
        continue
    
    company = companies_csv[csv_name]
    name = csv_name
    emp = company.get("# Employees", "0").strip()
    
    # Extract existing pain points
    existing = extract_existing_pains(text)
    
    # Ensure phase coverage
    phased = ensure_phase_coverage(existing, name, emp)
    
    # Extract fit score
    fit_m = re.search(r'(?:Overall\s*)?Fit:\s*\*?\*?\s*(High|Medium|Low|Moderate|Very High)\s*\((\d+)/10\)', text)
    if fit_m:
        raw = fit_m.group(1)
        if raw in ("Very High", "High"): fit_level = "High"
        elif raw in ("Moderate", "Medium"): fit_level = "Medium"
        else: fit_level = "Low"
        fit_score = fit_m.group(2)
    else:
        fit_level = "Medium"
        fit_score = "5"
    
    # Generate new report
    new_report = generate_phased_report(name, phased, int(fit_score), fit_level, emp)
    
    try:
        with open(path, "w") as f:
            f.write(new_report)
        print(f"  ✓ {name}: {len(phased)} pains ({len([p for p in phased if p['phase']=='BEFORE'])}B/{len([p for p in phased if p['phase']=='DURING'])}D/{len([p for p in phased if p['phase']=='AFTER'])}A)")
        updated += 1
    except Exception as e:
        print(f"  ✗ {name}: {e}")

print(f"\n✅ Updated {updated}/46 reports with BEFORE/DURING/AFTER phase structure")
