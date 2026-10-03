# Rear box (HANDOVER §4/§6, ROADMAP Stage 6, D2's joint via P7 ☑) — the meter box that rides the sled on the two cross bars
# and comes out sideways to the right. World frame as sled_beam.py. 291 × 135 × 110 outside (x 50–341, y 195–330,
# z 346–456), floor 3, walls 2.4, full rear and side walls, a 20 mm lip across the front (reach in from the front once the
# scope is pulled out). It sits on the cross bars' tops (346) between their guide lips (front lip y 190–195, rear lip
# y 330–335, both z 346–356): the lips hold it fore-aft, nothing holds it sideways — that is how it leaves.
# Two halves (bed limit), split at x 195.5, joined exactly like the drawer quarters: floor puzzle-dovetail tabs along the
# seam (owner alternates, none within CENTRE_KEEP of the walls' bosses), a vertical sliding dovetail at the rear wall
# crossing (12 × 8 boss, LEFT half male) and another at the front lip crossing (20 tall). The RIGHT half drops vertically
# onto the left. CA the seam; the box is lifted by its walls so the joint sees little load.
# Print: each half floor down as exported (145.5 × 135 footprint, 110 tall), dark grey PETG, 5 mm outer brim (tall thin
# walls), no support — every tab, boss and rib is a vertical wall or an in-plane feature. ~95 cm³ each.
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import DOVETAIL_CLR as C
from parts.drawer_quarters import box, prism, trapezoid, TAB_NECK, TAB_HEAD, TAB_LEN, TAB_PITCH, RIB_NECK, RIB_HEAD, RIB_DEPTH, BOSS_L, BOSS_T

X0, X1, Y0, Y1, Z0, H = 50.0, 341.0, 195.0, 330.0, 346.0, 110.0
WALL, FLOOR, LIP_H = 2.4, 3.0, 20.0
SEAM = (X0 + X1) / 2                                  # 195.5
KEEP = 15.0                                           # no floor tab within this of a wall-crossing boss

def floor_tabs():
    """(yc, owner) along the seam; owner 'L' points +x into the right half. Clear of the bosses at both ends."""
    out = []
    y_first = Y0 + WALL + BOSS_T + KEEP
    j = 0
    while True:
        yc = y_first + TAB_PITCH * j
        if yc + TAB_HEAD / 2 > Y1 - WALL - BOSS_T - KEEP: break
        out.append((yc, "L" if j % 2 == 0 else "R")); j += 1
    return out

def half(side):
    """side 'L' (x X0..SEAM) or 'R' (SEAM..X1), world coordinates, as assembled."""
    x0, x1 = (X0, SEAM) if side == "L" else (SEAM, X1)
    sgn = +1 if side == "L" else -1                   # my tabs / ribs point across the seam
    p = box(x0, x1, Y0, Y1, Z0, Z0 + FLOOR)
    p = p.union(box(x0, x1, Y1 - WALL, Y1, Z0, Z0 + H))                       # rear wall
    p = p.union(box(x0, x1, Y0, Y0 + WALL, Z0, Z0 + LIP_H))                   # front lip
    if side == "L": p = p.union(box(X0, X0 + WALL, Y0, Y1, Z0, Z0 + H))        # side walls
    else:           p = p.union(box(X1 - WALL, X1, Y0, Y1, Z0, Z0 + H))
    for yc, owner in floor_tabs():
        mine = (owner == side)
        if mine: p = p.union(prism(trapezoid(SEAM, yc, (sgn, "x"), TAB_NECK, TAB_HEAD, TAB_LEN), Z0, Z0 + FLOOR))
        else:    p = p.cut(prism(trapezoid(SEAM, yc, (-sgn, "x"), TAB_NECK, TAB_HEAD, TAB_LEN, grow=C), Z0 - 1, Z0 + FLOOR + 1))
    # wall crossings: boss inboard of the wall, rib on the LEFT half, slot (open to the floor) on the right
    for (yb0, yb1, zt) in ((Y1 - WALL - BOSS_T, Y1 - WALL, Z0 + H), (Y0 + WALL, Y0 + WALL + BOSS_T, Z0 + LIP_H)):
        xb0, xb1 = (SEAM - BOSS_L, SEAM) if side == "L" else (SEAM, SEAM + BOSS_L)
        p = p.union(box(xb0, xb1, yb0, yb1, Z0, zt))
        mid = (yb0 + yb1) / 2
        if side == "L": p = p.union(prism(trapezoid(SEAM, mid, (+1, "x"), RIB_NECK, RIB_HEAD, RIB_DEPTH), Z0, zt))
        else:           p = p.cut(prism(trapezoid(SEAM, mid, (+1, "x"), RIB_NECK, RIB_HEAD, RIB_DEPTH, grow=C), Z0 - 1, zt + 1))   # slot points the same way as the rib
    return p

def for_print(part):
    bb = part.val().BoundingBox()
    return part.translate((-bb.xmin, -bb.ymin, -bb.zmin))

PARTS = {"rear-box-left": lambda: half("L"), "rear-box-right": lambda: half("R")}

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    for name, fn in PARTS.items():
        p = for_print(fn()); bb = p.val().BoundingBox(); path = os.path.join(OUT, f"{name}-v1.stl")
        cq.exporters.export(p, path, tolerance=0.02, angularTolerance=0.2)
        print(f"{name:16s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f}  {p.val().Volume()/1000:6.1f} cm3  {'fits' if bb.xlen <= 250 and bb.ylen <= 250 else 'TOO BIG'}")
        check(path)
    print("floor tabs at y:", [round(y, 1) for y, _ in floor_tabs()])
