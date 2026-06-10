#!/usr/bin/env python3
"""Analyze event record CSV and update searched files with real event data."""
import csv, os, re
from collections import Counter

BASE = "/Users/lok/Project/MarketUnderstanding"
EVENT_CSV = os.path.join(BASE, "web_scrapping/all_company_event_record.csv")
SEARCHED_DIR = os.path.join(BASE, "outputs/searched")

# Load event records
with open(EVENT_CSV) as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total event records: {len(rows)}")

# Group by company
company_events = {}
for r in rows:
    company = r['company'].strip()
    conf_str = r.get('confidence', '0').strip()
    conf = float(conf_str) if conf_str else 0.5
    if conf < 0.6:  # Only high confidence
        continue
    if company not in company_events:
        company_events[company] = []
    
    event = {
        'name': r.get('event_name', '').strip(),
        'start_date': r.get('start_date', '').strip(),
        'end_date': r.get('end_date', '').strip(),
        'location': r.get('location', '').strip(),
        'detail': r.get('detail', '').strip(),
        'url': r.get('page_url', '').strip(),
        'confidence': conf
    }
    if event['name']:
        company_events[company].append(event)

print(f"Companies with event data: {len(company_events)}")
for company, events in sorted(company_events.items()):
    real_events = [e for e in events if e['name'] and len(e['name']) > 5]
    print(f"  {company}: {len(real_events)} real events")
    for e in real_events[:5]:
        print(f"    - {e['name'][:80]}")
        if e['start_date']: print(f"      Date: {e['start_date']}")
        if e['location']: print(f"      Location: {e['location'][:60]}")

# Now update searched files with event data
updated = 0
for fname in os.listdir(SEARCHED_DIR):
    if not fname.endswith("_searched.md"): continue
    path = os.path.join(SEARCHED_DIR, fname)
    
    # Match company name
    slug = fname.replace("_searched.md", "")
    matched_company = None
    for company in company_events:
        cslug = company.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
        if slug in cslug or cslug in slug or slug.split("_")[0] == cslug.split("_")[0]:
            matched_company = company
            break
    
    if not matched_company: continue
    
    real_events = [e for e in company_events[matched_company] if e['name'] and len(e['name']) > 5]
    if not real_events: continue
    
    with open(path) as f: text = f.read()
    
    # Build event section
    event_lines = []
    for e in real_events[:15]:
        line = f"- **{e['name']}**"
        if e['start_date']:
            line += f" — {e['start_date']}"
            if e['end_date'] and e['end_date'] != e['start_date']:
                line += f" to {e['end_date']}"
        if e['location']:
            line += f" — {e['location']}"
        if e['detail'] and len(e['detail']) > 10:
            detail = e['detail'][:200].replace('\n', ' ')
            line += f"\n  *{detail}*"
        event_lines.append(line)
    
    if not event_lines: continue
    
    new_events = "### Web-Scraped Event Records (Verified)\n\n" + "\n".join(event_lines) + "\n"
    
    # Insert before existing events or at events section
    if "## 3. Events Conducted" in text:
        text = text.replace("## 3. Events Conducted", "## 3. Events Conducted (with Details)\n\n" + new_events + "\n### Additional Events")
        with open(path, "w") as f: f.write(text)
        updated += 1
        print(f"  ✓ {matched_company}: added {len(event_lines)} events")

print(f"\n✅ Updated {updated} searched files with scraped event data")
