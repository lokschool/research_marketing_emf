#!/usr/bin/env python3
"""Update searched files with web-sourced event data, then regenerate website."""
import os

# ===== KAI TAK SPORTS PARK =====
with open("outputs/searched/kai_tak_searched.md") as f: text = f.read()
events = """
### Web-Searched Verified Event Records

- **Kai Tak Sports Park Grand Opening** — March 1, 2025 — CE John Lee presided; cultural performances; HK$30B venue
- **World Snooker Grand Prix** — March 4-9, 2025 — Kai Tak Stadium; first major sporting event
- **Hong Kong Sevens** — March 28-30, 2025 — Kai Tak Stadium; centenary airport tribute flyover by Cathay Pacific
- **Mayday 25th Anniversary Concert** — 2025 — Kai Tak Stadium; Taiwanese rock band milestone
- **G.E.M. "I AM GLORIA" World Tour 2.0** — 2025 — Kai Tak Stadium
- **MAMA 2025 (Mnet Asian Music Awards)** — November 28-29, 2025 — Kai Tak Stadium; 7th time in HK, first at Kai Tak, record audience
- **Stefanie Sun Concert** — Upcoming — Kai Tak Stadium
- **15th National Games of China** — KTSP designated as Hong Kong's main competition venue
- **Asian Coffee Music Festival** — Upcoming — community/F&B event
- **Kai Tak Arts Week** — Upcoming — cultural programming
- **90+ international and local events** hosted since opening; 7 million+ cumulative visitors; global top ticket sales ranking

Sources: [China Daily Asia](https://www.chinadailyasia.com/article/605830), [People's Daily](http://en.people.cn/n3/2025/0303/c90000-20283377.html), [Sohu](https://www.sohu.com/a/874004293_122342248), [Gov HK Press](https://www.info.gov.hk/gia/general/202503/01/P2025030100512.htm), [HKTB](https://www.discoverhongkong.com)
"""
text = text.replace("## 3. Events Conducted (with Details)", "## 3. Events Conducted (with Details)\n\n" + events)
with open("outputs/searched/kai_tak_searched.md", "w") as f: f.write(text)
print("✓ Kai Tak Sports Park updated")

# ===== INFORMA MARKETS =====
with open("outputs/searched/informa_markets_searched.md") as f: text2 = f.read()
events2 = """
### Web-Searched Verified Event Records

- **Jewellery & Gem ASIA Hong Kong (JGA)** — June 18-21, 2026 — HKCEC; 70,000 sqm; 1,390 exhibitors; 58,000+ visitors from 140+ countries
- **Jewellery & Gem WORLD Hong Kong** — September 16-20, 2026 — HKCEC + AsiaWorld-Expo; world's largest jewellery trade fair; annual event
- **Hong Kong International Jewellery Show (HKTDC)** — Annual — HKCEC; 140 countries; 37,000+ buyers; 2,870 exhibitors from 46 countries
- **Cosmoprof CBE ASEAN Bangkok** — June 25-27, 2025 — Bangkok QSNCC; joint Informa Markets + BolognaFiere; ASEAN's largest beauty trade show
- **Bangkok Jewelry & Gem Fair** — Annual — 12,000+ exhibitors globally; supports Thailand's 5000B THB jewellery industry
- **JMA Hong Kong International Jewelry Show** — November annually — HKCEC
- **INTERFILIÈRE SHANGHAI** — Annual — Shanghai; intimate apparel, swimwear, sportswear sourcing

Sources: [Jufair](https://www.jufair.com/exhibition/96.html), [Showguide](https://www.showguide.cn/z/20105089549.html), [Sohu Cosmoprof](https://www.sohu.com/a/857320264_121840436), [Sohu Bangkok Jewelry](https://www.sohu.com/a/824020860_362225), [JewelryShows](https://www.jewelryshows.org)
"""
text2 = text2.replace("## 3. Events Conducted", "## 3. Events Conducted (with Details)\n\n" + events2)
with open("outputs/searched/informa_markets_searched.md", "w") as f: f.write(text2)
print("✓ Informa Markets updated")

print("\nNow regenerate...")
