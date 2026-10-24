/* Renders ```mermaid blocks with the self-hosted Mermaid build.
   Re-renders when the theme changes so text stays legible. */
(function () {
  'use strict';
  if (!window.mermaid) return;
  var blocks = Array.prototype.slice.call(document.querySelectorAll('pre.mermaid'));
  blocks.forEach(function (b) { b.setAttribute('data-src', b.textContent); });

  function isDark() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function render() {
    var dark = isDark();
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      theme: 'base',
      fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
      themeVariables: dark ? {
        background: '#151b23', primaryColor: '#1b232d', primaryTextColor: '#e5e9ee',
        primaryBorderColor: '#7d8896', lineColor: '#9aa4b1', secondaryColor: '#3a2a0c',
        tertiaryColor: '#151b23', textColor: '#e5e9ee', mainBkg: '#1b232d', clusterBkg: '#121820',
        clusterBorder: '#3a4552', edgeLabelBackground: '#151b23', nodeTextColor: '#e5e9ee'
      } : {
        background: '#ffffff', primaryColor: '#f3f5f8', primaryTextColor: '#1e2633',
        primaryBorderColor: '#64748b', lineColor: '#64748b', secondaryColor: '#fdf1d6',
        tertiaryColor: '#ffffff', textColor: '#1e2633', mainBkg: '#f3f5f8', clusterBkg: '#fafbfc',
        clusterBorder: '#c9d0d8', edgeLabelBackground: '#ffffff', nodeTextColor: '#1e2633'
      },
      flowchart: { curve: 'basis', useMaxWidth: true },
      sequence: { useMaxWidth: true }
    });
    blocks.forEach(function (b) {
      b.removeAttribute('data-processed');
      b.textContent = b.getAttribute('data-src');
    });
    try { window.mermaid.run({ nodes: blocks }); } catch (e) { /* leave source visible */ }
  }

  render();
  document.addEventListener('forgeiec:theme', render);
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', function () {
      if (!document.documentElement.getAttribute('data-theme')) render();
    });
  }
})();
