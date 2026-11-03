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
