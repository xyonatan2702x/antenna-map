/* אין קליטה — שאלון לידים קצר (3 שאלות + פרטים).
   שימוש:
   - בתוך העמוד: <div data-lead-quiz data-city="חיפה" data-rec="pelephone"></div>
   - כחלון: LeadQuiz.open({ city: 'חיפה', rec: 'pelephone' })
   rec = הרשת עם האתר הקרוב / הכי הרבה אתרים (partner | pelephone | cellcom), לא חובה.
   הנתונים נשלחים ל-n8n (בדיקה, שמירה והתראה בטלגרם) ולגיליון Google. */
(function () {
  'use strict';
  var LEADS_URL = 'https://n8n.49-13-155-101.sslip.io/webhook/leads-intake';
  var EVENTS_URL = 'https://n8n.49-13-155-101.sslip.io/webhook/site-event';
  var SHEETS_URL = 'https://script.google.com/macros/s/AKfycbwnIUxUEHhYwqfFfY4tzBSu95sTen0qvdSfV_vXL5sr5OF0UpjQ_D7Wq1nhuC0ZJZzB/exec';
  var ROOT = (function () {
    var s = document.currentScript && document.currentScript.getAttribute('src') || '';
    return s.replace(/quiz\.js.*$/, '');
  })();
  var NET = { partner: 'פרטנר והוט מובייל', pelephone: 'פלאפון', cellcom: 'סלקום' };

  var STEPS = [
    { key: 'problem', q: 'מה הכי מפריע לך היום?', opts: [
      ['no_signal', 'אין קליטה טובה בבית או בעבודה'],
      ['expensive', 'משלם יותר מדי על הסלולר'],
      ['both', 'גם וגם'],
      ['check', 'רוצה לבדוק לפני שאני עובר חברה']] },
    { key: 'lines', q: 'כמה קווים יש לכם בבית?', opts: [['1', 'קו אחד'], ['2', '2 קווים'], ['3-4', '3–4 קווים'], ['5+', '5 קווים ומעלה']] },
    { key: 'company', q: 'באיזו חברה אתם היום?', opts: [
      ['partner', 'פרטנר / הוט מובייל / 012 / 019'], ['pelephone', 'פלאפון / רמי לוי'],
      ['cellcom', 'סלקום / גולן / wecom'], ['other', 'אחרת / לא בטוח']] },
  ];

  function css() {
    if (document.getElementById('lq-css')) return;
    var s = document.createElement('style');
    s.id = 'lq-css';
    s.textContent = [
      '.lq,.lq *{box-sizing:border-box}',
      '.lq{background:#fff;border:1px solid #e3e9f0;border-radius:16px;padding:20px 18px;max-width:460px;margin:0 auto;text-align:right;font-family:inherit;box-shadow:0 4px 18px rgba(0,0,0,.05)}',
      '.lq h3{font-size:1.1rem;font-weight:700;color:#1a1a2e;margin:0 0 4px}',
      '.lq .lq-sub{font-size:.86rem;color:#667;margin:0 0 14px;line-height:1.6}',
      '.lq .lq-bar{height:5px;background:#e8edf3;border-radius:6px;overflow:hidden;margin-bottom:14px}',
      '.lq .lq-bar i{display:block;height:100%;background:#00B4CC;transition:width .25s}',
      '.lq .lq-q{font-size:.98rem;font-weight:600;color:#1a1a2e;margin-bottom:10px}',
      '.lq .lq-opt{display:block;width:100%;text-align:right;background:#f7f9fc;border:1.5px solid #e3e9f0;border-radius:11px;padding:12px 14px;margin-bottom:8px;font:inherit;font-size:.95rem;color:#222;cursor:pointer}',
      '.lq .lq-opt:hover,.lq .lq-opt:focus{border-color:#00B4CC;background:#f0fbfd;outline:none}',
      '.lq label{display:block;font-size:.84rem;font-weight:600;color:#333;margin:8px 0 4px}',
      '.lq input[type=text],.lq input[type=tel]{width:100%;box-sizing:border-box;padding:11px 12px;border:1.5px solid #dfe6ee;border-radius:10px;font:inherit;font-size:1rem}',
      '.lq .lq-consent{display:flex;gap:8px;align-items:flex-start;font-size:.74rem;font-weight:400;color:#666;line-height:1.5;margin:10px 0}',
      '.lq .lq-consent input{margin-top:3px;flex:0 0 auto}',
      '.lq .lq-go{display:block;width:100%;background:#00B4CC;color:#fff;border:0;border-radius:11px;padding:13px;font:inherit;font-size:1.02rem;font-weight:700;cursor:pointer}',
      '.lq .lq-go:disabled{opacity:.6}',
      '.lq .lq-back{background:none;border:0;color:#667;font:inherit;font-size:.82rem;cursor:pointer;padding:6px 0;margin-top:4px}',
      '.lq .lq-err{color:#b42318;font-size:.84rem;margin:6px 0 0}',
      '.lq .lq-trust{font-size:.75rem;color:#889;text-align:center;margin:10px 0 0}',
      '.lq .lq-rec{background:#f0fbfd;border:1px solid #c9eef4;border-radius:10px;padding:9px 12px;font-size:.86rem;color:#1a1a2e;margin-bottom:12px}',
      '.lq{position:relative}',
      '.lq input.lq-hp{position:absolute!important;top:0;right:0;width:1px!important;height:1px!important;padding:0!important;border:0!important;margin:0!important;opacity:0;pointer-events:none;clip:rect(0 0 0 0);clip-path:inset(50%);overflow:hidden}',
      '.lq-ov{position:fixed;inset:0;background:rgba(20,25,40,.55);z-index:10000;display:flex;align-items:center;justify-content:center;padding:14px}',
      '.lq-ov .lq-card{position:relative;width:100%;max-width:460px}',
      '.lq-ov .lq{max-height:calc(100vh - 28px);overflow:auto}',
      '.lq-ov .lq-x{position:absolute;top:8px;left:10px;z-index:1;background:none;border:0;font-size:1.5rem;color:#889;cursor:pointer;line-height:1;padding:4px 8px}',
      '[hidden]{display:none!important}'
    ].join('');
    document.head.appendChild(s);
  }

  function track(type) {
    try {
      var ref = '';
      try { ref = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) {}
      if (ref === location.hostname) ref = '';
      var body = new URLSearchParams({ source: 'antenna-map', type: type, page: window.PAGE || location.pathname, ref: ref,
        device: matchMedia('(max-width: 768px)').matches ? 'mobile' : 'desktop' });
      fetch(EVENTS_URL, { method: 'POST', mode: 'no-cors', body: body, keepalive: true }).catch(function () {});
    } catch (e) {}
  }

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function build(host, opts) {
    opts = opts || {};
    var ans = {}, step = 0, started = false;
    var city = opts.city || '';
    var rec = NET[opts.rec] ? opts.rec : '';
    var el = document.createElement('div');
    el.className = 'lq';
    host.appendChild(el);

    function bar(i) { return '<div class="lq-bar" aria-hidden="true"><i style="width:' + Math.round(i / (STEPS.length + 1) * 100) + '%"></i></div>'; }
    function head() {
      return '<h3>' + esc(opts.title || 'רוצה הצעה לחבילה ברשת שקולטת אצלך?') + '</h3>' +
        '<p class="lq-sub">3 שאלות קצרות, ויחזרו אליך עם הצעה מתאימה. בלי עלות ובלי התחייבות.</p>';
    }
    function renderStep() {
      var s = STEPS[step];
      var html = (step === 0 ? head() : '') + bar(step) + '<div class="lq-q" id="lq-q-' + step + '">' + esc(s.q) + '</div><div role="group" aria-labelledby="lq-q-' + step + '">';
      s.opts.forEach(function (o) { html += '<button type="button" class="lq-opt" data-v="' + esc(o[0]) + '">' + esc(o[1]) + '</button>'; });
      html += '</div>' + (step > 0 ? '<button type="button" class="lq-back">→ חזרה</button>' : '');
      el.innerHTML = html;
      Array.prototype.forEach.call(el.querySelectorAll('.lq-opt'), function (b) {
        b.addEventListener('click', function () {
          if (!started) { started = true; track('form_open'); }
          ans[s.key] = b.getAttribute('data-v');
          step++;
          step < STEPS.length ? renderStep() : renderDetails();
        });
      });
      var back = el.querySelector('.lq-back');
      if (back) back.addEventListener('click', function () { step--; renderStep(); });
    }
    function renderDetails() {
      var recTxt = rec ? '<div class="lq-rec">לפי המפה, הרשת שבולטת ' + (city ? 'ב' + esc(city) : 'אצלך') + ' היא <strong>' + esc(NET[rec]) + '</strong>. נבקש הצעה ברשת הזו.</div>' : '';
      var u = 'lq' + Math.random().toString(36).slice(2, 7);
      el.innerHTML = bar(STEPS.length) + recTxt +
        '<div class="lq-q">לאן לשלוח את ההצעה?</div>' +
        '<form novalidate>' +
        '<label for="' + u + 'n">שם</label><input type="text" id="' + u + 'n" autocomplete="name" maxlength="80" />' +
        '<label for="' + u + 'p">טלפון</label><input type="tel" id="' + u + 'p" autocomplete="tel" dir="ltr" placeholder="050-0000000" maxlength="20" />' +
        '<label for="' + u + 'c">עיר / שכונה</label><input type="text" id="' + u + 'c" maxlength="120" value="' + esc(city) + '" />' +
        '<input type="text" class="lq-hp" tabindex="-1" autocomplete="off" aria-hidden="true" />' +
        '<label class="lq-consent"><input type="checkbox" /> <span>אני מאשר/ת שפרטיי יועברו לספקי שירות, למשווקים מורשים או לאתרי השוואה בתחום הסלולר, שיחזרו אליי בטלפון, בוואטסאפ או בהודעה, וקראתי את <a href="' + ROOT + 'privacy.html" target="_blank" rel="noopener">מדיניות הפרטיות</a> ואת <a href="' + ROOT + 'terms.html" target="_blank" rel="noopener">תנאי השימוש</a></span></label>' +
        '<p class="lq-err" role="alert" hidden></p>' +
        '<button type="submit" class="lq-go">שלחו לי הצעה ✓</button>' +
        '<p class="lq-trust">🔒 בלי ספאם. אפשר לבקש מחיקה של הפרטים בכל עת.</p>' +
        '</form><button type="button" class="lq-back">→ חזרה</button>';
      var f = el.querySelector('form'), err = el.querySelector('.lq-err');
      el.querySelector('.lq-back').addEventListener('click', function () { step = STEPS.length - 1; renderStep(); });
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var name = f.querySelector('#' + u + 'n').value.trim();
        var phone = f.querySelector('#' + u + 'p').value.trim();
        var loc = f.querySelector('#' + u + 'c').value.trim();
        var ok = f.querySelector('.lq-consent input').checked;
        var digits = phone.replace(/\D/g, '').replace(/^972/, '0');
        var msg = '';
        if (name.length < 2) msg = 'נא לכתוב שם.';
        else if (!/^0(5\d{8}|7\d{8}|[23489]\d{7})$/.test(digits)) msg = 'נא לבדוק את מספר הטלפון.';
        else if (!ok) msg = 'כדי שנוכל לשלוח לך הצעה, יש לאשר את העברת הפרטים.';
        if (msg) { err.textContent = msg; err.hidden = false; return; }
        err.hidden = true;
        f.querySelector('.lq-go').disabled = true;
        var lead = { source: 'antenna-map', name: name, phone: phone, location: loc, company: ans.company === 'other' ? '' : ans.company,
          consent: 'yes', problem: ans.problem, lines: ans.lines, recommended: rec, page_url: location.href,
          website: f.querySelector('.lq-hp').value };
        try { fetch(LEADS_URL, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(lead), keepalive: true }).catch(function () {}); } catch (x) {}
        try { fetch(SHEETS_URL, { method: 'POST', mode: 'no-cors', body: JSON.stringify(lead) }).catch(function () {}); } catch (x) {}
        track('form_submit');
        el.innerHTML = '<div style="text-align:center;padding:10px 0"><div style="font-size:2rem">🎉</div><h3>קיבלנו, תודה ' + esc(name) + '!</h3>' +
          '<p class="lq-sub" style="margin:6px 0 0">יחזרו אליך בהקדם עם הצעה' + (rec ? ' ברשת ' + esc(NET[rec]) : '') + '.<br/>בינתיים אפשר לקרוא <a href="' + ROOT + 'guide/' + encodeURIComponent('ניוד-מספר-סלולרי') + '.html">איך עובר ניוד מספר</a>.</p></div>';
        if (opts.onDone) opts.onDone();
      });
      var first = f.querySelector('#' + u + 'n'); if (first && opts.focus !== false) try { first.focus({ preventScroll: false }); } catch (x) {}
    }
    renderStep();
    return el;
  }

  function open(opts) {
    css();
    var ov = document.createElement('div');
    ov.className = 'lq-ov';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-modal', 'true');
    ov.setAttribute('aria-label', 'קבלת הצעה');
    document.body.appendChild(ov);
    var card = document.createElement('div');
    card.className = 'lq-card';
    ov.appendChild(card);
    // the close button sits outside the quiz box, so it stays when the steps re-render
    var x = document.createElement('button');
    x.className = 'lq-x'; x.type = 'button'; x.setAttribute('aria-label', 'סגירה'); x.textContent = '×';
    card.appendChild(x);
    var box = build(card, opts);
    function close() { ov.remove(); document.removeEventListener('keydown', onKey); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    x.addEventListener('click', close);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    document.addEventListener('keydown', onKey);
    var firstOpt = box.querySelector('.lq-opt'); if (firstOpt) firstOpt.focus();
  }

  function init() {
    css();
    Array.prototype.forEach.call(document.querySelectorAll('[data-lead-quiz]'), function (h) {
      if (h.getAttribute('data-ready')) return;
      h.setAttribute('data-ready', '1');
      build(h, { city: h.getAttribute('data-city') || '', rec: h.getAttribute('data-rec') || '', title: h.getAttribute('data-title') || '', focus: false });
    });
  }
  window.LeadQuiz = { open: open, init: init, NET: NET };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
