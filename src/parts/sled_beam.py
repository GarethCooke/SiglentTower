# Sled beams (HANDOVER §4, ROADMAP D6, PRINT-RULES §2) — the two 40 × 9 bars the scope rides on, z 337–346, one each
# side, each split at y 165 into a FRONT half (carries the scope: rear-bumper D cup + front-stand pocket) and a REAR half
# (carries the cross bars and the box). World frame: x from the outside of the left upright, y from the front plane, z from
# the bench. The LEFT beam is modelled; the right is its mirror about x = 180.5 (four STLs, all chiral).
#
#   body        x 20.5–60, y 12–330 (the front bar owns y 0–12), z 337–346
#   groove      underside, sled_foot.beam_groove(): x 22.0–27.4, z 337–341.2, CLOSED at y GROOVE_Y0 (119.5) and open at the
#               rear face — the foot's 210 rib threads in from the REAR until it hits the closed end, so the foot sits at
#               y 119.5–329.5; the beam is then bonded to the rib (ABS cement / CA at the groove ends). Nothing else holds
#               the two together: the pair is a sliding fit by design (P1) and the sled must move foot-and-beam as one.
#   split       y 165: P7 puzzle tab on the front half pointing +y, socket in the rear half (DOVETAIL_CLR), assembled
#               vertically and CA'd BEFORE threading onto the foot (a closed groove cannot be threaded half at a time).
#   front bar   the beam's front end carries the same tab pointing −y (y 4–12) into a socket in the bar's rear-bottom edge.
#   cross bars  y 190–210 and 308–328, between the beams (x 60–301): tab on each bar end, socket in the beam's inner edge.
#   cup boss    x 46.5–80 × y 109–143, 10 thick (z 337–347): the P9 D cup (BUMPER_* + BUMPER_CUP_CLR), 6 deep = 5 straight +
#               1 lead-in, floor at z 341 so the bumper's 14 puts the chassis at 355 (levels table). Flat faces the rear.
#   stand arm   x 60–95 × y 12–41, 9 thick: pocket STAND_W/L + STAND_CLR, 2.5 deep (floor 343.5 + 11.5 = 355), open at the
#               front face — the stand's leg is 1 mm behind the front bar, too close for a wall; the cups locate y anyway.
#   pegs        left beam only: two Ø4 × 2.5 pegs on the top at x 33, y 150 / 290, keying the cable channel's floor.
# Print: FLAT, top up, as exported (z = 0 on the bed). Groove ceiling is a 5.4 bridge; cup, pocket, sockets open upward;
# 0.4 chamfer on every bed edge (rule 7). Black ABS+ (sliding pair — same spool as the feet). printcheck on export.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import (DOVETAIL_CLR as C, BUMPER_W, BUMPER_D5, BUMPER_SIDE_L, BUMPER_CUP_D, BUMPER_CUP_CLR, BUMPER_H,
                 BUMPER_X_FROM_SIDE, BUMPER_REAR_FROM_FACE, STAND_W, STAND_L, STAND_CLR, STAND_POCKET_D, STAND_H,
                 STAND_X_FROM_SIDE, STAND_FRONT_FROM_FACE, SCOPE_X0, SCOPE_Y0, SCOPE_W, SCOPE_Z0)
from parts.drawer_quarters import box, prism, trapezoid, TAB_NECK, TAB_HEAD, TAB_LEN
from parts.sled_foot import beam_groove

Z0, T = 337.0, 9.0                    # beam underside / thickness
X0, BW = 20.5, 39.5                   # left beam outer face / width
Y_BAR, Y1 = 12.0, 330.0               # front bar's rear face / beam rear end
Y_SPLIT = 165.0
GROOVE_Y0 = 119.5                     # closed end of the groove -> foot at y 119.5–329.5 (0.5 short of the rear face)
XC = X0 + BW / 2                      # 40.25: tab centre line
XBAR_L, XBAR_R = 60.0, 301.0          # cross bars run between the beams' inner faces
CROSS_Y = (200.0, 318.0)              # cross-bar centre lines (bars 20 wide: 190–210, 308–328)
CUP_XC = SCOPE_X0 + BUMPER_X_FROM_SIDE            # 62
CUP_Y_FLAT = SCOPE_Y0 + BUMPER_REAR_FROM_FACE     # 138: the D's flat (rear) face
CUP_BOSS = (46.5, 80.0, 109.0, 143.0)             # x0 x1 y0 y1 — x0 clears the cable channel (x 20–46, y 140–334) on the beam top
CUP_FLOOR  = SCOPE_Z0 - BUMPER_H                  # 341: bumper 14 tall puts the chassis at 355
CUP_BOSS_T = CUP_FLOOR + BUMPER_CUP_D - Z0         # 10: rim at 347 (5 straight + 1 lead-in above the floor)
assert abs((Z0 + T - STAND_POCKET_D) + STAND_H - SCOPE_Z0) < 1e-6, 'stand pocket depth does not level the scope'
STAND_X0 = SCOPE_X0 + STAND_X_FROM_SIDE           # 47: stand's outer edge
STAND_Y0 = SCOPE_Y0 + STAND_FRONT_FROM_FACE       # 13: main leg's front edge
STAND_ARM = (XBAR_L, 95.0, Y_BAR, 41.0)
PEGS = ((33.0, 150.0), (33.0, 290.0)); PEG_D, PEG_H = 4.0, 2.5

def d_profile(wp, w, d, side):
    """P9 v3 D: flat at −d/2, straight sides `side` long, flatter three-point arc to the apex at +d/2 (centred on origin)."""
    r = w / 2; yc = -d / 2 + side
    return wp.moveTo(-r, -d / 2).lineTo(r, -d / 2).lineTo(r, yc).threePointArc((0, d / 2), (-r, yc)).close()

def cup_cutter(z_floor):
    """The P9 cup as a solid to cut: straight D for BUMPER_CUP_D − 1 above z_floor, then a 1 mm 45° lead-in, running out
    above the boss. Built with the flat at −y, then turned so the flat faces the REAR (+y), and placed at the bumper."""
    clr = BUMPER_CUP_CLR
    w, d, sd = BUMPER_W + 2 * clr, BUMPER_D5 + 2 * clr, BUMPER_SIDE_L + clr
    straight = d_profile(cq.Workplane("XY").workplane(offset=z_floor), w, d, sd).extrude(BUMPER_CUP_D - 1.0)
    z_lead = z_floor + BUMPER_CUP_D - 1.0
    lead = d_profile(cq.Workplane("XY").workplane(offset=z_lead), w, d, sd)
    lead = d_profile(lead.workplane(offset=1.0), w + 2, d + 2, sd + 1)
    lead = d_profile(lead.workplane(offset=2.0), w + 2, d + 2, sd + 1).loft(ruled=True)
    c = straight.union(lead).rotate((0, 0, 0), (0, 0, 1), 180)      # flat now at +y
    return c.translate((CUP_XC, CUP_Y_FLAT + clr - d / 2, 0))     # nominal flat at CUP_Y_FLAT, clr beyond it

def groove(y0, y1):
    """beam_groove() runs along +X in the beam frame (Y = world x − 20.5, Z = world z − 337); turn it to run along +y."""
    return beam_groove(y1 - y0).rotate((0, 0, 0), (0, 0, 1), -90).translate((X0, y1, Z0))

def tab(seam, along, dirn, grow=0.0, z0=Z0, z1=Z0 + T):
    return prism(trapezoid(seam, along, dirn, TAB_NECK, TAB_HEAD, TAB_LEN, grow=grow), z0, z1)

def left_front():
    b = box(X0, X0 + BW, Y_BAR, Y_SPLIT, Z0, Z0 + T)
    b = b.union(tab(Y_BAR, XC, (-1, "y")))                                   # into the front bar
    b = b.union(tab(Y_SPLIT, XC, (+1, "y")))                                 # into the rear half
    b = b.union(box(*CUP_BOSS, Z0, Z0 + CUP_BOSS_T))
    b = b.union(box(*STAND_ARM, Z0, Z0 + T))
    b = b.cut(cup_cutter(CUP_FLOOR))
    s = STAND_CLR
    b = b.cut(box(STAND_X0 - s, STAND_X0 + STAND_W + s, Y_BAR - 1, STAND_Y0 + STAND_L + s, Z0 + T - STAND_POCKET_D, Z0 + T + 1))
    b = b.cut(groove(GROOVE_Y0, Y_SPLIT + 1))                                  # closed at 119.5, open at the split
    b = b.union(cq.Workplane("XY").workplane(offset=Z0 + T).pushPoints([p for p in PEGS if p[1] < Y_SPLIT]).circle(PEG_D / 2).extrude(PEG_H))
    return b

def left_rear():
    b = box(X0, X0 + BW, Y_SPLIT, Y1, Z0, Z0 + T)
    b = b.cut(tab(Y_SPLIT, XC, (+1, "y"), grow=C, z0=Z0 - 1, z1=Z0 + T + 1))   # socket for the front half's tab
    for yc in CROSS_Y:                                                          # sockets for the cross-bar tabs
        b = b.cut(tab(XBAR_L, yc, (-1, "x"), grow=C, z0=Z0 - 1, z1=Z0 + T + 1))
    b = b.cut(groove(Y_SPLIT - 1, Y1 + 1))                                     # open both ends
    b = b.union(cq.Workplane("XY").workplane(offset=Z0 + T).pushPoints([p for p in PEGS if p[1] >= Y_SPLIT]).circle(PEG_D / 2).extrude(PEG_H))
    return b

def mirror_right(part):
    return part.mirror("YZ", (180.5, 0, 0))

def for_print(part):
    """Translate to the bed (bed face = underside), then 0.4 chamfer on the bed edges (rule 7)."""
    bb = part.val().BoundingBox()
    p = part.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    try:
        return p.edges("<Z").chamfer(0.4)
    except Exception as e:
        print("   chamfer skipped:", e); return p

PARTS = {"sled-beam-left-front": left_front, "sled-beam-left-rear": left_rear,
         "sled-beam-right-front": lambda: mirror_right(left_front().cut(pegs_cutter())),
         "sled-beam-right-rear": lambda: mirror_right(left_rear().cut(pegs_cutter()))}

def pegs_cutter():   # the channel is left-side only: the right beam has no pegs
    return cq.Workplane("XY").workplane(offset=Z0 + T).pushPoints(list(PEGS)).circle(PEG_D / 2 + 0.1).extrude(PEG_H + 1)

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    for name, fn in PARTS.items():
        p = for_print(fn()); bb = p.val().BoundingBox()
        path = os.path.join(OUT, f"{name}-v1.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:24s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:6.1f} cm3")
        check(path, min_rest_frac=0.5, max_down_frac=0.35)
