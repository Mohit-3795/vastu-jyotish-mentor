#!/usr/bin/env python3
"""panchang.py - period GATES + day panchang for the vastu-jyotish-mentor.

Checks, in the order a muhurta must:
  0) PERIOD GATES (month-level): Adhik Maas, Kharmas/Malmas  -> block new starts/big buys
  1) DAY: weekday, tithi+paksha (Rikta?), nakshatra, Moon/Sun rashi
  2) TIME: sunrise/sunset, Rahu Kaal window
  3) BUY: Mercury retrograde (purchases/contracts)
  + eclipse-near-syzygy warning.

Usage:
  python3 panchang.py 2026-06-19
  python3 panchang.py 2026-06-19 --place delhi --time 10:30
  python3 panchang.py 2026-06-06 --scan 40        # gate status for the next 40 days

Needs pyephem:  pip install ephem   (else verify on https://www.drikpanchang.com)
"""
import sys, math, datetime
try:
    import ephem
except ImportError:
    sys.exit("Needs pyephem:  pip install ephem   (or verify on https://www.drikpanchang.com)")

PLACES = {"agra": (27.18, 78.02), "delhi": (28.61, 77.21), "newdelhi": (28.61, 77.21)}
IST = 5.5 / 24.0
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
NAK = ['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha',
 'P.Phalguni','U.Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','P.Ashadha',
 'U.Ashadha','Shravana','Dhanishta','Shatabhisha','P.Bhadrapada','U.Bhadrapada','Revati']
TITHI = ['Pratipada','Dwitiya','Tritiya','Chaturthi','Panchami','Shashthi','Saptami','Ashtami','Navami',
 'Dashami','Ekadashi','Dwadashi','Trayodashi','Chaturdashi','Purnima']
GOOD_NAK = {'Ashwini','Rohini','Mrigashira','Punarvasu','Pushya','Hasta','Chitra','Swati','Anuradha',
            'U.Phalguni','U.Ashadha','U.Bhadrapada','Shravana','Dhanishta','Revati'}
RAHU_SEG = {0:2, 1:7, 2:5, 3:6, 4:4, 5:3, 6:8}  # python weekday Mon=0..Sun=6 -> segment (1..8) from sunrise

def ayan(dt):
    d = ephem.Date(dt).datetime()
    y = d.year + d.timetuple().tm_yday / 365.25
    return 22.4606 + (y - 1900) * 0.013925

def eclon(body, dt):
    b = body(); b.compute(ephem.Date(dt)); return math.degrees(ephem.Ecliptic(b).lon) % 360

def moon_lat(dt):
    m = ephem.Moon(); m.compute(ephem.Date(dt)); return math.degrees(ephem.Ecliptic(m).lat)

def utc(y, mo, d, hh, mm):
    return ephem.Date((y, mo, d, hh, mm, 0)) - IST

def sun_sign(dt):
    return int(((eclon(ephem.Sun, dt) - ayan(dt)) % 360) // 30)

def ist_str(dt, fmt='%Y-%m-%d'):
    return ephem.Date(ephem.Date(dt) + IST).datetime().strftime(fmt)

def _events(d0, d1):
    nms, sks = [], []
    t = ephem.Date(d0); pE = pS = None
    while t < d1:
        sl = eclon(ephem.Sun, t); ml = eclon(ephem.Moon, t)
        E = (ml - sl) % 360
        if pE is not None and pE > 350 and E < 10: nms.append(ephem.Date(t))
        s = int(((sl - ayan(t)) % 360) // 30)
        if pS is not None and s != pS: sks.append(ephem.Date(t))
        pE, pS = E, s
        t = ephem.Date(t + ephem.hour)
    return nms, sks

def adhik_maas(dt):
    """Return (is_adhik, (start,end)) for the amanta lunar month containing dt."""
    nms, sks = _events(ephem.Date(dt) - 45, ephem.Date(dt) + 45)
    for i in range(len(nms) - 1):
        if nms[i] <= ephem.Date(dt) < nms[i + 1]:
            inside = [s for s in sks if nms[i] <= s < nms[i + 1]]
            return (len(inside) == 0, (nms[i], nms[i + 1]))
    return (False, None)

def merc_retro(dt):
    a = eclon(ephem.Mercury, ephem.Date(dt) - 0.5)
    b = eclon(ephem.Mercury, ephem.Date(dt) + 0.5)
    return (((b - a + 540) % 360) - 180) < 0

YOGAS = ['Vishkambha','Priti','Ayushman','Saubhagya','Shobhana','Atiganda','Sukarma','Dhriti','Shula',
 'Ganda','Vriddhi','Dhruva','Vyaghata','Harshana','Vajra','Siddhi','Vyatipata','Variyana','Parigha',
 'Shiva','Siddha','Sadhya','Shubha','Shukla','Brahma','Indra','Vaidhriti']
BAD_YOGA = {'Vishkambha','Atiganda','Shula','Ganda','Vyaghata','Vajra','Vyatipata','Parigha','Vaidhriti'}
MOVABLE_KARANA = ['Bava','Balava','Kaulava','Taitila','Gara','Vanija','Vishti']
GOOD_CHOG = {'Amrit','Shubh','Labh','Char'}
CHOG_SEQ = {  # python weekday Mon=0..Sun=6 -> 8 daytime choghadiya from sunrise
 6:['Udveg','Char','Labh','Amrit','Kaal','Shubh','Rog','Udveg'],
 0:['Amrit','Kaal','Shubh','Rog','Udveg','Char','Labh','Amrit'],
 1:['Rog','Udveg','Char','Labh','Amrit','Kaal','Shubh','Rog'],
 2:['Labh','Amrit','Kaal','Shubh','Rog','Udveg','Char','Labh'],
 3:['Shubh','Rog','Udveg','Char','Labh','Amrit','Kaal','Shubh'],
 4:['Char','Labh','Amrit','Kaal','Shubh','Rog','Udveg','Char'],
 5:['Kaal','Shubh','Rog','Udveg','Char','Labh','Amrit','Kaal']}

def yoga_karana(dt):
    sl = eclon(ephem.Sun, dt); ml = eclon(ephem.Moon, dt)
    yoga = YOGAS[int(((sl + ml) % 360) / (360 / 27))]
    ki = int(((ml - sl) % 360) / 6)
    kar = 'Kimstughna' if ki == 0 else (MOVABLE_KARANA[(ki - 1) % 7] if ki <= 56 else ['Shakuni','Chatushpada','Naga'][ki - 57])
    return yoga, kar

def day_facts(dt):
    sl = eclon(ephem.Sun, dt); ml = eclon(ephem.Moon, dt)
    E = (ml - sl) % 360; tn = int(E // 12) + 1
    paksha = 'Shukla' if tn <= 15 else 'Krishna'; tin = ((tn - 1) % 15) + 1
    tname = 'Amavasya' if tn == 30 else ('Purnima' if tn == 15 else TITHI[tin - 1])
    nk = NAK[int(((ml - ayan(dt)) % 360) // (40 / 3))]
    return paksha, tname, tin, nk, E

def report(y, mo, d, place, hh, mm):
    lat, lon = PLACES.get(place, PLACES['agra'])
    noon = utc(y, mo, d, 12, 0); at = utc(y, mo, d, hh, mm)
    wd = datetime.date(y, mo, d).weekday()
    print(f"== {datetime.date(y,mo,d).strftime('%A %d %b %Y')}  ({place.title()}) ==")
    blocked = []
    isad, win = adhik_maas(noon)
    if isad:
        blocked.append(f"ADHIK MAAS ({ist_str(win[0])} -> {ist_str(win[1])})")
        print(f"  GATE  ** ADHIK MAAS **  {ist_str(win[0])} -> {ist_str(win[1])}  (no new starts / big purchases)")
    ss = sun_sign(noon)
    if ss in (8, 11):
        blocked.append("KHARMAS")
        print(f"  GATE  ** KHARMAS/MALMAS ** (Sun in {SIGNS[ss]}) - avoid auspicious starts")
    if not blocked:
        print("  GATE  clear (no Adhik Maas / Kharmas)")
    paksha, tname, tin, nk, E = day_facts(at)
    rikta = ' (RIKTA)' if tin in (4, 9, 14) else ''
    star = ' [good star]' if nk in GOOD_NAK else (' [weak star for starts]' if nk in ('Bharani','Krittika','Ashlesha','Jyeshtha','Mula') else '')
    print(f"  DAY   {paksha} {tname}{rikta} | Moon {nk}{star} | Sun {SIGNS[ss]}")
    yoga, kar = yoga_karana(at)
    print(f"  YOGA  {yoga}{' (inauspicious)' if yoga in BAD_YOGA else ''} | Karana {kar}{' - BHADRA/Vishti, avoid starts' if kar == 'Vishti' else ''}")
    print(f"  BUY   Mercury {'RETROGRADE - avoid buying/contracts' if merc_retro(noon) else 'direct (ok to buy)'}")
    try:
        obs = ephem.Observer(); obs.lat = str(lat); obs.lon = str(lon)
        obs.date = utc(y, mo, d, 0, 1); obs.pressure = 0; obs.horizon = '-0:50'
        sr = obs.next_rising(ephem.Sun()); st = obs.next_setting(ephem.Sun(), start=sr)
        seg = (st - sr) / 8.0; r0 = ephem.Date(sr + (RAHU_SEG[wd]-1)*seg); r1 = ephem.Date(sr + RAHU_SEG[wd]*seg)
        print(f"  TIME  sunrise {ist_str(sr,'%H:%M')}  sunset {ist_str(st,'%H:%M')}  | Rahu Kaal {ist_str(r0,'%H:%M')}-{ist_str(r1,'%H:%M')} (avoid)")
        mu = (st - sr) / 15.0
        print(f"  ABHJT Abhijit (safe noon window) {ist_str(ephem.Date(sr+7*mu),'%H:%M')}-{ist_str(ephem.Date(sr+8*mu),'%H:%M')}{' (skip on Wed)' if wd == 2 else ''}")
        chs = (st - sr) / 8.0
        goodc = [f"{ist_str(ephem.Date(sr+i*chs),'%H:%M')}-{ist_str(ephem.Date(sr+(i+1)*chs),'%H:%M')} {nm}" for i, nm in enumerate(CHOG_SEQ[wd]) if nm in GOOD_CHOG]
        print("  CHOG  good day-windows: " + ", ".join(goodc))
    except Exception:
        print("  TIME  (sunrise/sunset unavailable)")
    if (E < 6 or E > 354 or abs(E - 180) < 6) and abs(moon_lat(noon)) < 1.5:
        print("  WARN  near new/full moon with Moon close to a node -> possible ECLIPSE; verify (avoid + sutak)")
    ok = (not blocked) and (tin not in (4, 9, 14)) and (paksha == 'Shukla') and not merc_retro(noon)
    print(f"  ==>   {'GOOD window for a new start/purchase' if ok else 'NOT ideal - ' + ('postpone past ' + blocked[0] if blocked else 'pick a stronger day (see DAY line)')}")

def scan(y, mo, d, n):
    base = datetime.date(y, mo, d)
    print(f"Next {n} days from {base}:  (< = clean Shukla day, good star, no gate)")
    for i in range(n):
        dd = base + datetime.timedelta(days=i)
        noon = utc(dd.year, dd.month, dd.day, 12, 0)
        isad, _ = adhik_maas(noon); ss = sun_sign(noon)
        gate = 'ADHIK' if isad else ('KHARMAS' if ss in (8, 11) else 'clear')
        paksha, tname, tin, nk, _ = day_facts(utc(dd.year, dd.month, dd.day, 10, 30))
        clean = gate == 'clear' and paksha == 'Shukla' and tin not in (4, 9, 14) and nk in GOOD_NAK
        print(f"  {dd.strftime('%a %d %b')}  {gate:7s} {paksha[0]}-{tname:11s} {nk:13s}{'  <' if clean else ''}")

def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    y, mo, d = (int(x) for x in a[0].split('-'))
    place = a[a.index('--place') + 1].lower() if '--place' in a else 'agra'
    hh, mm = (int(x) for x in a[a.index('--time') + 1].split(':')) if '--time' in a else (10, 30)
    if '--scan' in a:
        scan(y, mo, d, int(a[a.index('--scan') + 1]))
    else:
        report(y, mo, d, place, hh, mm)

if __name__ == '__main__':
    main()
