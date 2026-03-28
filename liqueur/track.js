// Terroir HUB LIQUEUR — Behavior Tracking Layer v2
// 全イベントをSupabaseに送信 + localStorageにバックアップ

(function(){
  'use strict';

  const HUB_VERSION = '2.0';
  const STORAGE_KEY = 'thub_events';
  const SESSION_KEY = 'thub_session';
  const USER_KEY = 'thub_uid';
  const QUEUE_KEY = 'thub_queue';

  const SB_URL = 'https://hhwavxavuqqfiehrogwv.supabase.co';
  const SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhod2F2eGF2dXFxZmllaHJvZ3d2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5Njk3MzAsImV4cCI6MjA4OTU0NTczMH0.tHMQ_u51jp69AMUKKtTvxL09Sr11JFPKGRhKMmUzEjg';

  function getSession(){
    let s = sessionStorage.getItem(SESSION_KEY);
    if(!s){ s = 'ses_' + Date.now() + '_' + Math.random().toString(36).substr(2,6); sessionStorage.setItem(SESSION_KEY, s); }
    return s;
  }

  function getUser(){
    let u = localStorage.getItem(USER_KEY);
    if(!u){ u = 'anon_' + Date.now() + '_' + Math.random().toString(36).substr(2,8); localStorage.setItem(USER_KEY, u); }
    return u;
  }

  function getDevice(){
    const w = window.innerWidth;
    if(w <= 640) return 'mobile';
    if(w <= 1024) return 'tablet';
    return 'desktop';
  }

  function getLang(){
    return (navigator.language || navigator.userLanguage || 'unknown').substring(0,5);
  }

  function getProducerFromURL(){
    const m = window.location.pathname.match(/\/liqueur\/([a-z]+)\/([a-z0-9_]+)\.html/);
    if(m) return { pref: m[1], brewery_id: m[2] };
    return null;
  }

  function track(event, properties){
    const producer = getProducerFromURL();
    const payload = {
      event: event,
      properties: properties || {},
      timestamp: new Date().toISOString(),
      session_id: getSession(),
      user_id: getUser(),
      page: window.location.pathname,
      referrer: document.referrer,
      device: getDevice(),
      lang: getLang(),
      screen: window.innerWidth + 'x' + window.innerHeight,
      brewery_id: (properties && properties.brewery_id) || (producer && producer.brewery_id) || null,
      pref: (properties && properties.pref) || (producer && producer.pref) || null,
      country: userCountry,
      city: userCity,
      timezone: userTimezone,
      v: HUB_VERSION
    };

    try {
      const events = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      events.push(payload);
      if(events.length > 2000) events.splice(0, events.length - 2000);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(events));
    } catch(e){}

    sendToSupabase(payload);

    if(location.hostname === 'localhost' || location.protocol === 'file:'){
      console.log('[THUB]', event, properties);
    }
  }

  function sendToSupabase(payload){
    const row = {
      event: payload.event, properties: payload.properties, timestamp: payload.timestamp,
      session_id: payload.session_id, user_id: payload.user_id, page: payload.page,
      referrer: payload.referrer, device: payload.device, lang: payload.lang,
      screen: payload.screen, brewery_id: payload.brewery_id, pref: payload.pref,
      country: payload.country, city: payload.city, timezone: payload.timezone
    };

    fetch(SB_URL + '/rest/v1/analytics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'apikey': SB_KEY, 'Authorization': 'Bearer ' + SB_KEY, 'Prefer': 'return=minimal' },
      body: JSON.stringify(row)
    }).catch(function(){
      try {
        const q = JSON.parse(localStorage.getItem(QUEUE_KEY) || '[]');
        q.push(row);
        if(q.length > 500) q.splice(0, q.length - 500);
        localStorage.setItem(QUEUE_KEY, JSON.stringify(q));
      } catch(e){}
    });
  }

  function flushQueue(){
    try {
      const q = JSON.parse(localStorage.getItem(QUEUE_KEY) || '[]');
      if(q.length === 0) return;
      const batch = q.splice(0, 50);
      localStorage.setItem(QUEUE_KEY, JSON.stringify(q));
      fetch(SB_URL + '/rest/v1/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'apikey': SB_KEY, 'Authorization': 'Bearer ' + SB_KEY, 'Prefer': 'return=minimal' },
        body: JSON.stringify(batch)
      }).then(function(){ if(q.length > 0) setTimeout(flushQueue, 1000); });
    } catch(e){}
  }
  window.addEventListener('online', flushQueue);
  setTimeout(flushQueue, 5000);

  var userCountry = sessionStorage.getItem('thub_country') || null;
  var userCity = sessionStorage.getItem('thub_city') || null;
  var userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone || null;

  if(!userCountry){
    fetch('https://ipapi.co/json/', { mode: 'cors' }).then(function(r){ return r.json(); }).then(function(d){
      userCountry = d.country_code || null;
      userCity = d.city || null;
      sessionStorage.setItem('thub_country', userCountry || '');
      sessionStorage.setItem('thub_city', userCity || '');
      track('geo_detected', { country: userCountry, city: userCity, region: d.region, timezone: userTimezone });
    }).catch(function(){});
  }

  var producerInfo = getProducerFromURL();
  track('page_view', {
    title: document.title, path: window.location.pathname, query: window.location.search,
    brewery_id: producerInfo ? producerInfo.brewery_id : null,
    pref: producerInfo ? producerInfo.pref : null
  });

  var pageStart = Date.now();
  window.addEventListener('beforeunload', function(){
    track('page_exit', { duration_ms: Date.now() - pageStart, brewery_id: producerInfo ? producerInfo.brewery_id : null });
  });

  var maxScroll = 0;
  window.addEventListener('scroll', function(){
    var pct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
    if(pct > maxScroll) maxScroll = pct;
  });
  window.addEventListener('beforeunload', function(){
    if(maxScroll > 0) track('scroll_depth', { max_percent: maxScroll });
  });

  window.thub = {
    track: track,
    search: function(query, results_count){ track('search', { query: query, results: results_count }); },
    ai_query: function(query, response_preview, brewery_context){ track('ai_query', { query: query, response_preview: (response_preview||'').substring(0,200), brewery_context: brewery_context || null }); },
    favorite: function(brewery_id, brewery_name, pref){ track('favorite', { brewery_id: brewery_id, brewery_name: brewery_name, pref: pref }); },
    share: function(brewery_id, method){ track('share', { brewery_id: brewery_id, method: method }); },
    signup: function(method){ track('signup', { method: method || 'email' }); },
    login: function(method){ track('login', { method: method || 'email' }); },
    sakura_open: function(brewery_id){ track('sakura_open', { brewery_id: brewery_id }); },
    lang_switch: function(lang){ track('lang_switch', { lang: lang }); },
    addHistory: function(breweryId, breweryName, pref){
      var key = 'thub_history';
      var history = JSON.parse(localStorage.getItem(key) || '[]');
      history = history.filter(function(h){ return h.id !== breweryId; });
      history.unshift({ id: breweryId, name: breweryName, pref: pref, time: new Date().toISOString() });
      if(history.length > 50) history = history.slice(0, 50);
      localStorage.setItem(key, JSON.stringify(history));
      track('brewery_view', { brewery_id: breweryId, brewery_name: breweryName, pref: pref });
    },
    getHistory: function(){ return JSON.parse(localStorage.getItem('thub_history') || '[]'); },
    setUser: function(userId){ localStorage.setItem(USER_KEY, userId); track('identify', { user_id: userId }); }
  };

  document.addEventListener('click', function(e){
    var el = e.target.closest('a, button, [data-track]');
    if(!el) return;
    if(el.tagName === 'A' && el.hostname && el.hostname !== location.hostname){
      track('outbound_click', { url: el.href, text: el.textContent.trim().substring(0,50) });
    }
    if(el.dataset && el.dataset.track){
      track(el.dataset.track, { label: el.dataset.trackLabel || el.textContent.trim().substring(0,50) });
    }
    if(el.id === 'fab' || el.classList.contains('btn-p')){
      var bi = getProducerFromURL();
      if(bi) track('sakura_open', { brewery_id: bi.brewery_id });
    }
    if(el.classList.contains('sug')){
      track('sakura_suggestion_click', { suggestion: el.textContent.trim() });
    }
  });

  if(producerInfo){
    window.thub.addHistory(producerInfo.brewery_id, document.title.split(' — ')[0], producerInfo.pref);
  }

  (function(){
    var params = new URLSearchParams(window.location.search);
    var utm_source = params.get('utm_source');
    if(utm_source){
      track('utm_landing', { utm_source: utm_source, utm_medium: params.get('utm_medium') || '', utm_campaign: params.get('utm_campaign') || '' });
      sessionStorage.setItem('thub_utm', JSON.stringify({ source: utm_source, medium: params.get('utm_medium'), campaign: params.get('utm_campaign') }));
    }
  })();

  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window,document,"clarity","script","w00ia7v4xp");

})();
