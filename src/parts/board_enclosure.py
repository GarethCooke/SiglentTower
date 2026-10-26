# board_enclosure.py — the lighting controller's enclosure (ROADMAP Stage 8, D10 rev 5; 2026-10-26).
# Replaces board-holder-v1 (src/parts/board_holder.py), which covered only 44 of the board's 70 and nothing in front
# of it. Two parts: the HOLDER (plate on the rail, two slotted side walls, floor, board ledge) and a LID (hex-vented
# rear plate that slides down the walls' inner slots like the board does, with a top flange that closes the top).
#
# What is kept from v1 (Gareth 2026-10-26: "the slide mechanism, the width and the amount it allows for underneath
# the board are all correct"): plate x 90-150 on the rear base rail's rear face (y 350-355), one M5 x 10 at (120, 10)
# counterbored into a drop-in T-nut in the rail's REAR slot, side walls 8.3 with a 2.0 board slot 4.0 deep in each
# inner face (floor y 358.3, 45 deg roof), 0.7 float a side, the board plane 3.5 off the plate, and two wire passages
# through the plate onto the rail's slot mouth either side of the bolt — v1's Ø6.5 holes grown to 16 x 8 slots
# (x 92-108 and 132-148, z 6-14) so a lead made up on the bench with its crimped housing on passes through.
#
# What changes. The board is now 50 x 70 (photo 2026-10-26: XIAO ESP32-S3 Plus, 74AHCT125, SR3200, 1000 uF, two 330 R)
# with FOUR straight plugs standing off the component face — plug plus cable exit 20 off the board (Gareth) — a 2-pin
# (USB 5 V) at the USB-C end, and at the other end two 3-pins (the L and R strips) and a 5-pin (the sill). Holes counted from the board's edge nearest
# the 2-pin: 2-pin holes 2-3 at the top end; bottom end 3-pin holes 2-4, two empty, 3-pin 7-9, three empty, 5-pin 13-17.
# Component side faces REARWARD, so that edge is the LOW-x edge in the frame (x = 94.6 + 3.41 + (n-1) x 2.54):
# 2-pin x ~98-106, 3-pins x ~98-108 and ~111-121, 5-pin x ~126-141.
#   * The plugs stand INSIDE the box: the lid plate's inner face is 25 off the board's component face, 5 clear of
#     the 20. Nothing passes through a wall. The three bottom plugs' leads leave rearward, turn down beside the
#     board's bottom edge and forward through the plate passages into the rail's rear slot — the board stands on a
#     ledge at z 28 so the 25 mm under it is a WIRE BAY for that turn and for fingers on the housings. The sill
#     bundle goes through the LEFT passage (cover run B1) and crosses the bay from x ~133; the L strip left, the R
#     strip right (B2). To unplug anything: lid up, pull the housing off its header; the leads stay where they are
#     (leave ~25 mm of slack in each inside the box) and the board lifts out past them.
#   * Board z 28-98; the walls run to z 108 (board top + 10, Gareth's figure). The USB lead leaves the 2-pin rearward
#     straight through a 10-wide U-notch in the lid above it — cut up from z 88 through the plate and the flange, open
#     at the lid's top rear corner — so it never has to bend inside the box.
#   * LID: a 2.4 plate (x 94.5-145.5, y 385.1-387.5, z 3.3-108) in a second pair of inner-face slots at y 384.9-387.7
#     (same section as the board slot: 4.0 deep, 45 deg roof; walls run to y 390.5 to carry the roof), hex-perforated
#     like the side tiles (R 4.2, pitch 10.9 / 9.44), with a 3 mm top flange (x 90-150, y 355-387.5, z 108-111) that
#     rests on the walls' tops and closes the top. Seven 2.5 x 18 slots in the flange and seven in the floor make the
#     chimney: in at the bottom, out through the hexes and the top. The USB notch runs down the plate to z 88 so the
#     lead passes straight out. Gravity holds the lid (15 g, behind the frame where
#     nothing touches it); a drop of CA on the flange if it ever walks. Behind the board the walls thin to 2 mm
#     (y 361-383.3) so the XIAO, whose body comes within ~3.5 of the board's edge, clears them; the lid-slot band at
#     the rear is full thickness again, reached by a 45 deg ramp.
#   * To get the board out: lid up and off, board up and out. Plugs stay on the board; they are reached with the lid off.
#
# Printing (PRINT-RULES): holder plate face down as v1 (frame +y rises), walls, floor and ledge rise from the plate,
# both slot pairs have 45 deg roofs, the plate holes and counterbore are vertical, the step-out behind the board faces
# up and the step back in is a 45 deg ramp. Lid outer face down (frame -y rises): hexes are through-cuts, the
# flange is a 3 x 30 fin standing on the bed along its own edge, its vent slots are vertical,
# the plate's side edges (the fit faces) are vertical walls. Both black PETG, no brim, no support.
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))

# ---- holder (v1 values kept where noted)
X0, X1, Y0, PLATE_T = 90.0, 150.0, 350.0, 5.0            # v1
Z0, Z_TOP = 0.0, 108.0                                   # wall top = board top 98 + 10
BOLT_X, BOLT_Z, HOLE_D, CBORE_D, CBORE_H = 120.0, 10.0, 5.5, 10.0, 2.5   # v1
WALL_T = 8.3                                             # v1
WALL_Y1 = 390.5                                          # was 365: now carries the lid slot and its roof
BOARD_W, BOARD_H, BOARD_T = 50.0, 70.0, 1.6
BOARD_X0 = 94.6                                          # v1: slot bottoms 94.3 / 145.7, 0.7 float a side
SLOT_FLOAT, SLOT_Y0, SLOT_Y1, SLOT_DEPTH, ROOF_FLAT = 0.7, 358.3, 360.3, 4.0, 1.5   # v1
LEDGE_Z0, LEDGE_Z1 = 25.0, 28.0                          # board stands at z 28 (v1: 0-3) — the wire bay is below it
FLOOR_T = 3.0                                            # floor z 0-3 across the walls, y 355-WALL_Y1
WIRE_SLOTS, WIRE_Z0, WIRE_Z1 = ((92.0, 108.0), (132.0, 148.0)), 6.0, 14.0   # passages through the plate (v1: Ø6.5 at x 100 / 140, z 10)
SLOT_X0 = X0 + WALL_T - SLOT_DEPTH                       # 94.3
SLOT_X1 = X1 - WALL_T + SLOT_DEPTH                       # 145.7
assert abs((SLOT_X1 - SLOT_X0) - (BOARD_W + 2 * SLOT_FLOAT)) < 1e-6
# ---- lid
LID_T, LID_CLR = 2.4, 0.2                                # plate thickness; clearance per face in its slot and per edge
LID_Y1 = 387.5                                           # lid's outer (rear) face — the bed face in the print
LID_Y0 = LID_Y1 - LID_T                                  # 385.1
LSLOT_Y0, LSLOT_Y1 = LID_Y0 - LID_CLR, LID_Y1 + LID_CLR  # 384.9-387.7
assert LSLOT_Y1 + (SLOT_DEPTH - ROOF_FLAT) <= WALL_Y1    # the roof reaches the wall's rear face, not past it
LID_X0, LID_X1 = SLOT_X0 + LID_CLR, SLOT_X1 - LID_CLR    # 94.5-145.5
LID_Z0 = Z0 + FLOOR_T + 0.3                              # 0.3 above the floor: the flange carries it
FLANGE_T, FLANGE_Y0 = 3.0, Y0 + PLATE_T                  # z 108-111, y 355-387.5 (flush with the lid's rear face)
USB_X = BOARD_X0 + 3.41 + 2.54 * 1.5                     # 2-pin's centre: holes 2-3 from the low-x edge -> 101.8
USB_NOTCH_W, USB_NOTCH_Y0 = 10.0, 361.0                  # notch in the flange from its rear edge forward to y 361 ...
USB_NOTCH_Z0 = 88.0                                      # ... and down the lid plate to z 88: the lead goes straight out
VENT_W, VENT_Y0, VENT_Y1 = 2.5, 364.0, 382.0             # flange and floor vent slots (along y)
VENT_XS = tuple(110.0 + 5.0 * i for i in range(7))      # x 110 ... 140, clear of the USB notch
SKIN_T = 2.0                                             # wall thickness behind the board (y 361-383.3): the cavity is 56 wide there
STEP_Y0 = 361.0                                          # the walls step out 0.9 above the board's component face: the
                                                         # board slot's roof then runs only to x 96.5 (a 1.9 lip over the
                                                         # board's edge, which v1's pull-off test showed is plenty) and the
                                                         # side-entry plugs, whose bodies end ~3 from the board's edge, clear it
STEP_Y1 = 383.3                                          # the rear thick band (lid slot) starts here, 45 deg ramp in
HEX_R, HEX_DX, HEX_DY, HEX_BORDER = 4.2, 2 * 4.2 + 2.5, (2 * 4.2 + 2.5) * 0.866, 4.0   # side_tile.py's pattern

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def slot_cut(x_in, x_bottom, y0, y1, z0, z1):
    """Slot in a side wall's inner face: floor at y0, roof flat over the innermost ROOF_FLAT then 45 deg to the mouth.
    x_in = the wall's inner face, x_bottom = the slot bottom. Section in xy, extruded along z. (v1 geometry.)"""
    d, f = SLOT_DEPTH, ROOF_FLAT
    if x_bottom < x_in:
        pts = [(x_bottom, y0), (x_in + 1, y0), (x_in + 1, y1 + d - f + 1), (x_bottom + f, y1), (x_bottom, y1)]
    else:
        pts = [(x_bottom, y0), (x_in - 1, y0), (x_in - 1, y1 + d - f + 1), (x_bottom - f, y1), (x_bottom, y1)]
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))

def teardrop_z(cx, cy, d, z0, z1, up="+y"):
    """A hole along z (frame) that is horizontal in a print where frame y or -y becomes print z: a circle plus a 45 deg
    apex on the side that is UP in the print. up = "+y" (holder print) or "-y" (lid print)."""
    r = d / 2; s = 1 if up == "+y" else -1
    c = cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((cx, cy, z0))
    t = cq.Workplane("XY").polyline([(-r * math.cos(math.pi / 4), s * r * math.sin(math.pi / 4)),
                                      (r * math.cos(math.pi / 4), s * r * math.sin(math.pi / 4)),
                                      (0, s * r / math.cos(math.pi / 4))]).close().extrude(z1 - z0).translate((cx, cy, z0))
    return c.union(t)

def holder():
    h = box(X0, X1, Y0, WALL_Y1, Z0, Z_TOP)                                         # the outer block
    h = h.cut(box(X0 + WALL_T, X1 - WALL_T, Y0 + PLATE_T, WALL_Y1 + 1, Z0 + FLOOR_T, Z_TOP + 1))   # v1 inner width
    # behind the board the walls thin to SKIN_T so components may run to the board's edge: a shelf out at STEP_Y0
    # (faces up in the print) and a 45 deg ramp back in before the lid-slot band (faces down -> self-supporting)
    for x_in, x_out in ((X0 + WALL_T, X0 + SKIN_T), (X1 - WALL_T, X1 - SKIN_T)):
        ramp = abs(x_in - x_out)
        pts = [(x_in, STEP_Y0), (x_out, STEP_Y0), (x_out, STEP_Y1 - ramp), (x_in, STEP_Y1)]
        h = h.cut(cq.Workplane("XY").polyline(pts).close().extrude(Z_TOP - Z0 - FLOOR_T + 1).translate((0, 0, Z0 + FLOOR_T)))
    # the wire bay under the ledge is the full 56 width too (nothing is slotted below z 28; the ledge stands on the plate), so the plugs hang clear
    h = h.cut(box(X0 + SKIN_T, X1 - SKIN_T, Y0 + PLATE_T, STEP_Y1 - (WALL_T - SKIN_T), Z0 + FLOOR_T, LEDGE_Z1))
    # board slots from the ledge up, open at the top
    h = h.cut(slot_cut(X0 + WALL_T, SLOT_X0, SLOT_Y0, SLOT_Y1, LEDGE_Z1 - 1, Z_TOP + 1))   # from 1 below the ledge top: no coincident face with the bay
    h = h.cut(slot_cut(X1 - WALL_T, SLOT_X1, SLOT_Y0, SLOT_Y1, LEDGE_Z1 - 1, Z_TOP + 1))
    # board ledge on the plate, 1 clear of each wall face (to the board's rear face, not past it: the plugs sit on that face)
    h = h.union(box(X0 + WALL_T + 1, X1 - WALL_T - 1, Y0 + PLATE_T, 360.0, LEDGE_Z0, LEDGE_Z1))
    # lid slots from the floor up, open at the top
    h = h.cut(slot_cut(X0 + WALL_T, SLOT_X0, LSLOT_Y0, LSLOT_Y1, Z0 + FLOOR_T, Z_TOP + 1))
    h = h.cut(slot_cut(X1 - WALL_T, SLOT_X1, LSLOT_Y0, LSLOT_Y1, Z0 + FLOOR_T, Z_TOP + 1))
    # M5 through the plate, counterbore from the rear face (v1)
    h = h.cut(cq.Workplane("XZ", origin=(BOLT_X, Y0 - 1, BOLT_Z)).circle(HOLE_D / 2).extrude(-(PLATE_T + 2)))
    h = h.cut(cq.Workplane("XZ", origin=(BOLT_X, Y0 + PLATE_T - CBORE_H, BOLT_Z)).circle(CBORE_D / 2).extrude(-(CBORE_H + 1)))
    for x0, x1 in WIRE_SLOTS:                                                       # wire passages onto the slot mouth
        h = h.cut(box(x0, x1, Y0 - 1, Y0 + PLATE_T + 1, WIRE_Z0, WIRE_Z1))
    for x in VENT_XS:                                                               # floor vents
        h = h.cut(box(x - VENT_W / 2, x + VENT_W / 2, VENT_Y0, VENT_Y1, Z0 - 1, Z0 + FLOOR_T + 1))
    return h

def lid():
    l = box(LID_X0, LID_X1, LID_Y0, LID_Y1, LID_Z0, Z_TOP)                         # the plate in the slots
    l = l.union(box(X0, X1, FLANGE_Y0, LID_Y1, Z_TOP, Z_TOP + FLANGE_T))            # top flange on the walls
    # hex vents in the plate: pointy-top hexes, staggered rows, solid border HEX_BORDER (side_tile.hex_holes' pattern)
    w, hgt = LID_X1 - LID_X0, Z_TOP - LID_Z0
    z = HEX_BORDER + HEX_R; row = 0; cuts = None
    while z < hgt - HEX_BORDER - HEX_R + 0.01:
        x = HEX_BORDER + HEX_R + (HEX_DX / 2 if row % 2 else 0.0)
        while x < w - HEX_BORDER - HEX_R + 0.01:
            if (LID_X0 + x + HEX_R + 1.5 > USB_X - USB_NOTCH_W / 2 and LID_X0 + x - HEX_R - 1.5 < USB_X + USB_NOTCH_W / 2
                    and LID_Z0 + z + HEX_R + 1.5 > USB_NOTCH_Z0):   # keep a 1.5 web round the USB notch (side_tile's rule)
                x += HEX_DX; continue
            pts = [(x + HEX_R * math.cos(math.pi / 6 + k * math.pi / 3), z + HEX_R * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
            hx = cq.Workplane("XZ").polyline(pts).close().extrude(-(LID_T + 2)).translate((LID_X0, LID_Y0 - 1, LID_Z0))
            cuts = hx if cuts is None else cuts.union(hx)
            x += HEX_DX
        z += HEX_DY; row += 1
    l = l.cut(cuts)
    # USB notch: through the flange from its rear edge forward to y 361, and down the plate to z 88 — a U open at the
    # lid's top rear corner, so the lead leaves the 2-pin straight rearward and the lid still drops on over it
    l = l.cut(box(USB_X - USB_NOTCH_W / 2, USB_X + USB_NOTCH_W / 2, USB_NOTCH_Y0, LID_Y1 + 1, Z_TOP - 1, Z_TOP + FLANGE_T + 1))
    l = l.cut(box(USB_X - USB_NOTCH_W / 2, USB_X + USB_NOTCH_W / 2, LID_Y0 - 1, LID_Y1 + 1, USB_NOTCH_Z0, Z_TOP + 1))
    for x in VENT_XS:                                                               # flange vents
        l = l.cut(box(x - VENT_W / 2, x + VENT_W / 2, VENT_Y0, VENT_Y1, Z_TOP - 1, Z_TOP + FLANGE_T + 1))
    return l

def board():
    """The bare board in place (components rearward of y 360.1)."""
    return box(SLOT_X0 + SLOT_FLOAT, SLOT_X1 - SLOT_FLOAT, 358.5, 358.5 + BOARD_T, LEDGE_Z1, LEDGE_Z1 + BOARD_H)

def components():
    """Envelope of what stands on the board's rear face. In the first 0.9 off the board (y 360.1-361) parts keep
    under the slot roofs' slope (1.9 off the edge at the board face, 2.8 at y 361); above that (the XIAO on its
    headers, the chip, the cap at ~20) the envelope runs to 1 mm off the board's edges, because the walls step out
    to 2 mm there (the cap, the tallest part, is 3 in). The four plugs are STRAIGHT: header + plug + cable exit stand
    20 off the board over their pins (body = pins + 2.45 each end along the row, 7.5 across it), the bottom three in
    the board's rows 1-3 (z 29.5-37), the 2-pin in the top rows 2-3 (z 89-96.5); the USB lead then continues
    rearward from the 2-pin through the lid's notch (y 380-392, a 6-wide band)."""
    bx0, bx1 = SLOT_X0 + SLOT_FLOAT, SLOT_X1 - SLOT_FLOAT
    b = box(SLOT_X0 + SLOT_DEPTH - ROOF_FLAT + (STEP_Y0 - SLOT_Y1), SLOT_X1 - SLOT_DEPTH + ROOF_FLAT - (STEP_Y0 - SLOT_Y1), 360.1, STEP_Y0, LEDGE_Z1, LEDGE_Z1 + BOARD_H)   # under the roofs' slope
    b = b.union(box(bx0 + 1.0, bx1 - 1.0, STEP_Y0, 360.1 + 20.0, LEDGE_Z1, LEDGE_Z1 + BOARD_H))   # tall parts, 1 off the edges (the cap is 3 in)
    hx = lambda n: BOARD_X0 + 3.41 + (n - 1) * 2.54
    zb, zt = LEDGE_Z1 + 1.5, LEDGE_Z1 + BOARD_H - 1.5                                # bottom / top board edge, 1.5 in
    plugs = [(hx(2) - 2.45, hx(4) + 2.45, zb, zb + 7.5),                                # 3-pin, holes 2-4 (low x)
             (hx(7) - 2.45, hx(9) + 2.45, zb, zb + 7.5),                                # 3-pin, holes 7-9
             (hx(13) - 2.45, hx(17) + 2.45, zb, zb + 7.5),                              # 5-pin, holes 13-17
             (hx(2) - 2.45, hx(3) + 2.45, zt - 7.5, zt)]                                # 2-pin at the top
    for x0, x1, z0, z1 in plugs: b = b.union(box(x0, x1, 360.1, 360.1 + 20.0, z0, z1))
    b = b.union(box(USB_X - 3.0, USB_X + 3.0, 380.0, 392.0, zt - 7.5, zt))              # the USB lead going out
    return b

def surroundings():
    """What the holder must clear (v1's list): rear base rail, rear uprights, Addtam + lower bracket, TPU feet, cable drop."""
    bits = [box(20, 341, 330, 350, 0, 20), box(0, 20, 330, 350, 0, 510), box(341, 361, 330, 350, 0, 510),
            box(1, 79, 355, 385, 75, 425), box(0, 80, 350, 380, 51, 75),
            box(-2, 22, 328, 352, -6, 0), box(339, 363, 328, 352, -6, 0), box(14, 46, 350, 400, -6, 75)]
    s = bits[0]
    for b in bits[1:]: s = s.union(b)
    return s

def printable(part, up):
    """up='+y': plate face down (holder). up='-y': rear face down (lid). Rotation only — rule 13."""
    p = part.rotate((0, 0, 0), (1, 0, 0), 90 if up == "+y" else -90)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "wiring")); os.makedirs(OUT, exist_ok=True)
    H, L, B, C, S = holder(), lid(), board(), components(), surroundings()
    sh = lambda p, dx=0, dy=0, dz=0: p.translate((dx, dy, dz))
    print("--- proofs (cm3; 0 = clear) ---")
    print(f"holder vs frame/Addtam/feet/cable {vol(H, S):.4f}; pushed 0.5 into the rail {vol(sh(H, dy=-0.5), S):.4f} (>0: flat on it)")
    print(f"board in the holder {vol(B, H):.4f}; pulled 1.0 off the plate {vol(sh(B, dy=1), H):.4f} / pushed 1.0 {vol(sh(B, dy=-1), H):.4f} (>0: held); "
          f"left/right 1.0 {vol(sh(B, dx=-1), H):.4f}/{vol(sh(B, dx=1), H):.4f} (>0: 0.7 float); 0.5 down {vol(sh(B, dz=-0.5), H):.4f} (>0: on the ledge); "
          f"lifted 100 {vol(sh(B, dz=100), H):.4f} (0: out the top with the lid off)")
    print(f"components vs holder {vol(C, H):.4f}  vs lid {vol(C, L):.4f}  (plugs stand 20 off the board inside the box, the USB lead out through the notch)")
    print(f"lid in the holder {vol(L, H):.4f}; left/right 0.5 {vol(sh(L, dx=-0.5), H):.4f}/{vol(sh(L, dx=0.5), H):.4f} (>0: 0.2 play); "
          f"pulled 0.5 rearward {vol(sh(L, dy=0.5), H):.4f} / pushed 0.5 {vol(sh(L, dy=-0.5), H):.4f} (>0: held by the roofs); "
          f"lowered 0.5 {vol(sh(L, dz=-0.5), H):.4f} (>0: flange on the wall tops); lifted 110 {vol(sh(L, dz=110), H):.4f} (0: slides off)")
    print(f"lid vs board {vol(L, B):.4f}; lid plate inner face y {LID_Y0} vs the plugs' 20 (y {360.1 + 20}): {LID_Y0 - 380.1:.1f} clear")
    print(f"components pushed 0.5 rearward (toward the ramps) {vol(sh(C, dy=0.5), H):.4f} (0: a 20-tall part may stand 1.5 off the board's edge)")
    print(f"USB notch x {USB_X - USB_NOTCH_W / 2:.1f}-{USB_X + USB_NOTCH_W / 2:.1f} over the 2-pin (holes 2-3 from the LOW-x edge: x {BOARD_X0 + 3.41:.1f} + 2.54)")
    print(f"components pushed 0.5 toward a wall: {vol(sh(C, dx=-0.5), H):.4f}/{vol(sh(C, dx=0.5), H):.4f} (0: the cavity is wider than the board)")
    housing = box(132.5, 147.5, 340.0, 356.0, 6.5, 13.5)   # a 5-pin XH housing (15 x 7) half way through the right passage
    print(f"a 15 x 7 crimped housing through a passage {vol(housing, H):.4f} (0: leads can be made up on the bench first); bolt head x 115-125 clear of both")
    hb = H.val().BoundingBox(); lb = L.val().BoundingBox()
    print(f"holder frame bbox x {hb.xmin:.1f}-{hb.xmax:.1f} y {hb.ymin:.1f}-{hb.ymax:.1f} z {hb.zmin:.1f}-{hb.zmax:.1f}; lid x {lb.xmin:.1f}-{lb.xmax:.1f} y {lb.ymin:.1f}-{lb.ymax:.1f} z {lb.zmin:.1f}-{lb.zmax:.1f}")
    for name, part, up, rest, down in (("board-enclosure-v1", H, "+y", 0.3, 0.6), ("board-lid-v1", L, "-y", 0.3, 0.3)):
        p = printable(part, up); bb = p.val().BoundingBox(); path = os.path.join(OUT, name + ".stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name}  {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {p.val().Volume()/1000:.1f} cm3")
        check(path, min_rest_frac=rest, max_down_frac=down)
    # hand check (rule 13): in the holder print the wire holes / bolt sit at print x = frame x - 90 (no mirror)
    ph = printable(H, "+y"); pb = ph.val().BoundingBox()
    print(f"hand check: holder print bbox x 0-{pb.xmax:.1f}, the two wire passages at print x {WIRE_SLOTS[0][0] - X0:.0f}-{WIRE_SLOTS[0][1] - X0:.0f} and {WIRE_SLOTS[1][0] - X0:.0f}-{WIRE_SLOTS[1][1] - X0:.0f} (no mirror); "
          f"lid print: the USB notch (low frame x) at print x {USB_X - USB_NOTCH_W / 2 - X0:.1f}-{USB_X + USB_NOTCH_W / 2 - X0:.1f} from the lid's low-x end")
