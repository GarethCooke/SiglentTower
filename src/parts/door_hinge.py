# Door hinge — the two production knuckles (HANDOVER §5, PRINT-RULES §2 "Door hinge knuckles", ROADMAP §3 P5).
# v1 2026-09-22; v2 2026-10-20 BOTH leaves (TILE_Z0 347 -> 338: the door's edge comes down to 7 above the rail; the
# frame leaf's riser moves out to x 364.3 so the lower door clears it). Replaces the P5 v1 coupon, which was a generic block with its bore on the pads' mid-thickness: the two
# leaves could not fold, so the bores sat one pad-thickness apart and the pin would not pass. A butt hinge's axis lies
# OUTSIDE both leaves, and in this frame it has to lie outboard of the door's outer face as well.
#
# Geometry (frame coordinates: x across from the left outer face, y depth from the front, z from the bench):
#   right rails / uprights outer face   x 361          side tiles lie ON it, so the door panel is x 361–364
#   scope rail                          x 341–361, z 311–331, outer-face slot centreline z 321
#   sled band                           z 331–346, left open — nothing outboard of 361 in it
#   door tile                           230 x 143 x 3, y 20–250, z 347–490 (bottom edge 347, box floor 347)
#   HINGE AXIS                          x AXIS_X = 369, z AXIS_Z = 341, running along y
#
# AXIS_X moved 362 -> 369 (2026-09-22). The viewer's 362 was set against tiles drawn on the rail centreline (x 351);
# slot_clip.py puts them on the rail's outer face, so a Ø8 barrel at 362 (x 358–366) sat 3 mm inside the frame face and
# straight through the door panel. At 369 the barrel is x 365–373 — clear of the panel's outer face at 364 — and still
# z 337–345, topping out under the box floor at 347. Swept check: the door's nearest corner (361, 347) is r = 10 from the
# axis, so opening sweeps a 10 mm circle that never drops below z 331 (the scope rail's top); at 180 the door hangs at
# x 374–377, 10 proud of the tile below, which is HANDOVER §5's "hangs ~20 proud" behaviour.
#
# REACH RULE (Gareth, 2026-09-22): neither leaf extends further from the axis than the other. The frame leaf reaches 30
# down (341 -> 311, the rail's bottom); the door leaf therefore reaches 30 up (341 -> 371), so its glue pad is 24 tall
# above the tile's bottom edge, not a full-height strip.
#
# The leaves interleave in y: the DOOR leaf takes the two outer thirds, the FRAME leaf the middle one, AX_CLR apart.
# Everything of one leaf that lives in the other's y-third is cut back to its own thirds — that is why the door's shelf
# runs full length inboard of the panel but only over its own segments outboard of it.
#
# Print (PRINT-RULES §2): STANDING, y vertical, so every bore and both leaves' locating faces are vertical walls. The
# only faces that can float are a segment end that does not start at y = 0; those are coned 45° right in to the bore
# (zero flat area — the cone tip is a ring of zero width, so the slicer simply starts it on the next layer) and the
# shelf's matching end is chamfered 45°. The M5 hole is a teardrop, peak toward +y, because its axis is horizontal in
# the print (rule 4). No support anywhere.
#
# Fixing: frame leaf takes one M5 x 12 + T-nut into the scope rail's OUTER slot at z 321. That slot is shared with the
# side tiles' clips (P4) — check the clip positions against y 23–47 and y 223–247 when the tiles are modelled.
# Door leaf is glued to the tile's inner face; its shelf catches the tile's bottom edge, which locates it in z without
# the 2-pin socket (a 3 mm hex tile is a poor host for blind pin holes, and horizontal pins would overhang).
# Output: parts/hinge-door-v1.stl and parts/hinge-frame-v1.stl, two of each (both are symmetric about their mid-length).
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import PIN_HOLE_D

# ---- frame the hinge sits in ----
FACE_X   = 361.0          # right rails / uprights outer face
PANEL_T  = 3.0            # side tile / door panel thickness -> panel x 361–364
RAIL_Z0, RAIL_Z1 = 311.0, 331.0
SLOT_Z   = 321.0          # scope rail's outer-slot centreline
TILE_Z0  = 338.0          # door panel's bottom edge. v1: 347 (HANDOVER's box floor) left a 16 mm band open under the door.
                          # v2 2026-10-20 (Gareth): 338 — the shelf (335–338) clears the frame plate's top (333) and the right
                          # sled front rest's plate on the rail top (z 331–334, x 341–359, y 21–61, under the FRONT hinge) by
                          # 1; lower than this and the shelf lands on the rest. 7 above the rail, 4 above the fixed tile's edge.

# ---- hinge ----
AXIS_X, AXIS_Z = 369.0, 341.0
BARREL_D = 8.0
KN_L     = 24.0           # knuckle length along y (viewer draws 24)
SEG_DOOR = 6.0            # door takes the two outer segments, frame the long middle one: 6 / 12 / 6, not three 8s.
                          # The middle one has to be long enough for the frame leaf's riser to climb 10 mm at 45°.
AX_CLR   = 0.4            # axial gap between segments
REACH    = 30.0           # each leaf's reach from the axis (RAIL_Z0 = AXIS_Z - REACH)
CONE     = (BARREL_D - PIN_HOLE_D) / 2        # 45° cone on a floating segment end, right in to the bore

# ---- frame leaf ----
PLATE_T  = 6.0            # x 361–367; M5 x 12 leaves 6 in the T-nut
PLATE_Z1 = 333.0          # 2 above the rail's top: still r 8.25 from the axis, so outside the door's swept band, and
                          # it is what gives the standing print a bed face worth the name (6 x 22)
BOLT_D   = 5.5
RISER_X0, RISER_X1 = 364.3, AXIS_X + BARREL_D / 2      # 364.3–373, climbing from the plate's top to the barrel. v2 2026-10-20: was 363 —
                                                       # with the door's edge at 338 its outer face (364) ran into the riser at z 338–341;
                                                       # 364.3 clears it, and the door's swept bottom corner never passes x 364 below z 346
# No full-length arm above the rail: everything the door sweeps through must live in the frame leaf's own y-third.
# The plate itself is safe — its nearest corner (366, 331) is r 10.4 from the axis, outside the door's swept band.

# ---- door leaf ----
PAD_T    = 4.0            # x 357–361, against the panel's inner face
PAD_Z1   = AXIS_Z + REACH                     # 371
SHELF_T  = 3.0            # z 344–347, the panel's bottom edge lands on it
SHELF_Z0 = TILE_Z0 - SHELF_T
PANEL_CLR = 0.15


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def barrel(y0, y1):
    """Barrel segment over y0..y1 on the axis. If it does not start on the bed (y = 0) its lower end is coned 45° right
    in to the bore: zero flat area, so nothing floats — print-down is -y here, not -z."""
    b = (cq.Workplane("XZ").workplane(offset=-y0).center(AXIS_X, AXIS_Z)
         .circle(BARREL_D / 2).extrude(-(y1 - y0)))
    return b.faces("<Y").chamfer(CONE - 0.01) if y0 > 0.01 else b


def ramp_x(x0, x1, y0, y1, z0, z1, ramp):
    """Block [x0,x1] x [y0,y1] x [z0,z1]. `ramp` cuts its y0 end back at 45° in +x, so the end is self-supporting off
    whatever full-length material sits at x <= x0."""
    pts = [(x0, y0), (x1, y0 + (x1 - x0)), (x1, y1), (x0, y1)] if ramp else \
          [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))


def ramp_z(x0, x1, y0, y1, z0, z1, ramp, down=False):
    """Same, ramping in z. `down=False` climbs from z0 (anchored on what is below it); `down=True` hangs from z1. Either
    way each layer steps at most its own height, which is what makes a 45° face self-supporting."""
    h = z1 - z0
    if not ramp:      pts = [(y0, z0), (y0, z1), (y1, z1), (y1, z0)]
    elif not down:    pts = [(y0, z0), (y0 + h, z1), (y1, z1), (y1, z0)]
    else:             pts = [(y0, z1), (y0 + h, z0), (y1, z0), (y1, z1)]
    return cq.Workplane("YZ").workplane(offset=x0).polyline(pts).close().extrude(x1 - x0)


def spans():
    """(door lower, frame middle, door upper) along y, AX_CLR apart."""
    return ((0.0, SEG_DOOR - AX_CLR / 2),
            (SEG_DOOR + AX_CLR / 2, KN_L - SEG_DOOR - AX_CLR / 2),
            (KN_L - SEG_DOOR + AX_CLR / 2, KN_L))


def bore():
    return (cq.Workplane("XZ").workplane(offset=1.0).center(AXIS_X, AXIS_Z)
            .circle(PIN_HOLE_D / 2).extrude(-(KN_L + 2)))


def teardrop_hole(d, yc, zc, x0, x1):
    """Hole along x with a 45° teardrop peak toward +y (print-up), so a horizontal round hole needs no support."""
    r = d / 2; k = r / math.sqrt(2)
    pts = []
    for i in range(37):                                    # circle, 10° steps
        a = math.radians(i * 10)
        pts.append((yc + r * math.cos(a), zc + r * math.sin(a)))
    tri = [(yc + k, zc + k), (yc + r * math.sqrt(2), zc), (yc + k, zc - k)]
    circ = cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))
    peak = cq.Workplane("YZ").polyline(tri).close().extrude(x1 - x0).translate((x0, 0, 0))
    return circ.union(peak)


def frame_leaf():
    """Plate bolted to the scope rail's outer face (full length — its nearest corner is r 10.4 from the axis, outside
    everything the door sweeps through), then a riser in this leaf's own y-third climbing 45° off the plate's top into
    the barrel. There is deliberately NO full-length arm above the rail: anything there is inside the door's swept band
    and would stop it short of 180."""
    y0, y1 = spans()[1]
    body = box(FACE_X, FACE_X + PLATE_T, 0, KN_L, RAIL_Z0, PLATE_Z1)
    body = body.union(ramp_z(RISER_X0, RISER_X1, y0, y1, PLATE_Z1, AXIS_Z, ramp=True))
    body = body.union(barrel(y0, y1))
    body = body.cut(teardrop_hole(BOLT_D, KN_L / 2, SLOT_Z, FACE_X - 1, FACE_X + PLATE_T + 1))
    return body.cut(bore())


def door_leaf():
    """Glue pad on the panel's inner face (full length, all of it above z 347), and a shelf that catches the panel's
    bottom edge and carries on out to the barrel. The shelf lives ONLY in this leaf's own y-thirds: the frame leaf's
    riser passes through the middle third, and a full-length shelf would foul it near the end of the swing."""
    pad_x1 = FACE_X - PANEL_CLR                             # 360.85, clear of the panel
    body = box(FACE_X - PANEL_T - PAD_T, pad_x1, 0, KN_L, TILE_Z0, PAD_Z1)
    lo, _, hi = spans()
    for y0, y1 in (lo, hi):
        body = body.union(ramp_z(FACE_X - PANEL_T - PAD_T, AXIS_X, y0, y1,
                                 SHELF_Z0, TILE_Z0, ramp=y0 > 0.01, down=True))
        body = body.union(barrel(y0, y1))
    return body.cut(bore())


def printable(part):
    """Standing: frame +y becomes print +z, so every bore is vertical. Then z = 0 on the bed."""
    p = part.rotate((0, 0, 0), (1, 0, 0), 90)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(HERE, ".."))
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    for name, part in (("hinge-door-v2", door_leaf()), ("hinge-frame-v2", frame_leaf())):      # v2 pair: door leaf shelf 335–338, frame riser from x 364.3
        p = printable(part)
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        bb = p.val().BoundingBox()
        print(f"{name:16s} {bb.xlen:5.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}   {p.val().Volume()/1000:5.2f} cm3   (x2)")
        check(path, min_rest_frac=0.25, max_down_frac=0.2)
    print(f"axis x {AXIS_X} z {AXIS_Z}; barrel x {AXIS_X-BARREL_D/2:.0f}–{AXIS_X+BARREL_D/2:.0f}, "
          f"z {AXIS_Z-BARREL_D/2:.0f}–{AXIS_Z+BARREL_D/2:.0f}; each leaf reaches {REACH:.0f} from the axis; segments {spans()}")
