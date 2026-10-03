import cadquery as cq
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# ---------- parameters (mm) ----------
RAIL      = 20.0     # 2020
LIP_T     = 3.0      # side lips either side of rail
LIP_H     = 6.0      # how far lips drop down the rail sides
TOP_T     = 8.0      # thickness of saddle/arm above rail top
SADDLE_L  = 40.0     # length along rail
HOLE_PITCH= 20.0     # two M5 holes along the top slot
HOLE_D    = 5.5
CBORE_D   = 10.0
CBORE_H   = 4.0
REACH_V3  = 38.75    # left pair as printed (cup 41.75 from the rail face — see cradle())
REACH_V4R = 30.75    # right pair v4 2026-10-02: cup 8 nearer the inner rail (33.75 from its left face). Bench 2026-10-03: the REAR
                     # right foot sits in its v4 cup; the FRONT right foot wants the cup 'a few mm' further out than v4 (the PSU sits
                     # very slightly skewed) -> one more part:
REACH_V5RF = 34.75   # right FRONT only, v5: cup 37.75 from the inner rail's face — midway between v4 (33.75) and v3 (41.75)
def cradle(reach):
    """PSU corner cradle; reach = rail inner face... NOTE the code adds reach after the 3 mm lip, so the cup centre sits
    reach + 3 from the rail's inner face (the v3 'bug': 38.75 -> 41.75). v3 (left pair, as printed) keeps 38.75; right rear is
    v4 (30.75); right front is v5 (34.75), set on the bench 2026-10-03."""
    REACH = reach
    from fit import PSU_FOOT_PAD_D, PSU_FOOT_D4, CUP_CLR, RAIL_CLR   # v3: conical cup matching the measured foot taper, clearance from the P2 coupons
    CUP_DEPTH = 4.0      # cup floor = TOP_T - CUP_DEPTH = 4 mm above rail top
    CUP_LEAD  = 1.0      # 45° lead-in at the cup rim so the foot's 21.5 edge finds a 22.1 printed cup
    ARM_W     = 30.0
    GUSSET_H  = 14.0     # rib under the arm down the rail's inner face
    WALL      = 3.0

    cup_r0 = PSU_FOOT_PAD_D/2 + CUP_CLR   # cup floor radius 8.5 (coupon -2 winner: prints as a light, rattle-free fit on the 16.8 pad)
    cup_r  = PSU_FOOT_D4/2  + CUP_CLR   # cup rim radius 9.85 at 4 mm up (19.5 foot)
    arm_len = REACH + cup_r + WALL           # from rail inner face to arm tip

    # saddle block sitting on rail top (x along rail, y across, z up). Rail top = z 0.
    saddle = (cq.Workplane("XY")
              .box(SADDLE_L, RAIL + 2*LIP_T, TOP_T, centered=(True, True, False)))
    # channel that the rail sits in (lips)
    lips = (cq.Workplane("XY").box(SADDLE_L, RAIL + 2*LIP_T, LIP_H, centered=(True, True, False))
            .translate((0, 0, -LIP_H))
            .cut(cq.Workplane("XY").box(SADDLE_L, RAIL + RAIL_CLR, LIP_H, centered=(True, True, False)).translate((0,0,-LIP_H))))
    body = saddle.union(lips)

    # arm extending inward (+y) from the inner lip
    arm = (cq.Workplane("XY").box(ARM_W, arm_len + LIP_T, TOP_T, centered=(True, False, False))
           .translate((0, RAIL/2, 0)))
    body = body.union(arm)
    # round the arm tip
    body = body.edges("|Z").edges(">Y").fillet(ARM_W/2 - 0.01)

    # gusset under the arm against the inner rail face
    gus = (cq.Workplane("YZ").polyline([(RAIL/2 + LIP_T, 0), (RAIL/2 + LIP_T, -GUSSET_H), (RAIL/2 + LIP_T + arm_len*0.75, 0)]).close()
           .extrude(ARM_W/2, both=True))
    body = body.union(gus)

    # foot cup
    # conical cup: floor radius cup_r0 at z = TOP_T - CUP_DEPTH, rim radius cup_r at z = TOP_T — matches the foot's own taper so it self-centres
    cup = cq.Workplane("XY").add(cq.Solid.makeCone(cup_r0, cup_r, CUP_DEPTH,
            pnt=cq.Vector(0, RAIL/2 + LIP_T + REACH, TOP_T - CUP_DEPTH), dir=cq.Vector(0, 0, 1)))
    body = body.cut(cup)
    # 45° lead-in at the cup rim (a cone cut, so no edge selection ambiguity with the counterbores)
    lead = cq.Workplane("XY").add(cq.Solid.makeCone(cup_r, cup_r + CUP_LEAD, CUP_LEAD,
            pnt=cq.Vector(0, RAIL/2 + LIP_T + REACH, TOP_T - CUP_LEAD), dir=cq.Vector(0, 0, 1)))
    body = body.cut(lead)

    # two counterbored M5 holes into the top slot
    body = (body.faces(">Z").workplane(origin=(0,0,TOP_T))
            .pushPoints([(-HOLE_PITCH/2, 0), (HOLE_PITCH/2, 0)])
            .cboreHole(HOLE_D, CBORE_D, CBORE_H))


    return body
# ---------- export, oriented for printing ----------
# Cup-up (as modelled) cannot print unsupported: the gusset tip is the lowest point and the whole arm floats 14 mm up.
# Print it TOP FACE DOWN: rotate 180 about X so the 8 mm saddle/arm top (the largest flat face) is on the bed, lips and
# gusset point up, and the cup + counterbores become 4 mm-deep recesses open to the plate. Tree supports (on build plate
# only) fill the cup and counterbores; snap them out. Nothing else needs support.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # for printcheck
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)   # repo-root parts/

def printable(body):
    p = body.rotate((0, 0, 0), (1, 0, 0), 180); bb = p.val().BoundingBox()
    return p.translate((0, 0, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    for name, reach in (("psu-cradle-v3", REACH_V3), ("psu-cradle-right-v4", REACH_V4R), ("psu-cradle-right-front-v5", REACH_V5RF)):
        body = cradle(reach); path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(printable(body), path, tolerance=0.01, angularTolerance=0.1)
        bb = body.val().BoundingBox()
        print(f"{name}: bbox x {bb.xlen:.1f}  y {bb.ylen:.1f}  z {bb.zlen:.1f}   volume {body.val().Volume()/1000:.1f} cm3  cup centre {RAIL/2 + LIP_T + reach:.2f} from the saddle centre = {LIP_T + reach:.2f} from the rail face")
        check(path, max_down_frac=0.3)
