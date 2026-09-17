# P2 cup coupon — three conical PSU-foot cups at radial clearances 0.2 / 0.3 / 0.4 on one 96 x 30 x 8 bar, printed in
# the cradle's orientation (cup open to the plate, top face down) with the same HOLE_SHRINK. Black ASA, ~12 g, ~20 min.
# Pass: the foot drops fully into one cup, no rattle sideways, lifts out cleanly. Whichever cup wins sets fit.CUP_CLR
# before the full cradle prints. Engraved "2", "3", "4" beside each cup (reads on the printed top = the bed side).
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import PSU_FOOT_PAD_D, PSU_FOOT_D4, HOLE_SHRINK
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p2")); os.makedirs(OUT, exist_ok=True)

TOP_T, CUP_DEPTH, CUP_LEAD, PITCH = 8.0, 4.0, 1.0, 32.0
bar = cq.Workplane("XY").box(3 * PITCH, 30, TOP_T, centered=(False, False, False))
for i, clr in enumerate((0.2, 0.3, 0.4)):
    cx = PITCH / 2 + i * PITCH; cy = 15.0
    r0 = PSU_FOOT_PAD_D / 2 + clr + HOLE_SHRINK
    r1 = PSU_FOOT_D4 / 2 + clr + HOLE_SHRINK
    bar = bar.cut(cq.Workplane("XY").add(cq.Solid.makeCone(r0, r1, CUP_DEPTH, pnt=cq.Vector(cx, cy, TOP_T - CUP_DEPTH), dir=cq.Vector(0, 0, 1))))
    bar = bar.cut(cq.Workplane("XY").add(cq.Solid.makeCone(r1, r1 + CUP_LEAD, CUP_LEAD, pnt=cq.Vector(cx, cy, TOP_T - CUP_LEAD), dir=cq.Vector(0, 0, 1))))
    bar = bar.faces(">Z").workplane(origin=(cx, cy + 13, TOP_T)).text(str(int(clr * 10)), 4, -0.6, combine="cut")

printable = bar.rotate((0, 0, 0), (1, 0, 0), 180)
bb = printable.val().BoundingBox(); printable = printable.translate((0, -bb.ymin, -bb.zmin))
path = os.path.join(OUT, "p2-cup-coupon.stl")
cq.exporters.export(printable, path, tolerance=0.01, angularTolerance=0.1)
check(path, max_down_frac=0.6)   # the three cup floors are the only downward faces — sacrificial layer handles them
