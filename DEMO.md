# Demo

Real output from the skill. *Personal birth data is never shown — the chart example uses a fictitious person.*

## 1. "Should we order raw material to start the business now, or wait?"

The mentor checks the **period gate first** — and catches that early June 2026 falls inside **Adhik Maas** (the extra "leap month" when Hindu tradition pauses new beginnings and big purchases). No weekday, however good, rescues a blocked month.

```text
$ python3 scripts/panchang.py 2026-06-06 --place delhi
== Saturday 06 Jun 2026  (Delhi) ==
  GATE  ** ADHIK MAAS **  2026-05-17 -> 2026-06-15  (no new starts / big purchases)
  DAY   Krishna Shashthi | Moon Dhanishta [good star] | Sun Taurus
  YOGA  Ayushman | Karana Gara
  BUY   Mercury direct (ok to buy)
  TIME  sunrise 05:21  sunset 19:18  | Rahu Kaal 08:50-10:35 (avoid)
  ABHJT Abhijit (safe noon window) 11:51-12:47
  CHOG  good day-windows: 07:06-08:50 Shubh, 12:19-14:04 Char, 14:04-15:49 Labh, 15:49-17:33 Amrit
  ==>   NOT ideal - postpone past ADHIK MAAS (2026-05-17 -> 2026-06-15)
```

> **Mentor's reply:** *"Wait — don't order now. We're in Adhik Maas (the extra 'leap month' when new starts pause) until 15 June. Order after that."*

## 2. "What planetary period is the person running? Are they in Sade Sati?"

`kundli.py` computes **Vimshottari dasha** and **Sade Sati** from a birth chart:

```text
$ python3 scripts/kundli.py "1985-08-15 09:30 delhi" --on 2026-06-06 --lagna Scorpio
  Moon nakshatra : Pushya
  Vimshottari    : Venus mahadasha / Jupiter antardasha   (as of 2026-06-06)
  Saturn/transit : No Sade Sati (Saturn 9th from Moon). Saturn in Pisces, natal Moon in Cancer
  Manglik check  : Mars in Cancer = house 9 from lagna -> not Manglik
```

> **Mentor's reply:** *"You're in a Venus–Jupiter period — favourable and growth-friendly — and not in Sade Sati. A good window to expand."*

## The point

All the astronomy and rule-checking happens **inside the engine**. The mentor replies in plain language — a one-line verdict, two or three reasons, the next step. Depth under the hood; simplicity on the surface.
