# box_brace.py — corner braces for the rear box (ROADMAP Stage 6, 2026-10-14). Gareth cracked the right side wall of
# the printed box: a horizontal (layer) crack starting where the side wall meets the 20 mm front lip. The box prints
# floor down, so its walls are stacks of layers; the side wall's front edge is free above the lip, and the lip's top
# corner is a stress riser on a layer line — the wall split along it.
#
# The brace is an equal-leg L-angle, BRACE_T thick, LEG x LEG, BRACE_H tall, CA'd INTO each front corner: one leg flat
# on the side wall's inner face running rearward, the other flat on the lip's rear face and, above the lip, standing
# free as a flange that caps the wall's front edge — so the wall's free edge becomes a stiff corner post and the crack
# line is bridged by 100 mm of glued angle. One part serves both corners (an equal-leg L is its own mirror, turned 90°).
#
# Print: LYING on the wall leg, the other leg standing (100 x 15 footprint, 15 tall, grey PETG, no brim, no support).
# In use that puts the layer lines VERTICAL in both legs — the direction the crack opens — instead of copying the box's
# horizontal layers. Bottom edges chamfered 0.4 (rule 7).
#
# Fit (CA): glue the crack first (CA into it, hold closed), then the brace: CA on the wall leg, the lip leg and the
# bottom edge, press into the corner, hold 30 s. Both corners, cracked or not.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.drawer_quarters import box
import parts.rear_box as rb

LEG, BRACE_T, BRACE_H = 15.0, 4.0, 100.0
Z_BOT = rb.Z0 + rb.FLOOR                   # 349: sits on the floor
X_IN_L, X_IN_R = rb.X0 + rb.WALL, rb.X1 - rb.WALL     # side walls' inner faces 52.4 / 338.6
Y_IN = rb.Y0 + rb.WALL                     # lip's rear face 197.4

def brace_in_place(corner):
    """World coordinates, as glued into the left ('L') or right ('R') front corner of the box."""
    if corner == "L": xw0, xw1, xf0, xf1 = X_IN_L, X_IN_L + BRACE_T, X_IN_L, X_IN_L + LEG
    else:             xw0, xw1, xf0, xf1 = X_IN_R - BRACE_T, X_IN_R, X_IN_R - LEG, X_IN_R
    wall_leg = box(xw0, xw1, Y_IN, Y_IN + LEG, Z_BOT, Z_BOT + BRACE_H)
    lip_leg = box(xf0, xf1, Y_IN, Y_IN + BRACE_T, Z_BOT, Z_BOT + BRACE_H)
    return wall_leg.union(lip_leg)

def brace_print():
    """Lying on the wall leg: world z (height) -> print x, the wall leg's outer face on the bed."""
    b = brace_in_place("L").translate((-X_IN_L, -Y_IN, -Z_BOT))        # corner at the origin: wall leg x 0–4, lip leg y 0–4
    b = b.rotate((0, 0, 0), (0, 1, 0), -90)                             # z -> -x, x -> z: the wall leg lies at z 0..4, the lip leg stands
    bb = b.val().BoundingBox(); b = b.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    return b.faces("<Z").edges().chamfer(0.4)

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    halves = {"L": rb.half("L"), "R": rb.half("R")}
    for corner in ("L", "R"):
        b = brace_in_place(corner); h = halves[corner]
        dx = 0.5 if corner == "L" else -0.5
        print(f"{corner} brace in the corner: vs its box half {vol(b, h):.4f} cm3 (0); pushed 0.5 into the wall {vol(b.translate((-dx, 0, 0)), h):.4f} (>0, flat on it); "
              f"0.5 into the lip {vol(b.translate((0, -0.5, 0)), h):.4f} (>0); 0.5 down {vol(b.translate((0, 0, -0.5)), h):.4f} (>0, on the floor); "
              f"top at z {Z_BOT + BRACE_H:.0f} (wall top {rb.Z0 + rb.H:.0f}), lip top {rb.Z0 + rb.LIP_H:.0f}")
    p = brace_print(); bb = p.val().BoundingBox(); path = os.path.join(OUT, "box-brace-v1.stl")
    cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    print(f"box-brace-v1  {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  — print TWO, grey PETG, as exported")
    check(path)
