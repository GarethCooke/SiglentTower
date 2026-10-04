# column_plan.py — section through the column bay at y 150 (parts/column/column-plan.png): drawer, four strips, rails.
import os, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cadquery as cq, trimesh
from parts.column_drawer import drawer_in_frame, strip_in_frame
def secs(solid, level):
    tmp = "/tmp/c.stl"; cq.exporters.export(solid, tmp, tolerance=0.05); m = trimesh.load(tmp)
    s = m.section(plane_origin=[0, level, 0], plane_normal=[0, 1, 0])
    return [] if s is None else [s.vertices[e.points][:, [0, 2]] for e in s.entities]
fig, (ax, az) = plt.subplots(1, 2, figsize=(14, 9), gridspec_kw={"width_ratios": [1.2, 1]})
for a in (ax, az):
    for x0, z0 in ((251, 68), (251, 227.5), (341, 68), (341, 227.5)): a.add_patch(Rectangle((x0, z0), 20, 20, fc="0.55", ec="k"))
    for p in secs(drawer_in_frame(), 150): a.add_patch(Polygon(p, fc="0.85", ec="k", lw=0.8))
    for k in ("lower", "upper"):
        for s in ("L", "R"):
            for p in secs(strip_in_frame(k, s), 150): a.add_patch(Polygon(p, fc="C0" if k == "lower" else "C2", alpha=0.6, ec="k", lw=0.6))
ax.text(276, 320, "column drawer 64 × 285 × 240 (x 274–338, z 91–331)", fontsize=8)
ax.text(255, 100, "lower strips (blue): P3 rib — the drawer hangs on them;\nbolt bar z 70–86 under the drawer floor, 4 × M5 into the side slot", fontsize=7)
ax.text(255, 215, "upper strips (green): guide rib, bolts through the rib;\n0.5 slack — catches the roof only if the drawer tips", fontsize=7)
ax.set_xlim(245, 367); ax.set_ylim(60, 340); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_xlabel("x"); ax.set_ylabel("z"); ax.set_title("Column bay — section at y 150", fontsize=9)
az.set_xlim(266, 290); az.set_ylim(66, 114); az.set_aspect("equal"); az.grid(True, lw=0.3); az.set_title("Lower left strip detail: rail face x 271, plate 2.7, rib 7 into the groove, rib bottom = drawer floor top (z 94)", fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(HERE, "..", "parts", "column", "column-plan.png"), dpi=110); print("ok")
