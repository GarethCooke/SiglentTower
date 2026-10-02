# Bottom-drawer facia + pull insert (HANDOVER §6/§8, ROADMAP D3 + D9, P6 ☑). Drawer coordinates as drawer_quarters.py
# (x from the left wall face, y rearward from the body's front face, z from the drawer bottom); the facia sits in front of
# the body at y −3..0 (frame y 0–3, flush with the uprights) and spans frame x 23–338 (drawer x 0–315), frame z 3–86
# (drawer z 0–83).
#   facia      315 × 3 × 83, dark grey PETG. Top-edge NOTCH 100.3 wide × 23.15 deep for the pull insert (D9), centred.
#              Four Ø2.5 × 2.3 blind holes in its back face at the body's screw pads (x 40 / 117.5 / 197.5 / 275, z 20):
#              M3 × 10 from inside the drawer (wall 2.4 + pad 5.6 = 8 under the head, 2 into the facia) — CA the facia
#              to the wall and pads as well; the screws are location while it cures, not the structure.
#              LOGO: the IguanaWare iguana (logo.py, 58.7 × 21.1, head right) inlaid 0.8 deep top-right, dark blue PETG
#              — exported as TWO STLs (facia with the recess, logo plate) to be loaded as one multi-part object.
#   insert     100 × 3 face, slot 80 × 12 (JPULL_OPEN_H), hook 5, pocket 17 deep, floor 30°: the P6 geometry at 100 wide,
#              dark blue PETG, printed face down; glued into the notch flush front and top.
# Print: facia STANDING ON ITS BOTTOM EDGE on the diagonal (D3) — 315 × 3 footprint, 83 tall; the notch opens upward,
# the screw holes are horizontal teardrops, the logo recess is a vertical-wall feature. No brim needed on a 315 × 3 edge
# with the skirt off? It IS needed: a 3 mm edge 315 long wants a brim — outer only, 5 mm (nothing fit-critical on the
# facia's edges except the notch, which is at the top).
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import JPULL_OPEN_H, JPULL_HOOK, JPULL_DEPTH, JPULL_FLOOR_DEG, JPULL_WALL, JPULL_INSERT_CLR
from parts.drawer_quarters import box, PAD_X, PAD_Z, DW
from logo import logo_solid

FW, FT, FH = DW, 3.0, 83.0                          # facia width, thickness, height
PULL_W, SLOT_W, SLOT_Z = 100.0, 80.0, 4.0           # insert width, slot width, slot bottom above the insert bottom
SCREW_D, SCREW_DEPTH = 2.5, 2.3                     # blind holes for M3 x 10 (0.7 skin stays on the front face)
LOGO_W, LOGO_H, LOGO_DEPTH = 60.0, 30.0, 0.8
LOGO_POS = (240.0, 48.0)                            # bottom-left of the logo's box on the facia (top-right, clear of the notch)
w, d = JPULL_WALL, JPULL_DEPTH; t = math.tan(math.radians(JPULL_FLOOR_DEG))
H = SLOT_Z + JPULL_OPEN_H + JPULL_HOOK              # 21: cavity top; insert is H + w = 23 tall
NOTCH_W, NOTCH_H = PULL_W + 2 * JPULL_INSERT_CLR, H + w + JPULL_INSERT_CLR     # 100.3 × 23.15

def prism(pts, x0, x1):
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))

def insert():
    """Pull insert as used: face at y −3..0, bottom at z FH − H − w, pocket reaching back through the body's front wall."""
    z_floor = SLOT_Z - w
    cav = [(FT, z_floor), (FT + d, z_floor + d * t), (FT + d, H), (FT, H)]
    outer = [(FT, z_floor - w), (FT + d + w, z_floor - w + (d + w) * t), (FT + d + w, H + w), (FT, H + w)]
    face = cq.Workplane("XY").box(PULL_W, FT, H + w, centered=False)
    slot = cq.Workplane("XY").box(SLOT_W, FT + 2, JPULL_OPEN_H, centered=False).translate(((PULL_W - SLOT_W) / 2, -1, SLOT_Z))
    pocket = prism(outer, (PULL_W - SLOT_W) / 2 - w, (PULL_W + SLOT_W) / 2 + w)
    cavity = prism(cav, (PULL_W - SLOT_W) / 2, (PULL_W + SLOT_W) / 2)
    s = face.union(pocket, clean=True).cut(slot).cut(cavity).clean()
    return s.translate(((FW - PULL_W) / 2, -FT, FH - H - w))

def teardrop_y(xc, zc, r, y0, y1):
    a = r / 2 ** 0.5
    tri = cq.Workplane("XZ").polyline([(xc - a, zc + a), (xc, zc + r * 2 ** 0.5), (xc + a, zc + a)]).close().extrude(y1 - y0)
    return cq.Workplane("XZ").center(xc, zc).circle(r).extrude(y1 - y0).union(tri).translate((0, y1, 0))

def logo_plate():
    lg = logo_solid(LOGO_W, LOGO_H, LOGO_DEPTH)                       # in XY, z 0..0.8, from (0, 0)
    bb = lg.val().BoundingBox()
    lg = lg.rotate((0, 0, 0), (1, 0, 0), 90)                          # XY -> XZ, thickness along -y: y −0.8..0
    lg = lg.translate((LOGO_POS[0], -FT + LOGO_DEPTH, LOGO_POS[1]))   # sits in the front face: y −3..−2.2
    return lg

def facia():
    f = box(0, FW, -FT, 0, 0, FH)
    c = JPULL_INSERT_CLR
    f = f.cut(box((FW - NOTCH_W) / 2, (FW + NOTCH_W) / 2, -FT - 1, 1, FH - NOTCH_H, FH + 1))
    for xc in PAD_X:
        f = f.cut(teardrop_y(xc, PAD_Z, SCREW_D / 2, -SCREW_DEPTH, 1))
    f = f.cut(logo_plate())
    return f

def for_print(part, dy):
    """Facia and logo: stand on the bottom edge (already z-up); translate to the bed with the FRONT at y 0 ... the facia's
    front is y −3, so shift +3. Insert: face down (y -> z)."""
    bb = part.val().BoundingBox()
    return part.translate((-bb.xmin, dy, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "drawer")); os.makedirs(OUT, exist_ok=True)
    fa, lg, ins = facia(), logo_plate(), insert()
    # the facia and the logo share one coordinate frame so Bambu Studio can load them as one object (same origin shift)
    for name, part in (("drawer-facia-v1", fa), ("drawer-facia-logo-v1", lg)):
        p = part.translate((0, FT, 0)); path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1); bb = p.val().BoundingBox()
        print(f"{name:22s} {bb.xlen:6.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3")
    check(os.path.join(OUT, "drawer-facia-v1.stl"), min_rest_frac=0.5, max_down_frac=0.5)
    pi = ins.rotate((0, 0, 0), (1, 0, 0), 90); bb = pi.val().BoundingBox(); pi = pi.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, "drawer-pull-insert-v1.stl"); cq.exporters.export(pi, path, tolerance=0.01, angularTolerance=0.1)
    bb = pi.val().BoundingBox(); print(f"{'drawer-pull-insert-v1':22s} {bb.xlen:6.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}  {pi.val().Volume()/1000:5.1f} cm3")
    check(path, max_down_frac=0.6)
    # proofs: insert in the notch, logo in its recess, nothing intersecting; insert can't drop through; screw holes blind
    def vol(a, b):
        try: return a.intersect(b).val().Volume() / 1000
        except Exception: return 0.0
    print("insert in notch:", round(vol(fa, ins), 4), " logo in recess:", round(vol(fa, lg), 4), " logo vs insert:", round(vol(lg, ins), 4), "cm3 (all 0)")
    print("insert shifted down 0.5:", round(vol(fa, ins.translate((0, 0, -0.5))), 3), " left 0.5:", round(vol(fa, ins.translate((-0.5, 0, 0))), 3), "cm3 (both > 0: notch holds it)")
    print("insert top vs facia top:", round(ins.val().BoundingBox().zmax - FH, 3), " front:", round(ins.val().BoundingBox().ymin + FT, 3), "(both 0: flush)")
    skin = box(0, FW, -FT, -FT + 0.6, 0, FH)                      # the 0.6 in front of the screw holes' ends
    holes = None
    for xc in PAD_X:
        h = teardrop_y(xc, PAD_Z, SCREW_D / 2, -SCREW_DEPTH, 1); holes = h if holes is None else holes.union(h)
    print("screw holes reach the front skin?", round(vol(holes, skin), 4), "cm3 (0 = blind, 0.7 skin stays)")
    print("logo clear of the notch and the holes:", round(vol(lg, holes), 4), round(vol(lg, box((FW - NOTCH_W) / 2, (FW + NOTCH_W) / 2, -FT - 1, 1, FH - NOTCH_H, FH + 1)), 4), "cm3 (both 0)")
