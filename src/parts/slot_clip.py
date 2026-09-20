# Slot clip for the side tiles (HANDOVER §5, PRINT-RULES §2, ROADMAP P4). Tiles are 3 mm PETG lying on the rails' outer
# faces; adjacent tiles meet on each rail's slot centreline and both clip into that one slot, the upper tile hooking the
# upper lip and the lower tile the lower lip, their clips staggered along the rail.
#
# Why not a plain barb: the lip is 1.75 thick, so a peg that flexes on its own has ~2 mm of leg — a 0.6 barb would strain
# it past yield. So the SPRING is a finger cut free from the tile by a 1 mm U-slit, lying in the tile plane along the
# edge: FINGER_L long, FINGER_W wide, tile thickness thick, cantilevered from one end. It bends sideways in the tile plane
# (the slot's width direction). At its free end a peg rises from the tile's back into the slot: PEG_W wide (mouth minus
# 2 x PEG_CLR), PEG_L long; on the lip side it carries a barb that reaches BARB past the mouth edge and hooks under the
# lip with a 60° face (45° ramp on the way in). Pushing the tile on deflects the finger by BARB, it springs back behind
# the lip; a blade against the finger's free end releases it. ~11 N per finger over the 24 free mm, ~0.9 % strain.
# v2 (2026-09-20): a rigid STUB_L x (mouth - 2 x STUB_CLR) stub on the finger's root fills the mouth and locates the tile
# along the slot width; the peg + barb only hold it against the rail. v1 had no lateral location and rattled.
#
# Tile coordinates: x = thickness (face at -T, back at 0, +x into the slot), y along the rail, z across the rail with
# z = 0 the SLOT CENTRELINE = the tile's nominal edge (tile body at z >= 0). The finger straddles the edge: z -2.25 ..
# 3.25, so the peg body sits 0.7 off the far mouth edge and 0.1 off the near one. The barb points +z (toward the tile body's own side = the lip on
# this tile's side of the slot). The neighbouring tile carries a notch where this finger dips below z 0.
# Print: face down (x -> up). Fingers and pegs rise from the tile; the barb's underside is 60°, its ramp 45°.
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import SLOT_MOUTH, SLOT_LIP_T, SLOT_THROAT_D, SLOT_DEPTH, SLOT_CAVITY_W, SLOT_BOTTOM_W, CLIP_T, CLIP_BARB, CLIP_HOOK_DEG, CLIP_STUB_CLR

T         = CLIP_T            # tile / finger thickness 3.0
FINGER_L  = 30.0              # finger length along the rail: STUB_L rigid root + 24 free cantilever
FINGER_W  = 5.5               # finger width across the rail (z)
SLIT      = 1.0               # U-slit around the finger
PEG_CLR   = 0.7               # peg body to the FAR mouth edge (must exceed CLIP_BARB: the peg shifts this way to clear the lip)
PEG_NEAR  = 0.1               # peg body to the mouth edge on the barb side — the barb starts at the mouth edge, not at a
                              # centred body, so its face is only BARB + 0.1 tall and the peg stays short of the throat
PEG_W     = SLOT_MOUTH - PEG_CLR - PEG_NEAR   # 5.1
PEG_L     = 6.0               # along the rail
HOOK_GAP  = 0.0               # barb's hook face sits on the lip underside: no lift (v1 had 0.2 and rattled)
STUB_L    = 6.0               # rigid locating stub at the finger's ROOT: fills the mouth so the tile cannot move along the
STUB_CLR  = CLIP_STUB_CLR     # slot width (v1 had nothing locating the tile sideways — the pegs rattled in 0.8 of slack)
STUB_H    = 3.0
HOOK_DEG  = CLIP_HOOK_DEG     # hook face from the tile plane. P4 v2 winner C: 45° with a 1.2 barb (pull-off = push, held by the barb's reach)
RAMP_DEG  = 45.0
assert PEG_CLR > CLIP_BARB, "peg would jam on the far mouth edge before the barb clears the lip"

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def peg_profile(barb=CLIP_BARB, hook_deg=None):
    """(x, z) polygon of the peg + barb section; x from the tile back, barb toward +z."""
    zb0, zb1 = -SLOT_MOUTH / 2 + PEG_CLR, SLOT_MOUTH / 2 - PEG_NEAR      # -2.25 .. 2.85
    z_hook = SLOT_MOUTH / 2 + barb
    x_hook = SLOT_LIP_T + HOOK_GAP
    hook_deg = HOOK_DEG if hook_deg is None else hook_deg
    x_tip = x_hook + (z_hook - zb1) * math.tan(math.radians(hook_deg))    # from the tile plane: steeper = hooks harder, taller peg
    x_top = x_tip + (z_hook - zb1) * math.tan(math.radians(RAMP_DEG))     # 45° ramp back to the body
    assert x_top < SLOT_DEPTH - 0.8, "peg too tall for the slot"
    if x_top > SLOT_THROAT_D:   # into the tapered part of the cavity: check the barb still fits the width there
        w = SLOT_CAVITY_W - (SLOT_CAVITY_W - SLOT_BOTTOM_W) * (x_top - SLOT_THROAT_D) / (SLOT_DEPTH - SLOT_THROAT_D)
        assert z_hook - zb0 < w - 0.6, "barb hits the cavity taper"
    return [(0, zb0), (0, zb1), (x_hook, zb1), (x_tip, z_hook), (x_top, zb1), (x_top, zb0)]

def peg(barb=CLIP_BARB, hook_deg=None):
    """Peg solid over y 0..PEG_L (XZ profile extruded along y)."""
    return cq.Workplane("XZ").polyline(peg_profile(barb, hook_deg)).close().extrude(PEG_L).translate((0, PEG_L, 0))

def finger_span(y_root, direction):
    """(y_lo, y_hi) of the finger from its root, running +y (direction 1) or -y (-1)."""
    return (y_root, y_root + FINGER_L) if direction > 0 else (y_root - FINGER_L, y_root)

def add_finger(tile, y_root, direction, barb=CLIP_BARB, stub_clr=STUB_CLR, hook_deg=None, finger_w=None):
    """Cut the U-slit that frees a finger from `tile` (whose edge is z = 0), add its overhang below the edge and its peg.
    Root at y_root, finger running in `direction`; peg at the free end."""
    fw = FINGER_W if finger_w is None else finger_w
    zf0, zf1 = -SLOT_MOUTH / 2 + PEG_CLR, fw - SLOT_MOUTH / 2 + PEG_CLR   # finger straddles the edge under the peg
    y_lo, y_hi = finger_span(y_root, direction)
    y_free = y_hi if direction > 0 else y_lo
    # slit along the finger's inner edge, from the root to 1 past the free end
    if direction > 0: top = box(-T - 1, 1, y_lo, y_hi + SLIT, zf1, zf1 + SLIT)
    else:             top = box(-T - 1, 1, y_lo - SLIT, y_hi, zf1, zf1 + SLIT)
    # slit across the free end
    if direction > 0: end = box(-T - 1, 1, y_hi, y_hi + SLIT, zf0 - 1, zf1 + SLIT)
    else:             end = box(-T - 1, 1, y_lo - SLIT, y_lo, zf0 - 1, zf1 + SLIT)
    tile = tile.cut(top).cut(end)
    tile = tile.union(box(-T, 0, y_lo, y_hi, zf0, 0))                        # finger strip below the tile edge
    y_peg = (y_hi - PEG_L) if direction > 0 else y_lo
    tile = tile.union(peg(barb, hook_deg).translate((0, y_peg, 0)))
    sw = SLOT_MOUTH - 2 * stub_clr                                            # rigid stub at the root, centred in the mouth
    y_stub = y_lo if direction > 0 else y_hi - STUB_L
    return tile.union(box(0, STUB_H, y_stub, y_stub + STUB_L, -sw / 2, sw / 2))
