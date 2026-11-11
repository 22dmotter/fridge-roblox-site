(function(){
document.querySelectorAll('.yt[data-id]').forEach(function(box){var a=box.querySelector('a');if(!a)return;a.addEventListener('click',function(e){e.preventDefault();var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+box.dataset.id+'?autoplay=1&rel=0';f.title=box.dataset.title||'YouTube video';f.allow='accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture';f.allowFullscreen=true;f.loading='lazy';box.innerHTML='';box.appendChild(f);});});
var input=document.getElementById('guide-search');if(!input)return;
var cards=[].slice.call(document.querySelectorAll('.card[data-search]'));var btns=[].slice.call(document.querySelectorAll('.filters button'));var empty=document.querySelector('.empty');var cat='all';
function run(){var q=input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);var shown=0;cards.forEach(function(c){var t=c.dataset.search;var ok=(cat==='all'||c.dataset.cat===cat)&&q.every(function(w){return t.indexOf(w)>-1});c.hidden=!ok;if(ok)shown++;});if(empty)empty.style.display=shown?'none':'block';}
btns.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.cat;btns.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run();});});
var p=new URLSearchParams(location.search);if(p.get('q'))input.value=p.get('q');input.addEventListener('input',run);run();
})();
(function(){
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var root=document.querySelector('.bg-fx');
if(!root)return;
if(reduce){root.parentNode&&root.parentNode.removeChild(root);return;}
var c=root.querySelector('canvas');
if(!c){c=document.createElement('canvas');root.appendChild(c);}
var ctx=c.getContext('2d',{alpha:true});
if(!ctx){root.parentNode&&root.parentNode.removeChild(root);return;}
var particles=[],running=false,raf=0,dpr=1,w=0,h=0,last=0;
function cap(){return window.innerWidth<640?25:60;}
function spawn(anywhere){
  var amber=Math.random()<0.55;
  return {x:Math.random()*w,y:anywhere?Math.random()*h:h+Math.random()*24,r:1+Math.random()*2,vx:(Math.random()-0.5)*8,vy:-(4+Math.random()*10),a:0.15+Math.random()*0.25,color:amber?'255,176,32':'230,238,245'};
}
function make(){var n=cap(),i;particles=[];for(i=0;i<n;i++)particles.push(spawn(true));}
function resize(){
  dpr=Math.min(window.devicePixelRatio||1,2);
  w=Math.max(1,window.innerWidth);h=Math.max(1,window.innerHeight);
  c.width=Math.floor(w*dpr);c.height=Math.floor(h*dpr);
  c.style.width=w+'px';c.style.height=h+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
  if(particles.length!==cap())make();
}
function tick(ts){
  if(!running)return;
  var dt=last?Math.min(0.05,(ts-last)/1000):0.016,i,p;last=ts;
  ctx.clearRect(0,0,w,h);
  for(i=0;i<particles.length;i++){
    p=particles[i];
    p.vx+=(Math.random()-0.5)*2*dt;
    if(p.vx>10)p.vx=10;if(p.vx<-10)p.vx=-10;
    p.x+=p.vx*dt;p.y+=p.vy*dt;
    if(p.y+p.r<0){particles[i]=p=spawn(false);}
    if(p.x<-8)p.x=w+8;else if(p.x>w+8)p.x=-8;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle='rgba('+p.color+','+p.a+')';ctx.fill();
  }
  raf=requestAnimationFrame(tick);
}
function start(){if(running)return;running=true;last=0;raf=requestAnimationFrame(tick);}
function stop(){running=false;last=0;if(raf)cancelAnimationFrame(raf);}
window.addEventListener('resize',resize,{passive:true});
document.addEventListener('visibilitychange',function(){if(document.hidden)stop();else start();});
resize();start();
})();