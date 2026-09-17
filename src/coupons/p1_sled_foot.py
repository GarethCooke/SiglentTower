# P1 coupon — sled foot + web + beam rebate (ROADMAP §3). Black ASA (the rib/rebate is a production sliding pair).
#   foot-40:  40 mm of the real T-foot (src/parts/sled_foot.py), printed standing (flange + web edges on the bed). Slide it into the INNER side slot of a
#             2020 offcut: by hand, no rock, can't lift out; the web passes the 3.0 gauge.
#   beam-40:  40 x 39.5 x 9 stub of the sled beam with the rib rebate on its outer edge, printed TOP FACE DOWN (as the
#             production beam will be, cups to the plate). Thread it onto the foot's rib from the end: slides, no lift,
#             side play < 0.3. With the foot in the rail: beam underside sits 6.0 (+-0.3) above the rail's top face.
# Pass sets SLOT_FOOT_W / SLOT_LIP_T / WEB_T / WEB_RIB_CLR in fit.py. Output: coupons/p1/*.stl and p1-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.sled_foot import foot, beam_rebate
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p1")); os.makedirs(OUT, exist_ok=True)
L, BW, BT = 40.0, 39.5, 9.0

pieces = {"foot-40": foot(L)}
beam = cq.Workplane("XY").box(L, BW, BT, centered=False).cut(beam_rebate(L))          # rebate at the outer edge (Y 0), underside (Z 0)
beam = beam.rotate((0, 0, 0), (1, 0, 0), 180)                                        # top face down: rebate now opens upward
bb = beam.val().BoundingBox(); pieces["beam-40"] = beam.translate((0, -bb.ymin, -bb.zmin))

plate = None; x = 0.0
for name, p in pieces.items():
    bb = p.val().BoundingBox(); p0 = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p0, path, tolerance=0.01, angularTolerance=0.1)
    print(f"{name:8s} {bb.xlen:5.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3")
    placed = p0.translate((0, x, 0)); plate = placed if plate is None else plate.add(placed); x += bb.ylen + 10
cq.exporters.export(plate, os.path.join(OUT, "p1-plate.stl"), tolerance=0.01, angularTolerance=0.1)
for name in pieces: check(os.path.join(OUT, f"{name}.stl"), max_down_frac=0.6)   # foot: the neck underside is a 2.5 mm bridge (flange -> web)
