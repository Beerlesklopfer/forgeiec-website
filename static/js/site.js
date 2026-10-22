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

  // Forge sound: off by default. The synthesis script is loaded only when
  // the visitor has switched it on (stored flag) or switches it on now.
  var SOUND_KEY = 'forgeiec-sound';
  var soundBtn = document.querySelector('.sound-toggle');
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isBot = navigator.webdriver === true;
  function soundStored() {
    try { return localStorage.getItem(SOUND_KEY) === 'on'; } catch (e) { return false; }
  }
  var soundOn = soundStored();
  function loadSound(cb) {
    if (window.ForgeAnvil) { cb(); return; }
    var s = document.createElement('script');
    s.src = soundBtn.getAttribute('data-src');
    s.onload = cb;
    document.head.appendChild(s);
  }
  if (soundBtn) {
    soundBtn.setAttribute('aria-pressed', soundOn ? 'true' : 'false');
    soundBtn.addEventListener('click', function () {
      soundOn = !soundOn;
      soundBtn.setAttribute('aria-pressed', soundOn ? 'true' : 'false');
      try { localStorage.setItem(SOUND_KEY, soundOn ? 'on' : 'off'); } catch (e) { /* storage blocked: lasts for this page */ }
      if (soundOn) loadSound(function () { window.ForgeAnvil.play(); });
    });
    // Autoplay after load only when stored on, not for reduced motion, not for automation.
    if (soundOn && !reduced && !isBot) {
      window.addEventListener('load', function () {
        loadSound(function () { if (soundOn) window.ForgeAnvil.play(); });
      });
    }
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
