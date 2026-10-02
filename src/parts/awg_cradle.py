# AWG cradles (HANDOVER §10.2, ROADMAP Stage 3, gated by P2 ☑). The SDG2082X has no feet: its body (x 26.5–233.5,
# y 3–263, z 251.5–333.5) sits on four TPU pads at its bottom corners, 4 mm above the AWG rails' top (247.5). The front
# bezel (x 23–237, from z 248) hangs 3.5 below the body on each side and in front of it, so nothing may rise above the
# rail top under the bezel, and nothing may stand beside the body above z 247.5 within 3.5 of it except at the rear.
#
# LEFT cradle (x2, front + rear): PSU-style saddle on the left AWG rail (x 0–20) — same channel, lips and M5 counterbores
# as psu_cradle.py — with the inboard lip widened to x 26 (0.5 off the body edge: the lateral stop) and a 5 mm arm (v2)
# reaching to x 47.4 at z 239.5–247.5, its top FLUSH with the rail top. Pad pocket 20.4 x 20.4 x 1.5 in the arm.
# RIGHT cradle (x2): the inner AWG rail (x 251–271) carries the mini-slot drawer on its top, so the right cradle is a
# BRACKET on that rail's left face: a 4 mm plate (x 247–251, z 227.5–247.5; v1 was 10 and touched the PSU) with two COUNTERSUNK M5 into the rail's
# side slot (z 237.5), and the same 5 mm arm (v2; v1's 8 touched the PSU's top) reaching left to x 213.5 (20 under the body from its edge at 233.5),
# top flush at 247.5 — the mini slot starts at x 242, z 248, so nothing here rises above the rail top.
# TPU pads (P8): 20 x 20 x 5.5, standing 4 proud of the 1.5 pocket -> body at 251.5. The pads carry the corner lips
# (outer edge on all four, rear edge on the rear two); the front stop is the bezel against the front arms' front faces.
# Print: the right bracket ARM-TOP DOWN (the plate rises, counterbores horizontal Ø10 bridges; the pad pocket is a 1.5 mm
# recess open to the plate — tree support on build plate only fills it, snap out, exactly as the PSU cradles' cups); the left cradle STANDING ON ITS END (saddle top and arm top differ by 8, so neither can be the bed face):
# channel, lips, arm all walls, counterbores horizontal bridges, pocket a 1.5 mm side recess. 40 tall, 50 x 16 footprint.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import RAIL_CLR

RAIL, LIP_T, LIP_H, TOP_T = 20.0, 3.0, 6.0, 8.0     # psu_cradle values
SADDLE_L, HOLE_PITCH = 40.0, 20.0
HOLE_D, CBORE_D, CBORE_H = 5.5, 10.0, 5.2
ARM_T = 5.0                                         # arm thickness, top flush with the rail top. v2 2026-10-02: 8 -> 5 — the PSU's
                                                    # top (measured 150 on its feet, ~239.5 in the frame) touched the 8 mm arms' underside
                                                    # (239.5); 5 puts it at 242.5. Sag under the AWG's ~10 N per pad: 0.08 (left) / 0.15 (right)
PLATE_T = 4.0                                       # right bracket plate (v1 was 10): the PSU's side sits at x 244.5, so x 247–251 clears it by 2.5
CSK_D, CSK_DEPTH = 10.0, 2.25                        # M5 countersunk head (90°) sunk flush in the 4 mm plate
PAD, PAD_CLR, POCKET_D = 20.0, 0.2, 1.5             # TPU pad 20 x 20 x 5.5 in a 20.4 pocket, 4 proud
BODY_L, BODY_R = 26.5, 233.5                        # AWG body edges
UNDER = 20.0                                        # pad reach under the body from its edge
LIP_GAP = 0.5                                       # saddle inboard lip to the body edge
Z_RAIL_TOP = 247.5

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def pocket(x0, y0):
    return box(x0, x0 + PAD + 2 * PAD_CLR, y0, y0 + PAD + 2 * PAD_CLR, Z_RAIL_TOP - POCKET_D, Z_RAIL_TOP + 1)

def left_cradle():
    """Frame coordinates, y 0..SADDLE_L (place at y 20 front / y 223 rear), rail x 0–20."""
    lip_in = BODY_L - LIP_GAP                                       # 26.0
    saddle = box(-LIP_T, lip_in, 0, SADDLE_L, Z_RAIL_TOP, Z_RAIL_TOP + TOP_T)
    lips = box(-LIP_T, lip_in, 0, SADDLE_L, Z_RAIL_TOP - LIP_H, Z_RAIL_TOP)
    channel = box(-RAIL_CLR / 2, RAIL + RAIL_CLR / 2, -1, SADDLE_L + 1, Z_RAIL_TOP - LIP_H - 1, Z_RAIL_TOP)
    arm = box(RAIL, BODY_L + UNDER + PAD_CLR * 2 + 0.5, 0, SADDLE_L, Z_RAIL_TOP - ARM_T, Z_RAIL_TOP)
    body = saddle.union(lips).union(arm).cut(channel)
    body = body.cut(pocket(BODY_L + 0.5, (SADDLE_L - PAD - 2 * PAD_CLR) / 2))
    body = (body.faces(">Z").workplane(origin=(0, 0, Z_RAIL_TOP + TOP_T))
                .pushPoints([(RAIL / 2, SADDLE_L / 2 - HOLE_PITCH / 2), (RAIL / 2, SADDLE_L / 2 + HOLE_PITCH / 2)])
                .cboreHole(HOLE_D, CBORE_D, CBORE_H))
    return body

def right_bracket():
    """Frame coordinates, y 0..SADDLE_L (place at y 23 front / y 223 rear), rail x 251–271, its left face at x 251."""
    x_rail = 251.0; plate_t = PLATE_T
    plate = box(x_rail - plate_t, x_rail, 0, SADDLE_L, Z_RAIL_TOP - RAIL, Z_RAIL_TOP)
    arm = box(BODY_R - UNDER - PAD_CLR * 2 - 0.5, x_rail, 0, SADDLE_L, Z_RAIL_TOP - ARM_T, Z_RAIL_TOP)
    body = plate.union(arm)
    body = body.cut(pocket(BODY_R - UNDER - PAD_CLR * 2, (SADDLE_L - PAD - 2 * PAD_CLR) / 2))
    # two horizontal M5 counterbores from the plate's left face into the rail's side slot (centre z 237.5)
    for y in (SADDLE_L / 2 - HOLE_PITCH / 2, SADDLE_L / 2 + HOLE_PITCH / 2):
        zc = Z_RAIL_TOP - RAIL / 2
        hole = cq.Workplane("YZ", origin=(x_rail - plate_t - 1, y, zc)).circle(HOLE_D / 2).extrude(plate_t + 2)
        csk = cq.Workplane("XY").add(cq.Solid.makeCone(CSK_D / 2 + 1, HOLE_D / 2, CSK_DEPTH + 1,          # 90° countersink from the plate's left face
                                                     pnt=cq.Vector(x_rail - plate_t - 1, y, zc), dir=cq.Vector(1, 0, 0)))
        body = body.cut(hole).cut(csk)
    return body

def printable(part, on_end=False):
    """Right bracket: arm-top down (frame z -> -print z). Left cradle: STANDING ON ITS END (frame y -> print z) — its
    saddle top is 8 above the arm top, so neither can be the bed face without the other floating; on its end every
    extruded feature is a wall, the counterbores are horizontal Ø10 bridges and the pad pocket a 1.5 mm side recess."""
    p = part.rotate((0, 0, 0), (1, 0, 0), 90) if on_end else part.rotate((0, 0, 0), (0, 1, 0), 180)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    # left: the only down-facing areas are the two Ø10 horizontal counterbore ceilings (bridges, printed fine in v1); the thinner
    # v2 arm shrinks the resting face so their share rises to 33 %
    for name, part, on_end, kw in (("awg-cradle-left-v2", left_cradle(), True, dict(max_down_frac=0.4)), ("awg-cradle-right-v2", right_bracket(), False, dict(max_down_frac=0.6))):   # right: the pad pocket is a 1.5 recess on the plate, tree support on build plate only, as the PSU cradles' cups
        p = printable(part, on_end); path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        bb = p.val().BoundingBox(); print(f"{name}: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {part.val().Volume()/1000:.1f} cm3")
        check(path, **kw)
