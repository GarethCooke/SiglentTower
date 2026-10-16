# wiring_sheet.py — the lighting wiring (ROADMAP Stage 8, D10 rev 3, 2026-10-16). Three sheets in parts/wiring/:
#   wiring-1-schematic.png   what connects to what: board, pigtails, strips, pixel, button, Addtam, WLED settings
#   wiring-2-runs.png        where every wire goes on the frame: plan, rear-left corner, left side, lengths and covers
#   wiring-3-board.png       the 50 x 40 perfboard: D1 mini, parts, pads, and how it sits in the holder
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

# ---------------------------------------------------------------- 1. schematic
def sheet_schematic():
    fig, ax = plt.subplots(figsize=(17, 11)); ax.set_xlim(0, 170); ax.set_ylim(0, 110); ax.axis("off")
    ax.set_title("Lighting wiring 1 — what connects to what (D10 rev 3, 2026-10-16). Board: Wemos D1 mini running WLED.", fontsize=11)
    dot = lambda x, y, c: ax.add_patch(C((x, y), 0.6, fc=c, ec="none", zorder=5))
    # Addtam + USB pigtail -> board
    bx(ax, 2, 86, 26, 20, "ADDTAM strip\n(vertical, rear-left upright)\nUSB ports at the TOP end\n5 V, 4.5 A shared", fc="#eee")
    bx(ax, 34, 92, 22, 8, "USB-A → bare-wire\npigtail, cut to ~550", fc="#fff")
    wire(ax, [(28, 98), (34, 98)], C5V, 2.5); wire(ax, [(28, 94), (34, 94)], CGND, 2.5)
    wire(ax, [(56, 98), (66, 98)], C5V, 2.5); wire(ax, [(56, 94), (66, 94)], CGND, 2.5)
    # the board
    bx(ax, 62, 54, 46, 52, "", fc="#e9f0fb")
    ax.text(85, 103, "PERFBOARD 50 × 40, in the holder on the rear base rail", ha="center", fontsize=9, weight="bold")
    bx(ax, 66, 60, 26, 40, "D1 mini\n\n5V ···· 5 V in\nG ···· GND\nRX (GPIO3) ·· bus 1\nD3 (GPIO0) ·· button\nD4 (GPIO2) ·· bus 2", fc="#fff", fs=7.5)
    # pins on the mini's right edge (x 92): 5V 102 / G 98 / RX 96 / D3 88 / D4 84 — drawn as stubs to the board edge x 108
    bx(ax, 95, 94.8, 9, 2.4, "330 Ω", fc="#fff", fs=6.5); bx(ax, 95, 82.8, 9, 2.4, "330 Ω", fc="#fff", fs=6.5)
    wire(ax, [(92, 96), (95, 96)], CDAT, 2); wire(ax, [(104, 96), (122, 96)], CDAT, 2, label="data (28 AWG)")
    wire(ax, [(92, 84), (95, 84)], CDAT, 2); wire(ax, [(104, 84), (117, 84), (117, 46), (122, 46)], CDAT, 2)
    wire(ax, [(92, 88), (119, 88), (119, 92), (122, 92)], CSW, 2, label="button switch (28 AWG) → D3; its other side to GND inside the block")
    bx(ax, 94, 62, 12, 8, "1000 µF ×1\nacross 5 V / GND", fc="#fff", fs=6.5)
    ax.text(85, 56.5, "pigtail solder pads on the right-hand edge; 5 V and GND bussed along the bottom edge", ha="center", fontsize=7, style="italic")
    # 5 V and GND trunks down the right of the board, stubs to each load
    wire(ax, [(92, 102), (112, 102), (112, 44)], C5V, 2.5, label="5 V (24 AWG to the strips, 28 AWG to the sill)")
    wire(ax, [(92, 98), (114, 98), (114, 42)], CGND, 2.5, label="GND")
    for y in (100, 72, 44): wire(ax, [(112, y), (122, y)], C5V, 2.5); dot(112, y, C5V)
    for y in (98, 70, 42): wire(ax, [(114, y), (122, y)], CGND, 2.5); dot(114, y, CGND)
    wire(ax, [(112, 74), (100, 74), (100, 70)], C5V, 1.5); wire(ax, [(114, 76), (102, 76), (102, 70)], CGND, 1.5)   # caps hang on the trunks
    dot(112, 74, C5V); dot(114, 76, CGND)
    # loads
    bx(ax, 122, 88, 38, 18, "SILL LEFT BLOCK (front left)\n2 × 5 mm WS2812 pixels = LEDs 0–1 (chained, one in each slot)\n8 mm button with blue LED\n5 wires: 5 V · GND · data in · data out · switch", fc="#fdf3d6", fs=7.5)
    bx(ax, 122, 64, 38, 14, "LEFT STRIP — 28 × WS2812B (LEDs 2–29)\nrear-left upright, inner face\nfed at its BOTTOM (z 20)", fc="#dff0ff", fs=7.5)
    bx(ax, 122, 36, 38, 14, "RIGHT STRIP — 28 × WS2812B (LEDs 30–57)\nrear-right upright, inner face\nfed at its BOTTOM (z 20)", fc="#dff0ff", fs=7.5)
    wire(ax, [(160, 94), (166, 94), (166, 74), (160, 74)], CDAT, 2)
    ax.text(167, 84, "pixel 2 data OUT →\nleft strip data IN\n(comes back down\nthe same slot)", fontsize=7, va="center", color=CDAT)
    ax.text(141, 86.2, "button LED: + to 5 V, − to GND inside the block (3–6 V type; always on)", ha="center", fontsize=6.8)
    ax.text(141, 62.2, "bus 1 = RX (GPIO3): 2 pixels + left strip = 30 LEDs", ha="center", fontsize=8, weight="bold")
    ax.text(141, 34.2, "bus 2 = D4 (GPIO2): right strip = 28 LEDs", ha="center", fontsize=8, weight="bold")
    ax.text(163, 79.5, "JST-SM 4-pin + 2-pin\n(the ones you have)", fontsize=6.8, va="top")
    ax.text(163, 69, "JST-SM 3-pin pair (on order)", fontsize=6.8, va="top"); ax.text(163, 41, "JST-SM 3-pin pair (on order)", fontsize=6.8, va="top")
    # WLED settings
    bx(ax, 2, 12, 80, 38, "", fc="#f7f7f7")
    ax.text(42, 47.5, "WLED settings (Config → LED Preferences)", ha="center", fontsize=9, weight="bold")
    ax.text(4, 44.5, "LED outputs:\n  bus 1: WS281x, colour order GRB, GPIO 3, start 0, count 30\n  bus 2: WS281x, colour order GRB, GPIO 2, start 30, count 28\n"
                     "Maximum PSU current: 1500 mA   (58 LEDs full white would draw 3.5 A — the limit dims them)\n"
                     "Button 0: GPIO 0, type Pushbutton   (D3; WLED pulls it up, a press pulls it to GND)\n"
                     "Relay / status LED: none.   Serial debug is lost (RX drives bus 1) — updates go over the air.\n\n"
                     "Segments (main page → Segments):\n  0 'halo'  LEDs 0–1      1 'left'  LEDs 2–29      2 'right'  LEDs 30–57\n"
                     "Both strips are fed from the bottom, so both run upward — no 'reverse' needed.\n\n"
                     "First flash over the mini's own micro-USB at the desk BEFORE it goes in the holder, and put the\n"
                     "WiFi details in; everything after that is over the air (the micro-USB stays reachable in the holder).\n\n"
                     "Rule kept from D10: no level shifter — 3.3 V data through 330 Ω is fine over these runs.\n"
                     "If a strip ever flickers, a 74AHCT125 goes between the resistor and that strip.",
            fontsize=7.4, va="top", family="monospace")
    ax.text(88, 28, "Wire: 24 AWG silicone for 5 V / GND to the strips (1.5 A over 0.4 m = 0.1 V drop);\n"
                    "28 AWG for data, the button and all five sill wires — the five share a 5.9 × 3.6 slot\n"
                    "under a TPU cover, so thin wire matters there.\n"
                    "Colours on these sheets: red 5 V, black GND, green data, yellow switch.\n"
                    "Every run plugs in at the board: the board is the thing you will pull out,\n"
                    "the strips are stuck down and the sill block is behind the panel.\n"
                    "The 1 m strip cuts into two 28-LED pieces (cut on the marked line after LED 28).",
            fontsize=7.4, va="top")
    ax.legend(loc="lower left", bbox_to_anchor=(0.515, 0.02), fontsize=7.5, ncol=2)
    fig.savefig(os.path.join(OUT, "wiring-1-schematic.png"), dpi=100, bbox_inches="tight"); plt.close(fig)

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
    a.add_patch(R((90, 350), 60, 15, fc=BLUE, ec="k", alpha=0.8, label="BOARD HOLDER x 90–150 on the rail's rear face"))
    a.add_patch(R((10, 20), 8, 470 and 0.01, fc="none", ec="none"))
    for x in (14, 341): a.add_patch(R((x, 336), 6, 8, fc="#8bd", ec="k", label="LED strips: on the rear uprights' INNER faces, z 20–490 (seen end-on)" if x == 14 else None))
    for y0, y1 in ((20, 40), (310, 330)): a.add_patch(R((14, y0), 6, y1 - y0, fc=RED, ec="k", alpha=0.5, label="hidden L-connectors in the slot ends (wires hop over them)" if y0 == 20 else None))
    a.add_patch(R((17.5, 45), 2.5, 260, fc=BLUE, ec="k", label="cover A: left PSU rail inner slot, y 45–305"))
    a.add_patch(R((25, 348), 65, 2.5, fc=BLUE, ec="k", label="cover B1 / B2: rear base rail REAR slot, x 25–90 and x 150–336"))
    a.add_patch(R((150, 348), 186, 2.5, fc=BLUE, ec="k"))
    wire(a, [(45, 19.5), (21, 19.5), (21, 340), (23, 340), (25, 352), (100, 352)], CDAT, 2.5, label="SILL bundle (5 wires): block → PSU rail slot → upright slot → under the rail → rear slot → left hole")
    wire(a, [(100, 353), (26, 353), (24, 342), (22, 338)], C5V, 2.5, label="LEFT strip feed (3): left hole → rear slot → under the rail → up the upright slot to z 20")
    wire(a, [(140, 352), (336, 352), (338, 342), (340, 338)], CGND, 2.5, label="RIGHT strip feed (3): right hole → rear slot → under the rail → up the rear-right upright's slot")
    wire(a, [(82, 380), (88, 380), (95, 366)], "#a0a", 2.5, label="USB lead: Addtam's top-end port, down beside the strip, into the holder")
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
    b.add_patch(R((90, 0), 60, 44, fc=BLUE, ec="k", alpha=0.5, label="BOARD HOLDER x 90–150, z 0–44, M5 into the rear slot at (120, 10)"))
    b.add_patch(R((94.6, 3), 50, 40, fc="#e9f0fb", ec="k", label="perfboard 50 × 40, slid in from the top, parts facing you"))
    for x in (100, 140): b.add_patch(C((x, 10), 3.25, fc="white", ec="k", label="wire holes Ø6.5 through the plate, on the slot" if x == 100 else None))
    b.add_patch(R((25, 7.05), 65, 5.9, fc=BLUE, ec="k", alpha=0.7, label="cover B1 x 25–90 (65) and B2 x 150–336 (186)"))
    b.add_patch(R((150, 7.05), 100, 5.9, fc=BLUE, ec="k", alpha=0.7))
    wire(b, [(10, 125), (10, 2), (14, -3), (24, -3), (26, 2), (26, 10), (100, 10), (100, 20)], CDAT, 2.5, label="sill bundle down the upright's inner slot (under the strip), under the rail, along the rear slot, up through the left hole")
    wire(b, [(100, 18), (100, 12), (28, 12), (28, 4), (12, 4), (12, 22)], C5V, 2, label="left strip feed, the same way back, up to the strip's bottom at z 20")
    wire(b, [(140, 20), (140, 10), (250, 10)], CGND, 2.5, label="right strip feed → along the rear slot to x 336 → under the rail → up the rear-right upright")
    wire(b, [(82, 130), (82, 48), (120, 48), (120, 44)], "#a0a", 2.5, label="USB lead from the Addtam's top port, down its right-hand edge")
    b.text(130, 100, "Seen from BEHIND the frame, drawn in frame x\n(left upright on the left). The rail's rear slot is\nempty by design — its connectors are on the front face.", fontsize=8, ha="center")
    finish(b, "2. Rear elevation, rear-left corner — the holder, the under-rail passes, the USB lead", "frame x (mm)", "frame z (mm)", (-15, 260), (-12, 135), ncol=1)
    # c: left side seen from inside the frame (as tpu-where-2), now with the sill bundle and the pixel return
    c.add_patch(R((0, 0), 20, 130, fc=ALD, ec="k", label="front-left upright")); c.add_patch(R((330, 0), 20, 130, fc=ALD, ec="k", label="rear-left upright"))
    c.add_patch(R((20, 0), 310, 20, fc=AL, ec="k", label="base rail")); c.add_patch(R((20, 68), 310, 20, fc=AL, ec="k", label="left PSU rail z 68–88"))
    c.add_patch(R((20, 75.05), 310, 5.9, fc="white", ec="k", label="inner-face slot mouth, centre z 78"))
    for y0, y1 in ((20, 40), (310, 330)): c.add_patch(R((y0, 75.05), y1 - y0, 5.9, fc=RED, ec="k", alpha=0.5, label="hidden L-connector in the slot" if y0 == 20 else None))
    c.add_patch(R((45, 75), 260, 6, fc=BLUE, ec="k", label="cover A y 45–305 (one 240 + one 20)"))
    c.add_patch(R((3, 87), 16.5, 12, fc="#777", ec="k", label="sill left block z 87–99: the two pixels' legs and the button wires leave its BOTTOM at x 34–58"))
    c.add_patch(R((336, 20), 8, 110, fc="#8bd", ec="k", alpha=0.6, label="LED strip on the rear-left upright's inner face, z 20–490, over its slot — fed at the BOTTOM"))
    c.add_patch(R((336, 20), 8, 3, fc=RED, ec="k", label="strip input (JST at z 20)"))
    wire(c, [(19, 87), (19, 78), (20, 78), (20, 84), (42, 84), (42, 78), (308, 78), (308, 84), (330, 84), (335, 78), (340, 78), (340, -4), (355, -4)], CDAT, 2.5, label="SILL bundle: 5 wires (5 V, GND, data to the pixels, data back from them, switch) — to the board")
    wire(c, [(355, -2), (342, -2), (342, 20)], C5V, 2, label="left strip feed (5 V, GND) from the board")
    wire(c, [(338, 78), (338, 21)], CDAT, 1.5, ls="--", label="the pixel's data-back wire peels off the bundle and becomes the strip's data in")
    c.text(175, 110, "Bundle length block → board ≈ 510 mm: cut the five wires at 650. Cover A: 240 + 20 with scissors, stop 25 short of each rail end.\n"
                     "In the upright's slot the wires sit under the strip (z 20–78) then in the open 20 mm at the bottom, under the rail at x 23–28, beside the foot.",
           ha="center", fontsize=8.5)
    finish(c, "3. Left side, seen from INSIDE the frame — the sill bundle's route to the board, and the left strip's feed", "frame y (mm)", "frame z (mm)", (-10, 370), (-12, 135), ncol=3)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "wiring-2-runs.png"), dpi=100); plt.close(fig)

# ---------------------------------------------------------------- 3. board
def sheet_board():
    fig, (a, b) = plt.subplots(1, 2, figsize=(17, 9), gridspec_kw=dict(width_ratios=[1.3, 1]))
    # a: the perfboard, component side, as it sits in the holder (x across, z up; the mini's USB at the top edge)
    a.add_patch(R((0, 0), 50, 40, fc="#e9f0fb", ec="k", label="perfboard 50 × 40 (19 × 15 holes at 2.54), component side"))
    for i in range(19):
        for j in range(15): a.add_patch(C((2.17 + 2.54 * i, 2.22 + 2.54 * j), 0.45, fc="#c9a86a", ec="none"))
    a.add_patch(R((3, 6), 25.6, 34.2, fc="#246", ec="k", alpha=0.85, label="D1 mini on two 8-pin female headers (rows 22.86 apart), micro-USB at the TOP edge"))
    a.add_patch(R((11.3, 38), 8, 3, fc="#999", ec="k", label="micro-USB (points up, out of the holder's open top)"))
    a.text(15.8, 23, "D1 mini\n\n5V  G  D4  D3\nRX", ha="center", va="center", color="white", fontsize=8)
    a.add_patch(R((32, 33), 7, 2.5, fc="#dcb", ec="k", label="330 Ω ×2 (RX → bus 1, D4 → bus 2)")); a.add_patch(R((32, 28), 7, 2.5, fc="#dcb", ec="k"))
    a.add_patch(C((36, 20), 4.5, fc="#345", ec="k", label="1000 µF ×1 across 5 V / GND by the USB-in pads (stands ~12 tall, toward the rear)"))
    for z, lab in ((35.5, "SILL 4+2: 5V G Dout Dback · SW"), (22, "LEFT strip 3: 5V G D"), (11, "RIGHT strip 3: 5V G D"), (6, "USB in: 5V G")):
        a.add_patch(R((43, z - 1.5), 6, 3, fc=YEL, ec="k", label="pigtail solder pads on the right-hand edge" if z == 35.5 else None)); a.text(50.5, z, lab, fontsize=7.5, va="center")
    a.add_patch(R((0, 0.5), 50, 1.2, fc=RED, ec="none", alpha=0.6, label="5 V bus along the bottom edge; GND bus the row above")); a.add_patch(R((0, 2.2), 50, 1.2, fc=BLK, ec="none", alpha=0.5))
    a.text(25, -5, "Wire it so every pigtail lands on the right-hand edge: the holder's wire holes are at the bottom, so the pigtails\ndrop straight down behind the board and through. Keep the capacitors on the component side — the board's back has 3.5 mm.",
           ha="center", fontsize=8)
    finish(a, "1. The board, component side, as it sits in the holder (seen from behind the frame)", "mm", "mm", (-3, 80), (-12, 46), ncol=1)
    # b: section through the holder (x across, y out of the frame) at z 25
    b.add_patch(R((70, 330), 30, 20, fc=AL, ec="k", label="rear base rail (y 330–350)")); b.add_patch(R((70, 344), 30, 6, fc="none", ec="none"))
    b.add_patch(R((90, 350), 60, 5, fc=BLUE, ec="k", alpha=0.6, label="holder plate 5 thick, M5 at x 120 into the rail's rear slot (head under the board)"))
    b.add_patch(R((90, 355), 8.3, 10, fc=BLUE, ec="k", alpha=0.6, label="side walls 8.3, to y 365")); b.add_patch(R((141.7, 355), 8.3, 10, fc=BLUE, ec="k", alpha=0.6))
    for x0, d in ((94.3, 1), (145.7, -1)):
        b.add_patch(P([(x0, 358.3), (x0 + d * 4, 358.3), (x0 + d * 4, 362.8), (x0 + d * 1.5, 360.3), (x0, 360.3)], fc="white", ec="k", label="board slot 2.0 × 4.0 with a flat-then-45° roof (the board can't pull off)" if d == 1 else None))
    b.add_patch(R((94.6, 358.5), 50, 1.6, fc="#e9f0fb", ec="k", label="perfboard, 0.7 float each side, 3.5 off the plate for the header tails"))
    b.add_patch(R((98, 360.1), 25.6, 7, fc="#246", ec="k", alpha=0.6, label="D1 mini on its headers (components toward the rear, +y)"))
    b.add_patch(C((120, 352.5), 5, fc="#888", ec="k", alpha=0.7, label="M5 head in its Ø10 × 2.5 counterbore, 3.5 under the board"))
    b.annotate("rear of the frame →", (150, 372), (150, 376), fontsize=8, ha="right")
    finish(b, "2. Section through the holder at z 25 — plate on the rail, board in the slots, parts rearward", "frame x (mm)", "frame y (mm)", (65, 160), (326, 380), ncol=1)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "wiring-3-board.png"), dpi=100); plt.close(fig)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet_schematic(); sheet_runs(); sheet_board()
    print("wrote", OUT)
