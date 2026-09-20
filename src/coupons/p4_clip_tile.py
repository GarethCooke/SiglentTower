# P4 coupon — slot-clip tile (ROADMAP §3). Yellow PETG, face down. Two 60 x 60 x 3 SOLID tiles (no hex: the clip is
# what's on trial), each with two spring fingers on its bottom edge (src/parts/slot_clip.py), barb 0.6 on one tile and
# 0.9 on the other, stamped b06 / b09 on the back. The tile's bottom edge sits on the slot centreline of bar Z's
# outer... any face: press the fingers' pegs into the slot with the tile flat on the rail face and the tile body
# extending AWAY from the barb side (the barb hooks the lip on the tile's side).
# Pass: snaps in by thumb, no rock, pulls off only with a blade against a finger's free end, 10 cycles no cracks.
# Winner sets CLIP_BARB; CLIP_T stays 3. Output: coupons/p4/tile-b06.stl, tile-b09.stl, p4-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.slot_clip import add_finger, box, T, FINGER_L, PEG_W, PEG_L
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p4")); os.makedirs(OUT, exist_ok=True)

W, H = 60.0, 60.0                 # along the rail x across (z from the slot centreline up)
def tile(barb):
    t = box(-T, 0, 0, W, 0, H)                                          # tile body, edge on the slot centreline (z 0)
    t = add_finger(t, 4.0, +1, barb)                                    # finger A: root y 4, runs +y, peg at y 23–29
    t = add_finger(t, W - 4.0, -1, barb)                                # finger B: root y 56, runs -y, peg at y 31–37
    # deboss the label on the back (print top) in the tile's upper half
    t = t.cut(cq.Workplane("YZ", origin=(-0.6, 0, 0)).center(W / 2, H - 12).text(f"b{barb*10:02.0f}", 6.0, 1.6, combine=False, halign="center", valign="center"))   # 0.6 deep into the back
    return t

plate = None; x = 0.0
for barb in (0.6, 0.9):
    tl = tile(barb)
    p = tl.rotate((0, 0, 0), (0, 1, 0), -90)          # face down: tile x (thickness) -> print z; face (-T) -> bed
    bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"tile-b{barb*10:02.0f}.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    bb = p.val().BoundingBox(); print(f"tile b{barb*10:02.0f}: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.2f}  {tl.val().Volume()/1000:.1f} cm3")
    check(path, max_down_frac=0.3)
    placed = p.translate((x, 0, 0)); plate = placed if plate is None else plate.add(placed); x += bb.xlen + 10
cq.exporters.export(plate, os.path.join(OUT, "p4-plate.stl"), tolerance=0.01, angularTolerance=0.1)
print(f"finger {FINGER_L} x {T}, peg {PEG_W} x {PEG_L}, barbs 0.6 / 0.9")
