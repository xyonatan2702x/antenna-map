#!/usr/bin/env python3
"""Builds a page per city from antennas-data.js.

Run from the repo root:  python3 tools/build_cities.py
Outputs: city/<slug>.html, city/index.html, sitemap.xml
Change BASE_URL when the site moves to its own domain, then run again.
"""
import json, re, math, html, collections, datetime, os, shutil
from urllib.parse import quote

BASE_URL = 'https://xyonatan2702x.github.io/antenna-map/'
MIN_SITES = 3            # a city gets a page only with at least this many sites
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
CO = {'partner': 'פרטנר והוט מובייל', 'pelephone': 'פלאפון', 'cellcom': 'סלקום'}
CO_SHORT = {'partner': 'פרטנר', 'pelephone': 'פלאפון', 'cellcom': 'סלקום'}
ORDER = ['partner', 'pelephone', 'cellcom']
ALIASES = {'תלאביביפו': 'תלאביב'}   # normalized key -> normalized key

def load():
    t = open(os.path.join(ROOT, 'antennas-data.js'), encoding='utf8').read()
    updated = re.search(r'עודכן: (\d+/\d+)', t)
    i = t.index('const ANTENNAS_DATA')
    return json.loads(t[t.index('[', i):t.rindex(']') + 1]), (updated.group(1) if updated else '')

def clean_name(s):
    s = s.replace('``', '"').replace('`', "'")
    return re.sub(r'\s+', ' ', s.replace(' -', '-').replace('- ', '-')).strip()

def key_of(s):
    k = re.sub(r'[\s\-־\'"`]', '', s).replace('קריית', 'קרית')
    return ALIASES.get(k, k)

def slug_of(name):
    s = re.sub(r'[\'"`()]', '', name)
    return re.sub(r'[\s־]+', '-', s).strip('-')

def gens(tech):
    return sorted(set(re.findall(r'[2-5]', tech)))

def dist_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))

def median(v):
    v = sorted(v); return v[len(v) // 2]

E = html.escape

def group(data):
    groups = collections.defaultdict(list)
    for r in data:
        if r[4].strip(): groups[key_of(r[4])].append(r)
    cities = []
    for k, rows in groups.items():
        names = collections.Counter(clean_name(r[4]) for r in rows)
        # most common spelling; on a tie prefer the one with separators (not a glued-together variant)
        name = sorted(names.items(), key=lambda kv: (-kv[1], -len(kv[0])))[0][0]
        if ' ' not in name and '-' not in name:
            spaced = [n for n in names if ' ' in n or '-' in n]
            if spaced: name = sorted(spaced, key=lambda n: -names[n])[0]
        center = (median([r[0] for r in rows]), median([r[1] for r in rows]))
        cities.append({'key': k, 'name': name, 'slug': slug_of(name), 'rows': rows, 'center': center})
    return cities

def stats(c):
    by = {k: [r for r in c['rows'] if r[2] == k] for k in ORDER}
    return {k: {'n': len(v), 'g5': sum('5' in gens(r[5]) for r in v), 'g4': sum('4' in gens(r[5]) for r in v)} for k, v in by.items()}

def plural_sites(n):
    return 'אתר שידור אחד' if n == 1 else f'{n} אתרי שידור'

def page(c, cities_by_key, all_data, pages, updated):
    name, st, n = c['name'], stats(c), len(c['rows'])
    g5_total = sum(st[k]['g5'] for k in ORDER)
    present = [k for k in ORDER if st[k]['n']]
    missing = [k for k in ORDER if not st[k]['n']]
    top_n = max(st[k]['n'] for k in ORDER)
    leaders = [k for k in ORDER if st[k]['n'] == top_n]
    url = BASE_URL + 'city/' + quote(c['slug']) + '.html'
    title = f'אנטנות סלולריות ב{name} — קליטה של פרטנר, סלקום ופלאפון'
    counts_txt = ', '.join(f'{CO_SHORT[k]} {st[k]["n"]}' for k in ORDER)
    desc = f'ב{name} פועלים {plural_sites(n)} סלולריים: {counts_txt}. מפה, רשימת כתובות ודור 5 לפי חברה, מנתוני המשרד להגנת הסביבה.'
    # summary sentences
    if len(leaders) == 1:
        lead_txt = f'לחברת {CO[leaders[0]]} יש הכי הרבה אתרי שידור ב{name} ({top_n}).'
    else:
        lead_txt = f'{" ו".join(CO[k] for k in leaders)} מובילות ב{name} עם {top_n} אתרי שידור כל אחת.'
    if g5_total:
        g5_txt = f'ב-{g5_total} מתוך {n} האתרים משודר גם דור 5: ' + ', '.join(f'{CO_SHORT[k]} {st[k]["g5"]}' for k in present) + '.'
    else:
        g5_txt = f'לפי הנתונים, באף אחד מהאתרים ב{name} לא משודר כרגע דור 5.'
    # carriers with no site in the city: nearest site elsewhere
    miss_html = ''
    for k in missing:
        best = min((r for r in all_data if r[2] == k), key=lambda r: dist_km(c['center'], r))
        d = dist_km(c['center'], best)
        miss_html += f'<li>ל{CO[k]} אין אתר שידור בתוך {E(name)}. האתר הקרוב ביותר שלה נמצא ב{E(clean_name(best[4]))} ({E(best[3])}), כ-{d:.1f} ק"מ ממרכז היישוב.</li>'
    rows_html = ''.join(
        f'<tr><td>{E(r[3])}</td><td><span class="dot {r[2]}"></span>{CO_SHORT[r[2]]}</td><td>{" · ".join(gens(r[5])) or "לא צוין"}</td></tr>'
        for r in sorted(c['rows'], key=lambda r: (r[3], ORDER.index(r[2]))))
    table_co = ''.join(
        f'<tr><td><span class="dot {k}"></span>{CO[k]}</td><td>{st[k]["n"]}</td><td>{st[k]["g4"]}</td><td>{st[k]["g5"]}</td></tr>' for k in ORDER)
    near = sorted((p for p in pages if p['key'] != c['key']), key=lambda p: dist_km(c['center'], p['center']))[:8]
    near_html = ''.join(f'<a href="{quote(p["slug"])}.html">{E(p["name"])} <span>({len(p["rows"])})</span></a>' for p in near)
    faq = [
        (f'כמה אנטנות סלולריות יש ב{name}?',
         f'לפי נתוני המשרד להגנת הסביבה פועלים ב{name} {plural_sites(n)}: ' + ', '.join(f'{st[k]["n"]} של {CO[k]}' for k in ORDER) + '.'),
        (f'לאיזו חברה יש הכי הרבה אנטנות ב{name}?',
         lead_txt + ' מספר האתרים הוא אינדיקציה בלבד: הקליטה בפועל תלויה גם במרחק מהאתר, בבניין, בקומה ובעומס על הרשת.'),
        (f'יש דור 5 ב{name}?', g5_txt + ' כדי לגלוש בדור 5 צריך גם מכשיר תומך וחבילה שכוללת דור 5.'),
    ]
    faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    ld = [
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'מפת אנטנות ישראל', 'item': BASE_URL},
            {'@type': 'ListItem', 'position': 2, 'name': 'ערים ויישובים', 'item': BASE_URL + 'city/'},
            {'@type': 'ListItem', 'position': 3, 'name': name, 'item': url}]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
    ]
    city_json = json.dumps({'name': name, 'center': [round(c['center'][0], 5), round(c['center'][1], 5)],
                            'sites': [[r[0], r[1], r[2], r[3], ' '.join(gens(r[5]))] for r in c['rows']]},
                           ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <meta property="og:title" content="{E(title)}" />
  <meta property="og:description" content="{E(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:locale" content="he_IL" />
  <meta property="og:image" content="{BASE_URL}og-image.png" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📡</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <link rel="stylesheet" href="city.css?v=2" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')}</script>
</head>
<body>
<header class="top"><a href="../" class="brand">📡 מפת אנטנות ישראל</a><a href="../" class="back">בדיקה לפי כתובת ←</a></header>
<main>
  <nav class="crumbs" aria-label="מיקום באתר"><a href="../">ראשי</a> › <a href="./">ערים ויישובים</a> › <span>{E(name)}</span></nav>
  <h1>אנטנות סלולריות ב{E(name)}</h1>
  <p class="lede">ב{E(name)} פועלים <strong>{plural_sites(n)}</strong> סלולריים. {E(lead_txt)} {E(g5_txt)}</p>

  <div class="cards">
    {''.join(f'<div class="card {k}"><div class="num">{st[k]["n"]}</div><div class="lbl">{CO_SHORT[k]}</div><div class="sub">{st[k]["g5"]} עם דור 5</div></div>' for k in ORDER)}
  </div>

  <h2>מפת האנטנות ב{E(name)}</h2>
  <div id="map" role="img" aria-label="מפת אתרי השידור הסלולריים ב{E(name)}"></div>
  <p class="note">לחיצה על נקודה במפה מציגה את הכתובת, החברה והדורות המשודרים. לבדיקה לפי כתובת מדויקת: <a href="../">המפה המלאה</a>.</p>

  <h2>פירוט לפי חברה</h2>
  <table class="co"><thead><tr><th>חברה</th><th>אתרי שידור</th><th>עם דור 4</th><th>עם דור 5</th></tr></thead><tbody>{table_co}</tbody></table>
  {f'<ul class="missing">{miss_html}</ul>' if miss_html else ''}
  <p class="note">פרטנר והוט מובייל משתמשות ברשת משותפת (PHI), ולכן הן מופיעות יחד. מפעילים נוספים משתמשים ברשת של אחת משלוש החברות, וכדאי לבדוק מול המפעיל שלכם על איזו רשת הוא פועל.</p>

  <section class="lead" id="lead-form">
    <h2>קליטה גרועה ב{E(name)}?</h2>
    <p>השאירו פרטים ונבדוק איזו חברה מתאימה לכתובת שלכם. בלי עלות ובלי התחייבות.</p>
    <form id="city-form">
      <label for="cf-name">שם</label><input id="cf-name" name="name" type="text" required autocomplete="name" />
      <label for="cf-phone">טלפון</label><input id="cf-phone" name="phone" type="tel" required dir="ltr" autocomplete="tel" placeholder="050-0000000" />
      <label for="cf-loc">רחוב / שכונה</label><input id="cf-loc" name="location" type="text" placeholder="לא חובה" />
      <input type="text" id="cf-website" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp" />
      <label class="consent"><input type="checkbox" id="cf-consent" required /> <span>אני מאשר/ת שפרטיי יועברו לספקי שירות, למשווקים מורשים או לאתרי השוואה בתחום הסלולר, שיחזרו אליי בטלפון, בוואטסאפ או בהודעה, וקראתי את <a href="../privacy.html" target="_blank" rel="noopener">מדיניות הפרטיות</a> ואת <a href="../terms.html" target="_blank" rel="noopener">תנאי השימוש</a></span></label>
      <button type="submit">שלח — נבדוק ונחזור אליך ✓</button>
    </form>
    <div id="city-thanks" hidden><strong>קיבלנו ✅</strong><p>נחזור אליך בהקדם עם בדיקה לכתובת שלך.</p></div>
  </section>

  <h2>כל אתרי השידור ב{E(name)} ({n})</h2>
  <div class="tablewrap"><table class="sites"><thead><tr><th>כתובת</th><th>חברה</th><th>דורות</th></tr></thead><tbody>{rows_html}</tbody></table></div>

  <h2>שאלות נפוצות</h2>
  <div class="faq">{faq_html}</div>

  <h2>יישובים סמוכים</h2>
  <div class="near">{near_html}</div>

  <p class="source">מקור הנתונים: מאגר "אנטנות סלולריות פעילות" של המשרד להגנת הסביבה (data.gov.il){', עדכון ' + updated if updated else ''}. המידע מוצג כפי שהוא ועשוי להשתנות. מספר האתרים אינו מעיד בהכרח על איכות הקליטה בכתובת מסוימת.</p>
</main>
<footer><a href="../privacy.html">מדיניות פרטיות</a> · <a href="../terms.html">תנאי שימוש</a> · <a href="../accessibility.html">הצהרת נגישות</a><br/>אתר פרטי ועצמאי. אינו אתר ממשלתי ואינו פועל מטעם חברות הסלולר.</footer>
<script>window.CITY={city_json};</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" defer></script>
<script src="city.js?v=2" defer></script>
</body>
</html>
'''

def index_page(pages, total_sites, updated):
    by_letter = collections.defaultdict(list)
    for p in sorted(pages, key=lambda p: p['name']): by_letter[p['name'][0]].append(p)
    top = sorted(pages, key=lambda p: -len(p['rows']))[:24]
    top_html = ''.join(f'<a href="{quote(p["slug"])}.html">{E(p["name"])} <span>({len(p["rows"])})</span></a>' for p in top)
    letters = ''.join(
        f'<h3>{E(l)}</h3><div class="near">' + ''.join(f'<a href="{quote(p["slug"])}.html">{E(p["name"])} <span>({len(p["rows"])})</span></a>' for p in ps) + '</div>'
        for l, ps in sorted(by_letter.items()))
    url = BASE_URL + 'city/'
    title = 'אנטנות סלולריות לפי עיר ויישוב — מפת אנטנות ישראל'
    desc = f'רשימת {len(pages)} ערים ויישובים בישראל עם מספר אתרי השידור הסלולריים בכל אחד, לפי פרטנר, סלקום ופלאפון. מנתוני המשרד להגנת הסביבה.'
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📡</text></svg>">
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="city.css?v=2" />
</head>
<body>
<header class="top"><a href="../" class="brand">📡 מפת אנטנות ישראל</a><a href="../" class="back">בדיקה לפי כתובת ←</a></header>
<main>
  <nav class="crumbs" aria-label="מיקום באתר"><a href="../">ראשי</a> › <span>ערים ויישובים</span></nav>
  <h1>אנטנות סלולריות לפי עיר ויישוב</h1>
  <p class="lede">{total_sites:,} אתרי שידור סלולריים פעילים בישראל, מחולקים לפי יישוב. בחרו יישוב כדי לראות כמה אתרים יש בו לכל חברה, איפה משודר דור 5, ומפה של האתרים. המספר בסוגריים הוא מספר האתרים ביישוב.</p>
  <h2>הערים הגדולות</h2>
  <div class="near">{top_html}</div>
  <h2>כל היישובים לפי א"ב</h2>
  {letters}
  <p class="source">מקור הנתונים: מאגר "אנטנות סלולריות פעילות" של המשרד להגנת הסביבה (data.gov.il){', עדכון ' + updated if updated else ''}. מוצגים יישובים שיש בהם {MIN_SITES} אתרי שידור ומעלה. ליישובים קטנים יותר אפשר לבדוק <a href="../">לפי כתובת במפה המלאה</a>.</p>
</main>
<footer><a href="../privacy.html">מדיניות פרטיות</a> · <a href="../terms.html">תנאי שימוש</a> · <a href="../accessibility.html">הצהרת נגישות</a><br/>אתר פרטי ועצמאי. אינו אתר ממשלתי ואינו פועל מטעם חברות הסלולר.</footer>
<script src="city.js?v=2" defer></script>
</body>
</html>
'''

def sitemap(pages):
    urls = [(BASE_URL, '1.0', 'monthly'), (BASE_URL + 'city/', '0.8', 'monthly')]
    urls += [(BASE_URL + 'city/' + quote(p['slug']) + '.html', '0.6', 'monthly') for p in sorted(pages, key=lambda p: -len(p['rows']))]
    gdir = os.path.join(ROOT, 'guide')
    if os.path.isdir(gdir):
        urls.append((BASE_URL + 'guide/', '0.7', 'monthly'))
        urls += [(BASE_URL + 'guide/' + quote(f), '0.7', 'monthly') for f in sorted(os.listdir(gdir)) if f.endswith('.html') and f != 'index.html']
    urls += [(BASE_URL + f, '0.2', 'yearly') for f in ('privacy.html', 'terms.html', 'accessibility.html')]
    body = ''.join(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{f}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n' for u, pr, f in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n'

def main():
    data, updated = load()
    cities = group(data)
    pages = [c for c in cities if len(c['rows']) >= MIN_SITES]
    slugs = collections.Counter(p['slug'] for p in pages)
    assert all(v == 1 for v in slugs.values()), [s for s, v in slugs.items() if v > 1]
    out = os.path.join(ROOT, 'city')
    for f in os.listdir(out) if os.path.isdir(out) else []:
        if f.endswith('.html'): os.remove(os.path.join(out, f))
    os.makedirs(out, exist_ok=True)
    by_key = {c['key']: c for c in cities}
    for c in pages:
        open(os.path.join(out, c['slug'] + '.html'), 'w', encoding='utf8').write(page(c, by_key, data, pages, updated))
    open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(index_page(pages, len(data), updated))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf8').write(sitemap(pages))
    covered = sum(len(p['rows']) for p in pages)
    print(f'{len(pages)} city pages, {covered} of {len(data)} sites covered ({covered * 100 // len(data)}%), data updated {updated}')

if __name__ == '__main__':
    main()
