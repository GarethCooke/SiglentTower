# P4 coupon — slot-clip tile (ROADMAP §3). Yellow PETG, face down. v2: four 66 x 14 x 3 strips (the joint is what's on
# trial, nothing else), each with two spring fingers on its long edge (src/parts/slot_clip.py), hook on the lip, and a
# rigid root stub filling the mouth. Variants A–D stamped on the back, see VARIANTS.
# v1 (60 x 60, barb 0.6 / 0.9, no stubs): both very loose — nothing located the tile along the slot width. The tile's bottom edge sits on the slot centreline of bar Z's
# outer... any face: press the fingers' pegs into the slot with the tile flat on the rail face and the tile body
# extending AWAY from the barb side (the barb hooks the lip on the tile's side).
# Pass: snaps in by thumb, no rock, pulls off only with a blade against a finger's free end, 10 cycles no cracks.
# Winner sets CLIP_BARB; CLIP_T stays 3. Output: coupons/p4/tile-b06.stl, tile-b09.stl, p4-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.slot_clip import add_finger, box, T, FINGER_L, PEG_W, PEG_L, STUB_L
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p4")); os.makedirs(OUT, exist_ok=True)

W, H = 66.0, 14.0                 # v2 coupon strip: 66 along the rail, 14 up from the slot centreline — the joint is what's on test
def tile(barb, stub_clr, hook_deg, finger_w, tag):
    t = box(-T, 0, 0, W, 0, H)                                          # tile body, edge on the slot centreline (z 0)
    t = add_finger(t, 2.0, +1, barb, stub_clr, hook_deg, finger_w)      # finger A: root y 2 (stub 2–8), runs +y, peg at y 26–32
    t = add_finger(t, W - 2.0, -1, barb, stub_clr, hook_deg, finger_w)  # finger B: root y 64 (stub 58–64), runs -y, peg at y 34–40
    t = t.cut(cq.Workplane("YZ", origin=(-0.6, 0, 0)).center(W / 2, H - 5).text(tag, 4.0, 1.6, combine=False, halign="center", valign="center"))   # 0.6 deep into the back
    return t

# (barb, stub clearance per side, hook angle, finger width, tag)
VARIANTS = ((0.9, 0.1, 60.0, 5.5, "A"),    # A: stub 5.7, barb 0.9, 60° hook — the baseline fix
            (0.9, 0.2, 60.0, 5.5, "B"),    # B: as A with stub 5.5, if 5.7 won't enter the mouth
            (1.2, 0.1, 45.0, 5.5, "C"),    # C: barb 1.2 (the '+2 mm' reach) — needs a 45° hook to fit under the throat
            (0.9, 0.1, 60.0, 7.0, "D"))    # D: as A with a 7 mm finger, ~2x the snap force
plate = None; x = 0.0
for barb, stub_clr, hook_deg, finger_w, tag in VARIANTS:
    tl = tile(barb, stub_clr, hook_deg, finger_w, tag)
    p = tl.rotate((0, 0, 0), (0, 1, 0), -90)          # face down: tile x (thickness) -> print z; face (-T) -> bed
    bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"tile-v2-{tag}.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    bb = p.val().BoundingBox(); print(f"tile v2 {tag}: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.2f}  {tl.val().Volume()/1000:.1f} cm3")
    check(path, max_down_frac=0.3)
    placed = p.translate((x, 0, 0)); plate = placed if plate is None else plate.add(placed); x += bb.xlen + 10
cq.exporters.export(plate, os.path.join(OUT, "p4-v2-plate.stl"), tolerance=0.01, angularTolerance=0.1)
print(f"finger {FINGER_L} x {T} (root stub {STUB_L}), peg {PEG_W} x {PEG_L}; A stub 5.7 barb 0.9 60°, B stub 5.5, C barb 1.2 45°, D finger 7")
