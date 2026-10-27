# wiring_sheet.py — the lighting wiring runs on the frame (ROADMAP Stage 8, D10 rev 5, 2026-10-27). One sheet:
#   wiring-2-runs.png        where every wire goes on the frame: plan, rear-left corner, left side, lengths and covers
# Retired 2026-10-27 (D1 mini + WLED, rev 3): wiring-1-schematic -> wiring-4-connections.png (wiring_connections.py);
# wiring-3-board -> perfboard-layout.png (perfboard_layout.py) and board-enclosure-plan.png (enclosure_plan.py).
# Frame coordinates throughout: x from the outside of the left upright, y from the front plane, z from the rail bottoms
# (the frame stands 6 mm above the bench on its TPU feet).
import os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Polygon as P, Circle as C, FancyBboxPatch as FB
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "parts", "wiring"))
AL, ALD, BLUE, CAB, RED, BLK, GRN, YEL, WHT = "#c8c8c8", "#9a9a9a", "#2d6cdf", "#e8b04b", "#d33", "#222", "#2a8", "#dc3", "#fff"
C5V, CGND, CDAT, CSW = RED, BLK, GRN, YEL      # wire colours on the sheets: 5 V red, GND black, data green, switch yellow

def finish(ax, title, xl=None, yl=None, xlim=None, ylim=None, ncol=2, legend=True):
    ax.set_title(title, fontsize=10); ax.set_aspect("equal")
    if xl: ax.set_xlabel(xl)
    if yl: ax.set_ylabel(yl)
    if xlim: ax.set_xlim(*xlim)
    if ylim: ax.set_ylim(*ylim)
    if legend: ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fontsize=7.5, ncol=ncol)

def bx(ax, x, y, w, h, text, fc="#f4f4f4", fs=8, ec="k"):
    ax.add_patch(FB((x, y), w, h, boxstyle="round,pad=0.4", fc=fc, ec=ec, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)

def wire(ax, pts, color, lw=2, label=None, ls="-"):
    ax.add_patch(P(pts, closed=False, fc="none", ec=color, lw=lw, ls=ls, label=label))

# ---------------------------------------------------------------- 2. runs
def sheet_runs():
    fig = plt.figure(figsize=(17, 15)); gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1])
    a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[1, :])
    # a: plan of the whole frame
    for x, y in ((0, 0), (341, 0), (0, 330), (341, 330)): a.add_patch(R((x, y), 20, 20, fc=ALD, ec="k", label="uprights" if (x, y) == (0, 0) else None))
    a.add_patch(R((0, 20), 20, 310, fc=AL, ec="k", label="side rails (PSU level shown)")); a.add_patch(R((341, 20), 20, 310, fc=AL, ec="k"))
    a.add_patch(R((20, 330), 321, 20, fc=AL, ec="k", label="rear base cross rail"))
    a.add_patch(R((20.3, 3), 47.7, 16.5, fc="#777", ec="k", label="sill left block (button + pixel) x 20–68"))
    a.add_patch(R((1, 355), 78, 30, fc="#eee", ec="k", label="Addtam strip (behind the frame, z 75–425)"))
    a.add_patch(R((90, 350), 60, 40.5, fc=BLUE, ec="k", alpha=0.8, label="BOARD ENCLOSURE x 90–150, y 350–390.5 on the rail's rear face"))
    a.add_patch(R((10, 20), 8, 470 and 0.01, fc="none", ec="none"))
    for x in (14, 341): a.add_patch(R((x, 336), 6, 8, fc="#8bd", ec="k", label="LED strips (15 LEDs each): on the rear uprights' INNER faces from z 20, the top bent onto the top rail's underside" if x == 14 else None))
    for y0, y1 in ((20, 40), (310, 330)): a.add_patch(R((14, y0), 6, y1 - y0, fc=RED, ec="k", alpha=0.5, label="hidden L-connectors in the slot ends (wires hop over them)" if y0 == 20 else None))
    a.add_patch(R((17.5, 45), 2.5, 260, fc=BLUE, ec="k", label="cover A: left PSU rail inner slot, y 45–305"))
    a.add_patch(R((25, 348), 65, 2.5, fc=BLUE, ec="k", label="cover B1 / B2: rear base rail REAR slot, x 25–90 and x 150–336"))
    a.add_patch(R((150, 348), 186, 2.5, fc=BLUE, ec="k"))
    wire(a, [(45, 19.5), (21, 19.5), (21, 340), (23, 340), (25, 352), (100, 352)], CDAT, 2.5, label="SILL bundle (5 wires: 5 V, GND, data, data back, switch): block → PSU rail slot → upright slot → under the rail → rear slot → left passage")
    wire(a, [(100, 353), (26, 353), (24, 342), (22, 338)], C5V, 2.5, label="LEFT strip feed (3: 5 V, GND, data): left passage → rear slot → under the rail → up the upright slot to z 20")
    wire(a, [(140, 352), (336, 352), (338, 342), (340, 338)], CGND, 2.5, label="RIGHT strip feed (3): right passage → rear slot → under the rail → up the rear-right upright's slot")
    wire(a, [(82, 380), (88, 380), (95, 366)], "#a0a", 2.5, label="USB lead: Addtam's top-end port, down beside the strip, in through the lid's notch to the 2-pin at the board's top")
    a.annotate("under the rail here\n(6 mm on the feet)", (24, 345), (60, 300), arrowprops=dict(arrowstyle="->"), fontsize=8)
    a.annotate("and here", (338, 345), (290, 300), arrowprops=dict(arrowstyle="->"), fontsize=8)
    finish(a, "1. Plan — every run lives in a slot; the only wire in the open is the USB lead behind the frame", "frame x (mm)", "frame y (mm)", (-15, 375), (-10, 395), ncol=1)
    # b: rear elevation of the rear-left corner (seen from BEHIND, drawn in frame x)
    b.add_patch(R((0, 0), 20, 130, fc=ALD, ec="k", label="rear-left upright")); b.add_patch(R((20, 0), 321, 20, fc=AL, ec="k", label="rear base cross rail z 0–20"))
    b.add_patch(R((20, 7.05), 321, 5.9, fc="white", ec="k", label="its REAR slot (mouth), centre z 10 — wires + covers live here"))
    b.add_patch(R((-2, -6), 24, 6, fc=BLUE, ec="k", label="TPU foot (frame stands 6 above the bench)"))
    b.add_patch(R((1, 75), 78, 55, fc="#eee", ec="k", label="Addtam body z 75–425 (USB ports at its TOP end, off this view)"))
    b.add_patch(R((0, 51), 80, 24, fc="#bbb", ec="k", alpha=0.6, label="lower strip bracket + shelf z 51–75"))
    b.add_patch(R((14, -6), 32, 57, fc="none", ec="#777", ls="--", label="Addtam mains cable drops here (x 14–46)"))
    b.add_patch(R((90, 0), 60, 108, fc=BLUE, ec="k", alpha=0.4, label="BOARD ENCLOSURE x 90–150, z 0–108 (+3 flange), M5 into the rear slot at (120, 10); hex lid over the parts"))
    b.add_patch(R((94.6, 28), 50, 70, fc="#e9f0fb", ec="k", label="perfboard 50 × 70 on the ledge at z 28, slid in from the top, parts facing you; plugs along its bottom edge over the wire bay"))
    for x in (92, 132): b.add_patch(R((x, 6), 16, 8, fc="white", ec="k", label="wire passages 16 × 8 through the plate onto the slot (a crimped plug passes)" if x == 92 else None))
    b.add_patch(R((25, 7.05), 65, 5.9, fc=BLUE, ec="k", alpha=0.7, label="cover B1 x 25–90 (65) and B2 x 150–336 (186)"))
    b.add_patch(R((150, 7.05), 100, 5.9, fc=BLUE, ec="k", alpha=0.7))
    wire(b, [(10, 125), (10, 2), (14, -3), (24, -3), (26, 2), (26, 10), (100, 10), (100, 26)], CDAT, 2.5, label="sill bundle down the upright's inner slot (under the strip), under the rail, along the rear slot, up through the left passage to the 5-pin")
    wire(b, [(100, 24), (100, 12), (28, 12), (28, 4), (12, 4), (12, 22)], C5V, 2, label="left strip feed (from the L 3-pin), the same way back, up to the strip's bottom at z 20")
    wire(b, [(140, 26), (140, 10), (250, 10)], CGND, 2.5, label="right strip feed → along the rear slot to x 336 → under the rail → up the rear-right upright")
    wire(b, [(82, 130), (82, 100), (101.8, 100)], "#a0a", 2.5, label="USB lead from the Addtam's top port, down its right-hand edge, in through the lid's notch to the 2-pin (x 101.8, board top)")
    b.text(200, 95, "Seen from BEHIND the frame, drawn in frame x\n(left upright on the left). The rail's rear slot is\nempty by design — its connectors are on the front face.", fontsize=8, ha="center")
    finish(b, "2. Rear elevation, rear-left corner — the enclosure, the under-rail passes, the USB lead", "frame x (mm)", "frame z (mm)", (-15, 260), (-12, 135), ncol=1)
    # c: left side seen from inside the frame (as tpu-where-2), now with the sill bundle and the pixel return
    c.add_patch(R((0, 0), 20, 130, fc=ALD, ec="k", label="front-left upright")); c.add_patch(R((330, 0), 20, 130, fc=ALD, ec="k", label="rear-left upright"))
    c.add_patch(R((20, 0), 310, 20, fc=AL, ec="k", label="base rail")); c.add_patch(R((20, 68), 310, 20, fc=AL, ec="k", label="left PSU rail z 68–88"))
    c.add_patch(R((20, 75.05), 310, 5.9, fc="white", ec="k", label="inner-face slot mouth, centre z 78"))
    for y0, y1 in ((20, 40), (310, 330)): c.add_patch(R((y0, 75.05), y1 - y0, 5.9, fc=RED, ec="k", alpha=0.5, label="hidden L-connector in the slot" if y0 == 20 else None))
    c.add_patch(R((45, 75), 260, 6, fc=BLUE, ec="k", label="cover A y 45–305 (one 240 + one 20)"))
    c.add_patch(R((3, 87), 16.5, 12, fc="#777", ec="k", label="sill left block z 87–99: the two pixels' legs and the button wires leave its BOTTOM at x 34–58"))
    c.add_patch(R((336, 20), 8, 110, fc="#8bd", ec="k", alpha=0.6, label="LED strip on the rear-left upright's inner face from z 20 (15 LEDs, top bent under the top rail), over its slot — fed at the BOTTOM"))
    c.add_patch(R((336, 20), 8, 3, fc=RED, ec="k", label="strip input (soldered wires at z 20)"))
    wire(c, [(19, 87), (19, 78), (20, 78), (20, 84), (42, 84), (42, 78), (308, 78), (308, 84), (330, 84), (335, 78), (340, 78), (340, -4), (355, -4)], CDAT, 2.5, label="SILL bundle: 5 wires (5 V, GND, data to the pixels, data back from them, switch) — to the board")
    wire(c, [(355, -2), (342, -2), (342, 20)], C5V, 2, label="left strip feed (5 V, GND, data) from the board's L 3-pin")
    c.text(175, 110, "Bundle block → board ≈ 510 mm: the five wires are 650. The data-back wire (blue) goes all the way to the board's 5-pin and crosses to the L 3-pin there.\n"
                     "Cover A: 240 + 20 with scissors, stop 25 short of each rail end.\n"
                     "In the upright's slot the wires sit under the strip (z 20–78) then in the open 20 mm at the bottom, under the rail at x 23–28, beside the foot.",
           ha="center", fontsize=8.5)
    finish(c, "3. Left side, seen from INSIDE the frame — the sill bundle's route to the board, and the left strip's feed (D10 rev 5)", "frame y (mm)", "frame z (mm)", (-10, 370), (-12, 135), ncol=3)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "wiring-2-runs.png"), dpi=100); plt.close(fig)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet_runs()
    print("wrote", OUT)
