/* ---- parallax background: drifts a fraction of scroll ---- */
(function(){
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var bg = document.querySelector('.bg');
  if (!bg) return;
  var ticking = false;
  function update(){
    var maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    var buffer = window.innerHeight * 0.20;                 // matches the 20vh headroom on .bg
    var f = maxScroll > 0 ? Math.min(0.3, buffer / maxScroll) : 0;  // capped, scaled so it never over-travels
    var y = -window.scrollY * f;                            // drifts up slightly as you scroll down
    bg.style.transform = 'translate3d(0,' + y + 'px,0)';
    ticking = false;
  }
  function onScroll(){ if (!ticking){ ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive:true });
  window.addEventListener('resize', update);
  update();
})();

/* ---- soft sticky-follow for the rail block ----
   rounds off the sharp sticky "lock" with a softplus curve (smooth approximation
   of max(0, t)). CSS position:sticky stays as the no-JS / reduced-motion fallback. */
(function(){
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var block = document.querySelector('.rail-follow');
  if (!block) return;
  var STICK = 28;    // resting offset from top, matches the CSS top:28px
  var SOFT  = 80;    // smoothing width (px): bigger = gentler, longer ease-in
  var baseTop = 0;
  function softplus(t){
    var x = t / SOFT;
    if (x > 30) return t;                       // far past lock: linear (avoids exp overflow)
    return SOFT * Math.log(1 + Math.exp(x));
  }
  function measure(){
    block.style.transform = 'none';             // read natural position untransformed
    var r = block.getBoundingClientRect();
    baseTop = r.top + window.scrollY;
  }
  var ticking = false;
  function update(){
    var t = window.scrollY - (baseTop - STICK);  // >0 once past the lock line
    block.style.transform = 'translate3d(0,' + softplus(t) + 'px,0)';
    ticking = false;
  }
  function onScroll(){ if (!ticking){ ticking = true; requestAnimationFrame(update); } }
  block.style.position = 'static';              // take over from CSS sticky
  block.style.willChange = 'transform';
  measure();
  update();
  window.addEventListener('scroll', onScroll, { passive:true });
  window.addEventListener('resize', function(){ measure(); update(); });
})();
