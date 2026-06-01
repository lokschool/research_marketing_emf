#!/usr/bin/env python3
"""Generate HTML report pages for all companies from searched and report markdown files."""

import csv
import os
import re
import html
from pathlib import Path

BASE_DIR = Path("/Users/lok/Project/MarketUnderstanding")
SEARCHED_DIR = BASE_DIR / "outputs" / "searched"
REPORT_DIR = BASE_DIR / "outputs" / "reports"
WEBSITE_DIR = BASE_DIR / "outputs" / "website"
CSS_PATH = "css/style.css"

def slugify(name):
    return name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "").replace(",", "").replace("'", "").replace("/", "_").replace(".", "").replace("--", "-")

def find_file(directory, company_name, suffix):
    """Find a file matching the company name in the given directory.
    Tries exact slug match first, then fuzzy match."""
    slug = slugify(company_name)
    suffix_stem = suffix.replace(".md", "")  # Strip extension for stem matching
    exact = directory / f"{slug}{suffix}"
    if exact.exists():
        return exact
    
    # Try without common suffixes like " Management Limited", " Limited", " Ltd", etc.
    short_name = company_name
    for remove in [" Management Limited", " Pte Ltd", " Co Ltd", " GmbH", " Limited", " Ltd", " (Management) Limited", " - Marketing Agency", " (Shanghai) Co Ltd", " (Asia) Limited"]:
        if remove in short_name:
            candidate = slugify(short_name.replace(remove, ""))
            cand_path = directory / f"{candidate}{suffix}"
            if cand_path.exists():
                return cand_path
    
    # Try partial matching: find all files in directory and match by name segments
    name_parts = slugify(company_name).split("_")
    existing_files = list(directory.glob(f"*{suffix}"))
    
    for f in existing_files:
        f_stem = f.stem.replace(suffix_stem, "")
        # Count how many name parts match
        matches = sum(1 for part in name_parts if part in f_stem)
        if matches >= 2:  # At least 2 parts match
            return f
    
    # Last resort 1: try checking if any file matches by normalizing separators
    slug_normalized = slug.replace("-", "_")
    for f in existing_files:
        f_stem = f.stem.replace(suffix_stem, "")
        if f_stem == slug_normalized:
            return f
    
    # Last resort 2: subsequence match (ignore dashes/underscores)
    slug_clean = slug.replace("-", "").replace("_", "")
    for f in existing_files:
        f_stem = f.stem.replace(suffix_stem, "")
        f_clean = f_stem.replace("-", "").replace("_", "")
        slug_chars = list(slug_clean)
        f_chars = list(f_clean)
        si = 0
        for fc in f_chars:
            while si < len(slug_chars) and slug_chars[si] != fc:
                si += 1
            if si >= len(slug_chars):
                break
            si += 1
        else:
            return f
    
    # Last resort 2: try first word of company name
    first_word = slugify(company_name.split()[0] if " " in company_name else company_name)
    for f in existing_files:
        if f.stem.startswith(first_word):
            return f
    
    return exact  # Return the non-existent path as fallback

def parse_markdown_sections(md_text):
    """Parse markdown into sections based on ## headers"""
    sections = {}
    current_section = "_preamble"
    current_content = []
    
    for line in md_text.split("\n"):
        if line.startswith("## "):
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections

def extract_event_items(text):
    """Extract bullet point event items"""
    items = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- **") or line.startswith("**"):
            # Clean up
            cleaned = re.sub(r'\*\*', '', line).strip('- ')
            items.append(cleaned)
        elif line.startswith("- ") and not line.startswith("- **"):
            cleaned = line[2:].strip()
            if cleaned and not cleaned.startswith("[") and not cleaned.startswith("`"):
                items.append(cleaned)
    return items

def extract_pain_points(pain_text):
    """Extract individual pain points from various formats including phased structure."""
    points = []
    
    # Try #### Pain Point X: format (new phased structure)
    current_phase = ""
    current = None
    for line in pain_text.split("\n"):
        stripped = line.strip()
        
        # Phase headers
        if stripped.startswith("### Before") or stripped.startswith("### During") or stripped.startswith("### After"):
            phase_map = {"Before": "BEFORE", "During": "DURING", "After": "AFTER"}
            for k, v in phase_map.items():
                if k in stripped:
                    current_phase = v
                    break
        
        # Pain point headers (#### level)
        if stripped.startswith("#### Pain Point"):
            if current:
                points.append(current)
            title = stripped.replace("#### ", "").strip()
            current = {"title": title, "evidence": "", "impact": "", "urgency": "", "phase": current_phase}
        elif stripped.startswith("### Pain Point"):
            if current:
                points.append(current)
            title = stripped.replace("### ", "").strip()
            current = {"title": title, "evidence": "", "impact": "", "urgency": "", "phase": current_phase}
        elif current:
            if "**Evidence:**" in stripped:
                for sep in ["**Evidence:**", "**Evidence"]:
                    if sep in stripped:
                        current["evidence"] = stripped.split(sep, 1)[1].strip()
                        break
            elif "**Impact:**" in stripped:
                for sep in ["**Impact:**", "**Impact"]:
                    if sep in stripped:
                        current["impact"] = stripped.split(sep, 1)[1].strip()
                        break
            elif "**Urgency:**" in stripped:
                for sep in ["**Urgency:**", "**Urgency"]:
                    if sep in stripped:
                        raw = stripped.split(sep, 1)[1].strip()
                        # Clean emoji
                        raw = raw.replace("🔴", "").replace("🟡", "").replace("🟢", "").strip()
                        current["urgency"] = raw
                        break
    
    if current:
        points.append(current)
    
    # If no points found, try numbered list format
    if not points:
        for line in pain_text.split("\n"):
            stripped = line.strip()
            match = re.match(r'^\d+\.\s+\*\*(.+?)\*\*\s*[—\-–]\s*(.+?)(?:\s*\*\*Urgency:\s*(.+?)\*\*)?\.?$', stripped)
            if match:
                title = match.group(1).strip()
                evidence = match.group(2).strip()
                urgency = match.group(3).strip() if match.group(3) else "Medium"
                points.append({"title": title, "evidence": evidence, "impact": "", "urgency": urgency, "phase": ""})
    
    return points

def extract_table_rows(text):
    """Extract markdown table rows"""
    rows = []
    in_table = False
    header_skipped = False
    for line in text.split("\n"):
        if line.startswith("|") and "---" in line:
            in_table = True
            header_skipped = False
            continue
        if in_table and line.startswith("|"):
            if not header_skipped:
                header_skipped = True
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if cells:
                rows.append(cells)
        elif in_table and not line.startswith("|"):
            in_table = False
    return rows

def extract_citations(text):
    """Extract citation lines"""
    citations = []
    for line in text.split("\n"):
        match = re.match(r'\[(.+?)\s*-\s*(.+?)\s*-\s*(https?://\S+)\s*-\s*(.+?)\]', line.strip())
        if match:
            citations.append({
                "source": match.group(1),
                "title": match.group(2),
                "url": match.group(3),
                "date": match.group(4)
            })
    return citations

def html_escape(text):
    return html.escape(text)

def md_to_html(text):
    """Simple markdown to HTML converter"""
    if not text:
        return ""
    
    lines = text.split("\n")
    result = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Bold
        stripped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
        # Italic
        stripped = re.sub(r'\*(.+?)\*', r'<em>\1</em>', stripped)
        # Links
        stripped = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', stripped)
        
        if stripped.startswith("### "):
            if in_list:
                result.append("</ul>")
                in_list = False
            result.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith("**") and ":**" in stripped:
            if in_list:
                result.append("</ul>")
                in_list = False
            result.append(f'<p><strong>{stripped}</strong></p>')
        elif stripped.startswith("- **"):
            if not in_list:
                result.append('<ul>')
                in_list = True
            cleaned = stripped[2:]
            result.append(f'<li>{cleaned}</li>')
        elif stripped.startswith("- "):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{stripped[2:]}</li>')
        elif stripped.startswith("**Scale"):
            if in_list:
                result.append("</ul>")
                in_list = False
            result.append(f'<p class="evidence"><em>{stripped}</em></p>')
        elif stripped.startswith("**") and stripped.endswith("**"):
            if in_list:
                result.append("</ul>")
                in_list = False
            result.append(f'<p><strong>{stripped[2:-2]}</strong></p>')
        elif stripped == "":
            if in_list:
                result.append("</ul>")
                in_list = False
        elif stripped.startswith("[") and " - http" in stripped:
            continue
        else:
            if stripped:
                if in_list:
                    result.append("</ul>")
                    in_list = False
                result.append(f'<p>{stripped}</p>')
    
    if in_list:
        result.append("</ul>")
    
    return "\n".join(result)


def generate_company_html(company, searched_path, report_path, tm_data=None):
    """Generate HTML for a single company"""
    
    # Read searched file
    searched_text = ""
    if searched_path.exists():
        with open(searched_path, "r") as f:
            searched_text = f.read()
    
    # Read report file
    report_text = ""
    if report_path.exists():
        with open(report_path, "r") as f:
            report_text = f.read()
    
    searched_sections = parse_markdown_sections(searched_text)
    report_sections = parse_markdown_sections(report_text)
    
    name = company.get("Company Name", "Unknown")
    employees = company.get("# Employees", "N/A")
    website = company.get("Website", "#")
    keywords = company.get("Keywords", "")
    linkedin = company.get("Company Linkedin Url", "#")
    
    # Extract data from sections
    business_model = md_to_html(searched_sections.get("1. Business Model", ""))
    target_customers = md_to_html(searched_sections.get("2. Target Customers", ""))
    events_section = searched_sections.get("3. Events Conducted (with Details)", searched_sections.get("3. Number of Events", ""))
    events_html = md_to_html(events_section)
    event_scale = md_to_html(searched_sections.get("4. Event Scale", ""))
    event_types = md_to_html(searched_sections.get("5. Event Types", ""))
    event_themes = md_to_html(searched_sections.get("6. Event Themes", ""))
    digital_maturity = md_to_html(searched_sections.get("7. Digital Transformation Maturity", ""))
    tech_stack = md_to_html(searched_sections.get("8. Tech Stack", ""))
    hiring = md_to_html(searched_sections.get("9. Hiring Signals", ""))
    reviews = md_to_html(searched_sections.get("10. Reviews & Media Mentions", ""))
    geo = md_to_html(searched_sections.get("11. Geographic Presence", ""))
    expansion = md_to_html(searched_sections.get("12. Expansion Signals", ""))
    
    # Evidence
    evidence_table = searched_sections.get("Data Evidence List", "")
    evidence_rows = extract_table_rows(evidence_table)
    
    # Pain points - try multiple section header formats (including phased header)
    pain_text = (report_sections.get("2. Pain Point Analysis", "") or 
                 report_sections.get("2. Pain Point Analysis — By Event Phase", "") or
                 report_sections.get("Pain Points", "") or
                 report_sections.get("Pain Point Analysis", "") or "")
    # Also try partial match
    if not pain_text:
        for key in report_sections:
            if "Pain Point Analysis" in key or "Pain Points" in key:
                pain_text = report_sections[key]
                break
    pain_points = extract_pain_points(pain_text)
    
    # Solution fit
    fit_text = (report_sections.get("3. Solution Fit Mapping", "") or
                report_sections.get("Solution Fit", ""))
    fit_rows = extract_table_rows(fit_text)
    
    # Strategic assessment - always convert markdown to clean HTML
    strategy_raw = (report_sections.get("4. Strategic Opportunity Assessment", "") or
                    report_sections.get("Strategic Opportunity Assessment", "") or "")
    # Strip redundant fit line (shown separately), citations, and HRs
    strategy_raw = re.sub(r'\*\*Overall Fit:?\*\*[^\n]*\n?', '', strategy_raw)
    strategy_raw = re.sub(r'\[about_my_company\.md[^\]]*\]', '', strategy_raw)
    strategy_raw = re.sub(r'\n---\n', '\n', strategy_raw)
    strategy_raw = re.sub(r'^\s*---\s*$', '', strategy_raw, flags=re.MULTILINE)
    strategy = md_to_html(strategy_raw.strip()) if strategy_raw.strip() else ""
    
    # Overall fit
    fit_match = re.search(r'(?:\*\*)?\s*(?:Overall\s*)?Fit:[\s*]*(High|Medium|Low|Moderate|Very High)\s*\((\d+)\s*/\s*10\)', report_text)
    # Normalize: "Very High" -> "High", "Moderate" -> "Medium"
    if fit_match:
        raw = fit_match.group(1)
        if raw == "Very High":
            fit_level = "High"
        elif raw == "Moderate":
            fit_level = "Medium"
        else:
            fit_level = raw
        fit_score = fit_match.group(2)
    else:
        fit_level = "N/A"
        fit_score = "N/A"
    
    # Extract pain point summary text for display
    pain_text_display = md_to_html(pain_text) if not pain_points else ""
    
    # Citations
    citation_text = report_sections.get("5. Citation Index", "")
    citations = extract_citations(searched_text + "\n" + report_text)
    
    # Build urgent pain points summary
    urgent_pains = [p for p in pain_points if "High" in p.get("urgency", "")]
    
    def uclass(urgency):
        if "High" in urgency: return "urgency-high"
        if "Medium" in urgency: return "urgency-medium"
        return "urgency-low"
    
    def fit_class(fit):
        if "Strong" in fit or "strong" in fit.lower(): return "fit-strong"
        if "Moderate" in fit or "moderate" in fit.lower(): return "fit-moderate"
        return "fit-weak"
    
    # Build HTML
    slug = slugify(name)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_escape(name)} — Research Report | Market Understanding</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<header>
    <div class="container">
        <div>
            <h1>{html_escape(name)} <span>Research Report</span></h1>
            <div class="meta">Generated: 2026-05-29 | Market Understanding Project</div>
        </div>
        <a href="index.html" class="back-link">← All Companies</a>
        <a href="summary.html" class="back-link" style="margin-left:16px;">📊 Summary</a>
    </div>
</header>

<div class="hero">
    <div class="container">
        <div class="company-name">{html_escape(name)}</div>
        <div class="tagline">Hong Kong Event Management Firm Research</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-label">Employees</div>
                <div class="stat-value">{html_escape(employees)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Solution Fit</div>
                <div class="stat-value">{html_escape(fit_level)} ({fit_score}/10)</div>
            </div>
            <div class="stat">
                <div class="stat-label">Pain Points</div>
                <div class="stat-value">{len(pain_points)}</div>
            </div>
        </div>
    </div>
</div>

<div class="tab-nav">
    <div class="container">
        <button class="tab-btn active" onclick="scrollToSection('overview')">Overview</button>
        <button class="tab-btn" onclick="scrollToSection('events')">Events</button>
        <button class="tab-btn" onclick="scrollToSection('painpoints')">Pain Points</button>
        <button class="tab-btn" onclick="scrollToSection('solution')">Solution Fit</button>
        <button class="tab-btn" onclick="scrollToSection('evidence')">Evidence</button>
    </div>
</div>

<main>
<div class="container">

<!-- OVERVIEW -->
<section id="overview" class="section">
    <h2 class="section-title">Company Overview</h2>
    
    <div class="card">
        <h3>Business Model</h3>
        {business_model}
    </div>

    <div class="two-col">
        <div class="card">
            <h3>Target Customers</h3>
            {target_customers}
        </div>
        <div class="card">
            <h3>Geographic Presence</h3>
            {geo}
        </div>
    </div>

    <div class="two-col">
        <div class="card">
            <h3>Digital Transformation Maturity</h3>
            {digital_maturity}
        </div>
        <div class="card">
            <h3>Tech Stack</h3>
            {tech_stack}
        </div>
    </div>

    <div class="two-col">
        <div class="card">
            <h3>Hiring Signals</h3>
            {hiring}
        </div>
        <div class="card">
            <h3>Reviews & Media</h3>
            {reviews}
        </div>
    </div>
</section>

<!-- EVENTS -->
<section id="events" class="section">
    <h2 class="section-title">Events & Capabilities</h2>
    
    <div class="card">
        <h3>Events Conducted</h3>
        {events_html}
    </div>

    <div class="card-grid">
        <div class="card">
            <h3>Event Scale</h3>
            {event_scale}
        </div>
        <div class="card">
            <h3>Event Types</h3>
            {event_types}
        </div>
        <div class="card">
            <h3>Event Themes</h3>
            {event_themes}
        </div>
        <div class="card">
            <h3>Expansion Signals</h3>
            {expansion}
        </div>
    </div>
</section>

<!-- PAIN POINTS -->
<section id="painpoints" class="section">
    <h2 class="section-title">Pain Point Analysis</h2>
"""

    if pain_points:
        current_phase = ""
        for i, pp in enumerate(pain_points, 1):
            phase_label = ""
            if pp.get("phase"):
                if pp["phase"] != current_phase:
                    current_phase = pp["phase"]
                    phase_emoji = {"BEFORE": "📋", "DURING": "🎯", "AFTER": "📊"}
                    phase_name = {"BEFORE": "Before Event — Planning & Sales", "DURING": "During Event — Execution & Engagement", "AFTER": "After Event — Follow-up & Data"}
                    em = phase_emoji.get(current_phase, "")
                    pn = phase_name.get(current_phase, current_phase)
                    html_content += f"""
    <div style="margin-top:20px;margin-bottom:4px;padding:8px 16px;background:linear-gradient(135deg,#f0f4ff,#e8f0fe);border-radius:8px;font-weight:700;font-size:0.85rem;color:#0f3460;">
        {em} {pn}
    </div>
"""
            html_content += f"""
    <div class="card pain-point">
        <h4>#{i}: {html_escape(pp['title'])}</h4>
        {f'<div class="evidence">{html_escape(pp["evidence"])}</div>' if pp.get("evidence") else ""}
        {f'<div class="impact"><strong>Impact:</strong> {html_escape(pp["impact"])}</div>' if pp.get("impact") else ""}
        {f'<span class="urgency {uclass(pp.get("urgency", ""))}">{html_escape(pp.get("urgency", "Unspecified"))} Urgency</span>' if pp.get("urgency") else ""}
    </div>
"""
    elif pain_text_display:
        html_content += f"""
    <div class="card">
        {pain_text_display}
    </div>
"""
    else:
        html_content += """
    <div class="card">
        <p><em>No detailed pain point analysis available for this company.</em></p>
    </div>
"""

    html_content += """
</section>

<!-- SOLUTION FIT -->
<section id="solution" class="section">
    <h2 class="section-title">WeExpand Solution Fit</h2>
"""

    if fit_rows:
        html_content += """
    <table class="fit-table">
        <thead><tr><th>Pain Point</th><th>WeExpand Capability</th><th>Fit Strength</th></tr></thead>
        <tbody>
"""
        for row in fit_rows:
            if len(row) >= 3:
                html_content += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td class="{fit_class(row[2])}">{row[2]}</td>
            </tr>
"""
        html_content += """
        </tbody>
    </table>
"""

    if strategy:
        html_content += f"""
    <div class="card">
        <h3>Strategic Opportunity Assessment</h3>
        {strategy}
    </div>
"""

    # Recommendations box
    if fit_level and fit_level != "N/A":
        score_val = int(fit_score) if fit_score != "N/A" else 5
        gradient = "#667eea" if score_val >= 7 else ("#f39c12" if score_val >= 4 else "#e74c3c")
        html_content += f"""
    <div class="opportunity-card" style="background: linear-gradient(135deg, {gradient}, #764ba2);">
        <h3>Overall Solution Fit</h3>
        <div class="score">{fit_score}<span>/10 — {html_escape(fit_level)}</span></div>
        <p>This company presents a <strong>{html_escape(fit_level.lower())}</strong> opportunity for WeExpand's agentic AI solutions, with {len(pain_points)} identified pain points addressable through our platform.</p>
    </div>
"""

    html_content += f"""
</section>

<!-- RESEARCH METHODOLOGY -->
<section id=\"methodology\" class=\"section\">
    <h2 class=\"section-title\">Research Methodology & Sources</h2>
    <div class=\"card\">
        <h3>Data Collection Approach</h3>
        <ul>
            <li><strong>Primary Sources:</strong> Company official website ({html_escape(website)}), LinkedIn company page ({html_escape(linkedin)})</li>
            <li><strong>Secondary Sources:</strong> News outlets (QQ News, Sina Finance, Sohu, 163.com, People's Daily), event platforms (Clocate, QuFair, Tripadvisor), government press releases (info.gov.hk)</li>
            <li><strong>Internal Data:</strong> df_company.csv ({html_escape(employees)} employees, keyword profile)</li>
            <li><strong>Collection Date:</strong> 2026-05-29</li>
            <li><strong>Method:</strong> Structured web search, official website analysis, LinkedIn page review, keyword-based inference for digital maturity assessment</li>
        </ul>
        <p style=\"margin-top:12px;font-size:0.85rem;color:#888;\"><em>Note: Where specific data points are unavailable, we state \"No public data found\" in accordance with PROJECT_RULES.md. All pain point analyses are evidence-based and linked to specific data sources.</em></p>
    </div>
</section>
"""

    html_content += """
<!-- EVIDENCE -->
<section id="evidence" class="section">
    <h2 class="section-title">Evidence & Citations</h2>
"""

    if evidence_rows:
        html_content += """
    <div class="card">
        <table class="fit-table">
            <thead><tr><th>#</th><th>Claim</th><th>Source</th></tr></thead>
            <tbody>
"""
        for row in evidence_rows:
            if len(row) >= 3:
                html_content += f"""
            <tr>
                <td>{row[0] if len(row) > 0 else ""}</td>
                <td>{row[1] if len(row) > 1 else row[0] if len(row) == 1 else ""}</td>
                <td>{row[2] if len(row) > 2 else row[1] if len(row) == 2 else ""}</td>
            </tr>
"""
        html_content += """
            </tbody>
        </table>
    </div>
"""

    if citations:
        html_content += """
    <div class="card">
        <h3>External Sources</h3>
        <ul class="evidence-list">
"""
        for c in citations[:15]:
            html_content += f"""
            <li>
                <span class="claim">{html_escape(c['title'])}</span>
                <span class="source"><a href="{html_escape(c['url'])}" target="_blank">{html_escape(c['source'])}</a> — {html_escape(c['date'])}</span>
            </li>
"""
        html_content += """
        </ul>
    </div>
"""

    # Keywords tag cloud
    if keywords:
        kws = [k.strip() for k in keywords.split(",") if k.strip()]
        html_content += """
    <div class="card">
        <h3>Keywords</h3>
        <div>
"""
        for kw in kws[:30]:
            html_content += f'<span class="tag tag-event">{html_escape(kw)}</span>\n'
        html_content += """
        </div>
    </div>
"""

    html_content += """
</section>

</div>
</main>

<footer>
    <div class="container">
        <p>Market Understanding Project · Research generated 2026-05-29 · <a href="index.html" style="color:rgba(255,255,255,0.7);">All Companies</a> · <a href="summary.html" style="color:#e94560;">Executive Summary</a></p>
    </div>
</footer>

<script>
function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth', block: 'start' });
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
}
</script>

</body>
</html>"""
    
    out_path = WEBSITE_DIR / f"{slug}.html"
    with open(out_path, "w") as f:
        f.write(html_content)
    
    return {
        "name": name,
        "employees": employees,
        "fit_level": fit_level,
        "fit_score": fit_score,
        "pain_points": len(pain_points),
        "slug": slug
    }


def generate_index(companies_data):
    """Generate the index.html page listing all companies"""
    
    company_rows = ""
    for c in companies_data:
        score = int(c["fit_score"]) if c["fit_score"] != "N/A" else 0
        score_badge = f'<span class="tag tag-theme">{c["fit_level"]} ({c["fit_score"]}/10)</span>' if c["fit_level"] != "N/A" else '<span class="tag tag-event">N/A</span>'
        
        company_rows += f"""
        <tr>
            <td><a href="{c['slug']}.html"><strong>{html_escape(c['name'])}</strong></a></td>
            <td>{html_escape(c['employees'])}</td>
            <td>{score_badge}</td>
            <td>{c['pain_points']} identified</td>
        </tr>"""
    
    # Count stats
    total = len(companies_data)
    high = sum(1 for c in companies_data if c["fit_level"] == "High")
    medium = sum(1 for c in companies_data if c["fit_level"] == "Medium")
    
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hong Kong Event Management Firms — Research Dashboard | Market Understanding</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .dashboard-hero {{
            background: linear-gradient(135deg, #1a1a2e, #0f3460, #16213e);
            color: white;
            padding: 60px 0;
            text-align: center;
        }}
        .dashboard-hero h1 {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 12px; }}
        .dashboard-hero h1 span {{ color: var(--highlight); }}
        .dashboard-hero .subtitle {{ font-size: 1.15rem; opacity: 0.85; max-width: 700px; margin: 0 auto; }}
        .stat-bar {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 32px;
            flex-wrap: wrap;
        }}
        .stat-bar .stat-item {{ text-align: center; }}
        .stat-bar .stat-num {{ font-size: 2.5rem; font-weight: 800; }}
        .stat-bar .stat-label {{ font-size: 0.85rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px; }}
        .company-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        .company-table th {{
            background: var(--accent);
            color: white;
            padding: 14px 16px;
            text-align: left;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .company-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
        }}
        .company-table tr:hover {{ background: #f8f9ff; }}
        .company-table a {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
        }}
        .company-table a:hover {{ color: var(--highlight); text-decoration: underline; }}
        .filter-bar {{
            display: flex;
            gap: 12px;
            margin: 24px 0;
            flex-wrap: wrap;
        }}
        .filter-bar input {{
            flex: 1;
            min-width: 250px;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }}
        .filter-bar input:focus {{ border-color: var(--highlight); }}
        .filter-btn {{
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        .filter-btn.active {{ background: var(--highlight); color: white; }}
        .filter-btn:not(.active) {{ background: white; color: var(--text); border: 2px solid var(--border); }}
    </style>
</head>
<body>

<div class="dashboard-hero">
    <div class="container">
        <h1>Hong Kong<span> Event Management</span> Firms</h1>
        <p class=\"subtitle\">Comprehensive research and analysis of {total} event management companies operating in Hong Kong, with pain point analysis and WeExpand AI solution fit mapping. <a href=\"summary.html\" style=\"color:#e94560;font-weight:700;\">→ View Executive Summary &amp; Visualizations</a></p>
        <div class="stat-bar">
            <div class="stat-item">
                <div class="stat-num">{total}</div>
                <div class="stat-label">Companies Researched</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">{high}</div>
                <div class="stat-label">High Fit (7-8/10)</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">{medium}</div>
                <div class="stat-label">Medium Fit</div>
            </div>
            <div class="stat-item">
                <div class="stat-num" style="color: var(--highlight);">{sum(c['pain_points'] for c in companies_data)}</div>
                <div class="stat-label" style="color: var(--highlight);">Total Pain Points</div>
            </div>
        </div>
    </div>
</div>

<main>
<div class="container">

    <div class="filter-bar">
        <input type="text" id="searchInput" placeholder="🔍 Search companies by name..." onkeyup="filterTable()">
        <button class="filter-btn active" onclick="filterByFit('all', this)">All</button>
        <button class="filter-btn" onclick="filterByFit('High', this)">High Fit</button>
        <button class="filter-btn" onclick="filterByFit('Medium', this)">Medium Fit</button>
        <button class="filter-btn" onclick="filterByFit('Low', this)">Low/N/A</button>
    </div>

    <table class="company-table" id="companyTable">
        <thead>
            <tr>
                <th>Company Name</th>
                <th>Employees</th>
                <th>Solution Fit</th>
                <th>Pain Points</th>
            </tr>
        </thead>
        <tbody>
            {company_rows}
        </tbody>
    </table>

</div>
</main>

<footer>
    <div class="container">
        <p>Market Understanding Project · {total} companies researched · Generated 2026-05-29 · <a href=\"summary.html\" style=\"color:#e94560;\">Executive Summary &amp; Visualizations</a></p>
    </div>
</footer>

<script>
function filterTable() {{
    const input = document.getElementById('searchInput');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('companyTable');
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {{
        const td = tr[i].getElementsByTagName('td')[0];
        if (td) {{
            const txtValue = td.textContent || td.innerText;
            tr[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? '' : 'none';
        }}
    }}
}}

function filterByFit(fit, btn) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const table = document.getElementById('companyTable');
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {{
        const td = tr[i].getElementsByTagName('td')[2];
        if (td) {{
            const txtValue = td.textContent || td.innerText;
            if (fit === 'all') {{
                tr[i].style.display = '';
            }} else if (fit === 'Low') {{
                tr[i].style.display = (txtValue.indexOf('High') === -1 && txtValue.indexOf('Medium') === -1) ? '' : 'none';
            }} else {{
                tr[i].style.display = txtValue.indexOf(fit) > -1 ? '' : 'none';
            }}
        }}
    }}
}}
</script>

</body>
</html>"""
    
    with open(WEBSITE_DIR / "index.html", "w") as f:
        f.write(index_html)
    
    print(f"Generated index.html with {total} companies")


def generate_summary_data(companies_data):
    """Generate summary_data.json using the exact same data that powers the HTML pages."""
    import json
    from collections import Counter
    
    pain_categories = {
        "Manual Sales & Client Acquisition": ["sales", "client acquisition", "lead generation", "manual", "network", "referral", "outreach", "business development", "pipeline", "sponsor", "delegate acquisition", "exhibitor sales", "BD"],
        "No Digital Platform": ["digital platform", "no digital", "digital gap", "online", "app", "portal", "self-service", "digital presence", "e-commerce", "digital event", "digital tools", "digital marketing"],
        "Year-Round Engagement Gap": ["year-round", "annual", "biennial", "11-month", "2-year", "between event", "community platform", "365", "episodic", "engagement gap", "dormant", "community monetization"],
        "Team Scalability Crisis": ["small team", "micro", "lean", "scalability", "headcount", "capacity", "growth bottleneck", "cannot scale", "team size", "bandwidth", "stretched", "cannot handle"],
        "No AI & Automation": ["AI", "automation", "manual process", "no AI", "machine learning", "smart", "chatbot", "AI-driven", "AI-powered"],
        "Data Monetization Gap": ["data", "analytics", "insight", "monetiz", "attendee data", "post-event", "CRM", "visitor data", "lead capture"],
        "Competitive Pressure": ["competition", "competitor", "rival", "market share", "disruption", "threat", "encroach", "competitive"],
        "Revenue Model Risk": ["revenue", "project-based", "recurring", "one-off", "cash flow", "margin", "capital intensive", "rental", "predictab"],
        "Geographic Concentration": ["Hong Kong", "single location", "geographic", "regional", "one city", "China-centric", "concentration", "local market", "one venue"],
        "Operational Risk": ["single point of failure", "key person", "dependency", "operational risk", "vulnerab", "continuity", "burnout", "key people"],
        "Policy & Regulatory Dependency": ["policy", "regulation", "government", "compliance", "geopolitical", "trade", "political"],
        "Brand & Marketing Gap": ["brand", "marketing", "visibility", "social media", "credentials", "certification", "reputation", "amplified"],
    }
    
    cat_counts = Counter()
    urgency_counts = Counter()
    emp_groups = {"Micro (1-20)": 0, "Small (21-100)": 0, "Medium (101-500)": 0, "Large (501+)": 0}
    fit_dist = {"High": 0, "Medium": 0, "Low": 0}
    total_pains = 0
    total_emp = 0
    enriched = []
    
    for c in companies_data:
        emp = int(c.get("employees", "0").replace(",", "")) if c.get("employees", "N/A") != "N/A" else 0
        total_emp += emp
        total_pains += c["pain_points"]
        
        if emp <= 20: emp_groups["Micro (1-20)"] += 1
        elif emp <= 100: emp_groups["Small (21-100)"] += 1
        elif emp <= 500: emp_groups["Medium (101-500)"] += 1
        else: emp_groups["Large (501+)"] += 1
        
        fl = c["fit_level"] if c["fit_level"] != "N/A" else "Low"
        if fl in fit_dist:
            fit_dist[fl] += 1
        else:
            fit_dist["Low"] += 1
        
        # Determine company type
        slug = c["slug"]
        if any(kw in slug for kw in ["venue", "hotel", "sports_park", "exhibition_centre", "convention", "asiaworld"]):
            comp_type = "Venue Operator"
        elif any(kw in slug for kw in ["production", "staging", "showtex", "syma", "milton", "exr", "expomobilia", "chunky", "serious"]):
            comp_type = "Event Production/Fabrication"
        elif any(kw in slug for kw in ["1000meetings", "keys", "pyjama"]):
            comp_type = "Platform/Marketplace"
        elif any(kw in slug for kw in ["informa", "rx_global", "clarion", "gl_events", "closerstill", "comasia", "adsale", "messe", "oliver"]):
            comp_type = "Large Exhibition Organizer"
        elif any(kw in slug for kw in ["beacon", "leader", "marintec", "jec", "rethink", "beyond", "token", "superai", "121", "aplf", "branded", "beauty", "infocomm", "mykar"]):
            comp_type = "Conference/Niche Event Organizer"
        elif any(kw in slug for kw in ["eventist", "filament", "teamrite", "noah", "fuel", "artcom"]):
            comp_type = "Creative/Marketing Agency"
        else:
            comp_type = "Event Services"
        
        enriched.append({
            "name": c["name"], "slug": slug, "employees": emp,
            "fit_level": c["fit_level"], "fit_score": int(c.get("fit_score", "0")) if c.get("fit_score", "N/A") != "N/A" else 0,
            "pain_count": c["pain_points"], "type": comp_type
        })
    
    # Tier lists (use exact fit_score from HTML data)
    tier1 = sorted([c for c in enriched if c["fit_score"] >= 8], key=lambda x: -x["fit_score"])
    tier2 = sorted([c for c in enriched if 6 <= c["fit_score"] <= 7], key=lambda x: -x["fit_score"])
    tier3 = sorted([c for c in enriched if c["fit_score"] <= 5], key=lambda x: x["fit_score"])
    
    # For pain categories and urgency, we need the actual pain point text from reports
    # Extract from report files directly using same file-finding logic
    for c in enriched:
        rp = find_file(REPORT_DIR, c["name"], "_report.md")
        if rp.exists():
            with open(rp) as f:
                rtext = f.read()
            # Count urgencies (handle both ### and #### pain point formats)
            for m in re.finditer(r'\*\*Urgency:\*\*\s*(.+?)(?:\s*[—\-–]|\s*\n|\s*\.)', rtext):
                u = m.group(1).strip()
                u = u.replace("🔴", "").replace("🟡", "").replace("🟢", "").strip()
                if "High" in u: urgency_counts["High"] += 1
                elif "Medium" in u: urgency_counts["Medium"] += 1
                elif "Low" in u: urgency_counts["Low"] += 1
            # Categorize pain points (handle #### Pain Point B1: format)
            for m in re.finditer(r'#{3,4}\s*Pain Point\s*[A-Z]?\d*:\s*(.+)', rtext):
                title = m.group(1).lower()
                matched = False
                for cat, keywords in pain_categories.items():
                    if any(kw.lower() in title for kw in keywords):
                        cat_counts[cat] += 1
                        matched = True
                        break
                if not matched:
                    cat_counts["Other"] += 1
    
    # Top pain point companies
    top_pains = sorted([{"company": c["name"], "slug": c["slug"], "count": c["pain_count"], "fit": c["fit_level"]} 
                        for c in enriched], key=lambda x: -x["count"])[:10]
    
    summary = {
        "total_companies": len(companies_data),
        "total_employees": total_emp,
        "total_pain_points": total_pains,
        "avg_pains_per_company": round(total_pains / len(companies_data), 1) if companies_data else 0,
        "fit_distribution": fit_dist,
        "urgency_distribution": dict(urgency_counts.most_common()),
        "pain_categories": dict(cat_counts.most_common()),
        "employee_groups": emp_groups,
        "tier1_prime": tier1,
        "tier2_strong": tier2,
        "tier3_niche": tier3,
        "top_pains": top_pains,
        "companies": enriched
    }
    
    with open(WEBSITE_DIR / "summary_data.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Generated summary_data.json ({len(enriched)} companies, {total_pains} pain points, High: {fit_dist['High']}, Med: {fit_dist['Medium']})")


def main():
    # Read CSV
    companies = []
    csv_path = BASE_DIR / "df_company.csv"
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    
    print(f"Found {len(companies)} companies in CSV")
    
    # Load teammate collaboration data
    teammate_data = {}
    try:
        import json
        with open(WEBSITE_DIR / "merged_data.json") as f:
            md = json.load(f)
        for c in md.get("companies", []):
            teammate_data[c["name"].lower()] = c
    except: pass
    
    # Generate each company page
    results = []
    for i, company in enumerate(companies):
        name = company.get("Company Name", "").strip()
        if not name:
            continue
        
        slug = slugify(name)
        searched_path = find_file(SEARCHED_DIR, name, "_searched.md")
        report_path = find_file(REPORT_DIR, name, "_report.md")
        
        try:
            result = generate_company_html(company, searched_path, report_path, teammate_data.get(name.lower()))
            results.append(result)
            print(f"  [{i+1}/{len(companies)}] Generated: {name}")
        except Exception as e:
            print(f"  [{i+1}/{len(companies)}] ERROR generating {name}: {e}")
            # Add with defaults
            results.append({
                "name": name,
                "employees": company.get("# Employees", "N/A"),
                "fit_level": "N/A",
                "fit_score": "N/A",
                "pain_points": 0,
                "slug": slug
            })
    
    # Generate index
    generate_index(results)
    
    # Generate unified summary data (same source as HTML pages)
    generate_summary_data(results)
    
    print(f"\n✅ Generated {len(results)} company pages + index.html + summary_data.json in {WEBSITE_DIR}")

if __name__ == "__main__":
    main()
