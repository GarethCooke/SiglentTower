# publish_plates_sheet.py — draws publish/plates-sheet.png: every plate of publish/SiglentTower-complete.3mf from above,
# each object's footprint (the convex hull of its mesh, placed by its own transform in the file) with its name, so the
# layout can be checked without opening Bambu Studio. Reads the .3mf back rather than the plan, so it checks the file.
# Run after src/publish_3mf.py:  python src/publish_plates_sheet.py
import os, math, zipfile, xml.etree.ElementTree as ET
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F3MF = os.path.join(ROOT, "publish", "SiglentTower-complete.3mf")
OUT = os.path.join(ROOT, "publish", "plates-sheet.png")
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02", "p": "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"}
BED, STRIDE = 256.0, 256.0 * 1.2
SLOT = {"1": "#111111", "2": "#1e3a8a", "3": "#333333", "4": "#8a93a0", "5": "#2f80ed"}

def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def main():
    zf = zipfile.ZipFile(F3MF)
    root = ET.fromstring(zf.read("3D/3dmodel.model"))
    comps = {o.get("id"): [(c.get("{%s}path" % NS["p"]), c.get("objectid")) for c in o.find("m:components", NS)] for o in root.find("m:resources", NS)}
    items = {it.get("objectid"): list(map(float, it.get("transform").split())) for it in root.find("m:build", NS)}
    cache = {}
    def verts(path, mid):
        if (path, mid) not in cache:
            r = ET.fromstring(zf.read(path.lstrip("/")))
            for o in r.find("m:resources", NS):
                cache[(path, o.get("id"))] = [(float(v.get("x")), float(v.get("y"))) for v in o.find("m:mesh", NS).find("m:vertices", NS)]
        return cache[(path, mid)]
    ms = ET.fromstring(zf.read("Metadata/model_settings.config"))
    names, slots = {}, {}
    for o in ms.findall("object"):
        names[o.get("id")] = o.find("metadata[@key='name']").get("value"); slots[o.get("id")] = o.find("metadata[@key='extruder']").get("value")
    plates = ms.findall("plate"); n = len(plates); cols = math.ceil(math.sqrt(n)); rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.4 * rows))
    for pl, ax in zip(plates, axes.flat):
        pid = int(pl.find("metadata[@key='plater_id']").get("value")); pname = pl.find("metadata[@key='plater_name']").get("value")
        ox, oy = ((pid - 1) % cols) * STRIDE, -((pid - 1) // cols) * STRIDE
        ax.set_xlim(-4, BED + 4); ax.set_ylim(-4, BED + 4); ax.set_aspect("equal"); ax.set_xticks([0, 128, 256]); ax.set_yticks([0, 128, 256]); ax.tick_params(labelsize=6)
        ax.add_patch(Rectangle((0, 0), BED, BED, fill=False, lw=1.2, color="#444"))
        ax.set_title(pname, fontsize=6.5, loc="left", wrap=True)
        for mi in pl.findall("model_instance"):
            oid = mi.find("metadata[@key='object_id']").get("value"); t = items[oid]
            pts = [(v[0] * t[0] + v[1] * t[3] + t[9] - ox, v[0] * t[1] + v[1] * t[4] + t[10] - oy) for path, mid in comps[oid] for v in verts(path, mid)]
            h = hull(pts); col = SLOT.get(slots[oid], "#888")
            ax.add_patch(MplPolygon(h, closed=True, facecolor=col, alpha=0.55, edgecolor="#000", lw=0.5))
            cx = sum(p[0] for p in h) / len(h); cy = sum(p[1] for p in h) / len(h)
            ax.text(cx, cy, names[oid].replace(".stl", ""), fontsize=4.5, ha="center", va="center", color="#fff" if slots[oid] in ("1", "2", "3") else "#111")
    for ax in list(axes.flat)[n:]: ax.axis("off")
    fig.suptitle("SiglentTower-complete.3mf — the plates, from above (read back from the file; colours = filament slot)", fontsize=11)
    plt.tight_layout(rect=(0, 0, 1, 0.985)); plt.savefig(OUT, dpi=110); print(OUT)

if __name__ == "__main__":
    main()
