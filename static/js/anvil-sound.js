/* ForgeIEC "forge sound": three anvil strikes, synthesised with the
   Web Audio API. No audio file, no network request. Loaded only when
   the visitor has switched the sound on.

   Each strike = a short filtered noise burst (the hammer contact) plus a
   few inharmonic sine partials with fast exponential decay (the ringing
   steel). Master gain <= 0.25, followed by a compressor as soft limiter. */
(function () {
  'use strict';

  var MASTER = 0.22;
  // Inharmonic ratios of a struck steel bar/plate, amplitude, decay time (s)
  var PARTIALS = [
    [1.00, 0.55, 1.90],
    [2.76, 0.32, 1.10],
    [5.40, 0.18, 0.42],
    [8.93, 0.10, 0.25],
    [13.3, 0.05, 0.14]
  ];

  function rand(a, b) { return a + Math.random() * (b - a); }

  function noiseBuffer(ctx, seconds) {
    var len = Math.max(1, Math.floor(ctx.sampleRate * seconds));
    var buf = ctx.createBuffer(1, len, ctx.sampleRate);
    var d = buf.getChannelData(0);
    for (var i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    return buf;
  }

  function strike(ctx, out, t, f0, level) {
    // Hammer contact: band-passed noise, ~35 ms
    var n = ctx.createBufferSource();
    n.buffer = noiseBuffer(ctx, 0.06);
    var bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = rand(3200, 4200);
    bp.Q.value = 0.9;
    var ng = ctx.createGain();
    ng.gain.setValueAtTime(0.0001, t);
    ng.gain.exponentialRampToValueAtTime(0.9 * level, t + 0.002);
    ng.gain.exponentialRampToValueAtTime(0.0001, t + 0.045);
    n.connect(bp); bp.connect(ng); ng.connect(out);
    n.start(t); n.stop(t + 0.06);

    // Ringing partials
    PARTIALS.forEach(function (p) {
      var o = ctx.createOscillator();
      o.type = 'sine';
      o.frequency.value = f0 * p[0] * rand(0.995, 1.005);
      var g = ctx.createGain();
      var amp = p[1] * level;
      var dec = p[2] * rand(0.9, 1.1);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(amp, t + 0.003);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dec);
      o.connect(g); g.connect(out);
      o.start(t); o.stop(t + dec + 0.05);
    });
  }

  /** Schedules three strikes on ctx into dest, starting at t0. Returns the end time. */
  function schedule(ctx, dest, t0) {
    var master = ctx.createGain();
    master.gain.value = MASTER;
    var limiter = ctx.createDynamicsCompressor();
    limiter.threshold.value = -6;
    limiter.knee.value = 6;
    limiter.ratio.value = 20;
    limiter.attack.value = 0.002;
    limiter.release.value = 0.12;
    master.connect(limiter); limiter.connect(dest);

    var f0 = rand(505, 535);
    var t = t0;
    var levels = [1.0, 0.85, 1.0];
    for (var i = 0; i < 3; i++) {
      strike(ctx, master, t, f0 * rand(0.99, 1.01), levels[i]);
      t += (i === 1 ? 0.52 : 0.40) + rand(-0.03, 0.03);
    }
    return t + 2.0;
  }

  var ctx = null;
  function getCtx() {
    if (ctx) return ctx;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    return ctx;
  }

  function playNow() {
    var c = getCtx();
    if (!c) return;
    schedule(c, c.destination, c.currentTime + 0.05);
  }

  /** Plays the strikes; if autoplay is blocked, waits for the first user gesture (once). */
  function play() {
    var c = getCtx();
    if (!c) return;
    if (c.state === 'running') { playNow(); return; }
    try { c.resume(); } catch (e) { /* ignore */ }
    // resume() may stay pending while autoplay is blocked: check shortly after.
    setTimeout(function () {
      if (c.state === 'running') { playNow(); return; }
      var later = function (e) {
        // The sound toggle handles its own clicks; ignore gestures on it.
        if (e && e.target && e.target.closest && e.target.closest('.sound-toggle')) return;
        document.removeEventListener('pointerdown', later, true);
        document.removeEventListener('keydown', later, true);
        c.resume().then(playNow, function () {});
      };
      document.addEventListener('pointerdown', later, true);
      document.addEventListener('keydown', later, true);
    }, 250);
  }

  window.ForgeAnvil = { schedule: schedule, play: play };
})();
