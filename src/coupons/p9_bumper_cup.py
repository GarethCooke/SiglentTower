# P9 coupon — scope rear-bumper cup and front-stand pocket (ROADMAP §3). Yellow PETG. Needs only the scope.
#   cup-pad:   40 x 40 x 9 with the Ø(32 + 2*BUMPER_CUP_CLR) x 5 cup — bumper drops in, locates, no rattle, lifts out.
#   stand-pad: 52 x 51 x 9 with the (44 + 2*STAND_CLR) x (43 + 2*STAND_CLR) x 2.5 pocket — folded front stand sits in it flat.
# Both are sections of the sled beam's top face and print as the beam does: FLAT, pockets open upward, no overhangs.
# Output: coupons/p9/*.stl + p9-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import BUMPER_CUP_CLR, STAND_POCKET_D, STAND_CLR
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p9")); os.makedirs(OUT, exist_ok=True)
T = 9.0
cup_d = 32.0 + 2 * BUMPER_CUP_CLR
cup = cq.Workplane("XY").box(40, 40, T, centered=(True, True, False)).faces(">Z").workplane().hole(cup_d, 5.0)
sw, sd = 44.0 + 2 * STAND_CLR, 43.0 + 2 * STAND_CLR
stand = cq.Workplane("XY").box(52, 51, T, centered=(True, True, False)).faces(">Z").workplane().rect(sw, sd).cutBlind(-STAND_POCKET_D)
pieces = {"cup-pad": cup, "stand-pad": stand}
plate = None; x = 0.0
for name, p in pieces.items():
    bb = p.val().BoundingBox(); p0 = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p0, path, tolerance=0.01, angularTolerance=0.1)
    check(path)
    placed = p0.translate((x, 0, 0)); plate = placed if plate is None else plate.add(placed); x += bb.xlen + 10
cq.exporters.export(plate, os.path.join(OUT, "p9-plate.stl"), tolerance=0.01, angularTolerance=0.1)
print(f"cup Ø{cup_d} x 5, stand pocket {sw} x {sd} x {STAND_POCKET_D}")
