#!/usr/bin/env python3
"""Fix remaining 7 reports with proper pain point format."""
import os
base = "/Users/lok/Project/MarketUnderstanding/outputs/reports"

REPORTS = {
    "eventworks_report.md": """# EventWorks — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/eventworks_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Large Operational Workforce — Labor-Intensive Model
**Evidence:** 290 employees managing tent/equipment rental, furnishing, staging — all physical, labor-intensive operations.
**Impact:** Revenue directly tied to labor hours and physical equipment. Cannot scale without proportional headcount increase. High operational costs.
**Urgency:** High — operational efficiency gap.

### Pain Point 2: Manual Sales & Client Acquisition at Scale
**Evidence:** 290 employees suggests large sales team doing manual outreach for equipment rental and event services. No evidence of automated lead generation or digital client acquisition.
**Impact:** Client acquisition costs high at scale. Each new client requires manual sales effort. Cannot efficiently expand into new geographies.
**Urgency:** High — growth bottleneck.

### Pain Point 3: Commoditized Service — Low Digital Differentiation
**Evidence:** Equipment rental (tents, furniture, staging, lighting) is inherently commoditized. Many local and national competitors offer similar services.
**Impact:** Competing primarily on price and availability. Limited digital differentiation. Vulnerable to price competition from lower-cost providers.
**Urgency:** Medium — competitive positioning risk.

### Pain Point 4: No Digital Client Portal or Self-Service
**Evidence:** No evidence of online inventory browsing, self-service booking, digital contract management, or client portal for 290-person operation.
**Impact:** All client interactions require manual staff involvement. Slow response times. Competitors with digital platforms offer superior experience.
**Urgency:** Medium — client experience gap.

### Pain Point 5: Siloed Rental and Production Services
**Evidence:** Separate service lines (tenting, furnishings, staging, catering equipment) likely operated in silos without cross-selling automation.
**Impact:** Missed cross-selling opportunities. Clients using one service unaware of others. No integrated client view across service lines.
**Urgency:** Medium — revenue synergy gap.

[df_company.csv - 290 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Labor-intensive operations | AI engagement automates client touchpoints | **Moderate** |
| Manual sales at scale | Market Scout + automated outreach | **Strong** |
| Commoditized service | Social orchestration + brand building | **Moderate** |
| No digital client portal | 24/7 AI chatbot + automated booking | **Strong** |
| Siloed services | CRM integration + cross-sell automation | **Strong** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (6/10)** — Large event rental company. WeExpand can automate client acquisition and service cross-selling, but the labor-intensive physical business model limits AI impact on core operations.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | EventWorks | https://eventworksrentals.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "exr_report.md": """# EX-R International — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/exr_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Small Exhibition Contractor — Scale Limit
**Evidence:** 19 employees providing exhibition design and fabrication services in Hong Kong.
**Impact:** Cannot handle large volumes of exhibition stands. Each project requires manual design and construction. Growth directly tied to headcount.
**Urgency:** High — scalability constraint.

### Pain Point 2: Manual Client Acquisition in Competitive Market
**Evidence:** HK exhibition services market has many providers. 19 employees suggests relationship-based sales with limited digital marketing.
**Impact:** Client pipeline dependent on personal networks. Cannot systematically target new exhibitors at HK trade fairs.
**Urgency:** High — growth bottleneck.

### Pain Point 3: No Digital Portfolio or Self-Service Platform
**Evidence:** No evidence of online portfolio gallery, instant quoting, design preview tools, or client project tracking.
**Impact:** All client interactions require manual communication. Slow sales cycle. Competitors with digital platforms offer superior experience.
**Urgency:** Medium — digital gap.

### Pain Point 4: Physical Fabrication — No Digital Revenue Stream
**Evidence:** Revenue entirely from physical stand design and construction. No digital or recurring revenue.
**Impact:** Revenue is project-based and unpredictable. No SaaS or retainer model to smooth cash flow.
**Urgency:** Medium — business model limitation.

[df_company.csv - 19 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Small team scale limit | Automated lead gen + CRM | **Strong** |
| Manual client acquisition | Market Scout + automated outreach | **Strong** |
| No digital portfolio | Social orchestration + brand building | **Strong** |
| Physical fabrication only | Lead qualification for higher-value services | **Moderate** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Small exhibition design firm. WeExpand value primarily in automating client acquisition. Limited software monetization potential given physical business model.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | EX-R International | https://exr-intl.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "expomobilia_report.md": """# expomobilia GmbH — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/expomobilia_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Exhibition Fabrication — Physical Business Limits
**Evidence:** 110 employees. Swiss exhibition stand design, construction, museum displays, pop-up stores — all physical fabrication.
**Impact:** Revenue tied to physical labor and materials. Cannot scale through software. Each project requires physical presence.
**Urgency:** Medium — business model constraint.

### Pain Point 2: Global Operations with Manual Sales
**Evidence:** Global presence serving luxury brands, trade fairs, and art exhibitions. 110 employees suggests manual B2B sales across geographies.
**Impact:** Cannot efficiently target all potential exhibition clients globally. Each market requires local sales effort.
**Urgency:** High — global sales bottleneck.

### Pain Point 3: Luxury/Sustainability Positioning Not Digitally Amplified
**Evidence:** ISO 20121 certified, eco-friendly materials, luxury brand staging, Swiss craftsmanship — strong differentiators.
**Impact:** Premium credentials not reaching potential clients at scale. Competitive advantage underexploited through manual marketing only.
**Urgency:** Medium — marketing gap.

### Pain Point 4: Project-Based Revenue — No Recurring Model
**Evidence:** Revenue from one-off stand construction and design projects.
**Impact:** Unpredictable revenue streams. No retainer or recurring revenue from clients between exhibition cycles.
**Urgency:** Medium — revenue predictability gap.

[df_company.csv - 110 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Physical business limits | Automated lead gen + CRM | **Strong** |
| Manual global sales | Market Scout + automated outreach | **Strong** |
| Premium positioning not amplified | Cross-platform social orchestration | **Strong** |
| Project-based revenue | Lead nurturing + recurring engagement | **Moderate** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Premium exhibition fabricator. WeExpand value in automating global client acquisition and amplifying sustainability/luxury credentials. Limited software monetization.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | expomobilia | https://expomobilia.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "fuel_report.md": """# FUEL — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/fuel_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Creative Agency at Scale — Coordination Complexity
**Evidence:** 170 employees. Experiential marketing, content creation, brand experience, employee engagement — diverse creative services across multiple offices (Dublin, UK, US).
**Impact:** Large creative teams require significant coordination overhead. Cross-office project management is complex and manual.
**Urgency:** Medium — operational complexity.

### Pain Point 2: Manual Client Acquisition and Pitching
**Evidence:** 170 employees in creative services. Agency model relies on pitching and relationship-based business development. No evidence of automated lead generation.
**Impact:** Client acquisition is labor-intensive and unpredictable. Each pitch requires significant creative investment with no guarantee of winning.
**Urgency:** High — business development bottleneck.

### Pain Point 3: Content Creation at Scale — No AI Augmentation
**Evidence:** Content creation is core service (video, digital, social media, AR/VR). 170 employees suggests large content production team.
**Impact:** Content production is entirely human-driven. Cannot leverage AI for content personalization, localization, or scaling. Competitors using AI tools have cost advantage.
**Urgency:** High — competitive threat from AI-augmented agencies.

### Pain Point 4: Project-Based Revenue with Limited Retainers
**Evidence:** Agency model typically project-based. Campaigns have defined start/end dates.
**Impact:** Revenue lumpy and unpredictable. Limited recurring revenue from ongoing client relationships.
**Urgency:** Medium — revenue predictability gap.

[df_company.csv - 170 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Coordination complexity | CRM integration + workflow automation | **Moderate** |
| Manual client acquisition | Market Scout + automated outreach | **Strong** |
| No AI content augmentation | Hyper-localized content creation | **Strong** |
| Project-based revenue | Automated follow-up + client nurturing | **Strong** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (6/10)** — Large creative agency. WeExpand can automate client acquisition and content localization, but core creative production has inherent AI limitations. Lead gen and social orchestration are primary value points.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | FUEL | https://fuelhq.ie | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "hkcec_report.md": """# HKCEC — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/hkcec_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Passive Venue Operator — No Value-Added Digital Services
**Evidence:** 140 employees. 91,500 sqm venue. Provides space rental and basic services. No evidence of exhibitor-visitor matching, lead capture platforms, or attendee analytics.
**Impact:** Commoditized offering — competes on price and location. Event organizers get space but no data, no lead generation, no attendee insights.
**Urgency:** High — competitive differentiation gap.

### Pain Point 2: Single-Location Revenue Dependency
**Evidence:** Single venue at Wanchai waterfront. All revenue from one physical asset.
**Impact:** Revenue tied entirely to HK market health. No digital revenue streams. Vulnerable to regional disruptions.
**Urgency:** Medium — business model concentration risk.

### Pain Point 3: Competition from Newer Venues
**Evidence:** Kai Tak Sports Park (opened 2025, HK$30B) and AsiaWorld-Expo compete for same event organizers. HK venue market becoming oversupplied.
**Impact:** Without differentiation, faces price pressure and potential market share loss.
**Urgency:** Medium — competitive threat.

### Pain Point 4: Manual Event Sales & Client Acquisition
**Evidence:** 140 employees likely includes significant sales team manually reaching out to event organizers globally.
**Impact:** Client acquisition costs high. No automated lead generation or AI-driven venue matching.
**Urgency:** Medium — operational efficiency gap.

### Pain Point 5: Zero Post-Event Data Monetization
**Evidence:** No evidence of attendee data analytics, exhibitor lead management, or post-event engagement platforms despite hosting hundreds of events annually.
**Impact:** Massive data generated by events goes uncaptured. Missed recurring revenue from data services.
**Urgency:** Medium — significant missed revenue.

[df_company.csv - 140 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Passive venue model | Smart venue AI platform + lead capture | **Strong** |
| Single-location dependency | Year-round digital engagement platform | **Strong** |
| Competition from new venues | AI-driven differentiation + brand building | **Strong** |
| Manual event sales | Market Scout + automated outreach | **Strong** |
| No post-event data monetization | Automated follow-up + analytics | **Strong** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (8/10)** — Premier venue ripe for smart venue transformation. WeExpand can add digital engagement layer to complement iconic physical space, creating new revenue streams beyond venue rental.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | HKCEC | http://hkcec.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "infocommasia_report.md": """# InfoCommAsia — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/infocommasia_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Tiny Team Running Major Industry Event
**Evidence:** 13 employees organizing InfoComm Asia — the premier AV and systems integration exhibition in Asia Pacific. Part of AVIXA (global AV trade association).
**Impact:** 13 people cannot effectively manage delegate acquisition, exhibitor sales, event logistics, and marketing simultaneously. Extreme scalability constraint.
**Urgency:** High — operational capacity stretched.

### Pain Point 2: Manual Delegate and Exhibitor Sales
**Evidence:** 13 employees. Niche B2B event requiring specialized AV industry knowledge for delegate and exhibitor acquisition.
**Impact:** Cannot scale attendee or exhibitor acquisition without hiring. Each new exhibitor requires manual sales cycles.
**Urgency:** High — growth bottleneck.

### Pain Point 3: Annual Event — Year-Round Engagement Gap
**Evidence:** InfoComm Asia is annual. AV technology industry innovates continuously — but community only engages during event days.
**Impact:** Community value lost between events. AV professionals engage elsewhere 360 days per year.
**Urgency:** High — community monetization gap.

### Pain Point 4: Asia-Pacific Focus — Geographic Limitation
**Evidence:** Focused on Asia Pacific market. Global AV industry spans Americas and EMEA.
**Impact:** Missing global AV community. Parent AVIXA provides global reach but event remains APAC-centric.
**Urgency:** Medium — geographic expansion opportunity.

[df_company.csv - 13 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Tiny team at scale | Automated outreach + lead qualification | **Strong** |
| Manual delegate sales | Market Scout + automated outreach | **Strong** |
| Annual event year-round gap | Cross-platform community orchestration | **Strong** |
| APAC geographic focus | Hyper-localized content for expansion | **Strong** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (7/10)** — Small team running major industry event. WeExpand can multiply their output through AI automation of delegate acquisition, exhibitor matching, and year-round community building.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | InfoCommAsia | https://www.infocommasia.com/ | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "rx_global_report.md": """# RX Global — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/rx_global_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Enterprise Scale — Slow Digital Transformation
**Evidence:** 3,300 employees. 400+ events in 22 countries. Part of RELX Group (FTSE 100). Large enterprise with legacy systems and complex organizational structure.
**Impact:** Digital transformation is slow and bureaucratic. Innovation competes with maintaining existing event portfolio. Change management is challenging at enterprise scale.
**Urgency:** Medium — organizational inertia.

### Pain Point 2: Traditional Exhibition Model Under Digital Disruption
**Evidence:** Core business is physical B2B trade shows. B2B sourcing increasingly moving online. No evidence of fully integrated year-round digital platform across all 400+ events.
**Impact:** Physical exhibition model faces long-term disruption from digital platforms. Must transform before digital competitors erode market position.
**Urgency:** High — strategic imperative.

### Pain Point 3: Fragmented Data Across 400+ Events
**Evidence:** 400+ events across 22 countries and 43 sectors. Each event likely operates with its own systems, data, and processes.
**Impact:** Massive attendee and exhibitor data fragmented across events. Cannot leverage cross-event insights, cross-sell, or build unified customer view.
**Urgency:** High — data monetization gap.

### Pain Point 4: Manual Exhibitor and Delegate Sales at Scale
**Evidence:** 3,300 employees across 22 countries. Each event vertical requires specialized sales teams. No evidence of AI-driven, centralized lead generation.
**Impact:** Sales costs proportional to event portfolio size. Cannot efficiently cross-sell exhibitors across events.
**Urgency:** Medium — operational efficiency gap.

### Pain Point 5: Competition from Digital-Native Event Platforms
**Evidence:** Digital-native competitors (Hopin, Swapcard, Zoom Events) and tech giants entering event space. RX's physical-first model faces disruption.
**Impact:** Must build digital moat to defend market position. Physical events alone are no longer sufficient competitive advantage.
**Urgency:** Medium — competitive threat.

[df_company.csv - 3,300 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Slow digital transformation | AI platform as transformation accelerator | **Strong** |
| Traditional model disruption | Year-round digital engagement platform | **Strong** |
| Fragmented data across events | CRM integration + unified analytics | **Strong** |
| Manual sales at scale | Market Scout + automated outreach | **Strong** |
| Digital-native competition | AI-driven community moat | **Strong** |

[about_my_company.md - 2026-05-29]

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (9/10)** — Top-3 enterprise target alongside Informa and GL events. 3,300 employees with 400+ events. Parent RELX is a data/analytics company = board already values data + AI. Perfect WeExpand alignment for enterprise-scale deployment.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | RX Global | https://rxglobal.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",
}

for fname, content in REPORTS.items():
    path = os.path.join(base, fname)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✓ {fname}")

print(f"\nFixed {len(REPORTS)} reports")
