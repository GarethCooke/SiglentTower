# drawer_plan.py — check sheet for the bottom-drawer quarters (parts/drawer/drawer-quarters-plan.png): the four printed
# quarters put back together in drawer coordinates (x from the left wall face, y from the front face), sections at three
# heights, plus the groove section with the runner's rib in it. Run after parts/drawer_quarters.py.
import os, sys, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.normpath(os.path.join(HERE, "..", "parts", "drawer"))
from parts.drawer_quarters import QUARTERS, SEAM_X, SEAM_Y, PAD_X, PAD_Z
from parts.drawer_runner import runner_section, groove_cut, RAIL, GAP, RUNNER_CLR
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(15, 8), gridspec_kw={"width_ratios": [3, 1]})
def sec(i, level, color, lw):
    m = trimesh.load(os.path.join(OUT, f"drawer-Q{i}-v1.stl")); x0, x1, y0, y1 = QUARTERS[i]
    dx = x0 - (8.0 if x0 > 0 else 0.0); dy = y0 - (8.0 if y0 > 0 else 0.0)     # the STL is at the origin; tabs of the rear/right quarters stick out 8
    s = m.section(plane_origin=[0, 0, level], plane_normal=[0, 0, 1])
    if s is None: return
    for ent in s.entities:
        pts = s.vertices[ent.points]; ax.plot(pts[:, 0] + dx, pts[:, 1] + dy, color=color, lw=lw)
for i in range(1, 5):
    sec(i, 1.5, "0.6", 0.7); sec(i, 8.0, "C0", 0.8); sec(i, 40.0, "k", 1.0)
ax.axvline(SEAM_X, color="r", lw=0.5, ls=":"); ax.axhline(SEAM_Y, color="r", lw=0.5, ls=":")
for xc in PAD_X: ax.plot(xc, 5.2, "C3o", ms=4)
ax.text(2, 300 + 4, "grey: floor tabs (z 1.5)   blue: groove boss, runner grooves, facia pads (z 8)   black: walls and wall dovetails (z 40)   red dots: M3 facia screws at z 20", fontsize=8)
ax.text(SEAM_X + 2, 20, "seam x 157.5", color="r", fontsize=7, rotation=90); ax.text(20, SEAM_Y + 2, "seam y 150", color="r", fontsize=7)
for i, (x0, x1, y0, y1) in QUARTERS.items(): ax.text((x0 + x1) / 2, (y0 + y1) / 2, f"Q{i}", fontsize=16, ha="center", va="center", color="0.4")
ax.set_xlim(-12, 327); ax.set_ylim(-4, 312); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_xlabel("x (mm, left wall face at 0)"); ax.set_ylabel("y (mm, front at 0)")
ax.set_title("Bottom drawer — four quarters v1 assembled, drawer coordinates (315 × 300 × 60)", fontsize=9)
# groove section: left wall, looking from the front. Drawer coordinates; the runner in frame coords shifted x -23, z -3.
pts = [(x - (RAIL + GAP), z - 3) for x, z in runner_section()]
ax2.fill([p[0] for p in pts], [p[1] for p in pts], color="0.75", ec="k", lw=0.8, label="runner (ABS+), rail at x −23…−3")
g = groove_cut(10); s = g.section(plane_origin=[0, 5, 0], plane_normal=[0, 1, 0]) if False else None
# the drawer wall + boss + floor outline with the groove
wall = [(0, 0), (30, 0), (30, 3), (7.3, 3), (7.3, 10.0), (0, 17.3), (0, 60), (2.4, 60), (2.4, 20), (10, 20), (10, 3)]
wall = [(0, 0), (30, 0), (30, 3), (10, 3), (10, 20), (2.4, 20), (2.4, 60), (0, 60), (0, 17.3), (7.3, 10.0), (7.3, 3), (0, 3)]
ax2.fill([p[0] for p in wall], [p[1] for p in wall], color="C0", alpha=0.25, ec="C0", lw=1, label="drawer wall, boss, floor (PETG)")
ax2.axvline(-3, color="k", lw=0.5, ls=":"); ax2.text(-3.5, 40, "rail inner face x −3", fontsize=7, rotation=90, ha="right")
ax2.annotate(f"back {RUNNER_CLR}", (7.15, 6), fontsize=7); ax2.annotate("rib on the floor top (0)", (11, 3.5), fontsize=7)
ax2.annotate(f"roof / rib slope {RUNNER_CLR} (drawer hangs here)", (4, 14), fontsize=7)
ax2.set_xlim(-24, 34); ax2.set_ylim(-2, 34); ax2.set_aspect("equal"); ax2.grid(True, lw=0.3); ax2.legend(fontsize=7, loc="upper right")
ax2.set_title("Left wall section, from the front (P3 geometry)", fontsize=9); ax2.set_xlabel("x from the wall face"); ax2.set_ylabel("z from the drawer bottom")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "drawer-quarters-plan.png"), dpi=110); print("ok")
