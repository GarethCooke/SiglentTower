# Sill panel + end blocks (ROADMAP D10, Stage 8 trim): the grey strip that fills the reveal between the bottom-drawer
# facia (top z 86) and the PSU's front (bottom z 100), carrying the lighting button and its halo. Frame coordinates.
#
# v2 (2026-10-12, from the v1 print on the bench):
#   - Panel 230.7 long, x 20–250.7: v1's 251 fouled the sub-frame's front upright (x 251–271) — it is evidently flush
#     with the front, not set back 3. The panel now stops just short of it; that upright's front face shows for 20 mm.
#     The right block's bolt hole is a slot (y 8.5–14.5) so it bolts into the upright's left-face slot whether that slot
#     centre is at y 10 (flush upright) or y 13.
#   - Panel and window are exported with the SAME origin: load both and the window drops into its cut-out.
#   - Button at x 43 (bezel 18 from the upright's inner face), nearer the left end as asked. Its thread is 6 long behind
#     the window: the nut (10 AF, ~2 thick) sits DIRECTLY on the window's back inside a captive hex pocket in the block —
#     screw the button in from the front, the nut cannot turn. Behind the nut the body bore (Ø9) runs to the block's back
#     face at y 19.5; the left PSU cradle's arm is at y 20, so EVERYTHING behind the bezel must fit in 16.5 mm.
#   - Window 26 × 12 (x 30–56) with a light cavity (y 3–9) behind it either side of the hex pocket and a Ø5.3 pixel bore
#     from the rear on each side (x 32.9 and 53.1; fit one or two 5 mm WS2812). Print the blocks WHITE to bounce light.
#   - Pegs are a press fit (Ø3.2 in a Ø3.3 hole): no glue; the button clamps the panel to the left block as well. To
#     rewire: unscrew the button, pull the panel off its pegs.
#   - The left block no longer bolts: with the button at the left end there is no line for an M5 into the upright's slot
#     that misses the button. It carries a 5.3-wide TONGUE on its left face that sits in the upright's inner-face slot
#     mouth (locates it in y), and is held forward/back by the panel's pegs; CA the tongue if it ever walks.
#
# Parts:
#   PANEL   x 20–250.7 × y 0–3 × z 87–99, dark grey PETG; Ø8.4 button hole at (43, 93) in a 26 × 12 natural-PETG WINDOW
#           (x 30–56, separate STL, same origin). Four Ø3.2 × 7 pegs on the back (x 24, 62, 229, 248; z 93). Standing.
#   LEFT BLOCK  x 20.3–66 × y 3–19.5 × z 87–99, tongue x 18.7–20.3 × y 7.35–12.65 (full height). Hex nut pocket 10.6 AF
#           (flats top/bottom) y 3–6 round the Ø8.4 bore; body bore Ø9 y 6–19.5; light cavity x 30–56 × y 3–9 × z 88–98
#           minus the hex boss; pixel bores Ø5.3 from the rear face into the cavity; wire notch at the bottom-rear corner.
#           Prints FRONT FACE DOWN.
#   RIGHT BLOCK x 226–250.7 × y 3–19 × z 87–99: M5 × 10 along x at z 93 through a y 8.5–14.5 slot in its 7.7 right wall
#           into the sub-frame upright's left-face slot; head pocket x 229–243 open to the front. FRONT FACE DOWN.
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from parts.drawer_quarters import box, teardrop_y

Z0, Z1, T = 87.0, 99.0, 3.0
PX0, PX1 = 20.0, 250.7
BTN_X, BTN_Z, BTN_HOLE_D = 43.0, 93.0, 8.4
WIN_X0, WIN_X1 = 30.0, 56.0
PEG_XS, PEG_Z, PEG_D, PEG_L, PEG_HOLE_D, PEG_HOLE_L = (24.0, 62.0, 229.0, 248.0), 93.0, 3.2, 7.0, 3.3, 7.5
LB_X0, LB_X1, LB_Y1 = 20.3, 66.0, 19.5
TONGUE_D, TONGUE_W = 1.6, 5.3                    # into the upright's slot mouth (5.9 wide, lips 1.75 deep)
NUT_AF, NUT_T, HEX_WALL = 10.6, 3.0, 1.2            # captive nut pocket: 10 AF nut + 0.6, pocket depth, boss wall
BODY_D = 9.0
BOLT_Y, BOLT_Z, HOLE_D, CBORE_D, CBORE_H = 10.0, 93.0, 5.5, 9.0, 5.0
CAV = (30.0, 56.0, 3.0, 9.0, 88.0, 98.0)
LED_XS, LED_D = (32.9, 53.1), 5.3
NOTCH_W, NOTCH_H = 6.0, 4.0
RB_X0, RB_X1, RB_Y1 = 226.0, 250.7, 19.0
RB_POCKET, RB_SLOT_Y = (229.0, 243.0, 3.0, 17.0, 88.0, 98.0), (8.5, 14.5)   # slotted: the upright's slot centre is y 10 or 13

def teardrop_x(yc, zc, r, x0, x1):
    """Round hole along x with a 45° peak toward +y (print 'up' when the block prints front face down)."""
    a = r / 2 ** 0.5
    tri = cq.Workplane("YZ").polyline([(yc + a, zc - a), (yc + r * 2 ** 0.5, zc), (yc + a, zc + a)]).close().extrude(x1 - x0)
    cyl = cq.Workplane("YZ").center(yc, zc).circle(r).extrude(x1 - x0)
    return cyl.union(tri).translate((x0, 0, 0))

def panel():
    p = box(PX0, PX1, 0, T, Z0, Z1)
    p = p.cut(box(WIN_X0, WIN_X1, -1, T + 1, Z0 - 1, Z1 + 1))
    for x in PEG_XS:
        p = p.union(cq.Workplane("XZ", origin=(x, T, PEG_Z)).circle(PEG_D / 2).extrude(-PEG_L))      # +y, into the block
    return p

def window():
    w = box(WIN_X0, WIN_X1, 0, T, Z0, Z1)
    return w.cut(cq.Workplane("XZ", origin=(BTN_X, T + 1, BTN_Z)).circle(BTN_HOLE_D / 2).extrude(T + 2))

def hex_prism(af, y0, y1, xc, zc):
    """Hexagon (flats top and bottom) of across-flats af, along y."""
    r = af / 3 ** 0.5           # circumradius
    pts = [(xc + r * math.cos(math.radians(a)), zc + r * math.sin(math.radians(a))) for a in (0, 60, 120, 180, 240, 300)]
    return cq.Workplane("XZ").polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))

def left_block():
    b = box(LB_X0, LB_X1, T, LB_Y1, Z0, Z1)
    b = b.union(box(LB_X0 - TONGUE_D, LB_X0 + 0.01, BOLT_Y - TONGUE_W / 2, BOLT_Y + TONGUE_W / 2, Z0, Z1))   # tongue into the slot mouth
    x0, x1, y0, y1, z0, z1 = CAV
    cav = box(x0, x1, y0 - 1, y1, z0, z1)
    boss = hex_prism(NUT_AF + 2 * HEX_WALL, y0 - 1, y1 + 1, BTN_X, BTN_Z)                      # the hex boss stays solid inside the cavity
    b = b.cut(cav.cut(boss))                                                                  # light cavity either side of the boss
    b = b.cut(hex_prism(NUT_AF, T - 1, T + NUT_T, BTN_X, BTN_Z))                              # captive nut pocket on the window's back
    b = b.cut(cq.Workplane("XZ", origin=(BTN_X, LB_Y1 + 1, BTN_Z)).circle(BODY_D / 2).extrude(LB_Y1 + 2))      # body bore, through
    for x in LED_XS:
        b = b.cut(cq.Workplane("XZ", origin=(x, LB_Y1 + 1, BTN_Z)).circle(LED_D / 2).extrude(LB_Y1 + 1 - CAV[3] + 0.5))   # pixel bores, rear -> cavity
    b = b.cut(box(LB_X1 - NOTCH_W - 2, LB_X1 - 2, LB_Y1 - 6, LB_Y1 + 1, Z0 - 1, Z0 + NOTCH_H))    # wire notch, bottom-rear corner
    for x in PEG_XS[:2]:
        b = b.cut(cq.Workplane("XZ", origin=(x, T - 1, PEG_Z)).circle(PEG_HOLE_D / 2).extrude(-(PEG_HOLE_L + 1)))
    return b

def right_block():
    b = box(RB_X0, RB_X1, T, RB_Y1, Z0, Z1)
    x0, x1, y0, y1, z0, z1 = RB_POCKET
    b = b.cut(box(x0, x1, y0 - 1, y1, z0, z1))                                                       # bolt-head pocket, open at the front
    for yc in RB_SLOT_Y:                                                                          # slotted M5 hole y 8.5–14.5
        b = b.cut(teardrop_x(yc, BOLT_Z, HOLE_D / 2, x1 - 1, RB_X1 + 1))
    b = b.cut(box(x1 - 1, RB_X1 + 1, RB_SLOT_Y[0], RB_SLOT_Y[1], BOLT_Z - HOLE_D / 2, BOLT_Z + HOLE_D / 2))
    for x in PEG_XS[2:]:
        b = b.cut(cq.Workplane("XZ", origin=(x, T - 1, PEG_Z)).circle(PEG_HOLE_D / 2).extrude(-(PEG_HOLE_L + 1)))
    return b

def frame_bits():
    bits = [box(0, 20, 0, 20, 0, 510), box(0, 20, 20, 330, 68, 88),                 # left upright, left PSU rail
            box(0, 65, 20, 60, 88, 96), box(20, 38, 20, 60, 91, 100),               # left front PSU cradle envelope, PSU front feet
            box(23, 248, 3, 300, 100, 243),                                         # PSU body
            box(23, 338, 0, 3, 3, 86),                                              # bottom-drawer facia
            box(251, 271, 0, 23, 68, 247.5), box(271, 341, 3, 23, 68, 88), box(220, 251, 20, 60, 88, 96),   # sub-frame front upright (flush OR set back: y 0–23), tie, right PSU cradle reach
            box(273, 338, 0, 3, 91, 336), box(242, 268, 0, 3, 248, 336)]            # column facia, mini facia
    s = bits[0]
    for b in bits[1:]: s = s.union(b)
    return s.cut(box(20 - 1.75, 20.01, 10 - 5.9 / 2, 10 + 5.9 / 2, 60, 120))     # the left upright's inner-face slot mouth (the tongue sits in it)

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "sill")); os.makedirs(OUT, exist_ok=True)
    P, W, L, R, FR = panel(), window(), left_block(), right_block(), frame_bits()
    def vol(a, b): return a.intersect(b).val().Volume()
    print("--- proofs (mm3; 0 = clear) ---")
    print(f"panel vs frame {vol(P, FR):.3f}  window vs frame {vol(W, FR):.3f}  left block vs frame {vol(L, FR):.3f}  right block vs frame {vol(R, FR):.3f}")
    print(f"panel vs blocks (pegs in holes) {vol(P, L):.3f} / {vol(P, R):.3f}   window vs panel {vol(W, P):.3f}   blocks vs each other {vol(L, R):.3f}")
    print(f"pegs locate: panel shifted 0.5 x / z vs blocks {vol(P.translate((0.5, 0, 0)), L) + vol(P.translate((0.5, 0, 0)), R):.1f} / {vol(P.translate((0, 0, 0.5)), L) + vol(P.translate((0, 0, 0.5)), R):.1f}  (> 0)")
    print(f"left block: tongue x {LB_X0 - TONGUE_D}..{LB_X0} in the upright's slot mouth (y {BOLT_Y - TONGUE_W/2}..{BOLT_Y + TONGUE_W/2}); block back at y {LB_Y1}, cradle arm from y 20 -> button must fit in {LB_Y1 - 3:.1f} behind the panel's back")
    print(f"gaps: panel bottom {Z0} vs facia top 86 -> 1.0; panel top {Z1} vs PSU bottom 100 -> 1.0; panel right end {PX1} vs sub-frame upright 251 -> 0.3")
    # exports
    def export(part, name, rot=None, **kw):
        p = part if rot is None else part.rotate((0, 0, 0), rot[0], rot[1])
        bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin)); path = os.path.join(OUT, name + ".stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:22s} {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {part.val().Volume()/1000:.1f} cm3"); check(path, **kw)
    # panel + window standing on the bottom edge (frame z up stays up): as modelled
    # panel + window share ONE origin so they load as a multi-part object with the window in its cut-out
    bb = P.val().BoundingBox(); shift = (-bb.xmin, -bb.ymin, -bb.zmin)
    for part, name in ((P, "sill-panel-v2"), (W, "sill-panel-window-v2")):
        p = part.translate(shift); path = os.path.join(OUT, name + ".stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        b2 = part.val().BoundingBox(); print(f"{name:22s} {b2.xlen:.1f} x {b2.ylen:.1f} x {b2.zlen:.1f}  {part.val().Volume()/1000:.1f} cm3"); check(path, min_rest_frac=0.2, max_down_frac=1.0)
    export(L, "sill-block-left-v2", rot=((1, 0, 0), 90), min_rest_frac=0.3, max_down_frac=2.5)     # front face down; the cavity roof and hex-to-bore step are short bridges
    export(R, "sill-block-right-v2", rot=((1, 0, 0), 90), min_rest_frac=0.3, max_down_frac=1.2)    # front face down; the pocket roof is a 14 mm bridge
