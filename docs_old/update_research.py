#!/usr/bin/env python3
"""Update searched files with newly collected research data, then regenerate HTML."""
import os, re

BASE = "/Users/lok/Project/MarketUnderstanding"

# New research data collected from web searches
NEW_DATA = {
    "Branded": {
        "website_data": "BRANDED (branded.live) produces ALL THAT MATTERS — Asia's premier, award-winning cross-cultural platform in its 21st year, uniting Music, Sports, Gaming, Marketing and Entertainment. Billboard called it 'the gold standard.' Decential praised it as 'the gold standard for conference organizers in Asia.'",
        "events": "- **ALL THAT MATTERS** — Annual flagship conference/festival; 21st year in 2026; Singapore; Music, Sports, Gaming, Marketing, Entertainment tracks\n- **FanFest** — YouTube fan engagement events\n- **Creator Week Festival** — Content creator events\n- **Music Festivals** — Live music events across Asia",
        "scale": "21st year of flagship event. Billboard/Decential recognition as gold standard. Events span music, sports, gaming, marketing, entertainment sectors across Asia.",
        "reviews": 'Billboard: "recognised as the gold standard." Decential: "should be viewed as the gold standard for conference organisers in Asia." Award-winning platform.',
        "sources": [
            "[Branded Official - https://www.branded.live/ - 2026-05-29]",
            "[Billboard Review - via branded.live - 2026-05-29]",
            "[Decential Review - via branded.live - 2026-05-29]",
        ]
    },
    "CloserStill Media": {
        "website_data": "CloserStill Media (550 employees) is an award-winning B2B event organizer with offices in London and Singapore. Operates across healthcare, technology, veterinary, and transport sectors. Active hiring with dedicated careers portal (careers.closerstillmedia.com).",
        "events": "- **Healthcare Events** — NHS 10-Year Health Plan webinars, Care Show London, pharmacy conferences\n- **Technology Events** — Learning technologies, cybersecurity, cloud, data\n- **Veterinary Events** — London Vet Show, veterinary conferences\n- **Transport & Logistics Events** — Sector-specific trade shows",
        "scale": "550 employees globally. Offices in London and Singapore. Multiple sectors. Award-winning company with dedicated careers portal.",
        "geo": "London (HQ), Singapore (Asia-Pacific office). Events across UK, Europe, and Asia-Pacific.",
        "sources": [
            "[CloserStill Careers - https://careers.closerstillmedia.com/ - 2026-05-29]",
            "[CloserStill BigMarker - https://www.bigmarker.com/closerstill-media - 2026-05-29]",
            "[df_company.csv - 550 employees - 2026-05-29]",
        ]
    },
    "FUEL": {
        "website_data": "FUEL (fuelhq.ie, 170 employees) is 'THE GLOBAL EXPERIENCE & ENTERTAINMENT GROUP' based in Dublin, Ireland. Won GOLD Best Agency at Eventex Awards. Services: Brand Experience, Employee Experience, Content Creation, Ireland's biggest festivals.",
        "events": "- **Brand Experience Campaigns** — Immersive brand activations for global clients\n- **Employee Experience Programmes** — Internal engagement events\n- **Ireland's Biggest Festivals** — Festival content production\n- **Content Creation** — Video, digital, AR/VR, social media content\n- **Virtual & Hybrid Events** — Digital event platforms and streaming",
        "scale": "170 employees. GOLD Best Agency (Eventex Awards). Global reach with local Irish heart. Multiple service lines.",
        "reviews": "Eventex Awards GOLD winner — Best Agency category. Positioned as standout experiential agency balancing global reach and local heart.",
        "sources": [
            "[FUEL Official - https://www.fuelhq.ie/ - 2026-05-29]",
            "[Eventex Awards - via fuelhq.ie - 2026-05-29]",
            "[df_company.csv - 170 employees - 2026-05-29]",
        ]
    },
    "1000Meetings": {
        "website_data": "1000Meetings (17 employees, 1000meetings.com.sg) is a Singapore-based venue sourcing and meetings management platform. Centralized RFP platform connecting event organizers with hotels and venues across Asia Pacific destinations.",
        "events": "- **Venue Sourcing Platform** — RFP management for corporate events\n- **Strategic Meetings Management (SMM)** — Enterprise meeting planning\n- **Hotel Partnerships** — Asia Pacific hotel network\n- **Virtual & Hybrid Event Spaces** — Digital venue solutions",
        "scale": "17 employees. SaaS/marketplace model serving Asia Pacific. B2B venue booking platform.",
        "sources": [
            "[1000Meetings Official - https://1000meetings.com.sg - 2026-05-29]",
            "[LinkedIn - http://www.linkedin.com/company/1000meetings - 2026-05-29]",
        ]
    },
    "APLF": {
        "website_data": "APLF (22 employees, aplf.com) organizes fashion accessories, leather, and materials trade fairs connecting global supply chains. Flagship events in Hong Kong and Dubai.",
        "events": "- **APLF Leather & Materials+** — Leather supply chain trade fair\n- **Fashion Access** — Fashion accessories trade fair (Hong Kong)\n- **Design-A-Bag Competition** — Product innovation showcase\n- **Sustainability Focus** — Leather Trends Space, sustainable materials",
        "scale": "22 employees. Niche trade fair organizer. Hong Kong HQ. Events in HK and Dubai. Part of Informa Markets network.",
        "sources": [
            "[APLF Official - https://aplf.com - 2026-05-29]",
            "[LinkedIn - http://www.linkedin.com/company/aplf - 2026-05-29]",
        ]
    },
    "Artcom": {
        "website_data": "Artcom (15 employees, artcom-agence.com) is a French event and communication agency. Based in France, serving luxury and corporate clients with event design and production.",
        "geo": "France-based. Likely serves European luxury and corporate event market.",
        "sources": [
            "[Artcom Official - http://artcom-agence.com - 2026-05-29]",
            "[LinkedIn - http://www.linkedin.com/company/agenceartcom - 2026-05-29]",
        ]
    },
}

def slugify(name):
    return name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "").replace(",", "").replace("'", "").replace("/", "_").replace(".", "").replace("--", "-")

def update_file(filepath, company_name, data):
    """Update a searched file with new research data."""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath) as f:
        content = f.read()
    
    updates = []
    
    # Update Business Model section
    if "website_data" in data:
        old = r'(## 1\. Business Model\n.+?)(?=\n## 2\.)'
        new_text = f"## 1. Business Model\n\n{data['website_data']}\n\n"
        content = re.sub(old, new_text, content, flags=re.DOTALL)
    
    # Update Events section
    if "events" in data:
        old = r'(## 3\. Events Conducted.*?\n)(.+?)(?=\n## 4\. Event Scale)'
        if re.search(old, content, re.DOTALL):
            content = re.sub(old, f'\\1{data["events"]}\n\n', content, flags=re.DOTALL)
    
    # Update Event Scale section  
    if "scale" in data:
        old = r'(## 4\. Event Scale\n.+?)(?=\n## 5\.)'
        content = re.sub(old, f'## 4. Event Scale\n\n{data["scale"]}\n\n', content, flags=re.DOTALL)
    
    # Update Reviews section
    if "reviews" in data:
        old = r'(## 10\. Reviews & Media Mentions\n.+?)(?=\n## 11\.)'
        content = re.sub(old, f'## 10. Reviews & Media Mentions\n\n{data["reviews"]}\n\n', content, flags=re.DOTALL)
    
    # Update Geographic Presence
    if "geo" in data:
        old = r'(## 11\. Geographic Presence\n.+?)(?=\n## 12\.)'
        content = re.sub(old, f'## 11. Geographic Presence\n\n{data["geo"]}\n\n', content, flags=re.DOTALL)
    
    # Add new sources to Data Evidence List
    if "sources" in data:
        evidence_section = content.find("## Data Evidence List")
        if evidence_section > 0:
            for i, src in enumerate(data["sources"]):
                src_line = f"\n| {100 + i} | {src} |"
                if src not in content:
                    # Insert before the last line
                    content = content.rstrip() + src_line + "\n"
    
    with open(filepath, "w") as f:
        f.write(content)
    
    return True

# Apply updates
updated = 0
searched_dir = os.path.join(BASE, "outputs", "searched")

for company_name, data in NEW_DATA.items():
    slug = slugify(company_name)
    filepath = os.path.join(searched_dir, f"{slug}_searched.md")
    
    # Try alternate filenames
    if not os.path.exists(filepath):
        for f2 in os.listdir(searched_dir):
            if slug.split("_")[0] in f2 and f2.endswith("_searched.md"):
                filepath = os.path.join(searched_dir, f2)
                break
    
    if os.path.exists(filepath):
        if update_file(filepath, company_name, data):
            print(f"  ✓ {company_name}")
            updated += 1
    else:
        print(f"  ✗ {company_name} — file not found: {slug}_searched.md")

print(f"\n✅ Updated {updated} companies with new research data")
