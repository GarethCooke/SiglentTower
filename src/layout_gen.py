# Bench stack layout — dimensioned SVG, 1 unit = 1 mm
W_OUT   = 361      # overall width (uprights outside)
W_IN    = 321      # clear width between uprights / side rails
D_OUT   = 350      # overall depth
H_OUT   = 510      # upright length
EXT     = 20       # 2020

# vertical layout (z from bench)
BASE_RAIL   = (0, 20)
DRAWER      = (3, 65)          # drawer body
PSU_RAIL    = (68, 88)
PSU         = (91, 243)        # feet bottom .. top incl. bezel (152)
PSU_BODY    = (103, 240)       # body 137 on 11.5 feet; frame 143 (100–243)
AWG_RAIL    = (227.5, 247.5)
AWG         = (248, 336)       # bezel 88 tall; body 82 sits on 3.5 pads at 251.5
SCOPE_RAIL  = (311, 331)     # dropped 7 for the 15 mm sled sliders
SCOPE       = (341, 507)       # 166 incl. feet
SCOPE_BODY  = (355, 507)       # 152 body
TOP_RAIL    = (490, 510)
TRAY        = (342, 452)       # 110 tall walls

# depth (y from front face of front uprights)
SCOPE_D = 135; AWG_D = 260; PSU_D = 284.5; PSU_KNOB = 17
TRAY_Y  = (195, 330)
DRAWER_D = 300

# widths (x from outside of left upright)
def centred(w): return ((W_OUT - w)/2, (W_OUT + w)/2)
SCOPE_X = (23, 338)
AWG_X   = (23, 237)
AWG_BODY_X = (26.5, 233.5)
PSU_X   = (25.75, 245.25)
PSU_BEZ = (23, 248)
COL_X   = (273, 338)
COL_Z   = (91, 336)
MINI_X  = (242, 268)
INNER_X = (251, 271)
INNER_Z = (68, 247.5)
TIE_X   = (271, 341)
PSU_VENT = (35, 155)
DRAWER_X = (23, 338)
RACK_W  = 45

out = []
def emit(s): out.append(s)

def rect(x, y, w, h, fill="none", stroke="#222", sw=0.8, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')

def text(x, y, s, size=9, anchor="start", weight="normal", fill="#222", rot=None):
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    emit(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{r}>{s}</text>')

def line(x1,y1,x2,y2, stroke="#222", sw=0.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def hdim(x1, x2, y, label, off=0, size=8):
    # horizontal dimension line at sheet y
    line(x1, y-4, x1, y+4, "#0a4", 0.6); line(x2, y-4, x2, y+4, "#0a4", 0.6)
    line(x1, y, x2, y, "#0a4", 0.6)
    text((x1+x2)/2, y-2+off, label, size, "middle", fill="#0a4")

def vdim(y1, y2, x, label, size=8, side=1):
    line(x-4, y1, x+4, y1, "#0a4", 0.6); line(x-4, y2, x+4, y2, "#0a4", 0.6)
    line(x, y1, x, y2, "#0a4", 0.6)
    text(x + 3*side, (y1+y2)/2 + 3, label, size, "start" if side>0 else "end", fill="#0a4")

EXT_FILL = "#9aa4b1"; INST_FILL = "#eef1f5"; ZONE = "#d9534f"

# ---------------- FRONT ELEVATION ----------------
FX, FY = 90, 70            # sheet origin; z=0 at FY + H_OUT
def fz(z): return FY + H_OUT - z
def fr(x0,x1,z0,z1,**kw): rect(FX+x0, fz(z1), x1-x0, z1-z0, **kw)

text(FX, FY-30, "FRONT ELEVATION", 12, weight="bold")
text(FX, FY-17, "1 unit = 1 mm. Instruments to stated dimensions; extrusion 2020.", 8, fill="#555")

# rear cross rails (behind)
for z0,z1 in (BASE_RAIL, TOP_RAIL): fr(EXT, W_OUT-EXT, z0, z1, fill="#c5ccd6", stroke="#777")
# uprights
fr(0, EXT, 0, H_OUT, fill=EXT_FILL); fr(W_OUT-EXT, W_OUT, 0, H_OUT, fill=EXT_FILL)
# side rails seen end-on (inside the upright plane) - mark with small x
for z0,z1 in (PSU_RAIL, AWG_RAIL, SCOPE_RAIL):
    for x0 in (0, W_OUT-EXT):
        fr(x0, x0+EXT, z0, z1, fill="#7d8896", stroke="#333")
# drawer
fr(*DRAWER_X, DRAWER[0], 86, fill=INST_FILL); text(FX+W_OUT/2, fz(DRAWER[0]+40), "DRAWER  315 × 60 × 300 — facia 3–86; housing top 64–67", 9, "middle")
# PSU
fr(*PSU_BEZ, *PSU, fill=INST_FILL)
for x in (PSU_X[0]+20, PSU_X[1]-20): fr(x-8, x+8, PSU[0], PSU_BODY[0], fill="#555", stroke="#333")
fr(*PSU_X, PSU_BODY[0], PSU_BODY[1], fill="none", stroke="#999", dash="2,2")
text(FX+135, fz(170), "SPD3303X-E", 11, "middle", "bold"); text(FX+135, fz(155), "front frame 225 W × 143 H; body 219.5 × 137 × 284.5 (dashed); feet 11.5", 8, "middle")
# AWG
fr(*AWG_X, *AWG, fill=INST_FILL)
fr(*AWG_BODY_X, 251.5, 333.5, fill="none", stroke="#999", dash="2,2")
text(FX+130, fz(296), "SDG2082X (bumpers off)", 11, "middle", "bold"); text(FX+130, fz(281), "front frame 214 W × 88 H; body 207 × 82 × 260 (dashed)", 8, "middle")
# scope
fr(*SCOPE_X, *SCOPE, fill=INST_FILL)
fr(SCOPE_X[0], SCOPE_X[1], SCOPE[0], SCOPE_BODY[0], fill="#dfe3e8", stroke="#888", dash="3,2")
text(FX+W_OUT/2, fz(445), "SDS1104X-E", 11, "middle", "bold"); text(FX+W_OUT/2, fz(430), "315 W × 166 H (152 body + 14 feet) × 135 D", 8, "middle")
text(FX+W_OUT/2+40, fz(347), "feet / cradle zone 14", 7, "middle", fill="#666")
# inner sub-frame (option 2)
fr(*INNER_X, *INNER_Z, fill=EXT_FILL)                                   # inner uprights
for z0,z1 in (PSU_RAIL, AWG_RAIL): fr(*INNER_X, z0, z1, fill="#7d8896", stroke="#333")   # inner rails end-on
fr(*TIE_X, *PSU_RAIL, fill="#c5ccd6", stroke="#777")                     # front tie, PSU level
text(FX+306, fz(PSU_RAIL[0])-3, "tie 70 (front, PSU level)", 6, "middle", fill="#555")
text(FX+261, fz(110), "inner upright 179.5", 6, "middle", fill="#fff", rot=-90)
# column drawer
fr(*COL_X, *COL_Z, fill="#fff3d6", stroke="#c60", sw=1)
text(FX+(COL_X[0]+COL_X[1])/2-8, fz(212), "COLUMN DRAWER", 9, "middle", "bold", fill="#c60", rot=-90)
text(FX+(COL_X[0]+COL_X[1])/2+8, fz(212), "65 W × 245 H × 300 D (~4.7 L)", 7, "middle", fill="#c60", rot=-90)
# mini drawer beside AWG
fr(*MINI_X, *AWG, fill="#fff3d6", stroke="#c60", sw=1)
text(FX+256, fz(292), "MINI 26×85×180", 6, "middle", "bold", fill="#c60", rot=-90)
# side panels (in outer T-slots) and top panel
for x0 in (8.5, 349.5): fr(x0, x0+3, 20, 490, fill="#7d8896", stroke="#333", dash="2,2")
fr(EXT, W_OUT-EXT, 510, 513, fill="#7d8896", stroke="#333")
text(FX+W_OUT/2, fz(522), "top panel 321 × 310 × 3 on top rails, z 510–513 (solid, 2 tiles); caps 510–514 at corners", 6, "middle", fill="#333")
text(FX+5, fz(300), "hex side panel 310 × 470 × 3 (3 tiles)", 6, "middle", fill="#333", rot=-90)
# PSU side-vent air channel
fr(PSU_BEZ[1], COL_X[0], PSU[0], PSU[1], fill="none", stroke=ZONE, dash="4,3")
text(FX+(PSU_BEZ[1]+INNER_X[0])/2, fz(160), "air", 5, "middle", fill=ZONE, rot=-90)
# TPU feet + bench line
for x0 in (-2, W_OUT-EXT-2): fr(x0, x0+EXT+4, -6, 0, fill="#c9d3d0", stroke="#333")
text(FX+W_OUT/2, fz(-6)+10, "TPU feet 24 × 24 × 6, 5 mm spigot into extrusion bore (×4)", 7, "middle", fill="#333")
line(FX-30, fz(-6), FX+W_OUT+30, fz(-6), "#000", 1.2); text(FX-30, fz(-6)+10, "bench", 7, fill="#555")

# dimensions - horizontal
hdim(FX, FX+W_OUT, fz(-6)+22, "361 overall")
hdim(FX+EXT, FX+W_OUT-EXT, fz(-6)+38, "321 clear between uprights / rails")
hdim(FX+SCOPE_X[0], FX+SCOPE_X[1], FY-6, "315 scope (3 mm each side)")
hdim(FX+AWG_X[0], FX+AWG_X[1], fz(AWG[1])-6, "214 AWG frame")
hdim(FX+AWG_X[1], FX+MINI_X[0], fz(AWG[1])-6, "5"); hdim(FX+MINI_X[0], FX+MINI_X[1], fz(AWG[1])-6, "26"); hdim(FX+MINI_X[1], FX+COL_X[0], fz(AWG[1])-6, "5")
hdim(FX+COL_X[0], FX+COL_X[1], fz(AWG[1])-6, "65 column")
hdim(FX+PSU_BEZ[1], FX+INNER_X[0], fz(PSU[1])-6, "3")
hdim(FX+PSU_BEZ[0], FX+PSU_BEZ[1], fz(PSU[1])-6, "225 PSU frame")
# dimensions - vertical (right side)
DX = FX + W_OUT + 18
vdim(fz(-6), fz(514), DX+50, "520 overall (6 feet + 510 uprights + 4 caps)")
vdim(fz(DRAWER[0]), fz(DRAWER[1]), DX, "62 drawer")
vdim(fz(PSU[0]), fz(PSU[1]), DX, "152 PSU")
vdim(fz(AWG[0]), fz(AWG[1]), DX, "88 AWG")
vdim(fz(SCOPE[0]), fz(SCOPE[1]), DX, "166 scope")
vdim(fz(PSU[1]), fz(AWG[0]), DX+22, "5")
vdim(fz(AWG[1]), fz(SCOPE[0]), DX+22, "5")
# rail heights (left side)
LX = FX - 14
for (z0,z1),lab in ((BASE_RAIL,"base rail 0–20"),(PSU_RAIL,"PSU rail 68–88"),(AWG_RAIL,"AWG rail 227.5–247.5"),(SCOPE_RAIL,"scope rail 311–331"),(TOP_RAIL,"top rail 490–510")):
    line(LX, fz(z1), FX, fz(z1), "#0a4", 0.5, "2,2"); text(LX-2, fz(z1)-2, lab, 7, "end", fill="#0a4")
for z,lab in ((PSU[0],"91 (cup floor 4)"),(251.5,"251.5"),(SCOPE[0],"341")):
    line(LX, fz(z), FX, fz(z), "#c60", 0.5, "1,2"); text(LX-2, fz(z)+9, f"pad top z={lab}", 7, "end", fill="#c60")

# ---------------- SIDE ELEVATION (from right, front at left) ----------------
SX, SY = 600, 70
def sz(z): return SY + H_OUT - z
def sr(y0,y1,z0,z1,**kw): rect(SX+y0, sz(z1), y1-y0, z1-z0, **kw)
text(SX, SY-30, "SIDE ELEVATION (right side, front at left)", 12, weight="bold")
text(SX, SY-17, "Everything inside the frame sits 3 mm behind the front plane; drawer facias fill the 3 mm, flush with the uprights.", 8, fill="#555")
# rails
for z0,z1 in (BASE_RAIL, PSU_RAIL, AWG_RAIL, SCOPE_RAIL, TOP_RAIL): sr(EXT, D_OUT-EXT, z0, z1, fill=EXT_FILL)
sr(0, EXT, 0, H_OUT, fill=EXT_FILL); sr(D_OUT-EXT, D_OUT, 0, H_OUT, fill=EXT_FILL)
# drawer
sr(3, DRAWER_D+3, *DRAWER, fill=INST_FILL); sr(0, 3, 3, 86, fill="#2f6f73", stroke="#111"); text(SX+DRAWER_D/2, sz(30), "drawer 300 deep, facia 0–3 flush with frame", 8, "middle")
# PSU
sr(3, PSU_D+3, *PSU, fill=INST_FILL); sr(3-PSU_KNOB, 3, PSU[0]+40, PSU[1]-40, fill="#dfe3e8", stroke="#888")
text(SX+PSU_D/2, sz(170), "PSU 284.5 body, knobs +17", 9, "middle")
# AWG
sr(3, AWG_D+3, *AWG, fill=INST_FILL); text(SX+AWG_D/2, sz(288), "AWG body 260; frame at 3", 9, "middle")
# scope
sr(3, SCOPE_D+3, *SCOPE, fill=INST_FILL); sr(3, SCOPE_D+3, SCOPE[0], SCOPE_BODY[0], fill="#dfe3e8", stroke="#888", dash="3,2")
text(SX+SCOPE_D/2, sz(440), "scope", 9, "middle"); text(SX+SCOPE_D/2, sz(425), "135 deep", 8, "middle")
# tray
sr(*TRAY_Y, *TRAY, fill="#fff3d6", stroke="#c60")
text(SX+(TRAY_Y[0]+TRAY_Y[1])/2, sz(420), "REAR TRAY", 9, "middle", "bold", fill="#c60")
text(SX+(TRAY_Y[0]+TRAY_Y[1])/2, sz(405), "135 D × 110 H, two halves", 7, "middle", fill="#c60")
text(SX+(TRAY_Y[0]+TRAY_Y[1])/2, sz(392), "BM867s on edge + BM22s + leads", 7, "middle", fill="#c60")
# clearance zones
sr(SCOPE_D, TRAY_Y[0], SCOPE[0], SCOPE[1], fill="none", stroke=ZONE, dash="4,3"); text(SX+160, sz(500), "60 vent/plug", 7, "middle", fill=ZONE, rot=-90)
sr(AWG_D+3, D_OUT+40, AWG[0], AWG[1], fill="none", stroke=ZONE, dash="4,3"); text(SX+D_OUT+30, sz(292), "plugs ≥50", 7, "middle", fill=ZONE, rot=-90)
sr(PSU_D, D_OUT+40, PSU[0], PSU[1], fill="none", stroke=ZONE, dash="4,3"); text(SX+D_OUT+30, sz(167), "fan exhaust ≥50 — keep open", 7, "middle", fill=ZONE, rot=-90)
sr(EXT, D_OUT-EXT, 20, 490, fill="none", stroke="#333", dash="4,3", sw=1)
# hex perforation pattern (illustrative) on the side panel
import math
r=4.2; dx=r*2+2.5; dy=(r*2+2.5)*0.866
row=0; yy=30
while yy<482:
    xx=EXT+8+(dx/2 if row%2 else 0)
    while xx<D_OUT-EXT-8:
        pts=" ".join(f"{SX+xx+r*math.cos(math.pi/6+k*math.pi/3):.1f},{sz(yy)-r*math.sin(math.pi/6+k*math.pi/3):.1f}" for k in range(6))
        emit(f'<polygon points="{pts}" fill="none" stroke="#8a93a0" stroke-width="0.35"/>')
        xx+=dx
    yy+=dy; row+=1
for t in (177,334): line(SX+EXT, sz(t), SX+D_OUT-EXT, sz(t), "#333", 0.8, "6,3")
rect(SX+EXT+4, sz(486), D_OUT-2*EXT-8, 12, fill="#fff", stroke="#333", sw=0.4)
text(SX+D_OUT/2, sz(477), "HEX SIDE PANEL in outer T-slot — 3 tiles 310 × ~157 × 3 ASA; instruments shown through", 7, "middle", "bold", fill="#333")
sr(EXT, D_OUT-EXT, 510, 513, fill="#7d8896", stroke="#333")
sr(-2, EXT+2, -6, 0, fill="#c9d3d0", stroke="#333"); sr(D_OUT-EXT-2, D_OUT+2, -6, 0, fill="#c9d3d0", stroke="#333")
line(SX-40, sz(-6), SX+D_OUT+60, sz(-6), "#000", 1.2)
# dims
hdim(SX, SX+D_OUT, sz(-6)+22, "350 overall depth")
hdim(SX+EXT, SX+D_OUT-EXT, sz(-6)+38, "310 side rails")
hdim(SX, SX+3, SY-6, "3"); hdim(SX+3, SX+SCOPE_D+3, SY-6, "135")
hdim(SX+SCOPE_D+3, SX+TRAY_Y[0], SY-6, "57")
hdim(SX+TRAY_Y[0], SX+TRAY_Y[1], SY-6, "135 tray")
hdim(SX+3, SX+AWG_D+3, sz(AWG[1])-6, "260")
hdim(SX+AWG_D+3, SX+D_OUT, sz(AWG[1])-6, "87")
vdim(sz(TRAY[0]), sz(TRAY[1]), SX+D_OUT+12, "110")

# ---------------- PLAN ----------------
PX, PY = 90, 700    # front at top of view
def pr(x0,x1,y0,y1,**kw): rect(PX+x0, PY+y0, x1-x0, y1-y0, **kw)
text(PX, PY-30, "PLAN (front at top)", 12, weight="bold")
text(PX, PY-17, "Scope centred; AWG and PSU hard left (3 mm); column right; interior recessed 3 mm, facias flush.", 8, fill="#555")
# rails & uprights
for x0 in (0, W_OUT-EXT): pr(x0, x0+EXT, EXT, D_OUT-EXT, fill=EXT_FILL)
pr(EXT, W_OUT-EXT, D_OUT-EXT, D_OUT, fill="#c5ccd6", stroke="#777")   # rear cross rails
for x0,y0 in ((0,0),(W_OUT-EXT,0),(0,D_OUT-EXT),(W_OUT-EXT,D_OUT-EXT)): pr(x0,x0+EXT,y0,y0+EXT, fill="#6b7583")
# footprints
pr(*AWG_BODY_X, 3, AWG_D+3, fill="none", stroke="#666", dash="5,3"); text(PX+130, PY+AWG_D-8, "AWG body 207 × 260", 8, "middle", fill="#666")
pr(*PSU_BEZ, 3, PSU_D+3, fill="none", stroke="#666", dash="2,2"); text(PX+135, PY+PSU_D-8, "PSU 225 × 284.5", 8, "middle", fill="#666")
pr(*SCOPE_X, 3, SCOPE_D+3, fill=INST_FILL); text(PX+W_OUT/2, PY+SCOPE_D/2+4, "SCOPE 315 × 135", 10, "middle", "bold")
# tray halves
pr(EXT, W_OUT/2, *TRAY_Y, fill="#fff3d6", stroke="#c60"); pr(W_OUT/2, W_OUT-EXT, *TRAY_Y, fill="#fff3d6", stroke="#c60")
text(PX+W_OUT/2, PY+TRAY_Y[0]+40, "REAR TRAY — two halves, 160.5 each", 8, "middle", "bold", fill="#c60")
# slots in tray
pr(EXT+10, EXT+10+208.5, TRAY_Y[0]+10, TRAY_Y[0]+76, fill="none", stroke="#c60", dash="2,2"); text(PX+EXT+10+104, PY+TRAY_Y[0]+62, "BM867s slot 208.5 × 66 (on edge)", 7, "middle", fill="#c60")
pr(EXT+230, EXT+230+53, TRAY_Y[0]+10, TRAY_Y[0]+22, fill="none", stroke="#c60", dash="2,2"); text(PX+EXT+256, PY+TRAY_Y[0]+31, "BM22s 53×12", 6, "middle", fill="#c60")
text(PX+W_OUT/2, PY+TRAY_Y[0]+110, "leads / spares 321 × ~45", 7, "middle", fill="#c60")
# inner sub-frame
pr(*INNER_X, EXT+3, D_OUT-EXT, fill=EXT_FILL, extra='fill-opacity="0.45"')                       # inner rails (307)
pr(*INNER_X, 3, EXT+3, fill="#6b7583"); pr(*INNER_X, D_OUT-EXT, D_OUT, fill="#6b7583")  # inner uprights (front one at y 3–23)
pr(*TIE_X, 3, EXT+3, fill="#c5ccd6", stroke="#777"); pr(*TIE_X, D_OUT-EXT, D_OUT, fill="#c5ccd6", stroke="#777")
text(PX+261, PY+260, "inner rails 310 (PSU + AWG level)", 6, "middle", fill="#333", rot=-90)
# side panels in outer slots, mini drawer
for x0 in (8.5, 349.5): pr(x0, x0+3, EXT, D_OUT-EXT, fill="#7d8896", stroke="#333")
pr(*MINI_X, 0, 183, fill="none", stroke="#c60", dash="3,2"); text(PX+255, PY+90, "mini 26×180", 6, "middle", fill="#c60", rot=-90)
# column footprint
pr(*COL_X, 0, 303, fill="none", stroke="#c60", dash="6,3", sw=1.2); text(PX+(COL_X[0]+COL_X[1])/2, PY+100, "COLUMN 65 × 300 (below tray level)", 7, "middle", "bold", fill="#c60", rot=-90)
# vent markers
for x in (AWG_BODY_X[0], AWG_BODY_X[1]):
    line(PX+x, PY+110, PX+x, PY+190, "#c60", 2)
text(PX+AWG_X[0]-4, PY+150, "AWG side vent 110–190", 6, "end", fill="#c60", rot=-90)
text(PX+AWG_X[1]+5, PY+225, "AWG vent", 6, "start", fill="#c60", rot=-90)
for x in (PSU_BEZ[0]+2, PSU_BEZ[1]-2):
    line(PX+x, PY+PSU_VENT[0], PX+x, PY+PSU_VENT[1], "#36c", 2)
text(PX+PSU_BEZ[1]+12, PY+60, "PSU vent 35–155 both sides", 6, "start", fill="#36c", rot=-90)
# dims
hdim(PX, PX+W_OUT, PY+D_OUT+22, "361")
vdim(PY, PY+D_OUT, PX+W_OUT+14, "350")
vdim(PY, PY+SCOPE_D, PX+W_OUT+34, "135")
vdim(PY+TRAY_Y[0], PY+TRAY_Y[1], PX+W_OUT+34, "135")
hdim(PX+COL_X[0], PX+COL_X[1], PY-6, "65")

# ---------------- CUT LIST / NOTES ----------------
CX, CY = 600, 690
text(CX, CY, "2020 EXTRUSION CUT LIST", 12, weight="bold")
rows = [("Uprights", "4", "510"), ("Side rails (front–rear), 5 levels", "10", "310"), ("Rear cross rails (base + top)", "2", "321"), ("Inner rails (PSU + AWG level)", "4", "307"), ("Inner uprights", "2", "179.5"), ("Ties inner→outer (PSU front+rear, AWG rear)", "3", "70"), ("Total", "", "7,579 mm → buy 8 × 1,000 mm")]
y = CY+18
for a,b,c in rows:
    text(CX, y, a, 9, weight="bold" if a=="Total" else "normal"); text(CX+210, y, b, 9, "middle"); text(CX+240, y, c, 9); y += 14
text(CX, y+4, "Joints: 40 × 2020 corner brackets, 80 × M5 T-nuts, 80 × M5×8 button head. Feet: 4 printed.", 8, fill="#555")

text(CX, y+30, "LEVELS  (z from bench, mm)", 12, weight="bold")
lv = [("Base rails", "0–20", "drawer runs on inside faces; drawer body 3–65"),
      ("PSU rails", "68–88", "4 foot cups, floor 4 above rail = z 91; feet 11.5, body 102.5–239.5, frame 99.5–242.5"),
      ("AWG rails", "227.5–247.5", "4 corner pads 3.5 behind the front frame, top z=251.5; frame 248–336"),
      ("Scope rails", "311–331", "SLED: 2 × 250 T-slot sliders 15 tall + front bar; cups/pads top z=341; scope top 507; pulls 140"),
      ("Top rails", "490–510", "brace only; tray hangs off rear uprights below"),
      ("Inner sub-frame", "68–245", "x 251–271, y 3–350; front inner upright and front tie at y 3–23; column 273–338")]
y += 48
for a,b,c in lv:
    text(CX, y, a, 9, weight="bold"); text(CX+90, y, b, 9); text(CX+150, y, c, 8, fill="#444"); y += 14

text(CX, y+16, "PRINTED PARTS (all under 256 mm)", 12, weight="bold")
pp = ["8 × cradle corners (PSU/AWG: 4 left outer + 4 right inner); scope sled: 2 × slider 327 + front bar + 2 rear bars (page 2)",
      "2 × rear box halves 160.5 × 135 × 110 joined (dovetail), 20 mm front lip, rides the sled — access: page 2",
      "2 × drawer halves (front/back) 315 × 60 × 300, joined; facia 315 × 83 × 3; 2 × runners; housing top 315 × 300 × 3 (2 tiles)",
      "1 × column drawer 65 × 240 × 300 + facia; 1 × mini slot 26 × 83 × 180; shared housing top 96 × 300 × 3 at 333–336",
      "Side tiles 3 mm ASA, 4 mm solid border, clip into rail slots, one per band between rails: 20–68, 88–227.5, 247.5–311, 347–490 (band 331–346 open: sled sliders). Left 4 × 310 long; right 3 × 310 + top band split at y 250: 230 fold-down door (bottom hinge, knuckles outboard, magnet catch) + 80 fixed. Top 2 × 160.5 × 310 solid.",
      "4 × TPU feet; 2 × TPU sled-stop caps; 4 × ASA caps; 2 × door hinge knuckles + 2 × magnet clips (4 × Ø10×2 magnets); 1 × probe hanger"]
y += 34
for p in pp: text(CX, y, "• "+p, 8, fill="#444"); y += 13

text(CX, y+16, "RULES BAKED IN", 12, weight="bold")
rl = ["Width 361: 315 scope + 3 mm each side + 2 × 20 uprights. PSU/AWG hard left; screens align left",
      "Height 520 incl. feet and caps (limit 530): 5 mm reveals throughout; scope flat = 166, 3 mm under the top panel",
      "PSU vents 35–155 both sides: inner posts sit at y 0–20 and 330–350, clear of the vent; channel open end to end",
      "Interior 3 mm behind the frame front; facias 0–3 flush; all reveals 5 mm (3 mm to the uprights, set by the scope); rear open",
      "AWG frame 3.5 proud each side, 3 top/bottom; PSU frame 2.75 each side, 3 top/bottom, 3.5 deep — cradle pads and cups sit behind both frames",
      "Scope cradle equalises front/rear foot heights so it sits level"]
y += 34
for r in rl: text(CX, y, "• "+r, 8, fill="#444"); y += 13

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1130 1215" width="1130" height="1215" font-family="Helvetica, Arial, sans-serif">\n<rect width="1130" height="1215" fill="#ffffff"/>\n' + "\n".join(out) + '\n<text x="20" y="1200" font-size="8" fill="#888">bench-stack-layout v15 (tiles between rails; fold-down door) — page 1 of 2 — 2026-09-14 — for approval before extrusion order</text>\n</svg>\n'
open("/mnt/user-data/outputs/bench-stack-layout-v15.svg","w").write(svg)
print("ok", len(svg))
