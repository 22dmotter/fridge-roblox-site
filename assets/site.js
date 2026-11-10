(function(){
document.querySelectorAll('.yt[data-id]').forEach(function(box){var a=box.querySelector('a');if(!a)return;a.addEventListener('click',function(e){e.preventDefault();var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+box.dataset.id+'?autoplay=1&rel=0';f.title=box.dataset.title||'YouTube video';f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.loading='lazy';box.innerHTML='';box.appendChild(f);});});
var input=document.getElementById('guide-search');if(!input)return;
var cards=[].slice.call(document.querySelectorAll('.card[data-search]'));var btns=[].slice.call(document.querySelectorAll('.filters button'));var empty=document.querySelector('.empty');var cat='all';
function run(){var q=input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);var shown=0;cards.forEach(function(c){var t=c.dataset.search;var ok=(cat==='all'||c.dataset.cat===cat)&&q.every(function(w){return t.indexOf(w)>-1});c.hidden=!ok;if(ok)shown++;});if(empty)empty.style.display=shown?'none':'block';}
btns.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.cat;btns.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run();});});
var p=new URLSearchParams(location.search);if(p.get('q'))input.value=p.get('q');input.addEventListener('input',run);run();
})();