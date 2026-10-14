# sled_splice.py — a splice bar glued along the top of each sled beam, from the front bar's saddle to just past the front
# cross bar, bridging the P7 joint (y 165) and the bare span between the saddle (ends y 88) and the foot's front end
# (y 119.5). Gareth, 2026-10-15: the front rests are fitted and the scope's front still sags, mainly with the sled pulled
# out — with the sled out the beam ahead of the foot hangs 117 mm and the joint is where the halves give.
#
# Where it can go: the beam's OUTER strip, x 20.5–46 on the left (the mirror on the right), is the only clear top surface:
# inboard of it the cup boss (x 46.5–86, y 91–126) and the stand arm. Height 7.5: the scope body (x 27.7+) is at z 355,
# the beam top at 346 — 1.5 clear. Length y 88.5–200: 0.5 behind the saddle's rear face, over the joint, past the front
# cross bar's line (the bar itself runs between the beams, x 60–301, so the strip is free there). The left beam's
# cable-channel peg at (33, 150) passes through a Ø4.3 hole — it locates the splice; the right beam has no pegs, so one
# part serves both sides (hole unused on the right).
#
# Costs, stated: (1) the rear box's exit lane — with the sled out the box slides right across the right beam's top at
# y 95–230 with its floor at 346; the right splice stands 7.5 in that lane, so the box is LIFTED 7.5 mm as it crosses
# the beam (its top goes to 464, the door opening runs to 490). (2) The planned cable channel (x 20–46 from y 140) now
# starts at y 201 — it is not modelled yet, so nothing printed changes.
#
# Fit: CA the splice's underside and front end; press it onto the beam top with its front end against the saddle's rear
# face (and the peg in the hole on the left); hold 30 s. Both beams.
# Print: flat as exported, 111.5 x 25.5 x 7.5, ~21 cm³, black ABS or PETG, two off; no brim, no support.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from parts.drawer_quarters import box
import parts.sled_beam as sb
import parts.sled_bars as bars
import parts.rear_box as rb

X0, X1 = sb.X0, 46.0                           # 20.5–46: the outer strip, clear of the cup boss (46.5+)
Y0, Y1 = bars.SADDLE[3] + 0.5, 200.0           # 88.5 (saddle ends at 88) to 200
Z0, H = sb.Z0 + sb.T, 7.5                      # on the beam top 346, 1.5 under the scope body at 355
PEG_HOLE_D = sb.PEG_D + 0.3                    # 4.3 over the Ø4 channel peg at (33, 150)
SCOPE_BODY = (27.7, 333.3, 3.0, 111.0, 355.0, 507.0)      # blue body inset 4.7 behind the bezel (P9 jigs)

def splice_left():
    s = box(X0, X1, Y0, Y1, Z0, Z0 + H)
    for (px, py) in sb.PEGS:
        if Y0 < py < Y1:
            s = s.cut(cq.Workplane("XY").workplane(offset=Z0 - 1).center(px, py).circle(PEG_HOLE_D / 2).extrude(H + 2))
    return s

def splice_right(): return sb.mirror_right(splice_left())

def for_print(part):
    bb = part.val().BoundingBox(); p = part.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    return p.edges("<Z").chamfer(0.4)

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    L, R = splice_left(), splice_right()
    beams = {k: f() for k, f in sb.PARTS.items()}
    front_bar, xf = bars.front_bar(), bars.cross_front()
    scope = box(*SCOPE_BODY)
    for name, s, keys in (("left", L, ("sled-beam-left-front", "sled-beam-left-rear")), ("right", R, ("sled-beam-right-front", "sled-beam-right-rear"))):
        vb = sum(vol(s, beams[k]) for k in keys)
        down = sum(vol(s.translate((0, 0, -0.5)), beams[k]) for k in keys)
        print(f"{name} splice: vs beam halves {vb:.4f} cm3 (0); lowered 0.5 {down:.4f} (>0, flat on the beam top); vs front bar + saddle {vol(s, front_bar):.4f} (0); "
              f"vs front cross bar {vol(s, xf):.4f} (0); vs scope body {vol(s, scope):.4f} (0); shifted 0.6 forward {vol(s.translate((0, -0.6, 0)), front_bar):.4f} (>0, butts the saddle)")
    bb = L.val().BoundingBox()
    print(f"left splice x {bb.xmin}–{bb.xmax}, y {bb.ymin}–{bb.ymax}, z {bb.zmin}–{bb.zmax}: peg at (33, 150) in a Ø{PEG_HOLE_D} hole; cup boss starts x {sb.CUP_BOSS[0]}; scope body from z {SCOPE_BODY[4]}")
    # the costs: the box exit lane on the right (sled out 100 -> box at y 95–230) and the planned channel on the left
    box_out = box(rb.X0, rb.X1, rb.Y0 - 100, rb.Y1 - 100, rb.Z0, rb.Z0 + rb.FLOOR)
    print(f"right splice vs the rear box crossing the beam with the sled out: {vol(R, box_out):.3f} cm3 (>0 — the box is lifted {H} mm over it; "
          f"lifted {H}: {vol(R, box_out.translate((0, 0, H))):.3f})")
    chan = box(20, 46, 140, 334, 346, 366)
    print(f"left splice vs the PLANNED cable channel (x 20–46 from y 140): {vol(L, chan):.3f} cm3 — the channel starts at y {Y1 + 1:.0f} when it is modelled")
    p = for_print(L); pb = p.val().BoundingBox(); path = os.path.join(OUT, "sled-splice-v1.stl")
    cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    print(f"sled-splice-v1  {pb.xlen:.1f} x {pb.ylen:.1f} x {pb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3  — print TWO, flat as exported (the hole is unused on the right)")
    check(path)
