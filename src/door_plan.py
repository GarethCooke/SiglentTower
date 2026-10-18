# door_plan.py — check sheet for the door set (parts/door/door-plan.png): the right side's band 4 seen from outside,
# three sections through the magnets and the fixed tile's leg, and the print / fit notes. python src/door_plan.py
import os, sys, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Polygon as P, Circle as C
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "parts")); sys.path.insert(0, HERE)
import door_set as ds, door_hinge as dh
OUT = os.path.normpath(os.path.join(HERE, "..", "parts", "door"))
AL, ALD, TILE, DOOR, ABS, MAG, BLUE = "#c8c8c8", "#9a9a9a", "#3a3a3a", "#555", "#111", "#c33", "#2d6cdf"

def finish(ax, title, xl, yl, xlim, ylim, ncol=2):
    ax.set_title(title, fontsize=10); ax.set_aspect("equal"); ax.set_xlabel(xl); ax.set_ylabel(yl)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fontsize=7.5, ncol=ncol)

def main():
    fig = plt.figure(figsize=(18, 16)); gs = fig.add_gridspec(2, 3, height_ratios=[1.5, 1])
    a = fig.add_subplot(gs[0, :]); b = fig.add_subplot(gs[1, 0]); c = fig.add_subplot(gs[1, 1]); d = fig.add_subplot(gs[1, 2])
    # ---- a: right side elevation from outside (front on the LEFT), frame y across, z up
    a.add_patch(R((0, 200), 20, 320, fc=ALD, ec="k", label="uprights (front on the left)")); a.add_patch(R((330, 200), 20, 320, fc=ALD, ec="k"))
    a.add_patch(R((20, dh.RAIL_Z0), 310, 20, fc=AL, ec="k", label="scope rail z 311–331 (outer slot at 321)")); a.add_patch(R((20, 490), 310, 20, fc=AL, ec="k", label="top rail z 490–510 (slot at 500)"))
    a.add_patch(R((20, 318.05), 310, 5.9, fc="white", ec="k")); a.add_patch(R((20, 497.05), 310, 5.9, fc="white", ec="k"))
    a.add_patch(R((20, 237.5), 310, dh.SLOT_Z + 3.25 - 237.5, fc=TILE, ec="k", alpha=0.35, label="band-3 tiles (printed) up to the scope rail's slot"))
    a.add_patch(R((ds.DOOR_Y0, ds.DOOR_Z0), ds.DOOR_Y1 - ds.DOOR_Y0, ds.DOOR_H, fc=DOOR, ec="k", alpha=0.6, label=f"DOOR y 20–250, z 347–499 (230 × 152 × 3), hex, no clips"))
    a.add_patch(R((ds.FIX_Y0, ds.FIX_Z0), ds.FIX_Y1 - ds.FIX_Y0, ds.FIX_H, fc=TILE, ec="k", alpha=0.6, label=f"FIXED TILE y 250–330, z 334–500 (80 × 166 × 3), two fingers up into the top rail's slot"))
    for y0 in (294, 256): a.add_patch(R((y0, 494.75), 30, 8.5, fc=BLUE, ec="k", alpha=0.8, label="fixed tile's clip fingers (y 256–286, 294–324)" if y0 == 294 else None))
    for (y0, y1) in ds.PADS_Y:
        a.add_patch(R((y0, dh.RAIL_Z0), y1 - y0, dh.PLATE_Z1 - dh.RAIL_Z0, fc=ABS, ec="k", label="hinge FRAME leaves on the rail's outer face (y 23–47, 223–247), M5 × 12 at z 321" if y0 < 100 else None))
        a.add_patch(C(((y0 + y1) / 2, dh.AXIS_Z), 4, fc="none", ec="k", lw=1.5, label="hinge axis z 341 (barrel Ø8, outboard at frame x 369)" if y0 < 100 else None))
        a.add_patch(R((y0, ds.DOOR_Z0), y1 - y0, ds.PAD_Z1 - ds.DOOR_Z0, fc="none", ec="w", ls="--", label="hinge DOOR leaves glued to the door's back (z 347–371)" if y0 < 100 else None))
    for y in ds.MAG_Y:
        a.add_patch(R((y - 6, ds.MAG_Z - 6), 12, 12, fc=MAG, ec="k", label="magnet bosses on the door's back, 12 × 12 × 3, Ø10.4 × 2.2 pocket, centres (34, 479) and (236, 479)" if y < 100 else None))
    a.add_patch(R((ds.SLOT_Y - ds.SLOT_W / 2, ds.SLOT_Z - ds.SLOT_H / 2), ds.SLOT_W, ds.SLOT_H, fc="white", ec="k", label="finger slot 45 × 12 at (135, 482): hook the door's edge through it"))
    a.add_patch(R((20, 455), 29, 33, fc="none", ec=MAG, ls="--", lw=1.5, label="front magnet bracket behind the door: plate on the front upright's rear face y 20–26 (M5 at z 461), leg y 26–49"))
    a.add_patch(R((228, 467), 34, 21, fc="none", ec=MAG, ls=":", lw=1.5, label="rear magnet tab behind: glued to the fixed tile at y 250–262, plate reaching to y 228"))
    a.add_patch(R((327, ds.LEG_Z0), 3, ds.LEG_Z1 - ds.LEG_Z0, fc=BLUE, ec="k", label="fixed tile's LEG (19 deep, into the frame) on the rear upright's front face, M5 × 10 at z 361"))
    a.annotate("sled band z 331–347 stays open under the door (the box floor is at 346)", (175, 339), (175, 290), ha="center", arrowprops=dict(arrowstyle="->"), fontsize=8.5)
    a.annotate("door opens DOWN and OUT about the axis: at 180° it hangs at frame x 365–384, down to z 183", (135, 347), (135, 260), ha="center", arrowprops=dict(arrowstyle="->"), fontsize=8.5)
    finish(a, "1. Right side seen from OUTSIDE (front on the left): band 4 = the door + the fixed rear tile", "frame y (mm)", "frame z (mm)", (-10, 360), (225, 520), ncol=2)
    # ---- b: section at y 34 (front magnets), frame x across, z up
    b.add_patch(R((341, 490), 20, 20, fc=AL, ec="k", label="top rail x 341–361")); b.add_patch(R((348.05, 489), 5.9, 2.75, fc="white", ec="k"))
    b.add_patch(R((341, 455), 20, 33, fc="none", ec=MAG, ls="--", label="bracket plate (behind this section, y 20–26)"))
    b.add_patch(R((348.25, 488), 5.5, 5, fc=ABS, ec="k", label="tongue up into the top rail's bottom slot"))
    b.add_patch(R((351.5, 467), 6, 21, fc=ABS, ec="k", label="bracket leg x 351.5–357.5, y 26–49"))
    b.add_patch(R((355.3, 473.8), 2.2, 10.4, fc=MAG, ec="k", label="magnet in the leg's pocket, face at x 357.5"))
    b.add_patch(R((361, 347), 3, 152, fc=DOOR, ec="k", label="door x 361–364")); b.add_patch(R((358, 473), 3, 12, fc=DOOR, ec="k")); b.add_patch(R((358, 473.8), 2.2, 10.4, fc=MAG, ec="k", label="magnet in the door's boss, face at x 358"))
    b.annotate("0.5 gap", (357.75, 490), (350, 500), arrowprops=dict(arrowstyle="->"), fontsize=8)
    finish(b, "2. Section at y 34 — the front magnets (hinge as door_hinge.py, below this view)", "frame x (mm)", "frame z (mm)", (338, 368), (450, 512), ncol=1)
    # ---- c: section at y 236 (rear magnets)
    c.add_patch(R((341, 490), 20, 20, fc=AL, ec="k", label="top rail"))
    c.add_patch(R((361, 347), 3, 152, fc=DOOR, ec="k", label="door")); c.add_patch(R((358, 473), 3, 12, fc=DOOR, ec="k")); c.add_patch(R((358, 473.8), 2.2, 10.4, fc=MAG, ec="k", label="door magnet, face at x 358"))
    c.add_patch(R((354.5, 467), 3, 21, fc=ABS, ec="k", label="tab plate x 354.5–357.5 (y 228–250)")); c.add_patch(R((355.3, 473.8), 2.2, 10.4, fc=MAG, ec="k", label="tab magnet, face at x 357.5"))
    c.add_patch(R((354.5, 467), 6.5, 21, fc="none", ec=MAG, ls=":", label="tab block x 354.5–361 at y 250–262, CA'd to the fixed tile's back (behind this section)"))
    c.add_patch(R((361, 334), 3, 166, fc="none", ec=TILE, ls="--", label="fixed tile (behind, y 250–330)"))
    finish(c, "3. Section at y 236 — the rear magnets (the tab is glued to the fixed tile)", "frame x (mm)", "frame z (mm)", (338, 368), (450, 512), ncol=1)
    # ---- d: section at y 328 (the fixed tile's leg), frame x across, z up — the rear upright is at y 330–350 behind
    d.add_patch(R((341, 300), 20, 215, fc=ALD, ec="k", label="rear-right upright (y 330–350), its front face at y 330")); d.add_patch(R((348.05, 300), 5.9, 215, fc="white", ec="k", label="that face's slot, centre x 351"))
    d.add_patch(R((341, 490), 20, 20, fc=AL, ec="k", alpha=0.5, label="top rail (behind)"))
    d.add_patch(R((361, 334), 3, 166, fc=TILE, ec="k", label="fixed tile x 361–364, z 334–500"))
    d.add_patch(R((342, 341), 19, 40, fc=BLUE, ec="k", label="LEG x 342–361, y 327–330, z 341–381 — flat on the upright's front face"))
    d.add_patch(C((351, 361), 2.75, fc="white", ec="k", label="M5 × 10 + drop-in T-nut at z 361 (teardrop hole, bolt runs along y)"))
    d.add_patch(R((341, 311), 20, 20, fc=AL, ec="k", alpha=0.5, label="scope rail (behind, to y 330)"))
    d.add_patch(R((315, 337), 25.5, 9, fc="#444", ec="k", alpha=0.5, label="right sled beam x 315–340.5 (1.5 clear of the leg)"))
    d.annotate("the leg holds the bottom of a tile that has no rail to clip to;\nband 4 LEFT will use the same leg on its two uprights", (342, 381), (312, 388), fontsize=8, arrowprops=dict(arrowstyle="->"))
    finish(d, "4. Section at y 328 — the fixed tile's leg, bolted to the rear upright", "frame x (mm)", "frame z (mm)", (310, 368), (330, 395), ncol=1)
    fig.text(0.02, 0.005,
             "PRINT   door-v1: black PETG, face down as exported, 230 × 152, 68 cm³, no brim, no support (the bosses and glue pads rise from the back).   rear-tile-v1: black PETG, face down, 169 × 80 × 22 (the leg stands 19), 30 cm³.\n"
             "            magnet-bracket-front-v1: black ABS, plate face down as exported, 6.5 cm³.   magnet-tab-rear-v1: black ABS, lying on its back as exported, 3 cm³.   Door + rear tile share one PETG plate (230 × 240); bracket + tab go beside the hinge pair (ABS).\n"
             "HARDWARE   4 × Ø10 × 2 magnets · 2 × M5 × 10 + 2 drop-in T-nuts (bracket, leg) · the second hinge pair (hinge-door-v1 + hinge-frame-v1) with 2 × M5 × 12 + T-nuts and two 2.9 printed pins.\n"
             "FIT   1 hinge frame leaves into the scope rail's outer slot at y 23 and 223, bolts nipped.   2 door leaves CA'd to the door's back on their pads, shelf under the edge, pins in.   3 door on, bolts tight, swing it to 180 and back.\n"
             "         4 fixed tile: fingers into the top rail's slot, leg bolted to the rear upright.   5 magnets: mark polarity so door-to-holder ATTRACTS; CA the door's two in; close the door; set the bracket's magnet on its pocket,\n"
             "         bolt the bracket so the faces meet, then CA it; the tab's magnet in, the tab CA'd to the fixed tile with the door closed as the jig (0.5 gap = a strip of paper).",
             ha="left", va="bottom", fontsize=8.5, family="monospace")
    plt.tight_layout(rect=(0, 0.09, 1, 1)); fig.savefig(os.path.join(OUT, "door-plan.png"), dpi=100); plt.close(fig)
    print("wrote", os.path.join(OUT, "door-plan.png"))

if __name__ == "__main__":
    main()
