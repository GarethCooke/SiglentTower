# layout_gen.py — the dimensioned layout sheet, 1 unit = 1 mm. v16 (2026-11-05): AS BUILT, from HANDOVER v19 §2–§3 and
# fit.py. v15 (2026-09-14) was the design sheet for approval before the extrusion order; it stays in git history.
# Writes bench-stack-layout-v16.svg in the repo root; the PDF beside it is `rsvg-convert -f pdf` of the SVG.
# Frame coordinates: x from the left upright's outer face, y from the front plane, z from the rail bottoms (feet below 0).
import os, math, textwrap
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W_OUT   = 361      # overall width in the model (362 by tape; only the top panel is made to 362)
W_IN    = 321      # clear width between uprights / side rails
D_OUT   = 350      # overall depth
H_OUT   = 510      # upright length
EXT     = 20       # 2020

# vertical layout (z from the rail bottoms) — HANDOVER v19 §3
BASE_RAIL   = (0, 20)
DRAWER      = (3, 63)          # bottom drawer body (four quarters), facia 3–86
PSU_RAIL    = (68, 88)
PSU         = (99, 242)        # front face 143 tall; feet in the cradle cups at 92, 150 on its feet (fit.py PSU_H_FEET)
PSU_BODY    = (102, 242)       # body 140
AWG_RAIL    = (227.5, 247.5)
AWG         = (248, 336)       # bezel 88 tall; body 82 on TPU pads at 251.5
SCOPE_RAIL  = (311, 331)
SCOPE       = (341, 507)       # cup floors 341, chassis 355, top 507 — 3 under the panel
SCOPE_BODY  = (355, 507)
TOP_RAIL    = (490, 510)
PANEL       = (510, 513)       # top panel (D12), caps 513–519
BOX         = (346, 456)       # rear box on the sled's cross bars
SLED        = (337, 346)       # beams; front bar 337–355 at y 0–12

# depth (y from the front plane)
SCOPE_D = 135; AWG_D = 260; PSU_D = 284.5; PSU_KNOB = 17
BOX_Y   = (195, 330)
DRAWER_D = 300; COL_D = 285

# widths (x from the left upright's outer face)
SCOPE_X = (23, 338)
AWG_X   = (23, 237)
AWG_BODY_X = (26.5, 233.5)
PSU_X   = (22.25, 242.25)      # body 220
PSU_BEZ = (20, 244.5)          # front face, hard against the left PSU rail (fit.py PSU_FACE_X)
COL_X   = (274, 338)           # column drawer body (facia 273–338)
COL_Z   = (91, 331)            # body; facia 91–336
MINI_X  = (242, 268)
MINI_Z  = (252.8, 331)         # body; facia 248–336
INNER_X = (253.7, 273.7)       # sub-frame uprights and inner rails, as measured (model 251–271)
INNER_Z = (68, 247.5)
TIE_X   = (273.7, 341)
PSU_VENT = (35, 155)
DRAWER_X = (23, 338)
TILE_L, TILE_R = (-3, 0), (361, 364)    # side tiles on the rails' outer faces

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
    line(x1, y-4, x1, y+4, "#0a4", 0.6); line(x2, y-4, x2, y+4, "#0a4", 0.6)
    line(x1, y, x2, y, "#0a4", 0.6)
    text((x1+x2)/2, y-2+off, label, size, "middle", fill="#0a4")

def vdim(y1, y2, x, label, size=8, side=1):
    line(x-4, y1, x+4, y1, "#0a4", 0.6); line(x-4, y2, x+4, y2, "#0a4", 0.6)
    line(x, y1, x, y2, "#0a4", 0.6)
    text(x + 3*side, (y1+y2)/2 + 3, label, size, "start" if side>0 else "end", fill="#0a4")

EXT_FILL = "#9aa4b1"; INST_FILL = "#eef1f5"; ZONE = "#d9534f"; PRINT = "#c60"

# ---------------- FRONT ELEVATION ----------------
FX, FY = 90, 70            # sheet origin; z=0 at FY + H_OUT
def fz(z): return FY + H_OUT - z
def fr(x0,x1,z0,z1,**kw): rect(FX+x0, fz(z1), x1-x0, z1-z0, **kw)

text(FX, FY-44, "FRONT ELEVATION — as built", 12, weight="bold")
text(FX, FY-31, "1 unit = 1 mm. Frame 361 in the model, 362 by tape. Instruments as measured on the bench; printed parts in orange.", 8, fill="#555")

for z0,z1 in (BASE_RAIL, TOP_RAIL): fr(EXT, W_OUT-EXT, z0, z1, fill="#c5ccd6", stroke="#777")      # rear cross rails (behind)
fr(0, EXT, 0, H_OUT, fill=EXT_FILL); fr(W_OUT-EXT, W_OUT, 0, H_OUT, fill=EXT_FILL)                  # uprights
for z0,z1 in (PSU_RAIL, AWG_RAIL, SCOPE_RAIL):                                                     # side rails end-on
    for x0 in (0, W_OUT-EXT):
        fr(x0, x0+EXT, z0, z1, fill="#7d8896", stroke="#333")
# bottom drawer (facia 3–86, body behind it) and the sill panel over it
fr(*DRAWER_X, DRAWER[0], 86, fill=INST_FILL); text(FX+W_OUT/2, fz(DRAWER[0]+42), "BOTTOM DRAWER  315 × 60 × 300 — four quarters; facia 3–86; no lid (D14), no stop (D15)", 8, "middle")
fr(EXT, 253.4, 87, 99, fill="#dfe3e8", stroke="#555"); text(FX+140, fz(90), "sill panel 20–253.4, z 87–99 — button at x 45, two pixels behind the window", 6, "middle", fill="#333")
# PSU
fr(*PSU_BEZ, *PSU, fill=INST_FILL)
for x in (61.75, 215.25): fr(x-9.5, x+9.5, 92, PSU_BODY[0], fill="#555", stroke="#333")              # feet in the cradle cups (x 61.75; right 213.25 / 217.25)
fr(*PSU_X, PSU_BODY[0], PSU_BODY[1], fill="none", stroke="#999", dash="2,2")
text(FX+132, fz(172), "SPD3303X-E", 11, "middle", "bold"); text(FX+132, fz(157), "face 225 × 143 at x 20–244.5, hard against the left rail", 7, "middle"); text(FX+132, fz(146), "body 220 × 140 × 284.5; feet in the cups at z 92, 150 tall on them", 7, "middle")
# AWG
fr(*AWG_X, *AWG, fill=INST_FILL)
fr(*AWG_BODY_X, 251.5, 333.5, fill="none", stroke="#999", dash="2,2")
text(FX+130, fz(296), "SDG2082X (bumpers and handle off)", 11, "middle", "bold"); text(FX+130, fz(281), "face 214 × 88; body 207 × 82 × 260 on TPU pads at 251.5; 3 mm over the PSU", 7, "middle")
# scope on the sled
fr(*SCOPE_X, *SCOPE, fill=INST_FILL)
fr(SCOPE_X[0], SCOPE_X[1], SCOPE[0], SCOPE_BODY[0], fill="#dfe3e8", stroke="#888", dash="3,2")
fr(23, 338, 337, 355, fill="#fff3d6", stroke=PRINT)                                                 # sled front bar
text(FX+W_OUT/2, fz(445), "SDS1104X-E", 11, "middle", "bold"); text(FX+W_OUT/2, fz(430), "315 × 166 (152 body + 14 feet) × 135 — on the sled: cups 341, chassis 355, top 507, pulls out 92", 7, "middle")
text(FX+W_OUT/2, fz(348), "sled front bar 337–355 (pull liner)", 6, "middle", fill=PRINT)
# inner sub-frame, as measured: left face x 253.7, front upright flush with the front plane
fr(*INNER_X, *INNER_Z, fill=EXT_FILL)
for z0,z1 in (PSU_RAIL, AWG_RAIL): fr(*INNER_X, z0, z1, fill="#7d8896", stroke="#333")
fr(*TIE_X, *PSU_RAIL, fill="#c5ccd6", stroke="#777")
text(FX+307, fz(PSU_RAIL[0])-3, "tie 70 (front, PSU level)", 6, "middle", fill="#555")
text(FX+263.7, fz(112), "inner upright 179.5 — at x 253.7, flush (measured)", 6, "middle", fill="#fff", rot=-90)
# column drawer and mini slot (facias 273–338 / 242–268)
fr(COL_X[0]-1, COL_X[1], COL_Z[0], 336, fill="#fff3d6", stroke=PRINT, sw=1)
text(FX+(COL_X[0]+COL_X[1])/2-8, fz(212), "COLUMN DRAWER", 9, "middle", "bold", fill=PRINT, rot=-90)
text(FX+(COL_X[0]+COL_X[1])/2+8, fz(212), "64 × 240 × 285 on four guide strips (facia 65 × 245)", 7, "middle", fill=PRINT, rot=-90)
fr(*MINI_X, 248, 336, fill="#fff3d6", stroke=PRINT, sw=1)
text(FX+256, fz(292), "MINI SLOT 26 × 83 × 285, vent neck (D7)", 6, "middle", "bold", fill=PRINT, rot=-90)
# side tiles on the rails' outer faces, top panel over the whole frame top, caps on its corners
for x0,x1 in (TILE_L, TILE_R): fr(x0, x1, 10, 500, fill="#7d8896", stroke="#333", dash="2,2")
fr(0, 362, *PANEL, fill="#7d8896", stroke="#333")
for x0 in (0, W_OUT-EXT): fr(x0, x0+EXT, 513, 519, fill="#1e3a8a", stroke="#333")
text(FX+W_OUT/2, fz(524), "top panel 362 × 350 × 3 over the whole frame top, z 510–513 — four standing tiles on glued half-laps (D12); caps 513–519, M5 into the uprights' bores", 6, "middle", fill="#333")
text(FX-6, fz(300), "hex side tiles ON the rails' outer faces, 3 mm PETG, clipped into the slots (P4)", 6, "middle", fill="#333", rot=-90)
# PSU side-vent air channel between the PSU face and the sub-frame
fr(PSU_BEZ[1], INNER_X[0], PSU[0], PSU[1], fill="none", stroke=ZONE, dash="4,3")
text(FX+(PSU_BEZ[1]+INNER_X[0])/2, fz(160), "air 9.2", 5, "middle", fill=ZONE, rot=-90)
# TPU feet + bench line
for x0 in (-2, W_OUT-EXT-2): fr(x0, x0+EXT+4, -6, 0, fill="#c9d3d0", stroke="#333")
text(FX+W_OUT/2, fz(-6)+10, "TPU feet 24 × 24 × 6, Ø4.6 spigot glued into the uprights' bores (P8) ×4", 7, "middle", fill="#333")
line(FX-30, fz(-6), FX+W_OUT+30, fz(-6), "#000", 1.2); text(FX-30, fz(-6)+10, "bench", 7, fill="#555")

# dimensions — horizontal
hdim(FX, FX+W_OUT, fz(-6)+22, "361 overall (362 by tape)")
hdim(FX+EXT, FX+W_OUT-EXT, fz(-6)+38, "321 clear between uprights / rails")
hdim(FX+SCOPE_X[0], FX+SCOPE_X[1], FY-6, "315 scope (3 mm each side)")
AR = fz(245)   # the 6 mm gap between the PSU top and the AWG
hdim(FX+AWG_X[0], FX+AWG_X[1], AR, "214 AWG face")
hdim(FX+AWG_X[1], FX+MINI_X[0], AR, "5"); hdim(FX+MINI_X[0], FX+MINI_X[1], AR, "26"); hdim(FX+MINI_X[1], FX+COL_X[0], AR, "6")
hdim(FX+COL_X[0], FX+COL_X[1], AR, "64 column")
hdim(FX+PSU_BEZ[0], FX+PSU_BEZ[1], fz(-6)+54, "225 PSU face, x 20–244.5 (9.2 of air to the sub-frame)")
# dimensions — vertical (right side)
DX = FX + W_OUT + 18
vdim(fz(-6), fz(519), DX+50, "525 overall")
vdim(fz(DRAWER[0]), fz(DRAWER[1]), DX, "60 drawer body")
vdim(fz(92), fz(PSU[1]), DX, "150 PSU on its feet")
vdim(fz(AWG[0]), fz(AWG[1]), DX, "88 AWG")
vdim(fz(SCOPE[0]), fz(SCOPE[1]), DX, "166 scope")
vdim(fz(PSU[1]), fz(AWG[0]), DX+22, "6")
vdim(fz(AWG[1]), fz(SCOPE[0]), DX+22, "5")
# rail heights (left side): model heights; the measured gaps are in the note
LX = FX - 14
for (z0,z1),lab in ((BASE_RAIL,"base rail 0–20"),(PSU_RAIL,"PSU rail 68–88"),(AWG_RAIL,"AWG rail 227.5–247.5"),(SCOPE_RAIL,"scope rail 311–331"),(TOP_RAIL,"top rail 490–510")):
    line(LX, fz(z1), FX, fz(z1), "#0a4", 0.5, "2,2"); text(LX-2, fz(z1)-2, lab, 7, "end", fill="#0a4")
for z,lab,dy in ((92,"92 (cup floor)",9),(251.5,"251.5 (pads)",9),(SCOPE[0],"341 (cups)",-3)):
    line(LX, fz(z), FX, fz(z), PRINT, 0.5, "1,2"); text(LX-2, fz(z)+dy, f"z={lab}", 7, "end", fill=PRINT)
text(FX, fz(-6)+70, "Rail gaps as built, face to face — right 45.4 / 139.5 / 65.8 / 158, left 51.2 / 135 / 65.5 / 157", 6.5, fill="#555")
text(FX, fz(-6)+79, "(spacers 48 / 139.5 / 63.5 / 159). The model keeps the spacer heights; the side tiles were cut to the measured bands, per side.", 6.5, fill="#555")

# ---------------- SIDE ELEVATION (from the right, front at left) ----------------
SX, SY = 600, 70
def sz(z): return SY + H_OUT - z
def sr(y0,y1,z0,z1,**kw): rect(SX+y0, sz(z1), y1-y0, z1-z0, **kw)
text(SX, SY-30, "SIDE ELEVATION — right side, front at left", 12, weight="bold")
text(SX, SY-17, "Everything inside the frame sits 3 mm behind the front plane; the facias fill the 3 mm, flush with the uprights.", 8, fill="#555")
for z0,z1 in (BASE_RAIL, PSU_RAIL, AWG_RAIL, SCOPE_RAIL, TOP_RAIL): sr(EXT, D_OUT-EXT, z0, z1, fill=EXT_FILL)
sr(0, EXT, 0, H_OUT, fill=EXT_FILL); sr(D_OUT-EXT, D_OUT, 0, H_OUT, fill=EXT_FILL)
# bottom drawer
sr(3, DRAWER_D+3, *DRAWER, fill=INST_FILL); sr(0, 3, 3, 86, fill="#2f6f73", stroke="#111"); text(SX+DRAWER_D/2, sz(30), "bottom drawer 300 deep on two printed runners; facia 0–3 flush", 8, "middle")
# PSU
sr(3, PSU_D+3, *PSU, fill=INST_FILL); sr(3-PSU_KNOB, 3, PSU[0]+40, PSU[1]-40, fill="#dfe3e8", stroke="#888")
text(SX+PSU_D/2, sz(170), "PSU 284.5 body, knobs +17; fan exhaust rear", 9, "middle")
# AWG
sr(3, AWG_D+3, *AWG, fill=INST_FILL); text(SX+AWG_D/2, sz(288), "AWG body 260; face at 3; side vent Ø80 at y 86–166", 9, "middle")
# sled: beams 337–346 (y 12–330), front bar 337–355 (y 0–12), rests on the rail tops at the front, box behind the scope
sr(12, 330, *SLED, fill="#fff3d6", stroke=PRINT); sr(0, 12, 337, 355, fill="#fff3d6", stroke=PRINT)
sr(21, 61, 331, 334, fill="#fff3d6", stroke=PRINT)
text(SX+110, sz(339), "sled beams 337–346 on T-feet in the rails' inner slots; travel 92", 6, "middle", fill=PRINT)
# scope
sr(3, SCOPE_D+3, *SCOPE, fill=INST_FILL); sr(3, SCOPE_D+3, SCOPE[0], SCOPE_BODY[0], fill="#dfe3e8", stroke="#888", dash="3,2")
text(SX+SCOPE_D/2, sz(440), "scope", 9, "middle"); text(SX+SCOPE_D/2, sz(425), "135 deep", 8, "middle")
# rear box on the sled
sr(*BOX_Y, *BOX, fill="#fff3d6", stroke=PRINT)
text(SX+(BOX_Y[0]+BOX_Y[1])/2, sz(420), "REAR BOX", 9, "middle", "bold", fill=PRINT)
text(SX+(BOX_Y[0]+BOX_Y[1])/2, sz(405), "291 × 135 × 110, two halves", 7, "middle", fill=PRINT)
text(SX+(BOX_Y[0]+BOX_Y[1])/2, sz(392), "rides the sled; out to the right through the door", 6, "middle", fill=PRINT)
text(SX+(BOX_Y[0]+BOX_Y[1])/2, sz(380), "BM867s on edge + BM22s + leads", 7, "middle", fill=PRINT)
# clearance zones
sr(SCOPE_D+3, BOX_Y[0], SCOPE[0], SCOPE[1], fill="none", stroke=ZONE, dash="4,3"); text(SX+166, sz(420), "57 vent / plug / cable loop", 7, "middle", fill=ZONE, rot=-90)
sr(AWG_D+3, D_OUT+40, AWG[0], AWG[1], fill="none", stroke=ZONE, dash="4,3"); text(SX+D_OUT+30, sz(292), "plugs ≥50", 7, "middle", fill=ZONE, rot=-90)
sr(PSU_D, D_OUT+40, PSU[0], PSU[1], fill="none", stroke=ZONE, dash="4,3"); text(SX+D_OUT+30, sz(167), "fan exhaust ≥50 — kept open", 7, "middle", fill=ZONE, rot=-90)
# the skin: tiles cover the rails (centreline to centreline), 155 long; band 4 right = door + fixed rear tile
sr(10, D_OUT-10, 10, 321, fill="none", stroke="#333", dash="4,3", sw=1)
sr(20, 250, 338, 499, fill="none", stroke="#333", dash="4,3", sw=1); sr(250, 330, 334, 500, fill="none", stroke="#333", dash="4,3", sw=1)
r=4.2; dx=r*2+2.5; dy=(r*2+2.5)*0.866
row=0; yy=20
while yy<492:
    xx=EXT+8+(dx/2 if row%2 else 0)
    while xx<D_OUT-EXT-8:
        if not (321 < yy < 338):   # the sled band is open
            pts=" ".join(f"{SX+xx+r*math.cos(math.pi/6+k*math.pi/3):.1f},{sz(yy)-r*math.sin(math.pi/6+k*math.pi/3):.1f}" for k in range(6))
            emit(f'<polygon points="{pts}" fill="none" stroke="#8a93a0" stroke-width="0.35"/>')
        xx+=dx
    yy+=dy; row+=1
for t in (78, 237.5): line(SX+10, sz(t), SX+D_OUT-10, sz(t), "#333", 0.8, "6,3")      # band edges on the rail centrelines
line(SX+175, sz(10), SX+175, sz(321), "#333", 0.8, "6,3")                               # the 155 / 155 tile split
rect(SX+EXT+4, sz(486), D_OUT-2*EXT-8, 12, fill="#fff", stroke="#333", sw=0.4)
text(SX+D_OUT/2, sz(477), "HEX SIDE TILES on the rails' outer faces — 14 tiles, 155 long, 3 mm PETG, P4 clips", 6, "middle", "bold", fill="#333")
text(SX+135, sz(466), "DOOR 230 × 161, z 338–499 — hinge axis x 369 / z 341 (D11), magnets at the top; fixed tile 80 behind it", 6, "middle", "bold", fill="#333")
sr(0, D_OUT, *PANEL, fill="#7d8896", stroke="#333")
sr(-2, EXT+2, -6, 0, fill="#c9d3d0", stroke="#333"); sr(D_OUT-EXT-2, D_OUT+2, -6, 0, fill="#c9d3d0", stroke="#333")
line(SX-40, sz(-6), SX+D_OUT+60, sz(-6), "#000", 1.2)
# dims
hdim(SX, SX+D_OUT, sz(-6)+22, "350 overall depth")
hdim(SX+EXT, SX+D_OUT-EXT, sz(-6)+38, "310 side rails")
hdim(SX, SX+3, SY-6, "3"); hdim(SX+3, SX+SCOPE_D+3, SY-6, "135")
hdim(SX+SCOPE_D+3, SX+BOX_Y[0], SY-6, "57")
hdim(SX+BOX_Y[0], SX+BOX_Y[1], SY-6, "135 box")
hdim(SX+3, SX+AWG_D+3, sz(AWG[1])-6, "260")
hdim(SX+AWG_D+3, SX+D_OUT, sz(AWG[1])-6, "87")
vdim(sz(BOX[0]), sz(BOX[1]), SX+D_OUT+12, "110")

# ---------------- PLAN ----------------
PX, PY = 90, 725    # front at the top of the view
def pr(x0,x1,y0,y1,**kw): rect(PX+x0, PY+y0, x1-x0, y1-y0, **kw)
text(PX, PY-30, "PLAN — front at top", 12, weight="bold")
text(PX, PY-17, "Scope centred; AWG and PSU hard left; column right; interior recessed 3 mm, facias flush. Power strip and lighting board behind the frame.", 8, fill="#555")
for x0 in (0, W_OUT-EXT): pr(x0, x0+EXT, EXT, D_OUT-EXT, fill=EXT_FILL)
pr(EXT, W_OUT-EXT, D_OUT-EXT, D_OUT, fill="#c5ccd6", stroke="#777")   # rear cross rails
for x0,y0 in ((0,0),(W_OUT-EXT,0),(0,D_OUT-EXT),(W_OUT-EXT,D_OUT-EXT)): pr(x0,x0+EXT,y0,y0+EXT, fill="#6b7583")
# footprints
pr(*AWG_BODY_X, 3, AWG_D+3, fill="none", stroke="#666", dash="5,3"); text(PX+130, PY+AWG_D-8, "AWG body 207 × 260", 8, "middle", fill="#666")
pr(*PSU_BEZ, 3, PSU_D+3, fill="none", stroke="#666", dash="2,2"); text(PX+132, PY+PSU_D-8, "PSU face 225 × 284.5 at x 20–244.5", 8, "middle", fill="#666")
pr(*SCOPE_X, 3, SCOPE_D+3, fill=INST_FILL); text(PX+W_OUT/2, PY+SCOPE_D/2+4, "SCOPE 315 × 135 on the sled", 10, "middle", "bold")
pr(20.5, 60, 12, 330, fill="none", stroke=PRINT, dash="2,2"); pr(301, 340.5, 12, 330, fill="none", stroke=PRINT, dash="2,2"); pr(23, 338, 0, 12, fill="#fff3d6", stroke=PRINT)
text(PX+40, PY+320, "sled beams", 6, "middle", fill=PRINT); pr(20.5, 47, 201, 334, fill="none", stroke=PRINT, dash="1,2"); text(PX+34, PY+270, "cable channel", 5, "middle", fill=PRINT, rot=-90)
# rear box halves on the sled, split at x 195.5
pr(50, 195.5, *BOX_Y, fill="#fff3d6", stroke=PRINT); pr(195.5, 341, *BOX_Y, fill="#fff3d6", stroke=PRINT)
text(PX+195.5, PY+BOX_Y[0]+40, "REAR BOX 291 × 135 — two halves, dovetailed at x 195.5", 8, "middle", "bold", fill=PRINT)
text(PX+195.5, PY+BOX_Y[0]+62, "BM867s in its holster on edge, BM22s, leads", 7, "middle", fill=PRINT)
text(PX+195.5, PY+BOX_Y[0]+110, "sits between the cross bars' lips; lifts 7.5 over the right splice on its way out", 6, "middle", fill=PRINT)
# inner sub-frame as measured: uprights flush at y 0–20 and 330–350, rails between
pr(*INNER_X, EXT, D_OUT-EXT, fill=EXT_FILL, extra='fill-opacity="0.45"')
pr(*INNER_X, 0, EXT, fill="#6b7583"); pr(*INNER_X, D_OUT-EXT, D_OUT, fill="#6b7583")
pr(*TIE_X, 3, EXT+3, fill="#c5ccd6", stroke="#777"); pr(*TIE_X, D_OUT-EXT, D_OUT, fill="#c5ccd6", stroke="#777")
text(PX+263.7, PY+260, "inner rails 307 (PSU + AWG level) at x 253.7–273.7", 6, "middle", fill="#333", rot=-90)
# side tiles on the outer faces, mini slot with its vent neck, column
for x0,x1 in (TILE_L, TILE_R): pr(x0, x1, EXT, D_OUT-EXT, fill="#7d8896", stroke="#333")
pr(*MINI_X, 0, 81, fill="none", stroke=PRINT, dash="3,2"); pr(252, 268, 81, 171, fill="none", stroke=PRINT, dash="3,2"); pr(*MINI_X, 171, 288, fill="none", stroke=PRINT, dash="3,2")
text(PX+256, PY+45, "mini 26 × 285", 6, "middle", fill=PRINT, rot=-90); text(PX+260, PY+126, "neck 16", 5, "middle", fill=PRINT, rot=-90)
pr(*COL_X, 0, 288, fill="none", stroke=PRINT, dash="6,3", sw=1.2); text(PX+(COL_X[0]+COL_X[1])/2, PY+100, "COLUMN 64 × 285", 7, "middle", "bold", fill=PRINT, rot=-90)
# vents
for x in (AWG_BODY_X[0], AWG_BODY_X[1]):
    line(PX+x, PY+86, PX+x, PY+166, PRINT, 2)
text(PX+AWG_X[0]-4, PY+126, "AWG side vent Ø80, y 86–166", 6, "end", fill=PRINT, rot=-90)
text(PX+AWG_X[1]+5, PY+210, "fan vent → 15 mm channel", 6, "start", fill=PRINT, rot=-90)
for x in (PSU_BEZ[0]+2, PSU_BEZ[1]-2):
    line(PX+x, PY+PSU_VENT[0], PX+x, PY+PSU_VENT[1], "#36c", 2)
text(PX+PSU_BEZ[1]+12, PY+60, "PSU vent 35–155 both sides", 6, "start", fill="#36c", rot=-90)
# behind the frame: the power strip on the rear-left upright, the lighting board on the rear base rail
pr(1, 79, 354, 384, fill="#ececec", stroke="#333"); text(PX+40, PY+372, "Addtam strip, vertical z 75–425", 6, "middle", fill="#333")
pr(90, 150, 350, 390.5, fill="#fff3d6", stroke=PRINT); text(PX+120, PY+372, "lighting board", 6, "middle", fill=PRINT)
# dims
hdim(PX, PX+W_OUT, PY+D_OUT+54, "361 (362 by tape)")
vdim(PY, PY+D_OUT, PX+W_OUT+14, "350")
vdim(PY, PY+SCOPE_D, PX+W_OUT+34, "135")
vdim(PY+BOX_Y[0], PY+BOX_Y[1], PX+W_OUT+34, "135")
hdim(PX+COL_X[0], PX+COL_X[1], PY-6, "64")
hdim(PX+PSU_BEZ[1], PX+INNER_X[0], PY-6, "9.2")

# ---------------- CUT LIST / LEVELS / PARTS ----------------
CX, CY = 600, 715
text(CX, CY, "2020 EXTRUSION — AS CUT (CUT-TABLE.md)", 12, weight="bold")
rows = [("Uprights", "4", "510"), ("Side rails, 5 levels", "10", "310"), ("Rear cross rails (base + top)", "2", "321"),
        ("Inner rails (PSU + AWG level; 2 used, 2 spare)", "4", "307"), ("Inner uprights", "2", "179.5"), ("Ties, inner → right rails", "3", "70"),
        ("From", "", "8 × 1 m + the CNCMANS 300 mm 4-pack (D1)")]
y = CY+18
for a,b,c in rows:
    text(CX, y, a, 9, weight="bold" if a=="From" else "normal"); text(CX+230, y, b, 9, "middle"); text(CX+250, y, c, 9); y += 14
for i,t in enumerate(textwrap.wrap("Joints: 40 hidden L-connectors on the inward faces + 8 cast brackets (4 under the scope rails, 1 at the front tie); drop-in T-nuts; M5 × 8 for the brackets, M5 × 10 for the printed parts.", 118)): text(CX, y+4+10*i, t, 7, fill="#555")
y += 10

text(CX, y+30, "LEVELS AS BUILT  (z from the rail bottoms, mm)", 12, weight="bold")
lv = [("Base rails", "0–20", "feet −6–0; bottom drawer body 3–63 on runners in the base rails' top slots"),
      ("PSU rails", "68–88", "cradle cups floor at 92; PSU on its feet 92–242; sill panel 87–99 under the PSU"),
      ("AWG rails", "227.5–247.5", "5 mm cradle arms + 4 mm TPU pads → AWG body 251.5–333.5, face 248–336"),
      ("Scope rails", "311–331", "T-feet in the inner slots; beams 337–346, front bar to 355; cups 341, chassis 355, top 507; box 346–456"),
      ("Top rails", "490–510", "top panel 510–513 over the whole frame; caps 513–519"),
      ("Inner sub-frame", "68–247.5", "x 253.7–273.7 (measured), front upright flush; column 274–338, mini slot 242–268")]
y += 48
for a,b,c in lv:
    text(CX, y, a, 9, weight="bold"); text(CX+90, y, b, 9)
    for i,t in enumerate(textwrap.wrap(c, 92)): text(CX+150, y+9*i, t, 7, fill="#444")
    y += 14 if len(c) <= 92 else 22

text(CX, y+16, "PRINTED PARTS AS FITTED — 76 designs, 103 pieces (HANDOVER v19 §10)", 12, weight="bold")
pp = ["Cradles 8: PSU left v3 ×2, right rear v4, right front v5; AWG left v2 ×2, right v2 ×2 — black ABS, seated with the jigs",
      "Drawers: bottom quarters Q1–Q4 + facia with the logo inlay + pull insert v2 + two 300 runners (ABS+); column drawer + facia + insert + four guide strips; mini slot body + runner v3 + facia + insert",
      "Sled: two 210 T-feet, four beam halves (split, D6), front bar v3, cross bars v2, front rests v2, splices v2, cable channel, pull liner, two TPU stop caps",
      "Box: two halves (dovetailed) + two corner braces. Skin: 14 side tiles (bands at the measured heights), door v3 + two hinge pairs + pins, fixed rear tile, front bracket, rear tab",
      "Top: four standing tiles + four caps. Trim: 4 TPU feet, 4 AWG pads, 6 slot covers, 2 strip brackets, sill panel + window + 2 blocks, board enclosure + lid"]
y += 34
for p in pp:
    for i,t in enumerate(textwrap.wrap(p, 122)): text(CX+(8 if i else 0), y, ("" if i else "• ")+t, 7, fill="#444"); y += 10
    y += 2

text(CX, y+16, "AS BUILT — WHERE THE BENCH OVERRULED THE MODEL", 12, weight="bold")
rl = ["Sub-frame upright at x 253.7, flush with the front (model 251, 3 back) — only the sill panel bridges to it, so only the sill panel changed",
      "Rail gaps up to 6 mm off the spacers → every side tile cut to its own band per side (left 71.2 / 155 / 85.5, right 65.4 / 159.5 / 85.8)",
      "PSU feet 155.5 apart and 150 tall on them → right cradles v4 / v5, AWG arms 8 → 5 mm; the PSU sits very slightly skewed (accepted)",
      "Sled front droops past the foot → front rests on the rail tops and splice bars over the P7 joint; the box lifts 7.5 over the right splice",
      "Door edge 347 → 338 (7 over the scope rail); no drawer lids (D14) and no drawer stops (D15); strips 15 LEDs each, not 28; sled travel 92 to the TPU caps",
      "Not built, by choice: the probe hanger and the rear-right cable clips"]
y += 34
for r_ in rl:
    for i,t in enumerate(textwrap.wrap(r_, 122)): text(CX+(8 if i else 0), y, ("" if i else "• ")+t, 7, fill="#444"); y += 10
    y += 2

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1130 1300" width="1130" height="1300" font-family="Helvetica, Arial, sans-serif">\n<rect width="1130" height="1300" fill="#ffffff"/>\n' + "\n".join(out) + '\n<text x="20" y="1288" font-size="8" fill="#888">bench-stack-layout v16 — AS BUILT — 2026-11-05 — from HANDOVER v19 (v15 of 2026-09-14 was the design sheet; the sled sheet is sled-mechanism-v2.pdf, superseded by parts/sled-*.png)</text>\n</svg>\n'
path = os.path.join(ROOT, "bench-stack-layout-v16.svg")
open(path, "w", encoding="utf-8").write(svg)
print("ok", path, len(svg))
