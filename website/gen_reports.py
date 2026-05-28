#!/usr/bin/env python3
"""Generate pain point reports for remaining companies."""
import os

base = "/Users/lok/Project/MarketUnderstanding/outputs/reports"

# Define all remaining reports
REPORTS = {
    "jec_report.md": """# JEC — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/jec_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Niche Industry Leader — Growth Ceiling
**Evidence:** 200 employees. JEC World is the leading composites event globally. Niche market means total addressable audience is inherently limited.
**Impact:** Cannot grow indefinitely within composites niche. Must expand into adjacent sectors or build digital revenue streams.
**Urgency:** Medium — market saturation risk.

### Pain Point 2: Annual Event Model — Year-Round Gap
**Evidence:** JEC World is annual. Composites industry innovation happens year-round — but community only engages during event days.
**Impact:** Massive community value lost between events. No recurring digital revenue. Industry conversations happen elsewhere 360 days per year.
**Urgency:** High — community monetization gap.

### Pain Point 3: Manual Delegate & Exhibitor Sales
**Evidence:** 200 employees globally. Niche B2B sales require deep industry knowledge — likely manual, relationship-driven process.
**Impact:** Cannot scale into new geographies or adjacent sectors without hiring industry experts. Each new event requires manual sales build-up.
**Urgency:** Medium — growth bottleneck.

### Pain Point 4: No AI-Driven Materials Innovation Matching
**Evidence:** Composites industry is innovation-heavy. Events bring together innovators and manufacturers — but no AI matchmaking to accelerate connections.
**Impact:** High-value R&D connections left to chance. Exhibitors and attendees miss potential partnerships.
**Urgency:** Medium — value-add gap.

[df_company.csv - 200 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Niche growth ceiling | Market Scout for adjacent sector expansion | **Strong** |
| Annual event year-round gap | Cross-platform community orchestration | **Strong** |
| Manual delegate sales | Automated outreach + lead qualification | **Strong** |
| No AI matching | Smart meeting scheduling + AI recommendations | **Strong** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (8/10)**

JEC is a niche leader with a passionate global community and clear digital gaps. WeExpand can transform JEC World from an annual trade show into a 365-day composites innovation platform.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | JEC | https://jeccomposites.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "keys_report.md": """# KEYS — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/keys_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Tiny Team Running Venue Platform — Scale Crisis
**Evidence:** 18 employees running a luxury venue booking platform connecting event organizers with high-end Paris/Cannes venues. Venue sourcing is inherently manual at the luxury end.
**Impact:** 18 people cannot manually handle RFP responses, venue matching, and client management at scale. Each booking inquiry requires significant human effort.
**Urgency:** High — scalability crisis.

### Pain Point 2: Manual Venue-Client Matching Process
**Evidence:** Luxury venue booking (chateaux, private mansions, art galleries) requires detailed understanding of client needs and venue capabilities. No evidence of AI-driven matching.
**Impact:** Matching quality dependent on individual staff knowledge. Cannot efficiently scale to serve more clients or expand to new cities.
**Urgency:** High — core process bottleneck.

### Pain Point 3: Geographic Concentration in France
**Evidence:** Focused on Paris and Cannes. Luxury venue market exists globally (Hong Kong, London, New York, Dubai) but not served.
**Impact:** Total addressable market artificially limited to two French cities. Missing global luxury event market.
**Urgency:** Medium — geographic expansion blocked.

### Pain Point 4: No Automated RFP Response or 24/7 Client Engagement
**Evidence:** Luxury clients expect immediate, personalized service. 18 employees cannot provide 24/7 coverage.
**Impact:** Response delays lose high-value bookings. Overnight inquiries go unanswered. Competitors with automated systems win on speed.
**Urgency:** Medium — service quality gap.

[df_company.csv - 18 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Tiny team scalability | Automated outreach + 24/7 engagement | **Strong** |
| Manual venue-client matching | AI-driven lead qualification + smart matching | **Strong** |
| Geographic concentration | Market Scout + hyper-localized content | **Strong** |
| No automated RFP response | Automated follow-up + CRM integration | **Strong** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (8/10)**

KEYS is essentially a marketplace — the highest-WeExpand-fit business model. AI-driven venue matching, automated RFP response, and 24/7 client engagement would multiply their 18-person team's output.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | KEYS | https://keysvenue.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "leader_associates_report.md": """# Leader Associates — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/leader_associates_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Rapidly Growing Sector — Competition Intensifying
**Evidence:** 94 employees in renewable energy events. Hydrogen, offshore wind, CCUS, energy storage — all fast-growing sectors attracting major event organizers (Informa, RX Global).
**Impact:** As renewable energy becomes mainstream, larger organizers will enter and compete. Niche advantage erodes. Must build defensible position now.
**Urgency:** High — competitive window closing.

### Pain Point 2: Manual Delegate & Sponsor Sales for Specialist Events
**Evidence:** 94 employees across multiple energy sub-sectors. Each event vertical requires specialized knowledge for delegate acquisition.
**Impact:** Cannot scale into new energy sub-sectors without hiring domain experts. Sales efficiency limited by specialist knowledge requirements.
**Urgency:** Medium — growth bottleneck.

### Pain Point 3: No Year-Round Energy Community Platform
**Evidence:** Events are episodic. Renewable energy transition is a 24/7/365 global imperative — but community only engages during conferences.
**Impact:** Massive thought leadership value lost between events. Industry conversations happen on LinkedIn, Twitter, and competitor platforms.
**Urgency:** High — community ownership risk.

### Pain Point 4: Policy-Dependent Revenue Model
**Evidence:** Events focused on renewable energy policy, climate policy frameworks, energy transition financing. Government policy shifts directly impact event relevance and sponsor interest.
**Impact:** Revenue vulnerable to political changes. Anti-renewable administrations would reduce industry event spending.
**Urgency:** Medium — policy risk.

[df_company.csv - 94 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Competition intensifying | AI-driven community moat + year-round platform | **Strong** |
| Manual specialist sales | Market Scout + automated outreach | **Strong** |
| No year-round community | Cross-platform social orchestration | **Strong** |
| Policy-dependent revenue | Data-driven insights for diversification | **Moderate** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (8/10)**

Leader Associates operates in the hottest event sector (renewable energy) with clear digital gaps. The opportunity: become the year-round digital platform for the global energy transition community.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Leader Associates | https://leader-associates.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "marintec_china_report.md": """# Marintec China — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/marintec_china_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Biennial Event — 2-Year Engagement Gap
**Evidence:** Marintec China is a biennial maritime exhibition. The longest engagement gap in the dataset — 2 years between events.
**Impact:** Catastrophic community engagement gap. Maritime industry stakeholders have zero event touchpoints for 23 months. Community disperses to competitors.
**Urgency:** High — community retention critical.

### Pain Point 2: 50 Employees Managing Asia's Largest Maritime Event
**Evidence:** 50 employees for a major biennial trade fair. Joint venture between Informa Markets and Shanghai Society of Naval Architects.
**Impact:** Team likely overwhelmed during event year, underutilized in off years. Operational inefficiency from biennial cycle.
**Urgency:** Medium — operational rhythm challenge.

### Pain Point 3: No Digital Maritime Community or Content Platform
**Evidence:** Maritime industry has year-round news flow (shipping rates, regulations, technology, sustainability). But Marintec China only serves the industry once every 2 years.
**Impact:** Industry conversations happen elsewhere. Digital maritime media capture community attention between events.
**Urgency:** High — community platform gap.

### Pain Point 4: China-Centric Geographic Concentration
**Evidence:** Event is China-focused. Global maritime industry spans Singapore, Rotterdam, London, Dubai, Tokyo.
**Impact:** Missing global maritime community beyond China. Informa partnership provides global reach but event remains Shanghai-centric.
**Urgency:** Medium — geographic expansion opportunity.

[df_company.csv - 50 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| 2-year engagement gap | Year-round digital community platform | **Strong** |
| 50-person team, biennial cycle | Automated outreach + CRM optimization | **Strong** |
| No digital maritime community | Cross-platform content orchestration | **Strong** |
| China-centric concentration | Hyper-localized content for global expansion | **Strong** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (7/10)**

Marintec China has the most extreme engagement gap (2 years) in the dataset — making WeExpand's value proposition incredibly clear. A year-round digital maritime community would transform their business model.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Marintec China | https://marintecchina.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",
}

# Batch 2: Remaining 0-pain-point companies
REPORTS2 = {
    "messe_frankfurt_report.md": """# Messe Frankfurt (Shanghai) Co Ltd — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/messe_frankfurt_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Subsidiary with Limited Autonomy
**Evidence:** 91 employees. Shanghai subsidiary of Messe Frankfurt GmbH — one of the world's largest trade fair organizers. Local office executes parent company strategy with limited independent decision-making.
**Impact:** Cannot independently adopt new technologies or pivot strategy. Innovation must go through German HQ approval. Slow decision-making.
**Urgency:** Medium — organizational constraint.

### Pain Point 2: Manual Exhibition Sales in Competitive China Market
**Evidence:** 91 employees running exhibitions across automotive, textile, consumer goods in China. Market has numerous competitors (Informa, RX Global, local Chinese organizers).
**Impact:** Client acquisition is competitive and relationship-driven. No evidence of AI-driven lead generation or automated exhibitor acquisition.
**Urgency:** High — competitive market pressure.

### Pain Point 3: Fragmented Global Tech Stack
**Evidence:** Part of global Messe Frankfurt group with operations in 190+ countries. Likely operating with fragmented systems across regions.
**Impact:** Inefficient client management, inconsistent data, limited cross-selling between regions.
**Urgency:** Medium — operational inefficiency.

### Pain Point 4: Traditional Exhibition Model — Digital Disruption Risk
**Evidence:** Core business is physical trade fairs. Chinese B2B market rapidly digitizing (Alibaba, Pinduoduo, Douyin e-commerce).
**Impact:** Physical exhibition model faces same digital disruption as all traditional organizers. Must build digital complement to physical events.
**Urgency:** Medium — strategic imperative.

[df_company.csv - 91 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Limited subsidiary autonomy | Pilot that proves ROI to parent | **Moderate** |
| Manual exhibition sales | Market Scout + automated outreach | **Strong** |
| Fragmented tech stack | Seamless CRM + calendar integration | **Moderate** |
| Traditional model disruption | Year-round digital engagement platform | **Strong** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (7/10)** — Subsidiary of global giant. WeExpand play: use Shanghai office as pilot to prove ROI to Messe Frankfurt group globally.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Messe Frankfurt | https://www.cn.messefrankfurt.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "milton_exhibits_report.md": """# Milton Exhibits — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/milton_exhibits_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Physical Fabrication Business — Low Digital Leverage
**Evidence:** 110 employees providing exhibition stand design, construction, interior fitting — inherently physical, labor-intensive services.
**Impact:** Revenue directly tied to physical labor and materials. Each project requires physical presence. Cannot scale through software alone.
**Urgency:** Medium — business model limitation.

### Pain Point 2: Manual Client Acquisition in Competitive Market
**Evidence:** Exhibition stand market is fragmented and competitive. Many local and regional players. 110 employees suggests significant manual sales effort.
**Impact:** Client acquisition costs high. No evidence of automated lead generation or digital marketing at scale.
**Urgency:** High — growth bottleneck.

### Pain Point 3: Project-Based Revenue — No Recurring Income
**Evidence:** Revenue comes from one-off exhibition stand projects. Each client engagement is a discrete project with no recurring revenue.
**Impact:** Revenue unpredictable and lumpy. Cannot build SaaS-like recurring revenue streams from physical fabrication business.
**Urgency:** Medium — revenue predictability gap.

### Pain Point 4: Regional Focus Limits Growth
**Evidence:** Serves regional and international trade fairs but likely concentrated in specific geographies.
**Impact:** Geographic expansion requires physical presence (warehouses, fabrication facilities, local teams). High capital requirement for new market entry.
**Urgency:** Medium — expansion cost barrier.

[df_company.csv - 110 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Physical fabrication business | Automated lead gen + CRM | **Strong** |
| Manual client acquisition | Market Scout + automated outreach | **Strong** |
| Project-based revenue | Lead qualification + upselling | **Moderate** |
| Regional focus | Hyper-localized content for expansion | **Moderate** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Physical fabrication business with inherent digital limitations. WeExpand value primarily in client acquisition and brand building.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Milton Exhibits | https://milton-exhibits.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "mykar_events_report.md": """# Mykar Events — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/mykar_events_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Micro Team — Extreme Scalability Constraint
**Evidence:** 12 employees organizing infrastructure, energy, hospitality, and transportation summits in the Philippines. Multi-sector events with tiny team.
**Impact:** Cannot handle multiple events simultaneously. Single point of failure for all operations. Growth impossible without hiring.
**Urgency:** High — existential scalability limit.

### Pain Point 2: Fully Manual Government and Industry Stakeholder Management
**Evidence:** Events involve government-industry collaboration (Philippine Infrastructure Summit, Energy Summit, Hospitality Summit). Stakeholder management is complex and manual.
**Impact:** Each government and industry relationship requires manual nurturing. Cannot scale stakeholder engagement across sectors.
**Urgency:** Medium — operational complexity.

### Pain Point 3: Philippines Market Concentration
**Evidence:** All events are Philippines-focused. Small domestic market limits growth potential.
**Impact:** Revenue ceiling determined by Philippines event market size. Cannot grow beyond domestic demand without geographic expansion.
**Urgency:** Medium — market size limitation.

### Pain Point 4: No Digital Event or Community Platform
**Evidence:** Virtual summit platforms mentioned but no evidence of integrated digital community, year-round engagement, or automated delegate acquisition.
**Impact:** Events are episodic. No recurring digital revenue or community value between summits.
**Urgency:** Medium — digital gap.

[df_company.csv - 12 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Micro team scalability | Automated outreach + lead qualification | **Strong** |
| Manual stakeholder management | CRM integration + automated follow-up | **Strong** |
| Philippines concentration | Market Scout for regional expansion | **Strong** |
| No digital community | Cross-platform engagement + social orchestration | **Strong** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Very small company with potential but likely budget constraints. WeExpand can help them punch above their weight through automation.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Mykar Events | https://mykar-events.net | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "noah_asia_report.md": """# Noah (Asia) Limited — Pain Point Analysis & Solution Fit Report

**Generated:** 2026-05-29

---

## 1. Structured Research Summary
See: `outputs/searched/noah_asia_searched.md`

---

## 2. Pain Point Analysis

### Pain Point 1: Micro Agency — Extreme Scale Limit
**Evidence:** 11 employees providing decoration design, production, print/digital creative, public engagement, event project management, PR — massive service breadth for a tiny team.
**Impact:** Cannot scale any service line without hiring. Each new client requires significant manual effort. Growth directly tied to headcount.
**Urgency:** High — scalability crisis.

### Pain Point 2: Fully Manual Marketing Services
**Evidence:** Traditional marketing agency model — all services are human-delivered (design, production, PR, event management). No evidence of automation, AI tools, or digital platforms.
**Impact:** Revenue is labor-hours. Cannot productize services. Vulnerable to automation-disrupted agency model.
**Urgency:** Medium — industry disruption risk.

### Pain Point 3: Client Concentration Risk
**Evidence:** 11 employees likely serving a small number of clients. Loss of one major client could be catastrophic.
**Impact:** Revenue concentration risk. Client pipeline unpredictable. No systematic business development.
**Urgency:** High — revenue concentration risk.

### Pain Point 4: Competition from Digital-First Agencies
**Evidence:** Competitors increasingly offer AI-powered marketing, programmatic advertising, digital analytics. Traditional agency model being disrupted.
**Impact:** Risk of losing clients to agencies with more modern, data-driven capabilities. Cannot compete on digital sophistication.
**Urgency:** Medium — competitive threat.

[df_company.csv - 11 employees - 2026-05-29]

---

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Micro agency scale limit | Automated outreach + CRM | **Strong** |
| Manual marketing services | Cross-platform social orchestration | **Strong** |
| Client concentration risk | Market Scout for pipeline diversification | **Strong** |
| Competition from digital agencies | AI-driven differentiation | **Strong** |

[about_my_company.md - 2026-05-29]

---

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Small traditional agency that could benefit from automation but may have limited budget and digital maturity to adopt AI.

---

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Noah Asia | https://noahasia.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",
}

REPORTS.update(REPORTS2)

for fname, content in REPORTS.items():
    path = os.path.join(base, fname)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✓ {fname}")

print(f"\nGenerated {len(REPORTS)} reports total")
