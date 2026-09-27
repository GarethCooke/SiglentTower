# Addtam strip brackets (D8, HANDOVER §7, ROADMAP Stage 8). v1 2026-09-22; lower bracket v2 2026-09-26.
#
# The 4-way strip hangs VERTICALLY on the rear face of the rear-left upright, cable end down, on two printed brackets
# bolted into that upright's rear slot. Its keyhole slots run across the body, so the keyholes alone cannot hold it
# vertical: the pegs hold it against the frame and the LOWER bracket's shelf takes the weight.
#
# Measured 2026-09-17 (fit.py): keyholes 249.5 c-c, large hole Ø6.5, slot 3.5, nearest keyhole centre 20 from the cable
# end, pocket 6.5 deep behind the back face, body 78.1 wide with the keyhole line 29.2 from one long edge.
# Placement: peg line x 30.2 (the +8 tried in v3 was withdrawn 2026-09-27 — not the problem), strip body
# x 1–79. v4 (2026-09-27): strip bottom z 75 (was 25), pegs at z 95 and 344.5 — its Ø15 mains cable leaves the bottom end on
# the keyhole line and is rigid for 25 mm, so the shelf is a U round it and the strip sits high enough for the cable to bend.
#
# Local frame = the frame's, with y measured from the upright's rear face (frame y 350): plate y 0–PLATE_T, the strip's
# back face resting on it, pegs rising in +y into the keyhole pockets.
#
# Two DIFFERENT brackets (PRINT-RULES 10 — never two of the same): upper is plate + arm + peg; lower adds the shelf.
# The upper is built around its peg, so moving the strip up (v4) did not change its geometry: upper stays v1 (upper v2/v3
# were byte-for-byte the same part and were withdrawn 2026-09-27) — only its bolt height moved, z 294.5 -> 344.5.
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
PEG_X = 1.0 + STRIP_KEYHOLE_OFF                    # 30.2: strip body x 1–79, keyhole line 29.2 from its near edge
ARM_X1 = PEG_X + 4.0
ARM_H = 20.0
PEG_SHAFT_D, PEG_SHAFT_L = 3.2, 3.0
PEG_HEAD_D, PEG_HEAD_L = 6.0, 1.1
PEG_CONE = (PEG_HEAD_D - PEG_SHAFT_D) / 2
STRIP_Z0 = 75.0                                     # v4: was 25 — the mains cable leaves the strip's END on the keyhole line,
                                                    # Ø15, rigid for 25 below the end plate; at 25 it hit the bench. 75 gives
                                                    # 25 rigid + ~25 bend radius above z 25
CABLE_D, CABLE_RIGID = 15.0, 25.0                   # measured 2026-09-27
CABLE_GAP = (PEG_X - 16.0, PEG_X + 16.0)            # shelf U-cut round the cable: Ø15 + 8 of sideways keyhole travel either way
PEG_Z = (STRIP_Z0 + STRIP_KEYHOLE_END, STRIP_Z0 + STRIP_KEYHOLE_END + STRIP_KEYHOLE_PITCH)
SHELF_W, SHELF_D, SHELF_T = 80.0, 30.0, 4.0
SHELF_NOTCH = 10.0                                  # (v1-v3 cable notch at the strip's near edge — wrong place; superseded by CABLE_GAP)
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
        # v2 (2026-09-26): the brace goes UNDER the shelf, where nothing else lives (v1's stood on it, inside the strip's
        # footprint). v4 (2026-09-27): the strip's mains cable comes straight out of its bottom end ON the keyhole line,
        # Ø15 and rigid for 25 mm — v1-v3 put a 10 mm notch at the strip's near edge and a full plate under the cable.
        # The shelf is now a U: two bearing pads (x 0-22.2 and 54.2-80) joined by an 8 mm bridge against the plate,
        # open to the rear round the cable, with room for the 8 mm sideways keyhole travel either way.
        z_sh = STRIP_Z0 - SHELF_T
        body = body.union(box(0.0, PLATE_W, 0.0, PLATE_T, z_sh - GUSSET_H, z0 + 0.01))   # plate runs down to carry the brace
        sh = box(0.0, SHELF_W, 0.0, SHELF_D, z_sh, STRIP_Z0)
        sh = sh.cut(box(CABLE_GAP[0], CABLE_GAP[1], 8.0, SHELF_D + 1, z_sh - 1, STRIP_Z0 + 1))
        body = body.union(sh)
        g = (cq.Workplane("YZ").workplane(offset=0.0)
             .polyline([(PLATE_T, z_sh), (PLATE_T + GUSSET_H, z_sh), (PLATE_T, z_sh - GUSSET_H)])
             .close().extrude(min(PLATE_W, CABLE_GAP[0] - 0.5)))                        # brace stays clear of the cable's drop
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
    parts = {"strip-bracket-upper-v1": bracket(PEG_Z[1], shelf=False),
             "strip-bracket-lower-v4": bracket(PEG_Z[0], shelf=True)}
    for name, b in parts.items():
        p = printable(b)
        bb = p.val().BoundingBox()
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:26s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {p.val().Volume()/1000:5.1f} cm3")
        check(path, min_rest_frac=0.3, max_down_frac=0.2)
