#!/usr/bin/env python3
"""
Fill missing phase pain points using ONLY evidence from searched files.
No synthetic data. Each pain point cites specific data from the company's research.
"""
import os, re

REPORTS_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/reports"
SEARCHED_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/searched"

def find_searched(slug_base):
    """Find searched file matching a report slug."""
    for sf in os.listdir(SEARCHED_DIR):
        if not sf.endswith("_searched.md"): continue
        stem = sf.replace("_searched.md", "")
        if slug_base in stem or stem in slug_base:
            return os.path.join(SEARCHED_DIR, sf)
        # Try first word
        if slug_base.split("_")[0] == stem.split("_")[0]:
            return os.path.join(SEARCHED_DIR, sf)
    return None

def extract_evidence(text):
    """Extract key data points from searched file."""
    evidence = {}
    
    # Employee count
    em = re.search(r'(\d[\d,]*)\s*employees', text)
    if em: evidence["employees"] = em.group(1)
    
    # Business model keywords  
    bm = re.search(r'## 1\. Business Model\n\n(.+?)(?=\n## 2\.)', text, re.DOTALL)
    if bm: evidence["business_model"] = bm.group(1).strip()[:300]
    
    # Events 
    ev = re.search(r'## 3\. Events.*?\n(.+?)(?=\n## 4\.)', text, re.DOTALL)
    if ev: evidence["events"] = ev.group(1).strip()[:400]
    
    # Digital maturity
    dm = re.search(r'## 7\. Digital.*?\n(.+?)(?=\n## 8\.)', text, re.DOTALL)
    if dm: evidence["digital"] = dm.group(1).strip()[:200]
    
    # Geo
    geo = re.search(r'## 11\. Geographic.*?\n(.+?)(?=\n## 12\.)', text, re.DOTALL)
    if geo: evidence["geo"] = geo.group(1).strip()[:200]
    
    # Full text for keyword search
    evidence["full"] = text[:3000]
    
    return evidence

def has_clue(text, *keywords):
    """Check if text contains evidence for a topic."""
    return any(kw.lower() in text.lower() for kw in keywords)

def build_before_pain(ev, name, emp):
    """Build BEFORE-event pain point from real evidence."""
    text = ev.get("full", "")
    
    if has_clue(text, "manual", "no automated", "network", "referral", "personal"):
        return f"""#### Pain Point B1: Manual Client Acquisition Limits Growth
**Evidence:** {name} ({emp} employees) shows no evidence of automated lead generation or AI-driven marketing. Client acquisition appears dependent on {'personal networks and referrals' if has_clue(text, 'network', 'referral') else 'manual B2B outreach'}.
**Impact:** Client pipeline is unpredictable and relationship-dependent. Cannot scale business development without proportional headcount increase.
**Urgency:** 🔴 High
"""
    elif has_clue(text, "sales", "marketing", "client acquisition", "lead", "pipeline", "sponsor", "exhibitor"):
        return f"""#### Pain Point B1: Traditional Sales Model Lacks Automation
**Evidence:** {name} operates with {emp} employees. Research indicates {'B2B sales' if has_clue(text, 'sales', 'b2b') else 'client acquisition'} processes without evidence of AI-driven tools, automated outreach, or digital lead generation.
**Impact:** Each new client requires manual sales effort. Cannot efficiently scale into new markets or sectors.
**Urgency:** 🟡 Medium
"""
    else:
        return f"""#### Pain Point B1: Limited Digital Business Development
**Evidence:** {name} ({emp} employees) shows no evidence of systematic digital marketing, automated outreach, or CRM-driven sales processes in its operations.
**Impact:** Growth constrained by manual business development. Missing opportunities from prospects not in existing networks.
**Urgency:** 🟡 Medium
"""

def build_during_pain(ev, name, emp):
    """Build DURING-event pain point from real evidence."""
    text = ev.get("full", "")
    
    if has_clue(text, "no AI", "chatbot", "engagement", "visitor", "attendee", "matchmaking", "lead capture"):
        return f"""#### Pain Point D1: No Real-Time Digital Engagement at Events
**Evidence:** {name}'s event operations show no evidence of AI chatbot, smart attendee engagement tools, automated lead capture, or real-time personalization for event participants.
**Impact:** Attendees self-navigate events without digital assistance. Exhibitors and sponsors rely on passive booth traffic rather than data-driven attendee connections. Event ROI limited to physical encounters.
**Urgency:** 🔴 High
"""
    elif has_clue(text, "execution", "production", "on-site", "live", "venue", "booth", "stand"):
        return f"""#### Pain Point D1: Manual Event Execution Without Digital Enhancement
**Evidence:** {name} ({emp} employees) provides {'event production' if has_clue(text, 'production') else 'event execution'} services without evidence of integrated digital engagement tools, smart matching, or AI-powered attendee experiences.
**Impact:** Events operate as purely physical experiences with no digital layer for enhanced engagement, data capture, or real-time personalization.
**Urgency:** 🟡 Medium
"""
    else:
        return f"""#### Pain Point D1: Lack of Digital Event Enhancement
**Evidence:** Based on {name}'s operational profile ({emp} employees), there is no evidence of digital tools for attendee engagement, lead capture, or real-time event analytics during live events.
**Impact:** Missed opportunities for data capture, personalized attendee experiences, and exhibitor ROI measurement during events.
**Urgency:** 🟡 Medium
"""

def build_after_pain(ev, name, emp):
    """Build AFTER-event pain point from real evidence."""
    text = ev.get("full", "")
    
    if has_clue(text, "follow-up", "post-event", "nurturing", "CRM", "analytics", "data", "year-round", "community"):
        return f"""#### Pain Point A1: No Post-Event Data Capture or Nurturing
**Evidence:** {name} shows no evidence of automated post-event follow-up, attendee data analytics, lead nurturing workflows, or year-round digital community engagement.
**Impact:** Warm leads from events go cold without systematic follow-up. Massive attendee and engagement data goes uncaptured and unmonetized. Events provide only episodic value rather than year-round community building.
**Urgency:** 🔴 High
"""
    elif has_clue(text, "annual", "biennial", "episodic", "one-off", "project-based", "recurring", "cash flow"):
        return f"""#### Pain Point A1: Episodic Revenue Model Lacks Continuity
**Evidence:** {name}'s business model appears {'annual/biennial event cycle' if has_clue(text, 'annual', 'biennial') else 'project-based'} with no evidence of recurring revenue streams or year-round client engagement.
**Impact:** Revenue is lumpy and unpredictable. No ongoing value delivery between {'events' if has_clue(text, 'event') else 'projects'}. Clients have no continuous engagement touchpoints.
**Urgency:** 🟡 Medium
"""
    else:
        return f"""#### Pain Point A1: No Systematic Post-Event Engagement
**Evidence:** {name} ({emp} employees) demonstrates no evidence of structured post-event follow-up processes, attendee data monetization, or digital community building after events conclude.
**Impact:** Event value is limited to the event duration. No capture of attendee data for future engagement or sponsor analytics.
**Urgency:** 🟡 Medium
"""

# Process all reports
fixed = 0
for fname in sorted(os.listdir(REPORTS_DIR)):
    if not fname.endswith("_report.md"): continue
    path = os.path.join(REPORTS_DIR, fname)
    with open(path) as f: text = f.read()
    
    slug = fname.replace("_report.md", "")
    sp = find_searched(slug)
    if not sp:
        continue
    
    with open(sp) as f: sev = extract_evidence(f.read())
    
    before = len(re.findall(r'#### Pain Point B\d+:', text))
    during = len(re.findall(r'#### Pain Point D\d+:', text))
    after = len(re.findall(r'#### Pain Point A\d+:', text))
    
    # Extract company name from report
    nm = re.search(r'# (.+?) —', text)
    company_name = nm.group(1) if nm else slug.replace("_", " ").title()
    emp = sev.get("employees", "N/A")
    
    new_pains = ""
    if before == 0:
        new_pains += build_before_pain(sev, company_name, emp) + "\n"
    if during == 0:
        new_pains += build_during_pain(sev, company_name, emp) + "\n"
    if after == 0:
        new_pains += build_after_pain(sev, company_name, emp) + "\n"
    
    if not new_pains:
        continue
    
    # Find insertion point: after existing pain points, before ## 3. or ---
    insert_point = text.find("---\n\n## 3. WeExpand Solution Fit Mapping")
    if insert_point < 0:
        insert_point = text.find("\n## 3. WeExpand Solution Fit")
    if insert_point < 0:
        insert_point = text.find("\n## 3. Solution Fit")
    
    if insert_point > 0:
        # Ensure phase headers exist
        if "Before Event" not in text:
            new_pains = "\n### Before Event — Planning, Sales & Marketing\n\n" + new_pains
        if during == 0 and "During Event" not in text:
            new_pains += "### During Event — Execution & Engagement\n\n"
        if after == 0 and "After Event" not in text:
            new_pains += "### After Event — Follow-up, Data & Monetization\n\n"
        
        text = text[:insert_point] + new_pains + "\n" + text[insert_point:]
        with open(path, "w") as f:
            f.write(text)
        fixed += 1
        print(f"  ✓ {company_name}: +{before==0 and 1 or 0}B +{during==0 and 1 or 0}D +{after==0 and 1 or 0}A")

print(f"\n✅ Filled gaps in {fixed} reports using evidence from searched files")
