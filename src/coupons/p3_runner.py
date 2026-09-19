# P3 coupon — drawer runner + drawer-side groove stub (ROADMAP §3). Two materials, two files:
#   runner-80:  80 mm of the real runner (src/parts/drawer_runner.py), one M5 counterbore in the middle. BLACK ASA (the
#               production sliding half). Printed LEG-TOP DOWN as the production part: the counterbore opens onto the bed
#               (Bambu "bridge counterbore holes: sacrificial layer" — punch the disc out, as the cradles). Bolt it to the
#               200 coupon rail through the TOP slot, rib hanging over the rail's side face.
#   stub-100:   100 mm of the drawer's outer side wall with the floor strip, the 10 x 20 groove boss and the house-shaped
#               groove. YELLOW PETG, floor down. Slide it onto the runner from either end.
# Pass: stub slides the runner's full length by hand, side play < 0.5, no stick-slip dry or with PTFE, no support in the
# preview. Sets RUNNER_CLR in fit.py (grows the groove's back and roof only; the bearing flank rides on the rib).
# Output: coupons/p3/runner-80.stl, stub-100.stl, p3-section.png.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.drawer_runner import runner_printable, wall_stub, runner_section, groove_cut, RAIL, RIB_X1, Z_BEAR, RIB_H, RIB_TIP_H, BOSS_T, BOSS_H, DRAWER_FLOOR
from fit import RUNNER_CLR
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p3")); os.makedirs(OUT, exist_ok=True)

pieces = {"runner-80": runner_printable(80.0, [40.0]), "stub-100": wall_stub(100.0)}
for name, p in pieces.items():
    bb = p.val().BoundingBox(); p0 = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p0, path, tolerance=0.01, angularTolerance=0.1)
    print(f"{name:10s} {bb.xlen:5.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3")
check(os.path.join(OUT, "runner-80.stl"))          # only downward face: the counterbore ceiling on the bed (sacrificial layer)
check(os.path.join(OUT, "stub-100.stl"))           # roof is 45°: nothing steeper points down

# section sheet — frame coordinates, left side, looking along the rail from the front
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Rectangle
    fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=160)
    ax.add_patch(Rectangle((0, 0), RAIL, RAIL, fc="#d9d9d9", ec="#555", lw=1))                     # 2020 rail
    for cx, cy, horiz in [(10, 20, True), (20, 10, False)]:                                        # top and inner slots (schematic)
        if horiz: ax.add_patch(Polygon([(cx-2.95, 20), (cx-2.95, 18.25), (cx-5.3, 18.25), (cx-5.3, 13.85), (cx+5.3, 13.85), (cx+5.3, 18.25), (cx+2.95, 18.25), (cx+2.95, 20)], fc="white", ec="#555", lw=0.8))
        else:     ax.add_patch(Polygon([(20, cy-2.95), (18.25, cy-2.95), (18.25, cy-5.3), (13.85, cy-5.3), (13.85, cy+5.3), (18.25, cy+5.3), (18.25, cy+2.95), (20, cy+2.95)], fc="white", ec="#555", lw=0.8))
    ax.add_patch(Polygon(runner_section(), fc="#3a3a3a", ec="black", lw=1, label="runner (ASA)"))
    ax.add_patch(Rectangle((5.5 - 0.05 + 4.5, 20 - 0.1), 1, 0.1, fc="none"))                       # keeps autoscale honest
    # drawer wall + boss with the groove, drawn in frame coordinates: drawer x -> frame x + 23, z -> z + 3
    OX, OZ = RAIL + 3.0, 3.0
    wall = [(OX, OZ), (OX + 40, OZ), (OX + 40, OZ + DRAWER_FLOOR), (OX + BOSS_T, OZ + DRAWER_FLOOR), (OX + BOSS_T, OZ + BOSS_H),
            (OX + 2.4, OZ + BOSS_H), (OX + 2.4, OZ + 40), (OX, OZ + 40)]
    g = [(x + OX, z + OZ) for x, z in [(0, DRAWER_FLOOR), (RIB_X1 - RAIL - 3 + RUNNER_CLR, DRAWER_FLOOR), (RIB_X1 - RAIL - 3 + RUNNER_CLR, DRAWER_FLOOR + RIB_TIP_H + RUNNER_CLR), (0, DRAWER_FLOOR + RIB_H + RUNNER_CLR)]]
    ax.add_patch(Polygon(wall, fc="#f2d24b", ec="#7a6a10", lw=1, label="drawer wall + boss (PETG)"))
    ax.add_patch(Polygon(g, fc="white", ec="#7a6a10", lw=1))
    ax.plot([10, 10], [20, 34], color="#c33", lw=2); ax.plot([10], [34], marker="v", color="#c33", ms=8)   # M5 into the top slot
    for (x, z, t, ha) in [(15, 33.5, "M5 × 10 + T-nut, top slot\ncbore Ø10 × 5.2", "left"), (RIB_X1 + 0.5, Z_BEAR - 0.3, f"bearing z {Z_BEAR:.0f}: drawer floor top rests on the rib", "left"),
                          (RIB_X1 + 0.5, 13.5, f"rib tip x {RIB_X1:.0f} ⟷ groove back {RIB_X1 + RUNNER_CLR:.1f}", "left"),
                          (33, 26, f"roof 45°, {RUNNER_CLR} over the rib's slope", "left"), (21.3, 8.5, "plate 2.7\n0.3 to the wall", "left"),
                          (1, 22, "leg on the rail top", "left"), (2, 10, "2020 base rail", "left"), (OX + 12, OZ + 30, "drawer outer wall 2.4\nboss 10 × 20 inboard", "left")]:
        ax.text(x, z, t, fontsize=7.5, ha=ha, va="center", color="#111" if "rail" in t or "drawer" in t else "#c33" if "M5" in t else "#111")
    ax.set_xlim(-2, 66); ax.set_ylim(-2, 46); ax.set_aspect("equal"); ax.set_xlabel("x from the rail's outer face (mm)"); ax.set_ylabel("z from the rail bottom (mm)")
    ax.set_title("P3 — drawer runner on the base rail, drawer wall groove riding the rib (left side, from the front)", fontsize=9)
    ax.legend(loc="upper right", fontsize=7.5); ax.grid(alpha=0.25, lw=0.5)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "p3-section.png")); print("section sheet written")
except ImportError:
    print("matplotlib not available: no section sheet")
