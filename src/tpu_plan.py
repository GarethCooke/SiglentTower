# Check sheet for the TPU plate: the plate as laid out (top view of the exported STL), the slot-cover section in the 2020
# slot, the right AWG pad on its bracket beside the body, and the frame foot.  python src/tpu_plan.py -> parts/tpu/tpu-plate-plan.png
import os, sys, json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parts import tpu_parts as t
import parts.awg_cradle as ac
from fit import SLOT_MOUTH, SLOT_LIP_T, SLOT_CAVITY_W, SLOT_THROAT_D, SLOT_DEPTH, SLOT_BOTTOM_W
OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "parts", "tpu"))
meta = json.load(open(os.path.join(OUT, "tpu-plate-layout.json")))

fig = plt.figure(figsize=(16, 11)); gs = fig.add_gridspec(2, 3, height_ratios=[1.25, 1])
a = fig.add_subplot(gs[0, :]); a.set_title("tpu-plate-v1 — 240 × 136 on the 256 bed, blue TPU, everything flat as exported (top view)"); a.set_aspect("equal")
m = trimesh.load(os.path.join(OUT, "tpu-plate-v1.stl"))
up = m.face_normals[:, 2] > 0.5
from matplotlib.collections import PolyCollection
a.add_collection(PolyCollection(m.triangles[up][:, :, :2], facecolors="#2d6cdf", edgecolors="none", alpha=1.0))
a.add_patch(plt.Rectangle((-8, -8), 256, 256, fc="none", ec="#999", ls="--")); a.text(-6, 152, "256 × 256 bed (dashed)", fontsize=8, color="#666", va="top")
labels = {"slot-cover-240-v1": "slot cover 240, flare 7.4 — ×6 (1.44 m; cut to length)", "spigots-sweep-v1": "spigot sweep 4.2 / 4.6 / 5.0 / 5.4 — test in an upright's bottom bore",
          "cover-sweep-7.0-v1": "cover sweep 7.0", "cover-sweep-7.4-v1": "cover sweep 7.4", "cover-sweep-8.0-v1": "cover sweep 8.0",
          "sled-stop-cap-v1": "sled stop caps ×2 (8 mm of cover)", "frame-foot-v1": "frame feet ×4, spigot Ø4.6",
          "awg-pad-left-v1": "AWG pads LEFT ×2 (plain)", "awg-pad-right-v1": "AWG pads RIGHT ×2 (standing, lip up)"}
for name, pos in meta["layout"].items():
    x, y = pos[-1]; w, h = meta["dims"][name][:2]
    if name == "awg-pad-right-v1": a.annotate(labels[name], (x + w / 2, y), (x + w / 2, y - 6), ha="center", fontsize=7.5, color="#222")
    else: a.annotate(labels[name], (x + w / 2, y + h), (x + w / 2, y + h + 3), ha="center", fontsize=7.5, color="#222")
a.set_xlim(-12, 252); a.set_ylim(-12, 160); a.set_xlabel("bed x (mm)"); a.set_ylabel("bed y (mm)")

b = fig.add_subplot(gs[1, 0]); b.set_title("Slot cover in the 2020 slot (section; rail face at the top)"); b.set_aspect("equal")
hw_m, hw_c, hw_b = SLOT_MOUTH / 2, SLOT_CAVITY_W / 2, SLOT_BOTTOM_W / 2
rail = [(-10, 0), (-hw_m, 0), (-hw_m, -SLOT_LIP_T), (-hw_c, -SLOT_LIP_T), (-hw_c, -SLOT_THROAT_D), (-hw_b, -SLOT_DEPTH), (hw_b, -SLOT_DEPTH),
        (hw_c, -SLOT_THROAT_D), (hw_c, -SLOT_LIP_T), (hw_m, -SLOT_LIP_T), (hw_m, 0), (10, 0), (10, -12), (-10, -12)]
b.add_patch(plt.Polygon(rail, fc="#bbb", ec="k", label="2020 rail (slot as measured)"))
fh = t.flare_h(t.COVER_FLARE_W); hw_h, hw_f = t.COVER_HEAD_W / 2, t.COVER_FLARE_W / 2
cov = [(-hw_h, 0), (hw_h, 0), (hw_h, -SLOT_LIP_T), (hw_f, -SLOT_LIP_T), (hw_f - fh, -SLOT_LIP_T - fh), (-(hw_f - fh), -SLOT_LIP_T - fh), (-hw_f, -SLOT_LIP_T), (-hw_h, -SLOT_LIP_T)]
b.add_patch(plt.Polygon(cov, fc="#2d6cdf", ec="k", label=f"cover: head {t.COVER_HEAD_W} × {SLOT_LIP_T}, flare {t.COVER_FLARE_W}"))
b.add_patch(plt.Circle((0, -SLOT_DEPTH + 1.5), 1.5, fc="#e8b04b", ec="k", label="Ø3 cable"))
b.annotate(f"{fh:.2f} step under each lip", (hw_f, -SLOT_LIP_T), (6, -4.5), arrowprops=dict(arrowstyle="->"), fontsize=8)
b.annotate(f"{t.CABLE_DEPTH:.2f} for cable under the cover", (0, -SLOT_LIP_T - fh), (-9.5, -9.5), arrowprops=dict(arrowstyle="->"), fontsize=8)
b.text(0, 1.0, "flush with the rail face", ha="center", fontsize=8)
b.set_xlim(-10, 10); b.set_ylim(-12, 3); b.legend(loc="lower right", fontsize=7); b.set_xlabel("across the slot (mm)"); b.set_ylabel("depth (mm)")

c = fig.add_subplot(gs[1, 1]); c.set_title("Right AWG pad on its bracket (section across, front cradle)"); c.set_aspect("equal")
x0 = ac.BODY_R - ac.UNDER - ac.PAD_CLR * 2                                   # pocket x 213.1
c.add_patch(plt.Rectangle((251, 227.5), 20, 20, fc="#999", ec="k", label="inner AWG rail"))
c.add_patch(plt.Rectangle((247, 227.5), 4, 20, fc="#ccc", ec="k", label="bracket plate"))
arm = [(x0 - 0.5, 242.5), (251, 242.5), (251, 247.5), (x0 + 20.4, 247.5), (x0 + 20.4, 246), (x0, 246), (x0, 247.5), (x0 - 0.5, 247.5)]
c.add_patch(plt.Polygon(arm, fc="#ccc", ec="k", label="arm with the 20.4 × 1.5 pocket"))
px = x0 + ac.PAD_CLR
pad = [(px, 246), (px + 20, 246), (px + 20, 247.8), (px + t.TAIL_X1, 247.8), (px + t.TAIL_X1, 253.5), (px + 20 + ac.PAD_CLR + t.LIP_CLR, 253.5),
       (px + 20 + ac.PAD_CLR + t.LIP_CLR, 251.5), (px, 251.5)]
c.add_patch(plt.Polygon(pad, fc="#2d6cdf", ec="k", label="TPU pad + lip"))
c.add_patch(plt.Rectangle((ac.BODY_L, 251.5), ac.BODY_R - ac.BODY_L, 30, fc="#1f2226", ec="k", alpha=0.35, label="AWG body (x to 233.5)"))
c.add_patch(plt.Rectangle((242, 248), 26, 30, fc="none", ec="#999", ls="--", label="mini slot x 242+"))
c.annotate("lip 0.5 off the body", (ac.BODY_R + 0.5, 252.5), (243, 259.5), arrowprops=dict(arrowstyle="->"), fontsize=8)
c.annotate("tail 0.3 above the arm", (px + 22, 247.8), (209, 258.5), arrowprops=dict(arrowstyle="->"), fontsize=8)
c.set_xlim(208, 275); c.set_ylim(226, 262); c.legend(loc="lower left", fontsize=6.5); c.set_xlabel("frame x (mm)"); c.set_ylabel("frame z (mm)")

d = fig.add_subplot(gs[1, 2]); d.set_title("Frame foot (section) and the sled stop cap"); d.set_aspect("equal")
d.add_patch(plt.Rectangle((-12, 0), 24, 6, fc="#2d6cdf", ec="k", label="foot 24 × 24 × 6"))
d.add_patch(plt.Polygon([(-2.3, 6), (2.3, 6), (2.3, 13), (1.3, 14), (-1.3, 14), (-2.3, 13)], fc="#2d6cdf", ec="k"))
d.add_patch(plt.Rectangle((-10, 14), 20, 12, fc="#bbb", ec="k", label="upright (bottom end), Ø~4.2 centre bore"))
d.add_patch(plt.Rectangle((-2.1, 14), 4.2, 12, fc="white", ec="k"))
d.text(-21, -4.5, f"spigot Ø{t.FOOT_SPIGOT_D} × 8, 1 mm lead-in — the sweep decides", ha="left", fontsize=8)
d.text(0, 29, "Stop cap: 8 mm of cover profile pressed into the FRONT end of each\nscope rail's inner slot, against the front upright. The T-foot's\nfront end lands on it at full pull (travel 100 → 92). None at the rear.", ha="center", fontsize=8, va="bottom")
d.set_xlim(-22, 22); d.set_ylim(-7, 42); d.legend(loc="center right", fontsize=6.5); d.set_xticks([]); d.set_yticks([])
plt.tight_layout(); out = os.path.join(OUT, "tpu-plate-plan.png"); plt.savefig(out, dpi=110); print("wrote", out)
