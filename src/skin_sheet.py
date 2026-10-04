# skin_sheet.py — where every side tile goes and where its clip fingers land (parts/tiles/skin-sheet.png). Left side and
# right side elevations in frame coordinates (y rearward, z up), rails as grey bands, tiles as outlines, fingers as dark
# bars on the rail centrelines (section 2 mm behind the tile's back face = through the fingers), windows hatched.
import os, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "parts"))
import cadquery as cq, trimesh
from parts.side_tile import production, CENTRELINES, BANDS, band_height, TILE_L
P = production()
RAILS = [(10, "base"), (78, "PSU"), (237.5, "AWG"), (321, "scope"), (500, "top")]
# placement: (tile name, side, frame y of local y=0, direction, band)
PLACE = {"L": [("tile-band1", 20, +1, 1), ("tile-band1", 175, +1, 1), ("tile-band2-LF", 20, +1, 2), ("tile-band2-LR", 175, +1, 2),
               ("tile-band3-LF", 20, +1, 3), ("tile-band3-LR", 175, +1, 3)],
         "R": [("tile-band1", 175, -1, 1), ("tile-band1", 330, -1, 1), ("tile-band2-RF", 175, -1, 2), ("tile-band2-RR", 330, -1, 2),
               ("tile-band3-RF", 175, -1, 3), ("tile-band3-RR", 330, -1, 3)]}
def secs(solid, x):
    tmp = "/tmp/t.stl"; cq.exporters.export(solid, tmp, tolerance=0.05); m = trimesh.load(tmp)
    s = m.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
    return [] if s is None else [s.vertices[e.points][:, [1, 2]] for e in s.entities]
cache = {n: (secs(t, -1.5), secs(t, 2.0)) for n, t in P.items()}
fig, axes = plt.subplots(1, 2, figsize=(16, 9))
for ax, side in zip(axes, ("L", "R")):
    for zc, name in RAILS:
        ax.add_patch(Rectangle((20, zc - 10), 310, 20, fc="0.75", ec="0.4")); ax.text(332, zc - 3, f"{name} rail", fontsize=7)
    for name, y0, d, band in PLACE[side]:
        zlo = CENTRELINES[BANDS[band][0]]
        plate, fingers = cache[name]
        for p in plate:
            ax.add_patch(Polygon([(y0 + d * yy, zlo + zz) for yy, zz in p], closed=True, fc="none", ec="k", lw=0.7))
        for p in fingers:
            ax.add_patch(Polygon([(y0 + d * yy, zlo + zz) for yy, zz in p], closed=True, fc="C3", ec="C3", lw=0.5))
        ax.text(y0 + d * 77, zlo + band_height(band) / 2, name.replace("tile-", ""), ha="center", va="center", fontsize=8, color="0.3")
    ax.text(22, 540, "red = clip fingers (the pegs on their free ends go into the rail's outer slot); black = tile outline and windows; grey = rails (slot centreline mid-band)", fontsize=7)
    ax.text(22, 525, "front tiles y 20–175, rear tiles 175–330; right-side tiles are the left ones turned 180° about vertical (their local y runs rearward)" if side == "R" else
            "front tiles y 20–175, rear tiles 175–330; band 4 (above the scope rail) not modelled yet", fontsize=7)
    ax.set_xlim(0, 360); ax.set_ylim(-5, 550); ax.set_aspect("equal"); ax.grid(True, lw=0.3)
    ax.set_xlabel("y (mm, front at 0)"); ax.set_ylabel("z (mm)"); ax.set_title(f"{'Left' if side == 'L' else 'Right'} side, seen from outside — tiles A–F as printed", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(HERE, "..", "parts", "tiles", "skin-sheet.png"), dpi=100); print("ok")
