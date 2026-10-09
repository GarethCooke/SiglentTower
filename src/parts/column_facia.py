# Column drawer facia + pull insert (HANDOVER §6/§8, D3 + D9, P6 ☑). Drawer coordinates as column_drawer.py (x from the
# drawer's left wall face, y rearward from the body front, z from the drawer bottom): the facia sits at y −3..0, spans
# x −1..64 (frame 273–338: 1 mm wider than the body on the left, as the layout has it) and z 0..245 (frame 91–336, up to
# the housing top over the column). Dark grey PETG, 3 thick.
#   notch     50.3 × 23.15 in the top edge for a 50-wide insert (slot 40 × 12 — the HANDOVER's "column 40")
#   pegs      two Ø3.2 × 7 on the back at (16, 20) and (48, 20): they press into the drawer body's front-wall holes
#             (column_drawer PAD_XS / PAD_Z) and locate the facia exactly — no screws, CA
#   insert    the P6 geometry at 50 wide, dark blue PETG, face down, glued in flush front and top
# Print: facia on its LONG EDGE (x = −1 face down: 245 × 3 footprint, 65 tall — the same thin-part rule as the bottom
# facia: brim 15, gap 0, door closed, bed 80), pegs horizontal; the notch opens at the top end.
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import JPULL_OPEN_H, JPULL_HOOK, JPULL_DEPTH, JPULL_FLOOR_DEG, JPULL_WALL, JPULL_INSERT_CLR
from parts.drawer_quarters import box
from parts.column_drawer import PAD_XS, DW, X0, Y0, Z0
from parts.drawer_quarters import PAD_Z

FX0, FX1, FT, FH = -1.0, 64.0, 3.0, 245.0
PULL_W, SLOT_W, SLOT_Z = 50.0, 40.0, 4.0
PEG_D, PEG_L = 3.2, 7.0
w, d = JPULL_WALL, JPULL_DEPTH; t = math.tan(math.radians(JPULL_FLOOR_DEG))
H = SLOT_Z + JPULL_OPEN_H + JPULL_HOOK
NOTCH_W, NOTCH_H = PULL_W + 2 * JPULL_INSERT_CLR, H + w + JPULL_INSERT_CLR
XM = (FX0 + FX1) / 2

def prism(pts, x0, x1):
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1 - x0).translate((x0, 0, 0))

def insert():
    z_floor = SLOT_Z - w
    cav = [(FT, z_floor), (FT + d, z_floor + d * t), (FT + d, H), (FT, H)]
    outer = [(FT, z_floor - w), (FT + d + w, z_floor - w + (d + w) * t), (FT + d + w, H + w), (FT, H + w)]
    face = cq.Workplane("XY").box(PULL_W, FT, H + w, centered=False)
    slot = cq.Workplane("XY").box(SLOT_W, FT + 2, JPULL_OPEN_H, centered=False).translate(((PULL_W - SLOT_W) / 2, -1, SLOT_Z))
    pocket = prism(outer, (PULL_W - SLOT_W) / 2 - w, (PULL_W + SLOT_W) / 2 + w)
    cavity = prism(cav, (PULL_W - SLOT_W) / 2, (PULL_W + SLOT_W) / 2)
    s = face.union(pocket, clean=True).cut(slot).cut(cavity).clean()
    return s.translate((XM - PULL_W / 2, -FT, FH - H - w))

def facia():
    f = box(FX0, FX1, -FT, 0, 0, FH)
    f = f.cut(box(XM - NOTCH_W / 2, XM + NOTCH_W / 2, -FT - 1, 1, FH - NOTCH_H, FH + 1))
    for xc in PAD_XS:
        f = f.union(cq.Workplane("XZ", origin=(xc, 0, PAD_Z)).circle(PEG_D / 2).extrude(-PEG_L))   # +y: into the drawer
    return f

def facia_in_frame(): return facia().translate((X0, Y0, Z0))

if __name__ == "__main__":
    from printcheck import check
    from parts.column_drawer import drawer_in_frame
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "column")); os.makedirs(OUT, exist_ok=True)
    fa, ins = facia(), insert()
    p = fa.rotate((0, 0, 0), (0, 1, 0), -90); bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))   # on its long edge: facia z -> print x, x -> print z
    path = os.path.join(OUT, "column-facia-v1.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    bb = p.val().BoundingBox(); print(f"column-facia-v1        {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3")
    check(path, max_down_frac=0.5)
    pi = ins.rotate((0, 0, 0), (1, 0, 0), 90); bb = pi.val().BoundingBox(); pi = pi.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, "column-pull-insert-v1.stl"); cq.exporters.export(pi, path, tolerance=0.01, angularTolerance=0.1)
    bb = pi.val().BoundingBox(); print(f"column-pull-insert-v1  {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {pi.val().Volume()/1000:.1f} cm3")
    check(path, max_down_frac=0.6)
    def vol(a, b):
        try: return a.intersect(b).val().Volume() / 1000
        except Exception: return 0.0
    D = drawer_in_frame(); F = facia_in_frame()
    print("insert in notch:", round(vol(fa, ins), 4), " facia (pegs in the body's holes) vs drawer:", round(vol(F, D), 4), "cm3 (both 0)")
    print("insert held: down 0.5", round(vol(fa, ins.translate((0, 0, -0.5))), 3), " left 0.5", round(vol(fa, ins.translate((-0.5, 0, 0))), 3), "(> 0);  flush top/front:",
          round(ins.val().BoundingBox().zmax - FH, 3), round(ins.val().BoundingBox().ymin + FT, 3))
    print("facia shifted 0.5 in x / z vs drawer (pegs locate):", round(vol(F.translate((0.5, 0, 0)), D), 3), round(vol(F.translate((0, 0, 0.5)), D), 3), "(> 0)")
    print("facia vs frame uprights/rails round the column (x 341–361, x 251–271):", round(vol(F, box(341, 361, 0, 350, 0, 510).union(box(251, 271, 0, 350, 0, 510))), 4), "(0)")
