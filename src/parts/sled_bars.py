# Sled bars (HANDOVER §4/§5, ROADMAP Stage 5) — the three bars that tie the two sled beams into one rigid ladder: the FRONT
# BAR across the front of the beams and the two CROSS BARS the rear box rides on. World frame as sled_beam.py (x from the
# outside of the left upright, y from the front plane, z from the bench). Every joint is the P7 puzzle tab (DOVETAIL_CLR),
# assembled vertically and CA'd: a dry tab has 0.15 of play, and the whole point of the ladder is roll stiffness — on their
# own the beams lean inwards under the scope (2026-09-28, Gareth's photo: the scope would not seat in the stand pockets).
#
#   front bar   x 23–338 (315), y 0–12, z 337–355 (18 tall). v3 (2026-10-01): one CLOSED pocket per beam in its rear face
#               (x 27.85–96.15 and mirror, 4.3 tall, 8.15 deep, z 341.35–345.65, plus the 45° wedge under the root) takes
#               the beam's front tongue (sled_beam v2: beam body through to the stand pad's inboard edge); the bar slides
#               on from the FRONT, so the tongue is held above (9.35 of bar) and below (4.35 floor) along its whole 68 —
#               the stand pad's edge cannot drop. v1/v2 had dovetail sockets open at the bottom (bar dropped on),
#               which is a hinge in roll. Pull: a 120 × 6 notch in the top edge
#               (x 120.5–240.5, z 349–355) — the D9 notch; whether it gets an insert is decided when the sled is in use.
#               v2 (2026-09-28/10-01, after Gareth's photo of the stand arm's inboard edge dropping): two SADDLES on the
#               bar's rear face, x 20.5–46 / 315–340.5, y 12–88, z 346–353, that lie on top of each beam's body behind
#               the bar, CA'd to it and screwed (two M3 × 14 self-tappers per saddle, Ø3.4 teardrop holes at x 33 / 328,
#               y 30 / 70, Ø2.5 pilots drilled into the beam through them; 7 into the 9 mm beam). A 9 mm tab alone is a
#               hinge in roll; the saddle is a 25.5 × 76 lap, so the beam cannot roll about its foot without shearing the
#               lap — that is what holds the stand arm's inboard edge up (the arm itself hardly bends: 0.01 mm). 1.1
#               clear of the stand leg (x 47.1), 2 under the chassis (355), 0.5 / 3 clear of the cup boss (x 46.5, y 91),
#               clear of the cable channel (y 140+). The beam's and arm's front faces (y 12) are glued to the bar as well.
#   cross bars  v2 (2026-10-04): the printed v1 lips sat exactly 135 apart = the box's length, so the box would not drop
#               between them; each lip moved 1 mm outward (front lip y 189–194, rear lip y 331–336 → 2 mm of play).
#               Between the beams' inner faces (x 60–301), z 337–346 (level with the beams), tabs on both ends into the
#               beams' sockets at y 200 / 318 (sled_beam.CROSS_Y). Front cross bar y 190–210 with a 5 × 10 guide lip on its
#               front face (z 346–356, chamfered at the right = exit end); rear cross bar y 308–335 with a square lip on its
#               rear 5 (y 330–335). The box (y 195–330, floor 346) sits on the bars between the lips.
# Print: front bar FRONT FACE DOWN as exported (315 × 18 footprint, 12 tall, the saddles rising 76 from it, on the
# diagonal — D3's on-edge rule was for the 86-tall fronts; this way every socket flank is still a vertical wall, the
# sockets are open pockets from the top, the saddle holes are teardrops, nothing needs support), no brim, no support;
# cross bars FLAT, lips up. Front bar dark grey PETG, cross bars black ABS.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import DOVETAIL_CLR as C
from parts.drawer_quarters import box
from parts.sled_beam import tab, Z0, T, XC, Y_BAR, XBAR_L, XBAR_R, CROSS_Y, TONGUE_X0, TONGUE_X1, TONGUE_L, TONGUE_Z, tongue_wedge

BAR_X0, BAR_X1, BAR_Y1, BAR_H = 23.0, 338.0, 12.0, 18.0      # front bar
XC_R = 361.0 - XC                                            # 320.75: right beam's tab centre (mirror about x 180.5)
NOTCH_W, NOTCH_D = 120.0, 6.0
SADDLE = (20.5, 46.0, 12.0, 88.0, 346.0, 353.0)               # left saddle x0 x1 y0 y1 z0 z1; right is the mirror about x 180.5
SADDLE_HOLES = ((33.0, 30.0), (33.0, 70.0)); SADDLE_HOLE_D = 3.4   # M3 clearance, teardrop peak toward +y (horizontal in the print)
LIP_T, LIP_H = 5.0, 10.0
FRONT_CROSS = (189.0, 210.0)                                 # body y; lip on the front face. v2 2026-10-04: 1 further forward (lip y 189–194)
REAR_CROSS = (308.0, 336.0)                                  # body y (runs past the beams' ends to carry the lip); lip on its rear 5, y 331–336 (v2: 1 further back)

def front_bar():
    b = box(BAR_X0, BAR_X1, 0.0, BAR_Y1, Z0, Z0 + BAR_H)
    for x0, x1 in ((TONGUE_X0, TONGUE_X1), (361 - TONGUE_X1, 361 - TONGUE_X0)):   # one closed pocket per beam, open at the rear face
        b = b.cut(box(x0 - C, x1 + C, Y_BAR - TONGUE_L - C, Y_BAR + 1, TONGUE_Z[0] - C, TONGUE_Z[1] + C))
        b = b.cut(tongue_wedge(x0, x1, grow=C))               # and the 45° wedge under its root
    xm = (BAR_X0 + BAR_X1) / 2
    b = b.cut(box(xm - NOTCH_W / 2, xm + NOTCH_W / 2, -1, BAR_Y1 + 1, Z0 + BAR_H - NOTCH_D, Z0 + BAR_H + 1))
    x0, x1, y0, y1, z0, z1 = SADDLE
    b = b.union(box(x0, x1, y0, y1, z0, z1)).union(box(361 - x1, 361 - x0, y0, y1, z0, z1))
    for hx, hy in SADDLE_HOLES:
        for xc in (hx, 361 - hx):
            b = b.cut(teardrop_z(xc, hy, SADDLE_HOLE_D / 2, z0 - 1, z1 + 1))
    return b

def teardrop_z(xc, yc, r, z0, z1):
    """Round hole along z with a 45° peak toward +y: +y is 'up' when the bar prints front face down (rule 4)."""
    a = r / 2 ** 0.5
    tri = cq.Workplane("XY").workplane(offset=z0).polyline([(xc - a, yc + a), (xc, yc + r * 2 ** 0.5), (xc + a, yc + a)]).close().extrude(z1 - z0)
    return cq.Workplane("XY").workplane(offset=z0).center(xc, yc).circle(r).extrude(z1 - z0).union(tri)

def cross_bar(y0, y1, yc, lip_front):
    b = box(XBAR_L, XBAR_R, y0, y1, Z0, Z0 + T)
    b = b.union(tab(XBAR_L, yc, (-1, "x"))).union(tab(XBAR_R, yc, (+1, "x")))
    if lip_front:
        lip = box(XBAR_L, XBAR_R, y0, y0 + LIP_T, Z0 + T, Z0 + T + LIP_H)
        wedge = (cq.Workplane("XZ").polyline([(XBAR_R - LIP_H, Z0 + T + LIP_H), (XBAR_R + 1, Z0 + T + LIP_H), (XBAR_R + 1, Z0 + T - 1)])
                 .close().extrude(LIP_T + 2).translate((0, y0 + LIP_T + 1, 0)))
        lip = lip.cut(wedge)                                  # 45° run-out at the exit (right) end
    else:
        lip = box(XBAR_L, XBAR_R, y1 - LIP_T, y1, Z0 + T, Z0 + T + LIP_H)
    return b.union(lip)

def cross_front(): return cross_bar(*FRONT_CROSS, CROSS_Y[0], True)
def cross_rear():  return cross_bar(*REAR_CROSS, CROSS_Y[1], False)

VERSION = {"sled-front-bar": 3, "sled-cross-bar-front": 2, "sled-cross-bar-rear": 2}
PARTS = {"sled-front-bar": front_bar, "sled-cross-bar-front": cross_front, "sled-cross-bar-rear": cross_rear}

def for_print(part, on_front=False):
    if on_front: part = part.rotate((0, 0, 0), (1, 0, 0), 90)      # front face (y = 0) down, saddles rising
    bb = part.val().BoundingBox()
    return part.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts"))
    for name, fn in PARTS.items():
        p = for_print(fn(), on_front=(name == "sled-front-bar")); bb = p.val().BoundingBox()
        path = os.path.join(OUT, f"{name}-v{VERSION.get(name, 1)}.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        diag = (bb.xlen + bb.ylen) / 2 ** 0.5
        print(f"{name:22s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:6.1f} cm3  diag {diag:.0f}")
        check(path, min_rest_frac=0.5, max_down_frac=0.35)
