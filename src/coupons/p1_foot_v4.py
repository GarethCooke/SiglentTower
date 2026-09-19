# P1 v4 — slot-fit round for the sled T-foot (ROADMAP §3). v3 (SLOT_CLR 0.2, FLANGE_GAP 0.2) enters bar Z's inner slot
# from the end but is "a little tight" over 40 mm; the production foot is 210 mm in a slot that varies along its length,
# and it is THE moving part of the scope sled (100 mm travel under ~3 kg), so it must slide freely. The rib/beam pair
# passed and is unchanged. Three feet, same section as src/parts/sled_foot.py with the slot clearances opened up;
# the LENGTH says which is which:  40 mm = 0.3,  45 mm = 0.4,  50 mm = 0.5  (SLOT_CLR per side = FLANGE_GAP).
# Pass: the longest foot that still has no rock in the slot and cannot lift out; it slides its own length by hand with a
# fingertip push. Set SLOT_CLR / FLANGE_GAP in fit.py to it, then one 210 in black ASA before the pair.
# Yellow PETG (same material as v3 so the comparison is clean), standing, as p1-plate. Output: coupons/p1/p1-feet-v4.stl.
import os, sys, importlib, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import fit
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p1")); os.makedirs(OUT, exist_ok=True)

ROUND = {40.0: 0.3, 45.0: 0.4, 50.0: 0.5}      # length -> SLOT_CLR
plate = None; y = 0.0
for L, clr in ROUND.items():
    fit.SLOT_CLR = clr; fit.FLANGE_GAP = clr
    fit.SLOT_FOOT_W = fit.SLOT_MOUTH - 2 * clr
    fit.FOOT_FLANGE_W = fit.SLOT_CAVITY_W - 2 * clr
    import parts.sled_foot as sf; importlib.reload(sf)          # re-derives the section from the patched fit values
    f = sf.foot(L); bb = f.val().BoundingBox(); f0 = f.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"foot-{L:.0f}-clr{clr:.1f}.stl"); cq.exporters.export(f0, path, tolerance=0.01, angularTolerance=0.1)
    print(f"foot {L:.0f} mm: SLOT_CLR {clr}  neck {fit.SLOT_FOOT_W:.1f} in the {fit.SLOT_MOUTH} mouth, flange {fit.FOOT_FLANGE_W:.1f} in the {fit.SLOT_CAVITY_W} cavity, "
          f"flange top {clr} off the lips, bottom 0.3 off the floor -> flange {sf.Y_TOP:.2f} thick")
    check(path, min_rest_frac=0.15, max_down_frac=2.0)  # stands on two narrow edges (brim ok, no fit face on the bed); the only bridge is the 4.15 neck underside, printed fine at v3
    placed = f0.translate((0, y, 0)); plate = placed if plate is None else plate.add(placed); y += bb.ylen + 8
cq.exporters.export(plate, os.path.join(OUT, "p1-feet-v4.stl"), tolerance=0.01, angularTolerance=0.1)
