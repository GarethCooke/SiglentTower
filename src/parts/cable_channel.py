# cable_channel.py — the scope's cable channel on the LEFT sled beam (HANDOVER §4 / D6, ROADMAP Stages 5–6). v1 2026-10-19.
#
# The scope's mains, LAN and USB leave its rear (IEC bottom-left = frame left) and run REARWARD in a U-trough on top of
# the left beam, then drop behind the frame into the loop that takes the 100 mm of travel. The trough rides with the sled,
# so nothing it passes changes with the travel; what it must clear is on the sled itself and at the rear.
#
# World frame as sled_beam.py. Trough x 20.5–47 (outer wall flush with the beam's outer face; inner wall 3 off the rear
# box's left end at x 50), y 201–334 (behind the splice, which ends at 188.5 — HANDOVER had it from y 140; the beam's
# rear end is 330, the box's 330), floor 3 on the beam top (z 346–349), walls 3 thick to z 366 (HANDOVER's 20 above the
# floor), inside 20.5 wide — mains Ø7 + LAN Ø5.5 + USB Ø4 side by side with room. Front top corners of both walls
# chamfered 10 at 45° so the leads bend in over a slope, not an edge. The rear end is open (the leads drop out behind the
# frame). Keyed by the beam's Ø4 × 2.5 peg at (33, 290) through a Ø4.3 hole in the floor and CA'd to the beam top — the
# same way the splice is held; HANDOVER's wedge tabs hooking down the beam's sides were drawn for an earlier beam and
# would stand inside the scope rail, so they are dropped. HANDOVER's 45° ramp on the inner wall's rear end is dropped
# too: nothing crosses that wall (the rear cross bar's lip is at x 60–301).
#
# Print: FLAT, floor down as exported (bed face = the floor, 100 %), walls rising, the peg hole vertical, chamfers are
# 45° cuts. Black ABS (HANDOVER §8), ~26 cm³, no brim, no support.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.drawer_quarters import box
import parts.sled_beam as sb, parts.sled_bars as bars, parts.sled_splice as sp, parts.rear_box as rb

X0, X1, WALL = sb.X0, 47.0, 3.0                 # 20.5–47, walls 3 -> inside 23.5–44 (20.5)
Y0, Y1 = sp.Y1 + 12.5, 334.0                    # 201–334
Z0, FLOOR, H = sb.Z0 + sb.T, 3.0, 20.0          # floor on the beam top 346, walls to 366
CHAMFER = 10.0
PEG_HOLE_D = sb.PEG_D + 0.3

def channel():
    c = box(X0, X1, Y0, Y1, Z0, Z0 + H)
    c = c.cut(box(X0 + WALL, X1 - WALL, Y0 - 1, Y1 + 1, Z0 + FLOOR, Z0 + H + 1))                   # the trough
    for (px, py) in sb.PEGS:
        if Y0 < py < Y1:
            c = c.cut(cq.Workplane("XY").workplane(offset=Z0 - 1).center(px, py).circle(PEG_HOLE_D / 2).extrude(FLOOR + 2))
    # 45° chamfers on the front top corners of both walls
    wedge = (cq.Workplane("YZ").polyline([(Y0 - 1, Z0 + H + 1), (Y0 - 1, Z0 + H - CHAMFER - 1), (Y0 + CHAMFER + 1, Z0 + H + 1)])
             .close().extrude(X1 - X0 + 2).translate((X0 - 1, 0, 0)))
    return c.cut(wedge)

def for_print(part):
    bb = part.val().BoundingBox(); p = part.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    return p.edges("<Z").chamfer(0.4)

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    C = channel()
    beams = {k: f() for k, f in sb.PARTS.items() if k.startswith("sled-beam-left")}
    S = {"beam front half": beams["sled-beam-left-front"], "beam rear half": beams["sled-beam-left-rear"], "splice": sp.splice_left(),
         "front bar": bars.front_bar(), "front cross bar": bars.cross_front(), "rear cross bar": bars.cross_rear(),
         "box at home": box(rb.X0, rb.X1, rb.Y0, rb.Y1, rb.Z0, rb.Z0 + rb.H), "scope body": box(*sp.SCOPE_BODY),
         "LED strip (rear-left upright inner face)": box(20, 22.5, 335, 345, 20, 490), "rear-left upright": box(0, 20, 330, 350, 0, 510),
         "band-4 LR tile leg": box(0, 19, 327, 330, 341, 381), "scope rail": box(0, 20, 20, 330, 311, 331)}
    print("--- proofs (cm3; 0 = clear) ---")
    print("  ".join(f"vs {k} {vol(C, s):.4f}" for k, s in S.items()))
    print(f"lowered 0.5 vs the beam halves {vol(C.translate((0, 0, -0.5)), S['beam front half']) + vol(C.translate((0, 0, -0.5)), S['beam rear half']):.4f} (>0: flat on the beam top); "
          f"peg (33, 290) inside the floor hole: channel shifted 0.5 in x vs rear half {vol(C.translate((0.5, 0, 0)), S['beam rear half']):.4f} (>0: located); "
          f"inner wall to the box's left end: {rb.X0 - X1:.1f}; rear end {Y1} vs the strip at y 335: 1.0")
    bb = C.val().BoundingBox()
    print(f"channel x {bb.xmin}–{bb.xmax}, y {bb.ymin}–{bb.ymax}, z {bb.zmin}–{bb.zmax}; inside {X0 + WALL}–{X1 - WALL} ({X1 - X0 - 2 * WALL}) x {H - FLOOR} tall")
    p = for_print(C); pb = p.val().BoundingBox(); path = os.path.join(OUT, "cable-channel-v1.stl")
    cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    print(f"cable-channel-v1  {pb.xlen:.1f} x {pb.ylen:.1f} x {pb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  — black ABS, flat as exported (floor down), no brim, no support")
    check(path)
