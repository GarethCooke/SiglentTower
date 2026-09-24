# P9 position jigs — where the scope's rear bumpers and front stands sit relative to its front face and sides. The handover's
# "centre 39 from side / at the rear edge" were never measured; the apex came out at 91 from the front face (2026-09-21,
# so the flat is at 115, not 135) and the side figure could not be measured directly (bumper is a D on a curved shell).
# Two jigs, yellow PETG, flat as exported, used on the scope UPSIDE DOWN:
#   bumper jig: the P9 D cup (BUMPER_* + BUMPER_CUP_CLR, 5 straight + 1 lead-in) in a 4 mm plate with a 9 mm boss; a 3 mm
#     skirt rises along BOTH long edges, inner faces SKIRT_B from the cup's straight sides, and the plate's front edge is
#     FRONT_B ahead of the nominal apex. Cup down over a bumper (flat side to the rear); one skirt hangs beside the body's
#     side. Measure: gap skirt inner face -> body side (calipers, inside jaws or depth rod) -> bumper outer side from the
#     body side = SKIRT_B - gap; front face -> plate front edge (rule) -> apex = that + FRONT_B (checks the 91).
#   stand jig: the P9 stand pocket (STAND_W/L + STAND_CLR, 2.5 deep) in a 5 mm plate, skirts on both long edges (inner
#     faces SKIRT_S from the pocket's side walls) and one along the front edge (inner face FRONT_S from the pocket's front
#     wall). Pocket down over a folded stand: side gap -> stand outer edge = SKIRT_S - gap - STAND_CLR; front gap -> stand
#     front edge from the face = FRONT_S - gap - STAND_CLR (expect ~5.7 and ~19.7 if the handover's 24 and the measured 10 hold).
# Both jigs are mirror-symmetric in x, so either flip works and either side of the scope can be measured — do both.
# Output: coupons/p9/bumper-jig.stl, stand-jig.stl, p9-jigs-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import BUMPER_W, BUMPER_D5, BUMPER_SIDE_L, BUMPER_CUP_D, BUMPER_CUP_CLR, STAND_W, STAND_L, STAND_CLR, STAND_POCKET_D
from parts.drawer_quarters import box as _box
def box(x0, x1, y0, y1, z0, z1):   # order-agnostic (the mirrored skirts pass x1 < x0)
    return _box(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), z0, z1)
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p9")); os.makedirs(OUT, exist_ok=True)

SKIRT_B, FRONT_B = 40.0, 30.0      # bumper jig: skirt inner face from the cup's straight side; plate front edge from the apex
SKIRT_S, FRONT_S = 30.0, 30.0      # stand jig: skirt inner faces from the pocket's side / front walls
SKIRT_T, SKIRT_H = 3.0, 12.0       # skirt thickness; height above the plate top (hangs 4 past the chassis in use)
PLATE_B, PLATE_S = 4.0, 5.0        # plate thicknesses; the bumper jig gets a 9 mm boss round the cup
WALL = 5.0

def d_profile(wp, w, d, side):
    r = w / 2; yc = -d / 2 + side
    return wp.moveTo(-r, -d / 2).lineTo(r, -d / 2).lineTo(r, yc).threePointArc((0, d / 2), (-r, yc)).close()

def cup_cutter(z_floor):
    clr = BUMPER_CUP_CLR
    w, d, sd = BUMPER_W + 2 * clr, BUMPER_D5 + 2 * clr, BUMPER_SIDE_L + clr
    straight = d_profile(cq.Workplane("XY").workplane(offset=z_floor), w, d, sd).extrude(BUMPER_CUP_D - 1.0)
    z_lead = z_floor + BUMPER_CUP_D - 1.0
    lead = d_profile(cq.Workplane("XY").workplane(offset=z_lead), w, d, sd)
    lead = d_profile(lead.workplane(offset=1.0), w + 2, d + 2, sd + 1)
    lead = d_profile(lead.workplane(offset=2.0), w + 2, d + 2, sd + 1).loft(ruled=True)
    return straight.union(lead).rotate((0, 0, 0), (0, 0, 1), 180)     # flat at +y (rear), apex at -y (front)

def bumper_jig():
    hw = BUMPER_W / 2 + BUMPER_CUP_CLR                 # 13.25: cup straight sides
    hd = BUMPER_D5 / 2                                 # 12: nominal apex / flat
    x1 = hw + SKIRT_B + SKIRT_T                        # plate half-width incl. skirts
    y0, y1 = -(hd + FRONT_B), hd + BUMPER_CUP_CLR + WALL
    p = box(-x1, x1, y0, y1, 0, PLATE_B)
    p = p.union(box(-(hw + WALL), hw + WALL, -(hd + WALL), y1, 0, 9.0))               # boss round the cup, 9 thick
    for sgn in (-1, 1):
        p = p.union(box(sgn * (hw + SKIRT_B), sgn * x1, y0, y1, 0, PLATE_B + SKIRT_H))
    p = p.cut(cup_cutter(9.0 - BUMPER_CUP_D))
    return p

def stand_jig():
    hw, hl = STAND_W / 2 + STAND_CLR, STAND_L / 2 + STAND_CLR       # 22.3 x 11.85 pocket half-sizes
    x1 = hw + SKIRT_S + SKIRT_T
    y0, y1 = -(hl + FRONT_S + SKIRT_T), hl + WALL
    p = box(-x1, x1, y0, y1, 0, PLATE_S)
    for sgn in (-1, 1):
        p = p.union(box(sgn * (hw + SKIRT_S), sgn * x1, y0, y1, 0, PLATE_S + SKIRT_H))
    p = p.union(box(-x1, x1, y0, y0 + SKIRT_T, 0, PLATE_S + SKIRT_H))               # front skirt
    p = p.cut(box(-hw, hw, -hl, hl, PLATE_S - STAND_POCKET_D, PLATE_S + 1))
    return p

pieces = {"bumper-jig": bumper_jig(), "stand-jig": stand_jig()}
plate = None; y = 0.0
for name, p in pieces.items():
    bb = p.val().BoundingBox(); p0 = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p0, path, tolerance=0.01, angularTolerance=0.1)
    print(f"{name:11s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3")
    check(path, min_rest_frac=0.5, max_down_frac=0.3)
    placed = p0.translate((0, y, 0)); plate = placed if plate is None else plate.add(placed); y += bb.ylen + 10
cq.exporters.export(plate, os.path.join(OUT, "p9-jigs-plate.stl"), tolerance=0.01, angularTolerance=0.1)
print(f"bumper jig: skirt inner faces {SKIRT_B} from the cup sides, front edge {FRONT_B} ahead of the apex; "
      f"stand jig: side skirts {SKIRT_S} from the pocket walls, front skirt {FRONT_S} from the pocket's front wall")
