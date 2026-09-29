/* Mini slide-deck: điều hướng ← →, chấm tròn, Toàn màn hình, tự co giãn cỡ chữ (fit) */
(function(){
document.querySelectorAll('.mdeck').forEach(function(deck){
  var slides=[].slice.call(deck.querySelectorAll('.mdeck-slide'));
  var bar=deck.querySelector('.mdeck-bar');
  var prevBtn=bar.querySelector('.mdeck-prev'),nextBtn=bar.querySelector('.mdeck-next');
  var count=bar.querySelector('.mdeck-count'),dotsWrap=bar.querySelector('.mdeck-dots'),fsBtn=bar.querySelector('.mdeck-fs');
  var i=0;
  try{var saved=parseInt(sessionStorage.getItem('deck:'+location.pathname+':'+(deck.id||'0')),10);if(saved>=0&&saved<slides.length)i=saved;}catch(e){}
  slides.forEach(function(s,idx){var d=document.createElement('button');d.type='button';d.title='Slide '+(idx+1);d.addEventListener('click',function(){go(idx)});dotsWrap.appendChild(d)});
  var dots=[].slice.call(dotsWrap.children);
  function isFs(){return document.fullscreenElement===deck||document.webkitFullscreenElement===deck}
  function fit(){
    slides.forEach(function(s){s.style.fontSize='';s.style.height=''});
    var s=slides[i],fs=isFs(),lo=fs?13:14,hi=fs?40:26;
    if(!fs){s.style.height=Math.max(400,Math.min(720,window.innerHeight*0.66))+'px'}
    if(s.classList.contains('part-divider')){s.style.fontSize=(fs?26:20)+'px';if(!fs)s.style.height='';return}
    while(hi-lo>0.5){var mid=(lo+hi)/2;s.style.fontSize=mid+'px';if(s.scrollHeight<=s.clientHeight+1)lo=mid;else hi=mid}
    s.style.fontSize=lo+'px';
  }
  function fitSoon(){requestAnimationFrame(function(){requestAnimationFrame(fit)})}
  function render(){
    slides.forEach(function(s,idx){s.classList.toggle('active',idx===i)});
    dots.forEach(function(d,idx){d.classList.toggle('on',idx===i)});
    count.textContent=(i+1)+'/'+slides.length;prevBtn.disabled=i===0;nextBtn.disabled=i===slides.length-1;
    try{sessionStorage.setItem('deck:'+location.pathname+':'+(deck.id||'0'),i)}catch(e){}
    fitSoon();
  }
  function go(n){i=Math.max(0,Math.min(slides.length-1,n));render()}
  prevBtn.addEventListener('click',function(){go(i-1)});nextBtn.addEventListener('click',function(){go(i+1)});
  deck.tabIndex=0;
  deck.addEventListener('keydown',function(e){
    if(e.target.closest&&e.target.closest('input,textarea,select'))return;
    if(e.key==='ArrowRight'||e.key==='PageDown'){go(i+1);e.preventDefault()}
    if(e.key==='ArrowLeft'||e.key==='PageUp'){go(i-1);e.preventDefault()}
  });
  if(fsBtn)fsBtn.addEventListener('click',function(){if(!isFs())(deck.requestFullscreen||deck.webkitRequestFullscreen).call(deck);else(document.exitFullscreen||document.webkitExitFullscreen).call(document)});
  deck.addEventListener('toggle',fitSoon,true);
  document.addEventListener('fullscreenchange',fitSoon);document.addEventListener('webkitfullscreenchange',fitSoon);
  window.addEventListener('resize',fitSoon);
  render();
});
})();
