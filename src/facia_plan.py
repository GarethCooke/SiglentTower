# facia_plan.py — front view of the bottom-drawer facia with its pull insert and logo (parts/drawer/drawer-facia-plan.png).
import os, sys, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.normpath(os.path.join(HERE, "..", "parts", "drawer"))
sys.path.insert(0, HERE); from parts.drawer_facia import PAD_X, PAD_Z, FW, FH, NOTCH_W, NOTCH_H, FT
fig, ax = plt.subplots(figsize=(13, 5))
def outline(name, level, color, lw, dy=0.0):
    m = trimesh.load(os.path.join(OUT, name)); s = m.section(plane_origin=[0, level, 0], plane_normal=[0, 1, 0])
    for e in s.entities:
        p = s.vertices[e.points]; ax.plot(p[:, 0], p[:, 2], color=color, lw=lw)
outline("drawer-facia-v1.stl", 0.3, "k", 1.0)                      # just inside the front face: outline + logo recess
outline("drawer-facia-v1.stl", 2.5, "C3", 0.7)                     # near the back face: screw holes
m = trimesh.load(os.path.join(OUT, "drawer-pull-insert-v1.stl"))   # printed face down: its print z is the facia's -y; print y is the facia z
s = m.section(plane_origin=[0, 0, 0.5], plane_normal=[0, 0, 1])
for e in s.entities:
    p = s.vertices[e.points]; ax.plot(p[:, 0] + (FW - 100) / 2, FH - 23 + p[:, 1], color="C0", lw=1.0)
for xc in PAD_X: ax.plot(xc, PAD_Z, "C3o", ms=4)
ax.add_patch(Rectangle((0, 60), FW, 3, fc="0.85", ec="none")); ax.text(5, 60.5, "drawer body top 60 / housing top 61–64 behind", fontsize=7)
ax.text(FW / 2, FH - 10, "pull insert 100 × 23 (blue), slot 80 × 12 — the notch is 100.3 × 23.15", ha="center", fontsize=8, color="C0")
ax.text(240, 42, "iguana inlay 58.7 × 21.1 × 0.8 (blue), head right", fontsize=8)
ax.text(40, 14, "Ø2.5 blind holes (back face, 2.3 deep) for M3 × 10 from the screw pads", fontsize=7, color="C3")
ax.set_xlim(-5, 320); ax.set_ylim(-3, 88); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_xlabel("x (mm, drawer: left wall face at 0)"); ax.set_ylabel("z (mm, drawer bottom at 0; frame z = +3)")
ax.set_title("Bottom-drawer facia v1 — front view (315 × 83 × 3, dark grey PETG, prints standing on its bottom edge)", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "drawer-facia-plan.png"), dpi=110); print("ok")
