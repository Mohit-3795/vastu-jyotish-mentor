# Dasha & transits — personal timing

**Compute:** `scripts/kundli.py "<DOB> <HH:MM> <place>" --on <today>` → current Mahadasha/Antardasha, Sade Sati, Manglik. Needs birth **time**; flag confidence if missing.

## Vimshottari Dasha — the planetary "season" you're living in
Each person runs 120 years of planetary periods (**Mahadasha**), sub-divided into **Antardasha**, fixed by the Moon's nakshatra at birth. The lord colours the whole phase:
- **Benefic-lord period** (Jupiter, Venus, Mercury, strong Moon) → favourable; the lord's significations flow.
- **Malefic-lord period** (Saturn, Rahu, Ketu, Mars, weak Sun) → effortful; time carefully, lean on remedies.
- A period of the person's **lagna lord / functional benefic** = a green light for big moves.

**Apply it:** compute each key person with `scripts/kundli.py` and record their current Mahadasha/Antardasha in `profile.md`. Anchor the business's big moves on whoever is running a **benefic / lagna-lord** period.

## Gochara (transits) — Sade Sati & co.
- **Sade Sati** = Saturn in the **12th / 1st / 2nd** from your natal Moon (~7.5 yrs). Tests and matures — *not* doom. Avoid over-leverage; work hard, stay humble; Saturn remedies (Sat seva, Hanuman Chalisa).
- **Ashtama Shani / Dhaiya** = Saturn **8th (or 4th)** from Moon (~2.5 yrs). Watch health/stress; steady, no reckless risk.
- **Jupiter** transiting over/trine your Moon = the opposite, a lift — ride it for expansion.
- **Check each person:** `kundli.py` prints their Sade Sati / Ashtama-Shani status — flag anyone in a heavy Saturn phase ("go steady, don't over-leverage") and note it in `profile.md`.

## How to use
- Big personal move (loan, lease in your name, expansion) → favourable in a benefic dasha + not heavy Sade Sati; else go smaller + remedy.
- Anchor the company's big launches on whoever is in the **best dasha** (usually the principal) — note who, in `profile.md`.
- Dasha/transits *modify* a muhurta — a great day in a rough personal period = "fine, but modest." Say so simply.
