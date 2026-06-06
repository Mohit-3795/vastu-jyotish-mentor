# 🪔 Vastu–Jyotish Mentor

> A **"digital pandit"** skill for [Claude Code](https://claude.com/claude-code) — judge whether a decision is auspicious, pick an auspicious time (*muhurta*), check Vastu, numerology, and planetary periods, and get a remedy (*upaya*) when something's off. In plain language, backed by real astronomy.

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) &nbsp;![Built with Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-d97757) &nbsp;![Engine: pyephem](https://img.shields.io/badge/engine-pyephem-blue)

Ask it like you'd ask a family pandit — *"good day to launch?"*, *"vastu for my factory?"*, *"am I in Sade Sati?"*, *"is this brand name lucky?"* — and it answers simply, with the heavy reasoning kept under the hood.

## Why it's more than a prompt

Most "astrology bots" hallucinate planetary positions. This one **computes them**, and checks what a real pandit checks **in the right order**:

- 🚦 **Gate-first logic** — it checks the *period* before the day: **Adhik Maas, Kharmas, eclipses, Pitru Paksha**. A blocked month overrides any good weekday. *(It once caught its own Adhik-Maas miss — see [DEMO.md](DEMO.md).)*
- 🔭 **Real ephemeris** — `panchang.py` + `kundli.py` use [pyephem](https://rhodesmill.org/pyephem/) (Lahiri sidereal) for tithi, nakshatra, **yoga, karana, Choghadiya, Abhijit, Rahu Kaal**, Mercury retrograde, **Vimshottari dasha**, and **Sade Sati** — no guessing.
- 🗣️ **Mentor, not textbook** — a one-line verdict + two or three plain reasons. The depth lives in the engine, not the answer.
- 🔒 **Generic engine, private profile** — all knowledge is reusable; personal birth data lives only in a **git-ignored `profile.md`**, and new users are **onboarded automatically**.

## See it work
→ **[DEMO.md](DEMO.md)** — real output: gate-checking a date, and computing a chart.

## What it covers
| Lens | Examples |
|---|---|
| **Muhurta (timing)** | launch / register / buy / install dates; green-light festival days |
| **Jyotish** | dasha & transits (Sade Sati), the principal's benefics, doshas |
| **Vastu** | office / factory / desk / entrance / plot; dosha fixes |
| **Numerology** | brand & personal names, lucky numbers, Lo Shu grid |
| **Ceremonies** | Bhumi Pujan, Vishwakarma / Ayudha Puja, Griha Pravesh |
| **Compatibility** | partner / key-hire chart matching (Guna Milan) |
| **Remedies (upaya)** | the cheapest effective fix when something's off |
| **Logo / brand** | a chart-aligned visual brief |

## Install
```bash
# 1. Clone into your Claude Code skills folder
git clone https://github.com/Mohit-3795/vastu-jyotish-mentor \
  ~/.claude/skills/vastu-jyotish-mentor

# 2. Install the compute engine
pip install ephem
```
Restart Claude Code. The skill auto-triggers on relevant questions, or call `/vastu-jyotish-mentor`.

## First run (onboarding)
On first use it asks for the principal's **birth date / time / place** and **business details**, computes the charts, and writes a private `profile.md` from [`profile.example.md`](profile.example.md). After that, every answer is personalised — and the data never leaves the user's machine.

## How it works
```
SKILL.md            # the mentor's logic, routing & answer style
profile.md          # YOUR private context  (git-ignored; created on first run)
profile.example.md  # the blank template
references/         # the knowledge — jyotish, vastu, numerology, muhurta,
                    #   calendar-gates, dasha-transits, ceremonies, doshas, …
scripts/
  panchang.py       # a date   -> gates + full panchang + timing
  kundli.py         # a person -> dasha, Sade Sati, Manglik
```
`SKILL.md` is a router: it loads your `profile.md`, runs the relevant references + scripts **internally**, and replies with one synthesised, plain-language answer.

## Honest framing
Vastu, Jyotish, and numerology are **traditional systems**, offered here as a consistent, transparent **decision lens** — not a scientific guarantee. For marriage-matching, gemstone prescriptions, or a serious dosha, consult a human pandit. The skill says so itself.

## Built with
[Claude Code](https://claude.com/claude-code) · authored by **Mohit Manchanda**

## License
[MIT](LICENSE) © 2026 Mohit Manchanda
