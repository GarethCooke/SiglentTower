import cairosvg
out=[]
def emit(s): out.append(s)
def poly(pts,fill,stroke="#222",sw=0.8):
    emit('<polygon points="'+" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def rect(x,y,w,h,fill="none",stroke="#222",sw=0.8,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def text(x,y,s,size=9,anchor="start",weight="normal",fill="#222",rot=None):
    s=s.replace("&","&amp;")
    r=f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    emit(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{r}>{s}</text>')
def line(x1,y1,x2,y2,stroke="#222",sw=0.6,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def hdim(x1,x2,y,label,size=8):
    line(x1,y-4,x1,y+4,"#0a4");line(x2,y-4,x2,y+4,"#0a4");line(x1,y,x2,y,"#0a4");text((x1+x2)/2,y-2,label,size,"middle",fill="#0a4")
def vdim(y1,y2,x,label,size=8,side=1):
    line(x-4,y1,x+4,y1,"#0a4");line(x-4,y2,x+4,y2,"#0a4");line(x,y1,x,y2,"#0a4");text(x+3*side,(y1+y2)/2+3,label,size,"start" if side>0 else "end",fill="#0a4")
EXT="#9aa4b1"; SLED="#1f2226"; SLED2="#3a4048"; INST="#efe9d9"; UP="#6b7583"
# ---------------- A: cross-section through the LEFT scope rail and sled (×4), looking from the front ----------------
ox,oy=60,60; S=4
def X(x): return ox+x*S
def Z(z): return oy+(370-z)*S
text(ox,oy-10,"A — SECTION through the left scope rail and sled, looking from the front (×4)",11,weight="bold")
# 2020 rail profile with 4 slots (approx), x 0–20, z 311–331
def rail_profile(x0,z0):
    pts=[]
    # outer boundary with slot notches; build as one polygon: go around clockwise with notches
    o=6.9; i_=13.1; a=1.8; d=6.0  # slot opening 6.2 (6.9..13.1), lip 1.8, channel depth ~6
    P=lambda x,z:(X(x0+x),Z(z0+z))
    seq=[(0,0),(o,0),(o,a),(4.5,a),(4.5,a+4),(15.5,a+4),(15.5,a),(i_,a),(i_,0),(20,0),           # bottom slot
         (20,o),(20-a,o),(20-a,4.5),(20-a-4,4.5),(20-a-4,15.5),(20-a,15.5),(20-a,i_),(20,i_),(20,20),   # right (inner) side slot
         (i_,20),(i_,20-a),(15.5,20-a),(15.5,20-a-4),(4.5,20-a-4),(4.5,20-a),(o,20-a),(o,20),(0,20),   # top slot
         (0,i_),(a,i_),(a,15.5),(a+4,15.5),(a+4,4.5),(a,4.5),(a,o),(0,o)]                                # left (outer) side slot
    poly([P(x,z) for x,z in seq],EXT)
    rect(X(x0+8.5),Z(z0+11.5),3*S,3*S,fill="#fff",stroke="#999")  # centre bore
rail_profile(0,311)
text(X(10),Z(300),"scope rail 2020, z 311–331",7,"middle")
# upright behind (x 0–20) shown faint above the rail
rect(X(0),Z(370),20*S,(370-331)*S,fill="none",stroke="#999",dash="3,3"); text(X(10),Z(362),"front post (behind)",6,"middle",fill="#999")
# sled foot inside the inner side slot: channel x 20-1.8-4 .. 20-1.8 = 14.2..18.2, z 315.5..326.5 ; foot 10.6 × 4
rect(X(14.4),Z(326.3),3.8*S,10.6*S,fill=SLED)
# neck through the opening (z 317.9..324.1 -> 6.2), x 18.2..20
rect(X(18.2),Z(324.0),1.8*S,6.0*S,fill=SLED)
# web x 20.5–23, z 318–337
rect(X(20.5),Z(337),2.5*S,(337-318)*S,fill=SLED)
# beam x 20.5–60, z 337–346
rect(X(20.5),Z(346),39.5*S,9*S,fill=SLED)
# cup recess at bumper (x 46–78 → beyond beam; show partial) and scope
rect(X(23),Z(355),(120-23)*S,(355-341)*S,fill="#ddd",stroke="#888",dash="2,2"); text(X(70),Z(347),"scope feet zone 341–355",6,"middle",fill="#666")
rect(X(23),Z(370),(120-23)*S,(370-355)*S,fill=INST); text(X(70),Z(361),"scope body",8,"middle")
# AWG frame top at 336 (x 23-237)
rect(X(23),Z(336),(120-23)*S,3*S,fill="#e0dbcc",stroke="#888"); text(X(70),Z(333.5),"AWG frame top 336 (1 mm under the beam)",6,"middle",fill="#666")
# dims
hdim(X(14.4),X(18.2),Z(313),"foot 3.8 (channel 4)",6)
vdim(Z(326.3),Z(315.7),X(12),"10.6",6,-1)
vdim(Z(324),Z(318),X(27),"neck 6 (slot 6.2)",6)
hdim(X(20.5),X(23),Z(339.5),"web 2.5",6)
vdim(Z(346),Z(337),X(62),"beam 9",6)
hdim(X(20.5),X(60),Z(348.5),"beam 40",6)
text(X(0),Z(285),"Load path when pulled out: scope → beam → web (shear) → foot → slot lips (down at the front of the foot, up at the rear). Nothing above the rail top is inside the post's column.",7,fill="#333")

# ---------------- B: side elevation of the left rail, closed and at 100 (scale 1) ----------------
def side(ox,oy,pull,title):
    def sz(z): return oy+(520-z)
    def sr(y0,y1,z0,z1,**k): rect(ox+y0,sz(z1),y1-y0,z1-z0,**k)
    text(ox,oy-8,title,11,weight="bold")
    sr(0,20,300,520,fill=UP); sr(330,350,300,520,fill=UP)
    sr(20,330,311,331,fill=EXT)
    for y in range(24,330,10): line(ox+y,sz(321),ox+y+5,sz(321),"#fff",1.2)  # side-slot hint
    # foot (inside the slot) y 120–330 initially
    f0=120-pull; sr(f0,f0+210,316,326,fill=SLED2,stroke="#111")
    # web and beam y 3–330
    b0=3-pull; sr(b0,b0+327,326,337,fill=SLED,stroke="#111"); sr(b0,b0+327,337,346,fill=SLED,stroke="#111")
    # front bar, scope
    sr(b0-0.1,b0+12,337,355,fill="#4a4f57",stroke="#111")
    sr(b0,b0+108,355,507,fill=INST); sr(b0+103,b0+135,341,355,fill="#444"); sr(b0+10,b0+53,343.5,355,fill="#888")
    text(ox+b0+54,sz(430),"SDS1104X-E",9,"middle","bold")
    # box on the sled y 195–330
    x0=195-pull; sr(x0,x0+135,346,349,fill="#4a4f57",stroke="#111"); sr(x0+132,x0+135,346,456,fill="#4a4f57",stroke="#111"); sr(x0,x0+3,346,366,fill="#4a4f57",stroke="#111")
    # stops
    sr(332,338,316,326,fill="#c00",stroke="#800"); text(ox+335,sz(306),"push-in stop (T-nut in side slot)",5.5,"middle",fill="#c00")
    sr(14,20,316,326,fill="#c00",stroke="#800"); text(ox+17,sz(306),"pull-out stop: T-nut + TPU cap at the slot's front end",5.5,"start",fill="#c00")
    line(ox-160,sz(300),ox+360,sz(300),"#999",0.4)
    return sz
sz=side(700,70,0,"B — closed (side view, front at left)")
hdim(700+120,700+330,sz(316)+8,"foot 210, y 120–330",6.5); hdim(700+3,700+330,sz(346)-6,"beam 327",6.5)
sz=side(700,340,100,"C — pulled 100: foot still 20 mm inside the slot; box at y 95–230, clear of the rear 100 mm")
hdim(700-97,700+3,sz(300)+12,"100 travel",7); hdim(700+20,700+230,sz(316)+8,"210 engaged (20–230)",6.5)
# notes
nx,ny=60,700
text(nx,ny,"NOTES",11,weight="bold"); ny+=15
for n in ["Foot: printed ASA, 10.6 × 3.8 section, 210 long — a drop-in T-nut stretched to a runner. Fit: light sliding; sand the flanks if tight. PTFE dry spray in the channel.",
          "Web: 2.5 mm, in the 3 mm gap between rail and instrument frames; shear only. Beam: 40 × 9, limited by the AWG frame 1 mm below — hence 100 mm travel, not 140 (sag ≈ 1 mm at the front).",
          "Right side is the mirror image, riding the right rail's inner side slot. The two sides are joined by the front bar and the two rear cross bars into one sled.",
          "Top slots of the scope rails stay free for the side-tile clips above."]:
    text(nx,ny,n,7.5,fill="#333"); ny+=12
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 780" width="1180" height="780" font-family="Helvetica, Arial, sans-serif"><rect width="1180" height="780" fill="#fff"/>'+"\n".join(out)+'<text x="20" y="770" font-size="8" fill="#888">sled mechanism v2 (v18) — 2026-09-15</text></svg>'
cairosvg.svg2pdf(bytestring=svg.encode(),write_to='/mnt/user-data/outputs/sled-mechanism-v2.pdf')
cairosvg.svg2png(bytestring=svg.encode(),write_to='sled2.png',output_width=1600)
print('ok')
