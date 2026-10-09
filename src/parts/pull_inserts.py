# Pull inserts v2 (D9, P6 ☑) — every front's pull is a separate dark-blue insert dropped into a notch in the front's top edge.
# v1 held in the notch sideways and downward only; a forward pull went through the glue on the notch's three 3 mm edges in
# shear (Gareth 2026-10-09: "it'll last less than 10 secs"). v2 adds a FLANGE: a 2 mm plate behind the face that steps out
# past the notch at the sides (ears) and, where the drawer body allows, below it (lip); it sits flat against the facia's
# back, glued face to face, and a forward pull bears on the facia itself — the glue only stops it lifting out.
#   bottom drawer   face 100 (slot 80), ears 10, no lip (the 60-tall body's front wall is behind the facia below the notch)
#   column          face 50 (slot 40), ears 3.5 (the facia is 65 wide, the body 64 with 2.4 walls), lip 8 — the body's
#                   front wall gets a window: its top 29 mm between the side walls (column_drawer.py WIN_D; v1 print: cut)
#   mini slot       face 22 (slot 16), ears 1.5 (facia 26), lip 8 — mini_slot.py, when modelled, gets the notch 22.3 × 23.15
#                   and a body-wall window ≥ 25 wide × 29 deep
# The sled front bar's 120 × 6 notch cannot hold the 17-deep pocket; it gets a 1.5 mm L-shaped LINER (floor + front wall).
# Geometry: P6 — face 3, slot 12 tall (JPULL_OPEN_H) from 4 above the bottom, hook 5, pocket 17 deep, 30° floor, walls 2.
# Print FACE DOWN; the ears/lip are 2 mm plates 3 mm above the bed, so: supports ON, "on build plate only" (3 mm tall).
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import JPULL_OPEN_H, JPULL_HOOK, JPULL_DEPTH, JPULL_FLOOR_DEG, JPULL_WALL, JPULL_INSERT_CLR
FT, SLOT_Z, FL_T = 3.0, 4.0, 2.0
w, d = JPULL_WALL, JPULL_DEPTH; t = math.tan(math.radians(JPULL_FLOOR_DEG))
H = SLOT_Z + JPULL_OPEN_H + JPULL_HOOK                       # 21: cavity top; the face is H + w = 23 tall
INSERTS = {"bottom": (100.0, 80.0, 10.0, 0.0, 0.0, ((36.0, 64.0),)), "column": (50.0, 40.0, 2.5, 8.0, -11.0, ()), "mini": (22.0, 16.0, 1.5, 8.0, -11.0, ())}   # face W, slot, ear, lip, wall top (insert z), leg gaps
WALL_T, LEG_CLR, LEG_L = 2.4, 0.3, 20.0
LINER_T = 1.5

def prism(pts, x0, x1):
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))

def insert(W, SW, ear, lip, wall_top, leg_gaps=()):
    """As used: face x 0..W, y 0..FT (front at y 0), z 0..H+w; flange behind it at y FT..FT+FL_T, x -ear..W+ear, z -lip..H+w;
    bridge over the body wall's top (at z wall_top) and a leg LEG_L down its inside, the flange's full width."""
    z_floor = SLOT_Z - w
    cav = [(FT, z_floor), (FT + d, z_floor + d * t), (FT + d, H), (FT, H)]
    outer = [(FT, z_floor - w), (FT + d + w, z_floor - w + (d + w) * t), (FT + d + w, H + w), (FT, H + w)]
    face = cq.Workplane("XY").box(W, FT, H + w, centered=False)
    flange = cq.Workplane("XY").box(W + 2 * ear, FL_T, H + w + lip, centered=False).translate((-ear, FT, -lip))
    slot = cq.Workplane("XY").box(SW, FT + 2, JPULL_OPEN_H, centered=False).translate(((W - SW) / 2, -1, SLOT_Z))
    z0 = wall_top if lip == 0 else -lip - FL_T                       # bridge bottom: on the wall top, or 1 above the hand-cut edge
    yb = FT + WALL_T + LEG_CLR + FL_T                                 # back of the leg: facia 3, then the wall 2.4, 0.3 clear
    bridge = cq.Workplane("XY").box(W + 2 * ear, yb - FT, FL_T, centered=False).translate((-ear, FT, z0))
    leg = cq.Workplane("XY").box(W + 2 * ear, FL_T, z0 - (wall_top - LEG_L), centered=False).translate((-ear, yb - FL_T, wall_top - LEG_L))
    for gx0, gx1 in leg_gaps: leg = leg.cut(cq.Workplane("XY").box(gx1 - gx0, 20, 100, centered=False).translate((gx0, yb - FL_T - 1, wall_top - LEG_L - 1)))
    s = face.union(flange).union(bridge).union(leg).union(prism(outer, (W - SW) / 2 - w, (W + SW) / 2 + w), clean=True)
    return s.cut(slot).cut(prism(cav, (W - SW) / 2, (W + SW) / 2)).clean()

def sled_liner():
    """As used in the bar's notch: x 0..W (notch 120 wide, 0.15 clear per side), y 0 = bar front face, z 0 = notch floor."""
    from parts.sled_bars import NOTCH_W, NOTCH_D, BAR_Y1
    W = NOTCH_W - 2 * JPULL_INSERT_CLR
    return cq.Workplane("XY").box(W, BAR_Y1 - JPULL_INSERT_CLR, LINER_T, centered=False).union(
        cq.Workplane("XY").box(W, LINER_T, NOTCH_D, centered=False)).clean()

def printable(s):
    p = s.rotate((0, 0, 0), (1, 0, 0), 90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "inserts")); os.makedirs(OUT, exist_ok=True)
    plate = None; x = 0.0
    for name, (W, SW, ear, lip, wt, gaps) in INSERTS.items():
        p = printable(insert(W, SW, ear, lip, wt, gaps)); bb = p.val().BoundingBox(); path = os.path.join(OUT, f"pull-insert-{name}-v2.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"pull-insert-{name:7s}-v2 {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  (notch {W + 0.3:.1f} x {H + w + 0.15:.2f}, flange {W + 2*ear:.0f} wide, leg to z {wt - LEG_L:.0f})")
        check(path, min_rest_frac=0.2, max_down_frac=4.0)   # ears + leg (z 3 and z 5.7) print on build-plate supports; z 20 is the P6 7 mm bridge
        q = p.translate((x, 0, 0)); plate = q if plate is None else plate.add(q); x += bb.xlen + 8
    liner = sled_liner(); path = os.path.join(OUT, "sled-bar-pull-liner-v1.stl")
    cq.exporters.export(liner, path, tolerance=0.01, angularTolerance=0.1); check(path, max_down_frac=0.6)
    plate = plate.add(liner.translate((0, 62, 0)))
    cq.exporters.export(plate, os.path.join(OUT, "pull-inserts-plate-v3.stl"), tolerance=0.01, angularTolerance=0.1)
    print("plate: pull-inserts-plate-v3.stl — bottom/column/mini inserts v2 face down (supports on build plate only), liner floor down; dark blue PETG")

    # proofs — each insert in its facia's notch, flange flat on the facia's back, body clear; forward shift now collides
    from parts import drawer_facia as dfa, drawer_quarters as dq, column_facia as cfa, column_drawer as cd
    def vol(a, b): return a.intersect(b).val().Volume()
    W, SW, ear, lip, wt, gaps = INSERTS["bottom"]; ins = insert(W, SW, ear, lip, wt, gaps).translate(((dfa.FW - W) / 2, -FT, dfa.FH - H - w)); fa = dfa.facia()
    body = dq.quarter(1).union(dq.quarter(2))
    print(f"bottom: vs facia {vol(fa, ins):.3f}  vs body {vol(body, ins):.3f}  shift fwd 0.5 {vol(fa, ins.translate((0, -0.5, 0))):.1f}  left 0.5 {vol(fa, ins.translate((-0.5, 0, 0))):.1f}  down 0.5 facia {vol(fa, ins.translate((0, 0, -0.5))):.1f} body {vol(body, ins.translate((0, 0, -0.5))):.1f}  mm3")
    W, SW, ear, lip, wt, gaps = INSERTS["column"]; ins = insert(W, SW, ear, lip, wt).translate((cfa.XM - W / 2, -FT, cfa.FH - H - w)); fa = cfa.facia(); body = cd.drawer()
    bb = ins.val().BoundingBox()
    print(f"column: vs facia {vol(fa, ins):.3f}  vs body {vol(body, ins):.3f}  shift fwd 0.5 {vol(fa, ins.translate((0, -0.5, 0))):.1f}  left 0.5 {vol(fa, ins.translate((-0.5, 0, 0))):.1f}  down 0.5 {vol(fa, ins.translate((0, 0, -0.5))):.1f} mm3;  flange x {bb.xmin:.2f}..{bb.xmax:.2f} (walls 2.4 / 61.6), z {bb.zmin:.0f}..{bb.zmax:.0f}")
    W, SW, ear, lip, wt, gaps = INSERTS["mini"]; NW, NH = W + 2 * JPULL_INSERT_CLR, H + w + JPULL_INSERT_CLR
    fa = cq.Workplane("XY").box(26, FT, 100, centered=False).cut(cq.Workplane("XY").box(NW, FT + 2, NH, centered=False).translate(((26 - NW) / 2, -1, 100 - NH)))
    ins = insert(W, SW, ear, lip, wt).translate(((26 - W) / 2, 0, 100 - H - w))
    print(f"mini (stub facia): vs facia {vol(fa, ins):.3f}  shift fwd 0.5 {vol(fa, ins.translate((0, -0.5, 0))):.1f}  left 0.5 {vol(fa, ins.translate((-0.5, 0, 0))):.1f} mm3")
