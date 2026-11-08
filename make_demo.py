"""Build template demos of the Neon Arcade games for the iPhone 12 screen-test repo.
usage: python3 make_demo.py SRC_GAMES_DIR OUT_DIR"""
import sys, os
SRC, OUT = sys.argv[1], sys.argv[2]

TPL = r'''
<style id="tpl">
/* ===== 3-area template (iPhone 12 reference): banner 64 / game 667 / bar 36 / gap 30 ===== */
:root{--banner:64px;--game:667px;--barh:36px;--gap:30px;padding:0!important}
html{height:100vh!important;overflow:hidden;background:linear-gradient(#07030f,rgba(7,3,15,0) 64px),radial-gradient(120% 55% at 50% 0%,rgba(255,43,214,.18),transparent 60%),radial-gradient(120% 45% at 50% 100%,rgba(25,243,255,.13),transparent 60%),#07030f!important}
body{height:100vh!important;background:transparent!important}
#app{position:absolute!important;left:0!important;top:0!important;width:390px!important;height:var(--sh,100vh)!important;transform-origin:0 0!important;transform:var(--st,none)!important;padding:0!important;margin:0!important;background:transparent!important}
main{max-width:none!important;max-height:none!important;width:100%!important;height:100%!important;margin:0!important}
body:not(.flip) main{padding:var(--pt,0px) 14px var(--gap)!important;justify-content:flex-start!important}
body:not(.flip) main>TITLE{flex:none!important;height:var(--banner)!important;max-height:none!important;margin:0!important;display:flex!important;align-items:center;justify-content:center;font-size:20px!important}
body:not(.flip) main>FIRST{margin-top:auto!important}
body:not(.flip) .bar{position:relative!important;inset:auto!important;flex:none!important;height:var(--barh)!important;max-height:none!important;margin:auto 0 0!important;padding:0!important;width:100%!important;max-width:none!important;
  display:grid!important;grid-template-columns:1fr auto 1fr!important;align-items:end!important;align-content:end!important}
body:not(.flip) .bar button{padding:22px 0 0!important}
.bar #bRules{grid-column:1;justify-self:start}.bar .mnu{grid-column:2;justify-self:center;color:var(--yel)!important;text-shadow:0 0 6px var(--yel)!important}.bar #bSet{grid-column:3;justify-self:end}
/* flipped 2-player: same stage and bar position, its own layout */
body.flip main{padding:calc(var(--pt,0px) + 10px) 14px calc(40px + var(--gap))!important}
body.flip .bar{display:grid!important;grid-template-columns:1fr auto 1fr!important;padding:0 14px!important;bottom:var(--gap)!important;max-width:none!important}
EXTRA
/* guides: tap the title to show/hide */
.gd{position:absolute;left:2px;right:2px;border:2px dashed;pointer-events:none;z-index:30;display:none}
.gd span{position:absolute;right:4px;top:2px;font:400 16px/1 var(--vt)}
html.guides body:not(.flip) .gd{display:block}
#gB{border-color:var(--mag)}#gB span{color:var(--mag)}#gG{border-color:var(--cy)}#gG span{color:var(--cy)}#gM{border-color:var(--yel)}#gM span{color:var(--yel)}
#probe{position:fixed;visibility:hidden;padding:env(safe-area-inset-top) 0 env(safe-area-inset-bottom) 0}
</style>
'''
JS = r'''
<div id="probe"></div>
<script>
(function(){
var de=document.documentElement,app=document.getElementById('app'),main=app.querySelector('main'),tt=main.querySelector('TITLE'),bar=document.getElementById('bar');
var BLOCK=64+667+36+30; /* banner + game + bar + gap, scaled as one */
['gB','gG','gM'].forEach(function(id){var d=document.createElement('div');d.className='gd';d.id=id;d.innerHTML='<span></span>';app.appendChild(d)});
function stage(){
  var t=parseFloat(getComputedStyle(document.getElementById('probe')).paddingTop)||0;
  if(window.__SAFE)t=__SAFE.t;
  var W=innerWidth,H=innerHeight,k=Math.min(W/390,(H-t)/BLOCK),sh=t/k+BLOCK,x=(W-390*k)/2,y=(H-sh*k)/2;
  de.style.setProperty('--sh',sh+'px');de.style.setProperty('--pt',(t/k)+'px');
  de.style.setProperty('--st','translate('+x+'px,'+y+'px) scale('+k+')');
  try{if(typeof fit==='function')fit()}catch(e){}
  setTimeout(guides,0);
}
function box(el){var y=0,e=el;while(e&&e!==app){y+=e.offsetTop;e=e.offsetParent}return [y,el.offsetHeight]}
function put(id,top,h,lab){var g=document.getElementById(id);g.style.top=top+'px';g.style.height=h+'px';g.firstChild.textContent=lab}
function guides(){var a=box(tt),b=box(bar),gt=a[0]+a[1],gh=b[0]-gt;
  put('gB',a[0],a[1],'banner '+a[1]);put('gG',gt,gh,'game '+Math.round(gh));put('gM',b[0],b[1],'bar '+b[1]+' · gap '+Math.round(app.clientHeight-b[0]-b[1]))}
tt.addEventListener('click',function(){de.classList.toggle('guides');guides()});
document.addEventListener('touchmove',function(e){if(!e.target.closest('.panel'))e.preventDefault()},{passive:false});
stage();addEventListener('resize',stage);addEventListener('orientationchange',function(){setTimeout(stage,300)});
try{new ResizeObserver(guides).observe(main)}catch(e){}
de.classList.add('guides');
})();
</script>
'''
MENU = '<button type="button" class="mnu" onclick="location.href=\'index.html\'">Menu</button>'
META = '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="Screen Test">\n'

def make(src, out, title, first, menu_after, extra='', reps=()):
    s = open(os.path.join(SRC, src), encoding='utf-8').read()
    def rep(a, b):
        nonlocal s
        assert a in s, (src, a[:60]); s = s.replace(a, b, 1)
    rep(menu_after, menu_after + MENU)
    rep('<meta name="theme-color" content="#07030f">', '<meta name="theme-color" content="#07030f">\n' + META)
    # panel opens right above the bar, measured in stage coordinates
    rep("if(document.documentElement.classList.contains('rot')){", "if(1){")
    for a, b in reps: rep(a, b)
    rep('</style>\n</head>', '</style>' + TPL.replace('TITLE', title).replace('FIRST', first).replace('EXTRA', extra) + '</head>')
    rep('</body>', JS.replace('TITLE', title) + '</body>')
    open(os.path.join(OUT, out), 'w', encoding='utf-8').write(s)
    print('built', out, len(s))

make('Knucklebones.html', 'knucklebones.html', '.ttl1', '.ctl',
     'aria-controls="panel">Rules</button>',
     extra='body:not(.flip) .side{max-height:none!important;flex-grow:8}body:not(.flip) .ctl{margin-bottom:8px!important}body.flip .side{max-height:none!important;flex-grow:1!important}',
     reps=[('function fit(){var de', 'function fit(){return;var de')])

make('Othello.html', 'othello.html', '#t1', '.ctl',
     'id="bRules" aria-expanded="false">Rules</button>',
     extra='body:not(.flip) .mid:not(#msg2){margin-bottom:0!important}html:not(.rotated) h1{font-size:20px!important;margin:0!important}')

make('Water_Sort.html', 'water_sort.html', 'h1', '#game',
     'id="bRules" aria-expanded="false">Rules</button>',
     reps=[("var h=rot?W:H;de.classList.toggle('short',h<=600);de.classList.toggle('tiny',h<=440);layout()}",
            "de.classList.remove('rot','r270','short','tiny');layout()}"),
           ("parseFloat(hs.fontSize)+parseFloat(hs.marginTop)","h.offsetHeight+parseFloat(hs.marginTop)")])

make('Sudoku.html', 'sudoku.html', '#t1', '#mid',
     'id="bRules" aria-expanded="false">Rules</button>',
     extra='html:not(.rotated) h1{margin:0!important}')

make('Remi.html', 'remi.html', 'h1', '#game',
     'id="bRules" aria-expanded="false">Rules</button>',
     reps=[("const h=rot?W:H;de.classList.toggle('short',h<=640);de.classList.toggle('tiny',h<=520);layout()}",
            "de.classList.remove('rot','r270','short','tiny');layout()}"),
           ("parseFloat(hs.fontSize)+parseFloat(hs.marginTop)","h.offsetHeight+parseFloat(hs.marginTop)")])
