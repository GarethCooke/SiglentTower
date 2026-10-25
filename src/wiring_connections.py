# wiring_connections.py — every connection in the lighting, on one sheet (D10 rev 4, 2026-10-25).
# SN74AHCT125N level shifter on both data lines; strips are 15 LEDs each (30/m strip); every plug is a 2.54 mm locking
# pin header (KF2510 type) soldered on the board with a crimped housing on the cable (SN-28B crimper): sill bundle on a
# 4-pin (red, green, blue, black) + 2-pin (yellow), strips on 3-pin L and R.
# Output: parts/wiring/wiring-4-connections.png
import os, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "parts", "wiring"))
RED, BLK, GRN, BLU, YEL = "#d62728", "#222", "#2ca02c", "#1f5fd6", "#d49a00"
fig, ax = plt.subplots(figsize=(19, 12.5)); ax.set_xlim(0, 180); ax.set_ylim(0, 118); ax.axis("off")
Z = dict(zorder=2)

def box(x, y, w, h, fc="#fff", ec=BLK, lw=1.2, r=0.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={r}", fc=fc, ec=ec, lw=lw, zorder=1))
def txt(x, y, s, **k):
    k.setdefault("fontsize", 9); k.setdefault("va", "center"); ax.text(x, y, s, zorder=6, **k)
def tag(x, y, s, c, ha="center", fs=8.5):
    ax.text(x, y, s, ha=ha, va="center", fontsize=fs, color="w", weight="bold", zorder=7,
            bbox=dict(boxstyle="round,pad=0.25", fc=c, ec=c))
def dot(x, y, c): ax.add_patch(Circle((x, y), 0.65, fc=c, ec=c, zorder=8))

def path(pts, c, lw=2.6, hops=()):
    """Polyline; hops = [(x, y)] points on horizontal or vertical segments where this wire jumps another."""
    X, Y = [pts[0][0]], [pts[0][1]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        hs = [h for h in hops if (y0 == y1 == h[1] and min(x0, x1) < h[0] < max(x0, x1)) or
              (x0 == x1 == h[0] and min(y0, y1) < h[1] < max(y0, y1))]
        if y0 == y1: hs.sort(key=lambda h: h[0], reverse=x1 < x0)
        else: hs.sort(key=lambda h: h[1], reverse=y1 < y0)
        for hx, hy in hs:
            t = np.linspace(np.pi, 0, 16)
            if y0 == y1:
                s = 1 if x1 > x0 else -1
                X += list(hx - s * 1.2 * np.cos(t)); Y += list(hy + 1.2 * np.sin(t))
            else:
                s = 1 if y1 > y0 else -1
                X += list(hx + 1.2 * np.sin(t)); Y += list(hy - s * 1.2 * np.cos(t))
        X.append(x1); Y.append(y1)
    ax.plot(X, Y, color=c, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=3)

ax.text(1, 115.5, "Lighting — every connection (D10 rev 4, 2026-10-25)", fontsize=15, weight="bold")
ax.text(1, 112, "Wire colours are the real ones:  red 5 V · black GND · green data · blue data back from the sill lights · yellow button switch.     "
        "● = soldered together     bump = wires cross, NOT joined     red tag = board 5 V, black tag = board GND",
        fontsize=9.5)

# ---------------------------------------------------------------- Addtam + USB
box(2, 33, 26, 18, fc="#eee")
txt(15, 46, "ADDTAM power strip", ha="center", weight="bold")
txt(15, 41.5, "one USB-A port\n(the top end)", ha="center", fontsize=8.5)
path([(28, 38), (44, 38)], RED); path([(28, 35), (44, 35)], BLK)
txt(34, 41, "USB pigtail\n550 mm", ha="center", fontsize=8)

# ---------------------------------------------------------------- the board
box(40, 30, 64, 77, fc="#eef3fb")
txt(72, 105, "PERFBOARD in the holder on the rear base rail", ha="center", weight="bold", fontsize=10)
# USB in + cap
ax.add_patch(Rectangle((44, 34), 4, 5, fc="#cc0", ec=BLK, zorder=4)); txt(46, 41, "USB in", ha="center", fontsize=8)
tag(51.5, 38, "5V", RED); tag(51.5, 35, "GND", BLK)
ax.add_patch(Circle((60, 36.5), 2.6, fc="#345", ec=BLK, zorder=4)); txt(60, 36.5, "1000\nµF", ha="center", fontsize=6.5, color="w")
txt(63.5, 38.5, "+ leg → 5V", fontsize=8); txt(63.5, 34.5, "striped leg → GND", fontsize=8)
# D1 mini
box(44, 49, 13, 51, fc="#2b6cb0", ec=BLK)
txt(48.5, 74, "WEMOS D1 mini", ha="center", color="w", weight="bold", rotation=90, fontsize=10)
P = {}
for i, p in enumerate(["5V", "G", "D4", "D3", "D2", "D1", "RX", "TX"]):
    y = 96 - i * 6; P[p] = y
    ax.add_patch(Rectangle((57, y - 0.9), 2.4, 1.8, fc="#cc0", ec=BLK, zorder=4))
    txt(56.2, y, p, ha="right", color="w", weight="bold", fontsize=9.5)
tag(62.2, P["5V"], "5V", RED); tag(62.4, P["G"], "GND", BLK)
for p in ("D2", "D1", "TX"): txt(60.3, P[p], "empty", fontsize=7.5, color="#888")
# chip
CX0, CX1, CY0, CY1 = 71, 84, 63, 85
ax.add_patch(Rectangle((CX0, CY0), CX1 - CX0, CY1 - CY0, fc="#333", ec=BLK, zorder=4))
txt((CX0 + CX1) / 2, 74, "SN74AHCT\n125N", ha="center", color="w", fontsize=8.5, weight="bold")
IN5, IN2 = 80, 68
for y, a, b in ((IN5, "5", "6"), (IN2, "2", "3")):
    txt(CX0 + 0.5, y, a, color="w", fontsize=8); txt(CX1 - 0.5, y, b, color="w", fontsize=8, ha="right")
# connectors: 2.54 mm locking pin headers (KF2510 type) soldered on the board, crimped housings on the cables
J4 = dict(data=101, v5=98, gnd=95); J2 = dict(sw=87, nc=84); J1 = dict(red=76, grn=73, blu=70, blk=67); J3 = dict(data=57, v5=54, gnd=51)
def conn(ys, name):
    y0, y1 = min(ys) - 1.6, max(ys) + 1.6
    ax.add_patch(Rectangle((103, y0), 4, y1 - y0, fc="#bbb", ec=BLK, zorder=5))
    ax.add_patch(Rectangle((107.4, y0), 4, y1 - y0, fc="#777", ec=BLK, zorder=5))
    txt(109.4, y1 + 1.4, name, ha="center", fontsize=8, weight="bold")
conn(J4.values(), "R  3-pin"); conn(J2.values(), "2-pin"); conn(J1.values(), "4-pin"); conn(J3.values(), "L  3-pin")
txt(105, 27.5, "grey = pin header soldered on the board · dark = crimped housing on the cable · L and R are identical plugs: label them",
    ha="center", fontsize=8, style="italic")
# board wiring
txt((CX0 + CX1) / 2, 60.3, "chip pin 14 → 5V\npins 1 4 7 9 10 12 13 → GND\npins 8, 11 empty", ha="center", fontsize=7.5)
path([(59.4, P["D4"]), (65, P["D4"]), (65, IN5), (CX0, IN5)], GRN)
path([(59.4, P["RX"]), (67, P["RX"]), (67, IN2), (CX0, IN2)], GRN)
YSW = 91
path([(59.4, P["D3"]), (68.5, P["D3"]), (68.5, YSW), (100, YSW), (100, J2["sw"]), (103, J2["sw"])], YEL, hops=[(87.5, YSW)])
for yout, ydst in ((IN5, J4["data"]), (IN2, J1["grn"])):
    path([(CX1, yout), (87.5, yout), (87.5, ydst), (90, ydst)], GRN)
    ax.add_patch(Rectangle((90, ydst - 1), 6.5, 2, fc="#dcb", ec=BLK, zorder=5)); txt(93.25, ydst + 2, "330 Ω", ha="center", fontsize=7.5)
    path([(96.5, ydst), (103, ydst)], GRN)
for d in (J4, J3):
    path([(100.5, d["v5"]), (103, d["v5"])], RED); tag(98, d["v5"], "5V", RED, fs=7.5)
    path([(100.5, d["gnd"]), (103, d["gnd"])], BLK); tag(98, d["gnd"], "GND", BLK, fs=7.5)
path([(100.5, J1["red"]), (103, J1["red"])], RED); tag(98, J1["red"], "5V", RED, fs=7.5)
path([(100.5, J1["blk"]), (103, J1["blk"])], BLK); tag(97.6, J1["blk"], "GND", BLK, fs=7.5)
path([(103, J1["blu"]), (101.8, J1["blu"]), (101.8, J3["data"]), (103, J3["data"])], BLU, hops=[(101.8, J1["blk"])])
txt(99.8, 62, "blue passes\nstraight to\nL data", ha="right", fontsize=7, color=BLU)
ax.text(109.4, J2["nc"], "–", ha="center", va="center", fontsize=8, color="#ddd", zorder=9)

# ---------------------------------------------------------------- cables out
for y, c in ((J4["data"], GRN), (J4["v5"], RED), (J4["gnd"], BLK)): path([(111.4, y), (126, y)], c)
txt(118.5, 104, "320 mm", ha="center", fontsize=8.5)
for y, c in ((J3["data"], BLU), (J3["v5"], RED), (J3["gnd"], BLK)): path([(111.4, y), (126, y)], c)
txt(118.5, 60, "200 mm", ha="center", fontsize=8.5)
for y, c in ((J2["sw"], YEL), (J1["red"], RED), (J1["grn"], GRN), (J1["blu"], BLU), (J1["blk"], BLK)): path([(111.4, y), (126, y)], c)
txt(118.5, 90, "sill bundle\n5 wires, 650 mm", ha="center", fontsize=8.5)

# ---------------------------------------------------------------- strips
def strip(y0, name, ydata, yv5, ygnd):
    box(126, y0, 52, 10, fc="#fff8e6")
    ax.add_patch(Rectangle((129, y0 + 3.5), 47, 3, fc="#f5f5f5", ec=BLK, zorder=4))
    for i in range(15): ax.add_patch(Rectangle((130 + i * 3.1, y0 + 4), 2, 2, fc="#ffd84d", ec=BLK, lw=0.6, zorder=5))
    txt(152, y0 + 8.6, name, ha="center", weight="bold", fontsize=9)
    txt(152, y0 + 1.6, "input end at the BOTTOM of the upright → (arrows point away from it)", ha="center", fontsize=7.5)
    for y, lab in ((ydata, "DIN"), (yv5, "5V"), (ygnd, "GND")): txt(126.6, y, lab, fontsize=7, color="#444")
strip(94, "RIGHT strip — 15 LEDs, rear-right upright (bus 2)", J4["data"], J4["v5"], J4["gnd"])
strip(47, "LEFT strip — 15 LEDs, rear-left upright (bus 1)", J3["data"], J3["v5"], J3["gnd"])

# ---------------------------------------------------------------- sill block
box(126, 60.5, 52, 30, fc="#fdf3d6")
txt(152, 89, "LEFT SILL BLOCK — every join here is soldered + heat-shrunk", ha="center", weight="bold", fontsize=9)
RR, RB = 80, 63.5
path([(126, J1["red"]), (129, J1["red"]), (129, RR), (176, RR)], RED); dot(129, RR, RED)
path([(126, J1["blk"]), (128, J1["blk"]), (128, RB), (176, RB)], BLK); dot(128, RB, BLK)
def pixel(x, n):
    ax.add_patch(Rectangle((x, 70.5), 10, 6, fc="#fff", ec=BLK, zorder=4))
    txt(x + 5, 73.5, f"sill light {n}\n5 mm WS2812", ha="center", fontsize=6.8)
    path([(x + 5, 76.5), (x + 5, RR)], RED); dot(x + 5, RR, RED); txt(x + 5.5, 78.2, "5V", fontsize=6.5)
    path([(x + 5, 70.5), (x + 5, RB)], BLK); dot(x + 5, RB, BLK); txt(x + 5.5, 65.6, "GND", fontsize=6.5)
    return x
p1 = pixel(134, 1); p2 = pixel(150, 2)
path([(126, J1["grn"]), (p1, J1["grn"])], GRN); txt(p1 - 0.3, 74.6, "DIN", fontsize=6.3, ha="right")
path([(p1 + 10, 73), (p2, 73)], GRN); txt(p1 + 10.3, 74.6, "DOUT→DIN", fontsize=6.3)
YB = 68.6
path([(p2 + 10, 73), (162, 73), (162, YB), (127, YB), (127, J1["blu"]), (126, J1["blu"])], BLU, hops=[(p1 + 5, YB), (p2 + 5, YB)])
txt(p2 + 10.3, 74.6, "DOUT", fontsize=6.3)
bx0 = 165
ax.add_patch(Circle((bx0 + 5.5, 72), 4.6, fc="#ddd", ec=BLK, zorder=4)); ax.add_patch(Circle((bx0 + 5.5, 72), 2.3, fc="#3a7bd5", ec=BLK, zorder=5))
txt(bx0 + 5.5, 66.2, "8 mm button", ha="center", fontsize=7)
path([(126, J2["sw"]), (bx0 + 4, J2["sw"]), (bx0 + 4, 76.4)], YEL, hops=[(bx0 + 4, RR)]); txt(bx0 + 4.4, 84.5, "switch 1", fontsize=6.5)
path([(bx0 + 1.5, 74), (bx0 + 1.5, RR)], RED); dot(bx0 + 1.5, RR, RED); txt(bx0 - 2.6, 78.2, "LED +", fontsize=6.5)
path([(bx0 + 8, 69), (bx0 + 8, RB)], BLK); dot(bx0 + 8, RB, BLK); txt(bx0 + 8.4, 61.8, "LED − & switch 2 (linked)", fontsize=6.3, ha="right")

# ---------------------------------------------------------------- WLED
box(2, 7, 176, 15, fc="#f6f6f6")
txt(4, 19.5, "WLED  (Config → LED Preferences)", weight="bold", fontsize=10)
ax.text(4, 16.8,
        "Output 1:  WS281x · GRB · GPIO 3 (RX) · start 0 · length 17      ← the 2 sill lights (0–1), then the left strip (2–16)\n"
        "Output 2:  WS281x · GRB · GPIO 2 (D4) · start 17 · length 15     ← the right strip (17–31)\n"
        "Maximum current: 1500 mA        Button 0: GPIO 0 (D3), Pushbutton        Segments: halo 0–1 · left 2–16 · right 17–31\n"
        "Short press = on/off; long press = next preset.  Everything after the first USB flash is over Wi-Fi (RX is the LED output, so no serial console).",
        fontsize=8.8, va="top", family="monospace", zorder=6)

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "wiring-4-connections.png"), dpi=110, bbox_inches="tight")
print("ok")
