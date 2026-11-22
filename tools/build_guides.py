#!/usr/bin/env python3
"""Builds guide/<slug>.html and guide/index.html from tools/guides_content.py.

Run from the repo root:  python3 tools/build_guides.py   (then tools/build_cities.py refreshes the sitemap)
"""
import html, json, os, re, sys, datetime
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides_content import GUIDES

BASE = 'https://einklita.co.il/'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'guide')
TODAY = datetime.date.today().isoformat()
E = html.escape
CSS = '../city/city.css?v=7'
ICON = "<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📡</text></svg>\">"
HEADER = '<header class="top"><a href="../" class="brand">📡 אין קליטה <small>· מפת אנטנות סלולריות</small></a><a href="../" class="back">בדיקה לפי כתובת ←</a></header>'
FOOTER = ('<footer><a href="../stats/">נתונים ודירוגים</a> · <a href="../privacy.html">מדיניות פרטיות</a> · <a href="../terms.html">תנאי שימוש</a> · '
          '<a href="../accessibility.html">הצהרת נגישות</a> · <a href="../about.html">אודות</a> · <a href="../contact.html">יצירת קשר</a><br/>אתר פרטי ועצמאי. אינו אתר ממשלתי ואינו פועל מטעם חברות הסלולר.</footer>')
LEAD = '''  <section class="leadq" id="lead-form">
    <div data-lead-quiz></div>
  </section>'''


def url_of(g):
    return BASE + 'guide/' + quote(g['slug']) + '.html'


def he_date(iso):
    y, m, d = iso.split('-')
    return f'{int(d)}.{int(m)}.{y}'


def page(g):
    url = url_of(g)
    others = [o for o in GUIDES if o is not g]
    related = ''.join(f'<a href="{quote(o["slug"])}.html">{E(o["short"])}</a>' for o in others)
    faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in g['faq'])
    ld = [
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['desc'], 'inLanguage': 'he',
         'datePublished': g['published'], 'dateModified': TODAY, 'mainEntityOfPage': url, 'image': BASE + 'og-image.png',
         'author': {'@type': 'Organization', 'name': 'אין קליטה', 'url': BASE},
         'publisher': {'@type': 'Organization', 'name': 'אין קליטה', 'url': BASE}},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'אין קליטה', 'item': BASE},
            {'@type': 'ListItem', 'position': 2, 'name': 'מדריכים', 'item': BASE + 'guide/'},
            {'@type': 'ListItem', 'position': 3, 'name': g['short'], 'item': url}]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]},
    ]
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{E(g['title'])}</title>
  <meta name="description" content="{E(g['desc'])}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <meta property="og:title" content="{E(g['title'])}" />
  <meta property="og:description" content="{E(g['desc'])}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:locale" content="he_IL" />
  <meta property="og:site_name" content="אין קליטה" />
  <meta property="og:image" content="{BASE}og-image.png" />
  {ICON}
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{CSS}" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')}</script>
</head>
<body>
{HEADER}
<main class="article">
  <nav class="crumbs" aria-label="מיקום באתר"><a href="../">ראשי</a> › <a href="./">מדריכים</a> › <span>{E(g['short'])}</span></nav>
  <h1>{E(g['title'])}</h1>
  <p class="updated">עודכן: {he_date(TODAY)}</p>
  <p class="lede">{E(g['desc'])}</p>
{g['body'].strip()}
  <p class="cta"><a href="../">בדקו את הכתובת שלכם במפת האנטנות ←</a></p>

  <h2>שאלות נפוצות</h2>
  <div class="faq">{faq_html}</div>

{LEAD}

  <h2>מדריכים נוספים</h2>
  <div class="near">{related}</div>
  <h2>בדיקה לפי יישוב</h2>
  <p class="note">רוצים לראות כמה אנטנות יש לכל חברה אצלכם? <a href="../city/">רשימת כל היישובים</a>, <a href="../stats/">דירוג הערים</a> או <a href="../">חיפוש לפי כתובת במפה</a>.</p>
</main>
{FOOTER}
<script>window.PAGE='/guide/{g['slug']}';</script>
<script src="../city/city.js?v=2" defer></script>
<script src="../quiz.js?v=4" defer></script>
</body>
</html>
'''


def index_page():
    cards = ''.join(
        f'<a class="gcard" href="{quote(g["slug"])}.html"><span class="ic">{g["icon"]}</span><strong>{E(g["title"])}</strong><span class="ex">{E(g["desc"])}</span></a>'
        for g in GUIDES)
    ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'url': url_of(g), 'name': g['title']} for i, g in enumerate(GUIDES, 1)]}
    desc = 'מדריכים על קליטה סלולרית בישראל: מה עושים כשאין קליטה בבית, שיחות Wi-Fi, קליטה בממ"ד, מגברים, בדיקת עוצמת קליטה, סגירת דור 2 ו-3 ומי פועל על איזו רשת.'
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>מדריכים על קליטה סלולרית — אין קליטה</title>
  <meta name="description" content="{E(desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{BASE}guide/" />
  <meta property="og:title" content="מדריכים על קליטה סלולרית — אין קליטה" />
  <meta property="og:description" content="{E(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE}guide/" />
  <meta property="og:locale" content="he_IL" />
  <meta property="og:site_name" content="אין קליטה" />
  <meta property="og:image" content="{BASE}og-image.png" />
  {ICON}
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{CSS}" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')}</script>
</head>
<body>
{HEADER}
<main>
  <nav class="crumbs" aria-label="מיקום באתר"><a href="../">ראשי</a> › <span>מדריכים</span></nav>
  <h1>מדריכים על קליטה סלולרית</h1>
  <p class="lede">מה עושים כשאין קליטה, איך בודקים אותה נכון, ומה כדאי לדעת לפני שמחליפים חברה.</p>
  <div class="gcards">{cards}</div>
</main>
{FOOTER}
<script>window.PAGE='/guide/';</script>
<script src="../city/city.js?v=2" defer></script>
</body>
</html>
'''


def main():
    slugs = [g['slug'] for g in GUIDES]
    assert len(set(slugs)) == len(slugs), 'duplicate slug'
    for g in GUIDES:
        # every internal guide link in the body must point to an existing guide
        for href in re.findall(r'href="([^"#]+\.html)"', g['body']):
            assert href[:-5] in slugs, f'{g["slug"]}: broken link {href}'
    for f in os.listdir(OUT):
        if f.endswith('.html'): os.remove(os.path.join(OUT, f))
    for g in GUIDES:
        open(os.path.join(OUT, g['slug'] + '.html'), 'w', encoding='utf8').write(page(g))
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(index_page())
    update_home()
    print(f'{len(GUIDES)} guides')


def update_home():
    """Rewrites the guide cards on the home page (between the blog title and the end of the blog section)."""
    path = os.path.join(ROOT, 'index.html')
    t = open(path, encoding='utf8').read()
    start_tag = '<h2 class="blog-main-title">'
    s = t.index(start_tag)
    s = t.index('</h2>', s) + len('</h2>')
    e = t.index('  </div>\n</section>', s)
    cards = ''.join(f'''
  <article class="blog-card">
    <div class="blog-card-header">
      <div class="blog-card-icon">{g['icon']}</div>
      <h3>{E(g['title'])}</h3>
    </div>
    <p class="blog-excerpt">{E(g['desc'])}</p>
    <a class="blog-read-more" href="guide/{quote(g['slug'])}.html" style="text-decoration:none">למדריך המלא ←</a>
  </article>
''' for g in GUIDES[:6])
    more = '\n  <p style="text-align:center;margin-top:8px"><a href="guide/" style="color:#007a8c;font-weight:600">כל המדריכים ←</a></p>\n\n'
    open(path, 'w', encoding='utf8').write(t[:s] + '\n' + cards + more + t[e:])


if __name__ == '__main__':
    main()
