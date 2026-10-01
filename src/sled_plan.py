# sled_plan.py — plan-view check sheet of the sled ladder (parts/sled-ladder-plan.png): the four beam halves and the three
# bars in world coordinates, section at z 341 (tabs, sockets, bodies) and z 350 (front bar above the beams, guide lips).
import os, sys, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); PARTS = os.path.normpath(os.path.join(HERE, "..", "parts"))
from parts.sled_beam import PARTS as BEAMS
from parts.sled_bars import PARTS as BARS
fig, ax = plt.subplots(figsize=(9, 9))
def draw(solid, level, color, lw):
    tmp = os.path.join("/tmp", "sled_plan_tmp.stl"); import cadquery as cq; cq.exporters.export(solid, tmp, tolerance=0.05)
    m = trimesh.load(tmp); s = m.section(plane_origin=[0, 0, level], plane_normal=[0, 0, 1])
    if s is None: return
    for ent in s.entities:
        pts = s.vertices[ent.points]; ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw)
for fn in BEAMS.values(): draw(fn(), 341.0, "k", 0.8)
for n, fn in BARS.items(): draw(fn(), 341.0, "C0", 1.2); draw(fn(), 350.0, "C3", 1.2)
ax.add_patch(Rectangle((23, 3), 315, 132, fill=False, ec="C1", ls="--", lw=1)); ax.text(100, 60, "scope 23–338 × y 3–135 (with bumpers), chassis at z 355", color="C1", fontsize=8)
ax.add_patch(Rectangle((50, 195), 291, 135, fill=False, ec="C2", ls="--", lw=1)); ax.text(100, 255, "rear box 50–341 × y 195–330, floor 346", color="C2", fontsize=8)
ax.text(30, -8, "black: beams v1 (z 341)   blue: bars at z 341 (tabs into the beams' sockets)   red: above the beams (front bar to 355, its saddles on the beam tops 346–353 with the M3 holes, guide lips 346–356)", fontsize=8)
ax.set_xlim(0, 361); ax.set_ylim(-14, 345); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm, front at 0)")
ax.set_title("Sled ladder — beams (front halves v2: two tongues) + front bar v3 (closed pockets, saddles) + cross bars v1, plan, world coordinates", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(PARTS, "sled-ladder-plan.png"), dpi=110); print("ok")
