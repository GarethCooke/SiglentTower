# Sled front rest v2 (2026-10-12) — BOLTED, not glued: a plate on the scope rail's top face at its front end, one
# countersunk M5 into the rail's TOP slot, with a 1.8 mm lip standing up beside the rail's inner edge to the beam's
# underside. v1 (same evening, withdrawn before printing) was a fin CA'd to the front upright's inner face.
#
# The problem: each sled beam lies on its 210 T-foot from y 119.5 back and hangs free for the 108 mm in front of it;
# under the scope's front stand that length bends, and the rails were lowered to live with it. Anything outboard of
# the beam's outer face (x 20.5) above the rail is blocked by the front upright as soon as the sled moves; under the
# beam is the AWG (1 mm below its front frame, 3.5 below its body). What IS free: the rail's own top face (z 331),
# 6.0 under the beam, and the strip between the rail's inner edge and the foot's web, x 20–22.2, which the beam's
# solid outer wall (x 20.5–22, solid along the whole beam) passes straight over.
#
#   plate   x 2–20, y 21–61, z 331–334 on the rail top (lands either side of the top slot mouth x 7.05–12.95);
#           one M5 x 10 countersunk at (10, 41) into a drop-in T-nut in the top slot.
#   lip     x 20–21.8, y 21–61, z 331–337: top at the beam's underside, 0.4 off the foot's web (x 22.2), 0.2 off the
#           beam's groove (x 22.0, open underneath from y 119.5 back). The beam's outer wall rides on it along the
#           WHOLE travel (the lip is always under some part of the 318 mm beam), so the front is carried at y 21–61 —
#           under the front stand (y 13–36) at home — exactly as the rear is carried on the foot. Nothing to climb.
#   height  6.0 = the nominal beam line (P1: 6.0 ± 0.3). Short by 0.3 only pre-loads the foot in its play; long by 0.3
#           means the beam settles 0.3 before it bears. Tape under the plate raises it if needed.
# Symmetric in y, lip on one edge: the right side is the same part turned 180° (lip x 339.2–341 on the right rail,
# 1.2 clear of the column drawer at 338). Print: bottom face down (the rail face), lip and countersink up, 2 off.
# Proofs below: 0 mm³ against the rail (it sits ON it), the front upright, the real beam and foot slid 0–100 in
# 10 mm steps, the front bar, the AWG's front frame and body, the left AWG cradle; mirrored right, 0 against the
# column facia, drawer, housing-top envelope and the door hinge's frame leaf.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import SLOT_MOUTH

RAIL_TOP, BEAM_Z0 = 331.0, 337.0
PX0, PX1, PY0, PY1, PT = 2.0, 20.0, 21.0, 61.0, 3.0      # plate on the rail top
# 2026-10-13, Gareth: the gap between the rail's inner face and the beam's outer face is LARGER than the 0.5 designed,
# so the lip must be wider. The foot and beam move as one unit, so the foot's web is always 1.7 inboard of the beam's
# outer face (1.5 wall + 0.2 groove clearance) and the lip's outer edge stops 0.4 short of the web whatever the gap:
#     lip outer edge = 20 + GAP + 1.3        (bears on 1.3 of the beam's 1.5 outer wall)
# One STL per plausible gap, the gap stamped on the plate: measure the gap at the front, print the matching one.
GAPS = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
def lip_x1(gap): return 20.0 + gap + 1.3
LX1 = lip_x1(0.5)                                         # 21.8 at the design gap (foot web at 22.2, beam groove at 22.0)
HOLE_D, CSK_D, CSK_DEPTH = 5.5, 10.6, 2.55                # M5 clearance, 90° countersink flush in the 3 mm plate
HX, HY = 10.0, (PY0 + PY1) / 2

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def rest(gap=0.5):
    """Left scope rail, frame coordinates. `gap` = rail inner face to beam outer face, as measured."""
    lx1 = lip_x1(gap)
    r = box(PX0, PX1 + 0.01, PY0, PY1, RAIL_TOP, RAIL_TOP + PT).union(box(PX1, lx1, PY0, PY1, RAIL_TOP, BEAM_Z0))
    hole = cq.Workplane("XY").workplane(offset=RAIL_TOP - 1).center(HX, HY).circle(HOLE_D / 2).extrude(PT + 2)
    csk = cq.Workplane("XY").add(cq.Solid.makeCone(HOLE_D / 2, CSK_D / 2 + 1, CSK_DEPTH + 1,
                                                   pnt=cq.Vector(HX, HY, RAIL_TOP + PT - CSK_DEPTH), dir=cq.Vector(0, 0, 1)))
    r = r.cut(hole).cut(csk)
    stamp = (cq.Workplane("XY").workplane(offset=RAIL_TOP + PT - 0.4).center(11.0, PY1 - 8.0)
             .text(f"{gap:.1f}", 4.0, 1.0, combine=False, halign="center", valign="center"))
    return r.cut(stamp)

def printable(p):
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    rail = box(0, 20, 20, 330, 311, 331).cut(box(10 - SLOT_MOUTH / 2, 10 + SLOT_MOUTH / 2, 20, 330, 331 - 6.15, 331.01))   # with its top slot mouth
    upright = box(0, 20, 0, 20, 0, 510); bar = box(23, 338, 0, 12, 337, 355)
    bezel = box(23, 237, 3, 17, 248, 336); awg = box(26.5, 233.5, 3, 263, 251.5, 333.5)
    from parts.awg_cradle import left_cradle
    cradle = left_cradle().translate((0, 20, 0))
    tile_fingers = box(-3, 6.15, 20, 330, 316, 326)        # band-3 top fingers live in the OUTER slot, inside the rail
    from parts.sled_beam import left_front, left_rear
    from parts.sled_foot import foot as sfoot, X_BOTTOM, Z0_WORLD
    beam0 = left_front().union(left_rear())
    ft0 = sfoot(210.0).rotate((0, 0, 0), (0, 0, 1), -90).translate((X_BOTTOM, 0, Z0_WORLD))
    fb = ft0.val().BoundingBox(); ft0 = ft0.translate((0, 119.5 - fb.ymin, 0))
    facia = box(273, 338, 0, 3, 91, 336); drawer = box(274, 338, 3, 288, 91, 331); htop = box(242, 338, 3, 300, 333, 336)
    leaf = box(361, 367, 23, 47, 311, 333).union(box(361, 373, 23, 47, 333, 345)); rrail = box(341, 361, 20, 330, 311, 331)
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    for gap in GAPS:
        r = rest(gap); dx = gap - 0.5                       # the foot + beam unit sits `gap` off the rail face
        beam = beam0.translate((dx, 0, 0)); ft = ft0.translate((dx, 0, 0))
        fixed = [round(vol(r, e), 4) for e in (rail, upright, bar, bezel, awg, cradle, tile_fingers)]
        worst = max(vol(r, beam.translate((0, -t, 0))) + vol(r, ft.translate((0, -t, 0))) for t in range(0, 101, 10))
        bears = vol(r, beam.translate((0, 0, -0.5)))
        rr = r.mirror("YZ", (180.5, 0, 0)); right = [round(vol(rr, e), 4) for e in (facia, drawer, htop, leaf, rrail)]
        print(f"gap {gap:.1f}: lip x 20–{lip_x1(gap):.1f}; fixed parts {fixed} (0); beam+foot slid 0..100 worst {worst:.4f} (0); "
              f"beam lowered 0.5 bears {bears:.4f} (>0); right side {right} (0)")
        p = printable(r); path = os.path.join(OUT, f"sled-front-rest-v2-gap{gap:.1f}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        check(path)
    bb = p.val().BoundingBox()
    print(f"\nsled-front-rest-v2-gap<g>.stl: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}, ~{p.val().Volume()/1000:.1f} cm3 — measure the gap, print that one twice; 2 x M5 x 10 countersunk + 2 drop-in T-nuts")
