# frame_assembly_viewer.py — Stage 2 assembly viewer (ROADMAP 2.1–2.5): frame-assembly-3d.html.
# Step-by-step 3D of the extrusion frame going together, in the layout sheet's terminology (uprights, base rails, PSU rails,
# AWG rails, scope rails, top rails, rear cross rails, inner rails, inner uprights, ties). Each step colours the pieces it
# adds; the scope rails stay a ghost — they go in at 2.6, after the sled feet are bonded into the beams.
# three.js is lifted verbatim from bench-stack-3d.html so the two viewers always match.
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC_VIEWER = os.path.join(ROOT, "bench-stack-3d.html")
OUT = os.path.join(ROOT, "frame-assembly-3d.html")

s = open(SRC_VIEWER, encoding="utf-8").read()
m = re.search(r"<script>(/\*\*\s*\n \* @license.*?)</script>", s, re.S)
THREE = m.group(1)

# frame coordinates: x from the outside of the left upright, y from the front face, z from the bench. Boxes [x0,x1,y0,y1,z0,z1].
UP = 20.0
def box(x0, x1, y0, y1, z0, z1): return [x0, x1, y0, y1, z0, z1]
L, R = (0, 20), (341, 361)               # left / right upright and side-rail x
F, B = (0, 20), (330, 350)               # front / rear upright y
LEVELS = {"base": (0, 20), "PSU": (68, 88), "AWG": (227.5, 247.5), "scope": (311, 331), "top": (490, 510)}

parts = []   # name, label, box, kind, tnuts (what to slide into THIS piece before it is fitted — slide-in T-nuts only)
TNUTS = {
    "base-rail-left": "6 in the TOP slot (4 runner + 2 spare)", "base-rail-right": "6 in the TOP slot (4 runner + 2 spare)",
    "top-rail-left": "none", "top-rail-right": "2 spare in the INNER-face slot (door catch)",
    "PSU-rail-left": "4 TOP (cradles)",
    "PSU-rail-right": "4 TOP (cradles) + 1 INNER-face at y 27–43 (front-tie bracket) + 3 INNER-face (guide strips)",
    "AWG-rail-left": "4 TOP (cradles)", "AWG-rail-right": "2 spare TOP + 3 INNER-face (guide strips)",
    "scope-rail-left": "2 BOTTOM (cast brackets)", "scope-rail-right": "2 BOTTOM (cast brackets); hinge leaves later use the OUTER slot",
    "inner-rail-PSU": "3 in the RIGHT-face slot (guide strips)",
    "inner-rail-AWG": "4 LEFT-face (right AWG cradles) + 3 TOP (mini-slot runner) + 3 RIGHT-face (guide strips)",
}
def add(name, label, b, kind):
    t = TNUTS.get(name)
    if t is None:
        t = {"upright": "none now — its slots stay open at the top until the caps go on", "cross": "none", "inner": "none", "tie": "none",
             "spacer": "—", "foot": "—", "cast": "1 drop-in nut in each slot it bridges; 2 × M5×8 (the metal L brackets from the extrusion pack)"}[kind]
    parts.append({"name": name, "label": label, "box": b, "kind": kind, "tnuts": t})

for tag, (x0, x1) in (("left", L), ("right", R)):
    for pos, (y0, y1) in (("front", F), ("rear", B)):
        add(f"upright-{pos}-{tag}", f"{pos}-{tag} upright (510)", box(x0, x1, y0, y1, 0, 510), "upright")
    for lvl, (z0, z1) in LEVELS.items():
        add(f"{lvl}-rail-{tag}", f"{tag} {lvl} rail (310)", box(x0, x1, 20, 330, z0, z1), "rail")
add("rear-cross-base", "base rear cross rail (321)", box(20, 341, 330, 350, 0, 20), "cross")
add("rear-cross-top", "top rear cross rail (321)", box(20, 341, 330, 350, 490, 510), "cross")
add("inner-upright-front", "front inner upright (179.5)", box(251, 271, 3, 23, 68, 247.5), "inner")
add("inner-upright-rear", "rear inner upright (179.5)", box(251, 271, 330, 350, 68, 247.5), "inner")
add("inner-rail-PSU", "PSU-level inner rail (307)", box(251, 271, 23, 330, 68, 88), "inner")
add("inner-rail-AWG", "AWG-level inner rail (307)", box(251, 271, 23, 330, 227.5, 247.5), "inner")
add("tie-PSU-front", "PSU-level front tie (70)", box(271, 341, 3, 23, 68, 88), "tie")
add("tie-PSU-rear", "PSU-level rear tie (70)", box(271, 341, 330, 350, 68, 88), "tie")
add("tie-AWG-rear", "AWG-level rear tie (70)", box(271, 341, 330, 350, 227.5, 247.5), "tie")
# spacers (printed, PETG): stand on the rail below, rail above sits on them — one near each end of the rail being set
for tag, (x0, x1) in (("left", L), ("right", R)):
    for pos, y in (("front", 40), ("rear", 290)):
        add(f"spacer48-{tag}-{pos}", "48 spacer (base rail top → PSU rail)", box(x0 + 2, x1 - 2, y, y + 20, 20, 68), "spacer")
        add(f"spacer139-{tag}-{pos}", "139.5 spacer (PSU rail top → AWG rail)", box(x0 + 2, x1 - 2, y, y + 20, 88, 227.5), "spacer")
for tag, (x0, x1) in (("left", L), ("right", R)):
    for pos, y in (("front", 40), ("rear", 290)):
        add(f"spacer63-{tag}-{pos}", "63.5 spacer (AWG rail top → scope rail)", box(x0 + 2, x1 - 2, y, y + 20, 247.5, 311), "spacer")
add("foot-left", "210 sled foot in the scope rail's inner-face slot (rib pointing into the frame)", box(8, 23, 120, 330, 316, 326), "foot")
add("foot-right", "210 sled foot in the scope rail's inner-face slot (rib pointing into the frame)", box(338, 353, 120, 330, 316, 326), "foot")
add("spacer48-inner-rear", "48 spacer under the rear inner upright (on the base rear cross rail)", box(253, 269, 332, 348, 20, 68), "spacer")
# cast corner brackets: (a) UNDER the scope rails at both ends — those rails cannot take a hidden L (the sled feet run the
# inner slot, the tile fingers the outer); (b) one lying flat between the PSU-level front tie's rear face and the right PSU
# rail's inner face — the tie sits 3 mm behind the front upright, so no face of the two lines up for a hidden L. Legs 4 thick.
for tag, (x0, x1) in (("left", L), ("right", R)):
    for pos, (y0, y1, yf0, yf1) in (("front", (20, 40, 20, 24)), ("rear", (310, 330, 326, 330))):
        lab = "L-shaped metal corner bracket under the scope rail end (one M5×8 up into the rail's bottom slot, one into the upright's face)"
        add(f"cast-scope-{tag}-{pos}", lab, box(x0 + 2, x1 - 2, y0, y1, 307, 311), "cast")          # leg under the rail
        add(f"cast-scope-{tag}-{pos}-b", lab, box(x0 + 2, x1 - 2, yf0, yf1, 291, 311), "cast")      # leg down the upright's face
add("cast-tie-front-a", "L-shaped metal corner bracket, front tie rear face → right PSU rail inner face (2 × M5×8)", box(321, 341, 23, 27, 70, 86), "cast")
add("cast-tie-front-b", "L-shaped metal corner bracket, front tie rear face → right PSU rail inner face (2 × M5×8)", box(337, 341, 27, 43, 70, 86), "cast")

STEPS = [
    ("1 · Left side, all five rails", "Lay the front-left and rear-left uprights flat on the bench, 321 apart. Slide 4 connectors into each upright's inner-face slot from the top end (they only go in from an end) and push them down to roughly z 20, 88, 247 and 490. Push one 210 sled foot into the scope rail's inner-face slot from the end, rib pointing into the frame. Lay the five left rails between the uprights — base rail (z 0–20), PSU rail, AWG rail, scope rail, top rail — and close the uprights onto them so each connector leg enters its rail's end slot (the scope rail has no connector). All loose. Then: base rail flush with the uprights' bottom ends and top rail flush with their top ends, tighten; two 48 spacers on the base rail, PSU rail down onto them, tighten; two 139.5 spacers on the PSU rail, AWG rail down onto them, tighten; two 63.5 spacers on the AWG rail, scope rail down onto them, a metal L corner bracket under each end (M5×8 up into the rail's bottom slot, M5×8 into the upright's face — hold the drop-in nut in the downward slot with a fingertip until the bolt bites); spacers out. Diagonals equal within 1 mm. The foot stays loose in its rail; it cannot come out.",
     ["upright-front-left", "upright-rear-left", "base-rail-left", "top-rail-left", "spacer48-left-front", "spacer48-left-rear", "PSU-rail-left", "spacer139-left-front", "spacer139-left-rear", "AWG-rail-left",
      "spacer63-left-front", "spacer63-left-rear", "foot-left", "scope-rail-left", "cast-scope-left-front", "cast-scope-left-front-b", "cast-scope-left-rear"]),
    ("2 · Right side, all five rails", "Same again: front-right upright, rear-right upright, right base rail, right PSU rail, right AWG rail, right scope rail (foot in first), right top rail; 4 connectors per upright from the top; spacers 48, 139.5, 63.5; metal L corner brackets under the scope rail; diagonals.",
     ["upright-front-right", "upright-rear-right", "base-rail-right", "top-rail-right", "spacer48-right-front", "spacer48-right-rear", "PSU-rail-right", "spacer139-right-front", "spacer139-right-rear", "AWG-rail-right",
      "spacer63-right-front", "spacer63-right-rear", "foot-right", "scope-rail-right", "cast-scope-right-front", "cast-scope-right-front-b", "cast-scope-right-rear"]),
    ("3 · Join at the rear", "Stand both sides up. Into the rear-right upright's FRONT-face slot from the top end: 2 connectors pushed down to roughly z 88 and 247 (for the two rear ties, later), then 1 for the top cross rail; 1 into the same slot of the rear-left upright from the top; 1 each from the bottom ends for the base cross rail. Base rear cross rail and top rear cross rail (321) between the rear uprights, tighten. Check: 321 between the uprights at the front as well as the rear, 510 overall, plan diagonals equal within 1 mm.",
     ["rear-cross-base", "rear-cross-top"]),
    ("4 · Inner sub-frame", "On the bench, the same way as a side: the two inner uprights 307 apart, 2 connectors each in the RIGHT-face slot (x 271) from an end, the PSU-level inner rail and AWG-level inner rail closed onto them at the uprights' ends (a 347 × 247.5 ladder), tighten. Ties: PSU-level front tie on the front inner upright's right face (connector on their rear faces), PSU-level rear tie and AWG-level rear tie on the rear inner upright (connectors on their front faces; their upright-side legs are the two pre-loaded in step 3 — the tie slides on as the ladder goes in). Slide the ladder in from the front with a 48 spacer standing on the base rear cross rail under the rear inner upright; tie tops flush with the right PSU rail's top (z 88); tighten; spacer out. Front tie's outer end: a metal L corner bracket lying flat — one leg on the tie's rear face, the other on the right PSU rail's inner face, 2 × M5×8 on drop-in nuts.",
     ["inner-upright-front", "inner-upright-rear", "inner-rail-PSU", "inner-rail-AWG", "tie-PSU-front", "tie-PSU-rear", "tie-AWG-rear", "spacer48-inner-rear", "cast-tie-front-a", "cast-tie-front-b"]),
    ("5 · Done — rack test", "Push and rack the frame: if a corner gives, the 3 spare L brackets go under the PSU rails' rear ends first. All ten 310s are in. Later, from the rear: the sled beams thread onto the feet's ribs and are glued there (2.6's clearance check, 3.0 gauge against a 336 reference, happens then). Two of the four 307s cut are spare (the design uses two inner rails).",
     []),
]
GHOST = []
COLOURS = {"upright": "#4a4f57", "rail": "#4a4f57", "cross": "#4a4f57", "inner": "#4a4f57", "tie": "#4a4f57", "spacer": "#e8c547", "cast": "#2f6f73", "foot": "#8a2b2b"}
NEW = "#e0641b"

STYLE = """<title>Frame Assembly Stage 2</title>
<style>
:root{--bg:#ece7dc;--panel:rgba(255,255,255,.93);--ink:#1d1f22;--muted:#4b4f56;--rule:#cfc9bd;--new:#e0641b;--bench:#c9a46b}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#1b1d21;--panel:rgba(32,34,39,.94);--ink:#ecebe6;--muted:#b5b3ac;--rule:#3a3d44;--new:#f0783a;--bench:#6b5636}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#1b1d21;--panel:rgba(32,34,39,.94);--ink:#ecebe6;--muted:#b5b3ac;--rule:#3a3d44;--new:#f0783a;--bench:#6b5636}
html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font-family:Helvetica,Arial,sans-serif;overflow:hidden;touch-action:none}
#c{width:100%;height:100%;display:block}
#ui{position:absolute;top:calc(10px + env(safe-area-inset-top,0px));left:10px;width:min(420px,calc(100vw - 36px));max-height:calc(100% - 40px);overflow:auto;background:var(--panel);padding:10px 12px;border-radius:6px;font-size:13px;line-height:1.5;box-sizing:border-box}
#ui h1{font-size:14px;margin:0 0 6px}
#step{width:100%;display:block;margin-bottom:4px}
#title{font-weight:bold;margin:6px 0 2px}
#desc{color:var(--ink)}
#plist{margin:6px 0 0;padding-left:18px;color:var(--new)}
#plist li span{color:var(--muted);font-size:12px}
#tn{margin-top:6px;color:var(--muted);font-size:11px}
#legend{margin-top:8px;border-top:1px solid var(--rule);padding-top:6px;color:var(--muted);font-size:12px}
.sw{display:inline-block;width:10px;height:10px;margin-right:4px;vertical-align:middle;border:1px solid #666}
#hint{position:absolute;bottom:calc(10px + env(safe-area-inset-bottom,0px));left:10px;font-size:11px;color:var(--muted);background:var(--panel);padding:4px 8px;border-radius:4px}
button{font-size:13px;padding:2px 10px}
</style>
"""
BODY = f"""<canvas id="c"></canvas>
<div id="ui"><h1>Frame assembly — Stage 2 (ROADMAP 2.1–2.5)</h1>
<input type="range" id="step" min="1" max="{len(STEPS)}" value="1" step="1">
<div><button id="prev">◀ back</button> <button id="next">next ▶</button> <label style="margin-left:10px"><input type="checkbox" id="showall"> show finished frame</label></div>
<div id="title"></div><div id="desc"></div><ul id="plist"></ul>
<div id="tn">T-nuts are the drop-in type: drop each one in as its part is fitted (the counts are a tally per slot). Cast brackets M5×8; printed parts later M5×10.</div>
<div id="legend"><span class="sw" style="background:{NEW}"></span>added this step &nbsp; <span class="sw" style="background:#4a4f57"></span>already fitted &nbsp; <span class="sw" style="background:{COLOURS['spacer']}"></span>printed spacer (remove after) &nbsp; <span class="sw" style="background:{COLOURS['cast']}"></span>metal L corner bracket &nbsp; <span class="sw" style="background:{COLOURS['foot']}"></span>sled foot (in the scope rail's slot)<br>Hidden L-connectors go on the faces that look INTO the frame (side rails ↔ uprights: inner faces; rear cross rails and rear ties: front faces; inner rails ↔ inner uprights: right faces; front tie ↔ its inner upright: rear faces). One per joint. x from the outside of the left upright, y from the front face, z from the bench (mm). Front is the open side.</div>
</div>
<div id="hint">drag: orbit · right-drag / shift-drag: pan · wheel / pinch: zoom</div>
<script>{THREE}</script>
<script>
const PARTS={json.dumps(parts)};
const STEPS={json.dumps(STEPS)};
const GHOST={json.dumps(GHOST)};
const COLOURS={json.dumps(COLOURS)}; const NEW="{NEW}";
const canvas=document.getElementById('c');
const renderer=new THREE.WebGLRenderer({{canvas,antialias:true}}); renderer.setPixelRatio(Math.min(devicePixelRatio,2));
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const scene=new THREE.Scene(); scene.background=new THREE.Color(css('--bg'));
const camera=new THREE.PerspectiveCamera(40,1,10,10000);
const edgeMat=new THREE.LineBasicMaterial({{color:0x111111,transparent:true,opacity:0.35}});
const meshes={{}};
for(const p of PARTS){{
  const [x0,x1,y0,y1,z0,z1]=p.box;
  const geo=new THREE.BoxGeometry(x1-x0,z1-z0,y1-y0);
  const mat=new THREE.MeshLambertMaterial({{color:new THREE.Color(COLOURS[p.kind]),transparent:true,opacity:1}});
  const m=new THREE.Mesh(geo,mat); m.position.set((x0+x1)/2,(z0+z1)/2,-(y0+y1)/2);
  m.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo),edgeMat));
  scene.add(m); meshes[p.name]={{mesh:m,part:p}};
}}
// bench
{{ const g=new THREE.BoxGeometry(700,6,650); const m=new THREE.Mesh(g,new THREE.MeshLambertMaterial({{color:new THREE.Color(css('--bench'))}})); m.position.set(180,-3,-175); scene.add(m); }}
// front-face marker: a thin line on the bench along y=0 so "front" reads at a glance
{{ const g=new THREE.BoxGeometry(361,0.5,2); const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({{color:0xa4480f}})); m.position.set(180.5,0.3,0); scene.add(m); }}
scene.add(new THREE.AmbientLight(0xffffff,0.55));
const key=new THREE.DirectionalLight(0xffffff,0.75); key.position.set(400,700,500); scene.add(key);
const fill=new THREE.DirectionalLight(0xffffff,0.3); fill.position.set(-400,300,-200); scene.add(fill);

const slider=document.getElementById('step'), showall=document.getElementById('showall');
function apply(){{
  const k=+slider.value-1, all=showall.checked;
  const fitted=new Set(); for(let i=0;i<=k;i++) for(const n of STEPS[i][2]) fitted.add(n);
  const now=new Set(STEPS[k][2]);
  for(const [name,o] of Object.entries(meshes)){{
    const p=o.part, m=o.mesh;
    if(GHOST.includes(name)){{ m.visible=all||k===STEPS.length-1; m.material.color.set(0xbbbbbb); m.material.opacity=all?1:0.25; if(all) m.material.color.set(COLOURS[p.kind]); continue; }}
    if(p.kind==='spacer'){{ m.visible=!all && now.has(name); m.material.opacity=1; m.material.color.set(COLOURS.spacer); continue; }}
    if(p.kind==='foot'){{ m.visible=all||fitted.has(name); m.material.opacity=1; m.material.color.set(COLOURS.foot); continue; }}
    const on=all||fitted.has(name);
    m.visible=on; m.material.opacity=1;
    m.material.color.set(!all&&now.has(name)?NEW:COLOURS[p.kind]);
  }}
  document.getElementById('title').textContent=STEPS[k][0];
  document.getElementById('desc').textContent=STEPS[k][1];
  const ul=document.getElementById('plist'); ul.innerHTML='';
  const seen=new Set();
  for(const n of STEPS[k][2]){{ const lab=meshes[n].part.label; if(seen.has(lab)) continue; seen.add(lab);
    const cnt=STEPS[k][2].filter(x=>meshes[x].part.label===lab && !x.endsWith('-b')).length;   /* a two-box part counts once */ const li=document.createElement('li'); li.textContent=(cnt>1?cnt+' × ':'')+lab;
    const p=meshes[n].part; if(p.tnuts!=='—'){{ const sp=document.createElement('span'); sp.textContent=' — T-nuts: '+p.tnuts; li.appendChild(sp); }} ul.appendChild(li); }}
}}
slider.addEventListener('input',apply); showall.addEventListener('change',apply);
document.getElementById('prev').addEventListener('click',()=>{{slider.value=Math.max(1,+slider.value-1);apply();}});
document.getElementById('next').addEventListener('click',()=>{{slider.value=Math.min(STEPS.length-1,+slider.value+1);apply();}});
apply();

// orbit (as bench-stack-3d.html)
const target=new THREE.Vector3(60,240,-175); let theta=0.85, phi=1.2, dist=1500;
function place(){{camera.position.set(target.x+dist*Math.sin(phi)*Math.sin(theta),target.y+dist*Math.cos(phi),target.z+dist*Math.sin(phi)*Math.cos(theta));camera.lookAt(target);}}
let ptrs=new Map(), last=null, lastPinch=null;
canvas.addEventListener('pointerdown',e=>{{ptrs.set(e.pointerId,{{x:e.clientX,y:e.clientY,b:e.button}});canvas.setPointerCapture(e.pointerId);last=null;lastPinch=null;}});
canvas.addEventListener('pointerup',e=>{{ptrs.delete(e.pointerId);last=null;lastPinch=null;}});
canvas.addEventListener('pointercancel',e=>{{ptrs.delete(e.pointerId);last=null;lastPinch=null;}});
canvas.addEventListener('pointermove',e=>{{
  if(!ptrs.has(e.pointerId))return;
  ptrs.set(e.pointerId,{{x:e.clientX,y:e.clientY,b:ptrs.get(e.pointerId).b}});
  const pts=[...ptrs.values()];
  if(pts.length===1){{ const p=pts[0];
    if(last){{ const dx=p.x-last.x, dy=p.y-last.y; if(p.b===2||e.shiftKey){{pan(dx,dy);}} else {{theta-=dx*0.006; phi=Math.min(Math.PI-0.05,Math.max(0.05,phi-dy*0.006));}} }}
    last={{x:p.x,y:p.y}};
  }} else if(pts.length>=2){{ const [a,b]=pts; const cx=(a.x+b.x)/2, cy=(a.y+b.y)/2, d=Math.hypot(a.x-b.x,a.y-b.y);
    if(lastPinch){{ dist*=lastPinch.d/d; dist=Math.min(5000,Math.max(200,dist)); pan(cx-lastPinch.cx,cy-lastPinch.cy); }}
    lastPinch={{cx,cy,d}}; last=null; }}
  place();
}});
canvas.addEventListener('wheel',e=>{{e.preventDefault();dist*=Math.exp(e.deltaY*0.0012);dist=Math.min(5000,Math.max(200,dist));place();}},{{passive:false}});
canvas.addEventListener('contextmenu',e=>e.preventDefault());
function pan(dx,dy){{const right=new THREE.Vector3(),up=new THREE.Vector3();camera.matrix.extractBasis(right,up,new THREE.Vector3());const s=dist*0.0011;target.addScaledVector(right,-dx*s).addScaledVector(up,dy*s);}}
function resize(){{const w=canvas.clientWidth,h=canvas.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}}
window.addEventListener('resize',resize); resize(); place();
(function loop(){{requestAnimationFrame(loop);renderer.render(scene,camera);}})();
</script>
"""
# repo copy: a full document. Artifact copy (no skeleton — the publisher adds one): STYLE + BODY only.
html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, '
        'maximum-scale=1, user-scalable=no, viewport-fit=cover">\n' + STYLE + '</head><body>\n' + BODY + '</body></html>\n')
open(OUT, "w", encoding="utf-8").write(html)
import sys
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(STYLE + BODY)
print(OUT, len(html) // 1024, "kB", len(parts), "parts", len(STEPS), "steps")
