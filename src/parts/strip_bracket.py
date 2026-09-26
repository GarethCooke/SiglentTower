# Addtam strip brackets (D8, HANDOVER §7, ROADMAP Stage 8). v1 2026-09-22; lower bracket v2 2026-09-26.
#
# The 4-way strip hangs VERTICALLY on the rear face of the rear-left upright, cable end down, on two printed brackets
# bolted into that upright's rear slot. Its keyhole slots run across the body, so the keyholes alone cannot hold it
# vertical: the pegs hold it against the frame and the LOWER bracket's shelf takes the weight.
#
# Measured 2026-09-17 (fit.py): keyholes 249.5 c-c, large hole Ø6.5, slot 3.5, nearest keyhole centre 20 from the cable
# end, pocket 6.5 deep behind the back face, body 78.1 wide with the keyhole line 29.2 from one long edge.
# Placement: peg line x 38.2 (v3, 2026-09-26: the 29.2 was to the keyhole's start, the seat is 8 further in), strip body
# x 1–79, pegs at z 45 and 294.5, strip bottom z 25.
#
# Local frame = the frame's, with y measured from the upright's rear face (frame y 350): plate y 0–PLATE_T, the strip's
# back face resting on it, pegs rising in +y into the keyhole pockets.
#
# Two DIFFERENT brackets (PRINT-RULES 10 — never two of the same): upper is plate + arm + peg; lower adds the shelf.
#
# Deviations from the roadmap's sketch, both deliberate:
#   plate 4 -> 5 mm. A Ø10 counterbore for the M5 head needs 2.5, and 1.5 of plate under it is not enough. At 5 the
#   counterbore leaves 2.5 and an M5x10 still takes 7.5 of T-nut, so no new hardware. The arm matches at 5 so the strip
#   beds on one flat plane.
#   The strip therefore sits at frame y 355–385, not 350–380 — still well inside the 60 behind the frame.
#
# Lower bracket v2 (2026-09-26): v1's 45° gusset stood ON the shelf in front of the plate — inside the strip's own
# footprint — so the strip could not sit down on the shelf (found on the yellow run). The brace is now UNDER the shelf
# and the plate runs down to z 1 to carry it. Rule: a brace goes where nothing else lives; check every print-only
# feature against the part's working envelope (PRINT-RULES).
#
# Print: plate face (y = 0) down, peg rising, shelf coplanar with the plate on the bed. The peg's head is a mushroom, so
# it gets a 45° cone under it (PRINT-RULES rule 4) and needs no support. The counterbore opens upward.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import (STRIP_KEYHOLE_PITCH, STRIP_KEYHOLE_D, STRIP_KEYHOLE_SLOT, STRIP_KEYHOLE_END,
                 STRIP_KEYHOLE_DEPTH, STRIP_BODY_W, STRIP_KEYHOLE_OFF)

PLATE_W, PLATE_H, PLATE_T = 20.0, 40.0, 5.0
BOLT_D, CBORE_D, CBORE_H = 5.5, 10.0, 2.5
PEG_X = 1.0 + STRIP_KEYHOLE_OFF                    # 38.2: strip body x 1–79, seat 37.2 from its near edge (was 30.2 on the 29.2 measure)
ARM_X1 = PEG_X + 4.0
ARM_H = 20.0
PEG_SHAFT_D, PEG_SHAFT_L = 3.2, 3.0
PEG_HEAD_D, PEG_HEAD_L = 6.0, 1.1
PEG_CONE = (PEG_HEAD_D - PEG_SHAFT_D) / 2
STRIP_Z0 = 25.0
PEG_Z = (STRIP_Z0 + STRIP_KEYHOLE_END, STRIP_Z0 + STRIP_KEYHOLE_END + STRIP_KEYHOLE_PITCH)
SHELF_W, SHELF_D, SHELF_T = 80.0, 30.0, 4.0
SHELF_NOTCH = 10.0
GUSSET_H = 20.0
assert PEG_SHAFT_L + PEG_CONE + PEG_HEAD_L <= STRIP_KEYHOLE_DEPTH, "peg deeper than the keyhole pocket"
assert PEG_SHAFT_D < STRIP_KEYHOLE_SLOT and PEG_HEAD_D < STRIP_KEYHOLE_D, "peg will not enter the keyhole"
STRIP_X0 = PEG_X - STRIP_KEYHOLE_OFF
STRIP_X1 = STRIP_X0 + STRIP_BODY_W
assert STRIP_X1 <= 80.0, "strip would overhang the frame"


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def peg(z):
    """Shaft, 45° cone, head — rising in +y from the plate's outer face."""
    y0 = PLATE_T
    wp = cq.Workplane("XZ").workplane(offset=-y0)
    shaft = wp.center(PEG_X, z).circle(PEG_SHAFT_D / 2).extrude(-PEG_SHAFT_L)
    cone = cq.Workplane("XY").add(cq.Solid.makeCone(
        PEG_SHAFT_D / 2, PEG_HEAD_D / 2, PEG_CONE,
        pnt=cq.Vector(PEG_X, y0 + PEG_SHAFT_L, z), dir=cq.Vector(0, 1, 0)))
    head = (cq.Workplane("XZ").workplane(offset=-(y0 + PEG_SHAFT_L + PEG_CONE))
            .center(PEG_X, z).circle(PEG_HEAD_D / 2).extrude(-PEG_HEAD_L))
    return shaft.union(cone).union(head)


def bracket(peg_z, shelf=False):
    z0 = peg_z - PLATE_H / 2
    body = box(0.0, PLATE_W, 0.0, PLATE_T, z0, z0 + PLATE_H)
    body = body.union(box(PLATE_W, ARM_X1, 0.0, PLATE_T, peg_z - ARM_H / 2, peg_z + ARM_H / 2))
    body = body.union(peg(peg_z))
    hole = (cq.Workplane("XZ").workplane(offset=-PLATE_T - 1).center(PLATE_W / 2, peg_z)
            .circle(BOLT_D / 2).extrude(-(PLATE_T + 2)))
    cb = (cq.Workplane("XZ").workplane(offset=-PLATE_T - 1).center(PLATE_W / 2, peg_z)
          .circle(CBORE_D / 2).extrude(-(CBORE_H + 1)))
    body = body.cut(hole).cut(cb)
    if shelf:
        # v2 2026-09-26: v1's gusset stood ON the shelf, in front of the plate — i.e. inside the strip's own footprint
        # (x 1–79, y 5–35, z 25 up): 3.9 cm3 of clash, the strip could not sit down (Gareth, on the yellow run). The
        # brace now lives UNDER the shelf, where nothing else is, and the plate runs down to z 1 to anchor it.
        body = body.union(box(0.0, PLATE_W, 0.0, PLATE_T, 1.0, z0 + 0.01))          # plate extended down to z 1
        sh = box(0.0, SHELF_W, 0.0, SHELF_D, STRIP_Z0 - SHELF_T, STRIP_Z0)
        sh = sh.cut(box(STRIP_X0, STRIP_X0 + SHELF_NOTCH, -1.0, SHELF_D + 1, STRIP_Z0 - SHELF_T - 1, STRIP_Z0 + 1))
        body = body.union(sh)
        g = (cq.Workplane("YZ").workplane(offset=0.0)
             .polyline([(PLATE_T, STRIP_Z0 - SHELF_T), (PLATE_T + GUSSET_H, STRIP_Z0 - SHELF_T), (PLATE_T, STRIP_Z0 - SHELF_T - GUSSET_H)])
             .close().extrude(PLATE_W))
        body = body.union(g)
    return body


def printable(b):
    """Plate face down: +y becomes +z, so the peg rises and the counterbore opens upward."""
    p = b.rotate((0, 0, 0), (1, 0, 0), 90)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(HERE, ".."))
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    parts = {"strip-bracket-upper-v2": bracket(PEG_Z[1], shelf=False),
             "strip-bracket-lower-v3": bracket(PEG_Z[0], shelf=True)}
    for name, b in parts.items():
        p = printable(b)
        bb = p.val().BoundingBox()
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:26s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {p.val().Volume()/1000:5.1f} cm3")
        check(path, min_rest_frac=0.3, max_down_frac=0.2)
