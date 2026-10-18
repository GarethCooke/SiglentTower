# door_set.py — the right side's band 4 (ROADMAP Stage 7, HANDOVER §5, D11): the fold-down DOOR, the FIXED REAR TILE,
# and the two frame-side MAGNET holders. v1 2026-10-18.
#
# Everything here is built in the RAIL FRAME that skin_check.py uses for the right side: x = 0 is the rails' and
# uprights' OUTER face (frame x 361), +x goes INTO the frame (frame x = 361 - x), y = frame y, z = frame z. The tiles lie
# at x -3..0 (face at -3). The hinge leaves come from door_hinge.py (frame coordinates) mirrored into this frame.
#
# Band 4 on the right (z 347 -> 499, y 20 -> 330) is split at y 250: the door (230 long) and the fixed tile (80).
#   DOOR  x -3..0, y 20–250, z 347–499 (152 tall: bottom edge = the hinge's shelf at rail top + 16, top edge 1 under the
#         top rail's slot centreline; it is not clipped — it swings — so its height only has to clear). Hex pattern as the
#         side tiles. On its BACK: two 12 x 12 x 3 MAGNET BOSSES with Ø10.4 x 2.2 pockets at (y 34, z 479) and (y 236,
#         z 479), printed with the door; solid glue pads where the two door hinge leaves go (y 23–47 / 223–247,
#         z 347–371); a 45 x 12 FINGER SLOT through it at (y 135, z 482) — a fingertip hooks the door's edge through it
#         (HANDOVER's notch in the top border would open onto the rail face and give nothing to hold).
#   FIXED TILE  x -3..0, y 250–330, z 334–500 (166 tall; 3 clear of the scope rail's top), two clip fingers in the TOP
#         rail's outer slot (P4) and, because the sled band below it has no rail to clip to, a LEG: a 19 x 3 x 40 wall
#         rising from its back at the rear edge, lying on the rear-right upright's FRONT face (y 330), ONE M5 x 10 + T-nut
#         into that face's slot (x 10 = frame 351) at z 361 — adjustable in z, so the reading of the top rail's height
#         does not matter. A solid window on its back at y 250–262, z 467–488 where the rear magnet tab is glued.
#   FRONT MAGNET BRACKET  (black ABS) an L: plate x 0–20 x y 20–26 x z 455–488 on the front-right upright's REAR face,
#         one M5 x 10 + T-nut into that face's slot (x 10) at z 461, counterbored; a 5.5 x 5 tongue up into the top rail's
#         BOTTOM slot (anti-rotation); a leg x 3.5–9.5 x y 26–49 x z 467–488 reaching rearward behind the door's front
#         boss, its Ø10.4 x 2.2 pocket facing the boss, faces 0.5 apart. Pull-apart is in the door's opening direction.
#   REAR MAGNET TAB  (black ABS) glued to the fixed tile's back: block x 0–6.5 x y 250–262 x z 467–488 (the glue face is
#         x 0, on the tile) carrying a plate x 3.5–6.5 x y 228–250 that reaches forward behind the door's rear boss with
#         the same pocket. (HANDOVER grew this tab from the tile; printed face-down that is a 22 mm floating plate, so
#         it is a separate part lying on its back face, pocket upward.)
#   HINGE  as door_hinge.py v1: frame leaves on the scope rail's outer face at y 23–47 / 223–247 (printed, the second
#         pair on the list), door leaves glued to the door's back; axis frame x 369 / z 341.
#
# Print: door and fixed tile FACE DOWN (textured plate on the visible face), bosses, leg and fingers rise — the leg's
# M5 hole is a teardrop (axis along y = horizontal in the print, apex toward the tile's back = up). Bracket on its plate
# face, leg and tongue rising, magnet pocket a teardrop (apex +y = up). Tab on its back face, pocket upward. No support.
# Magnets: 4 x Ø10 x 2 (two pairs), CA'd in, polarity marked before gluing — door boss N out, holder N out = repel; flip one.
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, HERE)
import side_tile as st, slot_clip as sc, door_hinge as dh
from fit import MAG_POCKET_D, MAG_POCKET_H

T = st.T
# band 4 right
DOOR_Y0, DOOR_Y1, DOOR_Z0, DOOR_H = 20.0, 250.0, dh.TILE_Z0, 152.0        # 347 -> 499
FIX_Y0, FIX_Y1, FIX_Z0, FIX_H = 250.0, 330.0, 334.0, 166.0               # 334 -> 500 (3 clear of the rail top; 2 if the top rail reads 488.7)
# magnets
MAG_Y = (34.0, 236.0); MAG_Z = 479.0; BOSS = 12.0; BOSS_H = 3.0; MAG_GAP = 0.5
# finger slot
SLOT_W, SLOT_H, SLOT_Y, SLOT_Z = 45.0, 12.0, 135.0, 482.0
# hinge leaf glue pads (door back), y spans = the knuckles
PADS_Y = st.HINGES; PAD_Z1 = dh.PAD_Z1                                   # 371
# fixed tile's leg and its bolt
LEG_X1, LEG_T, LEG_Z0, LEG_Z1, LEG_BOLT_Z = 19.0, 3.0, 341.0, 381.0, 361.0
SLOT_X = 10.0                                                            # the uprights' slot centreline in this frame (frame 351)
# front bracket
BR_PLATE = (0.0, 20.0, 20.0, 26.0, 455.0, 488.0); BR_BOLT_Z = 461.0; BR_CB_D, BR_CB_H = 10.0, 2.5
BR_TONGUE = (SLOT_X - 2.75, SLOT_X + 2.75, 20.0, 26.0, 488.0, 493.0)
BR_LEG = (BOSS_H + MAG_GAP, BOSS_H + MAG_GAP + 6.0, 26.0, 49.0, 467.0, 488.0)   # tops at 488: 2 under the top rail (0.7 if it reads 488.7)
# rear tab
TAB_BLOCK = (0.0, BOSS_H + MAG_GAP + 3.0, 250.0, 262.0, 467.0, 488.0)
TAB_PLATE = (BOSS_H + MAG_GAP, BOSS_H + MAG_GAP + 3.0, 228.0, 250.0, 467.0, 488.0)

box = sc.box

def teardrop_y(d, xc, zc, y0, y1):
    """Hole along y with a 45° apex toward +x (the tile's back = up in a face-down print)."""
    r = d / 2; k = r / math.sqrt(2)
    circ = cq.Workplane("XZ").center(xc, zc).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
    peak = cq.Workplane("XZ").polyline([(xc + k, zc + k), (xc + r * math.sqrt(2), zc), (xc + k, zc - k)]).close().extrude(-(y1 - y0)).translate((0, y0, 0))
    return circ.union(peak)

def pocket_x(yc, zc, x_face, depth, into=+1):
    """Round magnet pocket Ø MAG_POCKET_D, `depth` deep from the face at x_face, cut in the +x (into=+1) or -x direction."""
    x0 = x_face if into > 0 else x_face - depth
    return cq.Workplane("YZ").workplane(offset=x0 - (0.01 if into > 0 else 0)).center(yc, zc).circle(MAG_POCKET_D / 2).extrude(depth + 0.01)

# ------------------------------------------------------------------ door
def door_local():
    """Door in side_tile's local frame: face x -3..0, y 0..230, z 0..152 (z 0 = the bottom edge)."""
    L, H = DOOR_Y1 - DOOR_Y0, DOOR_H
    yb = [y - DOOR_Y0 for y in MAG_Y]; zb = MAG_Z - DOOR_Z0
    keep = [(y0 - DOOR_Y0, y1 - DOOR_Y0, 0.0, PAD_Z1 - DOOR_Z0) for (y0, y1) in PADS_Y]          # hinge glue pads
    keep += [(y - BOSS / 2, y + BOSS / 2, zb - BOSS / 2, zb + BOSS / 2) for y in yb]                # magnet bosses
    keep += [(SLOT_Y - DOOR_Y0 - SLOT_W / 2, SLOT_Y - DOOR_Y0 + SLOT_W / 2, SLOT_Z - DOOR_Z0 - SLOT_H / 2, SLOT_Z - DOOR_Z0 + SLOT_H / 2)]
    d = st.tile(L, H, roots_lo=(), roots_hi=(), open_hi=True, keep=keep)
    for y in yb:
        d = d.union(box(0, BOSS_H, y - BOSS / 2, y + BOSS / 2, zb - BOSS / 2, zb + BOSS / 2))
        d = d.cut(pocket_x(y, zb, BOSS_H, MAG_POCKET_H, into=-1))
    slot = (cq.Workplane("YZ").workplane(offset=-T - 1).center(SLOT_Y - DOOR_Y0, SLOT_Z - DOOR_Z0)
            .slot2D(SLOT_W, SLOT_H, 0).extrude(T + BOSS_H + 2))
    return d.cut(slot)

def door():
    """Door in the rail frame (closed)."""
    return door_local().translate((0, DOOR_Y0, DOOR_Z0))

# ------------------------------------------------------------------ fixed rear tile
def fixed_local():
    """side_tile's local frame for a RIGHT tile: local y 0 is the REAR end (frame y 330), +y runs forward. Fingers on the
    top edge at local 6 and 44 (30 long, slit to 75, border to 80). Leg at the rear edge, tab window at the front."""
    L, H = FIX_Y1 - FIX_Y0, FIX_H
    keep = [(-1.0, 4.0, LEG_Z0 - FIX_Z0 - 2, LEG_Z1 - FIX_Z0 + 2),                                  # leg root
            (FIX_Y1 - TAB_BLOCK[3], FIX_Y1 - TAB_BLOCK[2] + 1, TAB_BLOCK[4] - FIX_Z0, TAB_BLOCK[5] - FIX_Z0)]   # glue face of the tab
    t = st.tile(L, H, roots_lo=(), roots_hi=(6.0, 44.0), keep=keep)
    leg = box(0, LEG_X1, 0, LEG_T, LEG_Z0 - FIX_Z0, LEG_Z1 - FIX_Z0)
    leg = leg.cut(teardrop_y(dh.BOLT_D, SLOT_X, LEG_BOLT_Z - FIX_Z0, -1, LEG_T + 1))
    return t.union(leg)

def fixed():
    """Fixed tile in the rail frame: mirror y (right-tile convention) then rear end at frame y 330, bottom at 333."""
    return fixed_local().mirror("XZ").translate((0, FIX_Y1, FIX_Z0))

# ------------------------------------------------------------------ magnet holders
def bracket_front():
    b = box(*BR_PLATE).union(box(*BR_TONGUE)).union(box(*BR_LEG))
    b = b.cut(cq.Workplane("XZ").center(SLOT_X, BR_BOLT_Z).circle(dh.BOLT_D / 2).extrude(-(BR_PLATE[3] + 1)).translate((0, BR_PLATE[2] - 1 + 0, 0)))
    b = b.cut(cq.Workplane("XZ").center(SLOT_X, BR_BOLT_Z).circle(BR_CB_D / 2).extrude(-(BR_CB_H + 1)).translate((0, BR_PLATE[3] - BR_CB_H, 0)))
    return b.cut(dh.teardrop_hole(MAG_POCKET_D, MAG_Y[0], MAG_Z, BR_LEG[0] - 1, BR_LEG[0] + MAG_POCKET_H))   # apex +y = up in the print

def tab_rear():
    t = box(*TAB_BLOCK).union(box(*TAB_PLATE))
    return t.cut(pocket_x(MAG_Y[1], MAG_Z, TAB_PLATE[0], MAG_POCKET_H, into=+1))

# ------------------------------------------------------------------ hinge leaves in this frame
def to_rail_frame(part):
    """door_hinge.py frame x -> this frame: x_local = 361 - x_frame (mirror about x = 180.5)."""
    return part.mirror("YZ", (dh.FACE_X / 2, 0, 0))

def hinge_pairs():
    """(door leaves, frame leaves) in the rail frame, at both hinge positions."""
    dl, fl = to_rail_frame(dh.door_leaf()), to_rail_frame(dh.frame_leaf())
    doors = [dl.translate((0, y0, 0)) for (y0, _) in PADS_Y]
    frames = [fl.translate((0, y0, 0)) for (y0, _) in PADS_Y]
    return doors, frames

AXIS = (dh.FACE_X - dh.AXIS_X, dh.AXIS_Z)        # (-8, 341) in this frame

def swing(part, deg):
    """Rotate about the hinge axis (along y). Positive = opening (the top of the door goes OUTWARD = -x here)."""
    return part.rotate((AXIS[0], 0, AXIS[1]), (AXIS[0], 1, AXIS[1]), -deg)

# ------------------------------------------------------------------ surroundings (rail frame, right side)
def surroundings():
    from skin_check import rail_with_outer_slot
    scope = rail_with_outer_slot(20, 330, dh.RAIL_Z0, dh.RAIL_Z1)
    top = rail_with_outer_slot(20, 330, 490.0, 510.0)
    # the top rail's BOTTOM slot too (the bracket's tongue goes in it): same section, turned to open downward at z 490
    from fit import SLOT_MOUTH, SLOT_LIP_T, SLOT_CAVITY_W, SLOT_THROAT_D, SLOT_DEPTH, SLOT_BOTTOM_W
    hm, hc, hb = SLOT_MOUTH / 2, SLOT_CAVITY_W / 2, SLOT_BOTTOM_W / 2
    pts = [(SLOT_X - hm, 489), (SLOT_X - hm, 490 + SLOT_LIP_T), (SLOT_X - hc, 490 + SLOT_LIP_T), (SLOT_X - hc, 490 + SLOT_THROAT_D), (SLOT_X - hb, 490 + SLOT_DEPTH),
           (SLOT_X + hb, 490 + SLOT_DEPTH), (SLOT_X + hc, 490 + SLOT_THROAT_D), (SLOT_X + hc, 490 + SLOT_LIP_T), (SLOT_X + hm, 490 + SLOT_LIP_T), (SLOT_X + hm, 489)]
    top = top.cut(cq.Workplane("XZ").polyline(pts).close().extrude(-310).translate((0, 20, 0)))
    uprights = box(0, 20, 0, 20, 0, 510).union(box(0, 20, 330, 350, 0, 510))
    band3 = box(-T, 0, 20, 330, 237.5, dh.SLOT_Z + 3.25)             # band-3 tiles with their top fingers' overhang...
    for (y0, y1) in st.HINGES:                                       # ...and their windows for the hinge plates (side_tile v2)
        band3 = band3.cut(box(-T - 1, 1, y0 - 0.5, y1 + 0.5, dh.RAIL_Z0 - 0.5, dh.SLOT_Z + 3.25 + 1))
    box_home = box(20, 311, 195, 330, 346, 456)                      # rear box at home (frame x 50-341)
    box_exit = box(-60, 311, 95, 230, 353.5, 463.5)                  # box leaving to the right, lifted 7.5 over the splice
    return dict(scope=scope, top=top, uprights=uprights, band3=band3, box_home=box_home, box_exit=box_exit)

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

def printable_tile(t):
    """Face down: the visible face (x = -T) on the bed. x -> z (as side_tile.printable)."""
    p = t.rotate((0, 0, 0), (0, 1, 0), -90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def printable_bracket(b):
    """Plate face (y = 20) down: +y -> +z."""
    p = b.rotate((0, 0, 0), (1, 0, 0), 90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def printable_tab(t):
    """Lying on its back face (x = 6.5): -x -> +z, so the pocket (at x 3.5, opening toward -x) faces up."""
    p = t.rotate((0, 0, 0), (0, 1, 0), 90); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "door")); os.makedirs(OUT, exist_ok=True)
    D, F, B, TB = door(), fixed(), bracket_front(), tab_rear()
    DL, FL = hinge_pairs()
    S = surroundings()
    door_asm = D.union(DL[0]).union(DL[1])
    print("--- proofs (cm3; 0 = clear) ---")
    for name, part in (("door", D), ("fixed tile", F), ("front bracket", B), ("rear tab", TB), ("door leaves", DL[0].union(DL[1])), ("frame leaves", FL[0].union(FL[1]))):
        print(f"{name:14s} " + "  ".join(f"vs {k} {vol(part, s):.4f}" for k, s in S.items() if not (k == "box_exit" and name in ("door", "door leaves"))))   # the closed door IS in the exit lane; it opens first
    print(f"door vs fixed tile {vol(D, F):.4f}; door vs tab {vol(D, TB):.4f}; door vs bracket {vol(D, B):.4f}; door vs frame leaves {vol(D, FL[0]) + vol(D, FL[1]):.4f}; "
          f"door vs door leaves {vol(D, DL[0]) + vol(D, DL[1]):.4f} (glued, 0.15 off); tab vs fixed tile {vol(TB, F):.4f} (glued); bracket vs tab {vol(B, TB):.4f}")
    probes = [box(BOSS_H, BOSS_H + MAG_GAP, y - BOSS / 2, y + BOSS / 2, MAG_Z - BOSS / 2, MAG_Z + BOSS / 2) for y in MAG_Y]        # the air between the faces
    probes2 = [box(BOSS_H, BOSS_H + MAG_GAP + 0.1, y - BOSS / 2, y + BOSS / 2, MAG_Z - BOSS / 2, MAG_Z + BOSS / 2) for y in MAG_Y]
    print(f"magnet gap: {MAG_GAP} of air in front of each boss vs bracket / tab {vol(probes[0], B):.4f} / {vol(probes[1], TB):.4f} (0); 0.1 more {vol(probes2[0], B):.4f} / {vol(probes2[1], TB):.4f} (>0: the holder faces are there)")
    print(f"door on its shelf: lowered 0.5 vs door leaves {vol(D.translate((0, 0, -0.5)), DL[0].union(DL[1])):.4f} (>0: sits on the shelves)")
    print(f"fixed tile: lifted 0.5 vs top rail {vol(F.translate((0, 0, 0.5)), S['top']):.4f} (fingers in the slot: >0 collides) / pulled 0.5 off the face {vol(F.translate((-0.5, 0, 0)), S['top']):.4f} (>0: barbs hold); "
          f"leg vs upright {vol(F, S['uprights']):.4f}; leg pushed 0.5 into the upright {vol(F.translate((0, 0.5, 0)), S['uprights']):.4f} (>0: flat on its face)")
    print(f"bracket: pushed 0.5 into the upright {vol(B.translate((0, -0.5, 0)), S['uprights']):.4f} (>0: flat on its face); tongue vs top rail {vol(B, S['top']):.4f} (0: in the slot); tongue shifted 0.5 in x {vol(B.translate((0.5, 0, 0)), S['top']):.4f} (>0: located)")
    # swing
    worst = {}
    for deg in range(0, 181, 15):
        d = swing(door_asm, deg)
        hits = {k: vol(d, s) for k, s in S.items() if k not in ("box_home", "box_exit")}
        hits["fixed"] = vol(d, F); hits["tab"] = vol(d, TB); hits["bracket"] = vol(d, B); hits["frame leaves"] = vol(d, FL[0]) + vol(d, FL[1])
        bb = d.val().BoundingBox()
        for k, v in hits.items(): worst[k] = max(worst.get(k, 0.0), v)
        print(f"  swing {deg:3d}°: x {bb.xmin:7.1f}..{bb.xmax:6.1f}  z {bb.zmin:6.1f}..{bb.zmax:6.1f}   " + "  ".join(f"{k} {v:.3f}" for k, v in hits.items() if v > 1e-6) or "")
    print("swing worst: " + ", ".join(f"{k} {v:.4f}" for k, v in worst.items()) + "  (all 0)")
    d180 = swing(door_asm, 180); print(f"door open 180: hangs at frame x {dh.FACE_X - d180.val().BoundingBox().xmax:.1f}..{dh.FACE_X - d180.val().BoundingBox().xmin:.1f}, z down to {d180.val().BoundingBox().zmin:.0f}; box exit lane vs open door {vol(d180, S['box_exit']):.4f} (0)")
    # exports
    for name, p, kw in (("door-v1", printable_tile(D), dict(min_rest_frac=0.25, max_down_frac=0.25)),
                        ("rear-tile-v1", printable_tile(F), dict(min_rest_frac=0.25, max_down_frac=0.25)),
                        ("magnet-bracket-front-v1", printable_bracket(B), dict(min_rest_frac=0.3, max_down_frac=0.6)),
                        ("magnet-tab-rear-v1", printable_tab(TB), dict(min_rest_frac=0.3, max_down_frac=0.2))):
        path = os.path.join(OUT, f"{name}.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        bb = p.val().BoundingBox()
        print(f"{name:24s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  {p.val().Volume()/1000:5.1f} cm3"); check(path, **kw)
