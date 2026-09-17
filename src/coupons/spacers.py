# Rail-height spacer set (ROADMAP 0.4) + the 3.0 mm web gauge. Any PETG, any colour.
# Each spacer is a 20 x 20 bar whose LENGTH is the rail gap: print it lying flat so the critical dimension is in XY
# (XY holds ±0.05; a standing print would quantise 63.5 / 139.5 to the layer height). 2 walls, 10 % infill is plenty.
# Gaps (rail top -> next rail bottom): 48 (20 -> 68), 139.5 (88 -> 227.5), 63.5 (247.5 -> 311), 159 (331 -> 490). Two of each.
# Gauge: 3.0 x 20 x 60 flat — the sled web must pass through the 3 mm gap between upright and AWG frame.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "spacers")); os.makedirs(OUT, exist_ok=True)

def bar(L, w=20.0, h=20.0, label=None):
    b = cq.Workplane("XY").box(L, w, h, centered=False).edges("|X").chamfer(1.0)
    if label:  # engraved length on the top face so the four sizes can't be mixed up
        b = b.faces(">Z").workplane(centerOption="CenterOfBoundBox").text(label, 7, -0.6, combine="cut")
    return b

for L in (48.0, 63.5, 139.5, 159.0):
    cq.exporters.export(bar(L, label=f"{L:g}"), os.path.join(OUT, f"spacer-{L:g}.stl"), tolerance=0.02, angularTolerance=0.2)
cq.exporters.export(cq.Workplane("XY").box(60, 20, 3.0, centered=False), os.path.join(OUT, "gauge-3.0.stl"), tolerance=0.02, angularTolerance=0.2)

# one plate: two of each spacer + the gauge, laid flat with 8 mm gaps
plate = None; y = 0.0
for L in (48.0, 63.5, 139.5, 159.0):
    for k in range(2):
        p = bar(L, label=f"{L:g}").translate((0, y, 0)); plate = p if plate is None else plate.add(p); y += 28
g = cq.Workplane("XY").box(60, 20, 3.0, centered=False).translate((0, y, 0)); plate = plate.add(g)
cq.exporters.export(plate, os.path.join(OUT, "spacers-plate.stl"), tolerance=0.02, angularTolerance=0.2)
print("plate footprint 159 x", y + 20)

# print check (PRINT-RULES.md §1)
from printcheck import check
for f in sorted(os.listdir(OUT)):
    if f.endswith(".stl"): check(os.path.join(OUT, f))
