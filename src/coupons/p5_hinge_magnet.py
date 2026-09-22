# P5 coupon — door hinge + magnet catch (HANDOVER §11.5, ROADMAP §3 P5). Yellow PETG, standing as exported.
#
# v2 2026-09-22. v1 was a generic block and FAILED: its bore sat on the pads' mid-thickness, so the leaves could not
# fold and the two bores ended up one pad-thickness apart — the pin would not pass. That is exactly what ROADMAP §0.3
# forbids ("each coupon is a literal section of the production part, in the production orientation, not a generic
# block"); with no production part to cut it from, nothing caught the error. So v2 IS the production part:
# `src/parts/door_hinge.py` models the real knuckles against the frame, and this plate prints one of each.
#
# Plate: one hinge-door + one hinge-frame, as exported. Test with a pin from the v1 plate (they are unchanged):
#   - the pin pushes through all three barrel segments and the pair swings free through 180
#   - the frame leaf's plate sits flat on the scope rail's outer face, M5 x 12 into a T-nut at z 321
#   - the door leaf's shelf catches a 3 mm panel offcut squarely, flush front and bottom
# Pass sets PIN_HOLE_D and releases the door, both knuckles, the magnet bosses, the frame L-bracket and the rear tile's
# tab. Print one pair, check, then print the second pair — the parts are the production ones, so a pass is a build.
#
# The magnet half of P5 is independent of all this and already printed from v1: two 12 x 12 x 3 bosses with the
# MAG_POCKET_D x MAG_POCKET_H pocket, and two Ø3 pins on snap-off discs. `magnet_boss()` and `pin()` stay here so the
# production bosses come from the same script.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "..", "parts"))
from fit import PIN_HOLE_D, MAG_POCKET_D, MAG_POCKET_H
from printcheck import check
import door_hinge as dh
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p5")); os.makedirs(OUT, exist_ok=True)

PIN_L, PIN_D = 34.0, (3.0, 2.9)
PIN_FOOT_D, PIN_FOOT_H = 12.0, 0.8     # snap-off disc so a Ø3 x 34 column prints upright unaided
MAG_BOSS, MAG_BOSS_T = 12.0, 3.0
assert MAG_POCKET_H < MAG_BOSS_T, "magnet pocket deeper than the boss"
assert PIN_L > dh.KN_L + 4, "pin shorter than the knuckle"


def pin(d):
    p = cq.Workplane("XY").circle(PIN_FOOT_D / 2).extrude(PIN_FOOT_H)
    p = p.union(cq.Workplane("XY").workplane(offset=PIN_FOOT_H - 0.01).circle(d / 2).extrude(PIN_L))
    return p.faces(">Z").chamfer(0.4)


def magnet_boss():
    b = cq.Workplane("XY").box(MAG_BOSS, MAG_BOSS, MAG_BOSS_T, centered=(True, True, False)).edges("|Z").fillet(1.0)
    return b.faces(">Z").workplane().circle(MAG_POCKET_D / 2).cutBlind(-MAG_POCKET_H)


if __name__ == "__main__":
    parts = {
        "knuckle-door-v2":  dh.printable(dh.door_leaf()),
        "knuckle-frame-v2": dh.printable(dh.frame_leaf()),
    }
    if "--all" in sys.argv:                      # v1 already printed these; regenerate only on request
        parts[f"pin-{PIN_D[0]:.1f}"] = pin(PIN_D[0])
        parts[f"pin-{PIN_D[1]:.1f}"] = pin(PIN_D[1])
        parts["magnet-boss"] = magnet_boss()

    placed, x, total = [], 0.0, 0.0
    for name, p in parts.items():
        bb = p.val().BoundingBox()
        p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        vol = p.val().Volume() / 1000
        print(f"{name:18s} {bb.xlen:5.1f} x {bb.ylen:5.1f} x {bb.zlen:5.1f}   {vol:5.2f} cm3")
        check(path, min_rest_frac=0.3, max_down_frac=0.2)
        placed.append(p.val().moved(cq.Location(cq.Vector(x, 0, 0)))); x += bb.xlen + 8.0; total += vol

    plate = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(OUT, "p5-v2-plate.stl")
    cq.exporters.export(plate, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate.val().BoundingBox()
    print(f"\np5-v2-plate {pb.xlen:.0f} x {pb.ylen:.0f} x {pb.zlen:.0f} mm, {total:.1f} cm3 "
          f"({'FITS' if pb.xlen < 250 and pb.ylen < 250 else 'TOO BIG'} the 256 bed); bore {PIN_HOLE_D}, "
          f"pocket {MAG_POCKET_D} x {MAG_POCKET_H}")
