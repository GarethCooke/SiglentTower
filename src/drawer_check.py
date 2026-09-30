# drawer_check.py — proves the bottom-drawer quarters before they print (ROADMAP Stage 4, PRINT-RULES rule 6 "proven by
# boolean intersection + shift test"). Run from anywhere: python src/drawer_check.py
#   1. the four quarters assembled in place do not intersect (tabs, wall dovetails, grooves, pads)
#   2. every joint is engaged: shifting any one quarter 0.5 in x or y collides with its neighbours
#   3. vertical assembly: Q2 and Q3 lifted 10 above Q1, and Q4 lifted 10 above Q2+Q3, still do not collide (open slots)
#   4. the runner's rib sits in the groove (P3 geometry): zero intersection at nominal (floor top touching the rib's
#      underside); the drawer shifted 0.2 up or 0.5 sideways collides with the rib, 0.2 sideways and 0.5 down are free —
#      in use the drawer drops 0.6 (RUNNER_CLR on both axes of the 45° line) until its two roofs hang on the two rib slopes
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cadquery as cq
from parts.drawer_quarters import production, DW, DD
from parts.drawer_runner import production as runner_production, RAIL, GAP, BOLTS

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

Q = production()
pairs = [(1, 2), (1, 3), (2, 4), (3, 4), (1, 4), (2, 3)]
print("1. assembled:", {f"Q{a}-Q{b}": round(vol(Q[a], Q[b]), 4) for a, b in pairs}, "cm3 (all must be 0)")
for i in range(1, 5):
    for dx, dy in ((0.5, 0), (-0.5, 0), (0, 0.5), (0, -0.5)):
        s = Q[i].translate((dx, dy, 0))
        hit = sum(vol(s, Q[j]) for j in range(1, 5) if j != i)
        print(f"2. Q{i} shifted ({dx:+.1f},{dy:+.1f}): {hit:.3f} cm3 {'engaged' if hit > 0.01 else 'FREE — joint not engaged'}")
up = 10.0
print("3. Q2 lifted:", round(vol(Q[2].translate((0, 0, up)), Q[1]), 4), " Q3 lifted:", round(vol(Q[3].translate((0, 0, up)), Q[1]), 4),
      " Q4 lifted:", round(vol(Q[4].translate((0, 0, up)), Q[2].union(Q[3])), 4), "cm3 (all must be 0)")
# runner, frame coords (left rail x 0-20, drawer wall x 23, drawer bottom z 3, runner y 23-323 on the 310 rail, drawer y 3-303)
# -> drawer coords: x - 23, y + 20, z - 3
left = runner_production().translate((-(RAIL + GAP), 20, -3))
right = left.mirror("YZ").translate((DW, 0, 0))
drawer = Q[1].union(Q[2]).union(Q[3]).union(Q[4])
rails = left.union(right)
print(f"4. production runners (bolts at y {BOLTS}) in place:", round(vol(drawer, rails), 4), "cm3 (must be 0)")
for tag, d in (("down 0.5", (0, 0, -0.5)), ("up 0.5", (0, 0, 0.5)), ("left 0.5", (-0.5, 0, 0)), ("right 0.5", (0.5, 0, 0)),
               ("up 0.2", (0, 0, 0.2)), ("left 0.2", (-0.2, 0, 0))):
    v = vol(drawer.translate(d), rails)
    if v > 0.0005:
        bb = drawer.translate(d).intersect(rails).val().BoundingBox()
        print(f"   drawer {tag}: {v:.3f} cm3  at x {bb.xmin:.1f}-{bb.xmax:.1f} y {bb.ymin:.1f}-{bb.ymax:.1f} z {bb.zmin:.1f}-{bb.zmax:.1f}")
    else: print(f"   drawer {tag}: {v:.3f} cm3 (free)")
