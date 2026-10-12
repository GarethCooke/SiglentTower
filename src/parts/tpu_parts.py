# tpu_parts.py — every blue TPU part in the build, on ONE plate (PRINT-RULES rule 12: TPU prints once, last; ROADMAP
# Stage 8 / P8). Blue TPU 95A, flat as exported, no brim, no support. Output: parts/tpu/<part>-v1.stl, tpu-plate-v1.stl
# and the check sheet tpu-plate-plan.png (src/tpu_plan.py draws it).
#
# What is on the plate and why each one is the shape it is:
#
#   frame-foot x4      24 x 24 x 6 pad, Ø SPIGOT_D x 8 spigot with a 1 mm lead-in, into the centre bore at the bottom of
#                      each 510 upright (HANDOVER §8). Prints pad-down, spigot up — exactly as it sits on the bench.
#                      SPIGOT_D (fit.py 4.6) has never been measured, so the spigot sweep below rides on the same plate.
#   spigots-sweep      the P8 coupon as it was (src/coupons/p8_tpu.py): 4.2 / 4.6 / 5.0 / 5.4 stamped on a 3 mm strip.
#                      Push each into an upright's bottom bore: winner = in by thumb, holds the frame's weight, out with
#                      a twist. If it is not 4.6, the four feet reprint alone on the same spool (14 cm³).
#   awg-pad-left x2    20 x 20 x 5.5 plain block for the LEFT cradles' 20.4 x 20.4 x 1.5 pocket (src/parts/awg_cradle.py):
#                      1.5 in the pocket, 4 proud -> AWG body at z 251.5. NO lips: the pocket puts the whole pad UNDER the
#                      body (pad x 27.2–47.2, body edge 26.5), so a lip on the pad's edge would sit under the body and
#                      lift it — the P8 coupon's lipped pad was wrong. The left lateral stop is the cradle's own saddle
#                      lip at x 26 (0.5 off the body); the rearward stop is the bezel against the front arms. Nothing pulls
#                      the AWG forward. Bottom edges chamfered 0.4 (rule 7: the bottom enters the pocket).
#   awg-pad-right x2   the same block for the RIGHT brackets' pocket (pad x 213.3–233.3, body edge 233.5) plus a TAIL that
#                      lies on the arm top outboard of the pocket (x 233.3–238, z 247.5 up) carrying a 4 x 2 LIP beside the
#                      body's right edge (lip inner face 0.5 off the body nominal, 0.3–0.7 with the pad's 0.2 float in the
#                      pocket): the right side had no lateral stop at all (bracket plate 13.5 away). The tail hangs 1.5
#                      above the pad's bottom, so the pad prints STANDING ON ITS FRONT FACE (rule 3: nothing hangs below
#                      the bed face) — every pocket-fit face is then a wall, the pad's rear face is the print top. One
#                      part serves front and rear (symmetric in y).
#   slot-cover x6      240 long, press-in cover for the 5.9 slot mouth, holding the lighting and USB leads in the left
#                      PSU rail's inner slot and the rear base rail's slot (cable plan, ROADMAP §0). Profile: head
#                      COVER_HEAD_W (6.0) x SLOT_LIP_T (1.75) so it finishes flush with the rail face, then a 45° flare
#                      to COVER_FLARE_W (7.4) behind the lips — the step under each lip is 0.75. The P8 coupon's 8.4
#                      flare (1.25 per side) was a solid wedge that would not squash through a 5.9 mouth in 95A; 0.75 of
#                      45° ridge folds under a thumb and 240 mm of it holds. Printed head-UP as the coupon was: the bed
#                      face is the flare's 5.9 lead-in, the step faces up. Leaves SLOT_DEPTH - 2.5 = 3.65 under it for
#                      cable (3-core data runs fit; the USB pigtail must be under that or its cover stands proud).
#                      Cut to length on the bench with scissors; stop short of the hidden L-connectors at the rail ends.
#   cover-sweep        three 40 mm covers at flare 7.0 / 7.4 / 8.0, stamped (rules 10–11): press each into an offcut's
#                      slot — should go in by thumb along its length and not pull out by a fingernail. If 7.4 is wrong,
#                      the six strips reprint alone at the winner (28 cm³), same spool.
#   sled-stop-cap x2   8 mm of the cover profile. Pressed into the FRONT end of each scope rail's inner slot (the slot the
#                      T-foot runs in), against the front upright: the foot's front end meets the cap's head and flare
#                      instead of bare aluminium at the end of a pull. Self-retaining (the flare under the lips), trapped
#                      between upright and foot, no glue, travel 100 -> 92. No cap at the rear: home is the foot against
#                      the rear upright and a cap there would push the scope 8 mm proud of the front plane. Spares: cut
#                      from a cover strip.
#
# Proofs (python src/parts/tpu_parts.py): each pad in its cradle pocket 0 mm³ and against the AWG body 0 mm³; pad shifted
# 0.5 in the pocket collides (located); body shifted 1.0 right collides with the right pads' lips, 0.3 clear; cover in the
# slot: only the head's 0.05-per-side interference, lifted 0.5 out of the slot the step hits the lips (held); every part
# passes printcheck with no down-facing area above the bed; the plate is 240 x 150, inside the 250 rule, flat.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from fit import (SPIGOT_D, SLOT_MOUTH, SLOT_LIP_T, SLOT_CAVITY_W, SLOT_THROAT_D, SLOT_DEPTH, SLOT_BOTTOM_W)
import parts.awg_cradle as ac

# ---- frame foot ----
FOOT_W, FOOT_H = 24.0, 6.0
SPIGOT_H, SPIGOT_LEAD = 8.0, 1.0
SPIGOT_SWEEP = (4.2, 4.6, 5.0, 5.4)
FOOT_SPIGOT_D = 4.6           # fit.py still carries the spec's 5.0 with "expect ~4.6" (a 2020 centre bore is ~Ø4.2 nominal); the
                              # feet print at 4.6 and the sweep on the same plate decides. SPIGOT_D in fit.py changes when P8 passes.

# ---- AWG pads (awg_cradle.py: PAD 20, PAD_CLR 0.2, POCKET_D 1.5, body at Z_RAIL_TOP + 4) ----
PAD, PAD_H, POCKET_D = ac.PAD, 5.5, ac.POCKET_D
LIP_CLR = 0.5                 # right lip inner face to the body's edge, pad centred in its pocket
LIP_W, LIP_H = 4.0, 2.0       # lip beside the body: 4 wide, 2 above the body's bottom
TAIL_LIFT = 0.3               # tail underside above the arm top: the lip hangs off the pad, it does not rest on the arm
TAIL_X1 = PAD + ac.PAD_CLR + LIP_CLR + LIP_W    # 24.7: tail/lip outboard edge (pad local x; body edge at PAD + PAD_CLR)

# ---- slot cover ----
COVER_HEAD_W = SLOT_MOUTH + 0.1          # 6.0 in the 5.9 mouth
COVER_FLARE_W = 7.4                      # 0.75 step under each lip; coupon's 8.4 withdrawn (see header)
COVER_SWEEP = (7.0, 7.4, 8.0)
COVER_L, SWEEP_L, CAP_L = 240.0, 40.0, 8.0
def flare_h(w): return (w - SLOT_MOUTH) / 2                      # 45°: rises as fast as it widens
CABLE_DEPTH = SLOT_DEPTH - SLOT_LIP_T - flare_h(COVER_FLARE_W)   # 3.65

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def stamp(part, x, y, text, size=4.0, depth=0.5, z=None):
    zt = part.val().BoundingBox().zmax if z is None else z
    return part.cut(cq.Workplane("XY").workplane(offset=zt - depth).center(x, y)
                    .text(text, size, depth + 1, combine=False, halign="center", valign="center"))

def spigot(d, h=SPIGOT_H, z0=0.0):
    body = cq.Workplane("XY").workplane(offset=z0).circle(d / 2).extrude(h - SPIGOT_LEAD)
    tip = cq.Workplane("XY").add(cq.Solid.makeCone(d / 2, d / 2 - SPIGOT_LEAD, SPIGOT_LEAD,
                                                   pnt=cq.Vector(0, 0, z0 + h - SPIGOT_LEAD), dir=cq.Vector(0, 0, 1)))
    return body.union(tip)

def frame_foot(d=FOOT_SPIGOT_D):
    pad = cq.Workplane("XY").box(FOOT_W, FOOT_W, FOOT_H, centered=(True, True, False)).edges("|Z").fillet(2.0)
    return pad.union(spigot(d, z0=FOOT_H - 0.01))

def spigot_sweep():
    t, pitch, margin = 3.0, 18.0, 9.0
    w = (len(SPIGOT_SWEEP) - 1) * pitch + 2 * margin
    s = cq.Workplane("XY").box(w, 26.0, t, centered=(True, True, False))
    for i, d in enumerate(SPIGOT_SWEEP):
        x = (i - (len(SPIGOT_SWEEP) - 1) / 2) * pitch
        s = s.union(spigot(d, z0=t - 0.01).translate((x, 5.0, 0)))
        s = stamp(s, x, -7.5, f"{d:.1f}", size=5.0, z=t)
    return s

def awg_pad(lip=False, fillet=0.8):
    """Pad in FRAME-like local coords: x 0..20 (+x = outboard on the right side), y 0..20, z 0 = pocket floor (frame 246).
    lip=True adds the right side's tail (z 1.8 up: 0.3 above the arm top, so it never bottoms before the pad does) and
    the lip beside the body (z 5.5–7.5). The right pad takes no corner fillets (its bed-edge chamfer is cut on the plain box)."""
    p = box(0, PAD, 0, PAD, 0, PAD_H)
    if fillet: p = p.edges("|Z").fillet(fillet)
    if lip:
        tail = box(PAD - 0.01, TAIL_X1, 0, PAD, POCKET_D + TAIL_LIFT, PAD_H)
        lipb = box(PAD + ac.PAD_CLR + LIP_CLR, TAIL_X1, 0, PAD, PAD_H - 0.01, PAD_H + LIP_H)
        p = p.union(tail).union(lipb)
    return p

def awg_pad_left_print():
    """Pad-down: the bed is the pocket face; its edges chamfered 0.4 (rule 7)."""
    return awg_pad(False).edges("<Z").chamfer(0.4)

def awg_pad_right_print():
    """Standing on its front face (local y = 0 -> bed): the tail's underside becomes a wall. The pad's own bed edges
    (the pocket-fit faces) are chamfered 0.4 on the bare box before the tail and lip go on."""
    pad = box(0, PAD, 0, PAD, 0, PAD_H).edges("<Y").chamfer(0.4)
    tail = box(PAD - 0.01, TAIL_X1, 0, PAD, POCKET_D + TAIL_LIFT, PAD_H)
    lipb = box(PAD + ac.PAD_CLR + LIP_CLR, TAIL_X1, 0, PAD, PAD_H - 0.01, PAD_H + LIP_H)
    p = pad.union(tail).union(lipb).rotate((0, 0, 0), (1, 0, 0), 90)
    bb = p.val().BoundingBox(); return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def slot_cover(length=COVER_L, flare_w=COVER_FLARE_W, head_w=COVER_HEAD_W, label=None):
    """Printed HEAD UP: bed = the flare's lead-in face (SLOT_MOUTH wide), 45° out to flare_w, step in to head_w (the
    retaining face, up = under the lip in use), head_w for SLOT_LIP_T so the cover finishes flush with the rail face."""
    fh = flare_h(flare_w); base_w = flare_w - 2 * fh
    pts = [(-base_w / 2, 0.0), (base_w / 2, 0.0), (flare_w / 2, fh), (head_w / 2, fh),
           (head_w / 2, fh + SLOT_LIP_T), (-head_w / 2, fh + SLOT_LIP_T), (-head_w / 2, fh), (-flare_w / 2, fh)]
    c = cq.Workplane("YZ").polyline(pts).close().extrude(length)             # profile in (y, z), length along x
    return stamp(c, length / 2, 0, label, size=3.5, depth=0.4) if label else c

def stop_cap(): return slot_cover(CAP_L)

# ---- the 2020 slot as a solid, for the cover proof: u = depth into the rail (0 at the face), v across, w along ----
def slot_void(length):
    hw_m, hw_c, hw_b = SLOT_MOUTH / 2, SLOT_CAVITY_W / 2, SLOT_BOTTOM_W / 2
    pts = [(-hw_m, -1), (hw_m, -1), (hw_m, SLOT_LIP_T), (hw_c, SLOT_LIP_T), (hw_c, SLOT_THROAT_D),
           (hw_b, SLOT_DEPTH), (-hw_b, SLOT_DEPTH), (-hw_c, SLOT_THROAT_D), (-hw_c, SLOT_LIP_T), (-hw_m, SLOT_LIP_T)]
    return cq.Workplane("YZ").polyline([(v, u) for v, u in pts]).close().extrude(length)   # y = v, z = u, x = w

def rail_material(length):
    return box(0, length, -10, 10, 0, 20).cut(slot_void(length))

def cover_in_slot(flare_w=COVER_FLARE_W, length=20.0):
    """The cover as it sits in use: head top at u = 0 (flush), head u 0..1.75, flare below. Print frame has the head up
    at z = fh..fh+1.75, so flip z and shift."""
    c = slot_cover(length, flare_w).rotate((0, 0, 0), (1, 0, 0), 180)      # z -> -z: the head (was on top) is now lowest
    bb = c.val().BoundingBox()
    return c.translate((-bb.xmin, 0, -bb.zmin))                             # head top at z (= u) 0, flare bottom at 2.5

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "tpu")); os.makedirs(OUT, exist_ok=True)

    # ---------------- proofs ----------------
    body = box(ac.BODY_L, ac.BODY_R, 3, 263, ac.Z_RAIL_TOP + 4, ac.Z_RAIL_TOP + 86)
    yc = (ac.SADDLE_L - PAD - 2 * ac.PAD_CLR) / 2 + ac.PAD_CLR                   # pad's y inside a cradle, centred in the pocket
    # left pad in the left front cradle (saddle at y 20); pad local x 0 at frame BODY_L + 0.5 + PAD_CLR
    lc = ac.left_cradle().translate((0, 20, 0))
    lp = awg_pad(False).translate((ac.BODY_L + 0.5 + ac.PAD_CLR, 20 + yc, ac.Z_RAIL_TOP - POCKET_D))
    print(f"left pad in its pocket: {vol(lp, lc):.4f} cm3 (0); vs AWG body {vol(lp, body):.4f} (0); "
          f"pad shifted 0.5 x: {vol(lp.translate((0.5, 0, 0)), lc):.4f} (>0, located); 0.5 y: {vol(lp.translate((0, 0.5, 0)), lc):.4f} (>0)")
    # right pad in the right front bracket (at y 23); pad local x 0 at frame BODY_R - UNDER - PAD_CLR, +x outboard
    rb = ac.right_bracket().translate((0, 23, 0))
    rp = awg_pad(True, fillet=0).translate((ac.BODY_R - ac.UNDER - ac.PAD_CLR, 23 + yc, ac.Z_RAIL_TOP - POCKET_D))
    rpb = rp.val().BoundingBox()
    print(f"right pad in its pocket: {vol(rp, rb):.4f} cm3 (0); vs AWG body {vol(rp, body):.4f} (0); lip x {rpb.xmax - LIP_W:.2f}–{rpb.xmax:.2f}, "
          f"z to {rpb.zmax:.1f}; body edge {ac.BODY_R}: clearance {rpb.xmax - LIP_W - ac.BODY_R:.2f}")
    print(f"   body shifted right 1.0: {vol(rp, body.translate((1.0, 0, 0))):.4f} (>0, lip catches); 0.3: {vol(rp, body.translate((0.3, 0, 0))):.4f} (0); "
          f"pad shifted 0.5 x: {vol(rp.translate((-0.5, 0, 0)), rb):.4f} (>0, located)")
    # right pad vs the mini-slot body envelope (x 242–268, z 248 up) and the bracket plate (x 247–251)
    mini = box(242, 268, 3, 288, 248, 336)
    print(f"   right pad vs mini-slot envelope: {vol(rp, mini):.4f} (0)")
    # cover in the slot
    for w in COVER_SWEEP:
        c = cover_in_slot(w)
        m = rail_material(20.0)
        print(f"cover flare {w}: in the slot {vol(c, m):.4f} cm3 (head interference only, {2 * 0.05 * SLOT_LIP_T * 20 / 1000:.4f} expected); "
              f"lifted 0.5 out: {vol(c.translate((0, 0, -0.5)), m):.4f} (>0, the step under the lips holds it); "
              f"cable depth under it {SLOT_DEPTH - SLOT_LIP_T - flare_h(w):.2f}")

    # ---------------- parts ----------------
    parts = {"frame-foot-v1": frame_foot(), "spigots-sweep-v1": spigot_sweep(),
             "awg-pad-left-v1": awg_pad_left_print(), "awg-pad-right-v1": awg_pad_right_print(),
             "slot-cover-240-v1": slot_cover(), "sled-stop-cap-v1": stop_cap()}
    for w in COVER_SWEEP: parts[f"cover-sweep-{w:.1f}-v1"] = slot_cover(SWEEP_L, w, label=f"{w:.1f}")
    # plate positions (x, y) of each copy's bounding-box corner; everything flat, 240 x 150
    layout = {"slot-cover-240-v1": [(0, 11.4 * i) for i in range(6)],
              "spigots-sweep-v1": [(0, 76)],
              "cover-sweep-7.0-v1": [(85, 76)], "cover-sweep-7.4-v1": [(135, 76)], "cover-sweep-8.0-v1": [(185, 76)],
              "sled-stop-cap-v1": [(85, 92), (100, 92)],
              "frame-foot-v1": [(0, 112), (34, 112), (68, 112), (102, 112)],
              "awg-pad-left-v1": [(140, 112), (170, 112)],
              "awg-pad-right-v1": [(205, 110), (205, 125)]}
    placed, total, dims = [], 0.0, {}
    for name, p in parts.items():
        bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        v = p.val().Volume() / 1000; dims[name] = (bb.xlen, bb.ylen, bb.zlen, v)
        print(f"{name:22s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {v:6.2f} cm3  x{len(layout[name])}")
        check(path)
        for (x, y) in layout[name]:
            placed.append(p.val().moved(cq.Location(cq.Vector(x, y, 0)))); total += v
    plate = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(OUT, "tpu-plate-v1.stl")
    cq.exporters.export(plate, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate.val().BoundingBox()
    print(f"\ntpu-plate-v1 {pb.xlen:.0f} x {pb.ylen:.0f} x {pb.zlen:.1f} mm, {total:.1f} cm3, {len(placed)} parts "
          f"({'FITS' if pb.xlen <= 250 and pb.ylen <= 250 else 'TOO BIG'} — 250 rule); feet at Ø{FOOT_SPIGOT_D}, covers at flare "
          f"{COVER_FLARE_W} ({CABLE_DEPTH:.2f} under them for cable), {6 * COVER_L / 1000:.2f} m of cover")
    import json; json.dump({"layout": layout, "dims": dims}, open(os.path.join(OUT, "tpu-plate-layout.json"), "w"))
