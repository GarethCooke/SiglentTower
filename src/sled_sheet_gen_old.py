import math, cairosvg
out=[]
def emit(s): out.append(s)
def rect(x,y,w,h,fill="none",stroke="#222",sw=0.8,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def text(x,y,s,size=9,anchor="start",weight="normal",fill="#222",rot=None):
    s=s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    r=f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    emit(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{r}>{s}</text>')
def line(x1,y1,x2,y2,stroke="#222",sw=0.6,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def poly(pts,fill,stroke="#222",sw=0.8):
    emit('<polygon points="'+" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def hdim(x1,x2,y,label,size=8):
    line(x1,y-4,x1,y+4,"#0a4");line(x2,y-4,x2,y+4,"#0a4");line(x1,y,x2,y,"#0a4");text((x1+x2)/2,y-2,label,size,"middle",fill="#0a4")
def vdim(y1,y2,x,label,size=8):
    line(x-4,y1,x+4,y1,"#0a4");line(x-4,y2,x+4,y2,"#0a4");line(x,y1,x,y2,"#0a4");text(x+3,(y1+y2)/2+3,label,size,fill="#0a4")
EXT="#9aa4b1"; SLED="#2f6f73"; INST="#eef1f5"; TRAY="#fff3d6"

# ---------- A: side elevation, scope level, closed and extended (scale 1) ----------
def side(ox,oy,pull,title):
    def sz(z): return oy+(520-z)
    def sr(y0,y1,z0,z1,**k): rect(ox+y0, sz(z1), y1-y0, z1-z0, **k)
    text(ox,oy-8,title,11,weight="bold")
    # frame: front/rear upright stubs, scope rail 311-331, top rail 490-510 (clipped), tray
    sr(0,20,300,520,fill=EXT); sr(330,350,300,520,fill=EXT)
    sr(20,330,311,331,fill=EXT)
    sr(20,330,490,510,fill=EXT); sr(20,341-20,510,513,fill="#7d8896")
    # T-slot symbol on rail top
    for y in range(24,330,12): line(ox+y,sz(331),ox+y+6,sz(331),"#fff",1.2)
    # tray: floor + rear wall + low front lip
    b0=195-pull
    sr(b0-5,b0+15,331,346,fill=SLED,stroke="#111"); sr(b0+115,b0+135,331,346,fill=SLED,stroke="#111")
    sr(b0,b0+135,346,349,fill=TRAY,stroke="#c60"); sr(b0+132,b0+135,346,456,fill=TRAY,stroke="#c60"); sr(b0,b0+3,346,366,fill=TRAY,stroke="#c60")
    text(ox+b0+67,sz(420),"BOX on the sled: 321 × 135 × 110, 20 mm front lip; lifts out sideways",6.5,"middle",fill="#c60")
    # sled slider: body 331-346, 250 long from y 3 (moves with pull)
    s0=3-pull
    sr(s0,s0+327,331,346,fill=SLED,stroke="#111")
    # T-foot under body inside the slot (only where over the rail)
    f0=max(s0,20); f1=min(s0+327,330)
    sr(f0,f1,326.5,331,fill=SLED,stroke="#111")
    # rear cup boss & front pad
    sr(s0+215,s0+250,346,351,fill=SLED,stroke="#111")  # cup wall sketch
    # front cross bar (handle/facia) y 0-3 at scope front
    sr(s0-3,s0,341,355,fill=SLED,stroke="#111")
    # scope: bumpers 14 (rear), stands 11.5 (front), body 355-507, depth 135 incl. bumpers
    sr(s0,s0+108,355,507,fill=INST); sr(s0+103,s0+135,341,355,fill="#444"); sr(s0+10,s0+53,343.5,355,fill="#888")
    text(ox+s0+54,sz(430),"SDS1104X-E",9,"middle","bold")
    # stops
    sr(255,262,331,336,fill="#c00",stroke="#800"); text(ox+258,sz(325),"push-in stop (T-nut)",5.5,"middle",fill="#c00")
    sr(98,104,331,338,fill="#c00",stroke="#800"); text(ox+101,sz(303),"pull-out stop (M5 in side slot)",5.5,"middle",fill="#c00")
    line(ox-160,sz(300),ox+360,sz(300),"#999",0.4)
    return sz
sz=side(300,70,0,"A — SCOPE SLED, closed (side view, front at left)")
hdim(300+20,300+330,sz(311)+30,"scope rail 310, top slot",7)
hdim(300+3,300+330,sz(346)-6,"slider 327 (ASA, 20 W × 15 H + T-foot; print diagonal)",7)
vdim(sz(311),sz(331),300+352,"20",7); vdim(sz(331),sz(346),300+352,"15",7); vdim(sz(346),sz(355),300+352,"cups/pads 9",7)
sz=side(300,340,140,"B — SLED pulled 140: box now at y 55–190, in the clear zone; remove right top tile, slide box out to the right (350 clear)")
hdim(300-137,300+3,sz(300)+12,"140 travel",7); hdim(300+20,300+190,sz(346)-6,"170 engaged",7)
text(300+125,sz(480),"box exits → right, through the side",8,"middle",fill="#c60")

# ---------- C: cross-section through rail + slider (scale 3) ----------
ox,oy=80,610; S=3
text(ox,oy-8,"C — SECTION through scope rail and slider (×3)",11,weight="bold")
def cx(x): return ox+x*S
def cz(z): return oy+(400-z)*S
# 2020 profile approx
poly([(cx(0),cz(311)),(cx(20),cz(311)),(cx(20),cz(331)),(cx(13.1),cz(331)),(cx(13.1),cz(329.2)),(cx(15.5),cz(329.2)),(cx(15.5),cz(325)),(cx(4.5),cz(325)),(cx(4.5),cz(329.2)),(cx(6.9),cz(329.2)),(cx(6.9),cz(331)),(cx(0),cz(331))],EXT)
# slider: T-foot 11 wide x 4 in channel, neck 6, body 20x15 with inward arm 8 thick
poly([(cx(4.7),cz(325.3)),(cx(15.3),cz(325.3)),(cx(15.3),cz(329.3)),(cx(13),cz(329.3)),(cx(13),cz(331.2)),(cx(20),cz(331.2)),(cx(20),cz(338)),(cx(82),cz(338)),(cx(82),cz(346)),(cx(0),cz(346)),(cx(0),cz(331.2)),(cx(7),cz(331.2)),(cx(7),cz(329.3)),(cx(4.7),cz(329.3))],SLED,"#111")
# cup recess in arm at bumber position (centre x 62, r16, 5 deep)
rect(cx(46),cz(346),cx(78)-cx(46),(346-341)*S,fill="#fff",stroke="#111")
text(cx(62),cz(343.2),"cup Ø32.6 × 5",6,"middle")
rect(cx(46),cz(355),cx(78)-cx(46),(355-341)*S,fill="#444",stroke="#111"); text(cx(62),cz(349),"bumper",6,"middle",fill="#fff")
rect(cx(23),cz(400),cx(140)-cx(23),(400-355)*S,fill=INST); text(cx(80),cz(378),"scope body",8,"middle")
hdim(cx(4.7),cx(15.3),cz(323),"T-foot 10.6 (slot 11)",6); hdim(cx(7),cx(13),cz(332.5),"neck 6 (opening 6.2)",6)
hdim(cx(20),cx(82),cz(349),"arm 62 reach",6); vdim(cz(346),cz(331.2),cx(-10),"15 body",6); vdim(cz(338),cz(346),cx(84),"8 arm",6)
hdim(cx(0),cx(20),cz(308),"2020",6)

# ---------- notes ----------
nx,ny=520,640
text(nx,ny,"LOADS AND CHECKS",11,weight="bold"); ny+=16
notes=[
"Scope 3 kg → 15 N per slider. Closed: pure compression on the rail top, nothing to check.",
"Pulled 140: scope CoG sits ~90 mm ahead of the rail's front end with 170 mm of slider still in the slot; box (~1 kg) rides behind the scope.",
"  Lever ≈ 0.5 : the rear of the T-foot pulls UP on the aluminium slot lip with ~8 N; the front bears DOWN on the rail end with ~30 N.",
"  Slot lip: aluminium, 1.8 mm — this joint carries 3D-printer gantries; 16 N is nothing.",
"  T-foot / neck (ASA): 16 N over 90 mm of engaged foot → < 0.1 MPa bearing, ~0.5 MPa shear at the neck. Yield 40 MPa.",
"  Slider body 20 × 15 ASA as a 140 mm cantilever with 15 N at the tip: bending stress ≈ 2.8 MPa; sag ≈ 0.9 mm. Acceptable.",
"  (An 8 mm body would sag ~5 mm — hence 15 mm, and the scope rails drop 7 mm to keep the scope at the same height.)",
"  Play: 0.2 mm slot clearance × lever ≈ 0.5 mm droop at the bezel when fully out. Print the T-foot 10.6 wide for a light sliding fit; sand if tight.",
"Arms 62 mm × 8 mm thick carrying the bumper cups: same section as the PSU cradle, 15 N → ~1 MPa.",
"Front bar 315 × 14 × 12 with J-pull = handle + reveal filler; two rear cross bars 321 × 20 × 15 carry the box. Sled = 2 sliders + 3 bars, one rigid frame.",
"Box guides on the sled: 10 mm lips along the front and rear bars (full width, 1 mm play) and an end stop on the left slider — the box slides in from the right between the lips until it meets the stop.",
"ACCESS: pull sled 140 → box sits at y 55–190 → fold down the FRONT section (y 20–250) of the top-right side tile (bottom hinge) → slide box out to the right (321 long, 350 clear). Scope never lifts.",
"Stops: push-in = T-nut in the top slot behind the slider; pull-out = M5 + T-nut in the rail's inner side slot that the rear arm meets at 140, with a TPU cap on the screw head so the sled stops softly.",
"Lube: PTFE dry spray in the slot. Leads: 150 mm slack on mains and probes behind the scope.",
"DOOR: 230 × 143 × 3 ASA hex tile, bottom-hinged on two printed knuckles (3 mm pin), axis z 341 outboard of the upright, opens 180. Catch: 2 pairs of Ø10 × 2 magnets at the top corners — door side in 12 × 12 × 3 bosses on the inside face, frame side: front catch is a rounded L-bracket (r 2) bolted to the front upright's inner slot and hung in the top rail's slot; rear catch is a tab grown from the fixed rear tile's border. Faces 0.5 mm apart, pull-apart in the opening direction. Pockets 10.4 × 2.2, CA glue, mark polarity. All edges r 2.",
"Layout change for v13: scope rails 311–331 (were 318–338). Scope, tray, top panel, everything else unchanged.",
]
for n in notes: text(nx,ny,n,7.5,fill="#333"); ny+=12
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 920" width="1180" height="920" font-family="Helvetica, Arial, sans-serif"><rect width="1180" height="920" fill="#fff"/>'+"\n".join(out)+'<text x="20" y="908" font-size="8" fill="#888">bench-stack-layout v15 — page 2 of 2: scope sled + box — 2026-09-15</text></svg>'
open('/mnt/user-data/outputs/scope-sled-v1.svg','w').write(svg)
cairosvg.svg2pdf(bytestring=svg.encode(),write_to='/mnt/user-data/outputs/scope-sled-v1.pdf')
cairosvg.svg2png(bytestring=svg.encode(),write_to='sled.png',output_width=1600)
print('ok')
