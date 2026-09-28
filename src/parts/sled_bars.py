# Sled bars (HANDOVER §4/§5, ROADMAP Stage 5) — the three bars that tie the two sled beams into one rigid ladder: the FRONT
# BAR across the front of the beams and the two CROSS BARS the rear box rides on. World frame as sled_beam.py (x from the
# outside of the left upright, y from the front plane, z from the bench). Every joint is the P7 puzzle tab (DOVETAIL_CLR),
# assembled vertically and CA'd: a dry tab has 0.15 of play, and the whole point of the ladder is roll stiffness — on their
# own the beams lean inwards under the scope (2026-09-28, Gareth's photo: the scope would not seat in the stand pockets).
#
#   front bar   x 23–338 (315), y 0–12, z 337–355 (18 tall). Sockets in its rear-bottom edge at x 40.25 / 320.75 take the
#               beams' tabs (y 4–12, z 337–346); the bar drops onto both tabs. Pull: a 120 × 6 notch in the top edge
#               (x 120.5–240.5, z 349–355) — the D9 notch; whether it gets an insert is decided when the sled is in use.
#   cross bars  between the beams' inner faces (x 60–301), z 337–346 (level with the beams), tabs on both ends into the
#               beams' sockets at y 200 / 318 (sled_beam.CROSS_Y). Front cross bar y 190–210 with a 5 × 10 guide lip on its
#               front face (z 346–356, chamfered at the right = exit end); rear cross bar y 308–335 with a square lip on its
#               rear 5 (y 330–335). The box (y 195–330, floor 346) sits on the bars between the lips.
# Print: front bar STANDING on its bottom edge as exported (315 × 12 footprint, 18 tall, on the diagonal — D3), sockets open
# to the bed (8 mm bridges over them); cross bars FLAT, lips up. Front bar dark grey PETG, cross bars black ABS.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import DOVETAIL_CLR as C
from parts.drawer_quarters import box
from parts.sled_beam import tab, Z0, T, XC, Y_BAR, XBAR_L, XBAR_R, CROSS_Y

BAR_X0, BAR_X1, BAR_Y1, BAR_H = 23.0, 338.0, 12.0, 18.0      # front bar
XC_R = 361.0 - XC                                            # 320.75: right beam's tab centre (mirror about x 180.5)
NOTCH_W, NOTCH_D = 120.0, 6.0
LIP_T, LIP_H = 5.0, 10.0
FRONT_CROSS = (190.0, 210.0)                                 # body y; lip on the front face
REAR_CROSS = (308.0, 335.0)                                  # body y (runs 5 past the beams' ends to carry the lip); lip on its rear 5, y 330–335

def front_bar():
    b = box(BAR_X0, BAR_X1, 0.0, BAR_Y1, Z0, Z0 + BAR_H)
    for xc in (XC, XC_R):                                    # sockets: open at the bottom, closed at z 346
        b = b.cut(tab(Y_BAR, xc, (-1, "y"), grow=C, z0=Z0 - 1, z1=Z0 + T))
    xm = (BAR_X0 + BAR_X1) / 2
    b = b.cut(box(xm - NOTCH_W / 2, xm + NOTCH_W / 2, -1, BAR_Y1 + 1, Z0 + BAR_H - NOTCH_D, Z0 + BAR_H + 1))
    return b

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

PARTS = {"sled-front-bar": front_bar, "sled-cross-bar-front": cross_front, "sled-cross-bar-rear": cross_rear}

def for_print(part):
    bb = part.val().BoundingBox()
    return part.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts"))
    for name, fn in PARTS.items():
        p = for_print(fn()); bb = p.val().BoundingBox()
        path = os.path.join(OUT, f"{name}-v1.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        diag = (bb.xlen + bb.ylen) / 2 ** 0.5
        print(f"{name:22s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:6.1f} cm3  diag {diag:.0f}")
        check(path, min_rest_frac=0.5, max_down_frac=0.35)
