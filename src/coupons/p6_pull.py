# P6 coupon — pull insert, 60 mm wide (production: 100 bottom drawer, 40 column, 16 slot, 120 x 6 sled bar), plus a 3 mm
# facia stub with the matching top-edge notch to glue it into. Yellow PETG.
#   pull-60:   face 60 x 21 x 3 with a 40 x 10 slot 4 up from the bottom, 5 mm hook strip above it, pocket 17 deep behind,
#              floor rising at 30°, walls 2. Printed FACE DOWN (front on the textured plate): end walls and the leaning
#              floor are walls, the back wall bridges 7 mm. No support anywhere.
#   facia-80:  80 x 45 x 3 facia section standing on its bottom edge (D3) with the 60.3 x 21.15 notch in its top edge.
# Pass: insert drops into the notch flush (front and top), fingertip goes in the slot, hooks up behind the strip and
# pulls comfortably; slicer preview shows no support. Sets JPULL_* in fit.py.
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import JPULL_OPEN_H, JPULL_HOOK, JPULL_DEPTH, JPULL_FLOOR_DEG, JPULL_WALL, JPULL_INSERT_CLR
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p6")); os.makedirs(OUT, exist_ok=True)

W, FACE_T, SLOT_W, SLOT_Z = 60.0, 3.0, 40.0, 4.0            # insert width, face thickness, slot width, slot bottom above the insert bottom
w, d = JPULL_WALL, JPULL_DEPTH; t = math.tan(math.radians(JPULL_FLOOR_DEG))
H = SLOT_Z + JPULL_OPEN_H + JPULL_HOOK                       # cavity top (19); insert/notch height = H + wall (21)
z_floor = SLOT_Z - w                                         # cavity floor at the face, 2 below the slot
cav = [(FACE_T, z_floor), (FACE_T + d, z_floor + d * t), (FACE_T + d, H), (FACE_T, H)]
outer = [(FACE_T, z_floor - w), (FACE_T + d + w, z_floor - w + (d + w) * t), (FACE_T + d + w, H + w), (FACE_T, H + w)]
def prism(pts, x0, x1):
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))
face = cq.Workplane("XY").box(W, FACE_T, H + w, centered=False)
slot = cq.Workplane("XY").box(SLOT_W, FACE_T + 2, JPULL_OPEN_H, centered=False).translate(((W - SLOT_W) / 2, -1, SLOT_Z))
box = prism(outer, (W - SLOT_W) / 2 - w, (W + SLOT_W) / 2 + w)
cavity = prism(cav, (W - SLOT_W) / 2, (W + SLOT_W) / 2)
insert = face.union(box, clean=True).cut(slot).cut(cavity).clean()
# print orientation: face down -> rotate so the front face (y = 0) lies on the bed
insert_p = insert.rotate((0, 0, 0), (1, 0, 0), 90)           # y -> z
bb = insert_p.val().BoundingBox(); insert_p = insert_p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
p = os.path.join(OUT, "pull-60.stl"); cq.exporters.export(insert_p, p, tolerance=0.01, angularTolerance=0.1); check(p, max_down_frac=0.5)

# facia stub with the notch (standing on its bottom edge)
FW, FH = 80.0, 45.0; c = JPULL_INSERT_CLR
facia = cq.Workplane("XY").box(FW, FACE_T, FH, centered=False)
notch = cq.Workplane("XY").box(W + 2 * c, FACE_T + 2, H + w + c + 1, centered=False).translate(((FW - W) / 2 - c, -1, FH - H - w - c))
facia = facia.cut(notch)
p = os.path.join(OUT, "facia-80.stl"); cq.exporters.export(facia, p, tolerance=0.01, angularTolerance=0.1); check(p, min_rest_frac=0.1)
print(f"insert {W} x {H + w} x {FACE_T + d + w:.0f}, slot {SLOT_W} x {JPULL_OPEN_H}, hook {JPULL_HOOK}, floor {JPULL_FLOOR_DEG} deg; notch {W + 2*c} x {H + w + c}")
