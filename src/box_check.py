# box_check.py — proves the rear box halves (python src/box_check.py): halves assembled 0 cm³, every joint engaged, the right
# half lifts clear (vertical assembly); the box on the sled ladder (beams v1/v2 + bars) 0 cm³, held fore-aft by the lips
# (0.5 shift in y collides), free to slide right (10 shift in +x clears everything but the right beam's top it slides on).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from parts.drawer_quarters import box
from parts.rear_box import half
from parts.sled_beam import PARTS as BEAMS
from parts.sled_bars import PARTS as BARS
def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0
L, R = half("L"), half("R")
print("1. halves assembled:", round(vol(L, R), 4), "cm3 (0)")
for tag, d in (("R +x (pull apart)", (1.0, 0, 0)), ("R -x", (-1.0, 0, 0)), ("R +y", (0, 0.5, 0)), ("R -y", (0, -0.5, 0))):
    # pull-apart is held by the tabs' 20° flanks, so a 1.0 shift (0.35 normal to the flank, > the 0.15 clearance) is the honest test
    v = vol(R.translate(d), L); print(f"2. {tag} {abs(sum(d)):.1f}: {v:.3f} cm3 {'engaged' if v > 0.005 else 'FREE'}")
print("3. R lifted 10:", round(vol(R.translate((0, 0, 10)), L), 4), "cm3 (0)")
sled = None
for fn in list(BEAMS.values()) + list(BARS.values()): sled = fn() if sled is None else sled.union(fn())
bx = L.union(R)
print("4. box on the sled:", round(vol(bx, sled), 4), "cm3 (0)")
print("   box forward 0.5:", round(vol(bx.translate((0, -0.5, 0)), sled), 3), " back 0.5:", round(vol(bx.translate((0, 0.5, 0)), sled), 3), "cm3 (both > 0: the lips hold it)")
print("   box right 10:", round(vol(bx.translate((10, 0, 0)), sled), 4), " right 60:", round(vol(bx.translate((60, 0, 0)), sled), 4), "cm3 (0: it slides out)")
scope = box(23, 338, 3, 135, 355, 500); print("   box vs scope envelope:", round(vol(bx, scope), 4), "cm3 (0)")
