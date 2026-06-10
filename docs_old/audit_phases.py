#!/usr/bin/env python3
"""Audit pain point phase coverage and identify real gaps from research data."""
import os, re

REPORTS_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/reports"
SEARCHED_DIR = "/Users/lok/Project/MarketUnderstanding/outputs/searched"

results = []
for fname in sorted(os.listdir(REPORTS_DIR)):
    if not fname.endswith("_report.md"): continue
    path = os.path.join(REPORTS_DIR, fname)
    with open(path) as f: text = f.read()
    
    before = len(re.findall(r'#### Pain Point B\d+:', text))
    during = len(re.findall(r'#### Pain Point D\d+:', text))
    after = len(re.findall(r'#### Pain Point A\d+:', text))
    
    total = before + during + after
    name = fname.replace("_report.md", "").replace("_", " ").title()
    
    gaps = []
    if before == 0: gaps.append("BEFORE")
    if during == 0: gaps.append("DURING")
    if after == 0: gaps.append("AFTER")
    
    results.append((name, fname, before, during, after, total, gaps))

print(f"{'Company':42s} {'B':>3} {'D':>3} {'A':>3} {'Tot':>3} {'Gaps'}")
print("-" * 75)
no_gaps = 0
gappy = []
for name, fname, b, d, a, t, gaps in results:
    gap_str = ",".join(gaps) if gaps else "✓"
    print(f"{name[:42]:42s} {b:3d} {d:3d} {a:3d} {t:3d} {gap_str}")
    if gaps:
        gappy.append((name, fname, gaps))
    else:
        no_gaps += 1

print(f"\n✓ Complete: {no_gaps}  ✗ Has gaps: {len(gappy)}")
print("\n=== COMPANIES NEEDING EVIDENCE-BASED FILL ===")
for name, fname, gaps in gappy:
    # Check searched file for real data that supports missing phases
    slug = fname.replace("_report.md", "")
    sp = os.path.join(SEARCHED_DIR, f"{slug}_searched.md")
    if not os.path.exists(sp):
        # Try fuzzy find
        for sf in os.listdir(SEARCHED_DIR):
            if slug.split("_")[0] in sf and sf.endswith("_searched.md"):
                sp = os.path.join(SEARCHED_DIR, sf)
                break
    
    data_clues = []
    if os.path.exists(sp):
        with open(sp) as f: stext = f.read()[:2000]
        if "sales" in stext.lower() or "client acquisition" in stext.lower() or "marketing" in stext.lower():
            data_clues.append("BEFORE-clues")
        if "engagement" in stext.lower() or "visitor" in stext.lower() or "lead capture" in stext.lower() or "execution" in stext.lower():
            data_clues.append("DURING-clues")
        if "follow-up" in stext.lower() or "post-event" in stext.lower() or "data" in stext.lower() or "analytics" in stext.lower():
            data_clues.append("AFTER-clues")
    
    print(f"  {name}: missing {gaps} | searched data clues: {data_clues}")
