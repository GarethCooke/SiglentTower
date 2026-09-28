# drawer_quarters.py — bottom drawer 315 x 300 x 60 as four quarters (ROADMAP D2, drawer-quarters-v1.pdf).
# Frame: x to the right, y rearward (front face at y = 0), z up; floor top at z = FLOOR. All mm.
# quarter(i) builds Q1..Q4 (front-left, front-right, rear-left, rear-right) with:
#   - floor puzzle-dovetail tabs and sockets along both seams (owner alternates, none within CENTRE_KEEP of the cross)
#   - vertical sliding dovetails at the four wall crossings (rib on the piece that goes down first; slot on the other)
#   - outer walls
# quarter(i, production=True) is the PRODUCTION pass (2026-09-28, v1): the coupon geometry above plus
#   - the runner groove (drawer_runner.groove_cut, P3 geometry) in a 10 x 20 boss along each OUTER side wall, closed at the
#     front wall, open at the rear so the runner's rib enters from behind; the left/right wall-crossing dovetails rise to
#     z 20-60 (PRINT-RULES §2) because the groove would otherwise cut through them
#   - four facia screw pads on the inside of the front wall (Q1 and Q2): M3 clearance holes (teardrop, axis y) through
#     wall + pad, M3 x 14 button-heads from inside the drawer into the facia's back (facia carries Ø2.6 blind holes)
# crop(part, box) returns the section of a quarter inside a box — this is how the P7 coupon is a literal piece of the part.
# Prints floor down as exported (parts/drawer/drawer-Q<i>-v1.stl), black PETG, no brim, no support; one quarter per plate
# (165.5 x 158 with its tabs — two do not fit the 256 bed in any orientation).
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import cadquery as cq
from fit import DOVETAIL_CLR as C

DW, DD, DH = 315.0, 300.0, 60.0
WALL, FLOOR = 2.4, 3.0
SEAM_X, SEAM_Y = 157.5, 150.0
TAB_NECK, TAB_HEAD, TAB_LEN, TAB_PITCH, CENTRE_KEEP = 12.0, 18.0, 8.0, 30.0, 15.0
TAB_START = 25.0   # first tab centre from the wall: clears the 8 mm wall-crossing boss (2.4 + 8 + 9 = 19.4 minimum)
RIB_NECK, RIB_HEAD, RIB_DEPTH = 4.0, 6.0, 3.0
BOSS_L, BOSS_T = 12.0, 8.0          # boss along the wall x thickness inboard of the wall
# production pass
from parts.drawer_runner import groove_cut, BOSS_T as GROOVE_BOSS_T, BOSS_H as GROOVE_BOSS_H   # 10 x 20 along the outer side walls
SIDE_RIB_Z0 = GROOVE_BOSS_H         # left/right wall-crossing dovetails run z 20-60, above the groove boss
PAD_W, PAD_T = 14.0, 5.6            # facia screw pad inboard of the front wall, rising from the floor (wall 2.4 + pad 5.6 = 8 under the head)
PAD_Z, PAD_Z1 = 20.0, 27.0          # screw centre height (drawer z; frame z 23 — below the pull insert and the logo), pad top
PAD_X = (40.0, 117.5, 197.5, 275.0) # screw x, symmetric about the seam; two per front quarter
SCREW_HOLE_D = 3.4                  # M3 clearance, teardrop (axis along y = horizontal in the print)

# ---------- primitives ----------
def prism(pts, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def trapezoid(seam, along, dirn, neck, head, length, grow=0.0):
    """Trapezoid in XY. seam: coordinate of the seam line; along: coordinate along the seam (tab centre);
    dirn: (+1/-1, axis) where axis 'x' means the tab points in x (seam is x = const)."""
    sgn, axis = dirn
    n, h, L = neck / 2 + grow, head / 2 + grow, length + grow
    s0 = seam - (1.0 if grow else 0.0) * sgn      # a socket starts 1 mm outside the seam so the cut is clean
    if axis == "x":
        pts = [(s0, along - n), (seam + sgn * L, along - h), (seam + sgn * L, along + h), (s0, along + n)]
    else:
        pts = [(along - n, s0), (along - h, seam + sgn * L), (along + h, seam + sgn * L), (along + n, s0)]
    return pts

# ---------- tab schedule (matches drawer_quarters_gen.py) ----------
def x_seam_tabs():
    """tabs along the seam x = SEAM_X: list of (yc, owner) with owner 'L' (left quarter, points +x) or 'R'."""
    out = []
    for j in range(10):
        yc = TAB_START + TAB_PITCH * j
        if yc + TAB_HEAD / 2 > DD - WALL or abs(yc - SEAM_Y) < CENTRE_KEEP + TAB_HEAD / 2: continue
        out.append((yc, "L" if j % 2 == 0 else "R"))
    return out

def y_seam_tabs():
    """tabs along the seam y = SEAM_Y: (xc, owner) with 'F' (front quarter, points +y) or 'B' (rear, points -y)."""
    out = []
    for j in range(11):
        xc = TAB_START + TAB_PITCH * j
        if xc + TAB_HEAD / 2 > DW - WALL or abs(xc - SEAM_X) < CENTRE_KEEP + TAB_HEAD / 2: continue
        out.append((xc, "F" if j % 2 == 0 else "B"))
    return out

QUARTERS = {  # i: (x0, x1, y0, y1)
    1: (0.0, SEAM_X, 0.0, SEAM_Y), 2: (SEAM_X, DW, 0.0, SEAM_Y),
    3: (0.0, SEAM_X, SEAM_Y, DD),  4: (SEAM_X, DW, SEAM_Y, DD)}

# wall crossings: (wall, seam) -> which quarter is male. Sheet: Q2 onto Q1, Q3 onto Q1, Q4 onto Q2 + Q3.
# front wall / x seam: Q1 male, Q2 female. rear wall / x seam: Q3 male, Q4 female.
# left wall / y seam:  Q1 male, Q3 female. right wall / y seam: Q2 male, Q4 female.
MALE = {("front", 1): True, ("front", 2): False, ("rear", 3): True, ("rear", 4): False,
        ("left", 1): True, ("left", 3): False, ("right", 2): True, ("right", 4): False}

def crossing_boss_and_joint(wall, i, production=False):
    """Return (boss_solid, rib_solid_or_None, slot_cut_or_None) for quarter i at the named wall crossing."""
    x0, x1, y0, y1 = QUARTERS[i]
    male = MALE[(wall, i)]
    if wall in ("front", "rear"):                 # seam x = SEAM_X, boss inboard of a wall that runs along x
        yb0, yb1 = (WALL, WALL + BOSS_T) if wall == "front" else (DD - WALL - BOSS_T, DD - WALL)
        xb0, xb1 = (SEAM_X - BOSS_L, SEAM_X) if x1 == SEAM_X else (SEAM_X, SEAM_X + BOSS_L)
        boss = box(xb0, xb1, yb0, yb1, 0, DH)
        sgn = +1 if x1 == SEAM_X else -1           # male rib points out of the piece across the seam
        mid = (yb0 + yb1) / 2
        rib = prism(trapezoid(SEAM_X, mid, (sgn, "x"), RIB_NECK, RIB_HEAD, RIB_DEPTH), 0, DH) if male else None
        slot = prism(trapezoid(SEAM_X, mid, (-sgn, "x"), RIB_NECK, RIB_HEAD, RIB_DEPTH, grow=C), -1, DH + 1) if not male else None
    else:                                          # seam y = SEAM_Y, wall runs along y
        xb0, xb1 = (WALL, WALL + BOSS_T) if wall == "left" else (DW - WALL - BOSS_T, DW - WALL)
        yb0, yb1 = (SEAM_Y - BOSS_L, SEAM_Y) if y1 == SEAM_Y else (SEAM_Y, SEAM_Y + BOSS_L)
        boss = box(xb0, xb1, yb0, yb1, 0, DH)
        sgn = +1 if y1 == SEAM_Y else -1
        mid = (xb0 + xb1) / 2
        rib = prism(trapezoid(SEAM_Y, mid, (sgn, "y"), RIB_NECK, RIB_HEAD, RIB_DEPTH), 0, DH) if male else None
        if male and production:   # rib z 20-60 with a 45° underside (it stands off the boss face across the seam, rule 4)
            zb = SIDE_RIB_Z0 - RIB_DEPTH
            wedge = (cq.Workplane("YZ").polyline([(SEAM_Y, zb), (SEAM_Y + sgn * (RIB_DEPTH + 1), zb),
                                                  (SEAM_Y + sgn * (RIB_DEPTH + 1), zb + RIB_DEPTH + 1)]).close()
                     .extrude(xb1 - xb0 + 2).translate((xb0 - 1, 0, 0)))
            rib = rib.intersect(box(xb0 - 1, xb1 + 1, SEAM_Y - 10, SEAM_Y + 10, zb, DH)).cut(wedge)
        # the slot stays open to the floor: the rib enters it from below when the rear quarter drops onto the front one
        slot = prism(trapezoid(SEAM_Y, mid, (-sgn, "y"), RIB_NECK, RIB_HEAD, RIB_DEPTH, grow=C), -1, DH + 1) if not male else None
    return boss, rib, slot

def quarter(i, production=False):
    x0, x1, y0, y1 = QUARTERS[i]
    part = box(x0, x1, y0, y1, 0, FLOOR)                                   # floor
    # outer walls
    if x0 == 0:  part = part.union(box(0, WALL, y0, y1, 0, DH))
    if x1 == DW: part = part.union(box(DW - WALL, DW, y0, y1, 0, DH))
    if y0 == 0:  part = part.union(box(x0, x1, 0, WALL, 0, DH))
    if y1 == DD: part = part.union(box(x0, x1, DD - WALL, DD, 0, DH))
    # floor tabs / sockets on the x seam
    on_left = (x1 == SEAM_X)
    for yc, owner in x_seam_tabs():
        if not (y0 <= yc <= y1): continue
        mine = (owner == "L") == on_left
        sgn = +1 if on_left else -1                                        # my tab points across the seam
        if mine: part = part.union(prism(trapezoid(SEAM_X, yc, (sgn, "x"), TAB_NECK, TAB_HEAD, TAB_LEN), 0, FLOOR))
        else:    part = part.cut(prism(trapezoid(SEAM_X, yc, (-sgn, "x"), TAB_NECK, TAB_HEAD, TAB_LEN, grow=C), -1, FLOOR + 1))
    # floor tabs / sockets on the y seam
    in_front = (y1 == SEAM_Y)
    for xc, owner in y_seam_tabs():
        if not (x0 <= xc <= x1): continue
        mine = (owner == "F") == in_front
        sgn = +1 if in_front else -1
        if mine: part = part.union(prism(trapezoid(SEAM_Y, xc, (sgn, "y"), TAB_NECK, TAB_HEAD, TAB_LEN), 0, FLOOR))
        else:    part = part.cut(prism(trapezoid(SEAM_Y, xc, (-sgn, "y"), TAB_NECK, TAB_HEAD, TAB_LEN, grow=C), -1, FLOOR + 1))
    # runner groove boss along the outer side wall (production) — before the crossings so their slot cuts go through it
    if production:
        gy0, gy1 = (WALL if y0 == 0 else y0), y1
        g = groove_cut(gy1 - gy0).translate((0, gy0, 0))
        if x0 == 0: part = part.union(box(0, GROOVE_BOSS_T, y0, y1, 0, GROOVE_BOSS_H))
        else:       part = part.union(box(DW - GROOVE_BOSS_T, DW, y0, y1, 0, GROOVE_BOSS_H)); g = g.mirror("YZ").translate((DW, 0, 0))
    # wall crossings
    walls = [("front" if y0 == 0 else "rear"), ("left" if x0 == 0 else "right")]
    for w in walls:
        boss, rib, slot = crossing_boss_and_joint(w, i, production)
        part = part.union(boss)
        if rib is not None:  part = part.union(rib)
        if slot is not None: part = part.cut(slot)
    if production:
        part = part.cut(g)     # the groove, closed at the front wall (starts at y = WALL), open at the rear for the runner's rib
        # facia screw pads on the inside of the front wall
        if y0 == 0:
            for xc in PAD_X:
                if not (x0 < xc < x1): continue
                part = part.union(box(xc - PAD_W / 2, xc + PAD_W / 2, WALL, WALL + PAD_T, 0, PAD_Z1))
                part = part.cut(teardrop_y(xc, PAD_Z, SCREW_HOLE_D / 2, -1, WALL + PAD_T + 1))
    return part

def teardrop_y(xc, zc, r, y0, y1):
    """Round hole of radius r along y (y0..y1) with a 45° peak on top so it prints without support (rule 4)."""
    a = r / 2 ** 0.5
    tri = cq.Workplane("XZ").polyline([(xc - a, zc + a), (xc, zc + r * 2 ** 0.5), (xc + a, zc + a)]).close().extrude(y1 - y0)
    cyl = cq.Workplane("XZ").center(xc, zc).circle(r).extrude(y1 - y0)
    return cyl.union(tri).translate((0, y1, 0))

def crop(part, x0, x1, y0, y1):
    return part.intersect(box(x0, x1, y0, y1, -5, DH + 5))

def production():
    """The four production quarters in drawer coordinates (as assembled)."""
    return {i: quarter(i, production=True) for i in range(1, 5)}

if __name__ == "__main__":
    # export: parts/drawer/drawer-Q<i>-v1.stl, each at the origin, floor on the bed, as printed
    HERE = os.path.dirname(os.path.abspath(__file__))
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "drawer")); os.makedirs(OUT, exist_ok=True)
    sys.path.insert(0, os.path.join(HERE, ".."))
    from printcheck import check
    for i, q in production().items():
        bb = q.val().BoundingBox()
        print(f"Q{i}: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  vol {q.val().Volume()/1000:.1f} cm3  "
              f"{'fits' if bb.xlen <= 250 and bb.ylen <= 250 else 'TOO BIG'}")
        out = os.path.join(OUT, f"drawer-Q{i}-v1.stl")
        cq.exporters.export(q.translate((-bb.xmin, -bb.ymin, -bb.zmin)), out, tolerance=0.02, angularTolerance=0.2)
        check(out)
