# Bottom drawer as four quarters (ROADMAP D2 option a) — dimensioned SVG sheet, 1 unit = 1 mm at 1:1 in the plan
# Emits drawer-quarters-v1.svg and .pdf (cairosvg). Same helper style as layout_gen.py.
import math, sys, os
try:
    import cairosvg
except ImportError:
    cairosvg = None

# ---------- drawer parameters (mm) ----------
DW, DD, DH = 315, 300, 60      # body outside
WALL, FLOOR = 2.4, 3.0
SEAM_X, SEAM_Y = 157.5, 150    # seams (from the drawer's own left/front)
TAB_NECK, TAB_HEAD, TAB_LEN, TAB_PITCH = 12, 18, 8, 30   # floor puzzle-dovetail tabs
TAB_CLR = 0.15                                          # -> fit.py DOVETAIL_CLR
RIB_NECK, RIB_HEAD, RIB_DEPTH = 4, 6, 3                 # wall vertical sliding dovetail
BOSS_W, BOSS_T = 12, 3                                  # female boss grown inboard of the wall
CENTRE_KEEP = 15                                        # tabs stop this far from the cross

out = []
def emit(s): out.append(s)
def rect(x, y, w, h, fill="none", stroke="#222", sw=0.8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def poly(pts, fill="none", stroke="#222", sw=0.8):
    emit('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def text(x, y, s, size=9, anchor="start", weight="normal", fill="#222", rot=None):
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    emit(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{r}>{s}</text>')
def line(x1, y1, x2, y2, stroke="#222", sw=0.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def hdim(x1, x2, y, label, off=0, size=8):
    line(x1, y-4, x1, y+4, "#0a4", 0.6); line(x2, y-4, x2, y+4, "#0a4", 0.6); line(x1, y, x2, y, "#0a4", 0.6)
    text((x1+x2)/2, y-2+off, label, size, "middle", fill="#0a4")
def vdim(y1, y2, x, label, size=8, side=1):
    line(x-4, y1, x+4, y1, "#0a4", 0.6); line(x-4, y2, x+4, y2, "#0a4", 0.6); line(x, y1, x, y2, "#0a4", 0.6)
    text(x + 3*side, (y1+y2)/2 + 3, label, size, "start" if side > 0 else "end", fill="#0a4")

Q = ["#dfe7f1", "#e8f1df", "#f1e8df", "#efe0ef"]   # quarter fills Q1..Q4
SEAM = "#c0392b"

# ================= PLAN, 1:1 =================
PX, PY = 60, 80
text(PX, 40, "BOTTOM DRAWER — FOUR-QUARTER BUILD (D2 option a)  v1", 14, weight="bold")
text(PX, 56, "Plan, 1:1, facia removed. Drawer 315 x 300 x 60 stays full size; printed as four quarters, each 157.5 x 150 (flat on the 256 bed). Q1 front-left … Q4 rear-right.", 9, fill="#444")
def P(x, y): return PX + x, PY + y         # drawer coords -> sheet (front edge at the top of the plan)
quarters = [(0, 0), (SEAM_X, 0), (0, SEAM_Y), (SEAM_X, SEAM_Y)]
for i, (qx, qy) in enumerate(quarters):
    w = SEAM_X if qx == 0 else DW - SEAM_X
    d = SEAM_Y if qy == 0 else DD - SEAM_Y
    x, y = P(qx, qy); rect(x, y, w, d, Q[i], "#222", 0.8)
    text(x + w/2, y + d/2 + 4, f"Q{i+1}", 14, "middle", "bold", "#334")
# walls
x, y = P(0, 0)
rect(x + WALL, y + WALL, DW - 2*WALL, DD - 2*WALL, "none", "#222", 0.5)
# seams
line(*P(SEAM_X, 0), *P(SEAM_X, DD), SEAM, 1.2, "4 2"); line(*P(0, SEAM_Y), *P(DW, SEAM_Y), SEAM, 1.2, "4 2")
# floor tabs along both seams (alternating owner), stopping CENTRE_KEEP from the cross
def tabs_along_x_seam():   # seam at x = SEAM_X, tabs point in ±x, run along y
    for j, yc in enumerate([15 + TAB_PITCH*k for k in range(10)]):
        if yc + TAB_HEAD/2 > DD - WALL or abs(yc - SEAM_Y) < CENTRE_KEEP + TAB_HEAD/2: continue
        sgn = 1 if j % 2 == 0 else -1          # even: tab belongs to the left quarter, points right
        x0 = SEAM_X; x1 = SEAM_X + sgn*TAB_LEN
        pts = [(x0, yc - TAB_NECK/2), (x1, yc - TAB_HEAD/2), (x1, yc + TAB_HEAD/2), (x0, yc + TAB_NECK/2)]
        poly([P(*p) for p in pts], Q[0 if sgn > 0 else 1] if yc < SEAM_Y else Q[2 if sgn > 0 else 3], "#222", 0.7)
def tabs_along_y_seam():
    for j, xc in enumerate([15 + TAB_PITCH*k for k in range(11)]):
        if xc + TAB_HEAD/2 > DW - WALL or abs(xc - SEAM_X) < CENTRE_KEEP + TAB_HEAD/2: continue
        sgn = 1 if j % 2 == 0 else -1          # even: tab belongs to the front quarter, points rearward
        y0 = SEAM_Y; y1 = SEAM_Y + sgn*TAB_LEN
        pts = [(xc - TAB_NECK/2, y0), (xc - TAB_HEAD/2, y1), (xc + TAB_HEAD/2, y1), (xc + TAB_NECK/2, y0)]
        poly([P(*p) for p in pts], Q[0 if sgn > 0 else 2] if xc < SEAM_X else Q[1 if sgn > 0 else 3], "#222", 0.7)
tabs_along_x_seam(); tabs_along_y_seam()
# wall dovetail bosses (female side) at the four wall crossings
for (bx, by, bw, bh) in [(SEAM_X, WALL, BOSS_W, BOSS_T), (SEAM_X, DD - WALL - BOSS_T, BOSS_W, BOSS_T),
                         (WALL, SEAM_Y, BOSS_T, BOSS_W), (DW - WALL - BOSS_T, SEAM_Y, BOSS_T, BOSS_W)]:
    x, y = P(bx - (bw/2 if bw == BOSS_W else 0), by - (bh/2 if bh == BOSS_W else 0)); rect(x, y, bw, bh, "#555", "#222", 0.5)
# runner grooves on the outer side walls (dashed) — the y seam crosses them: the wall dovetail keeps them aligned
for gx in (0, DW):
    line(*P(gx, 10), *P(gx, DD - 10), "#888", 2.5, "6 3")
text(*P(DW + 6, 30), "runner groove", 7, fill="#888", rot=90)
# facia screws (facia ties Q1 + Q2 across the front seam)
for sx in (SEAM_X - 40, SEAM_X - 12, SEAM_X + 12, SEAM_X + 40):
    x, y = P(sx, WALL/2); emit(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#fff" stroke="#222" stroke-width="0.6"/>')
text(*P(SEAM_X, -6), "facia screws x4 (M3, into printed bosses) tie Q1–Q2 across the front seam", 7, "middle", fill="#444")
# dims
hdim(PX, PX + DW, PY + DD + 16, "315"); hdim(PX, PX + SEAM_X, PY + DD + 30, "157.5"); hdim(PX + SEAM_X, PX + DW, PY + DD + 30, "157.5")
vdim(PY, PY + DD, PX - 46, "300", side=-1); vdim(PY, PY + SEAM_Y, PX - 30, "150", side=-1); vdim(PY + SEAM_Y, PY + DD, PX - 30, "150", side=-1)
text(PX, PY + DD + 50, "FRONT is the top edge of the plan. Red dashes = seams. Coloured tabs = floor puzzle-dovetails, owner shown by colour, alternate along each seam, pitch 30, none within 15 of the cross.", 8, fill="#444")
text(PX, PY + DD + 62, "Grey blocks = female bosses of the wall dovetails (front, rear, left, right walls). Runner grooves on the outer side walls cross the rear seam; the wall dovetail keeps them aligned.", 8, fill="#444")

# ================= DETAIL A — floor tab, 4:1 =================
AX, AY, S = 480, 80, 4
text(AX, AY - 26, "DETAIL A — floor puzzle-dovetail (plan), 4:1", 11, weight="bold")
def A(x, y): return AX + x*S, AY + y*S
# two floor pieces meeting at a seam, one tab
rect(*A(0, 0), 30*S, 40*S, Q[0], "#222", 0.8); rect(*A(30, 0), 30*S, 40*S, Q[1], "#222", 0.8)
tab = [(30, 20 - TAB_NECK/2), (30 + TAB_LEN, 20 - TAB_HEAD/2), (30 + TAB_LEN, 20 + TAB_HEAD/2), (30, 20 + TAB_NECK/2)]
poly([A(*p) for p in tab], Q[0], "#222", 1.0)
line(*A(30, 0), *A(30, 40), SEAM, 1.2, "4 2")
hdim(A(30, 0)[0], A(30 + TAB_LEN, 0)[0], A(0, 0)[1] - 8, f"{TAB_LEN}")
vdim(A(0, 20 - TAB_HEAD/2)[1], A(0, 20 + TAB_HEAD/2)[1], A(30 + TAB_LEN + 6, 0)[0], f"{TAB_HEAD} head")
vdim(A(0, 20 - TAB_NECK/2)[1], A(0, 20 + TAB_NECK/2)[1], A(30 - 6, 0)[0], f"{TAB_NECK} neck", side=-1)
text(AX, AY + 40*S + 14, f"Floor {FLOOR} thick. Tab clearance {TAB_CLR} all round (fit.py DOVETAIL_CLR) — coupon sets it. Tabs drop in from above, so every", 8, fill="#444")
text(AX, AY + 40*S + 26, "joint in the drawer assembles vertically: Q2 onto Q1, Q3 onto Q1, Q4 onto Q2 + Q3 last. Layers lie in the floor plane, so tabs are full-strength in-plane.", 8, fill="#444")

# ================= DETAIL B — wall vertical dovetail, 4:1 (plan section through the wall) =================
BX, BY = 480, 320
text(BX, BY - 26, "DETAIL B — wall vertical sliding dovetail (plan section), 4:1", 11, weight="bold")
def B(x, y): return BX + x*S, BY + y*S
# wall of Q1 (left) ending at seam with male rib; wall of Q2 (right) with female boss
rect(*B(0, 0), 30*S, WALL*S, Q[0], "#222", 0.8)                     # Q1 wall
rect(*B(30, 0), 30*S, WALL*S, Q[1], "#222", 0.8)                    # Q2 wall
# boss grown inboard on Q2 (12 long x 8 thick in plan); the dovetail runs vertically, into the page
rect(*B(30, WALL), BOSS_W*S, 8*S, Q[1], "#222", 0.8)
rib = [(30, WALL + 2), (30 + RIB_DEPTH, WALL + 1), (30 + RIB_DEPTH, WALL + 7), (30, WALL + 6)]
poly([B(*p) for p in rib], Q[0], "#222", 1.0)
line(*B(30, 0), *B(30, WALL + 8), SEAM, 1.2, "4 2")
hdim(B(30, 0)[0], B(30 + RIB_DEPTH, 0)[0], B(0, 0)[1] - 8, f"{RIB_DEPTH}")
vdim(B(0, WALL + 1)[1], B(0, WALL + 7)[1], B(30 + RIB_DEPTH + 6, 0)[0], f"{RIB_HEAD} head")
vdim(B(0, WALL + 2)[1], B(0, WALL + 6)[1], B(30 - 6, 0)[0], f"{RIB_NECK} neck", side=-1)
hdim(B(30, 0)[0], B(30 + BOSS_W, 0)[0], B(0, WALL + 8)[1] + 14, f"boss {BOSS_W} long")
text(BX, BY + 12*S + 30, f"Wall {WALL}. Rib on the Q1 wall end runs the full wall height (floor top to rim); pocket in a boss grown inboard on Q2 (boss {BOSS_W} x 8 x full height).", 8, fill="#444")
text(BX, BY + 12*S + 42, "Q2 slides down onto Q1: the dovetail takes the pull-apart load across the seam and keeps the two wall faces flush, so the runner groove stays straight.", 8, fill="#444")
text(BX, BY + 12*S + 54, "Four crossings: front wall (hidden behind the facia), rear wall, left wall, right wall. CA-glue the four dovetails only after the runner test passes.", 8, fill="#444")

# ================= P7 COUPON =================
CX, CY = 480, 560
text(CX, CY - 10, "P7 COUPON (redefined for D2) — one PETG plate, gates every split part", 11, weight="bold")
lines = ["1. Centre cross: four 60 x 60 floor corners with the real tab pattern (3 mm floor, 2.4 walls on the outer edges) — tests tab fit, flushness and the 15 mm keep-out at the cross.",
         "2. Wall crossing: two 40-long wall ends, 60 tall, one with the rib, one with the boss — tests the vertical slide, pull-apart and face flushness.",
         "3. Beam section (D6): two 40-long ends of the 9 x 40 sled beam with the same dovetail scaled to the section — tests the sled split.",
         "Pass: all three assemble by hand, hold without glue, faces flush within 0.2. Iterate DOVETAIL_CLR in 0.05 steps; expect 0.15–0.25 on the X1C.",
         "Print flat, tabs up, 0.2 layers, 4 walls, no supports. About one hour of PETG."]
y = CY + 6
for l in lines: text(CX, y, l, 8, fill="#444"); y += 13

# ================= ASSEMBLY ORDER =================
text(CX, y + 12, "ASSEMBLY", 11, weight="bold"); y += 30
for l in ["Q1 on the bench → Q2 down onto Q1 (front + rear wall dovetails, floor tabs) → Q3 down onto Q1 (left wall dovetail, tabs) → Q4 down onto Q2 + Q3 → facia screwed across Q1–Q2.",
          "Runner test (P3) on the assembled drawer before any glue. Housing top above it is four loose tiles (clipped, P4), not part of the drawer."]:
    text(CX, y, l, 8, fill="#444"); y += 13

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1130 760" width="1130" height="760" font-family="Helvetica, Arial, sans-serif">\n'
       f'<rect width="1130" height="760" fill="#ffffff"/>\n' + "\n".join(out) +
       '\n<text x="20" y="748" font-size="8" fill="#888">drawer-quarters v1 — D2 option (a) — 2026-09-15 — for approval; supersedes "2 x drawer halves" in layout v15</text>\n</svg>\n')
outdir = sys.argv[1] if len(sys.argv) > 1 else "."
open(os.path.join(outdir, "drawer-quarters-v1.svg"), "w").write(svg)
if cairosvg:
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(outdir, "drawer-quarters-v1.pdf"))
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(outdir, "drawer-quarters-v1.png"), output_width=2260)
print("ok")
