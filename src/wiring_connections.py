# wiring_connections.py — every connection in the lighting, on one sheet (D10 rev 5, 2026-10-25: XIAO ESP32-S3 + SiglentGlow
# firmware instead of the D1 mini + WLED; 5 V into the XIAO through an SR3200 Schottky; pins D0 / D1 / D4).
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

ax.text(1, 115.5, "Lighting — every connection (D10 rev 5.1, 2026-10-27: XIAO ESP32-S3 Plus, as built)", fontsize=15, weight="bold")
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
txt(72, 105, "PERFBOARD (50 × 70) in the enclosure on the rear base rail", ha="center", weight="bold", fontsize=10)
# USB in + cap
ax.add_patch(Rectangle((43, 33), 6, 7, fc="#f2f2f2", ec=BLK, zorder=4)); txt(46, 42, "2-pin PWR plug\n(board top edge)", ha="center", fontsize=7.5)
tag(51.5, 38, "5V", RED); tag(51.5, 35, "GND", BLK)
ax.add_patch(Circle((60, 36.5), 2.6, fc="#345", ec=BLK, zorder=4)); txt(60, 36.5, "1000\nµF", ha="center", fontsize=6.5, color="w")
txt(63.5, 38.5, "+ leg → 5V", fontsize=8); txt(63.5, 34.5, "striped leg → GND", fontsize=8)
# XIAO ESP32-S3 (pins drawn by the labels printed on the board, not in their physical order)
box(44, 49, 13, 51, fc="#2b6cb0", ec=BLK)
txt(48.5, 74, "SEEED XIAO ESP32-S3 Plus", ha="center", color="w", weight="bold", rotation=90, fontsize=9)
P = {}
for i, p in enumerate(["5V", "GND", "D1", "D4", "3V3", "D2", "D0", "D3"]):
    y = 96 - i * 6; P[p] = y
    ax.add_patch(Rectangle((57, y - 0.9), 2.4, 1.8, fc="#cc0", ec=BLK, zorder=4))
    txt(56.2, y, p, ha="right", color="w", weight="bold", fontsize=9.5)
# 5 V into the XIAO through the Schottky (stripe towards the XIAO)
path([(59.4, P["5V"]), (68, P["5V"])], RED)
ax.add_patch(plt.Polygon([(65.6, P["5V"] - 1.3), (65.6, P["5V"] + 1.3), (62.6, P["5V"])], fc=BLK, ec=BLK, zorder=6))
ax.add_patch(Rectangle((61.9, P["5V"] - 1.3), 0.6, 2.6, fc=BLK, ec=BLK, zorder=6))
tag(70.5, P["5V"], "5V", RED)
txt(63, P["5V"] + 3.2, "SR3200 Schottky\nstripe → XIAO", ha="center", fontsize=6.8)
tag(62.4, P["GND"], "GND", BLK)
for p in ("3V3", "D2", "D3"): txt(60.3, P[p], "empty", fontsize=7.5, color="#888")
txt(68, 46.5, "D5–D10 empty · flat antenna on the u.FL socket (lower-left corner), stuck to the board below the XIAO · hole-by-hole layout: perfboard-layout.png", ha="center", fontsize=7, color="#555")
# chip
CX0, CX1, CY0, CY1 = 71, 84, 63, 85
ax.add_patch(Rectangle((CX0, CY0), CX1 - CX0, CY1 - CY0, fc="#333", ec=BLK, zorder=4))
txt((CX0 + CX1) / 2, 74, "SN74AHCT\n125N", ha="center", color="w", fontsize=8.5, weight="bold")
IN5, IN2 = 80, 68
for y, a, b in ((IN5, "5", "6"), (IN2, "2", "3")):
    txt(CX0 + 0.5, y, a, color="w", fontsize=8); txt(CX1 - 0.5, y, b, color="w", fontsize=8, ha="right")
# connectors: 2.54 mm locking pin headers (KF2510 type) soldered on the board, crimped housings on the cables
J4 = dict(data=101, v5=98, gnd=95); J1 = dict(red=85, grn=82, blu=79, blk=76, sw=73); J2 = dict(sw=73); J3 = dict(data=57, v5=54, gnd=51)
def conn(ys, name):
    y0, y1 = min(ys) - 1.6, max(ys) + 1.6
    ax.add_patch(Rectangle((103, y0), 4, y1 - y0, fc="#bbb", ec=BLK, zorder=5))
    ax.add_patch(Rectangle((107.4, y0), 4, y1 - y0, fc="#777", ec=BLK, zorder=5))
    txt(109.4, y1 + 1.4, name, ha="center", fontsize=8, weight="bold")
conn(J4.values(), "R  3-pin"); conn(J1.values(), "S  5-pin (sill)"); conn(J3.values(), "L  3-pin")
txt(105, 27.5, "grey = pin header soldered on the board · dark = crimped housing on the cable · L and R are identical plugs: label them · the pigtail lands on its own 2-pin at the board's top edge",
    ha="center", fontsize=8, style="italic")
# board wiring
txt((CX0 + CX1) / 2, 60.3, "chip pin 14 → 5V\npins 1 4 7 9 10 12 13 → GND\npins 8, 11 empty", ha="center", fontsize=7.5)
path([(59.4, P["D1"]), (65, P["D1"]), (65, IN5), (CX0, IN5)], GRN)
path([(59.4, P["D0"]), (67, P["D0"]), (67, IN2), (CX0, IN2)], GRN)
path([(59.4, P["D4"]), (68.5, P["D4"]), (68.5, 61), (99, 61), (99, J1["sw"]), (103, J1["sw"])], YEL, hops=[(68.5, IN2)])
for yout, ydst, xv in ((IN5, J4["data"], 86.0), (IN2, J1["grn"], 88.5)):   # separate risers: pins 6 and 3 are NOT joined
    path([(CX1, yout), (xv, yout), (xv, ydst), (90, ydst)], GRN)
    ax.add_patch(Rectangle((90, ydst - 1), 6.5, 2, fc="#dcb", ec=BLK, zorder=5)); txt(93.25, ydst + 2, "330 Ω", ha="center", fontsize=7.5)
    path([(96.5, ydst), (103, ydst)], GRN)
for d in (J4, J3):
    path([(100.5, d["v5"]), (103, d["v5"])], RED); tag(98, d["v5"], "5V", RED, fs=7.5)
    path([(100.5, d["gnd"]), (103, d["gnd"])], BLK); tag(98, d["gnd"], "GND", BLK, fs=7.5)
path([(100.5, J1["red"]), (103, J1["red"])], RED); tag(98, J1["red"], "5V", RED, fs=7.5)
path([(100.5, J1["blk"]), (103, J1["blk"])], BLK); tag(97.6, J1["blk"], "GND", BLK, fs=7.5)
path([(103, J1["blu"]), (101.8, J1["blu"]), (101.8, J3["data"]), (103, J3["data"])], BLU, hops=[(101.8, J1["blk"])])
txt(99.8, 62, "blue passes\nstraight to\nL data", ha="right", fontsize=7, color=BLU)

# ---------------------------------------------------------------- cables out
for y, c in ((J4["data"], GRN), (J4["v5"], RED), (J4["gnd"], BLK)): path([(111.4, y), (126, y)], c)
txt(118.5, 104, "320 mm", ha="center", fontsize=8.5)
for y, c in ((J3["data"], BLU), (J3["v5"], RED), (J3["gnd"], BLK)): path([(111.4, y), (126, y)], c)
txt(118.5, 60, "200 mm", ha="center", fontsize=8.5)
for y, c in ((J1["sw"], YEL), (J1["red"], RED), (J1["grn"], GRN), (J1["blu"], BLU), (J1["blk"], BLK)): path([(111.4, y), (126, y)], c)
txt(118.5, 90, "sill bundle\n5 wires, 650 mm", ha="center", fontsize=8.5)

# ---------------------------------------------------------------- strips
def strip(y0, name, ydata, yv5, ygnd):
    box(126, y0, 52, 10, fc="#fff8e6")
    ax.add_patch(Rectangle((129, y0 + 3.5), 47, 3, fc="#f5f5f5", ec=BLK, zorder=4))
    for i in range(15): ax.add_patch(Rectangle((130 + i * 3.1, y0 + 4), 2, 2, fc="#ffd84d", ec=BLK, lw=0.6, zorder=5))
    txt(152, y0 + 8.6, name, ha="center", weight="bold", fontsize=9)
    txt(152, y0 + 1.6, "input end at the BOTTOM of the upright → (arrows point away from it) · 14 if its first LED was cut off: count in config.h", ha="center", fontsize=7)
    for y, lab in ((ydata, "DIN"), (yv5, "5V"), (ygnd, "GND")): txt(126.6, y, lab, fontsize=7, color="#444")
strip(94, "RIGHT strip — 15 LEDs, rear-right upright (bus 2)", J4["data"], J4["v5"], J4["gnd"])
strip(47, "LEFT strip — 15 LEDs, rear-left upright (bus 1)", J3["data"], J3["v5"], J3["gnd"])

# ---------------------------------------------------------------- sill block
box(126, 60.5, 52, 30, fc="#fdf3d6")
txt(152, 89, "LEFT SILL BLOCK — every join here is soldered + heat-shrunk", ha="center", weight="bold", fontsize=9)
RR, RB = 80, 63.5
path([(126, J1["red"]), (129.5, J1["red"]), (129.5, RR), (176, RR)], RED); dot(129.5, RR, RED)
path([(126, J1["blk"]), (128.5, J1["blk"]), (128.5, RB), (176, RB)], BLK, hops=[]); dot(128.5, RB, BLK)
def pixel(x, n):
    ax.add_patch(Rectangle((x, 70.5), 10, 6, fc="#fff", ec=BLK, zorder=4))
    txt(x + 5, 73.5, f"sill light {n}\n5 mm WS2812", ha="center", fontsize=6.8)
    path([(x + 5, 76.5), (x + 5, RR)], RED); dot(x + 5, RR, RED); txt(x + 5.5, 78.2, "5V", fontsize=6.5)
    path([(x + 5, 70.5), (x + 5, RB)], BLK, hops=[(x + 5, 66)]); dot(x + 5, RB, BLK); txt(x + 5.5, 68.6, "GND", fontsize=6.5)
    return x
p1 = pixel(134, 1); p2 = pixel(150, 2)
path([(126, J1["grn"]), (131.5, J1["grn"]), (131.5, 73), (p1, 73)], GRN, hops=[(131.5, RR)]); txt(p1 - 0.3, 74.6, "DIN", fontsize=6.3, ha="right")
path([(p1 + 10, 73), (p2, 73)], GRN); txt(p1 + 10.3, 74.6, "DOUT→DIN", fontsize=6.3)
YB = 66
path([(p2 + 10, 73), (162, 73), (162, YB), (127.5, YB), (127.5, J1["blu"]), (126, J1["blu"])], BLU,
     hops=[(128.5, YB), (127.5, J1["blk"]), (127.5, 73)])
txt(p2 + 10.3, 74.6, "DOUT", fontsize=6.3)
bx0 = 165
ax.add_patch(Circle((bx0 + 5.5, 72), 4.6, fc="#ddd", ec=BLK, zorder=4)); ax.add_patch(Circle((bx0 + 5.5, 72), 2.3, fc="#3a7bd5", ec=BLK, zorder=5))
txt(bx0 + 5.5, 84.6, "8 mm button", ha="center", fontsize=7)
path([(126, J1["sw"]), (130.5, J1["sw"]), (130.5, 61.5), (bx0 + 4, 61.5), (bx0 + 4, 76.4)], YEL,
     hops=[(130.5, YB), (130.5, RB), (bx0 + 4, RB)])
txt(bx0 + 4.6, 66.3, "switch 1", fontsize=6.3)
path([(bx0 + 1.5, 74), (bx0 + 1.5, RR)], RED); dot(bx0 + 1.5, RR, RED); txt(bx0 - 2.6, 78.2, "LED +", fontsize=6.5)
path([(bx0 + 8, 69), (bx0 + 8, RB)], BLK); dot(bx0 + 8, RB, BLK); txt(bx0 + 8.4, 61.8, "LED − & switch 2 (linked)", fontsize=6.3, ha="right")

# ---------------------------------------------------------------- firmware
box(2, 4, 176, 18, fc="#f6f6f6")
txt(4, 20.5, "Firmware: SiglentGlow (IguanaPlatform, like MorayGlow) — brief: SiglentGlow-BRIEF.md", weight="bold", fontsize=10)
ax.text(4, 17.8,
        "D0 (GPIO1) → bus 1: 17 LEDs = 2 sill lights (0–1) + left strip (2–16)      D1 (GPIO2) → bus 2: 15 LEDs = right strip\n"
        "D4 (GPIO5) ← button: short press = on/off · hold 5 s = factory reset (sill lights count down in red)      current limit 1500 mA\n"
        "Set-up: join Wi-Fi 'SiglentGlow-XXXXXX' (password siglentglow) → pick your network → http://siglentglow.local → MQTT on /settings.html\n"
        "The XIAO's USB-C is for the first flash at the desk; after that, updates go over Wi-Fi.  The LEDs take 5 V straight from the pigtail, never through the XIAO.\n"
        "Firmware: C:\\Development\\Projects\\SiglentGlow (built 2026-10-25).  Plug or unplug anything only with the supply OFF — data reaching an unpowered strip kills its first LED.",
        fontsize=8.8, va="top", family="monospace", zorder=6)

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "wiring-4-connections.png"), dpi=110, bbox_inches="tight")
print("ok")
