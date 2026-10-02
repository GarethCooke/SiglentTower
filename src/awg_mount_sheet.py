# awg_mount_sheet.py — how the AWG attaches to the frame (parts/awg-mount-sheet.png): a front elevation at the front
# cradle pair (section at y 40) and a plan view at z 245, from the cradle models in parts/awg_cradle.py. Frame coords.
import os, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); PARTS = os.path.normpath(os.path.join(HERE, "..", "parts"))
import cadquery as cq, trimesh
from parts.awg_cradle import left_cradle, right_bracket, Z_RAIL_TOP, BODY_L, BODY_R

def section(solid, dx, dy, plane, level):
    tmp = os.path.join("/tmp", "awg_sec.stl"); cq.exporters.export(solid.translate((dx, dy, 0)), tmp, tolerance=0.05)
    m = trimesh.load(tmp)
    s = m.section(plane_origin=[0, level, 0] if plane == "y" else [0, 0, level], plane_normal=[0, 1, 0] if plane == "y" else [0, 0, 1])
    out = []
    if s is None: return out
    for ent in s.entities:
        pts = s.vertices[ent.points]; out.append(pts[:, [0, 2]] if plane == "y" else pts[:, [0, 1]])
    return out

L, R = left_cradle(), right_bracket()
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(11, 12), gridspec_kw={"height_ratios": [1, 1.3]})
# ---- front elevation, section y 40 (through the front cradles) ----
for x0 in (0, 251, 341): ax.add_patch(Rectangle((x0, 227.5), 20, 20, fc="0.55", ec="k"))          # AWG rails: left, inner, right (end-on)
ax.text(2, 230, "left AWG\nrail", fontsize=7, color="w"); ax.text(253, 230, "inner\nAWG rail", fontsize=7, color="w"); ax.text(343, 230, "right\nAWG rail", fontsize=7, color="w")
ax.add_patch(Rectangle((0, 180), 20, 100, fc="none", ec="0.6", ls=":")); ax.add_patch(Rectangle((341, 180), 20, 100, fc="none", ec="0.6", ls=":"))
ax.add_patch(Rectangle((251, 68), 20, 179.5, fc="0.8", ec="0.4")); ax.text(254, 150, "inner upright", fontsize=7, rotation=90)
for poly in section(L, 0, 20, "y", 40): ax.add_patch(Polygon(poly, closed=True, fc="C0", alpha=0.5, ec="C0"))
for poly in section(R, 0, 23, "y", 40): ax.add_patch(Polygon(poly, closed=True, fc="C0", alpha=0.5, ec="C0"))
for x0 in (BODY_L + 0.5 + 0.2, BODY_R - 20 - 0.2): ax.add_patch(Rectangle((x0, 246), 20, 5.5, fc="C9", ec="C0"))   # pads
ax.add_patch(Rectangle((BODY_L, 251.5), BODY_R - BODY_L, 82, fc="#f3eedc", ec="k")); ax.text(100, 290, "AWG body 26.5–233.5, bottom at z 251.5 (on the pads)", fontsize=8)
ax.add_patch(Rectangle((23, 248), 214, 3.5, fc="none", ec="k", ls="--")); ax.text(60, 243.2, "front bezel 23–237 hangs 3.5 below the body (dashed) — ahead of the cradles, y < 20", fontsize=7)
ax.annotate("left cradle: saddle over the rail,\n2 × M5×10 down into the TOP slot;\ninboard lip 0.5 off the body = side stop",
            (10, 255.5), (-2, 300), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.annotate("arm 8 thick, top flush with the rail top (247.5),\npad pocket 20.4 × 1.5; TPU pad 5.5 → body sits 4 up",
            (40, 243), (60, 215), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.annotate("right bracket: 10 mm plate on the inner rail's\nLEFT face, 2 × M5 horizontal into its SIDE slot\n(z 237.5); arm reaches 20 under the body",
            (246, 237.5), (150, 200), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.annotate("vent channel: nothing beside the body\nabove z 247.5 within 3.5 of it", (240, 290), (280, 300), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.set_xlim(-10, 371); ax.set_ylim(180, 340); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_xlabel("x (mm, from the left upright's outer face)"); ax.set_ylabel("z (mm)")
ax.set_title("AWG mounting — front elevation, section at y 40 (through the front cradle pair)", fontsize=9)
# ---- plan at z 245 ----
ax2.add_patch(Rectangle((0, 20), 20, 310, fc="0.55", ec="k")); ax2.add_patch(Rectangle((251, 23), 20, 307, fc="0.55", ec="k")); ax2.add_patch(Rectangle((341, 20), 20, 310, fc="0.55", ec="k"))
ax2.text(3, 170, "left AWG rail (top slot: cradle bolts)", fontsize=7, rotation=90, color="w"); ax2.text(254, 120, "inner AWG rail (left-face slot: bracket bolts)", fontsize=7, rotation=90, color="w")
for dy in (20, 223):
    for poly in section(L, 0, dy, "z", 245): ax2.add_patch(Polygon(poly, closed=True, fc="C0", alpha=0.5, ec="C0"))
for dy in (23, 223):
    for poly in section(R, 0, dy, "z", 245): ax2.add_patch(Polygon(poly, closed=True, fc="C0", alpha=0.5, ec="C0"))
ax2.add_patch(Rectangle((BODY_L, 3), BODY_R - BODY_L, 260, fc="#f3eedc", alpha=0.6, ec="k")); ax2.text(80, 140, "AWG body 207 × 260 (y 3–263)", fontsize=8)
ax2.add_patch(Rectangle((23, 0), 214, 3, fc="none", ec="k", ls="--")); ax2.text(90, -9, "bezel, flush with the front plane", fontsize=7)
for (x0, y0) in ((27.2, 30), (27.2, 233), (213.3, 33), (213.3, 233)): ax2.add_patch(Rectangle((x0, y0), 20, 20, fc="C9", ec="C0"))
ax2.text(60, 32, "front pads: bezel stops against the front arms\n(fore-aft stop)", fontsize=7); ax2.text(60, 240, "rear pads carry a rear lip (rear stop)", fontsize=7)
ax2.text(30, 300, "all four pads carry an outer lip (side stop); nothing bolts to the AWG — it lifts straight out", fontsize=7)
ax2.add_patch(Rectangle((242, 81), 10, 90, fc="none", ec="C3", ls=":")); ax2.text(222, 176, "fan vent Ø80 (y 86–166) — kept clear", fontsize=7, color="C3")
ax2.set_xlim(-10, 371); ax2.set_ylim(-14, 340); ax2.set_aspect("equal"); ax2.grid(True, lw=0.3); ax2.set_xlabel("x (mm)"); ax2.set_ylabel("y (mm, front plane at 0)")
ax2.set_title("AWG mounting — plan at z 245 (rails, four cradles, pads)", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(PARTS, "awg-mount-sheet.png"), dpi=110); print("ok")
