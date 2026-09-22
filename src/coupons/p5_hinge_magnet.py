# P5 coupon — door hinge knuckle pair + pin + magnet catch (HANDOVER §11.5, ROADMAP §3 P5). Yellow PETG (house rule),
# printed STANDING so every bore is vertical (PRINT-RULES §2: a barrel on a face-down tile has its underside as an
# overhang, so the knuckles are separate standing parts located on the door by pins and glued; the door tile stays flat).
#
# The joint and nothing else (rule 9): a three-segment butt hinge on one axis, two printed pins, two magnet bosses.
#   knuckle-door    the leaf that glues to the door tile's inside face: pad + the two OUTER barrel segments.
#   knuckle-frame   the leaf that goes on the frame: pad + the MIDDLE segment, KNUCKLE_AX_CLR each side.
#   pin-3.0 / 2.9   printed pins, each on a snap-off disc foot so a Ø3 x 34 column prints upright without a brim.
#                   Production may well use a steel rod; these say whether a printed one is good enough.
#   magnet-boss x2  12 x 12 x 3 with the MAG_POCKET_D x MAG_POCKET_H pocket (HANDOVER §5), pocket UP. Two of them so the
#                   pull-apart force can be felt at the 0.5 mm gap the door closes to.
#
# Geometry: the axis lies in the plane where the two pads meet, KNUCKLE_OFF beyond the pads' ends, mid-thickness — so the
# leaves open to a flat 180 (the door "hangs ~20 proud of the tile below", HANDOVER §5) and fold face to face. Segment
# ends are chamfered 45°: it is the axial lead-in AND it means the middle segment's underside is not a floating ceiling.
#
# Pass (ROADMAP §3): pin pushes in and the pair swings free through 180; magnet CA-glues flush in the pocket; two bosses
# pull apart cleanly across a 0.5 gap. Then PIN_HOLE_D and MAG_POCKET are fixed and the door, its knuckles, the magnet
# bosses, the frame L-bracket and the rear tile's tab are all released.
# Output: coupons/p5/<part>.stl and p5-plate.stl.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import PIN_HOLE_D, MAG_POCKET_D, MAG_POCKET_H
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p5")); os.makedirs(OUT, exist_ok=True)

AX_L = 30.0                  # knuckle length along the axis
BARREL_D = 8.0               # OD; PIN_HOLE_D bore leaves a 2.4 wall
PAD_T, PAD_W = 5.0, 18.0     # leaf pad: thickness (stands off the tile face), width up the door
KNUCKLE_AX_CLR = 0.4         # axial gap between segments
KNUCKLE_CHAM = 0.8           # lead-in chamfer on a segment's top end
BARREL_OVL = 1.5             # barrel into the pad's end (tangent would be a zero-thickness union)
SEG = AX_L / 3               # three equal segments: outer-middle-outer
PIN_L, PIN_D = 34.0, (3.0, 2.9)
PIN_FOOT_D, PIN_FOOT_H = 12.0, 0.8     # snap-off disc so the pin prints upright unaided
MAG_BOSS, MAG_BOSS_T = 12.0, 3.0

assert MAG_POCKET_H < MAG_BOSS_T, "magnet pocket deeper than the boss"


def barrel(z0, z1):
    """Barrel segment on the axis, z0 to z1. A segment that starts above the bed has its BOTTOM end coned 45° all the
    way in to the bore, so there is no floating annulus to support; the top end gets a small lead-in chamfer. A segment
    starting at z = 0 keeps its full bottom annulus — that is resting face."""
    full = (BARREL_D - PIN_HOLE_D) / 2                      # cone runs out at the bore: no down-facing ring at all
    b = cq.Workplane("XY").workplane(offset=z0).circle(BARREL_D / 2).extrude(z1 - z0)
    if z0 > 0.01:
        b = b.faces("<Z").chamfer(full - 0.01)
    return b.faces(">Z").chamfer(KNUCKLE_CHAM)


def leaf(spans):
    """A hinge leaf: pad in x 0..PAD_T, y 0..PAD_W, z 0..AX_L, with barrel segments over `spans`.
    Axis at (PAD_T / 2, BARREL_OVL - BARREL_D / 2), on the pad's centre plane and just off its y = 0 end, so the two
    leaves open through a flat 180 and fold face to face. The barrel overlaps the pad by BARREL_OVL — tangent would be
    a zero-thickness union and gives a non-watertight mesh."""
    body = cq.Workplane("XY").box(PAD_T, PAD_W, AX_L, centered=False)
    ax = (PAD_T / 2, BARREL_OVL - BARREL_D / 2)
    for z0, z1 in spans:
        body = body.union(barrel(z0, z1).translate((ax[0], ax[1], 0)))
    bore = cq.Workplane("XY").circle(PIN_HOLE_D / 2).extrude(AX_L + 2).translate((ax[0], ax[1], -1))
    return body.cut(bore)


def pin(d):
    p = cq.Workplane("XY").circle(PIN_FOOT_D / 2).extrude(PIN_FOOT_H)
    p = p.union(cq.Workplane("XY").workplane(offset=PIN_FOOT_H - 0.01).circle(d / 2).extrude(PIN_L))
    return p.faces(">Z").chamfer(0.4)            # lead-in at the tip


def magnet_boss():
    b = cq.Workplane("XY").box(MAG_BOSS, MAG_BOSS, MAG_BOSS_T, centered=(True, True, False)).edges("|Z").fillet(1.0)
    return b.faces(">Z").workplane().circle(MAG_POCKET_D / 2).cutBlind(-MAG_POCKET_H)


if __name__ == "__main__":
    c = KNUCKLE_AX_CLR
    parts = {
        "knuckle-door":  leaf([(0.0, SEG - c / 2), (2 * SEG + c / 2, AX_L)]),
        "knuckle-frame": leaf([(SEG + c / 2, 2 * SEG - c / 2)]),
        f"pin-{PIN_D[0]:.1f}": pin(PIN_D[0]),
        f"pin-{PIN_D[1]:.1f}": pin(PIN_D[1]),
        "magnet-boss": magnet_boss(),
    }
    COPIES = {"magnet-boss": 2}

    placed, x, total = [], 0.0, 0.0
    for name, p in parts.items():
        bb = p.val().BoundingBox()
        p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        vol = p.val().Volume() / 1000
        print(f"{name:16s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {vol:6.2f} cm3")
        check(path, min_rest_frac=0.25, max_down_frac=0.35)
        for _ in range(COPIES.get(name, 1)):
            placed.append(p.val().moved(cq.Location(cq.Vector(x, 0, 0))))
            x += bb.xlen + 8.0; total += vol

    plate = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(OUT, "p5-plate.stl")
    cq.exporters.export(plate, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate.val().BoundingBox()
    print(f"\np5-plate {pb.xlen:.0f} x {pb.ylen:.0f} x {pb.zlen:.0f} mm, {total:.1f} cm3 "
          f"({'FITS' if pb.xlen < 250 and pb.ylen < 250 else 'TOO BIG'} the 256 bed); "
          f"bore {PIN_HOLE_D}, pins {PIN_D}, pocket {MAG_POCKET_D} x {MAG_POCKET_H}")
