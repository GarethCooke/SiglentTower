# P8 coupon — the TPU plate (ROADMAP §2 plate D, §3 P8). Blue TPU, flat, one plate. P8 owns exactly one fit.py value,
# SPIGOT_D, but the plate exists to prove every TPU part in the project in one print: the frame feet, the AWG pads, the
# sled-stop caps and the slot covers all use the same filament and the same profile, and none of them has been printed.
#
# Five parts on the plate:
#   spigots-sweep  the only real measurement. SPIGOT_D is a guess (fit.py: "~4.2 nominal; expect ~4.6") because the
#                  CNCMANS 2020's centre bore has never been put on calipers. Four spigots at SPIGOT_SWEEP on a 3 mm
#                  strip, diameter stamped beside each: push the strip's spigots into an offcut's bore, one at a time.
#                  Winner = goes in by thumb, holds the frame's weight, comes out with a twist. That sets SPIGOT_D.
#   foot-24        one production foot, 24 x 24 x 6 with an 8 mm spigot at the sweep's middle value (HANDOVER §8).
#                  Prints pad-down, spigot up — exactly as it sits on the bench. Tests how TPU at these settings sits:
#                  no wobble, no rock, doesn't squirm under 12 kg of frame.
#   awg-pad        20 x 20 x 5.5 for the AWG cradles' 20.4 x 20.4 x 1.5 pocket (src/parts/awg_cradle.py, printed), 4
#                  proud so the body lands at z 251.5. Carries the corner lips the cradles gave up: this is the REAR
#                  pattern (outer + rear, an L); the front pads get the outer lip only, the bezel is their front stop.
#                  Test: presses into a printed cradle's pocket and stays, body corner sits inside the L.
#   slot-cover     60 mm press-in strip for the 5.9 mouth (cable plan, ROADMAP §0) — two head widths, stamped. Profile:
#                  a head SLOT_LIP_T deep so the cover finishes flush with the rail face, then a 45° flare out to
#                  COVER_FLARE_W behind the lips. Printed head-UP, so the flare's lead-in is the bed face and the
#                  retaining step (flare -> head) faces up = under the lip. Nothing overhangs.
#   stop-cap       sled pull-out stop (HANDOVER §4: "T-nut + TPU cap at the slot front"). The T-nut in the slot is the
#                  hard stop; this is the pad that keeps the foot from hitting it metal-to-metal. Cavity section
#                  FOOT_FLANGE_W x CAP_L x CAP_H — the same width the foot's own flange runs at — CA-glued to the
#                  T-nut's face BEFORE the T-nut goes into the rail (both enter from the rail end, as the foot does).
#                  Two of them: one per scope rail.
#
# Print: blue TPU, flat as exported, no brim needed (TPU sticks), 0.20 mm, slow outer walls. Everything rises from its
# bed face; printcheck should report no down-facing area above the bed on any part.
# Output: coupons/p8/<part>.stl and p8-plate.stl (all of them laid out on one bed).
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import SPIGOT_D, SLOT_MOUTH, SLOT_LIP_T, SLOT_CAVITY_W, SLOT_THROAT_D, SLOT_DEPTH, SLOT_BOTTOM_W, FOOT_FLANGE_W
from printcheck import check
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p8")); os.makedirs(OUT, exist_ok=True)

# ---- frame foot (HANDOVER §8: "feet 24 x 24 x 6, 5 mm spigot into the extrusion bore") ----
FOOT_W, FOOT_H = 24.0, 6.0
SPIGOT_H, SPIGOT_LEAD = 8.0, 1.0            # lead-in chamfer at the tip so it starts in the bore square
SPIGOT_SWEEP = (4.2, 4.6, 5.0, 5.4)         # SPIGOT_D 5.0 is the spec figure; the bore is nominally ~4.2. Bracket both.

# ---- AWG pad (src/parts/awg_cradle.py: PAD 20, POCKET_D 1.5, pocket 20.4 square, pad stands 4 proud) ----
PAD, PAD_H, PAD_SEAT = 20.0, 5.5, 1.5       # 5.5 tall, 1.5 of it in the pocket, 4 proud -> body at 251.5
PAD_LIP_W, PAD_LIP_H = 2.0, 2.0             # corner lip: 2 wide, 2 above the pad top, against the body's bottom corner

# ---- slot cover (5.9 mouth, 1.75 lips, 10.6 cavity) ----
COVER_L = 60.0
COVER_HEAD_W = (SLOT_MOUTH + 0.1, SLOT_MOUTH + 0.4)   # 6.0 / 6.3 in the 5.9 mouth — TPU squashes, so interference is the point
COVER_FLARE_W = 8.4                          # behind the lips, well inside the 10.6 cavity
COVER_FLARE_H = (COVER_FLARE_W - SLOT_MOUTH) / 2      # 45° lead-in: rises as fast as it widens
# usable cable depth under a flush cover = SLOT_DEPTH - SLOT_LIP_T - COVER_FLARE_H
CABLE_DEPTH = SLOT_DEPTH - SLOT_LIP_T - COVER_FLARE_H

# ---- sled stop cap ----
CAP_L, CAP_H = 5.0, 4.0                      # along the slot, and up the cavity from the lip underside

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def stamp(part, x, y, text, size=4.0, depth=0.5, z=None):
    """Deboss a label into the face at height `z` (default: the part's highest face)."""
    zt = part.val().BoundingBox().zmax if z is None else z
    return part.cut(cq.Workplane("XY").workplane(offset=zt - depth).center(x, y)
                    .text(text, size, depth + 1, combine=False, halign="center", valign="center"))

def spigot(d, h=SPIGOT_H, z0=0.0):
    """Spigot rising from z0, with a 45° lead-in at the tip (self-supporting, and it starts square in the bore)."""
    body = cq.Workplane("XY").workplane(offset=z0).circle(d / 2).extrude(h - SPIGOT_LEAD)
    tip = (cq.Workplane("XY").workplane(offset=z0 + h - SPIGOT_LEAD)
           .add(cq.Solid.makeCone(d / 2, d / 2 - SPIGOT_LEAD, SPIGOT_LEAD,
                                  pnt=cq.Vector(0, 0, z0 + h - SPIGOT_LEAD), dir=cq.Vector(0, 0, 1))))
    return body.union(tip)

def foot(d=None):
    """Production foot: 24 x 24 x 6 pad, spigot up. Bed face = the whole 24 x 24 pad (it is the bench face in use)."""
    d = SPIGOT_SWEEP[len(SPIGOT_SWEEP) // 2 - 1] if d is None else d      # 4.6, the middle of the sweep
    pad = cq.Workplane("XY").box(FOOT_W, FOOT_W, FOOT_H, centered=(True, True, False)).edges("|Z").fillet(2.0)
    return pad.union(spigot(d, z0=FOOT_H - 0.01)), d

def spigot_strip():
    """The sweep: four spigots on a 3 mm strip, diameter stamped beside each. Push each into a 2020 offcut's bore."""
    t, pitch, margin = 3.0, 18.0, 9.0
    w = (len(SPIGOT_SWEEP) - 1) * pitch + 2 * margin
    s = cq.Workplane("XY").box(w, 26.0, t, centered=(True, True, False))
    for i, d in enumerate(SPIGOT_SWEEP):
        x = (i - (len(SPIGOT_SWEEP) - 1) / 2) * pitch
        s = s.union(spigot(d, z0=t - 0.01).translate((x, 5.0, 0)))
        s = stamp(s, x, -7.5, f"{d:.1f}", size=5.0, z=t)      # into the strip's own top face, not the spigot tips
    return s

def awg_pad():
    """20 x 20 x 5.5 pad with the REAR corner lips (outer edge + rear edge). Outer = -x, rear = +y."""
    p = box(0, PAD, 0, PAD, 0, PAD_H)
    p = p.union(box(0, PAD_LIP_W, 0, PAD, PAD_H, PAD_H + PAD_LIP_H))                 # outer lip, full length
    p = p.union(box(0, PAD, PAD - PAD_LIP_W, PAD, PAD_H, PAD_H + PAD_LIP_H))         # rear lip
    return p.edges("|Z").fillet(0.8)

def slot_cover(head_w, length=COVER_L):
    """Printed HEAD UP: bed = the flare's narrow lead-in face, then 45° out to COVER_FLARE_W, then a step in to head_w
    (the retaining face, pointing up = under the lip in use), then head_w for SLOT_LIP_T so the cover finishes flush."""
    z_flare = COVER_FLARE_H
    base_w = COVER_FLARE_W - 2 * COVER_FLARE_H   # narrow face on the bed; 45° out to COVER_FLARE_W
    pts = [(-base_w / 2, 0.0), (base_w / 2, 0.0),
           (COVER_FLARE_W / 2, z_flare), (head_w / 2, z_flare),
           (head_w / 2, z_flare + SLOT_LIP_T), (-head_w / 2, z_flare + SLOT_LIP_T),
           (-head_w / 2, z_flare), (-COVER_FLARE_W / 2, z_flare)]
    c = cq.Workplane("XZ").polyline(pts).close().extrude(length).translate((0, length / 2, 0))
    return stamp(c, 0, 0, f"{head_w:.1f}", size=3.5, depth=0.4)

def stop_cap():
    """Cavity-section pad, CA-glued to the T-nut's face. FOOT_FLANGE_W wide (the section the foot's own flange runs at),
    CAP_L along the slot, CAP_H up from the lip underside. Flat on the bed, nothing overhangs."""
    return box(-FOOT_FLANGE_W / 2, FOOT_FLANGE_W / 2, 0, CAP_L, 0, CAP_H).edges("|Z").fillet(0.8)

if __name__ == "__main__":
    parts = {}
    f, fd = foot(); parts["foot-24"] = f
    parts["spigots-sweep"] = spigot_strip()
    parts["awg-pad"] = awg_pad()
    for hw in COVER_HEAD_W:
        parts[f"slot-cover-60-w{hw * 10:.0f}"] = slot_cover(hw)
    parts["stop-cap"] = stop_cap()
    COPIES = {"stop-cap": 2}                       # one per scope rail

    placed, x, total = [], 0.0, 0.0
    for name, p in parts.items():
        bb = p.val().BoundingBox()
        p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        vol = p.val().Volume() / 1000
        print(f"{name:20s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {vol:6.2f} cm3")
        check(path)
        for _ in range(COPIES.get(name, 1)):
            placed.append(p.val().moved(cq.Location(cq.Vector(x, 0, 0))))
            x += bb.xlen + 8.0; total += vol

    print(f"\nfoot spigot {fd:.1f} (sweep {SPIGOT_SWEEP}); slot cover leaves {CABLE_DEPTH:.1f} mm of cavity depth "
          f"for cable under a flush cover — the USB pigtail must be under that or the cover stands proud")

    # ---- plate: everything on one bed, spaced 8 mm ----
    plate = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(OUT, "p8-plate.stl")
    cq.exporters.export(plate, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate.val().BoundingBox()
    print(f"p8-plate {pb.xlen:.0f} x {pb.ylen:.0f} x {pb.zlen:.0f} mm, {total:.1f} cm3 "
          f"({'FITS' if pb.xlen < 250 and pb.ylen < 250 else 'TOO BIG'} the 256 bed)")
