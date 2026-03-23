# דוח שיפור SEO לקלוד קוד
## מבוסס על ניתוח SEO Meta in 1 Click

> **הוראות:** קרא את הדוח ויישם את כל השינויים על index.html לפי סדר העדיפויות.

---

## 🔴 קריטי — תקן עכשיו

### 1. Canonical URL שבור
**הבעיה:** הכתובת הקנונית מכילה placeholder ולא כתובת אמיתית:
```
https://[הדומיין-שלך].co.il/
```
**תיקון:** החלף ל:
```html
<link rel="canonical" href="https://xyonatan2702x.github.io/antenna-map/">
```

### 2. og:url שבור
**הבעיה:** גם כתובת ה-Open Graph מכילה placeholder:
```
og:url = https://[הדומיין-שלך].co.il/
```
**תיקון:** החלף ל:
```html
<meta property="og:url" content="https://xyonatan2702x.github.io/antenna-map/">
```

### 3. תמונות בלי ALT — 14 תמונות
**הבעיה:** כל 14 התמונות בדף חסרות תג ALT — גוגל לא יכול לקרוא אותן.
**תיקון:** לתמונות של המפה (tiles) הוסף:
```html
alt="מפת אנטנות סלולריות ישראל"
```
לתמונות לוגו חברות:
```html
alt="לוגו פרטנר" / alt="לוגו פלאפון" / alt="לוגו סלקום"
```

---

## 🟠 חשוב — הוסף

### 4. Author ו-Publisher חסרים
הוסף ל-`<head>`:
```html
<meta name="author" content="קליטה טובה — ייעוץ סלולרי">
<meta name="publisher" content="קליטה טובה">
```

### 5. Twitter Card חסר לחלוטין
הוסף ל-`<head>`:
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="קליטה גרועה? עברו לחברה שמכסה אתכם">
<meta name="twitter:description" content="מפת אנטנות סלולריות בישראל — בדוק מי מכסה את האזור שלך. שירות ייעוץ חינמי.">
```

### 6. og:image חסר — תמונה לשיתוף
כשמשתפים את האתר בוואטסאפ/פייסבוק לא מופיעה תמונה.
צור קובץ תמונה בשם `og-image.png` (1200x630 פיקסל) עם הלוגו של האתר.
אז הוסף ל-`<head>`:
```html
<meta property="og:image" content="https://xyonatan2702x.github.io/antenna-map/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

### 7. H2 כפול "טוען נתוני אנטנות"
**הבעיה:** יש H2 עם הטקסט "טוען נתוני אנטנות" — זה כנראה הודעת טעינה שנשארת בקוד.
**תיקון:** וודא שה-H2 הזה מוסתר כשהאתר נטען:
```html
<h2 id="loading-h2" style="display:none">טוען נתוני אנטנות</h2>
```
או הסר אותו לגמרי אם לא צריך.

---

## 🟡 שיפור — כדאי לעשות

### 8. Sitemap.xml — לוודא שקיים ונגיש
בדוק שהקובץ `sitemap.xml` נמצא בתיקייה הראשית ונגיש בכתובת:
`https://xyonatan2702x.github.io/antenna-map/sitemap.xml`

עדכן את התוכן:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://xyonatan2702x.github.io/antenna-map/</loc>
    <lastmod>2026-03-22</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

### 9. Robots.txt — לוודא שמציין sitemap
```
User-agent: *
Allow: /
Sitemap: https://xyonatan2702x.github.io/antenna-map/sitemap.xml
```

### 10. Schema LocalBusiness חסר
הוסף לפני `</body>`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "קליטה טובה — ייעוץ סלולרי",
  "description": "ייעוץ חינמי למעבר חברת סלולר ללקוחות עם בעיות קליטה",
  "url": "https://xyonatan2702x.github.io/antenna-map/",
  "areaServed": "IL",
  "serviceType": "ייעוץ מעבר חברת סלולר",
  "priceRange": "חינם"
}
</script>
```

---

## סדר ביצוע

| עדיפות | משימה |
|--------|--------|
| 🔴 1 | תקן canonical URL |
| 🔴 2 | תקן og:url |
| 🔴 3 | הוסף ALT לכל 14 התמונות |
| 🟠 4 | הוסף Author + Publisher |
| 🟠 5 | הוסף Twitter Card |
| 🟠 6 | הוסף og:image |
| 🟠 7 | תקן H2 "טוען נתוני אנטנות" |
| 🟡 8 | עדכן sitemap.xml |
| 🟡 9 | עדכן robots.txt |
| 🟡 10 | הוסף Schema LocalBusiness |
