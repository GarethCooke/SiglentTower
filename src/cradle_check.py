# cradle_check.py — proves the 2026-10-02 cradle changes against the PSU AS MEASURED AND SEATED (python src/cradle_check.py):
#   PSU front face x 20–244.5 (gaps 0 / 6.5 measured), body 220 centred under it (x 22.25–242.25), feet 155.5 apart, height 150.
#   1. right PSU cup v4 centre lands on the right foot (left cup v3 on the left foot)
#   2. AWG arms v2 underside clear of the PSU top; right bracket plate v2 clear of the PSU side
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cadquery as cq
from fit import PSU_FACE_X, PSU_FEET_CC, PSU_H_FEET, PSU_BODY_W
from parts.psu_cradle import cradle, REACH_V3, REACH_V4R, REACH_V5RF, RAIL, LIP_T, TOP_T
from parts.awg_cradle import left_cradle, right_bracket, Z_RAIL_TOP, ARM_T, PLATE_T
from parts.drawer_quarters import box
# 2026-10-03, bench: left cups v3 fit; right REAR v4 fits; right FRONT wants a cup a few mm further out than v4 -> v5 at the
# midpoint between v4 and v3. The PSU sits very slightly skewed in the frame; the cups follow the feet, not the drawing.
cups = {"left (v3)": 20 + LIP_T + REACH_V3, "right rear (v4)": 251 - (LIP_T + REACH_V4R), "right front (v5)": 251 - (LIP_T + REACH_V5RF)}
print("1. cup centres x:", {k: round(v, 2) for k, v in cups.items()})
body_x0 = (PSU_FACE_X[0] + PSU_FACE_X[1]) / 2 - PSU_BODY_W / 2
# PSU in the frame: feet pads sit on the cup floors. Cup floor = PSU rail top 68 + TOP_T - 4 = 72; measured touching at the
# arms (239.5) with height 150 -> pad at 89.5?? The cups' floors are at 72, so the PSU top would be 222 — the measured
# contact says the PSU top is at 239.5: the feet do NOT reach the cup floors (the right pair sat on the rims). Use the
# measurement: top at 239.5 as seated today; with the right feet in their cups the PSU drops ~4 (cup depth) on the right,
# so the top ends up 235.5–239.5 — take the worst case 239.5.
psu_top = 239.5
arm_under = Z_RAIL_TOP - ARM_T
print(f"2. AWG arm underside {arm_under} vs PSU top {psu_top}: {arm_under - psu_top:.1f} mm clear;  right plate x {251 - PLATE_T} vs PSU face {PSU_FACE_X[1]}: {251 - PLATE_T - PSU_FACE_X[1]:.1f} mm clear")
psu = box(body_x0, body_x0 + PSU_BODY_W, 3, 287.5, psu_top - 150 + 11.5, psu_top).union(box(PSU_FACE_X[0], PSU_FACE_X[1], 3, 8, psu_top - 150 + 11.5, psu_top))
def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0
for name, part in (("AWG left front", left_cradle().translate((0, 20, 0))), ("AWG right front", right_bracket().translate((0, 23, 0))),
                   ("AWG right rear", right_bracket().translate((0, 223, 0)))):
    print(f"   {name} vs PSU envelope: {vol(part, psu):.4f} cm3 (0)")
