# tpu_where.py — placement sheets for the TPU parts that are not obvious: one sheet per item, three views each.
#   parts/tpu/tpu-where-1-stop-caps.png         sled stop caps ×2: front end of each scope rail's INNER slot
#   parts/tpu/tpu-where-2-cover-left-psu.png    slot cover run A: left PSU rail, INNER-face slot
#   parts/tpu/tpu-where-3-cover-rear-base.png   slot cover run B: rear base cross rail, REAR slot (wiring v1 2026-10-16: the board holder
#                                               sits on that face, so the right strip's feed runs in the rear slot, not the top — two pieces)
#   parts/tpu/tpu-where-4-test-pieces.png       the spigot sweep and the cover sweep: where to try them, then bin
# Frame coordinates throughout: x from the outside of the left upright, y from the front plane, z from the bench.
import os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Polygon as P, Circle as C, FancyArrowPatch as A
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "parts", "tpu"))
BLUE, DBLUE, AL, ALD, CAB = "#2d6cdf", "#1a4aa8", "#c8c8c8", "#9a9a9a", "#e8b04b"

def rail_section(ax, cx, cy, slots=("+u", "-u", "+v", "-v"), size=20.0, fc=AL):
    """A 2020 section centred at (cx, cy) in the axes' (u, v) plane with slot mouths on the named sides."""
    ax.add_patch(R((cx - size / 2, cy - size / 2), size, size, fc=fc, ec="k", zorder=2))
    ax.add_patch(C((cx, cy), 2.1, fc="white", ec="k", zorder=3))
    for s in slots:
        # mouth 5.9 wide, lips 1.75, cavity 10.6 wide from 1.75 to 4.45 deep, floor 6.5 wide at 6.15
        if s in ("+u", "-u"):
            d = 1 if s == "+u" else -1; x0 = cx + d * size / 2
            pts = [(x0, cy - 2.95), (x0 - d * 1.75, cy - 2.95), (x0 - d * 1.75, cy - 5.3), (x0 - d * 4.45, cy - 5.3), (x0 - d * 6.15, cy - 3.25),
                   (x0 - d * 6.15, cy + 3.25), (x0 - d * 4.45, cy + 5.3), (x0 - d * 1.75, cy + 5.3), (x0 - d * 1.75, cy + 2.95), (x0, cy + 2.95)]
        else:
            d = 1 if s == "+v" else -1; y0 = cy + d * size / 2
            pts = [(cx - 2.95, y0), (cx - 2.95, y0 - d * 1.75), (cx - 5.3, y0 - d * 1.75), (cx - 5.3, y0 - d * 4.45), (cx - 3.25, y0 - d * 6.15),
                   (cx + 3.25, y0 - d * 6.15), (cx + 5.3, y0 - d * 4.45), (cx + 5.3, y0 - d * 1.75), (cx + 2.95, y0 - d * 1.75), (cx + 2.95, y0)]
        ax.add_patch(P(pts, fc="white", ec="k", zorder=3))

def cover_in_slot(ax, cx, cy, side, size=20.0, label=None):
    """The cover/cap profile sitting in the slot on `side` of a section centred at (cx, cy): head flush with the face."""
    if side in ("+u", "-u"):
        d = 1 if side == "+u" else -1; x0 = cx + d * size / 2
        pts = [(x0, cy - 3.0), (x0 - d * 1.75, cy - 3.0), (x0 - d * 1.75, cy - 3.7), (x0 - d * 2.5, cy - 2.95), (x0 - d * 2.5, cy + 2.95),
               (x0 - d * 1.75, cy + 3.7), (x0 - d * 1.75, cy + 3.0), (x0, cy + 3.0)]
    else:
        d = 1 if side == "+v" else -1; y0 = cy + d * size / 2
        pts = [(cx - 3.0, y0), (cx - 3.0, y0 - d * 1.75), (cx - 3.7, y0 - d * 1.75), (cx - 2.95, y0 - d * 2.5), (cx + 2.95, y0 - d * 2.5),
               (cx + 3.7, y0 - d * 1.75), (cx + 3.0, y0 - d * 1.75), (cx + 3.0, y0)]
    ax.add_patch(P(pts, fc=BLUE, ec="k", zorder=4, label=label))

def finish(ax, title, xl, yl, xlim, ylim, ncol=2):
    ax.set_title(title, fontsize=10); ax.set_aspect("equal"); ax.set_xlabel(xl); ax.set_ylabel(yl)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), fontsize=7.5, ncol=ncol)

# ---------------------------------------------------------------- 1. stop caps
def sheet_stop_caps():
    fig = plt.figure(figsize=(17, 11)); gs = fig.add_gridspec(2, 2)
    a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[1, :])
    # a: section across the left scope rail at y 24, looking from the front
    rail_section(a, 10, 321, slots=("+u", "-u", "+v", "-v"))
    a.add_patch(R((0, 0), 20, 311, fc="#eee", ec="none"))
    cover_in_slot(a, 10, 321, "+u", label="stop cap: head flush with the rail's inner face, flare behind the lips")
    a.add_patch(R((20.5, 337), 39.5, 9, fc="#444", ec="k", label="sled beam (above)"))
    a.add_patch(R((23, 300), 40, 36, fc="#bcd", ec="k", alpha=0.6, label="AWG front frame (below)"))
    a.annotate("pushed in from THIS side\n(the inside of the frame)", (20, 321), (34, 318), arrowprops=dict(arrowstyle="->"), fontsize=9)
    a.annotate("rail's inner face x 20", (20, 311), (26, 304), fontsize=8)
    finish(a, "1. Looking from the front — section through the LEFT scope rail at y 24\nthe cap sits in the slot on the rail's INNER face (the one facing into the frame)", "frame x (mm)", "frame z (mm)", (-5, 65), (298, 352))
    # b: plan at the front-left corner
    b.add_patch(R((0, 0), 20, 20, fc=ALD, ec="k", label="front-left upright"))
    b.add_patch(R((0, 20), 20, 120, fc=AL, ec="k", label="left scope rail (y 20 →)"))
    b.add_patch(R((14.15, 119.5), 13, 30, fc="#8a6", ec="k", alpha=0.7, label="sled foot at home (y 119.5 →), in the inner slot"))
    b.add_patch(R((14.15, 28), 13, 20, fc="none", ec="#8a6", ls="--", label="foot at full pull: its front end lands on the cap"))
    b.add_patch(R((17.5, 20), 2.5, 8, fc=BLUE, ec="k", label="stop cap y 20–28, hard against the upright"))
    b.add_patch(R((20.5, 12), 39.5, 130, fc="#444", ec="k", alpha=0.3, label="beam (above the rail)"))
    b.annotate("cap", (18.8, 24), (34, 8), arrowprops=dict(arrowstyle="->"), fontsize=10)
    finish(b, "2. Plan view, front-left corner — the cap is at the FRONT END of the inner slot\n(the slot the sled foot runs in), right behind the upright", "frame x (mm)", "frame y (mm)", (-5, 65), (-5, 145))
    # c: side elevation looking outward from inside the frame at the left scope rail
    c.add_patch(R((0, 290), 20, 70, fc=ALD, ec="k", label="front-left upright"))
    c.add_patch(R((330, 290), 20, 70, fc=ALD, ec="k", label="rear-left upright"))
    c.add_patch(R((20, 311), 310, 20, fc=AL, ec="k", label="left scope rail, y 20–330"))
    c.add_patch(R((20, 318.05), 310, 5.9, fc="white", ec="k", label="inner-face slot (mouth), centre z 321"))
    c.add_patch(R((119.5, 316), 210, 25, fc="#8a6", ec="k", alpha=0.6, label="sled foot at home, y 119.5–329.5"))
    c.add_patch(R((28, 316), 100, 25, fc="none", ec="#8a6", ls="--", label="foot's front part at full pull (100 travel → 92 with the cap)"))
    c.add_patch(R((20, 317.3), 8, 7.4, fc=BLUE, ec="k", label="STOP CAP y 20–28 — press into the slot mouth with a thumb"))
    c.add_patch(R((12, 337), 318, 9, fc="#444", ec="k", alpha=0.3, label="beam"))
    c.annotate("cap, 8 mm long", (24, 324.7), (60, 352), arrowprops=dict(arrowstyle="->"), fontsize=10)
    c.text(175, 300, "Same again on the RIGHT scope rail (its inner face is x 341, facing left into the frame). Two caps in all — none at the rear.", ha="center", fontsize=9, style="italic")
    finish(c, "3. Looking outward from inside the frame at the LEFT scope rail — the cap at the front end of the slot", "frame y (mm)", "frame z (mm)", (-10, 360), (288, 362), ncol=4)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "tpu-where-1-stop-caps.png"), dpi=100); plt.close(fig)

# ---------------------------------------------------------------- 2. cover run A: left PSU rail, inner-face slot
def sheet_cover_left():
    fig = plt.figure(figsize=(17, 12)); gs = fig.add_gridspec(2, 2)
    a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[1, :])
    # a: section across the left PSU rail at y 150, looking from the front
    rail_section(a, 10, 78)
    a.add_patch(R((0, 0), 20, 68, fc="#eee", ec="none"))
    cover_in_slot(a, 10, 78, "+u", label="slot cover: head flush with the rail's inner face")
    a.add_patch(C((16.5, 78), 1.3, fc=CAB, ec="k", zorder=3, label="wires under it, in the slot (Ø ≤ 3.5 total)"))
    a.add_patch(R((22.25, 93.5), 40, 30, fc="#ddd", ec="k", alpha=0.7, label="PSU body (above, from z ~93)"))
    a.annotate("pushed in from THIS side", (20, 78), (32, 70), arrowprops=dict(arrowstyle="->"), fontsize=9)
    finish(a, "1. Looking from the front — section through the LEFT PSU rail (z 68–88) at y 150\ncover in the slot on the rail's INNER face, wires underneath", "frame x (mm)", "frame z (mm)", (-5, 65), (55, 125))
    # b: plan view of the left side
    b.add_patch(R((0, 0), 20, 20, fc=ALD, ec="k", label="front-left upright")); b.add_patch(R((0, 330), 20, 20, fc=ALD, ec="k", label="rear-left upright"))
    b.add_patch(R((0, 20), 20, 310, fc=AL, ec="k", label="left PSU rail"))
    b.add_patch(R((20.3, 3), 69.7, 16.5, fc="#777", ec="k", label="sill end block (button + pixel), x 20–90, y 3–19.5"))
    for y0 in (31, 233.5): b.add_patch(R((-3, y0), 26, 40, fc="#555", ec="k", alpha=0.5, label="PSU cradle saddles on the rail top" if y0 == 31 else None))
    for y0, y1 in ((20, 40), (310, 330)): b.add_patch(R((14, y0), 6, y1 - y0, fc="#d33", ec="k", alpha=0.6, label="hidden L-connector inside the slot (rail ends)" if y0 == 20 else None))
    b.add_patch(R((17.5, 45), 2.5, 260, fc=BLUE, ec="k", label="COVER A: y 45–305 (260 long) on the inner face"))
    b.add_patch(P([(25, 19.5), (25, 42), (19, 42), (19, 308), (25, 308), (25, 332), (19, 332)], closed=False, fc="none", ec=CAB, lw=2.5, label="wires: from the block, over the connector, along the slot, over the rear connector, into the rear-left upright's inner slot"))
    b.annotate("wires hop OVER the connector\non the rail face (no cover there)", (19, 30), (60, 60), arrowprops=dict(arrowstyle="->"), fontsize=9)
    b.annotate("…and again here", (19, 320), (60, 300), arrowprops=dict(arrowstyle="->"), fontsize=9)
    finish(b, "2. Plan view, left side — the cover runs along the rail's inner face\nbetween the two hidden L-connectors that live in the slot's ends", "frame x (mm)", "frame y (mm)", (-10, 120), (-5, 360))
    # c: elevation looking outward from inside the frame at the left side
    c.add_patch(R((0, 0), 20, 130, fc=ALD, ec="k", label="front-left upright")); c.add_patch(R((330, 0), 20, 130, fc=ALD, ec="k", label="rear-left upright"))
    c.add_patch(R((20, 0), 310, 20, fc=AL, ec="k", label="base rail")); c.add_patch(R((20, 68), 310, 20, fc=AL, ec="k", label="left PSU rail z 68–88"))
    c.add_patch(R((20, 75.05), 310, 5.9, fc="white", ec="k", label="inner-face slot mouth, centre z 78"))
    for y0, y1 in ((20, 40), (310, 330)): c.add_patch(R((y0, 75.05), y1 - y0, 5.9, fc="#d33", ec="k", alpha=0.6, label="hidden L-connector in the slot" if y0 == 20 else None))
    for y0 in (31, 233.5): c.add_patch(R((y0, 82), 40, 14, fc="#555", ec="k", alpha=0.5, label="PSU cradle saddle (its lip hangs to z 82 — above the slot)" if y0 == 31 else None))
    c.add_patch(R((45, 75), 260, 6, fc=BLUE, ec="k", label="COVER A y 45–305, flush with the rail face"))
    c.add_patch(R((3, 87), 16.5, 12, fc="#777", ec="k", label="sill end block (z 87–99), wires leave its bottom-rear corner"))
    c.add_patch(R((330, 20), 20, 110, fc="none", ec="k"))
    c.add_patch(R((336, 20), 8, 110, fc="#8bd", ec="k", alpha=0.6, label="LED strip stuck on the rear-left upright's inner face (z 20–490), over its slot"))
    c.add_patch(P([(19, 87), (19, 78), (20, 78), (20, 84), (42, 84), (42, 78), (308, 78), (308, 84), (330, 84), (335, 78), (340, 78), (340, 30)], closed=False, fc="none", ec=CAB, lw=2.5, label="wire run"))
    c.text(175, 110, "Cut the cover with scissors: one 240 strip + a 20 off-cut, or trim to fit. Stop 25 mm short of each rail end — the connectors are there.", ha="center", fontsize=9, style="italic")
    finish(c, "3. Looking outward from inside the frame at the left side — the cover sits in the PSU rail's inner slot with the wires beneath it", "frame y (mm)", "frame z (mm)", (-10, 360), (-5, 130), ncol=4)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "tpu-where-2-cover-left-psu.png"), dpi=100); plt.close(fig)

# ---------------------------------------------------------------- 3. cover run B: rear base cross rail, REAR slot (v2 2026-10-16)
def sheet_cover_rear():
    fig = plt.figure(figsize=(17, 12)); gs = fig.add_gridspec(2, 2)
    a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[1, :])
    # a: section through the rear base rail at x 180, looking from the left side (y across, z up)
    rail_section(a, 340, 10)
    cover_in_slot(a, 340, 10, "+u", label="slot cover: head flush with the rail's REAR face")
    a.add_patch(C((345, 10), 1.3, fc=CAB, ec="k", zorder=3, label="wires under it (the strips' feeds / the sill bundle)"))
    a.add_patch(R((280, 3), 23, 60, fc="#333", ec="k", alpha=0.5, label="bottom drawer (ends y 303) — in front"))
    a.add_patch(R((350, 0), 5, 44, fc="#2d6cdf", ec="k", alpha=0.5, label="board holder plate on the rear face (x 90–150 only)"))
    a.add_patch(R((355, 75), 30, 60, fc="#eee", ec="k", label="power strip on the upright's rear face (further back, y 355+, from z 75)"))
    a.annotate("pushed in from BEHIND", (350, 10), (365, 40), arrowprops=dict(arrowstyle="->"), fontsize=9)
    finish(a, "1. Looking from the LEFT side — section through the REAR base rail (y 330–350, z 0–20)\ncover in its REAR slot, wires underneath (v2 2026-10-16: was the top slot)", "frame y (mm)", "frame z (mm)", (270, 390), (-8, 75))
    # b: plan view from above
    for x, y in ((0, 0), (341, 0), (0, 330), (341, 330)): b.add_patch(R((x, y), 20, 20, fc=ALD, ec="k", label="uprights" if (x, y) == (0, 0) else None))
    b.add_patch(R((0, 20), 20, 310, fc=AL, ec="k")); b.add_patch(R((341, 20), 20, 310, fc=AL, ec="k"))
    b.add_patch(R((20, 330), 321, 20, fc=AL, ec="k", label="rear base cross rail x 20–341"))
    b.add_patch(R((20, 3), 321, 300, fc="#333", ec="k", alpha=0.25, label="bottom drawer (in front, y to 303)"))
    b.add_patch(R((90, 350), 60, 15, fc="#2d6cdf", ec="k", alpha=0.5, label="board holder on the rail's rear face, x 90–150"))
    b.add_patch(R((25, 349), 65, 3, fc=BLUE, ec="k", label="COVER B1 x 25–90 (65) and B2 x 150–336 (186) in the REAR slot"))
    b.add_patch(R((150, 349), 186, 3, fc=BLUE, ec="k"))
    b.add_patch(P([(10, 300), (10, 340), (24, 340), (26, 352), (100, 352)], closed=False, fc="none", ec=CAB, lw=1.8, alpha=0.9, label="wires: down the rear-left upright's inner slot, under the rail, along the rear slot to the holder"))
    b.add_patch(P([(140, 352), (336, 352), (338, 340), (351, 340), (351, 300)], closed=False, fc="none", ec=CAB, lw=1.8, alpha=0.9, label="right strip's feed: from the holder along the rear slot, under the rail, up the rear-right upright's inner slot"))
    b.annotate("covers pushed into the REAR slot from behind —\nnothing else lives in it (the rail's connectors are on its FRONT face)", (240, 350), (180, 250), ha="center", arrowprops=dict(arrowstyle="->"), fontsize=9)
    finish(b, "2. Plan view from above — covers B1 and B2 lie in the rear slot of the rear base rail either side of the board holder", "frame x (mm)", "frame y (mm)", (-15, 375), (-10, 390))
    # c: elevation from behind the frame (x reversed so left is left when you stand behind? keep frame x; say so)
    c.add_patch(R((0, 0), 20, 130, fc=ALD, ec="k", label="rear-left upright")); c.add_patch(R((341, 0), 20, 130, fc=ALD, ec="k", label="rear-right upright"))
    c.add_patch(R((20, 0), 321, 20, fc=AL, ec="k", label="rear base cross rail z 0–20"))
    c.add_patch(R((20, 7.05), 321, 5.9, fc="white", ec="k", label="the rail's REAR slot (mouth), centre z 10"))
    c.add_patch(R((25, 7.05), 65, 5.9, fc=BLUE, ec="k", label="COVER B1 x 25–90 and B2 x 150–336, flush with the rear face"))
    c.add_patch(R((150, 7.05), 186, 5.9, fc=BLUE, ec="k"))
    c.add_patch(R((90, 0), 60, 44, fc="#2d6cdf", ec="k", alpha=0.4, label="board holder x 90–150, z 0–44 (wiring sheets in parts/wiring/)"))
    c.add_patch(R((7.05, 0), 5.9, 130, fc="white", ec="k", label="uprights' inner-face slots (the wire goes up/down these, under the LED strips)"))
    c.add_patch(R((348.05, 0), 5.9, 130, fc="white", ec="k"))
    c.add_patch(R((25, 75), 78, 55, fc="#eee", ec="k", alpha=0.8, label="power strip (rear face of the rear-left upright, z 75–425)"))
    c.add_patch(P([(10, 120), (10, 2), (14, -3), (24, -3), (26, 10), (100, 10)], closed=False, fc="none", ec=CAB, lw=2.5, label="wire runs: down the uprights' inner slots, under the rail (6 mm, on the feet), along the rear slot to the holder"))
    c.add_patch(P([(140, 10), (336, 10), (338, -3), (348, -3), (351, 2), (351, 120)], closed=False, fc="none", ec=CAB, lw=2.5))
    c.text(180, 110, "Seen from BEHIND the frame, drawn in frame x (left upright at x 0 is on the left here).", ha="center", fontsize=9, style="italic")
    finish(c, "3. Rear elevation — the covers sit in the rear slot either side of the board holder; the wires come under the rail from the uprights' inner slots", "frame x (mm)", "frame z (mm)", (-15, 375), (-8, 135), ncol=3)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "tpu-where-3-cover-rear-base.png"), dpi=100); plt.close(fig)

# ---------------------------------------------------------------- 4. test pieces
def sheet_tests():
    fig, (a, b) = plt.subplots(1, 2, figsize=(17, 7))
    # a: spigot sweep into an upright's bottom bore (section)
    a.add_patch(R((-10, 0), 20, 60, fc=ALD, ec="k", label="an upright, bottom end (frame tipped on its side, or an offcut)"))
    a.add_patch(R((-2.1, 0), 4.2, 60, fc="white", ec="k", label="centre hole, ~Ø4.2"))
    a.add_patch(R((-27, -6), 72, 3, fc=BLUE, ec="k", label="spigot sweep strip: 4.2 / 4.6 / 5.0 / 5.4 stamped (shown with the 4.6 in the hole)"))
    for i, (x, d) in enumerate(zip((-18, 0, 18, 36), (4.2, 4.6, 5.0, 5.4))):
        a.add_patch(R((x - d / 2, -3), d, 8, fc=BLUE, ec="k")); a.text(x, -9, f"{d}", ha="center", fontsize=9)
    a.text(0, 66, "Push each spigot into the hole in turn.\nWinner: goes in with a thumb, holds the frame's weight when you lift that corner, comes out with a twist.", ha="center", fontsize=9)
    finish(a, "Test 1 — the spigot sweep goes into the centre hole at the BOTTOM of an upright (or any 2020 offcut)", "mm", "mm", (-40, 50), (-14, 75), ncol=1)
    # b: cover sweep pieces into an offcut's slot
    rail_section(b, 0, 0)
    cover_in_slot(b, 0, 0, "+v", label="cover test piece (40 mm) pressed into any slot of an offcut")
    b.text(0, 22, "Three 40 mm pieces: 7.0 / 7.4 / 8.0 stamped on top.\nWinner: goes in along its length with a thumb and a fingernail will NOT lift it out.\nBoth winners → tell me the numbers; if they are 4.6 and 7.4 nothing reprints.", ha="center", fontsize=9)
    b.text(0, -16, "After the tests: bin all four pieces. They go nowhere on the frame.", ha="center", fontsize=9, style="italic")
    finish(b, "Test 2 — the cover sweep pieces go into a slot on a 2020 offcut (bar Z / W)", "mm", "mm", (-30, 30), (-20, 30), ncol=1)
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "tpu-where-4-test-pieces.png"), dpi=100); plt.close(fig)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet_stop_caps(); sheet_cover_left(); sheet_cover_rear(); sheet_tests()
    print("wrote", OUT)
