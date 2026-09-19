# P6 coupon — pull insert, 60 mm wide (production: 100 bottom drawer, 40 column, 16 slot, 120 x 6 sled bar), plus a 3 mm
# facia stub with the matching top-edge notch to glue it into.
#   pull-60:   face 60 x (H + 2) x 3 with a 40 x OPEN slot 4 up from the bottom, 5 mm hook strip above it, pocket 17 deep
#              behind, floor rising at 30°, walls 2. Printed FACE DOWN (front on the textured plate): end walls and the
#              leaning floor are walls, the back wall bridges 7 mm. No support anywhere.
#   facia-80:  80 x 45 x 3 facia section standing on its bottom edge (D3) with the (60.3 x H + 2.15) notch in its top edge.
# v1 (OPEN 10): fit PASS 2026-09-19 — insert drops into the notch flush front and top. Slot too small for a thick finger.
# v2: two inserts at OPEN 12 / 14, each with its own stub (the notch deepens with the insert). Pick by finger. Winner sets
# JPULL_OPEN_H. 14 is the ceiling: the pocket's back wall is a bridge in the face-down print, OPEN + hook + wall - floor
# rise = 11.2 at 14 and 13.2 at 16, and rule 4 caps bridges at 12. Production inserts print in the blue PETG
# of the logo inlay (HANDOVER §8 "pull recesses") — the texture difference from the face-down print is meant to show.
# Output: coupons/p6/pull-60-oN.stl + facia-80-oN.stl per N, and p6-v2-plate.stl (all six, flat on one bed).
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import JPULL_OPEN_H, JPULL_HOOK, JPULL_DEPTH, JPULL_FLOOR_DEG, JPULL_WALL, JPULL_INSERT_CLR
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p6")); os.makedirs(OUT, exist_ok=True)

W, FACE_T, SLOT_W, SLOT_Z = 60.0, 3.0, 40.0, 4.0            # insert width, face thickness, slot width, slot bottom above the insert bottom
FW, FH = 80.0, 45.0                                          # facia stub
w, d = JPULL_WALL, JPULL_DEPTH; t = math.tan(math.radians(JPULL_FLOOR_DEG))

def prism(pts, x0, x1):
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))

def insert(open_h):
    """The pull insert, face at y = 0, bottom at z = 0, as used. Returns (solid, H) with H the cavity top."""
    H = SLOT_Z + open_h + JPULL_HOOK
    z_floor = SLOT_Z - w
    cav = [(FACE_T, z_floor), (FACE_T + d, z_floor + d * t), (FACE_T + d, H), (FACE_T, H)]
    outer = [(FACE_T, z_floor - w), (FACE_T + d + w, z_floor - w + (d + w) * t), (FACE_T + d + w, H + w), (FACE_T, H + w)]
    face = cq.Workplane("XY").box(W, FACE_T, H + w, centered=False)
    slot = cq.Workplane("XY").box(SLOT_W, FACE_T + 2, open_h, centered=False).translate(((W - SLOT_W) / 2, -1, SLOT_Z))
    box = prism(outer, (W - SLOT_W) / 2 - w, (W + SLOT_W) / 2 + w)
    cavity = prism(cav, (W - SLOT_W) / 2, (W + SLOT_W) / 2)
    return face.union(box, clean=True).cut(slot).cut(cavity).clean(), H

def insert_printable(open_h):
    s, H = insert(open_h)
    p = s.rotate((0, 0, 0), (1, 0, 0), 90)                   # face down: y -> z
    bb = p.val().BoundingBox(); return p.translate((-bb.xmin, -bb.ymin, -bb.zmin)), H

def facia_stub(H):
    c = JPULL_INSERT_CLR
    f = cq.Workplane("XY").box(FW, FACE_T, FH, centered=False)
    notch = cq.Workplane("XY").box(W + 2 * c, FACE_T + 2, H + w + c + 1, centered=False).translate(((FW - W) / 2 - c, -1, FH - H - w - c))
    return f.cut(notch)

def stamp(part, x, y, text):
    """Deboss a label 0.6 deep into the top face (z max) of a printable part."""
    zt = part.val().BoundingBox().zmax
    return part.cut(cq.Workplane("XY").workplane(offset=zt - 0.6).center(x, y).text(text, 4.0, 1.6, combine=False, halign="center", valign="center"))

if __name__ == "__main__":
    plate = None; x = 0.0
    for open_h in (12.0, 14.0):
        tag = f"o{open_h:.0f}"
        ins, H = insert_printable(open_h)
        ins = stamp(ins, W / 2, FACE_T + d + w - 4, tag)                            # on the pocket's back wall top (print top)
        p = os.path.join(OUT, f"pull-60-{tag}.stl"); cq.exporters.export(ins, p, tolerance=0.01, angularTolerance=0.1); check(p, max_down_frac=0.5)
        st = facia_stub(H)
        st = st.cut(cq.Workplane("XZ", origin=(FW / 2, 0, 10)).text(tag, 6.0, -0.6, combine=False, halign="center", valign="center"))   # deboss on the front face, below the notch
        p2 = os.path.join(OUT, f"facia-80-{tag}.stl"); cq.exporters.export(st, p2, tolerance=0.01, angularTolerance=0.1); check(p2, min_rest_frac=0.1)
        print(f"{tag}: insert {W} x {H + w:.0f} x {FACE_T + d + w:.0f}, slot {SLOT_W} x {open_h:.0f}, hook {JPULL_HOOK}; notch {W + 2*JPULL_INSERT_CLR} x {H + w + JPULL_INSERT_CLR:.2f}")
        bi = ins.val().BoundingBox(); bs = st.val().BoundingBox()
        for part in (ins.translate((x, 0, 0)), st.translate((x + bi.xlen + 8, 0, 0))):
            plate = part if plate is None else plate.add(part)
        x += bi.xlen + bs.xlen + 16
    cq.exporters.export(plate, os.path.join(OUT, "p6-v2-plate.stl"), tolerance=0.01, angularTolerance=0.1)
    print(f"v1 (OPEN {JPULL_OPEN_H:.0f}) files pull-60.stl / facia-80.stl are the passed fit coupon; v2 plate is the slot-height round")
