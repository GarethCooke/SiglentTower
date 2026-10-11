# Sill panel + end blocks (ROADMAP D10, Stage 8 trim): the grey strip that fills the reveal between the bottom-drawer
# facia (top z 86) and the PSU's front (bottom z 100), carrying the lighting button and its halo. Frame coordinates.
#
# Departures from D10 as written (2026-09-20), forced by what has been modelled since:
#   - The panel runs x 20–271, not 20–341: the column facia (x 273–338, z 91–336) now owns the right end of the band.
#     The panel's right end lies on the sub-frame's front upright (x 251–271, y 3–23), so the right end block sits just
#     left of that upright (x 226–251) and bolts sideways into its LEFT-face slot (y 13, z 93) — same pocket-from-the-front
#     arrangement as the left block, mirrored.
#   - The halo is a 14 × 12 translucent WINDOW (natural PETG, second colour) round the button, not a Ø10–14 ring: the strip
#     is only 12 tall and an 8 mm button's bezel is ~Ø10, so a ring would show 0.8 mm. The window shows 12 × 14 less the bezel.
#   - The button sits at x 78, not at the left end: the left PSU cradle's arm reaches x ~65 at y 20–60, z 88–96, so an 8 mm
#     button's ~20 mm body (thread + terminals) only fits behind the panel to the right of it. The left block is
#     16.5 deep (y 3–19.5) along the cradle and 25 deep (y 3–28) under the button and the pixel.
#   - The XIAO does not live in the block (12 × 25 × 17 cannot hold a 21 × 18 board and a button): the block holds the
#     button and the 5 mm pixel only; their 5 wires drop into the left PSU rail's inner slot as the USB lead does. XIAO
#     placement and the right strip's data route are Stage 8 decisions (see ROADMAP).
#   - No 4 × 4 groove in a 3 mm panel; the right strip's data run does not go behind the panel.
#   - The button is glued into its bore (no nut: a 13 AF M8 nut does not fit a 12 mm band).
#
# Parts:
#   PANEL   x 20–271 × y 0–3 × z 87–99, dark grey PETG. Ø8.4 button hole at (78, 93); window 14 × 12 at x 71–85 as a
#           separate STL (natural PETG) loaded as one multi-part object. Four Ø3.2 × 7 pegs on the back (x 24, 66, 249,
#           268.5; z 93) into the blocks. No holes through the front. Prints standing on its bottom edge.
#   LEFT BLOCK  x 20.3–90, z 87–99; y 3–19.5 (x < 70) / 3–28 (x 70–90). Against the left upright's inner face (x 20).
#           M5 × 10 along x at (y 10, z 93) into that face's slot (drop-in T-nut): Ø5.5 hole through the 7.7 wall, head in a
#           pocket x 28–42 × y 3–13 open to the FRONT (ball-end key from the front, before the panel goes on). Button bore
#           Ø8.4 along y at (78, 93) through; light cavity 20 × 8 × 3 (x 70–90, z 89–97, y 3–6) behind the window; pixel
#           bore Ø5.3 along y at (88, 93) from the rear face into the cavity; wire notch 6 × 4 at the bottom-rear corner.
#           Prints FRONT FACE DOWN (bores vertical, pocket and cavity open at the bed, M5 hole a horizontal teardrop).
#   RIGHT BLOCK x 226–251 × y 3–19 × z 87–99 against the sub-frame upright's left face (x 251): M5 × 10 along x at
#           (y 13, z 93) into that face's slot through the 7.7 right wall, head pocket x 229–243 open to the front.
#           Prints FRONT FACE DOWN like the left block.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from parts.drawer_quarters import box, teardrop_y

Z0, Z1, T = 87.0, 99.0, 3.0
PX0, PX1 = 20.0, 271.0
BTN_X, BTN_Z, BTN_HOLE_D = 78.0, 93.0, 8.4
WIN_X0, WIN_X1 = 71.0, 85.0
PEG_XS, PEG_Z, PEG_D, PEG_L, PEG_HOLE_D, PEG_HOLE_L = (24.0, 66.0, 229.0, 248.0), 93.0, 3.2, 7.0, 3.4, 7.5
LB_X0, LB_X1, LB_STEP_X, LB_Y1, LB_Y1_DEEP = 20.3, 90.0, 70.0, 19.5, 28.0
POCKET = (28.0, 42.0, 3.0, 13.0, 88.0, 98.0)
BOLT_Y, BOLT_Z, HOLE_D, CBORE_D, CBORE_H = 10.0, 93.0, 5.5, 9.0, 5.0
CAV = (70.0, 90.0, 3.0, 6.0, 89.0, 97.0)
LED_X, LED_D = 88.0, 5.3
NOTCH_W, NOTCH_H = 6.0, 4.0
RB_X0, RB_X1, RB_Y1 = 226.0, 250.7, 19.0
RB_POCKET, RB_BOLT_Y = (229.0, 243.0, 3.0, 16.0, 88.0, 98.0), 13.0   # the upright's left-face slot centre is y 13

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

def left_block():
    b = box(LB_X0, LB_STEP_X, T, LB_Y1, Z0, Z1).union(box(LB_STEP_X, LB_X1, T, LB_Y1_DEEP, Z0, Z1))
    x0, x1, y0, y1, z0, z1 = POCKET
    b = b.cut(box(x0, x1, y0 - 1, y1, z0, z1))                                                       # bolt-head pocket, open at the front
    b = b.cut(teardrop_x(BOLT_Y, BOLT_Z, HOLE_D / 2, LB_X0 - 1, x0 + 1))                              # M5 through the wall to the upright
    b = b.cut(cq.Workplane("XZ", origin=(BTN_X, LB_Y1_DEEP + 1, BTN_Z)).circle(BTN_HOLE_D / 2).extrude(LB_Y1_DEEP + 2))   # button bore
    x0, x1, y0, y1, z0, z1 = CAV
    b = b.cut(box(x0, x1, y0 - 1, y1, z0, z1))                                                       # light cavity behind the window
    b = b.cut(cq.Workplane("XZ", origin=(LED_X, LB_Y1_DEEP + 1, BTN_Z)).circle(LED_D / 2).extrude(LB_Y1_DEEP + 1 - CAV[3] + 0.5))   # pixel bore, rear -> cavity
    b = b.cut(box(LB_X1 - NOTCH_W - 2, LB_X1 - 2, LB_Y1_DEEP - 6, LB_Y1_DEEP + 1, Z0 - 1, Z0 + NOTCH_H))    # wire notch, bottom-rear corner
    for x in PEG_XS[:2]:
        b = b.cut(cq.Workplane("XZ", origin=(x, T - 1, PEG_Z)).circle(PEG_HOLE_D / 2).extrude(-(PEG_HOLE_L + 1)))
    return b

def right_block():
    b = box(RB_X0, RB_X1, T, RB_Y1, Z0, Z1)
    x0, x1, y0, y1, z0, z1 = RB_POCKET
    b = b.cut(box(x0, x1, y0 - 1, y1, z0, z1))                                                       # bolt-head pocket, open at the front
    b = b.cut(teardrop_x(RB_BOLT_Y, BOLT_Z, HOLE_D / 2, x1 - 1, RB_X1 + 1))                           # M5 through the right wall to the upright
    for x in PEG_XS[2:]:
        b = b.cut(cq.Workplane("XZ", origin=(x, T - 1, PEG_Z)).circle(PEG_HOLE_D / 2).extrude(-(PEG_HOLE_L + 1)))
    return b

def frame_bits():
    bits = [box(0, 20, 0, 20, 0, 510), box(0, 20, 20, 330, 68, 88),                 # left upright, left PSU rail
            box(0, 65, 20, 60, 88, 96), box(20, 38, 20, 60, 91, 100),               # left front PSU cradle envelope, PSU front feet
            box(23, 248, 3, 300, 100, 243),                                         # PSU body
            box(23, 338, 0, 3, 3, 86),                                              # bottom-drawer facia
            box(251, 271, 3, 23, 68, 247.5), box(271, 341, 3, 23, 68, 88), box(220, 251, 20, 60, 88, 96),   # sub-frame front upright + tie, right PSU cradle reach
            box(273, 338, 0, 3, 91, 336), box(242, 268, 0, 3, 248, 336)]            # column facia, mini facia
    s = bits[0]
    for b in bits[1:]: s = s.union(b)
    return s

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "sill")); os.makedirs(OUT, exist_ok=True)
    P, W, L, R, FR = panel(), window(), left_block(), right_block(), frame_bits()
    def vol(a, b): return a.intersect(b).val().Volume()
    print("--- proofs (mm3; 0 = clear) ---")
    print(f"panel vs frame {vol(P, FR):.3f}  window vs frame {vol(W, FR):.3f}  left block vs frame {vol(L, FR):.3f}  right block vs frame {vol(R, FR):.3f}")
    print(f"panel vs blocks (pegs in holes) {vol(P, L):.3f} / {vol(P, R):.3f}   window vs panel {vol(W, P):.3f}   blocks vs each other {vol(L, R):.3f}")
    print(f"pegs locate: panel shifted 0.5 x / z vs blocks {vol(P.translate((0.5, 0, 0)), L) + vol(P.translate((0.5, 0, 0)), R):.1f} / {vol(P.translate((0, 0, 0.5)), L) + vol(P.translate((0, 0, 0.5)), R):.1f}  (> 0)")
    print(f"left block vs left upright face: block x0 {LB_X0} (upright inner face x 20); cradle clearance: deep part starts x {LB_STEP_X} (cradle reaches ~65)")
    print(f"gaps: panel bottom {Z0} vs facia top 86 -> 1.0; panel top {Z1} vs PSU bottom 100 -> 1.0; panel right end {PX1} vs column facia 273 -> 2.0")
    # exports
    def export(part, name, rot=None, **kw):
        p = part if rot is None else part.rotate((0, 0, 0), rot[0], rot[1])
        bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin)); path = os.path.join(OUT, name + ".stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:22s} {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {part.val().Volume()/1000:.1f} cm3"); check(path, **kw)
    # panel + window standing on the bottom edge (frame z up stays up): as modelled
    export(P, "sill-panel-v1", min_rest_frac=0.2, max_down_frac=1.0)     # standing on its 3 mm edge, as every facia
    export(W, "sill-panel-window-v1", min_rest_frac=0.2, max_down_frac=1.0)
    export(L, "sill-block-left-v1", rot=((1, 0, 0), 90), min_rest_frac=0.3, max_down_frac=1.0)     # front face (y 3) down: y -> -z
    export(R, "sill-block-right-v1", rot=((1, 0, 0), 90), min_rest_frac=0.3, max_down_frac=1.2)    # front face down; the pocket roof is a 14 mm bridge
