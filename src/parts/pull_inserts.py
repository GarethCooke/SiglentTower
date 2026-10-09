# Pull inserts (D9, P6 ☑) — every front's pull is a separate dark-blue insert glued into a notch in the front's top edge:
#   bottom drawer   100 wide, slot 80   (parts/drawer/drawer-pull-insert-v1.stl, printed 2026-10-02)
#   column drawer    50 wide, slot 40   (column_facia.py; here as well)
#   mini slot        22 wide, slot 16   (the facia is 26 wide; notch 22.3 × 23.15 goes in mini_slot.py when that is modelled)
# The sled front bar's 120 × 6 top-edge notch is a finger notch in a 12 mm bar — the P6 pocket (17 deep) cannot live in it.
# It gets a blue LINER instead (sled_liner): an L of floor + front wall, 1.5 thick, glued into the notch so the blue shows on the
# bar's front face and the notch floor; the finger pulls on the wall, the glue line carries it to the bar. Trial — Gareth to judge. Geometry: P6 — face 3, slot 12 tall (JPULL_OPEN_H) starting 4 above the bottom, hook 5, pocket 17
# deep with a 30° floor, walls 2. Printed FACE DOWN; the pocket's back wall is a 7 mm bridge (P6 proved it).
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import JPULL_OPEN_H, JPULL_HOOK, JPULL_DEPTH, JPULL_FLOOR_DEG, JPULL_WALL, JPULL_INSERT_CLR
FT, SLOT_Z = 3.0, 4.0
w, d = JPULL_WALL, JPULL_DEPTH; t = math.tan(math.radians(JPULL_FLOOR_DEG))
H = SLOT_Z + JPULL_OPEN_H + JPULL_HOOK                       # 21: cavity top; the insert is H + w = 23 tall
INSERTS = {"column": (50.0, 40.0), "mini": (22.0, 16.0)}      # name: (insert width, slot width)
LINER_T = 1.5

def prism(pts, x0, x1):
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))

def insert(W, SW):
    """As used: face at y 0..FT (front at y = 0), bottom at z 0, x 0..W."""
    z_floor = SLOT_Z - w
    cav = [(FT, z_floor), (FT + d, z_floor + d * t), (FT + d, H), (FT, H)]
    outer = [(FT, z_floor - w), (FT + d + w, z_floor - w + (d + w) * t), (FT + d + w, H + w), (FT, H + w)]
    face = cq.Workplane("XY").box(W, FT, H + w, centered=False)
    slot = cq.Workplane("XY").box(SW, FT + 2, JPULL_OPEN_H, centered=False).translate(((W - SW) / 2, -1, SLOT_Z))
    return face.union(prism(outer, (W - SW) / 2 - w, (W + SW) / 2 + w), clean=True).cut(slot).cut(prism(cav, (W - SW) / 2, (W + SW) / 2)).clean()

def sled_liner():
    """As used in the bar's notch: x 0..W (notch 120 wide, 0.15 clear per side), y 0 = bar front face, z 0 = notch floor."""
    from parts.sled_bars import NOTCH_W, NOTCH_D, BAR_Y1
    W = NOTCH_W - 2 * JPULL_INSERT_CLR
    floor = cq.Workplane("XY").box(W, BAR_Y1 - JPULL_INSERT_CLR, LINER_T, centered=False)
    wall = cq.Workplane("XY").box(W, LINER_T, NOTCH_D, centered=False)
    return floor.union(wall).clean()

def printable(s):
    p = s.rotate((0, 0, 0), (1, 0, 0), 90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "inserts")); os.makedirs(OUT, exist_ok=True)
    plate = None; x = 0.0
    for name, (W, SW) in INSERTS.items():
        p = printable(insert(W, SW)); bb = p.val().BoundingBox(); path = os.path.join(OUT, f"pull-insert-{name}-v1.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"pull-insert-{name:7s} {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  (notch {W + 0.3:.1f} x {H + w + 0.15:.2f})")
        check(path, max_down_frac=0.6)
        q = p.translate((x, 0, 0)); plate = q if plate is None else plate.add(q); x += bb.xlen + 8
    liner = sled_liner(); path = os.path.join(OUT, "sled-bar-pull-liner-v1.stl")       # prints floor down as modelled
    cq.exporters.export(liner, path, tolerance=0.01, angularTolerance=0.1); check(path, max_down_frac=0.6)
    plate = plate.add(liner.translate((0, 32, 0)))
    cq.exporters.export(plate, os.path.join(OUT, "pull-inserts-plate-v2.stl"), tolerance=0.01, angularTolerance=0.1)
    print("plate: pull-inserts-plate-v2.stl — column + mini inserts face down, sled-bar liner floor down; dark blue PETG, no brim")
