#!/usr/bin/env python3
"""Generate final batch of pain point reports."""
import os

base = "/Users/lok/Project/MarketUnderstanding/outputs/reports"

REPORTS = {
    "oliver_kinross_report.md": """# Oliver Kinross — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/oliver_kinross_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Niche Construction Events — Growth Ceiling
**Evidence:** 120 employees. Specialized in construction, real estate, and built environment events. Niche focus limits total addressable market.
**Impact:** Cannot grow beyond construction sector without brand dilution. Must either dominate niche or expand into adjacent sectors.
**Urgency:** Medium — market saturation.

### Pain Point 2: Manual Delegate Sales Across Global Markets
**Evidence:** 120 employees running events globally (construction trade shows in multiple countries). B2B delegate acquisition is manual and market-specific.
**Impact:** Cannot efficiently scale into new geographies without local sales teams. Each new market requires manual build-up.
**Urgency:** High — growth bottleneck.

### Pain Point 3: No Year-Round Digital Community
**Evidence:** Construction industry has continuous project activity — but events are episodic. No evidence of year-round digital community platform.
**Impact:** Community value lost between events. Industry conversations dominated by media and trade publications.
**Urgency:** High — community monetization gap.

### Pain Point 4: Government-Supported Model — Policy Dependency
**Evidence:** Events described as "government-supported" and "government endorsed". Public sector engagement is key to event success.
**Impact:** Event viability dependent on continued government support. Policy changes could impact event permits and attendance.
**Urgency:** Medium — government dependency risk.

[df_company.csv - 120 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Niche growth ceiling | Market Scout for adjacent sector expansion | **Strong** |
| Manual delegate sales | Automated outreach + lead qualification | **Strong** |
| No year-round community | Cross-platform social orchestration | **Strong** |
| Government dependency | Data-driven insights for stakeholder management | **Moderate** |

## 4. Strategic Opportunity Assessment
**Overall Fit:** **High (7/10)** — Niche event leader with clear digital gaps. Strong WeExpand fit for delegate acquisition and year-round community building.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Oliver Kinross | https://oliver-kinross.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "royal_plaza_report.md": """# Royal Plaza Hotel — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/royal_plaza_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Hotel MICE — Manual Event Inquiry Handling
**Evidence:** 210 employees. Hotel receives event inquiries (conferences, weddings, banquets) through traditional channels — phone, email, website forms. No evidence of AI chatbot or automated inquiry qualification.
**Impact:** Event inquiries handled manually by sales team. Slow response times lose bookings. No 24/7 coverage for international inquiries.
**Urgency:** High — revenue leakage from slow response.

### Pain Point 2: Single Property — No Portfolio Diversification
**Evidence:** Single hotel in Mong Kok. All revenue from one physical asset.
**Impact:** Revenue entirely dependent on one property's performance. Cannot diversify across locations. Vulnerable to local market disruptions.
**Urgency:** Medium — concentration risk.

### Pain Point 3: No Digital Guest Engagement or Post-Stay Follow-Up
**Evidence:** 210 employees. No evidence of AI-driven guest engagement, automated post-stay follow-up, or personalized marketing automation.
**Impact:** Guest data captured but not leveraged for repeat bookings, upselling, or loyalty. Massive CRM value left on the table.
**Urgency:** Medium — guest monetization gap.

### Pain Point 4: Competition from Newer, Tech-Enabled Hotels
**Evidence:** Hong Kong hotel market is highly competitive with new properties and international chains offering digital check-in, smart rooms, and AI concierge services.
**Impact:** Risk of being perceived as traditional/outdated. Tech-savvy travelers may choose competitors.
**Urgency:** Medium — competitive positioning.

[df_company.csv - 210 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Manual event inquiry handling | 24/7 AI chatbot + automated lead qualification | **Strong** |
| Single property concentration | Year-round digital engagement platform | **Moderate** |
| No digital guest engagement | Automated follow-up + CRM integration | **Strong** |
| Competition from tech hotels | AI-driven guest experience differentiation | **Strong** |

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (6/10)** — Hotel venue with clear digital gaps in event inquiry handling and guest engagement. WeExpand can automate inquiry-to-booking pipeline.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Royal Plaza Hotel | https://royalplazahotel.net | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "serious_staging_report.md": """# Serious Staging — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/serious_staging_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Boutique Production House — Scale Limit
**Evidence:** 22 employees. Specialized in experiential design, fashion shows, heritage site events, concert production — all bespoke, high-touch services.
**Impact:** Revenue ceiling tied to billable project hours. Cannot scale to multiple simultaneous large productions.
**Urgency:** High — growth constrained.

### Pain Point 2: Manual Client Acquisition for Premium Services
**Evidence:** Luxury event services, heritage site production, unprecedented concerts — niche, premium positioning requiring relationship-based sales.
**Impact:** Client pipeline dependent on personal networks and reputation. Cannot systematically target new luxury clients.
**Urgency:** Medium — business development bottleneck.

### Pain Point 3: Heavy Production Risk — Single Point of Failure
**Evidence:** Live concert production, bespoke venue creation, rigging — high-risk, high-stakes operations with small team.
**Impact:** One key person's unavailability could cancel a major production. No redundancy in critical roles.
**Urgency:** Medium — operational vulnerability.

### Pain Point 4: Heritage/Niche Focus — Limited Addressable Market
**Evidence:** Heritage site events, luxury heritage, unprecedented concerts — extremely niche positioning.
**Impact:** Total addressable market is very small. Growth limited to premium heritage/luxury segment.
**Urgency:** Low — niche strategy choice.

[df_company.csv - 22 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Boutique scale limit | Automated outreach + lead qualification | **Strong** |
| Manual client acquisition | Market Scout for luxury client targeting | **Strong** |
| Production risk | AI engagement reduces manual touchpoints | **Moderate** |
| Niche market focus | Hyper-localized content for expansion | **Moderate** |

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Premium boutique with limited AI alignment. WeExpand value is primarily in client acquisition automation for their niche market.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | Serious Staging | http://www.serious-staging.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "showtex_report.md": """# ShowTex — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/showtex_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Manufacturing Business — Low Digital Leverage
**Evidence:** 130 employees. Global provider of event textiles, stage drapery, flame-retardant fabrics, projection screens. Manufacturing and rental of physical products.
**Impact:** Revenue from physical product sales and rental. Limited software/digital revenue potential. Business model inherently capital-intensive.
**Urgency:** Medium — business model limitation.

### Pain Point 2: Global Operations with Manual Sales
**Evidence:** 130 employees serving global entertainment, events, theatre, and museum industries. B2B sales of specialized textile products — likely manual, relationship-driven.
**Impact:** Cannot efficiently target all potential clients globally. Each new market requires local sales presence.
**Urgency:** High — global sales bottleneck.

### Pain Point 3: Projection/AV Innovation Not Monetized as Platform
**Evidence:** Offers cutting-edge products (hologram screens, 360 projection fabrics, video mapping surfaces, LED video animation systems) — but sold as physical products, not integrated solutions.
**Impact:** Innovation value captured through one-time product sales rather than recurring service/subscription revenue. Missed platform opportunity.
**Urgency:** Medium — monetization gap.

### Pain Point 4: E-Commerce Underdeveloped
**Evidence:** Company mentions e-commerce but primary model appears to be direct B2B sales and rental. No evidence of sophisticated digital sales platform.
**Impact:** Clients cannot easily browse, configure, and order products online. Manual quoting process slows sales cycle.
**Urgency:** Medium — digital sales gap.

[df_company.csv - 130 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Manufacturing business model | Automated lead gen + CRM | **Strong** |
| Global manual sales | Market Scout + automated outreach | **Strong** |
| Innovation not monetized | Data-driven strategic optimization | **Moderate** |
| E-commerce underdeveloped | AI engagement for online sales | **Moderate** |

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Product/manufacturing company serving events industry. WeExpand value primarily in automating global B2B sales. Limited software monetization potential.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | ShowTex | https://showtex.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",

    "syma_report.md": """# SYMA — Pain Point Analysis & Solution Fit Report
**Generated:** 2026-05-29

## 1. Structured Research Summary
See: `outputs/searched/syma_searched.md`

## 2. Pain Point Analysis

### Pain Point 1: Exhibition Hardware Business — Low Digital Leverage
**Evidence:** 93 employees. German exhibition stand system manufacturer. Modular aluminum profile systems, custom stands — physical product manufacturing and construction.
**Impact:** Revenue from physical product sales and stand construction. Limited digital/software revenue potential. Hardware business with inherent scalability limits.
**Urgency:** Medium — business model constraint.

### Pain Point 2: Manual Client Acquisition in Global Markets
**Evidence:** 93 employees serving trade fairs globally. Exhibition stand construction is a local, relationship-driven business.
**Impact:** Cannot efficiently scale into new geographies without local presence. Each market requires physical operations.
**Urgency:** High — global expansion bottleneck.

### Pain Point 3: Sustainability Credentials Not Digitally Amplified
**Evidence:** Recycling, green stands, environmental certification mentioned in company profile. Sustainability is a differentiator in stand construction.
**Impact:** Sustainability credentials not reaching potential clients at scale. Competitive advantage underexploited.
**Urgency:** Medium — marketing gap.

### Pain Point 4: Competition from Local and Digital-First Providers
**Evidence:** Exhibition stand market is fragmented with many local providers. Digital-first competitors offer virtual exhibition solutions.
**Impact:** Risk of market share loss to virtual/hybrid event platforms that reduce demand for physical stands.
**Urgency:** Medium — disruption risk.

[df_company.csv - 93 employees - 2026-05-29]

## 3. Solution Fit Mapping
| Pain Point | WeExpand Capability | Fit Strength |
|---|---|---|
| Hardware business model | Automated lead gen + CRM | **Strong** |
| Manual global sales | Market Scout + automated outreach | **Strong** |
| Sustainability not amplified | Cross-platform social orchestration | **Strong** |
| Competition from digital providers | AI-driven differentiation | **Moderate** |

## 4. Strategic Opportunity Assessment
**Overall Fit:** **Medium (5/10)** — Exhibition hardware manufacturer. WeExpand value in automating global B2B sales and amplifying sustainability credentials. Limited software monetization potential.

## 5. Citation Index
| # | Source | URL | Access Date |
|---|--------|-----|-------------|
| 1 | SYMA | https://syma.com | 2026-05-29 |
| 2 | df_company.csv | Internal dataset | 2026-05-29 |
| 3 | about_my_company.md | Internal document | 2026-05-29 |
""",
}

for fname, content in REPORTS.items():
    path = os.path.join(base, fname)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✓ {fname}")

print(f"\nGenerated {len(REPORTS)} reports")
