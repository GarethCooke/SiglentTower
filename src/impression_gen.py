import math, cairosvg
S3=math.sqrt(3)/2
def P(x,y,z):   # isometric projection, viewer front-right-above
    return ((x + y)*S3, (x - y)/2 - z)
def shade(hexc, f):
    r,g,b=int(hexc[1:3],16),int(hexc[3:5],16),int(hexc[5:7],16)
    return '#%02x%02x%02x'%(min(255,int(r*f)),min(255,int(g*f)),min(255,int(b*f)))
out=[]
def poly(pts, fill, stroke="#111", sw=0.5, op=1.0):
    d=" ".join(f"{u:.1f},{v:.1f}" for u,v in pts)
    out.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-opacity="{op}" stroke-linejoin="round"/>')
items=[]
def box(x0,x1,y0,y1,z0,z1,color,stroke="#111",sw=0.5,decor=None,name=""):
    key=-x1+y0-z1   # nearest-corner depth; more negative = nearer
    items.append((key,('box',(x0,x1,y0,y1,z0,z1),color,stroke,sw,decor)))
def draw_box(b,color,stroke,sw,decor):
    x0,x1,y0,y1,z0,z1=b
    # right face (x=x1), front face (y=y0), top face (z=z1)
    poly([P(x1,y0,z0),P(x1,y1,z0),P(x1,y1,z1),P(x1,y0,z1)], shade(color,0.72), stroke, sw)
    poly([P(x0,y0,z0),P(x1,y0,z0),P(x1,y0,z1),P(x0,y0,z1)], shade(color,0.90), stroke, sw)
    poly([P(x0,y0,z1),P(x1,y0,z1),P(x1,y1,z1),P(x0,y1,z1)], shade(color,1.08), stroke, sw)
    if decor: decor(b)
def frect(x0,x1,z0,z1,y,fill,stroke="#111",sw=0.4):   # rectangle on a front face
    poly([P(x0,y,z0),P(x1,y,z0),P(x1,y,z1),P(x0,y,z1)], fill, stroke, sw)
def fcircle(cx,cz,r,y,fill,stroke="#111"):
    pts=[P(cx+r*math.cos(t),y,cz+r*math.sin(t)) for t in [i*math.pi/12 for i in range(24)]]
    poly(pts,fill,stroke,0.4)
def trect(x0,x1,y0,y1,z,fill,stroke="#111",sw=0.4):    # rectangle on a top face
    poly([P(x0,y0,z),P(x1,y0,z),P(x1,y1,z),P(x0,y1,z)], fill, stroke, sw)

EXT="#4a4f57"; INST="#d9dce1"; PRINT="#2f6f73"; TRAY="#d8b56a"; SCR="#16263a"; BENCH="#c9a46b"
# ---- bench
box(-90,450,-70,430,-3,0,BENCH,stroke="#8a6d3a"); items[-1]=(10**9,items[-1][1])
# ---- outer frame
for x0 in (0,341):
    for y0 in (0,330): box(x0,x0+20,y0,y0+20,0,510,EXT)
    for z0,z1 in ((0,20),(68,88),(225,245),(319,339),(490,510)): box(x0,x0+20,20,330,z0,z1,EXT)
for z0,z1 in ((0,20),(490,510)): box(20,341,330,350,z0,z1,EXT)
# ---- inner sub-frame
for y0 in (0,330): box(251,271,y0,y0+20,68,245,EXT)
for z0,z1 in ((68,88),(225,245)): box(251,271,20,330,z0,z1,EXT)
box(271,341,0,20,68,88,EXT); box(271,341,330,350,68,88,EXT); box(271,341,330,350,225,245,EXT)
# ---- bottom drawer
def d_drawer(b):
    x0,x1,y0,y1,z0,z1=b
    frect((x0+x1)/2-40,(x0+x1)/2+40,(z0+z1)/2-4,(z0+z1)/2+4,y0-0.1,shade(PRINT,0.6))
box(23,338,0,300,3,65,PRINT,decor=d_drawer)
# ---- PSU
def d_psu(b):
    frect(35,150,150,225,-0.1,SCR)                      # display
    for i in range(6): frect(40+i*18,48+i*18,108,116,-0.1,"#222")   # terminals
    for i,x in enumerate((175,195,215)): frect(x,x+12,205,213,-0.1,"#eee")
    fcircle(222,160,10,-0.1,"#bfc3c9")                  # knob
box(23,248,0,284.5,91,243,INST,decor=d_psu)
# ---- AWG
def d_awg(b):
    frect(35,125,262,325,-0.1,SCR)
    for r in range(3):
        for c in range(3): frect(150+c*14,160+c*14,300-r*14,308-r*14,-0.1,"#eee")
    fcircle(215,300,10,-0.1,"#bfc3c9")
    fcircle(200,262,5,-0.1,"#333"); fcircle(222,262,5,-0.1,"#333")
box(23,237,0,298,248,337,INST,decor=d_awg)
# ---- column drawer
def d_col(b):
    x0,x1,y0,y1,z0,z1=b
    frect((x0+x1)/2-18,(x0+x1)/2+18,(z0+z1)/2-4,(z0+z1)/2+4,y0-0.1,shade(PRINT,0.6))
box(273,338,0,300,91,334,PRINT,decor=d_col)
# ---- rear tray (open top)
def d_tray(b):
    x0,x1,y0,y1,z0,z1=b
    trect(x0+3,x1-3,y0+3,y1-3,z1,shade(TRAY,0.55),sw=0.3)
box(20,341,195,330,342,452,TRAY,decor=d_tray)
# ---- scope
def d_scope(b):
    frect(35,190,392,490,-0.1,SCR)
    for r in range(4):
        for c in range(4): frect(215+c*22,229+c*22,470-r*18,478-r*18,-0.1,"#eee")
    for x in (240,270,300): fcircle(x,415,7,-0.1,"#bfc3c9")
    for i in range(4): fcircle(215+i*30,365,6,-0.1,"#444")
box(23,338,0,135,342,508,INST,decor=d_scope)
# ---- caps on uprights
for x0 in (0,341):
    for y0 in (0,330): box(x0,x0+20,y0,y0+20,510,514,PRINT)

# paint far-to-near
for key,it in sorted(items, key=lambda t:-t[0]):
    _,b,color,stroke,sw,decor=it
    draw_box(b,color,stroke,sw,decor)

# bounds
allp=[P(x,y,z) for x in (-90,450) for y in (-70,430) for z in (0,514)]
us=[p[0] for p in allp]; vs=[p[1] for p in allp]
u0,u1,v0,v1=min(us)-20,max(us)+20,min(vs)-40,max(vs)+20
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{u0:.0f} {v0:.0f} {u1-u0:.0f} {v1-v0:.0f}" width="1000" font-family="Helvetica, Arial, sans-serif">'
     f'<rect x="{u0}" y="{v0}" width="{u1-u0}" height="{v1-v0}" fill="#f4f1ea"/>'
     + "\n".join(out) +
     f'<text x="{u0+20}" y="{v0+30}" font-size="16" font-weight="bold" fill="#333">Bench stack — v5, option B</text>'
     f'<text x="{u0+20}" y="{v0+48}" font-size="10" fill="#555">Black 2020 frame · printed drawers and caps (teal) · rear tray (tan) · isometric, not to be scaled from</text></svg>')
open('/mnt/user-data/outputs/bench-stack-impression.svg','w').write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to='/mnt/user-data/outputs/bench-stack-impression.png', output_width=2000)
cairosvg.svg2png(bytestring=svg.encode(), write_to='check.png', output_width=1200)
print("ok")
