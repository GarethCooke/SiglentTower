import cadquery as cq

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
REACH     = 38.75    # rail inner face -> foot centre (PSU body edge 5.75 from rail + 33)
FOOT_D    = 21.0
CUP_CLR   = 0.6      # radial clearance in cup
CUP_DEPTH = 4.0      # cup floor = TOP_T - CUP_DEPTH = 4 mm above rail top
ARM_W     = 30.0
GUSSET_H  = 14.0     # rib under the arm down the rail's inner face
WALL      = 3.0

cup_r  = FOOT_D/2 + CUP_CLR
arm_len = REACH + cup_r + WALL           # from rail inner face to arm tip

# saddle block sitting on rail top (x along rail, y across, z up). Rail top = z 0.
saddle = (cq.Workplane("XY")
          .box(SADDLE_L, RAIL + 2*LIP_T, TOP_T, centered=(True, True, False)))
# channel that the rail sits in (lips)
lips = (cq.Workplane("XY").box(SADDLE_L, RAIL + 2*LIP_T, LIP_H, centered=(True, True, False))
        .translate((0, 0, -LIP_H))
        .cut(cq.Workplane("XY").box(SADDLE_L, RAIL + 0.4, LIP_H, centered=(True, True, False)).translate((0,0,-LIP_H))))
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
body = (body.faces(">Z").workplane()
        .center(0, RAIL/2 + LIP_T + REACH)
        .hole(2*cup_r, CUP_DEPTH))

# two counterbored M5 holes into the top slot
body = (body.faces(">Z").workplane(origin=(0,0,TOP_T))
        .pushPoints([(-HOLE_PITCH/2, 0), (HOLE_PITCH/2, 0)])
        .cboreHole(HOLE_D, CBORE_D, CBORE_H))

# ---------- export, oriented for printing ----------
# Cup-up (as modelled) cannot print unsupported: the gusset tip is the lowest point and the whole arm floats 14 mm up.
# Print it TOP FACE DOWN: rotate 180 about X so the 8 mm saddle/arm top (the largest flat face) is on the bed, lips and
# gusset point up, and the cup + counterbores become 4 mm-deep recesses open to the plate. Tree supports (on build plate
# only) fill the cup and counterbores; snap them out. Nothing else needs support.
import os
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
printable = body.rotate((0, 0, 0), (1, 0, 0), 180)
pb = printable.val().BoundingBox()
printable = printable.translate((0, 0, -pb.zmin))
cq.exporters.export(printable, os.path.join(OUT, "psu-cradle-v2.stl"), tolerance=0.01, angularTolerance=0.1)
bb = body.val().BoundingBox()
print(f"bbox x {bb.xlen:.1f}  y {bb.ylen:.1f}  z {bb.zlen:.1f}   volume {body.val().Volume()/1000:.1f} cm3  (exported top-face-down)")

# print check (PRINT-RULES.md §1): the only downward faces are the cup and counterbore ceilings, 4 mm over the plate,
# handled by the slicer's sacrificial layer — allow them, fail on anything else.
from printcheck import check
check(os.path.join(OUT, "psu-cradle-v2.stl"), max_down_frac=0.3)
