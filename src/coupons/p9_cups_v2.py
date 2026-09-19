# P9 v2 — rear-bumper cup plate (ROADMAP §3). Yellow PETG, flat. Six D-shaped cups in one 9 mm slab, each the bumper's
# 5 mm-up section (fit.BUMPER_W x BUMPER_D5, flat + half-round) grown by the net clearance stamped beside it: straight
# walls for 5 mm, then a 1 mm 45° lead-in — 6 deep in total. Straight, not conical: the bumper is a bullnose below its
# 5 mm section, so the cup can only locate it at the rim, and any lead-in inside that height would leave nothing touching.
# The old cup pad (Ø32.6) was sized on the handover's Ø32, which is not a dimension the bumper has.
# Test: drop the bumper into each cup. Winner = seats fully on the floor, no rattle, lifts straight out. Set
# BUMPER_CUP_CLR to it, and say which way the D's flat faces on the scope (the beam arm needs that).
# Plus stand-pad-v2: the front-stand pocket at 44 x 23.1 + STAND_CLR (v1 used the 43 overall; the folded flap tucks under
# the main leg and never reaches the pocket). Output: coupons/p9/p9-cups-v2.stl, stand-pad-v2.stl, p9-v2-plate.stl (both).
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import BUMPER_W, BUMPER_D5, BUMPER_CUP_D, BUMPER_CUP_V2, STAND_W, STAND_L, STAND_CLR, STAND_POCKET_D
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p9")); os.makedirs(OUT, exist_ok=True)

T, LEAD, PITCH, MARGIN = 9.0, 1.0, 42.0, 8.0
COLS, ROWS = 3, 2
assert BUMPER_CUP_D <= T - 3, "keep a 3 mm floor"

def d_profile(wp, w, d):
    """Tombstone: flat at the bottom (y = -d/2), half-round of radius w/2 at the top. Centred on the workplane origin."""
    r = w / 2; yc = d / 2 - r
    return wp.moveTo(-r, -d / 2).lineTo(r, -d / 2).lineTo(r, yc).threePointArc((0, yc + r), (-r, yc)).close()

def cup(clr):
    """Solid to cut: straight D for BUMPER_CUP_D - LEAD, then a 45° lead-in of LEAD, running out above the slab."""
    w, d = BUMPER_W + 2 * clr, BUMPER_D5 + 2 * clr
    z0 = T - BUMPER_CUP_D
    straight = d_profile(cq.Workplane("XY").workplane(offset=z0), w, d).extrude(BUMPER_CUP_D - LEAD)
    lead = d_profile(cq.Workplane("XY").workplane(offset=T - LEAD), w, d)
    lead = d_profile(lead.workplane(offset=LEAD), w + 2 * LEAD, d + 2 * LEAD)
    lead = d_profile(lead.workplane(offset=1.0), w + 2 * LEAD, d + 2 * LEAD).loft(ruled=True)
    return straight.union(lead)

PW = (COLS - 1) * PITCH + BUMPER_W + 2 * MARGIN
PH = (ROWS - 1) * PITCH + BUMPER_D5 + 2 * MARGIN + 6
plate = cq.Workplane("XY").box(PW, PH, T, centered=(True, True, False))
for i, c in enumerate(BUMPER_CUP_V2):
    col, row = i % COLS, i // COLS
    x = (col - (COLS - 1) / 2) * PITCH; y = ((ROWS - 1) / 2 - row) * PITCH + 3
    plate = plate.cut(cup(c).translate((x, y, 0)))
    plate = plate.cut(cq.Workplane("XY").workplane(offset=T - 0.6).center(x, y - BUMPER_D5 / 2 - 4.5)
                      .text(f"{c:+.1f}", 5.0, 1.6, combine=False, halign="center", valign="center"))
path = os.path.join(OUT, "p9-cups-v2.stl"); cq.exporters.export(plate, path, tolerance=0.01, angularTolerance=0.1)
bb = plate.val().BoundingBox()
print(f"plate {bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.0f}, {plate.val().Volume()/1000:.0f} cm3; cups {[f'{c:+.1f}' for c in BUMPER_CUP_V2]} on "
      f"{BUMPER_W} x {BUMPER_D5}: {BUMPER_W + 2*BUMPER_CUP_V2[0]:.1f} x {BUMPER_D5 + 2*BUMPER_CUP_V2[0]:.1f} .. {BUMPER_W + 2*BUMPER_CUP_V2[-1]:.1f} x {BUMPER_D5 + 2*BUMPER_CUP_V2[-1]:.1f}, "
      f"{BUMPER_CUP_D - LEAD} straight + {LEAD} lead-in")
check(path)

# stand pad v2 — pocket for the main leg only, x = across the scope, y = front-to-back
sw, sl = STAND_W + 2 * STAND_CLR, STAND_L + 2 * STAND_CLR
stand = cq.Workplane("XY").box(sw + 8, sl + 8, T, centered=(True, True, False)).faces(">Z").workplane().rect(sw, sl).cutBlind(-STAND_POCKET_D)
sp = os.path.join(OUT, "stand-pad-v2.stl"); cq.exporters.export(stand, sp, tolerance=0.01, angularTolerance=0.1); check(sp)
print(f"stand pocket {sw:.1f} x {sl:.1f} x {STAND_POCKET_D}")
both = plate.add(stand.translate((0, -(PH / 2 + 10 + (sl + 8) / 2), 0)))
cq.exporters.export(both, os.path.join(OUT, "p9-v2-plate.stl"), tolerance=0.01, angularTolerance=0.1)
