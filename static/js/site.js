/* ForgeIEC site script: theme toggle, mobile menu, submenu on touch.
   No dependencies, no tracking, no network requests. */
(function () {
  'use strict';
  var root = document.documentElement;
  var KEY = 'forgeiec-theme';

  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t === 'light' || t === 'dark') return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* storage blocked: choice lasts for this page */ }
      document.dispatchEvent(new CustomEvent('forgeiec:theme', { detail: next }));
    });
  }

  var header = document.querySelector('.site-header');
  var menuBtn = document.querySelector('.menu-toggle');
  if (header && menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('nav-open')) {
        header.classList.remove('nav-open');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.focus();
      }
    });
  }

  // Submenu buttons: click toggles (touch devices), Escape closes.
  var subs = document.querySelectorAll('.has-sub > .nav-link[aria-expanded]');
  Array.prototype.forEach.call(subs, function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentNode;
      var open = li.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(document.querySelectorAll('.has-sub.is-open'), function (li) {
      if (!li.contains(e.target)) {
        li.classList.remove('is-open');
        var b = li.querySelector('.nav-link[aria-expanded]');
        if (b) b.setAttribute('aria-expanded', 'false');
      }
    });
  });
})();
