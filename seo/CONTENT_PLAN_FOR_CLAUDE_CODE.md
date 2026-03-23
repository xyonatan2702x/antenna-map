# תוכנית תוכן — שיפור אתר קליטה-טובה
## מבוסס על ניתוח מתחרים ומחקר שוק

> **הוראות לקלוד קוד:** קרא את הדוח הזה ויישם את כל השינויים על index.html לפי סדר העדיפויות.

---

## המסר המרכזי של האתר (לשים בכל מקום)

> **"לא עוד השוואה בטבלה — אנחנו עושים את זה בשבילך"**

המתחרים (כמו השוואת מחירים) נותנים מידע קר. אנחנו נותנים שירות אישי.
זה ההבדל — לבטא אותו בכל כותרת, בכל כפתור, בכל משפט.

---

## שלב 1 — כותרות (H1, H2) לשנות/להוסיף

### H1 ראשי (הכותרת הגדולה של הדף):
```
קליטה גרועה? נעזור לך לעבור לחברה שתתאים לך — בלי טבלאות, בלי בלבול
```

### H2 משנה — לפזר לאורך הדף:
```
למה הקליטה שלך גרועה — והפתרון האמיתי
איזו חברת סלולר יש לה קליטה טובה באזור שלך?
כמה עולה לעבור חברת סלולר? (ספוילר: פחות ממה שחשבת)
עוברים חברה בלי לאבד את המספר שלך
אנחנו עושים את זה בשבילך — בחינם
```

---

## שלב 2 — סקשן "למה הקליטה שלך גרועה"

הוסף סקשן טקסט חדש עם הכותרת `<h2>למה הקליטה שלך גרועה?</h2>` והתוכן הבא:

```
לכל חברת סלולר יש רשת אנטנות משלה — ולא כל חברה מכסה את כל האזורים באותה רמה.

הסיבות הנפוצות לקליטה גרועה:
• החברה שלך פשוט לא מכסה טוב את האזור שלך
• קירות בטון עבים בבית או במרתף
• עומס על הרשת בשעות שיא
• תשתית ישנה של הספק באזורך

הפתרון הכי פשוט? לעבור לחברה שיש לה קליטה טובה דווקא אצלך — 
ואנחנו יודעים בדיוק איזו חברה זו.
```

---

## שלב 3 — סקשן FAQ מלא (עם Schema)

החלף או הוסף סקשן FAQ עם הקוד הבא **במלואו**:

```html
<section itemscope itemtype="https://schema.org/FAQPage">
  <h2>שאלות נפוצות על מעבר חברת סלולר</h2>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">כמה עולה לעבור חברת סלולר?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">המעבר עצמו עולה בין אפס ל-49 שקלים (דמי התחברות וכרטיס סים). בחלק מהחברות ההצטרפות חינמית לגמרי. אנחנו נדאג שתעברו לחברה שמציעה את התנאים הטובים ביותר עבורכם.</p>
    </div>
  </div>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">האם אאבד את המספר שלי כשאעבור חברה?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">לא. בישראל אפשר לשמור על אותו מספר סלולרי בכל מעבר בין חברות. התהליך נקרא "ניוד מספר" והוא פשוט וחינמי.</p>
    </div>
  </div>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">כמה זמן לוקח המעבר לחברה חדשה?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">המעבר לוקח בין כמה שעות ליום עסקים אחד. במרבית המקרים הסים החדש מופעל תוך שעות ספורות מרגע ההצטרפות.</p>
    </div>
  </div>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">איזו חברת סלולר יש לה קליטה הכי טובה?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">אין תשובה אחת לכולם — כל חברה מכסה אזורים שונים בצורה שונה. פלאפון, סלקום ופרטנר הן החברות הגדולות עם רשתות עצמאיות. הוט מובייל חולקת רשת עם פרטנר. השאר פרטים ואנחנו נבדוק עבורך מי מכסה הכי טוב בדיוק באזור שלך.</p>
    </div>
  </div>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">מה קורה לחוזה הישן שלי כשאני עובר?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">אם אתה בחוזה מחייב, ייתכן קנס יציאה. אם אתה על חבילה חודשית מתגלגלת — אפשר לעזוב בכל עת ללא קנס. נבדוק את המצב שלך ונמצא את הדרך הטובה ביותר לעבור.</p>
    </div>
  </div>

  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">האם השירות שלכם עולה כסף?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">לא. הייעוץ והעזרה במעבר הם חינמיים לחלוטין. השאר פרטים ואנחנו נחזור אליך.</p>
    </div>
  </div>

</section>
```

---

## שלב 4 — סקשן "למה אנחנו ולא השוואת מחירים"

הוסף סקשן חדש שמדגיש את היתרון הייחודי:

```html
<section>
  <h2>למה לא פשוט לחפש בגוגל לבד?</h2>
  <p>אפשר. אבל אתרי השוואה נותנים לך טבלה — ואתה צריך להבין אותה לבד.</p>
  <p>אנחנו שונים:</p>
  <ul>
    <li>✓ בודקים עבורך מי מכסה את האזור שלך</li>
    <li>✓ מסבירים בשפה פשוטה מה האפשרויות שלך</li>
    <li>✓ עוזרים בכל תהליך המעבר מא' עד ת'</li>
    <li>✓ חינם לגמרי — בלי עמלות נסתרות</li>
  </ul>
</section>
```

---

## שלב 5 — שיפור טופס הליד

### כותרת הטופס — לשנות ל:
```
ספר לנו איפה הקליטה גרועה — נחזור אליך תוך שעה עם פתרון
```

### שדות הטופס — לוודא שיש:
```html
<form id="lead-form">
  <h2>ספר לנו איפה הקליטה גרועה — נחזור אליך תוך שעה עם פתרון</h2>

  <label for="location">באיזה אזור אתה גר / עובד?</label>
  <input type="text" id="location" name="location" placeholder="לדוגמה: רמת השרון, קומה 3 בבניין בטון">

  <label for="problem">מה הבעיה הכי מציקה לך?</label>
  <textarea id="problem" name="problem" placeholder="לדוגמה: בבית אין לי בכלל קליטה, בעבודה הקליטה נופלת כל הזמן..."></textarea>

  <label for="current-company">באיזו חברה אתה היום?</label>
  <select id="current-company" name="current-company">
    <option value="">בחר חברה...</option>
    <option>פלאפון</option>
    <option>סלקום</option>
    <option>פרטנר / אורנג'</option>
    <option>הוט מובייל</option>
    <option>גולן טלקום</option>
    <option>רמי לוי</option>
    <option>אחר</option>
  </select>

  <label for="name">שם פרטי</label>
  <input type="text" id="name" name="name" required placeholder="השם שלך">

  <label for="phone">טלפון לחזרה</label>
  <input type="tel" id="phone" name="phone" required placeholder="05X-XXXXXXX">

  <button type="submit">שלח — נחזור אליך בחינם תוך שעה ✓</button>
</form>
```

### הודעת תודה אחרי שליחה — לוודא שמופיעה:
```html
<div id="thank-you" style="display:none">
  <h2>קיבלנו! 🎉</h2>
  <p>ניצור איתך קשר תוך שעה לכל היותר עם הפתרון המתאים לך.</p>
</div>
```

---

## שלב 6 — כפתור טלפון לחיץ למובייל

וודא שמספר הטלפון מופיע כקישור לחיץ:
```html
<a href="tel:05XXXXXXXX" style="font-size:1.5rem; font-weight:bold;">
  📞 התקשר עכשיו: 05X-XXXXXXX
</a>
```

---

## שלב 7 — מילות מפתח לשלב בטקסט באופן טבעי

לאורך כל הדף, לוודא שמופיעות המילים הבאות (לפחות פעם אחת כל אחת):
- קליטה גרועה
- קליטה סלולרית
- לעבור חברת סלולר
- מעבר חברת סלולר
- קליטה בבית
- ניוד מספר
- פלאפון קליטה
- סלקום קליטה
- פרטנר קליטה
- קליטה באזור שלי

---

## סדר ביצוע מומלץ

| עדיפות | משימה |
|--------|--------|
| 🔴 1 | החלף H1 למסר החדש |
| 🔴 2 | הוסף סקשן "למה הקליטה גרועה" |
| 🔴 3 | הוסף FAQ מלא עם Schema |
| 🟠 4 | שפר טופס הליד (שדות + כותרת) |
| 🟠 5 | הוסף סקשן "למה אנחנו" |
| 🟡 6 | הוסף כפתור טלפון לחיץ |
| 🟡 7 | בדוק פיזור מילות מפתח בטקסט |
