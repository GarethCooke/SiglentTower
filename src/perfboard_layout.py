# perfboard_layout.py — the lighting perfboard (D10 rev 5, 2026-10-25): XIAO ESP32-S3, SN74AHCT125N, SR3200, 2 x 330R,
# 1000 uF, USB pigtail header, three 2.54 mm locking pin headers along the bottom edge (5-pin sill, 3-pin L, 3-pin R) and a 2-pin for the USB pigtail. 50 x 40 board = 19 x 15 holes.
# Component side shown; every wire runs on the back. Output: parts/wiring/perfboard-layout.png
import os, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "parts", "wiring")
RED, BLK, GRN, BLU, YEL, GRY = "#d62728", "#222", "#2ca02c", "#1f5fd6", "#d49a00", "#888"
fig = plt.figure(figsize=(19, 10.5)); ax = fig.add_axes([0.01, 0.06, 0.52, 0.86]); tb = fig.add_axes([0.55, 0.06, 0.44, 0.86])
ax.set_xlim(-1.6, 19.6); ax.set_ylim(-2.6, 15.6); ax.set_aspect("equal"); ax.axis("off"); tb.axis("off")
fig.text(0.01, 0.955, "Lighting perfboard — component side, USB-C at the top (as it sits in the holder)", fontsize=15, weight="bold")
fig.text(0.01, 0.925, "Columns A–S left to right, rows 1–15 bottom to top. Parts sit on this side; every wire in the table runs on the back.", fontsize=10)
COLS = "ABCDEFGHIJKLMNOPQRS"
def h(c, r): return f"{COLS[c]}{r + 1}"
ax.add_patch(FancyBboxPatch((-0.9, -0.9), 19.8, 15.8, boxstyle="round,pad=0.1", fc="#e8dcc0", ec="#9a8a60", lw=1.5))
for c in range(19):
    for r in range(15): ax.add_patch(Circle((c, r), 0.17, fc="#c9b98f", ec="#8a7a50", lw=0.5, zorder=1))
for c in range(19): ax.text(c, -1.45, COLS[c], ha="center", fontsize=8, color="#555")
for r in range(15): ax.text(-1.35, r, str(r + 1), ha="center", va="center", fontsize=8, color="#555")
def pin(c, r, col="#cc0", z=6): ax.add_patch(Circle((c, r), 0.24, fc=col, ec=BLK, lw=0.8, zorder=z))
def lab(x, y, s, **k): k.setdefault("fontsize", 7.5); k.setdefault("ha", "center"); k.setdefault("va", "center"); ax.text(x, y, s, zorder=9, **k)
# XIAO: left row col B (D0..D6) rows 14..8, right row col H (5V,GND,3V3,D10,D9,D8,D7), USB-C at the top
ax.add_patch(Rectangle((0.35, 6.55), 7.3, 8.25, fc="#2b6cb0", ec=BLK, alpha=0.85, zorder=3))
ax.add_patch(Rectangle((2.9, 13.9), 2.2, 1.0, fc="#bbb", ec=BLK, zorder=4)); lab(4, 14.4, "USB-C", fontsize=6.5)
lab(4, 10.3, "XIAO\nESP32-S3", color="w", weight="bold", fontsize=10)
L = ["D0", "D1", "D2", "D3", "D4", "D5", "D6"]; Rr = ["5V", "GND", "3V3", "D10", "D9", "D8", "D7"]
for i, (a, b) in enumerate(zip(L, Rr)):
    r = 13 - i; pin(1, r); pin(7, r); lab(1.65, r, a, color="w", fontsize=6.5, ha="left"); lab(6.35, r, b, color="w", fontsize=6.5, ha="right")
# chip: notch at the top, pin 1 top-left K13, pins 1-7 down col K (rows 13..7), 8-14 up col N
ax.add_patch(Rectangle((9.5, 5.5), 4.0, 7.0, fc="#333", ec=BLK, zorder=3)); ax.add_patch(Circle((11.5, 12.5), 0.45, fc="#e8dcc0", ec=BLK, zorder=4))
lab(11.5, 9, "SN74AHCT\n125N", color="w", weight="bold", fontsize=8)
for k in range(1, 8): pin(10, 13 - k, "#bbb"); lab(10.55, 13 - k, str(k), color="w", fontsize=6.5, ha="left")
for m in range(8, 15): pin(13, m - 2, "#bbb"); lab(12.45, m - 2, str(m), color="w", fontsize=6.5, ha="right")
lab(11.5, 13.15, "notch", fontsize=6.5)
# diode SR3200: cathode I15 (stripe, by the XIAO), anode N15
ax.add_patch(Rectangle((8.8, 13.55), 3.4, 0.9, fc="#333", ec=BLK, zorder=4)); ax.add_patch(Rectangle((8.95, 13.55), 0.35, 0.9, fc="#ddd", ec=BLK, zorder=5))
ax.plot([8, 8.8], [14, 14], color=GRY, lw=2, zorder=3); ax.plot([12.2, 13], [14, 14], color=GRY, lw=2, zorder=3)
pin(8, 14, "#bbb"); pin(13, 14, "#bbb"); lab(10.6, 14.75, "SR3200 — stripe at I15", fontsize=7)
# cap: + P13, - P11
ax.add_patch(Circle((16, 11), 1.97, fc="#345", ec=BLK, zorder=3)); lab(16, 11, "1000 µF", color="w", fontsize=7)
pin(16, 12, RED); pin(16, 10, BLK); lab(17.3, 12, "+", color="w", fontsize=9, weight="bold"); lab(17.3, 10, "−", color="w", fontsize=9, weight="bold")
lab(16, 8.6, "stripe (−) at Q11", fontsize=7)
# resistors R1 D5–H5, R2 L5–P5
for (c0, c1, name) in ((3, 7, "R1 330 Ω"), (11, 15, "R2 330 Ω")):
    ax.plot([c0, c1], [4, 4], color=GRY, lw=2, zorder=3)
    ax.add_patch(Rectangle((c0 + 1.1, 3.55), c1 - c0 - 2.2, 0.9, fc="#dcb", ec=BLK, zorder=4)); pin(c0, 4, "#bbb"); pin(c1, 4, "#bbb")
    lab((c0 + c1) / 2, 4.95, name, fontsize=7)
# Wi-Fi antenna: the XIAO's flat antenna stuck to the board between the XIAO and the headers (rows 2-4, cols A-I),
# component side; its lead goes up to the u.FL socket at the XIAO's lower-left corner. The only metal near it is the
# rail behind the board, ~10 mm away; the frame is an open lattice.
ax.add_patch(Rectangle((-0.6, 1.4), 8.8, 2.2, fc="#fff", ec=BLK, lw=1.2, ls="--", zorder=5, alpha=0.9))
lab(3.8, 2.5, "Wi-Fi antenna stuck here\nlead up to the XIAO's socket, lower-left corner", fontsize=6.8)
# pin headers on row 1 (latch ramp towards the board edge)
HDR = [("5-pin S (sill)", [(1, RED, "5V"), (2, GRN, "data"), (3, BLU, "back"), (4, BLK, "GND"), (5, YEL, "sw")]),
       ("3-pin L", [(8, RED, "5V"), (9, BLK, "GND"), (10, BLU, "data")]),
       ("3-pin R", [(13, RED, "5V"), (14, BLK, "GND"), (15, GRN, "data")])]
for name, pins in HDR:
    cs = [p[0] for p in pins]
    ax.add_patch(Rectangle((min(cs) - 0.6, -0.55), max(cs) - min(cs) + 1.2, 1.1, fc="#f2f2f2", ec=BLK, zorder=4))
    for c, col, t in pins:
        pin(c, 0, col or "#ddd"); lab(c, -0.85, t, fontsize=6.3)
    lab((min(cs) + max(cs)) / 2, 0.95, name, fontsize=7.5, weight="bold")
# USB pigtail: a 2-pin locking header at P15 (5V) / Q15 (GND), crimped like the other plugs
ax.add_patch(Rectangle((14.4, 13.45), 2.2, 1.1, fc="#f2f2f2", ec=BLK, zorder=4))
pin(15, 14, RED); pin(16, 14, BLK); lab(15.5, 14.85, "2-pin PWR (USB pigtail)", fontsize=7, weight="bold"); lab(15, 13.15, "5V", fontsize=6.3); lab(16, 13.15, "GND", fontsize=6.3)

WIRES = [  # (colour, from (c,r), to (c,r), what)
    (RED, (15, 14), (13, 14), "pigtail 5V → diode anode"),
    (RED, (15, 14), (16, 12), "pigtail 5V → capacitor +"),
    (RED, (16, 12), (13, 12), "capacitor + → chip pin 14 (5V)"),
    (RED, (16, 12), (13, 0), "capacitor + → R plug 5V"),
    (RED, (13, 0), (8, 0), "R plug 5V → L plug 5V"),
    (RED, (8, 0), (1, 0), "L plug 5V → sill plug 5V"),
    (RED, (8, 14), (7, 13), "diode stripe end → XIAO 5V"),
    (BLK, (16, 14), (16, 10), "pigtail GND → capacitor −"),
    (BLK, (16, 10), (14, 0), "capacitor − → R plug GND"),
    (BLK, (14, 0), (9, 0), "R plug GND → L plug GND"),
    (BLK, (9, 0), (4, 0), "L plug GND → sill plug GND"),
    (BLK, (7, 12), (10, 12), "XIAO GND → chip pin 1"),
    (BLK, (10, 12), (10, 9), "chip pin 1 → pin 4"),
    (BLK, (10, 9), (10, 6), "chip pin 4 → pin 7"),
    (BLK, (10, 6), (9, 0), "chip pin 7 → L plug GND"),
    (BLK, (13, 7), (13, 8), "chip pin 9 → pin 10"),
    (BLK, (13, 8), (13, 10), "chip pin 10 → pin 12 (skip pin 11)"),
    (BLK, (13, 10), (13, 11), "chip pin 12 → pin 13"),
    (BLK, (13, 10), (16, 10), "chip pin 12 → capacitor −"),
    (GRN, (1, 13), (10, 11), "XIAO D0 → chip pin 2"),
    (GRN, (1, 12), (10, 8), "XIAO D1 → chip pin 5"),
    (GRN, (10, 10), (7, 4), "chip pin 3 → R1"),
    (GRN, (3, 4), (2, 0), "R1 → sill plug data"),
    (GRN, (10, 7), (11, 4), "chip pin 6 → R2"),
    (GRN, (15, 4), (15, 0), "R2 → R plug data"),
    (BLU, (3, 0), (10, 0), "sill plug 'back' → L plug data"),
    (YEL, (1, 9), (5, 0), "XIAO D4 → sill plug switch"),
]
for i, (col, a, b, _) in enumerate(WIRES, 1):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=1.8, alpha=0.8, zorder=5.5, ls=(0, (4, 2)))
# table
tb.set_xlim(0, 1); tb.set_ylim(0, 1)
tb.text(0, 0.985, "Wires on the back — solder in this order", fontsize=12, weight="bold", va="top")
tb.text(0, 0.955, "Insulated 28 AWG where a wire crosses another; a bare tinned link is fine between neighbouring holes.", fontsize=8.5, va="top")
y = 0.92
for i, (col, a, b, what) in enumerate(WIRES, 1):
    tb.add_patch(Rectangle((0.0, y - 0.011), 0.03, 0.02, fc=col, ec=BLK, lw=0.5))
    tb.text(0.045, y, f"{i:>2}", fontsize=9, va="center", family="monospace")
    tb.text(0.09, y, f"{h(*a):>4} → {h(*b):<4}", fontsize=9.5, va="center", family="monospace", weight="bold")
    tb.text(0.30, y, what, fontsize=9, va="center")
    y -= 0.03
tb.text(0, y - 0.01,
        "Parts first: XIAO pins in B8–B14 and H8–H14 (USB-C at the top edge) · chip in K7–K13 / N7–N13, notch at the top ·\n"
        "SR3200 I15 (stripe) – N15 · 1000 µF + Q13, − Q11 · R1 D5–H5 · R2 L5–P5 · headers: B1–F1 (5-pin), I1–K1 and N1–P1 (3-pin), P15–Q15 (2-pin PWR) ·\n"
        "pigtail 2-pin header P15–Q15 · XIAO on two 7-way female headers so it unplugs · antenna stuck at rows 2–4.\nBefore the XIAO goes in: 5 V on the pigtail header, meter reads 5 V at N13 and\n"
        "at each plug's 5V pin, and about 4.4 V at H14 (after the diode).",
        fontsize=8.3, va="top")
os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "perfboard-layout.png"), dpi=110)
print("ok")
