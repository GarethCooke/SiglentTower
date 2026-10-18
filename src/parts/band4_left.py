# band4_left.py — the LEFT side's band 4 (ROADMAP Stage 7; the last two side tiles). v1 2026-10-18.
#
# Frame coordinates for the left side = skin_check's rail frame: x 0 is the rails' and uprights' outer face, +x into
# the frame, tiles at x -3..0 (face at -3), y = frame y, z = frame z. Two tiles, y 20–175 (front) and 175–330 (rear),
# z 335–500 (165 tall: 1 under the top rail's slot centreline... the fingers set the top; the bottom lands 2–3 above the
# scope rail's top whether the scope->top gap reads 157 or 159). Each tile: three P4 fingers up into the top rail's
# outer slot (no partner in that slot), the side-tile hex pattern, and — the sled band below it has no rail to clip to —
# a LEG as the right fixed tile's (door_set.py): a 19 x 3 x 40 wall rising from the tile's back at its upright end, flat
# on that upright's face (front-left upright's REAR face y 20 / rear-left upright's FRONT face y 330), one M5 x 10 +
# drop-in T-nut into the face's slot (x 10) at z 361, adjustable in z. The two tiles meet at y 175 on a plain edge.
#
# Clear of (checked below): the scope and top rails, both uprights, the band-3 tiles with their top fingers, the left sled
# beam (x 20.5–46, z 337–346 — the leg stops at x 19), the cast brackets under the scope rail's ends (z 291–311), the LED
# strip on the rear-left upright's inner face (x 20, y 330–350) and the probe hanger's face (the upright's OUTER face).
#
# Print: face down, legs and fingers rise, the leg's M5 hole a teardrop (apex up = the tile's back). One tile per plate
# (155 + 155 does not fit the bed). Black PETG, no brim, no support, ~45 cm3 each.
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, HERE)
import side_tile as st, slot_clip as sc, door_hinge as dh
from door_set import teardrop_y, vol

T = st.T
Z0, H = 335.0, 165.0
TILE_L = st.TILE_L                                   # 155
ROOTS = st.BASE_ROOTS                                # 10 / 62 / 114: three fingers, no partner in the top slot
LEG_X1, LEG_T, LEG_Z0, LEG_Z1, LEG_BOLT_Z, SLOT_X = 19.0, 3.0, 341.0, 381.0, 361.0, 10.0
box = sc.box

def tile_with_leg(leg_at_end):
    """side_tile local frame (face x -3..0, y 0..155, z 0..165). leg_at_end: 'lo' = the leg at local y 0..3, 'hi' = at 152..155."""
    y0 = 0.0 if leg_at_end == "lo" else TILE_L - LEG_T
    keep = [(y0 - 1.0, y0 + LEG_T + 1.0, LEG_Z0 - Z0 - 2.0, LEG_Z1 - Z0 + 2.0)]
    t = st.tile(TILE_L, H, roots_lo=(), roots_hi=ROOTS, keep=keep)
    leg = box(0, LEG_X1, y0, y0 + LEG_T, LEG_Z0 - Z0, LEG_Z1 - Z0)
    leg = leg.cut(teardrop_y(dh.BOLT_D, SLOT_X, LEG_BOLT_Z - Z0, y0 - 1, y0 + LEG_T + 1))
    return t.union(leg)

def front(): return tile_with_leg("lo").translate((0, 20.0, Z0))      # leg on the front upright's rear face, y 20–23
def rear():  return tile_with_leg("hi").translate((0, 175.0, Z0))     # leg on the rear upright's front face, y 327–330

def surroundings():
    from skin_check import rail_with_outer_slot
    g = st.GAPS["L"]
    scope_z0 = 20.0 + g[1] + 20.0 + g[2] + 20.0 + g[3]                 # 311.7 as measured on the left
    S = dict(scope=rail_with_outer_slot(20, 330, scope_z0, scope_z0 + 20), top=rail_with_outer_slot(20, 330, 490.0, 510.0),
             uprights=box(0, 20, 0, 20, 0, 510).union(box(0, 20, 330, 350, 0, 510)),
             band3=box(-T, 0, 20, 330, 237.5, scope_z0 + 10 + 3.25),
             beam=box(20.5, 46, 3, 330, 337, 346), channel=box(20, 46, 201, 334, 346, 366),
             brackets=box(3, 17, 20, 40, scope_z0 - 20, scope_z0).union(box(3, 17, 310, 330, scope_z0 - 20, scope_z0)),
             strip=box(20, 23, 335, 345, 20, 490), box_home=box(50, 341, 195, 330, 346, 456))
    return S

def printable(t):
    p = t.rotate((0, 0, 0), (0, 1, 0), -90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "tiles")); os.makedirs(OUT, exist_ok=True)
    F, R, S = front(), rear(), surroundings()
    print("--- proofs (cm3; 0 = clear) ---")
    for name, t in (("band4-LF", F), ("band4-LR", R)):
        print(f"{name}: " + "  ".join(f"{k} {vol(t, s):.4f}" for k, s in S.items()))
        print(f"   lifted 0.5 vs top rail {vol(t.translate((0, 0, 0.5)), S['top']):.4f} (>0: fingers in the slot); pulled 0.5 off the face {vol(t.translate((-0.5, 0, 0)), S['top']):.4f} (>0: barbs hold); "
              f"leg pushed 0.5 into its upright {vol(t.translate((0, -0.5 if name.endswith('LF') else 0.5, 0)), S['uprights']):.4f} (>0: flat on the face); "
              f"bottom edge {Z0} vs scope rail top {S['scope'].val().BoundingBox().zmax:.1f}")
    print(f"front vs rear tile {vol(F, R):.4f} (0: they meet at y 175)")
    for name, t in (("tile-band4-LF-v1", F), ("tile-band4-LR-v1", R)):
        p = printable(t); path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        bb = p.val().BoundingBox(); print(f"{name:18s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3  — black PETG, face down as exported, one per plate")
        check(path, min_rest_frac=0.25, max_down_frac=0.25)
