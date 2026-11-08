# build_guide_sheets.py — the three diagrams docs/BUILD-GUIDE.md needs that no part sheet shows (2026-11-08):
#   docs/build-guide/frame-flat-side.svg      one side of the frame laid flat on the bench: five rails, two uprights,
#                                             the spacers where they stand, the sled foot in the scope rail, connectors
#   docs/build-guide/drawer-quarters-order.svg the four bottom-drawer quarters and the order they go together
#   docs/build-guide/sled-order.svg           the sled parts in the order they are fitted, from the frame step onward
# Every number is HANDOVER v19 (§2 levels, §4 sled, §6 drawer) — nothing here is measured from a part.
# python src/build_guide_sheets.py
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "docs", "build-guide")); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 9, "svg.fonttype": "none"})

AL, AL_E = "#c9c9c9", "#555555"          # extrusion fill / edge
SP, SP_E = "#f2d16b", "#8a6d00"          # spacer (yellow PETG)
FOOT, FOOT_E = "#8db4e2", "#1f4e79"      # sled foot (black ABS+ drawn blue so it reads)
CON = "#d9534f"                          # hidden L-connector / cast bracket marker
GREY, DK = "#9e9e9e", "#333333"


def rect(ax, x0, y0, w, h, fc, ec=DK, lw=1.0, z=2, **kw):
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, **kw))


def label(ax, x, y, s, **kw):
    kw.setdefault("ha", "center"); kw.setdefault("va", "center"); kw.setdefault("fontsize", 8.5)
    ax.text(x, y, s, zorder=6, **kw)


# ---------------------------------------------------------------- 1. one side, flat on the bench
def frame_flat_side():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    # The side lies on the bench: this is a plan view of it, y along the frame's depth, z along the frame's height.
    # Uprights 510 long at y 0–20 and 330–350; rails 310 long between them (y 20–330); levels as HANDOVER §2.
    levels = {"base rail": (0, 20), "PSU rail": (68, 88), "AWG rail": (227.5, 247.5), "scope rail": (311, 331), "top rail": (490, 510)}
    for y0 in (0, 330):
        rect(ax, 0, y0, 510, 20, AL, AL_E)
    label(ax, 255, 10, "front upright 510", fontsize=8)
    label(ax, 255, 340, "rear upright 510", fontsize=8)
    for name, (z0, z1) in levels.items():
        rect(ax, z0, 20, z1 - z0, 310, AL, AL_E)
        label(ax, (z0 + z1) / 2, 175, name, rotation=90, fontsize=8)
    # spacers: 48 (20→68), 139.5 (88→227.5), 63.5 (247.5→311), 159 (331→490) — stood on the lower rail, the next rail sat on them
    for z0, L in ((20, 48), (88, 139.5), (247.5, 63.5), (331, 159)):
        for y0 in (60, 250):
            rect(ax, z0, y0, L, 20, SP, SP_E, z=3)
        label(ax, z0 + L / 2, 160, f"spacer\n{L:g}", fontsize=8, color=SP_E)
    # sled T-foot in the scope rail's inner slot, home = against the rear upright: y 119.5–329.5
    rect(ax, 311 + 7, 119.5, 6, 210, FOOT, FOOT_E, z=4)
    label(ax, 300, 224.5, "sled T-foot 210 in the scope rail's INNER slot\n(its home end against the rear upright) — in before the uprights close", fontsize=7.5, color=FOOT_E, ha="right")
    # connectors: hidden L on the upright's inner face at every rail but the scope rail; cast bracket under the scope rail's ends
    for z0, z1 in list(levels.values()):
        if z0 == 311:
            continue
        for y0 in (20, 330):
            ax.plot([z0 + 10], [y0], marker="s", color=CON, ms=7, zorder=5)
    for y0 in (20, 330):
        ax.plot([311 + 10], [y0], marker="^", color=CON, ms=9, zorder=5)
    label(ax, 0, -28, "■  hidden L-connector on the face that looks INTO the frame — pushed down the upright's slot before the top rail closes it\n"
                      "▲  cast bracket UNDER the scope rail at each end (x 3–17) — the scope rail takes no hidden connector: the foot owns its inner slot\n"
                      "Two spacers of each length, one near each end of the gap. Yellow = spacer, blue = sled T-foot.",
          fontsize=7.5, ha="left", va="top", color=DK, linespacing=1.5)
    ax.set_xlim(-15, 525); ax.set_ylim(-80, 370); ax.set_aspect("equal")
    ax.set_xlabel("frame z (mm) — height, lying along the bench"); ax.set_ylabel("frame y (mm) — front at 0")
    ax.set_title("One side of the frame built FLAT on the bench — left side shown from above (inner face up); the right side is its mirror.\n"
                 "Base and top rails flush with the upright ends; PSU / AWG / scope rails sit on the spacers; spacers out once the connectors are tight.", fontsize=9.5)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "frame-flat-side.svg")); plt.close(fig)


# ---------------------------------------------------------------- 2. drawer quarters, order
def drawer_quarters_order():
    fig, axs = plt.subplots(1, 4, figsize=(13, 4.6))
    quarters = {"Q1": (0, 0), "Q2": (157.5, 0), "Q3": (0, 150), "Q4": (157.5, 150)}   # drawer x (left wall 0), y (front 0)
    order = ["Q1", "Q2", "Q3", "Q4"]
    titles = ["1  Q1 down — front-left,\n    floor on the bench",
              "2  Q2 drops onto Q1 from above —\n    seam x 157.5: floor tabs interleave,\n    the wall dovetail slides DOWN",
              "3  Q3 drops on behind Q1 —\n    seam y 150",
              "4  Q4 last, onto two seams at once —\n    then CA every wall dovetail"]
    for k, ax in enumerate(axs):
        for i, q in enumerate(order):
            x0, y0 = quarters[q]
            placed = i <= k
            fc = "#bfbfbf" if placed else "none"
            ec = DK if placed else GREY
            rect(ax, x0, y0, 157.5, 150, fc, ec, lw=1.2 if placed else 0.8, ls="-" if placed else "--")
            label(ax, x0 + 78.75, y0 + 75, q, fontsize=13, color=DK if placed else GREY)
        if k >= 1:
            ax.plot([157.5, 157.5], [0, 150 if k < 3 else 300], color=CON, lw=2, zorder=5)
        if k >= 2:
            ax.plot([0, 157.5 if k < 3 else 315], [150, 150], color=CON, lw=2, zorder=5)
        # runner groove boss along each outer wall, closed at the front, open at the rear
        for xg in (0, 305):
            rect(ax, xg, 10, 10, 290, "#dbe8f5", "#1f4e79", lw=0.6, z=1)
        ax.annotate("", xy=(157.5, -12), xytext=(157.5, -45), arrowprops=dict(arrowstyle="-|>", color=DK)) if k == 0 else None
        ax.text(157.5, -50, "FRONT (facia goes here)", ha="center", va="top", fontsize=8)
        ax.set_xlim(-10, 325); ax.set_ylim(-60, 312); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(titles[k], fontsize=8.5, loc="left")
    fig.suptitle("Bottom drawer — the four quarters go together in this order (seen from above). Red = the seam just made;\n"
                 "blue = the runner groove along each outer wall, open at the REAR, so the finished drawer slides onto its runners from the front.", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(os.path.join(OUT, "drawer-quarters-order.svg")); plt.close(fig)


# ---------------------------------------------------------------- 3. sled order
def sled_order():
    fig, axs = plt.subplots(2, 3, figsize=(12.5, 8.4))
    axs = axs.ravel()
    steps = [
        "1  Already done in the frame step: a T-foot in each scope rail's\n    INNER slot, home against the rear upright (y 119.5–329.5)",
        "2  CA each beam's front half (v2) to its rear half (v1) at the\n    tab, y 165. Thread each beam's groove onto its foot's rib\n    FROM THE REAR until it stops",
        "3  Slide the front bar on FROM THE FRONT over both beams'\n    tongues; CA the tongues in their pockets and the saddles\n    to the beam tops",
        "4  Drop the two cross bars into the beam sockets (y 190–210\n    and 308–335), lips up; CA the tabs. Bond each foot to its beam",
        "5  Front rests on the scope rails (y 21–61), one M5 × 10\n    countersunk each; splice bars CA'd on the beams' outer strips\n    (y 88.5–188.5); cable channel on the left beam (y 201–334)",
        "6  TPU stop cap in the FRONT end of each inner slot (trim step).\n    Scope on: rear bumpers in the D cups, front stands in the\n    pockets. Rear box on the cross bars between the lips",
    ]
    for k, ax in enumerate(axs):
        # scope rails (plan), x 0–20 and 341–361, y 20–330
        for x0 in (0, 341):
            rect(ax, x0, 20, 20, 310, AL, AL_E, z=1)
        for y0 in (0, 330):          # front / rear uprights as context
            for x0 in (0, 341):
                rect(ax, x0, y0, 20, 20, "#a8a8a8", AL_E, z=1)
        # feet
        for x0 in (17, 338):
            rect(ax, x0, 119.5, 6, 210, FOOT, FOOT_E, z=3)
        if k >= 1:                   # beams x 20.5–60 / 301–340.5, y 12–330; split at 165
            for x0 in (20.5, 301):
                rect(ax, x0, 12, 39.5, 318, "#e0e0e0", DK, z=2)
                ax.plot([x0, x0 + 39.5], [165, 165], color=CON, lw=1.5, zorder=4)
        if k >= 2:                   # front bar x 23–338, y 0–12; saddles y 12–88
            rect(ax, 23, 0, 315, 12, "#7f7f7f", DK, z=4)
            for x0 in (20.5, 315):
                rect(ax, x0, 12, 25.5, 76, "#9a9a9a", DK, z=4)
        if k >= 3:                   # cross bars between the beams
            rect(ax, 60, 190, 241, 20, "#6f6f6f", DK, z=4)
            rect(ax, 60, 308, 241, 27, "#6f6f6f", DK, z=4)
        if k >= 4:                   # rests, splices, channel
            for x0 in (2, 341):
                rect(ax, x0, 21, 18, 40, "#4472c4", "#1f3864", z=5)
            for x0 in (20.5, 315):
                rect(ax, x0, 88.5, 25.5, 100, "#bdbdbd", DK, z=5)
            rect(ax, 20.5, 201, 26.5, 133, "#d6d6d6", DK, z=5)
        if k >= 5:                   # stop caps, box
            for x0 in (17, 338):
                rect(ax, x0, 20, 6, 8, "#2e75b6", "#1f3864", z=6)
            rect(ax, 50, 195, 291, 135, "#8c8c8c", DK, z=6, alpha=0.85)
            label(ax, 195.5, 262, "rear box", color="white", fontsize=9)
        ax.set_xlim(-10, 371); ax.set_ylim(-10, 360); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(steps[k], fontsize=8.3, loc="left")
    fig.suptitle("The sled in fitting order — plan view from above, front at the bottom (frame x across, y up). "
                 "Blue = the T-feet; red line = the beam's glued split at y 165; dark blue = front rests and stop caps.", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(OUT, "sled-order.svg")); plt.close(fig)


if __name__ == "__main__":
    frame_flat_side(); drawer_quarters_order(); sled_order()
    for f in sorted(os.listdir(OUT)):
        print(os.path.join("docs", "build-guide", f))
