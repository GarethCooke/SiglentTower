# P7 coupon — quarter joint (ROADMAP §3, drawer-quarters-v1.pdf). One PETG plate, three tests:
#   1. centre cross: the four quarters cropped to 60 mm each side of the cross (floor tabs + sockets, real pattern)
#   2. wall crossing: Q1 + Q2 cropped to 40 mm each side of the front-wall crossing (rib, boss, slot) and the first floor tab
#   3. beam section (D6): two 40 x 40 x 9 ends of the sled beam with one puzzle tab / socket
# Pass: everything assembles by hand, holds without glue, faces flush within 0.2. Sets fit.DOVETAIL_CLR.
# Output (repo root): coupons/p7/<piece>.stl and coupons/p7/p7-plate.stl (all pieces laid out flat, 10 mm apart). Run from anywhere.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import cadquery as cq
from fit import DOVETAIL_CLR as C
from parts.drawer_quarters import quarter, crop, prism, box, trapezoid, SEAM_X, SEAM_Y, TAB_NECK, TAB_HEAD, TAB_LEN, DH

OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p7")); os.makedirs(OUT, exist_ok=True)
pieces = {}

# 1. centre cross — 65 each side of (SEAM_X, SEAM_Y)
R = 65   # takes the tabs at 115 and 205 whole and leaves the ones at 235 out, so the crop never slices a tab
for i in range(1, 5):
    pieces[f"cross-Q{i}"] = crop(quarter(i), SEAM_X - R, SEAM_X + R, SEAM_Y - R, SEAM_Y + R)

# 2. wall crossing — front wall, 40 each side of SEAM_X, 40 deep (takes the wall, the boss and the first floor tab at y 25)
pieces["wall-Q1"] = crop(quarter(1), SEAM_X - 40, SEAM_X + 10, 0, 40)
pieces["wall-Q2"] = crop(quarter(2), SEAM_X, SEAM_X + 40, 0, 40)

# 3. beam section — 40 wide x 9 thick, one central tab across the split (production beam split at y 165)
BW, BT, L = 40.0, 9.0, 40.0
front = box(0, BW, 0, L, 0, BT).union(prism(trapezoid(L, BW / 2, (+1, "y"), TAB_NECK, TAB_HEAD, TAB_LEN), 0, BT))
rear = box(0, BW, L, 2 * L, 0, BT).cut(prism(trapezoid(L, BW / 2, (+1, "y"), TAB_NECK, TAB_HEAD, TAB_LEN, grow=C), -1, BT + 1))
pieces["beam-front"] = front
pieces["beam-rear"] = rear

# export each piece at the origin, and a plate with everything laid out
plate = None; cursor_x = 0.0; row_y = 0.0; row_h = 0.0
for name, p in pieces.items():
    bb = p.val().BoundingBox()
    p0 = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    cq.exporters.export(p0, os.path.join(OUT, f"{name}.stl"), tolerance=0.02, angularTolerance=0.2)
    if cursor_x + bb.xlen > 240: cursor_x, row_y, row_h = 0.0, row_y + row_h + 10, 0.0
    placed = p0.translate((cursor_x, row_y, 0))
    plate = placed if plate is None else plate.add(placed)
    cursor_x += bb.xlen + 10; row_h = max(row_h, bb.ylen)
    print(f"{name:12s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:6.1f} cm3")
cq.exporters.export(plate, os.path.join(OUT, "p7-plate.stl"), tolerance=0.02, angularTolerance=0.2)
pb = plate.combine().val().BoundingBox() if hasattr(plate, "combine") else None
print("plate footprint", f"{cursor_x:.0f} x {row_y + row_h:.0f}", "clearance", C)
