# Bottom-drawer runner + the groove it rides in (HANDOVER §6, PRINT-RULES §2, ROADMAP P3). One runner per side on the base
# side rails, the drawer's outer side walls carry the groove. Frame coordinates for the LEFT side: x from the rail's outer
# face (rail x 0–20, inner face x 20, drawer wall x 23), y along the rail, z from the rail bottom (rail z 0–20, drawer
# body z 3–63). The right side is the same part turned end for end.
#
# Why this shape. The drawer wall sits 3 mm off the rail's inner face, so nothing bolted to that face through the 3 mm gap
# can hide an M5 head: a counterbore at the side-slot centre (z 10) breaks through whatever bearing face sits under it.
# So the runner is an L that bolts DOWN into the rail's TOP slot and hangs a rib over the inner face:
#   leg    x 3–22.7 × z 20–30  on the rail top, three M5 counterbores at x 10 (top slot centre)  — carries the load
#   plate  x 20–22.7 × z 6–30  down the rail's inner face (0.3 short of the drawer wall)
#   rib    x 22.7–30 × z 6–20  into the drawer's groove; bottom face z 6 is the BEARING (the drawer's floor top, z 3 + 3,
#          rests on it); tip x 30 locates the drawer sideways (0.3 to the groove back); top face slopes 45° from
#          (30, 12.7) up to the plate at (22.7, 20) so it prints without support.
# Drawer side (drawer coordinates: x inward from the outer wall face, z from the drawer bottom): a boss 10 thick × 20 tall
# along the outer wall with a house-shaped groove open to the outside: flank z 3 (bearing), back x 7.3, roof 45° from
# (7.3, 10.0) to the wall face at (0, 17.3). Only the back and roof carry RUNNER_CLR; the flank sits on the rib.
# The rib runs out through the open rear end of the groove; a stop block on the runner behind the drawer sets home.
#
# Print: runner LEG-TOP DOWN (frame z pointing at the bed): leg top is the bed face (~70 % of the footprint), plate and
# rib rise from it, the rib's sloped top becomes a 45° underside, the counterbores open onto the bed (Bambu "bridge
# counterbore holes: sacrificial layer", as the cradles). Bearing faces are the rib top-in-print (a top surface) and the
# drawer's groove flank (a top surface): flat and smooth, and their height only sets the 0.3 vertical play — rule 2's
# XY-accuracy demand applies to the locating faces (rib tip, groove back), which are vertical walls. Drawer prints
# floor-down as designed; the groove is a side pocket with a 45° roof (rule 4).
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import RUNNER_CLR

RAIL        = 20.0
GAP         = 3.0                    # rail inner face -> drawer wall (HANDOVER: 321 clear, 315 drawer)
PLATE_T     = GAP - RUNNER_CLR       # 2.7: plate stops 0.3 short of the drawer wall
RIB_ENGAGE  = 7.0                    # rib into the drawer beyond the wall face (x 23 -> 30)
RIB_X1      = RAIL + GAP + RIB_ENGAGE          # 30.0 rib tip
Z_BEAR      = 6.0                    # rib bottom = bearing = drawer floor top (drawer bottom z 3 + FLOOR 3)
Z_RAIL_TOP  = RAIL                   # 20
RIB_H       = Z_RAIL_TOP - Z_BEAR    # 14 at the plate
RIB_TIP_H   = RIB_H - (RIB_X1 - (RAIL + PLATE_T))   # 6.7 at the tip: 45° slope back to the plate
LEG_H       = 10.0                   # z 20–30; M5x10 head in a 5.2 counterbore leaves 4.8 under it -> 5.2 into the slot (cradle: 6, passed)
HOLE_D, CBORE_D, CBORE_H = 5.5, 10.0, 5.2     # cradle values (HOLE_D passed unshrunk in ASA)
BOLT_X      = RAIL / 2               # top slot centre
LEG_X0      = 3.0                    # leg starts 3 in from the rail's outer face: 2 mm wall outside the Ø10 counterbore is enough
END_LEAD    = 1.0                    # chamfer on the rib's end edges so the groove finds it
# drawer side
DRAWER_FLOOR = 3.0                   # drawer_quarters.FLOOR
BOSS_T, BOSS_H = 10.0, 20.0          # boss along the outer wall (x 0–10 from the wall face), 2.7 behind the groove back

def runner_section():
    """(x, z) polygon of the runner, frame coordinates, counter-clockwise."""
    xp = RAIL + PLATE_T
    return [(LEG_X0, Z_RAIL_TOP), (RAIL, Z_RAIL_TOP), (RAIL, Z_BEAR), (RIB_X1, Z_BEAR), (RIB_X1, Z_BEAR + RIB_TIP_H),
            (xp, Z_RAIL_TOP), (xp, Z_RAIL_TOP + LEG_H), (LEG_X0, Z_RAIL_TOP + LEG_H)]

def runner(length, bolt_ys):
    """Runner `length` along y (0..length), bolts at the given y positions, frame coordinates (as used, z up)."""
    r = cq.Workplane("XZ").polyline(runner_section()).close().extrude(length).translate((0, length, 0))
    r = r.edges("|Z").edges(">X").chamfer(END_LEAD)              # rib tip end edges
    r = r.edges("|X").edges("<Z").chamfer(END_LEAD)              # bearing face end edges
    r = r.edges(">Z").chamfer(0.4)                               # bed edges in the print (rule 7)
    r = (r.faces(">Z").workplane(origin=(0, 0, Z_RAIL_TOP + LEG_H))
          .pushPoints([(BOLT_X, y) for y in bolt_ys]).cboreHole(HOLE_D, CBORE_D, CBORE_H))
    return r

def runner_printable(length, bolt_ys):
    """Same part turned leg-top down, z = 0 on the bed, x/y from 0."""
    p = runner(length, bolt_ys).rotate((0, 0, 0), (0, 1, 0), 180)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def groove_cut(length, clr=RUNNER_CLR):
    """Solid to CUT from a drawer's LEFT outer wall (drawer coordinates: x inward from the wall face, z from the drawer
    bottom) over y 0..length. Mirror in x for the right wall. Flank at the floor top, back and roof grown by clr."""
    back = RIB_ENGAGE + clr                                      # 7.3
    z0 = DRAWER_FLOOR                                            # 3: bearing flank, no clearance
    z_back = z0 + RIB_TIP_H + clr                                # 10.0: vertical back ends, roof starts
    z_mouth = z0 + RIB_H + clr                                   # 17.3: roof meets the wall face
    pts = [(-1, z0), (back, z0), (back, z_back), (0, z_mouth), (-1, z_mouth + 1)]
    return cq.Workplane("XZ").polyline(pts).close().extrude(length).translate((0, length, 0))

def wall_stub(length, floor_w=30.0, wall_h=40.0, wall_t=2.4):
    """A section of the drawer's left outer wall with floor strip, groove boss and groove — the P3 drawer-side coupon and
    the literal section of the production quarter. Drawer coordinates, floor on z = 0."""
    def box(x0, x1, y0, y1, z0, z1):
        return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
    s = box(0, floor_w, 0, length, 0, DRAWER_FLOOR).union(box(0, wall_t, 0, length, 0, wall_h)).union(box(0, BOSS_T, 0, length, 0, BOSS_H))
    return s.cut(groove_cut(length)).clean()

# ---- production (Stage 4) ----
# Bottom-drawer runners x2, 300 long on the 310 base side rails (frame y 23-323; drawer y 3-303), black ABS+.
# FOUR M5 x 10 into the rail's top slot, not three: the bolts pull a long printed bar flat onto the rail (the 80 mm P3
# coupon stuck where one bolt could not straighten it). Bolts symmetric about mid-length, so the left and right runners are
# the SAME part (the right is this one turned end for end) — print it twice. Rear bolt at y 280 = frame y 303, the drawer's
# rear face: the home stop behind the drawer is a separate small part, modelled after the P3 friction verdict.
LENGTH = 300.0
BOLTS = (20.0, 107.0, 193.0, 280.0)

def production():
    return runner(LENGTH, BOLTS)

def plate():
    """One runner leg-top down, turned 45° onto the bed diagonal and centred on the 256 bed. Two runners with the ABS+
    5 mm outer brim do not fit one plate ((300 + 2 x 27 + gap + 10) / sqrt 2 > 250), so it is one runner per plate."""
    p = runner_printable(LENGTH, BOLTS).rotate((0, 0, 0), (0, 0, 1), 45)
    bb = p.val().BoundingBox()
    return p.translate((128 - (bb.xmin + bb.xmax) / 2, 128 - (bb.ymin + bb.ymax) / 2, -bb.zmin))

if __name__ == "__main__" and "--export" in sys.argv:
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "drawer"))
    path = os.path.join(OUT, "drawer-runner-300-v1.stl")
    p = plate(); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    bb = p.val().BoundingBox(); flat = runner_printable(LENGTH, BOLTS).val().BoundingBox()
    print(f"drawer-runner-300-v1: {flat.xlen:.1f} x {flat.ylen:.1f} x {flat.zlen:.1f} flat, {bb.xlen:.1f} x {bb.ylen:.1f} on the "
          f"diagonal (with 5 mm brim {bb.xlen + 10 / 2 ** 0.5 * 2:.0f}), {p.val().Volume() / 1000:.1f} cm3, bolts at y {BOLTS}")
    flat_path = os.path.join(OUT, "_runner-flat-check.stl")          # printcheck on the unturned part: on the diagonal the
    cq.exporters.export(runner_printable(LENGTH, BOLTS), flat_path, tolerance=0.01, angularTolerance=0.1)   # bbox footprint is
    try: check(flat_path, min_rest_frac=0.3)                           # mostly empty and the resting-face ratio means nothing
    finally: os.remove(flat_path)
    sys.exit()

if __name__ == "__main__":
    r = runner(300, [40, 150, 260]); bb = r.val().BoundingBox()
    print(f"runner 300: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {r.val().Volume()/1000:.1f} cm3  rib tip x {RIB_X1}, bearing z {Z_BEAR}, "
          f"rib {RIB_H} at the plate / {RIB_TIP_H} at the tip; groove back {RIB_ENGAGE + RUNNER_CLR}, roof to z {DRAWER_FLOOR + RIB_H + RUNNER_CLR} at the wall")
