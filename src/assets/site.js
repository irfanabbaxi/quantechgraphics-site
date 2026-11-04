// Mobile nav toggle
(function () {
  var btn = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'CLOSE' : 'MENU';
    });
  }

  // Forms are not wired to a backend yet. Each form has data-endpoint; when it is
  // empty we show a message instead of sending. To go live, set data-endpoint to a
  // form service URL (e.g. Formspree or Buttondown) in build.py.
  document.querySelectorAll('form[data-endpoint]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.form-msg');
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) {
        if (msg) msg.textContent = form.getAttribute('data-offline-msg') || 'Sign-ups open at launch.';
        return;
      }
      var data = new FormData(form);
      fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('bad status');
          form.reset();
          if (msg) msg.textContent = form.getAttribute('data-ok-msg') || 'Received. We will be in touch.';
        })
        .catch(function () {
          if (msg) msg.textContent = 'That did not go through. Email info@quantechgraphics.com instead.';
        });
    });
  });

  // Links that are not live yet
  document.querySelectorAll('[aria-disabled="true"]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); });
  });
})();

// Preview-only theme switcher
(function () {
  var root = document.documentElement;
  var btns = document.querySelectorAll('[data-skin-btn]');
  if (!btns.length) return;
  function set(skin) {
    if (skin === 'ops') root.removeAttribute('data-skin'); else root.setAttribute('data-skin', skin);
    btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-skin-btn') === skin ? 'true' : 'false'); });
    try { localStorage.setItem('qg-skin', skin); } catch (e) {}
  }
  btns.forEach(function (b) { b.addEventListener('click', function () { set(b.getAttribute('data-skin-btn')); }); });
  set(root.getAttribute('data-skin') || 'ops');
})();

// Animated logo: header pulse + first-visit intro (assets/brand/quantech-logo.js)
(function () {
  if (!window.QuantechLogo) { if (window.console) console.info('[QG logo] animation script not loaded'); return; } // static logo stays
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var KEY = 'qg-logo-intro-seen';

  var holder = document.querySelector('[data-logo-anim]');
  if (holder) {
    holder.innerHTML = '';
    QuantechLogo.mount(holder, { intro: 'never', idle: true, idleEvery: 9000, wordmark: false });
  }

  var mode = window.QG_INTRO || 'first-visit';
  var seen = false;
  try { seen = localStorage.getItem(KEY) === '1'; } catch (e) {}
  var force = location.hash === '#intro', reducedSetting = reduced;
  if (force) { seen = false; reduced = false; } // test hook: quantechgraphics.com/#intro replays the intro
  if (window.console) console.info('[QG logo] v3', { reduceMotionSetting: reducedSetting, forced: force, introAlreadySeen: seen, mode: mode });
  if (reduced || mode === 'never' || (mode === 'first-visit' && seen)) return;
  try { localStorage.setItem(KEY, '1'); } catch (e) {}

  var overlay = document.createElement('div');
  overlay.className = 'qg-intro';
  overlay.innerHTML = '<div class="qg-intro-logo"></div><button type="button" class="qg-intro-skip">Skip intro</button>';
  document.body.appendChild(overlay);
  var done = false, logo;
  function finish() {
    if (done) return; done = true;
    overlay.classList.add('out');
    setTimeout(function () { if (logo) logo.destroy(); overlay.remove(); }, 500);
  }
  logo = QuantechLogo.mount(overlay.querySelector('.qg-intro-logo'), {
    intro: 'always', idle: false, hoverPulse: false, ignoreReducedMotion: force, storageKey: KEY, wordmarkLines: 2,
    onIntroEnd: function () { setTimeout(finish, 450); }
  });
  overlay.querySelector('.qg-intro-skip').addEventListener('click', finish);
  if (location.hash === '#intro') { // diagnostics for browsers where the intro doesn't show
    [300, 1500, 3000].forEach(function (t) {
      setTimeout(function () {
        try {
          var sv = overlay.querySelector('svg'), r = sv ? sv.getBoundingClientRect() : null;
          var an = document.getAnimations ? document.getAnimations() : [];
          var run = an.filter(function (a) { return a.playState === 'running'; }).length;
          var poly = sv && sv.querySelector('polygon'), cs = poly ? getComputedStyle(poly) : null;
          console.info('[QG logo] t=' + t, { svg: r ? Math.round(r.width) + 'x' + Math.round(r.height) : 'none', anims: an.length, running: run,
            firstTime: an[0] ? Math.round(an[0].currentTime) : null, timeline: document.timeline ? Math.round(document.timeline.currentTime) : null,
            shardOpacity: cs ? cs.opacity : null, shardFill: cs ? cs.fill : null });
        } catch (e) { console.info('[QG logo] diag error', String(e)); }
      }, t);
    });
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') finish(); });
  setTimeout(finish, 6500); // safety net
})();

// Header: tall on load, compact once the page scrolls
(function () {
  var h = document.querySelector('.site-header');
  if (!h) return;
  function upd() { h.classList.toggle('compact', window.scrollY > 40); }
  window.addEventListener('scroll', upd, { passive: true });
  upd();
})();
