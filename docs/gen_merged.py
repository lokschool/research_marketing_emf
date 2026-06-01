#!/usr/bin/env python3
"""Generate merged_report.html combining me + teamate1 + teamate2 data."""
import json

with open("/Users/lok/Project/MarketUnderstanding/outputs/website/merged_data.json") as f:
    merged = json.load(f)

companies = merged["companies"]
total = merged["total"]

# Count stats
me_only = len([c for c in companies if c["source"] == "me" and not c.get("has_t1") and not c.get("has_t2")])
all_three = len([c for c in companies if c.get("has_t1") and c.get("has_t2")])
t1_contrib = len([c for c in companies if c.get("has_t1")])
t2_contrib = len([c for c in companies if c.get("has_t2")])
with_contacts = len([c for c in companies if c.get("contacts")])
with_outreach = len([c for c in companies if c.get("outreach")])

rows = ""
for i, c in enumerate(companies):
    badge_me = '<span class="src src-me">Me</span>' if c["source"] == "me" else ""
    badge_t1 = '<span class="src src-t1">T1</span>' if c.get("has_t1") else ""
    badge_t2 = '<span class="src src-t2">T2</span>' if c.get("has_t2") else ""
    contact_note = f'📇 {len(c["contacts"])} contacts' if c.get("contacts") else ""
    outreach_note = "🎯 outreach" if c.get("outreach") else ""
    
    fit_badge = ""
    if c["fit_score"] >= 8:
        fit_badge = f'<span class="badge badge-high">{c["fit_score"]}/10</span>'
    elif c["fit_score"] >= 5:
        fit_badge = f'<span class="badge badge-med">{c["fit_score"]}/10</span>'
    elif c["fit_score"] > 0:
        fit_badge = f'<span class="badge badge-low">{c["fit_score"]}/10</span>'
    
    rows += f"""
    <tr>
        <td>{i+1}</td>
        <td><strong>{c['name']}</strong></td>
        <td>{c['employees']}</td>
        <td>{c['type']}</td>
        <td>{c['pain_count']}</td>
        <td>{fit_badge}</td>
        <td>{badge_me}{badge_t1}{badge_t2}</td>
        <td style="font-size:12px;color:#888;">{contact_note} {outreach_note}</td>
    </tr>"""

# Detailed cards for companies with teammate data
detail_cards = ""
for c in companies:
    if not c.get("has_t1") and not c.get("has_t2"):
        continue
    
    detail_cards += f"""
    <div class="detail-card">
        <div class="detail-header">
            <h3>{c['name']}</h3>
            <div class="detail-badges">
                {'<span class="src src-me">My Analysis</span>' if c['source'] == 'me' else ''}
                {'<span class="src src-t1">Teamate1 Contacts</span>' if c.get('has_t1') else ''}
                {'<span class="src src-t2">Teamate2 Strategy</span>' if c.get('has_t2') else ''}
            </div>
        </div>
        <div class="detail-grid">"""
    
    # My pain point summary
    if c["source"] == "me":
        detail_cards += f"""
            <div class="detail-col">
                <h4>My Analysis</h4>
                <p>Fit: <strong>{c['fit_level']}</strong> ({c['fit_score']}/10) · {c['pain_count']} pain points · {c['employees']} employees</p>
                <p><a href="{c['slug']}.html" target="_blank">→ Full Report</a></p>
            </div>"""
    
    # Teamate1 contacts + outreach
    if c.get("has_t1"):
        detail_cards += f"""
            <div class="detail-col">
                <h4>Teamate1 — Contacts & Outreach</h4>"""
        if c.get("contacts"):
            for contact in c["contacts"][:3]:
                detail_cards += f"""
                <div class="contact-card"><strong>{contact['name']}</strong><br><small>{contact['role']}</small></div>"""
        if c.get("outreach"):
            detail_cards += f"""
                <p style="margin-top:8px;font-size:13px;"><strong>🎯 Outreach:</strong> {c['outreach'][:200]}...</p>"""
        if c.get("pains_t1"):
            detail_cards += """
                <ul style="margin-top:8px;font-size:13px;">"""
            for p in c["pains_t1"][:3]:
                detail_cards += f'<li><strong>{p["title"]}</strong></li>'
            detail_cards += "</ul>"
        detail_cards += "</div>"
    
    # Teamate2 strategic insights
    if c.get("has_t2"):
        detail_cards += f"""
            <div class="detail-col">
                <h4>Teamate2 — Strategic Insights</h4>
                <ul style="font-size:13px;">"""
        for insight in c.get("insights_t2", [])[:5]:
            detail_cards += f"<li>{insight[:150]}</li>"
        detail_cards += "</ul></div>"
    
    detail_cards += """
        </div>
    </div>"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Merged Report — Hong Kong EMF Research | Team Collaboration</title>
    <style>
        :root {{ --navy: #0A192F; --teal: #00A896; --gold: #D4AF37; --cyan: #06B6D4; --red: #e94560;
               --bg: #F8FAFC; --card: #FFFFFF; --text: #1E293B; --muted: #64748B; --line: #E2E8F0; }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); line-height:1.6; }}
        .container {{ max-width: 1320px; margin: 0 auto; padding: 0 24px; }}
        
        .merged-hero {{
            background: linear-gradient(135deg, var(--navy) 0%, #112240 50%, #1a365d 100%);
            color: white; padding: 60px 0 50px; text-align: center;
        }}
        .merged-hero h1 {{ font-size: 2.5rem; font-weight: 800; }}
        .merged-hero h1 span {{ color: var(--teal); }}
        .merged-hero .subtitle {{ font-size: 1.1rem; opacity: 0.85; max-width: 700px; margin: 10px auto 0; }}
        
        .stat-row {{
            display: flex; justify-content: center; gap: 24px; margin-top: 32px; flex-wrap: wrap;
        }}
        .stat {{ background: rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 24px; text-align: center; min-width: 120px; }}
        .stat .num {{ font-size: 2rem; font-weight: 800; }}
        .stat .lbl {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }}
        .stat.accent {{ background: rgba(0,168,150,0.15); }}
        .stat.accent .num {{ color: var(--teal); }}
        
        .legend {{ display: flex; gap: 20px; justify-content: center; margin: 20px 0 0; flex-wrap: wrap; }}
        .legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 0.85rem; }}
        .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
        .dot-me {{ background: #667eea; }}
        .dot-t1 {{ background: #00A896; }}
        .dot-t2 {{ background: #D4AF37; }}
        
        main {{ padding: 40px 0; }}
        .section-title {{ font-size: 1.5rem; font-weight: 700; margin: 40px 0 16px; padding-bottom: 8px; border-bottom: 3px solid var(--teal); display: inline-block; }}
        .section-title:first-child {{ margin-top: 0; }}
        
        table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }}
        th {{ background: var(--navy); color: white; padding: 12px 14px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; text-align: left; }}
        td {{ padding: 10px 14px; border-bottom: 1px solid var(--line); font-size: 0.9rem; }}
        tr:hover {{ background: #f8fafd; }}
        
        .src {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; margin: 1px 2px; }}
        .src-me {{ background: #eef0ff; color: #667eea; }}
        .src-t1 {{ background: #e6f7f5; color: #00A896; }}
        .src-t2 {{ background: #fff8e6; color: #b8941f; }}
        
        .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}
        .badge-high {{ background: #d4edda; color: #155724; }}
        .badge-med {{ background: #fff3cd; color: #856404; }}
        .badge-low {{ background: #f8d7da; color: #721c24; }}
        
        .detail-card {{
            background: var(--card); border-radius: 12px; padding: 24px; margin: 16px 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05); border: 1px solid var(--line);
        }}
        .detail-header {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; }}
        .detail-header h3 {{ font-size: 1.15rem; }}
        .detail-badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
        .detail-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .detail-col h4 {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); margin-bottom: 8px; }}
        .detail-col p, .detail-col li {{ font-size: 0.88rem; color: var(--text); }}
        .detail-col ul {{ padding-left: 18px; }}
        .detail-col li {{ margin: 4px 0; }}
        .contact-card {{ padding: 8px 12px; background: #f8fafc; border-radius: 6px; margin: 4px 0; border: 1px solid var(--line); }}
        
        footer {{ text-align: center; padding: 24px; background: var(--navy); color: rgba(255,255,255,0.5); font-size: 0.85rem; }}
        footer a {{ color: var(--teal); }}
        
        .nav {{ display: flex; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--line); position: sticky; top: 0; background: var(--bg); z-index: 10; }}
        .nav a {{ color: var(--muted); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
        .nav a:hover {{ color: var(--teal); }}
    </style>
</head>
<body>

<div class="merged-hero">
    <div class="container">
        <h1>Hong Kong EMF <span>— Merged Research Report</span></h1>
        <p class="subtitle">Combined intelligence from 3 collaborators: My structured research + Teamate1's contact/outreach data + Teamate2's strategic analysis across {total} companies.</p>
        <div class="stat-row">
            <div class="stat"><div class="num">{total}</div><div class="lbl">Total Companies</div></div>
            <div class="stat"><div class="num">{len([c for c in companies if c['source']=='me'])}</div><div class="lbl">My Research</div></div>
            <div class="stat"><div class="num">{t1_contrib}</div><div class="lbl">Teamate1 Contact Data</div></div>
            <div class="stat"><div class="num">{t2_contrib}</div><div class="lbl">Teamate2 Strategy</div></div>
            <div class="stat accent"><div class="num">{all_three}</div><div class="lbl">Full Collaboration</div></div>
        </div>
        <div class="legend">
            <div class="legend-item"><div class="dot dot-me"></div> My Work (structured research, pain points, solution fit)</div>
            <div class="legend-item"><div class="dot dot-t1"></div> Teamate1 (contacts, outreach angles, workflow pain points)</div>
            <div class="legend-item"><div class="dot dot-t2"></div> Teamate2 (strategic enterprise analysis, challenges)</div>
        </div>
    </div>
</div>

<main>
<div class="container">

<h2 class="section-title">All Companies — Master Index</h2>
<p style="color:var(--muted);margin-bottom:12px;">{total} companies. Click company name for detailed report. Sources indicated in Attribution column.</p>

<table>
    <thead>
        <tr><th>#</th><th>Company</th><th>Emp</th><th>Type</th><th>Pains</th><th>Fit</th><th>Sources</th><th>Notes</th></tr>
    </thead>
    <tbody>{rows}</tbody>
</table>

<h2 class="section-title">Collaboration Details — Companies with Multiple Contributors</h2>
<p style="color:var(--muted);margin-bottom:12px;">Showing companies where two or more team members contributed data.</p>

{detail_cards}

</div>
</main>

<footer>
    <div class="container">
        <p>Merged Research Report · {total} companies · My work + Teamate1 contact data + Teamate2 strategic analysis · Generated 2026-06-01</p>
    </div>
</footer>

</body>
</html>"""

out = "/Users/lok/Project/MarketUnderstanding/outputs/website/merged_report.html"
with open(out, "w") as f:
    f.write(html)

print(f"✅ Merged report generated: {out}")
print(f"   {total} companies, {t1_contrib} with T1 contacts, {t2_contrib} with T2 strategy")
print(f"   {all_three} companies have full 3-source collaboration")
