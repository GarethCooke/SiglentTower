# wiring_connections.py — every connection in the lighting, on one sheet (D10 rev 4, 2026-10-25; v2 same day: the sill
# bundle on a 3-pin S (5V, GND, data — the strips' order) + a 2-pin (switch, data back); no 4-pin in hand).
# Supersedes wiring-1-schematic.png where they differ: SN74AHCT125N level shifter added (bus 1 and bus 2 data pass
# through it), strips are 15 LEDs each (30/m strip), sill bundle on JST-SM 4-pin + 2-pin, strips on 3-pin pairs.
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
# connectors (board halves, contacts recessed) at x 104 — every 3-pin in the same order: 5V, GND, data
J4 = dict(v5=101, gnd=98, data=95); J1 = dict(v5=88, gnd=85, data=82); J2 = dict(sw=74, blu=71); J3 = dict(v5=57, gnd=54, data=51)
def conn(ys, name):
    y0, y1 = min(ys) - 1.6, max(ys) + 1.6
    ax.add_patch(Rectangle((103, y0), 4, y1 - y0, fc="#bbb", ec=BLK, zorder=5))
    ax.add_patch(Rectangle((107.4, y0), 4, y1 - y0, fc="#777", ec=BLK, zorder=5))
    txt(109.4, y1 + 1.4, name, ha="center", fontsize=8, weight="bold")
conn(J4.values(), "R  3-pin"); conn(J1.values(), "S  3-pin"); conn(J2.values(), "2-pin"); conn(J3.values(), "L  3-pin")
txt(105, 27.5, "grey half on the board: contacts recessed · dark half on the cable: pins out · all three 3-pins wired 5V, GND, data in the same order", ha="center", fontsize=8, style="italic")
# board wiring
txt((CX0 + CX1) / 2, 88.5, "chip pin 14 → 5V\npins 1 4 7 9 10 12 13 → GND\npins 8, 11 empty", ha="center", fontsize=7.5)
path([(59.4, P["D4"]), (65, P["D4"]), (65, IN5), (CX0, IN5)], GRN)
path([(59.4, P["RX"]), (67, P["RX"]), (67, IN2), (CX0, IN2)], GRN)
path([(59.4, P["D3"]), (68.5, P["D3"]), (68.5, 59), (100, 59), (100, J2["sw"]), (103, J2["sw"])], YEL, hops=[(68.5, IN2)])
def res(x, y):
    ax.add_patch(Rectangle((x, y - 1), 6.5, 2, fc="#dcb", ec=BLK, zorder=5)); txt(x + 3.25, y + 2, "330 Ω", ha="center", fontsize=7.5)
path([(CX1, IN5), (86, IN5), (86, J4["data"]), (89.5, J4["data"])], GRN); res(89.5, J4["data"]); path([(96, J4["data"]), (103, J4["data"])], GRN)
path([(CX1, IN2), (88.5, IN2), (88.5, J1["data"]), (90, J1["data"])], GRN); res(90, J1["data"]); path([(96.5, J1["data"]), (103, J1["data"])], GRN)
for d in (J4, J1, J3):
    path([(100.5, d["v5"]), (103, d["v5"])], RED); tag(98, d["v5"], "5V", RED, fs=7.5)
    path([(100.5, d["gnd"]), (103, d["gnd"])], BLK); tag(98, d["gnd"], "GND", BLK, fs=7.5)
path([(103, J2["blu"]), (101.8, J2["blu"]), (101.8, J3["data"]), (103, J3["data"])], BLU, hops=[(101.8, J3["v5"]), (101.8, J3["gnd"])])
txt(99.3, 66, "blue passes\nstraight to\nL data", ha="right", fontsize=7, color=BLU)

# ---------------------------------------------------------------- cables out
for d, cols in ((J4, dict(v5=RED, gnd=BLK, data=GRN)), (J1, dict(v5=RED, gnd=BLK, data=GRN)), (J3, dict(v5=RED, gnd=BLK, data=BLU))):
    for k, c in cols.items(): path([(111.4, d[k]), (126, d[k])], c)
for k, c in (("sw", YEL), ("blu", BLU)): path([(111.4, J2[k]), (126, J2[k])], c)
txt(118.5, 104, "320 mm", ha="center", fontsize=8.5); txt(118.5, 60, "200 mm", ha="center", fontsize=8.5)
txt(118.5, 78.5, "sill bundle\n5 wires\n650 mm", ha="center", fontsize=8.5)

# ---------------------------------------------------------------- strips
def strip(y0, name, d):
    box(126, y0, 52, 10, fc="#fff8e6")
    ax.add_patch(Rectangle((129, y0 + 3.5), 47, 3, fc="#f5f5f5", ec=BLK, zorder=4))
    for i in range(15): ax.add_patch(Rectangle((130 + i * 3.1, y0 + 4), 2, 2, fc="#ffd84d", ec=BLK, lw=0.6, zorder=5))
    txt(152, y0 + 8.6, name, ha="center", weight="bold", fontsize=9)
    txt(152, y0 + 1.6, "input end at the BOTTOM of the upright → (arrows point away from it)", ha="center", fontsize=7.5)
    for k, lab in (("data", "DIN"), ("v5", "5V"), ("gnd", "GND")): txt(126.6, d[k], lab, fontsize=7, color="#444")
strip(94, "RIGHT strip — 15 LEDs, rear-right upright (bus 2)", J4)
strip(46, "LEFT strip — 15 LEDs, rear-left upright (bus 1)", J3)

# ---------------------------------------------------------------- sill block
box(126, 59.5, 52, 32, fc="#fdf3d6")
txt(152, 90.2, "LEFT SILL BLOCK — every join here is soldered + heat-shrunk", ha="center", weight="bold", fontsize=9)
path([(126, J1["v5"]), (131, J1["v5"])], RED); dot(131, J1["v5"], RED)
txt(132.3, J1["v5"], "red joins EVERY red 5V tag in the block", fontsize=7.5, color=RED, weight="bold")
path([(126, J1["gnd"]), (131, J1["gnd"])], BLK); dot(131, J1["gnd"], BLK)
txt(132.3, J1["gnd"], "black joins EVERY black GND tag in the block", fontsize=7.5, weight="bold")
def pixel(x, n):
    ax.add_patch(Rectangle((x, 70.5), 10, 6, fc="#fff", ec=BLK, zorder=4))
    txt(x + 5, 73.5, f"sill light {n}\n5 mm WS2812", ha="center", fontsize=6.8)
    tag(x + 5, 78.3, "5V", RED, fs=7); tag(x + 5, 68.4, "GND", BLK, fs=7)
    return x
p1 = pixel(136, 1); p2 = pixel(152, 2)
path([(126, J1["data"]), (132.5, J1["data"]), (132.5, 73), (p1, 73)], GRN); txt(p1 - 0.3, 74.6, "DIN", fontsize=6.3, ha="right")
path([(p1 + 10, 73), (p2, 73)], GRN); txt(p1 + 10.3, 74.6, "DOUT→DIN", fontsize=6.3)
txt(p2 + 10.3, 74.6, "DOUT", fontsize=6.3)
YB = 65.4
path([(p2 + 10, 73), (164, 73), (164, YB), (128.3, YB), (128.3, J2["blu"]), (126, J2["blu"])], BLU, hops=[(128.3, J2["sw"])] if False else [])
path([(126, J2["sw"]), (130, J2["sw"]), (130, 62.3), (170.5, 62.3), (170.5, 67.6)], YEL, hops=[(130, YB)])
# button
bx, by = 171, 72
ax.add_patch(Circle((bx, by), 4.4, fc="#ddd", ec=BLK, zorder=4)); ax.add_patch(Circle((bx, by), 2.2, fc="#3a7bd5", ec=BLK, zorder=5))
txt(bx - 0.4, 64.4, "switch 1", fontsize=6.3, ha="right")
tag(bx - 3.2, 79.0, "LED +", RED, fs=6.8); tag(bx + 3.0, 82.6, "LED − & switch 2", BLK, fs=6.5)
txt(bx, 86.2, "8 mm button", ha="center", fontsize=7)

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
