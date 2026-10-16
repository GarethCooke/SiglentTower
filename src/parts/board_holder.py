# board_holder.py — the lighting controller's holder (ROADMAP Stage 8, D10; wiring v1 2026-10-16).
#
# The controller is a Wemos D1 mini (ESP8266, WLED) on a 50 x 40 x 1.6 piece of perfboard with the two 330 R, the two
# 1000 uF and the pigtail solder pads. It lives on the REAR FACE of the rear base cross rail (y 350, z 0-20), just right
# of the Addtam strip's cable drop: every wire in the build already ends at the frame's rear-left bottom corner (the sill
# wires come down the left PSU rail's inner slot into the rear-left upright's inner slot, the left LED strip starts at the
# bottom of that upright, the right strip's feed leaves along the rear base rail), and the rear-left upright has no free
# face (strip inside, Addtam behind, tiles outside). The rear base rail's REAR slot is otherwise empty (its hidden
# L-connectors are on the FRONT face), so the wires run in it under a TPU cover and come through the holder's plate.
#
# Geometry (frame coordinates): plate x 90-150 x y 350-355 x z 0-44 on the rail's rear face, ONE M5 x 10 at (x 120, z 10)
# counterbored 2.5 into a drop-in T-nut in the rail's rear slot (plate 5, counterbore 2.5 -> 7.5 of thread, as the strip
# brackets). Two side walls x 90-98.3 / 141.7-150, y 355-365, each with a board slot 2.0 wide (y 358.3-360.3) x 4.0 deep
# in its inner face, its roof flat for the inner 1.5 (a 1.5 mm overhang, nothing) then 45 deg to the mouth; a 3 mm ledge
# the board stands on at z 0-3. The board (x 94.6-144.6, y 358.5-360.1,
# z 3-43, components facing REARWARD) slides in from the top after the bolt is done up (the bolt head sits behind it).
# Two Ø6.5 wire holes through the plate at (x 100, z 10) and (x 140, z 10) open onto the rail's slot mouth: wires from the
# LEFT (sill + left strip) use the left hole, wires to the RIGHT strip the right hole; nothing passes the T-nut.
#
# Bed face: the plate's RAIL side (y 350), everything rises in +y. Precision surfaces: none (a tray for a 20 g board).
# The slot roofs are 45 deg (rule 4), the wire holes and the counterbore are vertical in the print, the ledge and walls
# rise from the plate. Any PETG, ~21 cm3, no brim, no support.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))

X0, X1, Y0, PLATE_T, Z0, Z1 = 90.0, 150.0, 350.0, 5.0, 0.0, 44.0
BOLT_X, BOLT_Z, HOLE_D, CBORE_D, CBORE_H = 120.0, 10.0, 5.5, 10.0, 2.5
WALL_T, WALL_Y1 = 8.3, 365.0                    # side walls x 90-98.3 and 141.7-150, rising to y 365
BOARD_W, BOARD_H, BOARD_T = 50.0, 40.0, 1.6     # perfboard, cut by hand (+-0.5)
SLOT_FLOAT = 0.7                                # per side: slot bottoms 51.4 apart
SLOT_Y0, SLOT_Y1 = 358.3, 360.3                 # board plane y 358.5-360.1 (3.5 off the plate for the header tails)
SLOT_DEPTH = 4.0                                # into each wall from its inner face
ROOF_FLAT = 1.5                                 # the roof is flat over the innermost 1.5 of the slot, then 45 deg
LEDGE_H = 3.0
WIRE_XS, WIRE_D = (100.0, 140.0), 6.5
SLOT_X0 = X0 + WALL_T - SLOT_DEPTH              # 94.3 left slot bottom
SLOT_X1 = X1 - WALL_T + SLOT_DEPTH              # 145.7 right slot bottom
assert abs((SLOT_X1 - SLOT_X0) - (BOARD_W + 2 * SLOT_FLOAT)) < 1e-6

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def slot_cut(x_in, x_bottom, z0, z1):
    """Board slot in a side wall: floor at SLOT_Y0, 45 deg roof from SLOT_Y1 at the slot bottom rising toward the mouth.
    x_in = the wall's inner face, x_bottom = the slot bottom. Section in the xy plane, extruded along z."""
    d, f = SLOT_DEPTH, ROOF_FLAT
    if x_bottom < x_in:   # left wall: bottom at the smaller x
        pts = [(x_bottom, SLOT_Y0), (x_in + 1, SLOT_Y0), (x_in + 1, SLOT_Y1 + d - f + 1), (x_bottom + f, SLOT_Y1), (x_bottom, SLOT_Y1)]
    else:
        pts = [(x_bottom, SLOT_Y0), (x_in - 1, SLOT_Y0), (x_in - 1, SLOT_Y1 + d - f + 1), (x_bottom - f, SLOT_Y1), (x_bottom, SLOT_Y1)]
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))

def holder():
    h = box(X0, X1, Y0, Y0 + PLATE_T, Z0, Z1)
    h = h.union(box(X0, X0 + WALL_T, Y0 + PLATE_T, WALL_Y1, Z0, Z1))
    h = h.union(box(X1 - WALL_T, X1, Y0 + PLATE_T, WALL_Y1, Z0, Z1))
    h = h.union(box(X0 + WALL_T, X1 - WALL_T, Y0 + PLATE_T, SLOT_Y1, Z0, Z0 + LEDGE_H))      # ledge the board stands on
    h = h.cut(slot_cut(X0 + WALL_T, SLOT_X0, Z0 + LEDGE_H, Z1 + 1))
    h = h.cut(slot_cut(X1 - WALL_T, SLOT_X1, Z0 + LEDGE_H, Z1 + 1))
    # M5 through the plate, counterbore from the rear face
    h = h.cut(cq.Workplane("XZ", origin=(BOLT_X, Y0 - 1, BOLT_Z)).circle(HOLE_D / 2).extrude(-(PLATE_T + 2)))
    h = h.cut(cq.Workplane("XZ", origin=(BOLT_X, Y0 + PLATE_T - CBORE_H, BOLT_Z)).circle(CBORE_D / 2).extrude(-(CBORE_H + 1)))
    for x in WIRE_XS:
        h = h.cut(cq.Workplane("XZ", origin=(x, Y0 - 1, BOLT_Z)).circle(WIRE_D / 2).extrude(-(PLATE_T + 2)))
    return h

def board():
    return box(SLOT_X0 + SLOT_FLOAT, SLOT_X1 - SLOT_FLOAT, 358.5, 358.5 + BOARD_T, Z0 + LEDGE_H, Z0 + LEDGE_H + BOARD_H)

def surroundings():
    """What the holder must clear: the rear base rail, the Addtam + its shelf bracket, the TPU foot pads, the rear uprights."""
    bits = [box(20, 341, 330, 350, 0, 20),                 # rear base cross rail
            box(0, 20, 330, 350, 0, 510), box(341, 361, 330, 350, 0, 510),   # rear uprights
            box(1, 79, 355, 385, 75, 425),                  # Addtam strip body
            box(0, 80, 350, 380, 51, 75),                   # lower strip bracket incl. shelf + brace
            box(-2, 22, 328, 352, -6, 0), box(339, 363, 328, 352, -6, 0),    # TPU feet under the rear uprights
            box(14, 46, 350, 400, -6, 75)]                  # the Addtam's mains cable drop (Ø15 + keyhole travel)
    s = bits[0]
    for b in bits[1:]: s = s.union(b)
    return s

def printable(h):
    """Plate face down: +y -> +z (features rise), as the strip brackets."""
    p = h.rotate((0, 0, 0), (1, 0, 0), 90)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "wiring")); os.makedirs(OUT, exist_ok=True)
    H, B, S = holder(), board(), surroundings()
    print("--- proofs (cm3; 0 = clear) ---")
    print(f"holder vs frame/Addtam/feet/cable {vol(H, S):.4f}  pushed 0.5 into the rail {vol(H.translate((0, -0.5, 0)), S):.4f} (>0: flat on it)")
    print(f"board in the holder {vol(B, H):.4f}; pulled 1.0 off the plate {vol(B.translate((0, 1.0, 0)), H):.4f} (>0: held by the roofs); "
          f"pushed 1.0 toward the plate {vol(B.translate((0, -1.0, 0)), H):.4f} (>0); "
          f"shifted 1.0 left/right {vol(B.translate((-1.0, 0, 0)), H):.4f}/{vol(B.translate((1.0, 0, 0)), H):.4f} (>0: 0.7 float); "
          f"0.5 down {vol(B.translate((0, 0, -0.5)), H):.4f} (>0: on the ledge); lifted 45 {vol(B.translate((0, 0, 45)), H):.4f} (0: slides out the top)")
    print(f"board vs surroundings {vol(B, S):.4f}; bolt head under the board: counterbore y {Y0 + PLATE_T - CBORE_H}-{Y0 + PLATE_T}, board from y 358.5 -> {358.5 - (Y0 + PLATE_T):.1f} clear of the plate for a 2.7 head")
    p = printable(H); bb = p.val().BoundingBox(); path = os.path.join(OUT, "board-holder-v1.stl")
    cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    print(f"board-holder-v1  {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  — any PETG, plate face down as exported, no brim, no support")
    check(path, min_rest_frac=0.3, max_down_frac=0.6)   # the two 45 deg roofs and the 3 mm ledge top are the only down-facing area
