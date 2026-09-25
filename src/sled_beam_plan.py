# sled_beam_plan.py — plan-view check sheet for the left sled beam (parts/sled-beam-plan.png): the printed halves'
# outlines put back in world coordinates, with the scope, bumper, stand leg, foot, bars and channel overlaid.
# Run after parts/sled_beam.py. Black = section at z 345.5 (top face, cup and pocket outlines); grey = z 339 (groove).
import os, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.normpath(os.path.join(HERE, "..", "parts"))
fig, ax = plt.subplots(figsize=(7, 14))
def sec(name, dx, dy, level, color):
    m = trimesh.load(os.path.join(PARTS, f"{name}.stl")); s = m.section(plane_origin=[0, 0, level], plane_normal=[0, 0, 1])
    for ent in s.entities:
        pts = s.vertices[ent.points]; ax.plot(pts[:, 0] + dx, pts[:, 1] + dy, color=color, lw=0.9)
sec("sled-beam-left-front-v1", 20.5, 4, 8.5, "k"); sec("sled-beam-left-front-v1", 20.5, 4, 2.0, "0.6")
sec("sled-beam-left-rear-v1", 20.5, 165, 8.5, "k"); sec("sled-beam-left-rear-v1", 20.5, 165, 2.0, "0.6")
ax.add_patch(Rectangle((23, 3), 315, 108, fill=False, ec="C1", ls="--", lw=1)); ax.text(24, 60, "scope body 23–338 × y 3–111", color="C1", fontsize=7)
ax.add_patch(Rectangle((67.15 - 12.95, 95.9), 25.9, 24, fill=False, ec="C3", lw=1.2)); ax.text(82, 100, "bumper 25.9×24\ncentre x 67.15, flat y 119.9 (jigs)", color="C3", fontsize=7)
ax.add_patch(Rectangle((47.7, 13), 44, 23.1, fill=False, ec="C2", lw=1.2)); ax.text(93, 20, "stand leg 44×23.1\nx 47.7, y 13 (jigs)", color="C2", fontsize=7)
ax.add_patch(Rectangle((14.15, 119.5), 13.05, 210, fill=True, fc="C0", alpha=0.15, ec="C0")); ax.text(2, 220, "foot 210\ny 119.5–329.5", color="C0", fontsize=7, rotation=90)
for y0 in (190, 308): ax.add_patch(Rectangle((60, y0), 241, 20, fill=True, fc="0.8", alpha=0.5, ec="0.4")); ax.text(70, y0 + 6, "cross bar (tab into the beam)", fontsize=7)
ax.add_patch(Rectangle((23, 0), 315, 12, fill=True, fc="0.7", alpha=0.5, ec="0.4")); ax.text(70, 4, "front bar y 0–12", fontsize=7)
ax.add_patch(Rectangle((20, 140), 26, 194, fill=False, ec="C4", ls=":")); ax.text(21, 250, "channel", color="C4", fontsize=7, rotation=90)
ax.axhline(165, color="r", lw=0.6, ls=":"); ax.text(100, 166, "split y 165 (P7 tab)", color="r", fontsize=7)
ax.set_xlim(0, 140); ax.set_ylim(-5, 340); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm, front at 0)")
ax.set_title("Left sled beam v1 — plan, world coordinates (black: z 345.5; grey: z 339 groove)", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(PARTS, "sled-beam-plan.png"), dpi=110); print("ok")
