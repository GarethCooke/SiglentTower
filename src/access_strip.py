# access_strip.py — the sled / box access sequence as a three-frame strip for docs/WRITE-UP.md (2026-11-08):
#   docs/access-sequence.svg — plan view from above at scope level: home · sled out 92 · door open, box out to the right
# Numbers from HANDOVER v19: frame x 0–361, y 0–350; scope bezel x 23–338 at y 3, body 135 deep; sled beams y 12–330;
# rear box x 50–341, y 195–330 (291 × 135); door y 20–250 on the right face, hinge axis x 369; travel 92;
# the bench is free to the right only along the front 250 mm of depth, and shelves sit directly above.
# python src/access_strip.py
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "docs")); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 9, "svg.fonttype": "none"})

AL, DK, GREY = "#bdbdbd", "#333333", "#8a8a8a"
SCOPE, BOX, DOOR, ZONE = "#dfe3e8", "#6f6f6f", "#4472c4", "#f6e3b4"
TRAVEL = 92


def rect(ax, x0, y0, w, h, fc, ec=DK, lw=1.0, z=2, **kw):
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, **kw))


def frame(ax, blocked=True):
    # the bench: free to the right only along the front 250; shelves above (the reason nothing lifts out)
    if blocked:
        BB = dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9)
        rect(ax, 361, 250, 340, 100, "#e6e6e6", "none", z=0, hatch="///")
        ax.text(540, 300, "blocked beyond y 250", ha="center", va="center", fontsize=7.5, color=GREY, zorder=8, bbox=BB)
        rect(ax, 361, 0, 340, 250, ZONE, "none", z=0)
        ax.text(540, 8, "bench free to the right, front 250 only", ha="center", va="bottom", fontsize=7.5, color="#7a5a00", zorder=8, bbox=BB)
    for x0 in (0, 341):                       # uprights (plan) and scope rails
        for y0 in (0, 330):
            rect(ax, x0, y0, 20, 20, "#9a9a9a", DK, z=3)
        rect(ax, x0, 20, 20, 310, AL, DK, z=2)
    rect(ax, 20, 330, 321, 20, AL, DK, z=2)  # rear cross rail
    ax.annotate("", xy=(-30, 0), xytext=(-30, 350), arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.8))
    ax.text(-38, 175, "350", rotation=90, ha="right", va="center", fontsize=8, color=GREY)
    ax.text(180, -14, "FRONT", ha="center", va="top", fontsize=8, color=GREY)


def sled(ax, dy, box=True, box_x=50, box_y=None):
    # beams and the scope on them, moved forward by dy
    for x0 in (20.5, 301):
        rect(ax, x0, 12 - dy, 39.5, 318, "#e0e0e0", DK, z=4)
    rect(ax, 23, 3 - dy, 315, 135, SCOPE, DK, z=5)
    ax.text(180.5, 70 - dy, "scope\n315 × 135", ha="center", va="center", fontsize=8.5, zorder=6)
    rect(ax, 23, 0 - dy, 315, 12, "#7f7f7f", DK, z=6)   # front bar
    if box:
        by = (195 - dy) if box_y is None else box_y
        rect(ax, box_x, by, 291, 135, BOX, DK, z=6)
        ax.text(box_x + 145.5, by + 67.5, "rear box\n291 × 135", ha="center", va="center", fontsize=8.5, color="white", zorder=7)


def door(ax, open_):
    if not open_:
        rect(ax, 361, 20, 3, 230, DOOR, "#1f3864", z=7)
        ax.text(372, 135, "door (closed)", rotation=90, ha="left", va="center", fontsize=7.5, color="#1f3864", zorder=8,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))
    else:
        # the door hangs down past 180°: in plan it is a 3 mm line at x 365–384, proud of the tile face below
        rect(ax, 374, 20, 3, 230, DOOR, "#1f3864", z=7, alpha=0.5)
        ax.text(372, 150, "door folded down", rotation=90, ha="left", va="center", fontsize=7.5, color="#1f3864", zorder=8,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))


def main():
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 5.2))
    titles = [
        "1  Home: the box sits over y 195–330, inside the blocked\n    part of the bench — nothing can come out, and the shelves\n    above rule out lifting",
        f"2  Sled forward {TRAVEL} to its stop caps: the scope comes out\n    over the bench and the box comes with it, to y {195 - TRAVEL}–{330 - TRAVEL} —\n    now inside the clear 250",
        "3  Door folded down: the box is lifted 7.5 over the right\n    splice and drawn out to the right, between the beams'\n    cross-bar lips, into the free bench",
    ]
    for k, ax in enumerate(axs):
        frame(ax)
        if k == 0:
            sled(ax, 0); door(ax, False)
        elif k == 1:
            sled(ax, TRAVEL); door(ax, False)
            ax.annotate("", xy=(180.5, -TRAVEL - 4), xytext=(180.5, -4), arrowprops=dict(arrowstyle="-|>", color=DK, lw=1.5))
            ax.text(192, -TRAVEL / 2, f"{TRAVEL}", va="center", fontsize=8.5)
        else:
            sled(ax, TRAVEL, box=True, box_x=50 + 300, box_y=195 - TRAVEL)
            door(ax, True)
            ax.annotate("", xy=(50 + 300, 170), xytext=(50, 170), arrowprops=dict(arrowstyle="-|>", color=DK, lw=1.5))
            ax.text(200, 158, "box out to the right", ha="center", va="top", fontsize=8.5)
        ax.set_xlim(-50, 710); ax.set_ylim(-120, 370); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(titles[k], fontsize=8.5, loc="left")
    fig.suptitle("The access sequence, plan view from above (frame x across, y back from the front). "
                 "Sled out → door down → box out sideways. Reverse to put it back.", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(OUT, "access-sequence.svg")); plt.close(fig)
    print(os.path.join("docs", "access-sequence.svg"))


if __name__ == "__main__":
    main()
