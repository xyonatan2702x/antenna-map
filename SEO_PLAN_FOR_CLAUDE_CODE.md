# תוכנית SEO — אתר לידים לחילוף חברת סלולר

> **הוראות לקלוד קוד:** קרא את כל המסמך לפני שאתה מתחיל. זהו PLAN מלא ליישום. בצע את כל השלבים לפי הסדר. אין לדלג על שלב.

---

## רקע על האתר

**מטרת האתר:** איסוף לידים מלקוחות פרטיים שסובלים מקליטה גרועה ורוצים לעבור חברת סלולר.

**קהל יעד:** גולשים שמחפשים בגוגל (ובמנועי AI) ביטויים כמו:
- "אין קליטה בבית"
- "קליטה גרועה [שם חברה]"
- "איך לשפר קליטה סלולרית"
- "להחליף חברת סלולר"
- "פלאפון / סלקום / הוט קליטה גרועה מה לעשות"

**פלטפורמה:** HTML סטטי (קובץ/קבצים)

**אזור שירות:** כל הארץ

**שם העסק:** [← מלא את שם העסק כאן]

**חברת סלולר שמפנים אליה:** [← מלא: פלאפון / סלקום / הוט / אחר]

---

## שלב 1 — תיקון ה-`<head>` בכל דף HTML

### 1.1 — Title Tag
החלף את ה-title הקיים ב:

```html
<title>קליטה גרועה? עברו לחברה שמכסה אתכם | [שם העסק]</title>
```

**כללים לכתיבת Title:**
- אורך: 50–60 תווים
- לכלול מילת מפתח ראשית + שם עסק
- לא לחזור על אותו title בכמה דפים

### 1.2 — Meta Description
הוסף מיד אחרי ה-title:

```html
<meta name="description" content="סובלים מקליטה גרועה? אנחנו עוזרים לכם לעבור לחברת סלולר שמתאימה לאזור שלכם. השאירו פרטים ונחזור אליכם תוך שעה.">
```

**כללים:**
- אורך: 150–160 תווים
- לכלול call-to-action ברור

### 1.3 — Meta Tags נוספים חובה

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://[הדומיין-שלך].co.il/">

<!-- Open Graph (לשיתוף בווטסאפ ופייסבוק) -->
<meta property="og:title" content="קליטה גרועה? עברו לחברה שמכסה אתכם">
<meta property="og:description" content="עוזרים לכם לעבור חברת סלולר בקלות. השאירו פרטים ונחזור אליכם תוך שעה.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://[הדומיין-שלך].co.il/">
<meta property="og:locale" content="he_IL">
```

---

## שלב 2 — מבנה כותרות (H1, H2, H3)

### כלל ברזל:
- **H1 אחד בלבד** בכל דף — מכיל מילת מפתח ראשית
- **H2** לכל סקשן/נושא
- **H3** לפרטים תחת H2

### H1 מומלץ לדף הבית:
```html
<h1>סובלים מקליטה גרועה? נעזור לכם לעבור חברת סלולר בקלות</h1>
```

### H2 מומלצים לסקשנים:
```html
<h2>למה הקליטה שלכם גרועה?</h2>
<h2>איך אנחנו עוזרים לכם לעבור?</h2>
<h2>אילו חברות סלולר מכסות את האזור שלכם?</h2>
<h2>השאירו פרטים ונחזור אליכם</h2>
```

---

## שלב 3 — תוכן הדף (Copywriting ממוקד SEO)

### 3.1 — פסקת פתיחה אחרי ה-H1

```html
<p>
  אם אתם חווים קליטה גרועה בבית, בעבודה או בדרך — אתם לא לבד.
  אלפי ישראלים סובלים מאותה בעיה, ולרוב הפתרון פשוט: מעבר לחברת סלולר
  שמספקת כיסוי טוב יותר באזורכם. אנחנו עוזרים לכם לבדוק מי מכסה אתכם
  ולעבור בקלות ובמהירות.
</p>
```

### 3.2 — סקשן "למה הקליטה גרועה"

```html
<section>
  <h2>למה הקליטה שלכם גרועה?</h2>
  <p>
    קליטה גרועה יכולה להיגרם ממספר סיבות: מיקום גיאוגרפי, מבנים עם
    קירות עבים, עומס על התורנים באזורכם, או פשוט כיסוי חלקי של החברה
    שלכם. הדרך הכי מהירה לפתור את זה — לבדוק אם חברה אחרת מכסה את
    האזור שלכם טוב יותר.
  </p>
</section>
```

### 3.3 — סקשן תהליך (ממוקד המרה)

```html
<section>
  <h2>איך זה עובד?</h2>
  <ol>
    <li>משאירים פרטים בטופס</li>
    <li>אנחנו בודקים מי מכסה את האזור שלכם</li>
    <li>מקבלים המלצה אישית ועוברים בקלות</li>
  </ol>
</section>
```

---

## שלב 4 — טופס הליד (שיפור ל-CRO + SEO)

```html
<section id="lead-form">
  <h2>השאירו פרטים ונחזור אליכם תוך שעה</h2>
  <form>
    <label for="name">שם מלא</label>
    <input type="text" id="name" name="name" placeholder="ישראל ישראלי" required>

    <label for="phone">טלפון</label>
    <input type="tel" id="phone" name="phone" placeholder="05X-XXXXXXX" required>

    <label for="city">עיר מגורים</label>
    <input type="text" id="city" name="city" placeholder="תל אביב, ירושלים..." required>

    <label for="current_company">חברת הסלולר הנוכחית שלך</label>
    <select id="current_company" name="current_company">
      <option value="">בחר חברה</option>
      <option value="pelephone">פלאפון</option>
      <option value="cellcom">סלקום</option>
      <option value="hot">הוט מובייל</option>
      <option value="partner">פרטנר</option>
      <option value="other">אחר</option>
    </select>

    <label for="problem">תאר בקצרה את הבעיה</label>
    <textarea id="problem" name="problem" placeholder="למשל: אין קליטה בבית, השיחות נופלות..."></textarea>

    <button type="submit">שליחה — נחזור אליך תוך שעה</button>
  </form>
</section>
```

**חשוב:** וודא שהטופס שולח לשירות אמיתי (Formspree / EmailJS / Google Forms embed). אם לא — הוסף אינטגרציה.

---

## שלב 5 — Schema Markup (JSON-LD)

הוסף לפני סגירת `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[שם העסק]",
  "description": "עוזרים ללקוחות פרטיים לעבור חברת סלולר בגלל קליטה גרועה",
  "url": "https://[הדומיין-שלך].co.il",
  "areaServed": {
    "@type": "Country",
    "name": "Israel"
  },
  "serviceType": "מעבר בין חברות סלולר",
  "availableLanguage": "Hebrew",
  "potentialAction": {
    "@type": "LeaveAction",
    "name": "השאר פרטים",
    "target": "https://[הדומיין-שלך].co.il/#lead-form"
  }
}
</script>
```

---

## שלב 6 — קובץ sitemap.xml

צור קובץ `sitemap.xml` בתיקיית הבסיס של האתר:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://[הדומיין-שלך].co.il/</loc>
    <lastmod>[תאריך היום YYYY-MM-DD]</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

---

## שלב 7 — קובץ robots.txt

צור קובץ `robots.txt` בתיקיית הבסיס:

```
User-agent: *
Allow: /

Sitemap: https://[הדומיין-שלך].co.il/sitemap.xml
```

---

## שלב 8 — ביצועים (Performance)

### תמונות
- לכל `<img>` להוסיף `alt` בעברית עם מילת מפתח:
  ```html
  <img src="..." alt="קליטה גרועה בסלולר — מעבר חברה">
  ```
- להוסיף `loading="lazy"` לתמונות שלא בחלק הראשון של הדף

### מהירות
- להוסיף ל-`<head>`:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  ```

---

## שלב 9 — אופטימיזציה למנועי AI (AEO)

מנועי AI כמו ChatGPT ו-Perplexity מחפשים תוכן שעונה על שאלות ישירות.

### הוסף סקשן FAQ לדף:

```html
<section id="faq">
  <h2>שאלות נפוצות</h2>

  <details>
    <summary>מה עושים כשיש קליטה גרועה בבית?</summary>
    <p>אם יש לכם קליטה גרועה בבית, הצעד הראשון הוא לבדוק אם חברת הסלולר שלכם מכסה את האזור שלכם. אם לא — מעבר לחברה אחרת הוא הפתרון המהיר והיעיל ביותר. השאירו פרטים ואנחנו נבדוק עבורכם.</p>
  </details>

  <details>
    <summary>איזו חברת סלולר הכי טובה לקליטה?</summary>
    <p>זה תלוי באזור המגורים שלכם. כל חברה מכסה אזורים שונים בצורה שונה. אנחנו בודקים עבורכם מי מכסה את האזור שלכם ומציעים את ההתאמה הטובה ביותר.</p>
  </details>

  <details>
    <summary>כמה עולה לעבור חברת סלולר?</summary>
    <p>המעבר עצמו הוא בחינם. אנחנו מסייעים לכם למצוא חבילה מתאימה ועוברים יחד בתהליך פשוט ומהיר.</p>
  </details>

  <details>
    <summary>כמה זמן לוקח המעבר?</summary>
    <p>תהליך מעבר בין חברות סלולר לוקח בדרך כלל 24–48 שעות. המספר שלכם נשמר.</p>
  </details>
</section>
```

### הוסף Schema FAQ:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "מה עושים כשיש קליטה גרועה בבית?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "הצעד הראשון הוא לבדוק אם חברת הסלולר שלכם מכסה את האזור שלכם. אם לא — מעבר לחברה אחרת הוא הפתרון המהיר ביותר."
      }
    },
    {
      "@type": "Question",
      "name": "איזו חברת סלולר הכי טובה לקליטה?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "זה תלוי באזור המגורים. אנחנו בודקים עבורכם מי מכסה את האזור שלכם ומציעים התאמה אישית."
      }
    }
  ]
}
</script>
```

---

## שלב 10 — בדיקות אחרי היישום

| בדיקה | כלי | מה לבדוק |
|-------|-----|-----------|
| מהירות | PageSpeed Insights | ציון 90+ במובייל |
| Schema | Google Rich Results Test | ללא שגיאות |
| Mobile | Google Mobile-Friendly Test | עובר |
| Meta Tags | פתח דפדפן | Title נכון בטאב |
| טופס | שלח טופס בדיקה | מגיע למייל |

---

## סיכום — סדר ביצוע

1. שלב 1 — תיקון `<head>` (title + meta)
2. שלב 2 — תיקון כותרות H1/H2/H3
3. שלב 3 — שיפור תוכן הדף
4. שלב 4 — שיפור טופס הליד
5. שלב 5 — הוספת Schema JSON-LD
6. שלב 6 — יצירת sitemap.xml
7. שלב 7 — יצירת robots.txt
8. שלב 8 — אופטימיזציה לביצועים
9. שלב 9 — הוספת FAQ (לגוגל + AI)
10. שלב 10 — בדיקות סיום

---

**הערה לקלוד קוד:** בכל מקום שמופיע `[הדומיין-שלך]` או `[שם העסק]` — תשאל את המשתמש לפני שמתחילים.
