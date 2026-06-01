#!/usr/bin/env python3
"""Generate summary.html dashboard with visualizations and market insights."""
import json

with open("/Users/lok/Project/MarketUnderstanding/outputs/website/summary_data.json") as f:
    data = json.load(f)

# Build the pain category chart data
cats = data["pain_categories"]
cat_labels = json.dumps(list(cats.keys()))
cat_values = json.dumps(list(cats.values()))

urgency = data["urgency_distribution"]
urg_labels = json.dumps(list(urgency.keys()))
urg_values = json.dumps(list(urgency.values()))

emp_groups = data["employee_groups"]
emp_labels = json.dumps(list(emp_groups.keys()))
emp_values = json.dumps(list(emp_groups.values()))

# Tier tables
def tier_rows(tier_data):
    rows = ""
    for i, c in enumerate(tier_data):
        rows += f"""
        <tr>
            <td>{i+1}</td>
            <td><a href="{c['slug']}.html"><strong>{c['name']}</strong></a></td>
            <td>{c['type']}</td>
            <td>{c['employees']}</td>
            <td>{c['pain_count']} pain points</td>
            <td><span class="badge badge-high">{c['fit_score']}/10</span></td>
        </tr>"""
    return rows

# Top pain points by company
top_pains_rows = ""
for i, c in enumerate(data["top_pains"]):
    top_pains_rows += f"""
        <tr>
            <td>{i+1}</td>
            <td><a href="{c['slug']}.html">{c['company']}</a></td>
            <td>{c['count']}</td>
            <td><span class="badge badge-{'high' if c['fit']=='High' else 'medium'}">{c['fit']}</span></td>
        </tr>"""

# All companies summary
all_rows = ""
for c in data["companies"]:
    badge = f'badge-{"high" if c["fit_level"]=="High" else "medium" if c["fit_level"]=="Medium" else "low"}'
    all_rows += f"""
        <tr>
            <td><a href="{c['slug']}.html">{c['name']}</a></td>
            <td>{c['employees']}</td>
            <td>{c['type']}</td>
            <td>{c['pain_count']}</td>
            <td><span class="badge {badge}">{c['fit_score']}/10</span></td>
        </tr>"""

# WeExpand market insights
market_insights = f"""
<div class="insight-card">
    <h3>Primary Target: Large Exhibition Organizers</h3>
    <p>Companies like <strong>Informa Markets (3,500 emp), RX Global (3,300), GL events (5,000), Clarion Events (1,100), The Adsale Group (170)</strong> represent the highest-value prospects. They have:</p>
    <ul>
        <li>Massive attendee bases (100K-300K+ per event) → enormous data & community value</li>
        <li>Annual/biennial event cycles → critical year-round engagement gap</li>
        <li>Large sales teams doing manual B2B outreach → immediate automation ROI</li>
        <li>Enterprise budgets and existing digital transformation initiatives</li>
    </ul>
    <p><strong>WeExpand Value:</strong> Year-round digital community platform, AI-driven exhibitor-visitor matching, automated lead capture, post-event analytics. Enterprise deal size: $100K-$500K+ ARR.</p>
</div>

<div class="insight-card">
    <h3>Secondary Target: Niche Conference Organizers</h3>
    <p><strong>Beacon Events (130), Leader Associates (94), JEC (200), Marintec China (50), ReThink HK (16), BEYOND Expo (17), TOKEN2049 (36), SuperAI (20)</strong> are fast-growing niche players with:</p>
    <ul>
        <li>Highly engaged specialist communities → premium community monetization</li>
        <li>Lean teams (13-200 employees) → extreme need for automation</li>
        <li>Tech-savvy audiences (crypto, AI, sustainability) → low education barrier</li>
        <li>Rapidly growing sectors → scaling pressure</li>
    </ul>
    <p><strong>WeExpand Value:</strong> AI delegate acquisition, automated sponsor matching, year-round community orchestration, cross-platform engagement. Deal size: $30K-$100K ARR.</p>
</div>

<div class="insight-card">
    <h3>Tertiary Target: HK Venue Operators</h3>
    <p><strong>Kai Tak Sports Park (160), HKCEC (140), AsiaWorld-Expo (110)</strong> are prime candidates for smart venue transformation:</p>
    <ul>
        <li>Kai Tak is brand new (opened 2025) → greenfield opportunity with no legacy systems</li>
        <li>All three venues generate massive visitor data (millions annually) that goes completely uncaptured</li>
        <li>Zero digital engagement layer for visitors → chatbot, smart wayfinding, personalized recommendations</li>
        <li>Competing against each other → AI-driven differentiation is a competitive moat</li>
    </ul>
    <p><strong>WeExpand Value:</strong> Smart venue AI platform, real-time visitor engagement, automated lead capture for exhibitors, post-event data monetization. Deal size: $50K-$150K ARR.</p>
</div>

<div class="insight-card">
    <h3>Platform/Marketplace Opportunity</h3>
    <p><strong>1000Meetings (17), KEYS (18)</strong> are venue/platform marketplaces where AI matching between event organizers and venues is the core value proposition:</p>
    <ul>
        <li>Both have tiny teams (17-18 employees) → automation multiplies output</li>
        <li>Core business is matching supply-demand → AI matching is natural fit</li>
        <li>Venue RFP and booking process is entirely manual → 24/7 AI engagement is transformative</li>
    </ul>
    <p><strong>WeExpand Value:</strong> AI-driven venue-client matching, automated RFP response, 24/7 chatbot engagement, smart meeting scheduling. Deal size: $20K-$60K ARR.</p>
</div>

<div class="insight-card insight-card--warning">
    <h3>Lower Priority: Physical Fabrication & Creative Agencies</h3>
    <p>Companies like <strong>EventWorks, Milton Exhibits, expomobilia, SYMA, ShowTex, Chunky Onion, Teamrite, Noah Asia</strong> have inherent AI limitations due to physical/hardware business models:</p>
    <ul>
        <li>Revenue tied to physical products, labor, or bespoke creative work → limited software monetization</li>
        <li>WeExpand value is primarily in <strong>client acquisition automation</strong> and <strong>brand building</strong></li>
        <li>Approach as lightweight CRM/outreach tool rather than full platform transformation</li>
        <li>Deal size: $5K-$20K ARR — high volume, lower ticket</li>
    </ul>
</div>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Understanding — Executive Summary | WeExpand</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="css/style.css">
    <style>
        :root {{
            --we-purple: #667eea;
            --we-dark: #1a1a2e;
            --we-red: #e94560;
            --we-green: #27ae60;
            --we-orange: #f39c12;
            --we-blue: #3498db;
        }}
        
        .summary-hero {{
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 40%, #16213e 100%);
            color: white;
            padding: 60px 0 50px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .summary-hero::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at 30% 50%, rgba(102,126,234,0.15) 0%, transparent 50%),
                        radial-gradient(circle at 70% 30%, rgba(233,69,96,0.1) 0%, transparent 40%);
        }}
        .summary-hero h1 {{ font-size: 2.8rem; font-weight: 800; position: relative; z-index: 1; }}
        .summary-hero h1 span {{ color: var(--we-red); }}
        .summary-hero .subtitle {{ font-size: 1.2rem; opacity: 0.85; max-width: 750px; margin: 12px auto 0; position: relative; z-index: 1; }}
        
        .kpi-bar {{
            display: flex; justify-content: center; gap: 32px; margin-top: 36px;
            flex-wrap: wrap; position: relative; z-index: 1;
        }}
        .kpi {{
            background: rgba(255,255,255,0.08); backdrop-filter: blur(10px);
            border-radius: 16px; padding: 24px 32px; text-align: center;
            min-width: 140px; border: 1px solid rgba(255,255,255,0.1);
        }}
        .kpi .num {{ font-size: 2.5rem; font-weight: 800; }}
        .kpi .label {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.7; margin-top: 4px; }}
        .kpi.highlight {{ background: rgba(233,69,96,0.2); border-color: rgba(233,69,96,0.3); }}
        .kpi.highlight .num {{ color: var(--we-red); }}
        
        main {{ padding: 40px 0 60px; }}
        .section-title {{
            font-size: 1.6rem; font-weight: 700; color: var(--we-dark); margin: 48px 0 24px;
            padding-bottom: 10px; border-bottom: 3px solid var(--we-red); display: inline-block;
        }}
        .section-title:first-child {{ margin-top: 0; }}
        
        .chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin: 24px 0; }}
        @media (max-width: 768px) {{ .chart-grid {{ grid-template-columns: 1fr; }} }}
        .chart-card {{
            background: white; border-radius: 16px; padding: 28px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.06); border: 1px solid #e9ecef;
        }}
        .chart-card h3 {{ font-size: 1.1rem; color: var(--we-dark); margin-bottom: 16px; }}
        .chart-card canvas {{ max-height: 300px; }}
        
        .insight-card {{
            background: white; border-radius: 16px; padding: 28px;
            margin: 16px 0;
            box-shadow: 0 2px 16px rgba(0,0,0,0.06);
            border-left: 5px solid var(--we-purple);
        }}
        .insight-card h3 {{ color: var(--we-dark); margin-bottom: 12px; font-size: 1.15rem; }}
        .insight-card p {{ margin: 8px 0; line-height: 1.7; color: #444; }}
        .insight-card ul {{ margin: 8px 0; padding-left: 20px; }}
        .insight-card li {{ margin: 6px 0; line-height: 1.6; color: #444; }}
        .insight-card strong {{ color: var(--we-dark); }}
        .insight-card--warning {{ border-left-color: var(--we-orange); background: #fffdf5; }}
        
        .summary-table {{
            width: 100%; border-collapse: collapse; margin: 16px 0;
            background: white; border-radius: 12px; overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        .summary-table th {{
            background: var(--we-dark); color: white; padding: 12px 16px;
            font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; text-align: left;
        }}
        .summary-table td {{ padding: 10px 16px; border-bottom: 1px solid #e9ecef; font-size: 0.9rem; }}
        .summary-table tr:hover {{ background: #f8f9ff; }}
        .summary-table a {{ color: var(--we-purple); text-decoration: none; font-weight: 600; }}
        .summary-table a:hover {{ text-decoration: underline; }}
        
        .badge {{
            display: inline-block; padding: 4px 12px; border-radius: 20px;
            font-size: 0.78rem; font-weight: 700;
        }}
        .badge-high {{ background: #d4edda; color: #155724; }}
        .badge-medium {{ background: #fff3cd; color: #856404; }}
        .badge-low {{ background: #f8d7da; color: #721c24; }}
        
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
        
        .nav-strip {{
            background: white; border-bottom: 2px solid #e9ecef;
            position: sticky; top: 0; z-index: 100;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .nav-strip .container {{ display: flex; gap: 24px; overflow-x: auto; padding: 12px 20px; }}
        .nav-strip a {{ color: #888; text-decoration: none; font-weight: 600; font-size: 0.9rem; white-space: nowrap; padding: 8px 0; border-bottom: 2px solid transparent; }}
        .nav-strip a:hover, .nav-strip a.active {{ color: var(--we-red); border-bottom-color: var(--we-red); }}
        
        footer {{ text-align: center; padding: 24px; background: var(--we-dark); color: rgba(255,255,255,0.5); font-size: 0.85rem; }}
        footer a {{ color: var(--we-red); text-decoration: none; }}
    </style>
</head>
<body>

<div class="summary-hero">
    <div class="container">
        <h1>Hong Kong EMF <span>Market Intelligence</span></h1>
        <p class="subtitle">Executive Summary: 46 Event Management Firms — Pain Point Analysis, Solution Fit & WeExpand Market Opportunity</p>
        <div class="kpi-bar">
            <div class="kpi"><div class="num">{data['total_companies']}</div><div class="label">Companies Analyzed</div></div>
            <div class="kpi"><div class="num">{data['total_pain_points']}</div><div class="label">Pain Points Identified</div></div>
            <div class="kpi"><div class="num">{data['total_employees']:,}</div><div class="label">Total Employees</div></div>
            <div class="kpi highlight"><div class="num">{data['fit_distribution']['High']}</div><div class="label">High-Fit Prospects</div></div>
            <div class="kpi"><div class="num">{data['avg_pains_per_company']}</div><div class="label">Avg Pains / Company</div></div>
        </div>
    </div>
</div>

<div class="nav-strip">
    <div class="container">
        <a href="#overview" class="active">Overview</a>
        <a href="#charts">Visualizations</a>
        <a href="#market">Market Opportunity</a>
        <a href="#tiers">Target Tiers</a>
        <a href="#all">All Companies</a>
        <a href="index.html">Company Index →</a>
    </div>
</div>

<main>
<div class="container">

<!-- OVERVIEW -->
<section id="overview">
    <h2 class="section-title">Executive Summary</h2>
    <div class="two-col">
        <div class="chart-card">
            <h3>Key Findings</h3>
            <ul>
                <li><strong>168 pain points</strong> identified across 46 companies — avg {data['avg_pains_per_company']} per company</li>
                <li><strong>#1 pain theme:</strong> Manual Sales & Client Acquisition — nearly every company lacks automated lead gen</li>
                <li><strong>#2 pain theme:</strong> Year-Round Engagement Gap — annual/biennial events lose community value</li>
                <li><strong>#3 pain theme:</strong> No Digital Platform — most companies are "dumb" physical operations</li>
                <li><strong>Top opportunity:</strong> Large exhibition organizers (Informa, RX, GL events, Clarion) represent highest WeExpand ARR potential</li>
                <li><strong>Greenfield:</strong> Kai Tak Sports Park (opened 2025) — zero legacy systems, HK$30B investment</li>
            </ul>
        </div>
        <div class="chart-card">
            <h3>WeExpand Go-to-Market Strategy</h3>
            <ol>
                <li><strong>Tier 1 (Prime):</strong> {len(data['tier1_prime'])} companies — immediate outreach. Large organizers + tech-forward events.</li>
                <li><strong>Tier 2 (Strong):</strong> {len(data['tier2_strong'])} companies — nurture pipeline. Growing niche players.</li>
                <li><strong>Tier 3 (Niche):</strong> {len(data['tier3_niche'])} companies — lightweight CRM play. Physical/hardware businesses.</li>
            </ol>
            <p style="margin-top:12px; color:#888;"><strong>Total Addressable Market:</strong> 46 companies. <strong>Priority targets:</strong> {len(data['tier1_prime']) + len(data['tier2_strong'])} companies with strong WeExpand fit.</p>
        </div>
    </div>
</section>

<!-- CHARTS -->
<section id="charts">
    <h2 class="section-title">Data Visualizations</h2>
    
    <div class="chart-grid">
        <div class="chart-card">
            <h3>Pain Points by Category</h3>
            <canvas id="painCatChart"></canvas>
        </div>
        <div class="chart-card">
            <h3>Urgency Distribution</h3>
            <canvas id="urgencyChart"></canvas>
        </div>
    </div>
    
    <div class="chart-grid">
        <div class="chart-card">
            <h3>Companies by Employee Size</h3>
            <canvas id="empSizeChart"></canvas>
        </div>
        <div class="chart-card">
            <h3>Solution Fit Distribution</h3>
            <canvas id="fitDistChart"></canvas>
        </div>
    </div>
</section>

<!-- MARKET OPPORTUNITY -->
<section id="market">
    <h2 class="section-title">WeExpand Market Opportunity Analysis</h2>
    {market_insights}
</section>

<!-- TARGET TIERS -->
<section id="tiers">
    <h2 class="section-title">Target Prioritization</h2>
    
    <div class="chart-card" style="margin-bottom:24px;">
        <h3>🎯 Tier 1 — Prime Targets (Fit Score 8-10)</h3>
        <p style="color:#888;margin-bottom:12px;">Highest WeExpand product-market fit. Immediate outreach priority.</p>
        <table class="summary-table">
            <thead><tr><th>#</th><th>Company</th><th>Type</th><th>Employees</th><th>Pain Points</th><th>Fit</th></tr></thead>
            <tbody>{tier_rows(data['tier1_prime'])}</tbody>
        </table>
    </div>

    <div class="chart-card" style="margin-bottom:24px;">
        <h3>🥈 Tier 2 — Strong Prospects (Fit Score 6-7)</h3>
        <p style="color:#888;margin-bottom:12px;">Good WeExpand fit. Nurture pipeline, case-study-driven sales.</p>
        <table class="summary-table">
            <thead><tr><th>#</th><th>Company</th><th>Type</th><th>Employees</th><th>Pain Points</th><th>Fit</th></tr></thead>
            <tbody>{tier_rows(data['tier2_strong'])}</tbody>
        </table>
    </div>

    <div class="chart-card">
        <h3>🥉 Tier 3 — Niche Plays (Fit Score 0-5)</h3>
        <p style="color:#888;margin-bottom:12px;">Limited AI alignment. Lightweight CRM/lead-gen tool approach.</p>
        <table class="summary-table">
            <thead><tr><th>#</th><th>Company</th><th>Type</th><th>Employees</th><th>Pain Points</th><th>Fit</th></tr></thead>
            <tbody>{tier_rows(data['tier3_niche'][:20])}</tbody>
        </table>
        {f'<p style="margin-top:8px;color:#888;font-size:0.85rem;">+ {len(data["tier3_niche"]) - 20} more companies in Tier 3</p>' if len(data['tier3_niche']) > 20 else ''}
    </div>
</section>

<!-- ALL COMPANIES -->
<section id="all">
    <h2 class="section-title">All 46 Companies — At a Glance</h2>
    <table class="summary-table">
        <thead><tr><th>Company</th><th>Employees</th><th>Type</th><th>Pain Points</th><th>Fit Score</th></tr></thead>
        <tbody>{all_rows}</tbody>
    </table>
</section>

</div>
</main>

<footer>
    <div class="container">
        <p>Market Understanding Project · <a href="index.html">Company Index</a> · Generated 2026-05-29 · WeExpand Agentic AI Solution</p>
    </div>
</footer>

<script>
// Pain Categories Chart
new Chart(document.getElementById('painCatChart'), {{
    type: 'bar',
    data: {{
        labels: {cat_labels},
        datasets: [{{
            label: 'Pain Points',
            data: {cat_values},
            backgroundColor: ['#e94560','#667eea','#f39c12','#27ae60','#3498db','#9b59b6','#e67e22','#1abc9c','#e74c3c','#2ecc71','#34495e','#95a5a6'],
            borderRadius: 6,
            borderSkipped: false,
        }}]
    }},
    options: {{
        indexAxis: 'y',
        responsive: true,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ beginAtZero: true, ticks: {{ stepSize: 5 }} }} }}
    }}
}});

// Urgency Chart
new Chart(document.getElementById('urgencyChart'), {{
    type: 'doughnut',
    data: {{
        labels: {urg_labels},
        datasets: [{{
            data: {urg_values},
            backgroundColor: ['#e94560','#f39c12','#27ae60'],
            borderWidth: 2,
            borderColor: '#fff'
        }}]
    }},
    options: {{
        responsive: true,
        plugins: {{ legend: {{ position: 'bottom' }} }}
    }}
}});

// Employee Size Chart
new Chart(document.getElementById('empSizeChart'), {{
    type: 'bar',
    data: {{
        labels: {emp_labels},
        datasets: [{{
            label: 'Companies',
            data: {emp_values},
            backgroundColor: ['#27ae60','#3498db','#f39c12','#e94560'],
            borderRadius: 8,
        }}]
    }},
    options: {{
        responsive: true,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 5 }} }} }}
    }}
}});

// Fit Distribution Chart
new Chart(document.getElementById('fitDistChart'), {{
    type: 'doughnut',
    data: {{
        labels: ['High Fit','Medium Fit','Low'],
        datasets: [{{
            data: [{data['fit_distribution']['High']},{data['fit_distribution']['Medium']},{data['fit_distribution'].get('Low',0)}],
            backgroundColor: ['#27ae60','#f39c12','#95a5a6'],
            borderWidth: 2,
            borderColor: '#fff'
        }}]
    }},
    options: {{
        responsive: true,
        plugins: {{ legend: {{ position: 'bottom' }} }}
    }}
}});
</script>
</body>
</html>"""

with open("/Users/lok/Project/MarketUnderstanding/outputs/website/summary.html", "w") as f:
    f.write(html)

print("✅ summary.html generated")
