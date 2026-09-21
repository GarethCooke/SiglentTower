# P1 coupon — sled foot + web + beam rebate (ROADMAP §3). Black ASA (the rib/rebate is a production sliding pair).
#   foot-40:  40 mm of the real T-foot (src/parts/sled_foot.py), printed standing (flange + web edges on the bed). Slide it into the INNER side slot of a
#             2020 offcut: by hand, no rock, can't lift out; the web passes the 3.0 gauge.
#   beam-40:  40 x 39.5 x 9 stub of the sled beam with the closed dovetail groove in its underside, printed FLAT (as the
#             production beam: cups and pockets open upward, the 5.4 groove ceiling is a bridge). Thread it onto the foot's
#             rib from the end: slides, no lift, side play < 0.3. Foot in the rail: beam underside 6.0 (+-0.3) above the rail top.
# v3 (2026-09-19): flange is a T-nut section from the measured slot (mouth 5.9, cavity 10.6, throat at 4.45, bottom 6.5 at 6.15).
# v2 (2026-09-19): web moved to x 22.2 so the beam keeps a 1.5 outer wall and the groove is closed; v1 had an open rebate
# that forced the beam top-face-down. The v1 foot still tests the slot fit; only the rib/groove pair changed.
# v5 (2026-09-21): foot-40 re-exported at SLOT_CLR 0.3 (P1 v4 winner) for the ABS+ confirm — black ABS+, standing, no brim on the flange.
# Pass sets SLOT_FOOT_W / SLOT_LIP_T / WEB_T / WEB_RIB_CLR in fit.py. Output: coupons/p1/*.stl and p1-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.sled_foot import foot, beam_groove
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p1")); os.makedirs(OUT, exist_ok=True)
L, BW, BT = 40.0, 39.5, 9.0

pieces = {"foot-40": foot(L)}
pieces["beam-40"] = cq.Workplane("XY").box(L, BW, BT, centered=False).cut(beam_groove(L))   # groove open to the bed, flat print

plate = None; x = 0.0
for name, p in pieces.items():
    bb = p.val().BoundingBox(); p0 = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p0, path, tolerance=0.01, angularTolerance=0.1)
    print(f"{name:8s} {bb.xlen:5.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3")
    placed = p0.translate((0, x, 0)); plate = placed if plate is None else plate.add(placed); x += bb.ylen + 10
cq.exporters.export(plate, os.path.join(OUT, "p1-plate.stl"), tolerance=0.01, angularTolerance=0.1)
check(os.path.join(OUT, "foot-40.stl"), min_rest_frac=0.2, max_down_frac=2.0)   # stands on two narrow edges (brim ok: no fit face on the bed); neck underside = 4.15 bridge (166 % of the rest at 0.3 clr)
check(os.path.join(OUT, "beam-40.stl"), max_down_frac=1.0)                       # groove ceiling = 5.4 mm bridge
