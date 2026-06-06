#!/usr/bin/env python3
"""kundli.py - personal Jyotish timing: Vimshottari dasha, Sade Sati, Manglik.

Usage:
  python3 kundli.py "1985-08-15 09:30 delhi" --on 2026-06-06
  python3 kundli.py "1985-08-15 09:30 delhi" --on 2026-06-06 --lagna Scorpio
Place: agra|delhi or LAT,LON. If no birth time, pass 12:00 and treat Moon/dasha as approximate.
Needs pyephem.
"""
import sys, math
try:
    import ephem
except ImportError:
    sys.exit("Needs pyephem: pip install ephem")

PLACES = {"agra": (27.18, 78.02), "delhi": (28.61, 77.21), "newdelhi": (28.61, 77.21)}
IST = 5.5 / 24.0
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
NAK = ['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha',
 'P.Phalguni','U.Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','P.Ashadha',
 'U.Ashadha','Shravana','Dhanishta','Shatabhisha','P.Bhadrapada','U.Bhadrapada','Revati']
ORDER = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']  # = nakshatra-lord cycle
YEARS = {'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}

def ayan(dt):
    d = ephem.Date(dt).datetime(); y = d.year + d.timetuple().tm_yday/365.25
    return 22.4606 + (y-1900)*0.013925
def eclon(body, dt):
    b = body(); b.compute(ephem.Date(dt)); return math.degrees(ephem.Ecliptic(b).lon) % 360
def sid(body, dt):
    return (eclon(body, dt) - ayan(dt)) % 360

def vimshottari(birth, today):
    ml = sid(ephem.Moon, birth)
    nidx = int(ml // (40/3)); frac = (ml % (40/3)) / (40/3)
    lord = ORDER[nidx % 9]
    seq = [(lord, (1-frac)*YEARS[lord])]
    li = ORDER.index(lord)
    for k in range(1, 18):
        l = ORDER[(li+k) % 9]; seq.append((l, YEARS[l]))
    elapsed = (ephem.Date(today) - ephem.Date(birth)) / 365.25
    t = 0; md = md_yrs = md_start = None
    for (l, yrs) in seq:
        if t + yrs > elapsed: md, md_yrs, md_start = l, yrs, t; break
        t += yrs
    into = elapsed - md_start
    ai = ORDER.index(md); at = 0; ad = None
    for k in range(9):
        sl = ORDER[(ai+k) % 9]; syr = md_yrs * YEARS[sl] / 120
        if at + syr > into: ad = sl; break
        at += syr
    return NAK[nidx], md, ad

def sade_sati(birth, today):
    msign = int(sid(ephem.Moon, birth) // 30)
    ssign = int(sid(ephem.Saturn, today) // 30)
    diff = (ssign - msign) % 12
    where = f"Saturn in {SIGNS[ssign]}, natal Moon in {SIGNS[msign]}"
    if diff == 11: return f"SADE SATI - rising phase (Saturn in 12th from Moon). {where}"
    if diff == 0:  return f"SADE SATI - PEAK (Saturn over natal Moon). {where}"
    if diff == 1:  return f"SADE SATI - setting phase (Saturn in 2nd from Moon). {where}"
    if diff == 3:  return f"Small panoti / Ashtama-adjacent (Saturn 4th from Moon). {where}"
    if diff == 7:  return f"Ashtama Shani (Saturn 8th from Moon) - a 'dhaiya'. {where}"
    return f"No Sade Sati (Saturn {diff+1}th from Moon). {where}"

def manglik(birth, lagna_sign):
    msign = int(sid(ephem.Mars, birth) // 30)
    house = (msign - lagna_sign) % 12 + 1
    bad = {1,2,4,7,8,12}
    return f"Mars in {SIGNS[msign]} = house {house} from lagna -> {'MANGLIK' if house in bad else 'not Manglik'}"

def parse(s):
    parts = s.split(); date = parts[0]; tm = parts[1] if len(parts) > 1 else "12:00"
    place = parts[2].lower() if len(parts) > 2 else "agra"
    y, mo, d = (int(x) for x in date.split('-')); hh, mm = (int(x) for x in tm.split(':'))
    lat, lon = PLACES.get(place, PLACES['agra'])
    return ephem.Date((y, mo, d, hh, mm, 0)) - IST

def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    birth = parse(a[0])
    on = a[a.index('--on')+1] if '--on' in a else '2026-06-06'
    oy, om, od = (int(x) for x in on.split('-')); today = ephem.Date((oy, om, od, 12, 0, 0)) - IST
    nak, md, ad = vimshottari(birth, today)
    print(f"  Moon nakshatra : {nak}")
    print(f"  Vimshottari    : {md} mahadasha / {ad} antardasha   (as of {on})")
    print(f"  Saturn/transit : {sade_sati(birth, today)}")
    if '--lagna' in a:
        lg = a[a.index('--lagna')+1]; print(f"  Manglik check  : {manglik(birth, SIGNS.index(lg))}")

if __name__ == '__main__':
    main()
