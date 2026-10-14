# tray_plan.py — PROPOSAL sheet (2026-10-14, D13): a second, enclosed box in the gap between the scope's rear bumpers and
# the rear box, riding on two new rails glued to the sled; plus the rear-box corner braces. Nothing here is modelled yet
# except the braces (parts/box_brace.py).  python src/tray_plan.py -> parts/scope-tray-plan.png
import os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Polygon
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "parts"))

# ---- the sled as built (frame coordinates) ----
BEAMS = [(20, 60), (301, 341)]; BEAM_Z = (337, 346); BEAM_Y = (3, 330)
CUPS = [(46.5, 86), (275, 314.5)]; CUP_Y = (91, 126); CUP_Z = (337, 347)
FRONT_BAR = (3, 12); FRONT_BAR_Z = (337, 355)
XBAR_F, XBAR_F_LIP = (189, 210), (189, 194); XBAR_R, XBAR_R_LIP = (308, 336), (331, 336); XBAR_Z = (337, 346); LIP_Z = (346, 356)
BOX = (50, 341, 195, 330, 346, 456); BOX_LIP_H = 20
CHANNEL = (20, 46, 140, 334, 346, 366)                      # cable channel (D6) — planned, not printed
SCOPE = (23, 338, 3, 111, 355, 507); IEC = (30, 58, 111, 141, 360, 380)
TOP_RAIL_Z = 490; TOP_PANEL_Z = 510; DOOR_Y = (20, 250)
# ---- proposed ----
BAR_A = (20, 341, 126, 138, 346, 349); BAR_A_UP = (20, 341, 126, 129, 349, 356)        # tray bar: shelf on the beams + upstand against the cup bosses
BAR_B = (20, 341, 183, 189, 346, 349); BAR_B_UP = (20, 341, 186, 189, 349, 356)        # ledge: shelf + leg glued to the cross bar's lip face
TRAY = (111, 341, 129.5, 185.5, 349, 479); LID_Z = (479, 482); WALL = 2.4

def rect(ax, x0, x1, y0, y1, **kw): ax.add_patch(R((x0, y0), x1 - x0, y1 - y0, **kw))

fig = plt.figure(figsize=(17, 12)); gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1], height_ratios=[1.15, 1])

# ---------- plan ----------
a = fig.add_subplot(gs[0, 0]); a.set_aspect("equal"); a.set_title("Sled from above — the new tray (blue) between the bumper cups and the rear box, on two glued rails (green)")
for x0, x1 in BEAMS: rect(a, x0, x1, *BEAM_Y, fc="#555", ec="k", lw=0.5)
rect(a, 23, 338, *FRONT_BAR, fc="#777", ec="k", lw=0.5); a.text(180, 7, "front bar", ha="center", va="center", fontsize=7, color="w")
for y0, y1 in (XBAR_F, XBAR_R): rect(a, 20, 341, y0, y1, fc="#555", ec="k", lw=0.5)
rect(a, 20, 341, *XBAR_F_LIP, fc="#333", ec="k", lw=0.5); rect(a, 20, 341, *XBAR_R_LIP, fc="#333", ec="k", lw=0.5)
for x0, x1 in CUPS: rect(a, x0, x1, *CUP_Y, fc="#888", ec="k", lw=0.5)
a.text(66, 108, "cup\nboss", ha="center", va="center", fontsize=7); a.text(295, 108, "cup\nboss", ha="center", va="center", fontsize=7)
rect(a, *BOX[:4], fc="#bbb", ec="k", lw=0.8); a.text(195, 262, "rear box (meters)\nx 50–341, y 195–330", ha="center", va="center", fontsize=9)
rect(a, *CHANNEL[:4], fc="none", ec="k", ls="--", lw=0.8); a.text(33, 240, "cable\nchannel\n(planned)", ha="center", va="center", fontsize=6.5, rotation=90)
rect(a, *SCOPE[:4], fc="#e9e3d3", ec="k", lw=0.5, alpha=0.7); a.text(180, 57, "scope body (y 3–111); bumpers in the cups to y 126", ha="center", va="center", fontsize=8)
rect(a, *IEC[:4], fc="#222", ec="k"); a.text(85, 175, "IEC plug +\nUSB/LAN leads\ndrop into the\nchannel here", ha="center", va="top", fontsize=6.5)
rect(a, *BAR_A[:4], fc="#5a9e5a", ec="k", lw=0.6); rect(a, *BAR_B[:4], fc="#5a9e5a", ec="k", lw=0.6)
rect(a, *TRAY[:4], fc="#2d6cdf", ec="k", lw=0.8, alpha=0.75)
a.text((TRAY[0] + TRAY[1]) / 2, (TRAY[2] + TRAY[3]) / 2, "NEW TRAY  230 × 56 × 130 (+3 lid)\nx 111–341, y 129.5–185.5", ha="center", va="center", fontsize=9, color="w")
a.annotate("A: tray bar — 321 × 12 × 3 shelf on both beams, 7 mm upstand\nalong its front edge against the cup bosses' rear faces (y 126). CA.\nTies the beams behind the scope — the roadmap's 'third bar'.",
           (200, 132), (120, 95), fontsize=7.5, arrowprops=dict(arrowstyle="->"), bbox=dict(fc="w", ec="#5a9e5a"))
a.annotate("B: ledge — 321 × 6 × 3 shelf + 7 mm leg CA'd to the\nfront face of the cross bar's lip (y 189).", (200, 186), (60, 300), fontsize=7.5,
           arrowprops=dict(arrowstyle="->"), bbox=dict(fc="w", ec="#5a9e5a"))
a.annotate("tray slides OUT to the right over the beam, through the door\n(y 20–250) — with the sled HOME, no need to pull the scope", (341, 157), (355, 60), fontsize=7.5,
           arrowprops=dict(arrowstyle="->", lw=1.5, color="#2d6cdf"))
a.annotate("left end at x 111:\n61 mm kept clear for\nthe scope's plug and leads", (111, 140), (-65, 95), fontsize=7.5, arrowprops=dict(arrowstyle="->"))
a.text(361 + 3, 135, "right\nbeam", fontsize=6.5, va="center")
a.set_xlim(-70, 470); a.set_ylim(-10, 350); a.set_xlabel("frame x (mm)"); a.set_ylabel("frame y (mm, front at 0)")

# ---------- side section ----------
b = fig.add_subplot(gs[0, 1]); b.set_aspect("equal"); b.set_title("Section at x ≈ 200, looking from the right (y–z)")
rect(b, BEAM_Y[0], BEAM_Y[1], *BEAM_Z, fc="#555", ec="k", lw=0.5); b.text(60, 341, "beam (x 20–60 / 301–341)", fontsize=7, va="center", color="w")
rect(b, *CUP_Y, *CUP_Z, fc="#888", ec="k", lw=0.5); b.text(108, 351, "cup boss", fontsize=7, ha="center")
rect(b, *XBAR_F, *XBAR_Z, fc="#555", ec="k", lw=0.5); rect(b, *XBAR_F_LIP, *LIP_Z, fc="#333", ec="k", lw=0.5); b.text(191, 360, "lip", fontsize=7, ha="center")
rect(b, *XBAR_R, *XBAR_Z, fc="#555", ec="k", lw=0.5); rect(b, *XBAR_R_LIP, *LIP_Z, fc="#333", ec="k", lw=0.5)
rect(b, BOX[2], BOX[3], BOX[4], BOX[4] + 3, fc="#bbb", ec="k", lw=0.5)
rect(b, BOX[2], BOX[2] + WALL, BOX[4], BOX[4] + BOX_LIP_H, fc="#bbb", ec="k", lw=0.5); rect(b, BOX[3] - WALL, BOX[3], BOX[4], BOX[5], fc="#bbb", ec="k", lw=0.5)
b.text(262, 400, "rear box", fontsize=9, ha="center")
rect(b, SCOPE[2], SCOPE[3], SCOPE[4], SCOPE[5], fc="#e9e3d3", ec="k", lw=0.5, alpha=0.7); b.text(57, 430, "scope", fontsize=10, ha="center")
rect(b, 98, 126, 341, 355, fc="#333", ec="k", lw=0.5); b.text(112, 348, "bumper", fontsize=6, ha="center", color="w")
rect(b, 0, 350, TOP_RAIL_Z, TOP_RAIL_Z + 20, fc="#999", ec="k", lw=0.5); b.text(175, 500, "top rail", fontsize=8, ha="center")
rect(b, 0, 350, TOP_PANEL_Z, TOP_PANEL_Z + 3, fc="#333", ec="k", lw=0.5)
rect(b, BAR_A[2], BAR_A[3], BAR_A[4], BAR_A[5], fc="#5a9e5a", ec="k", lw=0.6); rect(b, BAR_A_UP[2], BAR_A_UP[3], BAR_A_UP[4], BAR_A_UP[5], fc="#5a9e5a", ec="k", lw=0.6)
rect(b, BAR_B[2], BAR_B[3], BAR_B[4], BAR_B[5], fc="#5a9e5a", ec="k", lw=0.6); rect(b, BAR_B_UP[2], BAR_B_UP[3], BAR_B_UP[4], BAR_B_UP[5], fc="#5a9e5a", ec="k", lw=0.6)
rect(b, TRAY[2], TRAY[3], TRAY[4], TRAY[5], fc="#2d6cdf", ec="k", lw=0.8, alpha=0.75)
rect(b, TRAY[2] + WALL, TRAY[3] - WALL, TRAY[4] + 3, TRAY[5], fc="w", ec="none")
rect(b, TRAY[2] - 1, TRAY[3] + 1, LID_Z[0], LID_Z[1], fc="#1e3a8a", ec="k", lw=0.6); b.text(157, 486, "lid (drop-on, 3)", fontsize=7, ha="center")
b.text(157, 415, "tray\n130 tall\n56 wide", ha="center", va="center", fontsize=9)
b.annotate("A", (132, 352), (120, 375), fontsize=9, color="#2a6e2a", arrowprops=dict(arrowstyle="->")); b.annotate("B", (186, 352), (205, 375), fontsize=9, color="#2a6e2a", arrowprops=dict(arrowstyle="->"))
b.annotate("8 mm under the top rail", (157, 482), (230, 470), fontsize=7, arrowprops=dict(arrowstyle="->"))
b.annotate("18 mm behind the scope body", (120, 440), (130, 455), fontsize=7)
b.set_xlim(-5, 350); b.set_ylim(330, 520); b.set_xlabel("frame y (mm)"); b.set_ylabel("frame z (mm)")

# ---------- brace detail ----------
c = fig.add_subplot(gs[1, 0]); c.set_aspect("equal"); c.set_title("Rear box, right front corner from above: the corner brace (orange) glued inside — and the crack it bridges")
rect(c, 300, 341, 195, 240, fc="none", ec="none")
rect(c, 338.6, 341, 195, 240, fc="#bbb", ec="k", lw=0.6)                     # side wall
rect(c, 300, 341, 195, 197.4, fc="#bbb", ec="k", lw=0.6)                     # lip
rect(c, 334.6, 338.6, 197.4, 212.4, fc="#e8873a", ec="k", lw=0.6)            # wall leg
rect(c, 323.6, 338.6, 197.4, 201.4, fc="#e8873a", ec="k", lw=0.6)            # lip leg
c.text(336.6, 220, "side wall 2.4", fontsize=7, rotation=90, va="center"); c.text(318, 196.2, "front lip (20 tall)", fontsize=7, va="center", ha="center")
c.annotate("box-brace-v1: 15 × 15 × 4 L-angle, 100 tall,\nlying on the floor — one leg on the wall,\none on the lip; above the lip (z 366) that leg\nstands free as a flange along the wall's front edge",
           (330, 199.5), (302, 225), fontsize=7.5, arrowprops=dict(arrowstyle="->"), bbox=dict(fc="w", ec="#e8873a"))
c.set_xlim(298, 346); c.set_ylim(193, 242); c.set_xlabel("frame x (mm)"); c.set_ylabel("frame y (mm)")

d = fig.add_subplot(gs[1, 1]); d.set_aspect("equal"); d.set_title("Same corner from inside the box (y–z): the brace bridges the crack line")
rect(d, 195, 330, 346, 349, fc="#bbb", ec="k", lw=0.5); rect(d, 195, 197.4, 346, 366, fc="#bbb", ec="k", lw=0.5)
rect(d, 197.4, 330, 349, 456, fc="#ddd", ec="k", lw=0.5); d.text(265, 400, "right side wall (inner face)", fontsize=8, ha="center")
d.plot([197.4, 250], [366, 366], color="r", lw=2, ls="--"); d.text(252, 366, "crack: horizontal (a layer line)\nfrom the lip's top corner", color="r", fontsize=7.5, va="center")
rect(d, 197.4, 212.4, 349, 449, fc="#e8873a", ec="k", lw=0.6, alpha=0.9); d.text(205, 420, "brace\n(wall leg)", fontsize=7, ha="center", rotation=90, va="center")
rect(d, 197.4, 201.4, 349, 449, fc="#c96a1e", ec="k", lw=0.6)
d.text(199.4, 440, "lip leg", fontsize=6, rotation=90, ha="center", va="center", color="w")
d.annotate("printed lying on the wall leg:\nlayer lines run UP the wall in use", (205, 380), (225, 440), fontsize=7.5, arrowprops=dict(arrowstyle="->"))
d.set_xlim(190, 330); d.set_ylim(340, 462); d.set_xlabel("frame y (mm)"); d.set_ylabel("frame z (mm)")

fig.suptitle("Proposal D13 — scope-back tray on two glued rails (A, B) + rear-box corner braces (box-brace-v1, modelled)", fontsize=13)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "scope-tray-plan.png"), dpi=105); print("ok")
