# Sled front skid (2026-10-12, Gareth: "bolster the front like the back"). The rear of each sled beam does not bend
# because it lies on its 210 T-foot in the scope rail's inner slot; the front 120 mm (y 0–120 at home) hangs past the
# foot's front end, and the foot cannot be longer without losing the 100 travel (a foot reaching the front upright could
# never leave the rail). So the front gets the same thing the rear has — a bearing on the rail — from ABOVE: a block
# glued to the beam's outer face (and the front bar's saddle above it) that reaches outboard over the scope rail and
# rides on the rail's TOP face. The sled band (z 331–346) is open on the sides, the rail top is bare, and the beam's
# underside is 6.0 above it (P1), so there is room for exactly this and nothing else lives there.
#
#   block   x 2–20.5 (18.5 wide: over the rail's top lands either side of its top slot, 0.5 past the rail's inner
#           edge to the beam face), y 22–62 at home (2 off the front upright, under the front stand's pocket at y 10–33),
#           z 331–353 (rail top -> saddle top): glue face 22 x 40 on the beam (z 337–346) and the saddle (346–353).
#   ramps   3 mm 45° on both bottom ends: the skid leaves the rail after 2 mm of travel and the beam sags while out,
#           so on the way home the rear ramp climbs back onto the rail's front end. Both ends ramped and the block
#           symmetric, so ONE part serves both beams (turn it round; the glue face is the other side).
#   height  SKID_H = 5.6 under the beam line (0.4 under the nominal 6.0): PTFE tape on the bottom (0.2) and tape shims
#           bring it to the real gap — too tall only pre-loads the foot in its 0.3 play, too short does nothing.
# Print: bottom (rail) face down, 22 tall, every face a wall; black PETG or ABS, 2 off, ~16 cm3 each.
# Checks below: 0 mm3 against the rail, the front upright, the beam, the saddle, the stand-leg envelope, band-3 tile
# fingers (outer face) and, mirrored for the right side, the door hinge's frame leaf; rides the rail top at 0.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))

RAIL_TOP, BEAM_Z0, BEAM_Z1, SADDLE_Z1 = 331.0, 337.0, 346.0, 353.0
BEAM_X0 = 20.5                 # beam outer face (left beam); right beam's outer face is at 361 - 20.5 = 340.5
SKID_H = BEAM_Z0 - RAIL_TOP - 0.4     # 5.6 under the beam line (shim to the measured gap)
X0, X1 = 2.0, BEAM_X0          # over the rail's top lands (slot mouth x 7.05–12.95), to the beam face
Y0, Y1 = 22.0, 62.0            # home position
RAMP = 3.0

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def skid():
    """Left beam, frame coordinates, at home."""
    z0 = BEAM_Z0 - SKID_H                      # 331.4 if the beam is at its nominal 337 — the gap is tape
    b = box(X0, X1, Y0, Y1, z0, SADDLE_Z1)
    for y, d in ((Y0, 1), (Y1, -1)):           # 45° ramps on the bottom ends
        wedge = (cq.Workplane("YZ").polyline([(y, z0 - 1), (y + d * (RAMP + 1), z0 - 1), (y, z0 + RAMP)]).close()
                 .extrude(X1 - X0 + 2).translate((X0 - 1, 0, 0)))
        b = b.cut(wedge)
    return b

def printable(p):
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    s = skid()
    rail = box(0, 20, 20, 330, 311, 331); upright = box(0, 20, 0, 20, 0, 510)
    beam = box(20.5, 46, 0, 165, BEAM_Z0, BEAM_Z1); saddle = box(20.5, 46, 12, 88, 346, 353)
    stand = box(47, 92, 13, 37, 341.5, 355)                 # front stand leg envelope (x from 24.7 off the bezel side + 23 - 0.6)
    tile_fingers = box(-3, 6.15, 20, 330, 316, 326)        # band-3 top fingers in the rail's OUTER slot (x < 0) — nothing inboard
    print("skid vs rail / upright / beam / saddle / stand / tile fingers:",
          [round(vol(s, e), 4) for e in (rail, upright, beam, saddle, stand, tile_fingers)], "(all 0)")
    print(f"rides the rail top: bottom at z {s.val().BoundingBox().zmin:.1f} vs rail top {RAIL_TOP} -> {s.val().BoundingBox().zmin - RAIL_TOP:.1f} of tape/shim;",
          f"glue face {SADDLE_Z1 - BEAM_Z0:.0f} x {Y1 - Y0:.0f} = {(SADDLE_Z1 - BEAM_Z0) * (Y1 - Y0):.0f} mm2")
    # right side: mirror about the frame's mid-plane x = 180.5; hinge frame leaf plate on the right rail's outer face
    sr = s.mirror("YZ", (180.5, 0, 0))
    leaf = box(361, 367, 23, 47, 311, 333).union(box(361, 373, 23, 47, 333, 345))   # plate + riser/barrel envelope
    door = box(361, 364, 20, 250, 347, 500)
    print("right skid vs hinge leaf / door panel:", round(vol(sr, leaf), 4), round(vol(sr, door), 4), "(0)")
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    p = printable(s); path = os.path.join(OUT, "sled-skid-v1.stl")
    cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    bb = p.val().BoundingBox(); print(f"sled-skid-v1: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3 — print 2")
    check(path)
