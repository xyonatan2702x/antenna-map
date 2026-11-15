"""Builds stats/index.html and stats/antennas-by-city.csv. Called from build_cities.py (not run on its own)."""
import csv, io, json, os
from urllib.parse import quote


def build(b, pages, data, nat, pop_year, updated):
    E, CO, CO_SHORT, ORDER, BASE = b.E, b.CO, b.CO_SHORT, b.ORDER, b.BASE_URL
    f1, pct = b.f1, b.pct
    out = os.path.join(b.ROOT, 'stats')
    os.makedirs(out, exist_ok=True)
    url = BASE + 'stats/'
    link = lambda p: f'<a href="../city/{quote(p["slug"])}.html">{E(p["name"])}</a>'
    for p in pages:
        p['st'] = b.stats(p)

    # ---- national figures
    co = {k: {'n': sum(r[2] == k for r in data), 'g5': sum(r[2] == k and '5' in b.gens(r[5]) for r in data)} for k in ORDER}
    all_places = {b.key_of(r[4]) for r in data if r[4].strip()} - b.EXCLUDE
    no5 = [p for p in pages if p['g5'] == 0]
    lead = {k: 0 for k in ORDER}
    for p in pages:
        top = max(p['st'][k]['n'] for k in ORDER)
        winners = [k for k in ORDER if p['st'][k]['n'] == top]
        if len(winners) == 1: lead[winners[0]] += 1
    tied = len(pages) - sum(lead.values())

    co_rows = ''.join(
        f'<tr><td><span class="dot {k}"></span>{CO[k]}</td><td>{co[k]["n"]:,}</td><td>{pct(co[k]["n"], nat["n"])}</td>'
        f'<td>{co[k]["g5"]:,}</td><td>{pct(co[k]["g5"], co[k]["n"])}</td><td>{lead[k]}</td></tr>' for k in ORDER)

    # ---- most sites
    top_sites = sorted(pages, key=lambda p: -p['n'])[:20]
    top_rows = ''.join(
        f'<tr><td>{i}</td><td>{link(p)}</td><td>{p["n"]}</td>' + ''.join(f'<td>{p["st"][k]["n"]}</td>' for k in ORDER)
        + f'<td>{pct(p["g5"], p["n"])}</td></tr>' for i, p in enumerate(top_sites, 1))

    # ---- per 10,000 residents, cities with POP_MIN_RANK residents and more
    big = sorted((p for p in pages if p.get('rank10k')), key=lambda p: -p['per10k'])
    big_rows = ''.join(
        f'<tr><td>{p["rank10k"]}</td><td>{link(p)}</td><td>{p["pop"]:,}</td><td>{p["n"]}</td><td>{f1(p["per10k"])}</td><td>{pct(p["g5"], p["n"])}</td></tr>'
        for p in big)
    hi, lo = big[:5], big[::-1][:5]
    names = lambda ps: ', '.join(f'{p["name"]} ({f1(p["per10k"])})' for p in ps)

    # ---- 5G
    big5 = sorted(big, key=lambda p: -p['g5'] / p['n'])
    g5_hi = ', '.join(f'{p["name"]} ({pct(p["g5"], p["n"])})' for p in big5[:5])
    g5_lo = ', '.join(f'{p["name"]} ({pct(p["g5"], p["n"])})' for p in big5[::-1][:5])
    no5_big = sorted(no5, key=lambda p: -p['n'])[:10]
    no5_html = ''.join(f'<a href="../city/{quote(p["slug"])}.html">{E(p["name"])} <span>({p["n"]})</span></a>' for p in no5_big)

    # ---- CSV for download (all places with a page)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(['יישוב', 'אתרי שידור', 'פרטנר והוט מובייל', 'פלאפון', 'סלקום', 'אתרים עם דור 5',
                f'תושבים (מפקד {pop_year})', 'אתרי שידור ל-10,000 תושבים'])
    for p in sorted(pages, key=lambda p: -p['n']):
        w.writerow([p['name'], p['n']] + [p['st'][k]['n'] for k in ORDER] + [p['g5'], p['pop'] or '', f1(p['per10k']) if p['per10k'] else ''])
    open(os.path.join(out, 'antennas-by-city.csv'), 'w', encoding='utf-8-sig', newline='').write(buf.getvalue())

    title = 'אנטנות סלולריות בישראל במספרים — דירוג ערים, דור 5 וחברות | אין קליטה'
    desc = (f'{nat["n"]:,} אתרי שידור סלולריים פעילים בישראל: כמה לכל חברה, באילו ערים יש הכי הרבה והכי מעט אנטנות ביחס לתושבים, '
            f'ואיפה משודר דור 5. מעובד מנתוני המשרד להגנת הסביבה והלמ"ס.')
    ld = [
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'אין קליטה', 'item': BASE},
            {'@type': 'ListItem', 'position': 2, 'name': 'נתונים ודירוגים', 'item': url}]},
        {'@context': 'https://schema.org', '@type': 'Dataset', 'name': 'אתרי שידור סלולריים בישראל לפי יישוב',
         'description': f'מספר אתרי השידור הסלולריים הפעילים בכל יישוב בישראל, לפי חברה (פרטנר והוט מובייל, פלאפון, סלקום), מספר האתרים עם דור 5, '
                        f'ומספר האתרים ביחס לתושבים. עיבוד של מאגר "אנטנות סלולריות פעילות" של המשרד להגנת הסביבה ושל מפקד האוכלוסין {pop_year}.',
         'url': url, 'inLanguage': 'he', 'isAccessibleForFree': True, 'dateModified': b.TODAY,
         'spatialCoverage': {'@type': 'Country', 'name': 'Israel'},
         'creator': {'@type': 'Organization', 'name': 'אין קליטה', 'url': BASE},
         'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'text/csv', 'contentUrl': url + 'antennas-by-city.csv'}]},
    ]
    upd = f', עדכון {updated}' if updated else ''
    html = f'''<!DOCTYPE html>
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
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:locale" content="he_IL" />
  <meta property="og:site_name" content="אין קליטה" />
  <meta property="og:image" content="{BASE}og-image.png" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📡</text></svg>">
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../city/city.css?v=6" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')}</script>
</head>
<body>
<header class="top"><a href="../" class="brand">📡 אין קליטה <small>· מפת אנטנות סלולריות</small></a><a href="../" class="back">בדיקה לפי כתובת ←</a></header>
<main>
  <nav class="crumbs" aria-label="מיקום באתר"><a href="../">ראשי</a> › <span>נתונים ודירוגים</span></nav>
  <h1>אנטנות סלולריות בישראל במספרים</h1>
  <p class="lede">בישראל פועלים <strong>{nat["n"]:,} אתרי שידור סלולריים</strong> ב-{len(all_places):,} יישובים ואזורים. דור 5 משודר ב-{round(nat["g5_pct"])}% מהם. בממוצע יש {f1(nat["per10k"])} אתרי שידור לכל 10,000 תושבים, אבל הפער בין הערים גדול: מ-{f1(big[-1]["per10k"])} ב{E(big[-1]["name"])} ועד {f1(big[0]["per10k"])} ב{E(big[0]["name"])}.</p>

  <div class="cards">
    {''.join(f'<div class="card {k}"><div class="num">{co[k]["n"]:,}</div><div class="lbl">{CO_SHORT[k]}</div><div class="sub">{pct(co[k]["g5"], co[k]["n"])} עם דור 5</div></div>' for k in ORDER)}
  </div>

  <h2>אתרי שידור לפי חברה</h2>
  <div class="tablewrap"><table class="co"><thead><tr><th>חברה</th><th>אתרי שידור</th><th>חלק מהסך</th><th>עם דור 5</th><th>שיעור דור 5</th><th>יישובים שבהם היא מובילה</th></tr></thead><tbody>{co_rows}</tbody></table></div>
  <p class="note">"מובילה" פירושו שלחברה יש יותר אתרי שידור ביישוב מלכל חברה אחרת, מתוך {len(pages)} יישובים שיש בהם {b.MIN_SITES} אתרים ומעלה. ב-{tied} יישובים יש שוויון. פרטנר והוט מובייל משתמשות ברשת משותפת (PHI) ולכן נספרות יחד.</p>

  <h2>אנטנות ביחס למספר התושבים: דירוג {len(big)} הערים הגדולות</h2>
  <p>הטבלה מדרגת את הערים שיש בהן {b.POP_MIN_RANK // 1000} אלף תושבים ומעלה לפי מספר אתרי השידור לכל 10,000 תושבים. בראש הדירוג: {E(names(hi))}. בתחתית: {E(names(lo))}.</p>
  <div class="tablewrap"><table class="rank"><thead><tr><th>#</th><th>עיר</th><th>תושבים</th><th>אתרי שידור</th><th>ל-10,000 תושבים</th><th>עם דור 5</th></tr></thead><tbody>{big_rows}</tbody></table></div>
  <p class="note">מספר אתרים נמוך ביחס לתושבים לא אומר בהכרח שהקליטה גרועה: אתרי שידור נבדלים בעוצמה ובכיסוי, אתר בעיר אחת משרת לעיתים גם את שכנתה, ובערי תיירות ותעסוקה יש הרבה יותר משתמשים מתושבים.</p>

  <h2>20 היישובים עם הכי הרבה אתרי שידור</h2>
  <div class="tablewrap"><table class="rank"><thead><tr><th>#</th><th>יישוב</th><th>אתרי שידור</th><th>פרטנר</th><th>פלאפון</th><th>סלקום</th><th>עם דור 5</th></tr></thead><tbody>{top_rows}</tbody></table></div>

  <h2>דור 5: איפה יש ואיפה עדיין לא</h2>
  <p>דור 5 משודר ב-{nat["g5"]:,} מתוך {nat["n"]:,} אתרי השידור בארץ ({round(nat["g5_pct"])}%). מבין הערים הגדולות, השיעור הגבוה ביותר הוא ב: {E(g5_hi)}. הנמוך ביותר: {E(g5_lo)}.</p>
  <p>ב-{len(no5)} מתוך {len(pages)} היישובים שמופיעים באתר אין כרגע אף אתר שמשדר דור 5. הגדולים שבהם, לפי מספר אתרי השידור:</p>
  <div class="near">{no5_html}</div>

  <h2>להורדה ולציטוט</h2>
  <p>הטבלה המלאה של {len(pages)} היישובים זמינה להורדה: <a href="antennas-by-city.csv" download>antennas-by-city.csv</a>. מותר להשתמש בנתונים ולצטט אותם, עם קישור למקור: <span dir="ltr">einklita.co.il/stats</span>. לכל יישוב יש גם <a href="../city/">דף עם מפה ורשימת כתובות</a>.</p>

  <h2>איך חושבו הנתונים</h2>
  <ul class="facts">
    <li>מקור האנטנות: מאגר "אנטנות סלולריות פעילות" של המשרד להגנת הסביבה (data.gov.il){upd}. כל רשומה במאגר היא אתר שידור של חברה אחת, כך שתורן שמשמש שלוש חברות נספר שלוש פעמים.</li>
    <li>השיוך ליישוב הוא לפי שם היישוב שמופיע במאגר. איחדנו כתיבים שונים של אותו יישוב. אתרים שמשויכים למועצה אזורית או לשטח פתוח לא נספרים לעיר הסמוכה.</li>
    <li>מספר התושבים: מפקד האוכלוסין והדיור {pop_year} של הלשכה המרכזית לסטטיסטיקה. האנטנות מעודכנות יותר מנתוני האוכלוסייה, ולכן היחס מקורב.</li>
    <li>"עם דור 5" פירושו שבאתר מדווח שידור בדור 5. כדי לגלוש בדור 5 צריך גם מכשיר תומך וחבילה מתאימה.</li>
  </ul>

  <p class="source">הנתונים מוצגים כפי שהם ועשויים להשתנות. מספר אתרי השידור אינו מעיד בהכרח על איכות הקליטה בכתובת מסוימת. לבדיקה לפי כתובת: <a href="../">המפה המלאה</a>.</p>
</main>
<footer><a href="../city/">ערים ויישובים</a> · <a href="../guide/">מדריכים</a> · <a href="../privacy.html">מדיניות פרטיות</a> · <a href="../terms.html">תנאי שימוש</a> · <a href="../accessibility.html">הצהרת נגישות</a> · <a href="../contact.html">יצירת קשר</a><br/>אתר פרטי ועצמאי. אינו אתר ממשלתי ואינו פועל מטעם חברות הסלולר.</footer>
<script>window.PAGE='/stats/';</script>
<script src="../city/city.js?v=2" defer></script>
</body>
</html>
'''
    open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(html)
