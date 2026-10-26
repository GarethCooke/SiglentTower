# enclosure_sketch.py — confirmation sketch for the lighting board enclosure (Stage 8, 2026-10-26).
# The board grew from 50 x 40 to 50 x 70 and the holder (board-holder-v1, 44 tall) no longer covers it.
# Panel 1: the board's component side with the four plugs where Gareth described them. Panel 2: a side
# section through the holder on the rail showing the extra height the enclosure needs. Nothing here is
# modelled yet — it exists to be confirmed or corrected. Output: parts/wiring/board-enclosure-sketch.png
import os, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "parts", "wiring")

fig = plt.figure(figsize=(16, 9.5))
fig.text(0.02, 0.965, "Lighting board enclosure — sketch to confirm (nothing modelled yet)", fontsize=15, weight="bold")
fig.text(0.02, 0.937, "v2 — plugs mirrored and placed by hole count as you described; '?' = still to confirm. Board 50 wide x 70 long, 1.6 thick, as it stands in the holder.", fontsize=10)

# ---------------------------------------------------------------- panel 1: board face
ax = fig.add_axes([0.03, 0.05, 0.40, 0.86]); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-16, 66); ax.set_ylim(-18, 84)
ax.text(25, 80, "1. Board, component side (the side the plugs are on)", ha="center", fontsize=11, weight="bold")
ax.add_patch(Rectangle((0, 0), 50, 70, fc="#e8dcc0", ec="#333", lw=1.5))
# hole grid: 18 holes across at 2.54 (margin 3.41 each side), 27 rows; hole n from the RIGHT side = HX(n)
PITCH, NCOL = 2.54, 18
MARGIN = (50 - (NCOL - 1) * PITCH) / 2
def HX(n_from_right): return 50 - MARGIN - (n_from_right - 1) * PITCH
for c in range(NCOL):
    for r in range(27):
        ax.plot(MARGIN + c * PITCH, 1.9 + r * PITCH, ".", color="#b8a878", ms=2)
RED, BLU = "#c0392b", "#1f5fd6"
def plug(n_first, n_last, y0, name, h=5.8):
    """n_first/n_last = hole numbers counted from the RIGHT side; body = pins +1.27 +1.2 each end"""
    x1, x0 = HX(n_first) + 1.27 + 1.2, HX(n_last) - 1.27 - 1.2
    ax.add_patch(Rectangle((x0, y0), x1 - x0, h, fc="#f4f4f4", ec="#111", lw=1.2, zorder=4))
    for n in range(n_first, n_last + 1): ax.plot(HX(n), y0 + 1.6, "o", color="#333", ms=3.5, zorder=6)
    ax.text((x0 + x1) / 2, y0 + 3.7, name, ha="center", va="center", fontsize=8, weight="bold", zorder=5)
    return x0, x1
P2 = plug(2, 3, 63, "2-pin")        # top end, holes 2-3 from the right (row from the top: ?)
A = plug(2, 4, 1.2, "3-pin")        # bottom end, holes 2-4 from the right
B = plug(7, 9, 1.2, "3-pin")        # two empty holes (5, 6), then holes 7-9
F = plug(13, 17, 1.2, "5-pin")      # three empty holes (10-12), then holes 13-17 = holes 2-6 from the LEFT
def dim(x0, x1, y, s, above=True, col=RED):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=col, lw=1))
    ax.text((x0 + x1) / 2, y + (1.2 if above else -2.6), s, ha="center", fontsize=8, color=col)
def vdim(x, y0, y1, s, col=RED, left=False):
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=col, lw=1))
    ax.text(x + (-1.2 if left else 1.2), (y0 + y1) / 2, s, va="center", ha="right" if left else "left", fontsize=8, color=col, rotation=90)
dim(HX(5), HX(6), -4, "2 empty", above=False); dim(HX(10), HX(12), -4, "3 empty", above=False)
ax.text(HX(1), -3, "hole 1\nempty", ha="center", va="top", fontsize=7, color=RED); ax.text(HX(18), -3, "hole 1\nempty", ha="center", va="top", fontsize=7, color=RED)
dim(0, 50, 77, "50", col="#333")
vdim(-6, 0, 70, "70", col="#333", left=True)
vdim(56, 63, 70, "? rows from this end", left=False)
ax.text(25, -11, "Pin centres from the RIGHT edge: hole 2 = 6.0, hole 7 = 18.6, hole 13 = 33.9\n(18 holes at 2.54, 3.4 margin each side) — close enough?  ?", ha="center", va="top", fontsize=8.5, color=RED)
ax.text(-14, 35, "end A\n(top in the holder,\nUSB-C end — confirm)", ha="center", va="center", fontsize=8, color="#333", rotation=90)
ax.text(-14, 68, "2-pin at THIS end", fontsize=8, color=RED, rotation=90, ha="center", va="center")
ax.text(-14, 5, "three plugs\nat THIS end", fontsize=8, color=RED, rotation=90, ha="center", va="center")
ax.text(62, 35, "left / right as you see it\nlooking down on the board,\ncomponents up (mirrored from v1 of this sketch)", fontsize=8, color=RED, rotation=90, ha="center", va="center")
ax.text(25, 40, "XIAO ESP32-S3, chip,\ndiode, cap, resistors\n(not drawn — where they sit\ndoesn't change the box)", ha="center", va="center", fontsize=8, color="#777")

# ---------------------------------------------------------------- panel 2: side section
bx = fig.add_axes([0.47, 0.05, 0.51, 0.86]); bx.set_aspect("equal"); bx.axis("off")
bx.set_xlim(318, 410); bx.set_ylim(-16, 100)
bx.text(364, 96, "2. Side section (frame y right, z up) — rail, plate, board, plugs", ha="center", fontsize=11, weight="bold")
bx.add_patch(Rectangle((330, 0), 20, 20, fc="#999", ec="#333", lw=1)); bx.text(340, 10, "rear base\nrail", ha="center", va="center", fontsize=7.5, color="w")
# slot mouth on the rear face
bx.add_patch(Rectangle((344, 7), 6, 6, fc="#ddd", ec="#333", lw=0.6)); bx.text(347, 10, "slot", ha="center", va="center", fontsize=6)
# existing holder: plate y 350-355 z 0-44, walls to 365 z 0-44 (shown as the section through a wall)
bx.add_patch(Rectangle((350, 0), 5, 44, fc="#f2b84a", ec="#333", lw=1.2)); bx.text(352.5, 22, "plate 5", rotation=90, ha="center", va="center", fontsize=7)
bx.add_patch(Rectangle((355, 0), 10, 44, fc="#f2b84a", ec="#333", lw=1.2, alpha=0.55)); bx.text(362.5, 30, "wall\n(to 365)", rotation=90, ha="center", va="center", fontsize=7)
bx.add_patch(Rectangle((355, 0), 5.3, 3, fc="#f2b84a", ec="#333", lw=1.2))
bx.text(368, 44, "holder today: 44 tall", fontsize=8.5, va="center")
# board y 358.5-360.1, z 3-73
bx.add_patch(Rectangle((358.5, 3), 1.6, 70, fc="#2b6cb0", ec="#111", lw=1, zorder=5))
bx.text(361.5, 60, "board 70 tall\n(z 3-73)", fontsize=8, color="#2b6cb0", va="center")
# plugs standing off the board at the bottom end (straight-out type, ~12 with the housing) and the 2-pin at the top
for z0, h in ((3 + 1.2, 5.8), (3 + 63, 5.8)):
    bx.add_patch(Rectangle((360.1, z0), 12, h, fc="#f4f4f4", ec="#111", lw=1, zorder=6))
    bx.plot([372.1, 384], [z0 + h / 2, z0 + h / 2], color="#444", lw=2.2, zorder=6)
bx.text(378, 15, "plug + wire straight\noff the board face\n= ~12 deep  ?  (or a\nright-angle header, wires\nalong the board?)", fontsize=8, color=RED, va="center")
bx.text(376, 73, "2-pin PWR\n(USB lead)", fontsize=8, color="#333", va="center")
# proposed enclosure: walls to 83, a cover from y 355 out to ~386, vented
bx.add_patch(Rectangle((350, 44), 5, 39, fc="none", ec=RED, lw=1.5, ls="--")); bx.add_patch(Rectangle((355, 44), 10, 39, fc="none", ec=RED, lw=1.5, ls="--"))
bx.annotate("", (347, 73), (347, 83), arrowprops=dict(arrowstyle="<->", color=RED, lw=1)); bx.text(346, 78, "10", ha="right", va="center", fontsize=8, color=RED)
bx.plot([358.5, 346], [73, 73], color=RED, lw=0.6, ls=":"); bx.plot([355, 346], [83, 83], color=RED, lw=0.6, ls=":")
bx.text(332, 83, "walls up to z 83\n(board top + 10)  ?", fontsize=8.5, color=RED, va="center", ha="center")
cover = Polygon([(365, -0.01), (365, 83), (388, 83), (388, 0)], closed=False, fc="none", ec=RED, lw=1.8)
bx.add_patch(cover)
for z in range(20, 80, 8):   # vent slots drawn on the rear face
    bx.plot([388, 388], [z, z + 4], color="w", lw=3, zorder=7); bx.plot([388, 388], [z, z + 4], color=RED, lw=1, ls=":", zorder=8)
bx.text(389.5, 50, "cover: rear wall + top,\nvent slots, snaps or screws\nonto the holder — depth set\nby the plugs (~388 drawn)", fontsize=8.5, color=RED, va="center")
bx.annotate("", (354, -4), (365, -4), arrowprops=dict(arrowstyle="<->", color="#333", lw=1)); bx.text(359.5, -7.5, "holder 15 deep today", ha="center", fontsize=7.5)
bx.text(364, -13.5, "Wires: today they left through two holes in the plate into the rail slot, soldered on the board's back. With plugs on the front they "
        "would exit\nthe box at its bottom corners and enter the slot beside the holder instead — unless you want the holes kept.  ?",
        ha="center", fontsize=8.5, color=RED)
bx.plot([318, 410], [0, 0], color="#333", lw=0.8); bx.text(320, 1, "bench / frame base z 0", fontsize=7, color="#333")

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "board-enclosure-sketch.png"), dpi=110)
print("ok", os.path.join(OUT, "board-enclosure-sketch.png"))
