// Shared script for the city pages: small map, lead form and anonymous counters.
(function(){
  var CONFIG={
    SHEETS_URL:'https://script.google.com/macros/s/AKfycbwnIUxUEHhYwqfFfY4tzBSu95sTen0qvdSfV_vXL5sr5OF0UpjQ_D7Wq1nhuC0ZJZzB/exec',
    LEADS_WEBHOOK_URL:'https://n8n.49-13-155-101.sslip.io/webhook/leads-intake',
    EVENTS_URL:'https://n8n.49-13-155-101.sslip.io/webhook/site-event',
    LEADS_SOURCE:'antenna-map'
  };
  var NAMES={partner:'פרטנר והוט מובייל',pelephone:'פלאפון',cellcom:'סלקום'};
  var COLORS={partner:'#008a9c',pelephone:'#0057A8',cellcom:'#9C27B0'};
  var city=window.CITY||null;
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}

  function track(type){
    try{
      var ref='';
      try{ref=document.referrer?new URL(document.referrer).hostname:''}catch(e){}
      if(ref===location.hostname)ref='';
      var body=new URLSearchParams({source:CONFIG.LEADS_SOURCE,type:type,
        page:city?'/city/'+city.name:(window.PAGE||'/city/'),ref:ref,
        device:window.matchMedia('(max-width: 768px)').matches?'mobile':'desktop'});
      fetch(CONFIG.EVENTS_URL,{method:'POST',mode:'no-cors',body:body,keepalive:true}).catch(function(){});
    }catch(e){}
  }
  track('view');

  function initMap(){
    if(!city||!window.L||!document.getElementById('map'))return;
    var map=L.map('map',{scrollWheelZoom:false}).setView(city.center,13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,
      attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
    var pts=[];
    city.sites.forEach(function(s){
      L.circleMarker([s[0],s[1]],{radius:7,color:'#fff',weight:2,fillColor:COLORS[s[2]]||'#666',fillOpacity:.95})
        .bindPopup('<strong>'+esc(s[3])+'</strong><br>'+esc(NAMES[s[2]]||s[2])+(s[4]?'<br>דור '+esc(s[4]):''))
        .addTo(map);
      pts.push([s[0],s[1]]);
    });
    if(pts.length>1)map.fitBounds(pts,{padding:[24,24],maxZoom:15});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initMap);else initMap();

  var form=document.getElementById('city-form');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    var v=function(id){var el=document.getElementById(id);return el?el.value.trim():''};
    var name=v('cf-name'),phone=v('cf-phone'),loc=v('cf-loc');
    if(!name||!phone||!document.getElementById('cf-consent').checked)return;
    var where=(city?city.name:'')+(loc?', '+loc:'');
    var now=new Date();
    var lead={name:name,phone:phone,location:where,company:'',consent:'yes',
      date:now.toLocaleDateString('he-IL'),time:now.toLocaleTimeString('he-IL',{hour:'2-digit',minute:'2-digit'})};
    try{fetch(CONFIG.SHEETS_URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(lead)}).catch(function(){})}catch(err){}
    try{
      var body=new URLSearchParams({source:CONFIG.LEADS_SOURCE,name:name,phone:phone,location:where,company:'',
        consent:'yes',page_url:location.href,website:v('cf-website')});
      fetch(CONFIG.LEADS_WEBHOOK_URL,{method:'POST',mode:'no-cors',body:body,keepalive:true}).catch(function(){});
    }catch(err){}
    track('form_submit');
    form.hidden=true;
    document.getElementById('city-thanks').hidden=false;
  });
})();
