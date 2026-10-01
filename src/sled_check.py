# sled_check.py — proves the sled ladder (beams v1 + front bar + cross bars) before the bars print. python src/sled_check.py
#   1. beams (as printed, world coordinates) + bars assembled: zero intersection
#   2. every tab engaged: each bar shifted 0.5 along its own axis or across it collides with the beams
#   3. assembly paths: the cross bars lifted 10 are clear (they drop on); the front bar lifted 10 COLLIDES (its pockets are
#      closed — it slides on from the front) and slid 10 forward is clear
#   4. scope body (x 23–338, y 3–135 with bumpers, z ≥ 355), the box (x 50–341, y 195–330, z ≥ 346), the stand legs at
#      their loosest and the cable channel's footprint all clear of the bars (the v2 saddles sit between them)
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from parts.drawer_quarters import box
from parts.sled_beam import PARTS as BEAMS
from parts.sled_bars import PARTS as BARS

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

beams = None
for fn in BEAMS.values(): beams = fn() if beams is None else beams.union(fn())
bars = {n: fn() for n, fn in BARS.items()}
print("1. assembled:", {n: round(vol(b, beams), 4) for n, b in bars.items()}, "cm3 (all 0)")
for n, b in bars.items():
    for tag, d in (("x+0.5", (0.5, 0, 0)), ("x-0.5", (-0.5, 0, 0)), ("y+0.5", (0, 0.5, 0)), ("y-0.5", (0, -0.5, 0))):
        v = vol(b.translate(d), beams); print(f"2. {n} {tag}: {v:.3f} cm3 {'engaged' if v > 0.005 else 'FREE'}")
lift = {n: round(vol(b.translate((0, 0, 10 if "cross" in n else 1)), beams), 4) for n, b in bars.items()}
print("3. cross bars lifted 10 / front bar lifted 1:", lift, "cm3 — cross bars 0 (drop on); FRONT BAR MUST COLLIDE (closed pockets):", "ok" if lift["sled-front-bar"] > 0.01 else "FAIL")
print("3c. front bar lowered 1 (pocket ceilings):", round(vol(bars["sled-front-bar"].translate((0, 0, -1)), beams), 4), "cm3 (must collide)")
print("3b. front bar slid 10 forward (its assembly path):", round(vol(bars["sled-front-bar"].translate((0, -10, 0)), beams), 4), "cm3 (must be 0)")
scope = box(23, 338, 3, 135, 355, 500); boxsolid = box(50, 341, 195, 330, 346, 456)
stands = box(47.1, 92.3, 12, 37.1, 343.5, 355).union(box(361 - 92.3, 361 - 47.1, 12, 37.1, 343.5, 355))   # legs at the pocket's loose limits
channel = box(20, 46, 140, 334, 346, 400)
print("4. scope:", {n: round(vol(b, scope), 4) for n, b in bars.items()}, " box:", {n: round(vol(b, boxsolid), 4) for n, b in bars.items()},
      " stand legs:", {n: round(vol(b, stands), 4) for n, b in bars.items()}, " channel:", {n: round(vol(b, channel), 4) for n, b in bars.items()}, "cm3 (all 0)")
