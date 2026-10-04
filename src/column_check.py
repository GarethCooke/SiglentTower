# column_check.py — proves the column drawer on its four strips (python src/column_check.py):
#   1. drawer + 4 strips in place: 0 cm³; drawer up 0.2 / down 0.5 / sideways 0.5 behaviour as the bottom drawer (hangs on
#      the lower ribs' slopes); the upper ribs only catch the roof when the drawer tips (drawer rotated nose-down 1° about
#      the lower front rib collides with the upper ribs)
#   2. strips vs the frame: rails, uprights, the front/rear ties and the front-tie cast bracket; strip bolt heads clear of
#      the drawer; lower bolt bar clear of the bottom-drawer housing top (z 64–67) and facia
#   3. drawer envelope vs the PSU-level/AWG-level inner rails and the right rails, and vs the housing top over it (333)
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cadquery as cq
from parts.drawer_quarters import box
from parts.column_drawer import drawer_in_frame, strip_in_frame, X0, Y0, Z0, DW, DD, DH, STRIP_Y0, STRIP_L
def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0
D = drawer_in_frame()
strips = {f"{k} {s}": strip_in_frame(k, s) for k in ("lower", "upper") for s in ("L", "R")}
S = None
for v in strips.values(): S = v if S is None else S.union(v)
print("1. in place:", {k: round(vol(D, v), 4) for k, v in strips.items()}, "cm3 (all 0)")
for tag, d in (("up 0.2", (0, 0, 0.2)), ("down 0.5", (0, 0, -0.5)), ("left 0.5", (-0.5, 0, 0)), ("right 0.5", (0.5, 0, 0)), ("down 0.8", (0, 0, -0.8))):
    print(f"   drawer {tag}: {vol(D.translate(d), S):.3f} cm3")
# tipping: rotate the drawer nose-down about the lower ribs' front end (y 45, z 94) by 1°
tip = D.rotate((0, STRIP_Y0, 94), (1, STRIP_Y0, 94), 1.0)
print("   drawer tipped 1° nose-down:", {k: round(vol(tip, v), 3) for k, v in strips.items()}, "(upper strips must catch it)")
# frame pieces round the bay (frame coords)
frame = [box(251, 271, 23, 330, 68, 88), box(251, 271, 23, 330, 227.5, 247.5),            # inner rails
         box(341, 361, 20, 330, 68, 88), box(341, 361, 20, 330, 227.5, 247.5),            # right PSU / AWG rails
         box(251, 271, 23, 43, 68, 247.5), box(251, 271, 310, 330, 68, 247.5),            # inner uprights
         box(341, 361, 0, 20, 0, 510), box(341, 361, 330, 350, 0, 510),                   # right uprights
         box(271, 341, 23, 43, 68, 88), box(271, 341, 310, 330, 68, 88), box(271, 341, 310, 330, 227.5, 247.5),   # ties
         box(321, 341, 23, 43, 68, 88)]                                                   # front-tie cast bracket region
F = None
for f in frame: F = f if F is None else F.union(f)
print("2. strips vs frame:", {k: round(vol(v, F), 4) for k, v in strips.items()}, "cm3 (all 0)")
heads = box(271, 279, STRIP_Y0, STRIP_Y0 + STRIP_L, 70, 86).union(box(333, 341, STRIP_Y0, STRIP_Y0 + STRIP_L, 70, 86))
print("   lower bolt bars vs drawer:", round(vol(heads, D), 4), " vs housing top 64–67 + facia:", round(vol(heads, box(23, 338, 0, 303, 3, 67)), 4), "cm3 (0)")
print("3. drawer vs frame:", round(vol(D, F), 4), " vs housing top over the column (333–336):", round(vol(D, box(242, 338, 0, 300, 333, 336)), 4), "cm3 (0)")
