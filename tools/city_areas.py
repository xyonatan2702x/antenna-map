# -*- coding: utf-8 -*-
"""Per-city unique analysis for larger cities (22.11.2026):
- which network has the most sites in each part of the city (center / north / south / east / west)
- the street names with the most sites in each part
- for each network, the spot in the city (among site locations) farthest from that network's nearest site
Everything is computed from antennas-data.js only."""
import math, re, collections, html as _h
import numpy as np

MIN_SITES_AREAS = 12
ZONE_MIN = 4

def _xy(lat, lon, clat):
    return (lon * 111.32 * math.cos(math.radians(clat)), lat * 110.57)

def street(addr):
    s = (addr or '').replace('`', "'").strip()
    s = re.sub(r"^(רח'|רח |רחוב |רח\.)\s*", '', s)
    s = re.sub(r"^שד'\s*", 'שדרות ', s)
    s = re.sub(r'^(בסמוך ל|סמוך ל|ליד )', '', s)
    s = re.sub(r"\s(פ'|פינת)\s.*$", '', s)
    s = re.split(r'\d', s)[0]
    s = re.sub(r'[\s\-,.;:"]+$', '', s).strip()
    s = re.sub(r'\s+', ' ', s)
    if len(s) < 3 or len(s.split()) > 3: return ''
    if re.search(r'חח"י|חח\'י|עמוד|ארוב|תורן|מגדל מים|מתקן|גג |בריכת|מס\'$', s): return ''
    return s

class Nearest:
    """Distance (km) from a point to the nearest site of a network, using numpy over all sites."""
    def __init__(self, data, order):
        self.pts, self.rows = {}, {}
        for k in order:
            self.rows[k] = [r for r in data if r[2] == k]
            self.pts[k] = np.array([(r[0], r[1]) for r in self.rows[k]], dtype=float)
    def _d(self, k, lat, lon):
        a = self.pts[k]
        dy = (a[:, 0] - lat) * 110.57
        dx = (a[:, 1] - lon) * 111.32 * math.cos(math.radians(lat))
        return np.sqrt(dx * dx + dy * dy)
    def dist(self, k, lat, lon):
        return float(self._d(k, lat, lon).min())
    def nearest(self, k, lat, lon):
        d = self._d(k, lat, lon); i = int(d.argmin())
        return float(d[i]), self.rows[k][i]

def fmt_dist(km):
    if km < 0.1: return 'פחות מ-100 מ\''
    if km < 1: return f'כ-{int(round(km * 1000 / 50.0) * 50):,} מ\''
    return f'כ-{km:.1f} ק"מ'

def nearest_section(c, near, order, co, clean_name, key_of=None):
    """For every locality: distance from its center to the nearest site of each network."""
    name = c['name']
    lat, lon = c['center']
    res = []
    for k in order:
        d, r = near.nearest(k, lat, lon)
        where = _h.escape((r[3].strip() or clean_name(r[4])).replace('`', "'"))
        town = clean_name(r[4])
        same = (key_of(r[4]) == c['key']) if key_of else (town == name)
        place = where if same or not town else f'{where}, {_h.escape(town)}'
        g = ' '.join(sorted(set(re.findall(r'\d', r[5] or ''))))
        res.append((d, k, place, g))
    res.sort()
    items = ''.join(f'<li><strong>{co[k]}</strong>: {fmt_dist(d)} ({place}{", דור " + g.replace(" ", "/") if g else ""})</li>' for d, k, place, g in res)
    closest = res[0]
    gap = res[-1][0] - res[0][0]
    if gap < 0.15:
        summ = f'לכל שלוש הרשתות יש אתר שידור במרחק דומה ממרכז {name}.'
    else:
        near_ks = [k for d, k, _, _ in res if d - closest[0] < 0.05]
        if len(near_ks) == 1:
            summ = f'הרשת עם אתר השידור הקרוב ביותר למרכז {name} היא {co[near_ks[0]]}, והרחוקה היא {co[res[-1][1]]}.'
        else:
            summ = f'ל{co[near_ks[0]]} ול{co[near_ks[1]]} יש אתר שידור קרוב למרכז {name} במרחק דומה, ול{co[res[-1][1]]} האתר הקרוב רחוק יותר.'
    return (f'<h2>כמה רחוק אתר השידור הקרוב ב{name}?</h2>\n'
            f'  <p>{summ} המרחק מחושב בקו אווירי ממרכז היישוב לאתר הקרוב של כל רשת, גם אם הוא מחוץ ליישוב:</p>\n'
            f'  <ul class="areas">{items}</ul>\n'), (f'איזו רשת הכי קרובה ל{name}?', re.sub(r'<[^>]+>', '', summ + ' ' + '; '.join(f'{co[k]} {fmt_dist(d)}' for d, k, _, _ in res) + '.'))

ZONE_NAME = {'center': 'במרכז העיר', 'north': 'בצפון העיר', 'south': 'בדרום העיר', 'east': 'במזרח העיר', 'west': 'במערב העיר'}
ZONE_ORDER = ['center', 'north', 'south', 'east', 'west']

def zones(c):
    clat, clon = c['center']
    cx, cy = _xy(clat, clon, clat)
    pos = []
    for r in c['rows']:
        x, y = _xy(r[0], r[1], clat)
        pos.append((x - cx, y - cy, r))
    dists = sorted(math.hypot(x, y) for x, y, _ in pos)
    r_center = dists[len(dists) // 3]  # inner third of the sites = center
    out = collections.defaultdict(list)
    for x, y, r in pos:
        if math.hypot(x, y) <= r_center:
            z = 'center'
        else:
            a = math.degrees(math.atan2(y, x))  # 0 = east, 90 = north
            z = 'north' if 45 <= a < 135 else 'west' if a >= 135 or a < -135 else 'south' if -135 <= a < -45 else 'east'
        out[z].append(r)
    return out

def analyse(c, near, order, co, co_short):
    """Returns (html, faq_list) or ('', []) for small cities."""
    if len(c['rows']) < MIN_SITES_AREAS: return '', []
    name = c['name']
    zs = zones(c)
    items, faq_bits = [], []
    for z in ZONE_ORDER:
        rows = zs.get(z, [])
        if len(rows) < ZONE_MIN: continue
        cnt = {k: sum(r[2] == k for r in rows) for k in order}
        ranked = sorted(order, key=lambda k: -cnt[k])
        leaders = [ranked[0]] if cnt[ranked[0]] - cnt[ranked[1]] >= max(2, 0.05 * len(rows)) else ranked
        sts = collections.Counter(s for s in (street(r[3]) for r in rows) if s)
        st_txt = ', '.join(s for s, _ in sts.most_common(3))
        st_txt = _h.escape(st_txt)
        counts = ', '.join(f'{co_short[k]} {cnt[k]}' for k in order)
        if len(leaders) == 1:
            lead = f'<strong>{co[leaders[0]]}</strong> מובילה'
            faq_bits.append(f'{ZONE_NAME[z]} מובילה {co[leaders[0]]}')
        else:
            lead = 'הרשתות קרובות, בלי רשת בולטת'
        items.append(f'<li><strong>{ZONE_NAME[z]}</strong> ({len(rows)} אתרים{", באזור " + st_txt if st_txt else ""}): {lead}. {counts}.</li>')
    # sparsest spot per network
    weak = []
    for k in order:
        best = None
        clat, clon = c['center']
        dc = sorted(math.hypot(*[a - b for a, b in zip(_xy(r[0], r[1], clat), _xy(clat, clon, clat))]) for r in c['rows'])
        lim = dc[int(len(dc) * 0.8)]  # skip the outer 20% (outskirts, highways, industrial edges)
        for r in c['rows']:
            if math.hypot(*[a - b for a, b in zip(_xy(r[0], r[1], clat), _xy(clat, clon, clat))]) > lim: continue
            if r[2] == k or not street(r[3]): continue
            d = near.dist(k, r[0], r[1])
            if best is None or d > best[0]: best = (d, r)
        if best is None: continue
        d, r = best
        m = int(round(d * 1000 / 50.0) * 50)
        s = _h.escape(street(r[3]))
        if m >= 400 and s:
            weak.append(f'<li><strong>{co[k]}</strong>: הכיסוי הדליל ביותר שלה בעיר הוא באזור {s}. אתר השידור הקרוב שלה נמצא כ-{m:,} מ\' משם.</li>')
        elif m < 400:
            weak.append(f'<li><strong>{co[k]}</strong>: בכל מיקומי אתרי השידור בעיר, יש אתר של {co_short[k]} במרחק של עד כ-{max(m, 50):,} מ\'.</li>')
    if not items and not weak: return '', []
    out = f'<h2>הקליטה לפי אזורים ב{name}</h2>\n  <p>חילקנו את אתרי השידור ב{name} לפי האזור בעיר. כך רואים שהרשת שמובילה בעיר כולה לא בהכרח מובילה בשכונה שלכם.</p>\n'
    if items: out += f'  <ul class="areas">{"".join(items)}</ul>\n'
    if weak:
        out += f'  <h3>איפה כל רשת דלילה יותר</h3>\n  <ul class="areas">{"".join(weak)}</ul>\n'
    out += '  <p class="note">החלוקה לאזורים היא לפי מיקום האתרים ביחס למרכז היישוב, והמרחקים מחושבים בקו אווירי. גרים באזור דליל? כדאי לבדוק את הכתובת המדויקת במפה.</p>\n'
    faq = []
    if len(faq_bits) >= 2:
        faq.append((f'האם אותה חברת סלולר הכי טובה בכל {name}?',
                    f'לא בהכרח. לפי מספר אתרי השידור בכל אזור: ' + '; '.join(faq_bits) + '. לכן כדאי לבדוק את הכתובת המדויקת.'))
    return out, faq
