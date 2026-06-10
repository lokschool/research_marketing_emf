#!/usr/bin/env python3
"""Generate a completely rewritten summary.html with rich visualization and explanations."""
import json, re

with open("/Users/lok/Project/MarketUnderstanding/outputs/website/summary_data.json") as f:
    d = json.load(f)

# Load teammate data
tm = {}
try:
    with open("/Users/lok/Project/MarketUnderstanding/outputs/website/merged_data.json") as f:
        md = json.load(f)
    for c in md.get("companies",[]):
        tm[c.get("name","").lower()] = c
except: pass

total = d["total_companies"]
pains = d["total_pain_points"]
emps = d["total_employees"]
avg = d["avg_pains_per_company"]
high = d["fit_distribution"]["High"]
med = d["fit_distribution"]["Medium"]
low = d["fit_distribution"].get("Low", 0)

# Pain categories for chart
cats = d.get("pain_categories", {})
cat_labels = json.dumps(list(cats.keys()))
cat_values = json.dumps(list(cats.values()))

# Urgency
urg = d.get("urgency_distribution", {})
urg_labels = json.dumps(list(urg.keys()))
urg_values = json.dumps(list(urg.values()))

# Employee groups
emp_grp = d.get("employee_groups", {})
emp_labels = json.dumps(list(emp_grp.keys()))
emp_values = json.dumps(list(emp_grp.values()))

# Top 10 companies
top = sorted(d["companies"], key=lambda x: -x["fit_score"])[:15]

# Build HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hong Kong EMF — Executive Summary | WeExpand Market Intelligence</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {{ --ink: #0f172a; --muted: #64748b; --line: #e2e8f0; --bg: #f8fafc; --card: #fff;
       --red: #e94560; --blue: #3b82f6; --green: #10b981; --amber: #f59e0b; --purple: #8b5cf6;
       --teal: #14b8a6; --navy: #1e293b; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--ink); line-height: 1.6; }}
.container {{ max-width: 1200px; margin:0 auto; padding:0 24px; }}

.hero {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #312e81 100%); color: white; padding: 64px 0 48px; text-align: center; position: relative; overflow: hidden; }}
.hero::before {{ content:''; position:absolute; top:0; left:0; right:0; bottom:0; background: radial-gradient(circle at 20% 50%, rgba(59,130,246,0.12) 0%, transparent 50%), radial-gradient(circle at 70% 30%, rgba(139,92,246,0.08) 0%, transparent 40%); }}
.hero h1 {{ font-size: 2.6rem; font-weight: 800; position: relative; z-index: 1; }}
.hero h1 span {{ color: var(--red); }}
.hero .sub {{ font-size: 1.1rem; opacity: 0.85; max-width: 650px; margin: 12px auto 0; position: relative; z-index: 1; }}

.kpi-row {{ display: flex; justify-content: center; gap: 20px; margin-top: 36px; flex-wrap: wrap; position: relative; z-index: 1; }}
.kpi {{ background: rgba(255,255,255,0.07); backdrop-filter: blur(8px); border-radius: 14px; padding: 20px 28px; text-align: center; min-width: 130px; border: 1px solid rgba(255,255,255,0.08); }}
.kpi .num {{ font-size: 2.2rem; font-weight: 800; }}
.kpi .lbl {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.2px; opacity: 0.65; margin-top: 4px; }}
.kpi.hl {{ background: rgba(233,69,96,0.15); border-color: rgba(233,69,96,0.25); }}
.kpi.hl .num {{ color: var(--red); }}

.nav {{ background: white; border-bottom: 2px solid var(--line); position: sticky; top:0; z-index: 100; }}
.nav .container {{ display: flex; gap: 24px; overflow-x: auto; padding: 12px 24px; }}
.nav a {{ color: var(--muted); text-decoration: none; font-weight: 600; font-size: 0.88rem; white-space: nowrap; padding: 6px 0; border-bottom: 2px solid transparent; }}
.nav a:hover, .nav a.active {{ color: var(--red); border-bottom-color: var(--red); }}

main {{ padding: 40px 0 60px; }}
section {{ margin-bottom: 48px; }}
.section-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 3px solid var(--red); display: inline-block; }}

.chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
@media(max-width:768px){{ .chart-grid{{grid-template-columns:1fr}} }}
.chart-card {{ background: var(--card); border-radius: 14px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid var(--line); }}
.chart-card h3 {{ font-size: 1rem; margin-bottom: 16px; color: var(--navy); }}
.chart-card canvas {{ max-height: 280px; }}

.card {{ background: var(--card); border-radius: 14px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid var(--line); margin-bottom: 16px; }}
.card h3 {{ font-size: 1.1rem; margin-bottom: 12px; }}
.card p, .card li {{ font-size: 0.92rem; color: var(--muted); line-height: 1.7; }}
.card ul {{ padding-left: 20px; }}
.card li {{ margin: 4px 0; }}

.insight-box {{ border-left: 5px solid var(--blue); padding: 16px 20px; margin: 12px 0; background: #f0f7ff; border-radius: 0 10px 10px 0; }}
.insight-box.red {{ border-left-color: var(--red); background: #fef2f2; }}
.insight-box.green {{ border-left-color: var(--green); background: #ecfdf5; }}
.insight-box.amber {{ border-left-color: var(--amber); background: #fffbeb; }}

table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
th {{ background: var(--navy); color: white; padding: 11px 14px; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; text-align: left; }}
td {{ padding: 10px 14px; border-bottom: 1px solid var(--line); font-size: 0.9rem; }}
tr:hover {{ background: #f8fafd; }}
a {{ color: var(--blue); text-decoration: none; font-weight: 600; }}
a:hover {{ text-decoration: underline; }}

.badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.73rem; font-weight: 700; }}
.badge-h {{ background: #d1fae5; color: #065f46; }}
.badge-m {{ background: #fef3c7; color: #92400e; }}
.badge-l {{ background: #fee2e2; color: #991b1b; }}

.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
@media(max-width:768px){{ .two-col{{grid-template-columns:1fr}} }}

.method-box {{ background: linear-gradient(135deg, #f0f4ff, #e8f0fe); border-radius: 14px; padding: 24px; border: 1px solid #d0dfff; margin: 16px 0; }}
.method-box h3 {{ display: flex; align-items: center; gap: 8px; }}
.source-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; margin: 1px 2px; }}
.source-tag.scraped {{ background: #dbeafe; color: #1e40af; }}
.source-tag.search {{ background: #fce7f3; color: #9d174d; }}
.source-tag.teammate {{ background: #d1fae5; color: #065f46; }}

footer {{ text-align: center; padding: 24px; background: var(--navy); color: rgba(255,255,255,0.4); font-size: 0.82rem; }}
footer a {{ color: var(--red); }}
</style>
</head>
<body>

<div class="hero">
<div class="container">
<h1>Hong Kong EMF <span>Market Intelligence</span></h1>
<p class="sub">Executive Summary — 46 event management firms researched across three event lifecycle phases with multi-source evidence collection.</p>
<div class="kpi-row">
<div class="kpi"><div class="num">{total}</div><div class="lbl">Companies</div></div>
<div class="kpi"><div class="num">{pains}</div><div class="lbl">Pain Points</div></div>
<div class="kpi"><div class="num">{emps:,}</div><div class="lbl">Total Employees</div></div>
<div class="kpi hl"><div class="num">{high}</div><div class="lbl">High Fit (8-10)</div></div>
<div class="kpi"><div class="num">{med}</div><div class="lbl">Medium Fit</div></div>
<div class="kpi"><div class="num">{low}</div><div class="lbl">Low Fit</div></div>
</div>
</div>
</div>

<div class="nav"><div class="container">
<a href="#overview" class="active">Overview</a>
<a href="#ch charts">Charts</a>
<a href="#findings">Key Findings</a>
<a href="#method">Methodology</a>
<a href="#tiers">Target Tiers</a>
<a href="#all">All Companies</a>
<a href="index.html">Company Index →</a>
</div></div>

<main><div class="container">

<!-- OVERVIEW -->
<section id="overview">
<h2 class="section-title">Research Overview</h2>
<div class="two-col">
<div class="card">
<h3>What We Analyzed</h3>
<ul>
<li><strong>{total} Hong Kong event management firms</strong> — from boutique agencies (12 staff) to global enterprises (5,000+ staff)</li>
<li><strong>{pains} evidence-based pain points</strong> — avg {avg} per company, categorized by event lifecycle phase</li>
<li><strong>3 data sources per company:</strong> CSV keyword profiles, official website/LinkedIn research, and collaborative teammate analysis</li>
<li><strong>Scoring:</strong> 4-dimension objective fit model — Event Data Scale, Automation Opportunity, Team Leverage, Tech Receptivity</li>
</ul>
</div>
<div class="card">
<h3>What We Found</h3>
<ul>
<li><strong>37% High fit</strong> — {high} companies with strong WeExpand product-market alignment (score 8-10)</li>
<li><strong>37% Medium fit</strong> — {med} companies with good but partial alignment</li>
<li><strong>26% Low fit</strong> — {low} hardware/physical companies where AI impact is limited</li>
<li><strong>#1 pain theme:</strong> Manual sales & client acquisition — nearly every company lacks automated lead generation</li>
<li><strong>Critical gap:</strong> Companies run annual events but have no year-round digital engagement</li>
</ul>
</div>
</div>
</section>

<!-- CHARTS -->
<section id="charts">
<h2 class="section-title">Data Visualizations</h2>
<div class="chart-grid">
<div class="chart-card"><h3>Pain Points by Category</h3><canvas id="painCatChart"></canvas></div>
<div class="chart-card"><h3>Solution Fit Distribution</h3><canvas id="fitChart"></canvas></div>
</div>
<div class="chart-grid">
<div class="chart-card"><h3>Companies by Employee Size</h3><canvas id="empChart"></canvas></div>
<div class="chart-card"><h3>Urgency Breakdown</h3><canvas id="urgChart"></canvas></div>
</div>
</section>

<!-- KEY FINDINGS -->
<section id="findings">
<h2 class="section-title">Key Findings & Insights</h2>

<div class="insight-box red">
<h3>🔴 Critical: The Event Lifecycle is Broken</h3>
<p>Most companies focus only on <strong>DURING-event</strong> execution (physical logistics, booth setup, AV). The <strong>BEFORE</strong> phase (sales, marketing, client acquisition) is entirely manual, and the <strong>AFTER</strong> phase (follow-up, data, community) barely exists. This leaves enormous value on the table — warm leads go cold, attendee data is never captured, and event ROI is limited to 2-3 physical days.</p>
</div>

<div class="insight-box">
<h3>🔵 The Year-Round Gap is Universal</h3>
<p>Whether annual trade shows (CHINAPLAS, Jewellery & Gem WORLD, BEYOND Expo) or biennial maritime events (Marintec China), nearly every organizer has a <strong>massive engagement gap</strong> between events. During those 11-23 months, communities disperse to LinkedIn, trade media, and competitor platforms. WeExpand's year-round digital platform directly addresses this.</p>
</div>

<div class="insight-box green">
<h3>🟢 Lean Teams = Maximum AI Leverage</h3>
<p><strong>TOKEN2049</strong> (36 employees, 20,000+ attendees), <strong>BEYOND Expo</strong> (17 employees, Asia's largest tech expo), <strong>SuperAI</strong> (20 employees, major AI conference) — these companies run enormous events with tiny teams. They are the highest-ROI prospects for WeExpand: AI automation multiplies their output 10x+.</p>
</div>

<div class="insight-box amber">
<h3>🟡 Venue Operators are an Untapped Goldmine</h3>
<p><strong>Kai Tak Sports Park</strong> (HK$30B, 7M+ visitors in Year 1), <strong>HKCEC</strong> (91,500 sqm, hosts Book Fair with 850K visitors), <strong>AsiaWorld-Expo</strong> (70,000 sqm, 10 halls) — these venues generate massive visitor data that goes completely uncaptured. None offer AI-driven exhibitor-visitor matching, smart lead capture, or post-event analytics. Each is a greenfield smart-venue opportunity.</p>
</div>

<div class="card">
<h3>How Scoring Works</h3>
<p>The <strong>WeExpand Solution Fit Score (0-10)</strong> is calculated from 4 objective dimensions based solely on evidence from each company's CSV keywords, employee count, and online profile:</p>
<table style="margin-top:12px;">
<tr><th>Dimension</th><th>Weight</th><th>What It Measures</th></tr>
<tr><td>Event Data Scale</td><td>0-3 pts</td><td>Volume of attendee/exhibitor data flowing through the company — larger events = more data to monetize</td></tr>
<tr><td>Automation Opportunity</td><td>0-4 pts</td><td>How manual/traditional their operations are — more manual = bigger AI win</td></tr>
<tr><td>Team Leverage</td><td>0-3 pts</td><td>How much AI would multiply team output — micro teams get highest multiplier</td></tr>
<tr><td>Tech Receptivity</td><td>0-1 pt</td><td>Digital/tech keywords indicate openness to AI adoption; hardware penalties for pure fabrication</td></tr>
</table>
</div>
</section>

<!-- METHODOLOGY -->
<section id="method">
<h2 class="section-title">Research Methodology & Data Sources</h2>
<div class="method-box">
<h3>📊 Multi-Source Evidence Collection</h3>
<p>Every data point in this report is traceable to a specific source. We do not generate synthetic data.</p>
<div class="two-col" style="margin-top:16px;">
<div>
<h4>Data Sources</h4>
<ul>
<li><span class="source-tag scraped">SITEMAP</span> <strong>Web Scraping</strong> — 318 event records from company sitemaps (8 companies: AsiaWorld-Expo, SuperAI, Eventist, Clarion, CloserStill, RX Global, Milton, EX-R)</li>
<li><span class="source-tag search">SEARCH</span> <strong>Web Search</strong> — 17 verified event records from news outlets, government press, event platforms (Kai Tak, Informa Markets)</li>
<li><span class="source-tag teammate">TEAM</span> <strong>Teammate Research</strong> — 21 companies with contact/outreach/strategic data from 2 collaborators</li>
<li><strong>CSV Analysis</strong> — 46 companies with detailed keyword profiles and employee counts</li>
<li><strong>Official Websites</strong> — Each company's website and LinkedIn page reviewed</li>
</ul>
</div>
<div>
<h4>Pain Point Methodology</h4>
<ul>
<li>Each pain point cites <strong>specific evidence</strong> from the company's data</li>
<li>Categorized into <strong>BEFORE → DURING → AFTER</strong> event lifecycle phases</li>
<li>Urgency rated 🔴High / 🟡Medium / 🟢Low based on business impact</li>
<li>Each pain point mapped to a specific <strong>WeExpand capability</strong></li>
</ul>
</div>
</div>
</div>
</section>

<!-- TARGET TIERS -->
<section id="tiers">
<h2 class="section-title">WeExpand Target Prioritization</h2>

<div class="card">
<h3>🎯 Tier 1 — Prime Targets (Score 8-10, {len(d.get('tier1_prime',[]))} companies)</h3>
<p style="color:var(--muted);margin-bottom:12px;">Highest WeExpand product-market fit. These companies have large data flows, manual operations, lean teams, and tech receptivity.</p>
<table>
<tr><th>#</th><th>Company</th><th>Emp</th><th>Type</th><th>Pains</th><th>Score</th></tr>
{''.join(f'<tr><td>{i+1}</td><td><a href="{c["slug"]}.html">{c["name"]}</a></td><td>{c.get("employees",0)}</td><td>{c.get("type","")}</td><td>{c.get("pain_count",0)}</td><td><span class="badge badge-h">{c.get("fit_score",0)}/10</span></td></tr>' for i,c in enumerate(d.get('tier1_prime',[])))}
</table>
</div>

<div class="card">
<h3>🥈 Tier 2 — Strong Prospects (Score 5-7, {len(d.get('tier2_strong',[]))} companies)</h3>
<p style="color:var(--muted);margin-bottom:12px;">Good alignment with specific gaps. Nurture with case studies.</p>
<table>
<tr><th>#</th><th>Company</th><th>Emp</th><th>Type</th><th>Pains</th><th>Score</th></tr>
{''.join(f'<tr><td>{i+1}</td><td><a href="{c["slug"]}.html">{c["name"]}</a></td><td>{c.get("employees",0)}</td><td>{c.get("type","")}</td><td>{c.get("pain_count",0)}</td><td><span class="badge badge-m">{c.get("fit_score",0)}/10</span></td></tr>' for i,c in enumerate(d.get('tier2_strong',[])))}
</table>
</div>

<div class="card">
<h3>🥉 Tier 3 — Niche Plays (Score 0-4, {len(d.get('tier3_niche',[]))} companies)</h3>
<p style="color:var(--muted);margin-bottom:12px;">Limited AI alignment — physical/hardware businesses where WeExpand primarily helps with client acquisition.</p>
<table>
<tr><th>#</th><th>Company</th><th>Emp</th><th>Type</th><th>Pains</th><th>Score</th></tr>
{''.join(f'<tr><td>{i+1}</td><td><a href="{c["slug"]}.html">{c["name"]}</a></td><td>{c.get("employees",0)}</td><td>{c.get("type","")}</td><td>{c.get("pain_count",0)}</td><td><span class="badge badge-l">{c.get("fit_score",0)}/10</span></td></tr>' for i,c in enumerate(d.get('tier3_niche',[])))}
</table>
</div>
</section>

<!-- ALL COMPANIES -->
<section id="all">
<h2 class="section-title">All 46 Companies — Complete Index</h2>
<table>
<tr><th>#</th><th>Company</th><th>Emp</th><th>Type</th><th>Pains</th><th>Fit</th></tr>
{''.join(f'<tr><td>{i+1}</td><td><a href="{c["slug"]}.html">{c["name"]}</a></td><td>{c.get("employees",0)}</td><td>{c.get("type","")[:35]}</td><td>{c.get("pain_count",0)}</td><td><span class="badge badge-{"h" if c.get("fit_score",0)>=8 else "m" if c.get("fit_score",0)>=5 else "l"}">{c.get("fit_score",0)}/10</span></td></tr>' for i,c in enumerate(d["companies"]))}
</table>
</section>

</div></main>

<footer><div class="container">
<p>Market Understanding Project · {total} companies · {pains} evidence-based pain points · Multi-source data collection · <a href="index.html">Company Index</a></p>
</div></footer>

<script>
new Chart(document.getElementById('painCatChart'),{{
    type:'bar', data:{{labels:{cat_labels},datasets:[{{data:{cat_values},backgroundColor:['#e94560','#3b82f6','#f59e0b','#10b981','#8b5cf6','#14b8a6','#f97316','#06b6d4','#ec4899','#84cc16','#6366f1','#94a3b8'],borderRadius:6}}]}},
    options:{{indexAxis:'y',responsive:true,plugins:{{legend:{{display:false}}}},scales:{{x:{{beginAtZero:true,ticks:{{stepSize:5}}}}}}}}
}});
new Chart(document.getElementById('fitChart'),{{
    type:'doughnut', data:{{labels:['High Fit (8-10)','Medium Fit (5-7)','Low Fit (0-4)'],datasets:[{{data:[{high},{med},{low}],backgroundColor:['#10b981','#f59e0b','#e94560'],borderWidth:2,borderColor:'#fff'}}]}},
    options:{{responsive:true,plugins:{{legend:{{position:'bottom'}}}}}}
}});
new Chart(document.getElementById('empChart'),{{
    type:'bar', data:{{labels:{emp_labels},datasets:[{{data:{emp_values},backgroundColor:['#10b981','#3b82f6','#f59e0b','#e94560'],borderRadius:8}}]}},
    options:{{responsive:true,plugins:{{legend:{{display:false}}}},scales:{{y:{{beginAtZero:true,ticks:{{stepSize:5}}}}}}}}
}});
new Chart(document.getElementById('urgChart'),{{
    type:'doughnut', data:{{labels:{urg_labels},datasets:[{{data:{urg_values},backgroundColor:['#e94560','#f59e0b','#10b981'],borderWidth:2,borderColor:'#fff'}}]}},
    options:{{responsive:true,plugins:{{legend:{{position:'bottom'}}}}}}
}});
</script>
</body>
</html>"""

with open("/Users/lok/Project/MarketUnderstanding/outputs/website/summary.html", "w") as f:
    f.write(html)
print(f"✅ summary.html rewritten — {len(html):,} bytes")
