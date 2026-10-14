# Check sheet for the top panel: the plate as laid out (top view of the exported STL), the panel in plan with its four
# tiles, laps and screwed caps, the lap section, and the corner with the cap and M5.  python src/top_plan.py -> parts/top/top-panel-plan.png
import os, sys, json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, trimesh
from matplotlib.collections import PolyCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parts import top_panel as tp
OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "parts", "top"))
meta = json.load(open(os.path.join(OUT, "top-plate-layout.json")))

fig = plt.figure(figsize=(16, 12)); gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.1])

a = fig.add_subplot(gs[0, 0:2]); a.set_aspect("equal")
a.set_title("top-plate-v1 — 246 × 123 on the 256 bed: four tiles STANDING on their front/rear edges (180 tall), four caps (top view)")
m = trimesh.load(os.path.join(OUT, "top-plate-v1.stl"))
up = m.face_normals[:, 2] > 0.5
a.add_collection(PolyCollection(m.triangles[up][:, :, :2], facecolors="#333", edgecolors="none"))
a.add_patch(plt.Rectangle((-5, -5), 256, 256, fc="none", ec="#999", ls="--")); a.text(-3, 150, "256 × 256 bed (dashed)", fontsize=8, color="#666", va="top")
for name, lab in [("top-tile-FL", "FL — front left, stands on its FRONT edge"), ("top-tile-FR", "FR — front right"),
                  ("top-tile-RL", "RL — rear left, stands on its REAR edge"), ("top-tile-RR", "RR — rear right")]:
    x, y = meta["layout"][name][0]; a.text(x + 2, y + 6, lab + "  (black PETG, 94 cm³, brim 15 both sides)", fontsize=8, va="bottom")
x, y = meta["layout"]["upright-cap-v1"][0]; a.text(x, y + 50, "caps ×4\n(dark blue PETG,\nclosed face down,\ncounterbore up)", fontsize=8, va="bottom")
a.set_xlim(-8, 252); a.set_ylim(-8, 160); a.set_xlabel("bed x (mm)"); a.set_ylabel("bed y (mm)")

b = fig.add_subplot(gs[0, 2]); b.set_aspect("equal"); b.set_title("Lap section at a seam (frame z, 1:1 exaggerated ×4)")
k = 4.0   # vertical exaggeration
def rect(ax, x0, x1, z0, z1, **kw): ax.add_patch(plt.Rectangle((x0, z0 * k), x1 - x0, (z1 - z0) * k, **kw))
s = tp.SEAM_X; h = tp.LAP / 2; e = tp.END_CLR / 2
rect(b, s - 30, s - h - e, 0, tp.T, fc="#333", ec="k", label="left / front tile")
rect(b, s - h - e, s + h - e, 0, tp.LOWER_T, fc="#333", ec="k")
rect(b, s + h + e, s + 30, 0, tp.T, fc="#777", ec="k", label="right / rear tile")
rect(b, s - h + e, s + h + e, tp.LOWER_T + tp.GLUE, tp.T, fc="#777", ec="k")
b.annotate(f"lower tongue {tp.LOWER_T} thick, {tp.LAP} wide", (s, tp.LOWER_T / 2 * k), (s - 28, -4), arrowprops=dict(arrowstyle="->"), fontsize=8)
b.annotate(f"upper tongue, {tp.GLUE} glue line under it (CA)", (s, (tp.T + tp.LOWER_T + tp.GLUE) / 2 * k), (s - 2, 18), arrowprops=dict(arrowstyle="->"), fontsize=8)
b.annotate(f"{tp.END_CLR} at each tongue end — the top seam is a hairline", (s - h, tp.T * k), (s - 30, 24), arrowprops=dict(arrowstyle="->"), fontsize=8)
b.text(s, -8, "scope top 507 is 3 mm below the panel — nothing can go under the seam, hence the lap (D4's spline dropped)", ha="center", fontsize=7.5)
b.set_xlim(s - 32, s + 32); b.set_ylim(-11, 30); b.set_yticks([0, tp.LOWER_T * k, tp.T * k]); b.set_yticklabels(["0", f"{tp.LOWER_T}", f"{tp.T}"])
b.legend(loc="upper right", fontsize=7); b.set_xlabel("frame x (mm)"); b.set_ylabel("z above 510 (mm)")

c = fig.add_subplot(gs[1, 0:2]); c.set_aspect("equal"); c.set_title("The panel in plan (from above): four tiles, 10 mm glued half-laps, four M5 corners — on the three top rails and the uprights")
for (x0, x1, y0, y1, col) in [(0, 20, 20, 330, "#bbb"), (341, 361, 20, 330, "#bbb"), (20, 341, 330, 350, "#bbb"),
                              (0, 20, 0, 20, "#999"), (341, 361, 0, 20, "#999"), (0, 20, 330, 350, "#999"), (341, 361, 330, 350, "#999")]:
    c.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fc=col, ec="k", lw=0.5))
c.add_patch(plt.Rectangle((23, 3), 315, 108, fc="#e9e3d3", ec="k", lw=0.5, alpha=0.6)); c.text(180, 57, "scope top at 507 (3 below)", ha="center", fontsize=8, color="#555")
for key, name in tp.NAMES.items():
    (lx, ly), (ux, uy) = tp.regions(*key)
    cx0, cx1, cy0, cy1 = max(lx[0], ux[0]), min(lx[1], ux[1]), max(ly[0], uy[0]), min(ly[1], uy[1])
    col = "#333" if key == (0, 0) else ("#555" if key[0] != key[1] else "#444")
    c.add_patch(plt.Rectangle((lx[0], ly[0]), lx[1] - lx[0], ly[1] - ly[0], fc=col, ec="none", alpha=0.3))   # lower layer
    c.add_patch(plt.Rectangle((ux[0], uy[0]), ux[1] - ux[0], uy[1] - uy[0], fc=col, ec="none", alpha=0.3))   # upper layer
    c.add_patch(plt.Rectangle((cx0, cy0), cx1 - cx0, cy1 - cy0, fc=col, ec="none", alpha=0.3))
    c.text((cx0 + cx1) / 2, (cy0 + cy1) / 2, name[-2:] + f"\n{cx1 - cx0 + tp.LAP:.1f} × {cy1 - cy0 + tp.LAP:.1f}", ha="center", va="center", fontsize=10, color="w")
for xx in (tp.SEAM_X - tp.LAP / 2, tp.SEAM_X + tp.LAP / 2): c.plot([xx, xx], [0, 350], color="#e8b04b", lw=1)
for yy in (tp.SEAM_Y - tp.LAP / 2, tp.SEAM_Y + tp.LAP / 2): c.plot([0, 361], [yy, yy], color="#e8b04b", lw=1)
c.text(tp.SEAM_X + 7, 300, "10 mm lap: left/front tongue UNDER, right/rear OVER, CA", fontsize=8, color="#8a6a1a", rotation=90, va="top")
c.text(100, tp.SEAM_Y + 7, "10 mm lap: front tongue under, rear over", fontsize=8, color="#8a6a1a")
for (cx, cy) in [(10, 10), (351, 10), (10, 340), (351, 340)]:
    c.add_patch(plt.Rectangle((cx - 10, cy - 10), 20, 20, fc="#2d6cdf", ec="k", lw=0.8, alpha=0.9)); c.add_patch(plt.Circle((cx, cy), 2.75, fc="w", ec="k", lw=0.5))
c.annotate("cap 20 × 20 × 6, M5 × 10 button head\ninto the upright's centre bore (self-taps)", (351, 340), (250, 365), arrowprops=dict(arrowstyle="->"), fontsize=8)
c.text(180, -14, "FRONT (no top rail here — the front edge spans free between the uprights, sag ≈ 0.2–0.5 mm)", ha="center", fontsize=8)
c.set_xlim(-10, 372); c.set_ylim(-22, 385); c.set_xlabel("frame x (mm)"); c.set_ylabel("frame y (mm)")

d = fig.add_subplot(gs[1, 2]); d.set_aspect("equal"); d.set_title("Corner, section (frame z): cap on the panel on the upright")
d.add_patch(plt.Rectangle((0, 470), 20, 40, fc="#999", ec="k", label="upright (top at 510)"))
d.add_patch(plt.Rectangle((20, 490), 30, 20, fc="#bbb", ec="k", label="top rail"))
d.add_patch(plt.Rectangle((0, 510), 50, 3, fc="#333", ec="k", label="panel 3 (z 510–513)"))
cap = [(0, 513), (20, 513), (20, 519), (14.75, 519), (14.75, 515), (12.75, 515), (12.75, 513), (7.25, 513), (7.25, 515), (5.25, 515), (5.25, 519), (0, 519)]
d.add_patch(plt.Polygon(cap, fc="#2d6cdf", ec="k", label="cap 20 × 20 × 6, Ø9.5 × 4 counterbore"))
d.add_patch(plt.Rectangle((7.5, 505), 5, 10, fc="#444", ec="k")); d.add_patch(plt.Rectangle((5.75, 515), 8.5, 2.7, fc="#444", ec="k", label="M5 × 10 button head"))
d.add_patch(plt.Rectangle((7.9, 480), 4.2, 30, fc="none", ec="k", ls=":", label="Ø4.2 centre bore")); d.annotate("5 mm of thread in the bore", (10, 507), (24, 500), arrowprops=dict(arrowstyle="->"), fontsize=8)
d.annotate("Ø5.5 hole, a teardrop in the standing print", (10, 511.5), (24, 523), arrowprops=dict(arrowstyle="->"), fontsize=8)
d.set_xlim(-5, 52); d.set_ylim(472, 528); d.legend(loc="lower right", fontsize=6.5); d.set_xlabel("frame x (mm)"); d.set_ylabel("frame z (mm)")

fig.suptitle("Top panel v1 — four standing tiles + four caps on ONE plate (386 cm³, black + dark blue PETG, thin-part settings)", fontsize=13)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "top-panel-plan.png"), dpi=110); print("ok")
