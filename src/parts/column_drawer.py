# Column drawer (HANDOVER §6, ROADMAP D5, Stage 4; P3 ☑ geometry) and its four guide strips. World frame: x from the left
# upright's outer face, y from the front plane, z from the bench.
#
# The column bay is x 271–341 (inner uprights' right face to the right uprights' inner face), z 91–331. The drawer body is
# 64 × 285 × 240: x 274–338 (3 mm gap each side — the HANDOVER's 2/3 split made the two sides different parts), y 3–288
# (D5), z 91–331. Walls 2.4, floor 3. Two front screw pads for the facia (M3 x 10, as the bottom drawer).
# It runs on FOUR strips, two heights, two sides (HANDOVER: "four points, no tipping"):
#   LOWER (PSU level): the bearing pair — the P3 rib (14 at the plate, 45° top to 6.7 at the tip, 7 into the drawer) at
#     rib bottom z 94 = drawer floor top, exactly the bottom drawer's geometry: the drawer hangs on the two 45° slopes.
#     Mounted on the PSU-level rails' faces (inner rail's RIGHT face x 271, right PSU rail's INNER face x 341, side slot
#     centre z 78): an L — an 8 mm BOLT BAR in front of the rail face at z 70–86 (under the drawer floor, nothing else
#     lives there), four M5 x 10 counterbored into the side slot, a 2.7 plate rising from it to z 110 with the rib on it.
#   UPPER (AWG level, side slots at z 237.5): guides only — a plain rectangular rib 14 x 7 (2 mm 45° chamfer on its top
#     edge) at z 232–246 on a 2.7 plate; the four M5 x 10 go THROUGH the rib (Ø10 counterbore 4.5 deep from the rib's tip
#     face, 5.2 of material under the head). The drawer's upper grooves clear this rib by 0.5 all round except the roof,
#     which catches it if the drawer tries to tip when pulled out.
# Both strips are symmetric end for end, so one STL serves left and right (turn it round). Length 260, y 45–305: clear of
# the front tie / cast bracket (y 23–43) and the rear ties (y 310–330) on every face they use.
# Drawer grooves: lower = drawer_runner.groove_cut (P3, RUNNER_CLR) in a 10 x 20 boss along each outer wall at the floor,
# closed at the front wall, open at the rear; upper = a 10 x 26 boss at drawer z 138.5–164.5 with a house groove round
# the rectangular rib (0.5 slack, 45° roof).
# Print: drawer floor down on the diagonal (285 x 64 -> 247 diag, 240 tall), black PETG (or PLA), 5 mm brim, no support.
# Strips: rail face DOWN (bolt bar, plate and rib all rise from the bed; rib bottom = vertical wall, rib top = 45° wall;
# counterbores open upward), ABS+ dried, 5 mm outer brim, on the diagonal.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import RUNNER_CLR
from parts.drawer_quarters import box, teardrop_y, SCREW_HOLE_D, PAD_W, PAD_T, PAD_Z, PAD_Z1
from parts.drawer_runner import groove_cut, RIB_ENGAGE, RIB_H, RIB_TIP_H, BOSS_T, BOSS_H, HOLE_D, CBORE_D, CBORE_H

# ---- drawer, drawer coordinates (x from the left wall face, y from the body front, z from the bottom) ----
DW, DD, DH = 64.0, 285.0, 240.0
WALL, FLOOR = 2.4, 3.0
WIN_D = 29.0                        # pull-pocket window: the front wall's top 29 between the side walls (v3; cut by hand in the v1 print)
X0, Y0, Z0 = 274.0, 3.0, 91.0                     # body in the frame
PAD_XS = (16.0, 48.0)                             # facia screw pads
# strips
GAP = 3.0; PLATE_T = GAP - RUNNER_CLR             # 2.7
STRIP_L, STRIP_Y0 = 260.0, 45.0
BOLT_YS = (20.0, 93.3, 166.7, 240.0)
# LEFT lower strip (inner rail's right face): the right PSU cradles sit on that rail and their saddle lips hang 6 mm down its
# right face (y 23–63 and 223–263, z 82–88) — exactly where the 260 strip's bolt bar wants to be (Gareth, 2026-10-08:
# 144 clear between them). So the left lower strip is a SHORT one, 140 long with two bolts, centred in that gap; the drawer
# still hangs on both sides over its whole travel (the groove is 285 long, the right rib 260).
SHORT_L, SHORT_Y0 = 140.0, 73.0          # y 73–213 (gap 63–223 in the model; place it mid-gap on the bench)
SHORT_BOLT_YS = (25.0, 115.0)
LOW_SLOT, UP_SLOT = 78.0, 237.5                   # side-slot centres
BAR_T, BAR_Z = 8.0, (70.0, 86.0)                  # lower bolt bar
LOW_PLATE_Z = (70.0, 110.0); LOW_RIB_Z0 = Z0 + FLOOR   # 94: rib bottom = drawer floor top (P3)
UP_RIB_H, UP_RIB_CH = 14.0, 2.0
UP_RIB_Z = (UP_SLOT - UP_RIB_H / 2, UP_SLOT + UP_RIB_H / 2)   # 230.5–244.5
UP_PLATE_Z = (UP_RIB_Z[0] - 6, UP_RIB_Z[1] + 6)
UP_CLR = 0.5
UP_CBORE_H = 4.5

def upper_groove_cut(length):
    """Drawer-coordinate cutter for the LEFT wall round the upper rib: flank UP_CLR under the rib, back RUNNER_CLR past the
    tip, roof: flat UP_CLR over the rib top to the chamfer, then 45° to the wall face (prints as a 45° roof)."""
    z0 = UP_RIB_Z[0] - Z0 - UP_CLR; z1 = UP_RIB_Z[1] - Z0 + UP_CLR
    back = RIB_ENGAGE + RUNNER_CLR
    pts = [(-1, z0), (back, z0), (back, z1 - UP_RIB_CH), (back - UP_RIB_CH, z1), (0, z1 + back - UP_RIB_CH), (-1, z1 + back)]   # 45° throughout (0.57 off the rib's chamfer)
    return cq.Workplane("XZ").polyline(pts).close().extrude(length).translate((0, length, 0))

def drawer():
    d = box(0, DW, 0, DD, 0, FLOOR)
    for (x0, x1) in ((0, WALL), (DW - WALL, DW)): d = d.union(box(x0, x1, 0, DD, 0, DH))
    for (y0, y1) in ((0, WALL), (DD - WALL, DD)): d = d.union(box(0, DW, y0, y1, 0, DH))
    # lower bosses + P3 grooves (closed at the front wall, open at the rear); upper bosses + guide grooves
    ub0 = UP_RIB_Z[0] - Z0 - UP_CLR - 3; ub1 = UP_RIB_Z[1] - Z0 + RIB_ENGAGE + RUNNER_CLR + 3
    def upper_boss(left):   # 10 x (ub1-ub0) boss with a 45° underside (it hangs on the wall mid-height: rule 4)
        pts = [(0, ub0 - BOSS_T), (BOSS_T, ub0), (BOSS_T, ub1), (0, ub1)]
        b = cq.Workplane("XZ").polyline(pts).close().extrude(DD).translate((0, DD, 0))
        return b if left else b.mirror("YZ").translate((DW, 0, 0))
    for side in ("L", "R"):
        d = d.union(box(0, BOSS_T, 0, DD, 0, BOSS_H) if side == "L" else box(DW - BOSS_T, DW, 0, DD, 0, BOSS_H))
        d = d.union(upper_boss(side == "L"))
        g = groove_cut(DD - WALL).translate((0, WALL, 0)); u = upper_groove_cut(DD - WALL).translate((0, WALL, 0))
        if side == "R": g = g.mirror("YZ").translate((DW, 0, 0)); u = u.mirror("YZ").translate((DW, 0, 0))
        d = d.cut(g).cut(u)
    for xc in PAD_XS:
        d = d.union(box(xc - PAD_W / 2, xc + PAD_W / 2, WALL, WALL + PAD_T, 0, PAD_Z1))
        d = d.cut(teardrop_y(xc, PAD_Z, SCREW_HOLE_D / 2, -1, WALL + PAD_T + 1))
    # pull-pocket window: the facia's insert (pocket z 222–245, flange 57 wide down to z 214) passes through the front wall —
    # the wall's top 29 mm goes, side wall to side wall. The v1 print (2026-10-09) predates this: cut it by hand.
    d = d.cut(box(WALL, DW - WALL, -1, WALL + 1, DH - WIN_D, DH + 1))
    return d

def drawer_in_frame(): return drawer().translate((X0, Y0, Z0))

# ---- strips, frame coordinates for the LEFT side of the bay (rail face at x 271, rib pointing +x); y 0..STRIP_L ----
def lower_strip(length=STRIP_L, bolt_ys=BOLT_YS):
    xf = 271.0
    s = box(xf, xf + BAR_T, 0, length, BAR_Z[0], BAR_Z[1])                               # bolt bar
    s = s.union(box(xf, xf + PLATE_T, 0, length, LOW_PLATE_Z[0], LOW_PLATE_Z[1]))          # plate
    xp = xf + PLATE_T; xt = xp + RIB_ENGAGE
    rib = (cq.Workplane("XZ").polyline([(xp, LOW_RIB_Z0), (xt, LOW_RIB_Z0), (xt, LOW_RIB_Z0 + RIB_TIP_H), (xp, LOW_RIB_Z0 + RIB_H)])
           .close().extrude(length).translate((0, length, 0)))
    s = s.union(rib)
    for y in bolt_ys:                                                                     # M5 through the bar into the side slot
        s = s.cut(cq.Workplane("YZ", origin=(xf - 1, y, LOW_SLOT)).circle(HOLE_D / 2).extrude(BAR_T + 2))
        s = s.cut(cq.Workplane("YZ", origin=(xf + BAR_T - CBORE_H, y, LOW_SLOT)).circle(CBORE_D / 2).extrude(CBORE_H + 1))
    return s

def upper_strip():
    xf = 271.0
    s = box(xf, xf + PLATE_T, 0, STRIP_L, UP_PLATE_Z[0], UP_PLATE_Z[1])
    xp = xf + PLATE_T; xt = xp + RIB_ENGAGE
    rib = (cq.Workplane("XZ").polyline([(xp, UP_RIB_Z[0]), (xt, UP_RIB_Z[0]), (xt, UP_RIB_Z[1] - UP_RIB_CH), (xt - UP_RIB_CH, UP_RIB_Z[1]), (xp, UP_RIB_Z[1])])
           .close().extrude(STRIP_L).translate((0, STRIP_L, 0)))
    s = s.union(rib)
    for y in BOLT_YS:                                                                     # M5 through the rib into the side slot
        s = s.cut(cq.Workplane("YZ", origin=(xf - 1, y, UP_SLOT)).circle(HOLE_D / 2).extrude(PLATE_T + RIB_ENGAGE + 2))
        s = s.cut(cq.Workplane("YZ", origin=(xt - UP_CBORE_H, y, UP_SLOT)).circle(CBORE_D / 2).extrude(UP_CBORE_H + 1))
    return s

def strip_in_frame(kind, side):
    if kind == "lower" and side == "L":
        return lower_strip(SHORT_L, SHORT_BOLT_YS).translate((0, SHORT_Y0, 0))            # the short one, between the cradles
    s = (lower_strip() if kind == "lower" else upper_strip()).translate((0, STRIP_Y0, 0))
    return s if side == "L" else s.mirror("YZ", (306.0, 0, 0))                            # bay centre x 306: 271 <-> 341

def for_print(part):
    """rail face down: frame x -> print z."""
    p = part.rotate((0, 0, 0), (0, 1, 0), -90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "column")); os.makedirs(OUT, exist_ok=True)
    d = drawer(); bb = d.val().BoundingBox(); path = os.path.join(OUT, "column-drawer-v3.stl")
    cq.exporters.export(d, path, tolerance=0.02, angularTolerance=0.2)
    print(f"column-drawer-v3   {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {d.val().Volume()/1000:.0f} cm3  diag {(bb.xlen + bb.ylen)/2**0.5:.0f}")
    check(path, max_down_frac=0.5)
    for name, fn in (("column-strip-lower-v1", lower_strip), ("column-strip-lower-short-v1", lambda: lower_strip(SHORT_L, SHORT_BOLT_YS)),
                     ("column-strip-upper-v1", upper_strip)):
        p = for_print(fn()); bb = p.val().BoundingBox(); path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        n = 1 if ("short" in name or "lower-v1" in name) else 2
        print(f"{name:28s} {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  diag {(bb.xlen + bb.ylen)/2**0.5:.0f}  (print {n})")
        check(path, max_down_frac=0.5)
