# Sill panel + end blocks (ROADMAP D10, Stage 8 trim):
#
# v10 LEFT BLOCK + WINDOW v4 (2026-10-27, Gareth, 17:03: the BUTTON's wires — "I can't push them in from the front
# because they won't fit. There needs to be a small gap at the bottom as you look at it from the front when it is
# mounted"): a WIRE SLIT 3.2 wide (x 43.4–46.6) runs from the block's bottom face up to the button's axis, from the front
# face right through to the back, and the same slit is notched into the bottom edge of the clear WINDOW under its hole.
# So the pre-wired button goes in from the FRONT with its four wires hanging down through the notch and the slit; as it
# is pushed home the wires trail rearward along the open-bottom slit, and when the thread meets the captive nut the
# tail is already over the wire channel (y 13.5–19.5), where the wires drop out of the bottom as before. The nut stays
# captive: the slit takes 3.2 of its pocket's 10.6 floor. From the front the notch shows under the bezel as a 3.2 ×
# ~1 mm nick in the clear window, 1 mm above the facia. Pixels as v8: pushed in from the REAR, pre-wired, and the two
# clip rails on the back face hold their wires. In the print the slit is a channel along print z with vertical walls;
# the window's notch is a 3.2 mm bridge 1.8 above the bed. Nothing else changes (v8 geometry otherwise).
# v9 LEFT BLOCK (2026-10-27, superseded the same day — a misreading: pixels fitted from underneath; it was the button's
# wires that needed the way in from below).
# v8 LEFT BLOCK (2026-10-27): the pixels' legs and the button's tags leave through the BACK face (y 19.5), the top of the
# front-face-down print, so v7's leg slots and bottom groove were dropped and two CLIP RAILS went on the back face on
# the clear strip left of the left pixel, x 22–30, standing 5.5 off the back face, one along the top edge (z 96.2–98)
# with its lip pointing down and one along the bottom edge (z 88–89.8) with its lip pointing up, lips 2.2 long with a
# 2.0 mouth between their tips, every lip underside a 45° slope (no support). The wires from both pixels run left along
# the back face, push in through the mouth one at a time and lie under the lips, then drop off the left end of the
# block to the left PSU rail's inner slot. Flange seat 6 deep as v7 (dome 4.1 into the cavity); the rails are 1.3 left
# of the pixel's counterbore, so a pixel still pulls out backwards.
# v7 LEFT BLOCK (2026-10-27, superseded the same day): leg slots to the bottom + a wire groove along the bottom face —
# wrong face: the legs leave through the back.
# v6 LEFT BLOCK (2026-10-27, same day): bore Ø5.7 (v5's 5.3 printed tight), flange seat Ø6.6 x 4 (dome 2.1 into the cavity).
# v5 LEFT BLOCK ONLY (2026-10-27, Gareth): the pixels go in from the REAR, pre-wired, so they can come out again. v3/v4's
# slots open to the bottom meant soldering the legs in place. The 2026-10-12 note that put the slots there ("the PSU cradle
# is 0.5 behind the block — no room for legs") was a crude envelope: psu_cradle.py's left front cradle is a 40 saddle at
# y 31–71 on the rail (x -3..23) with its 30-wide arm at y 36–66; behind the block at x 26–68, z 87–99 nothing is nearer
# than y 36, and the PSU's feet start at y 40.5. So v5 runs a Ø5.3 BORE along y from the light cavity (y 9) out of the
# back face (y 19.5) at each pixel position, with a Ø6.2 x 2.5 counterbore in the back face for the LED's flange: the
# 5 mm WS2812 pushes in from behind until its flange seats, its dome 0.6 into the cavity; the four legs, soldered to
# their wires beforehand, bend down 90° right behind the block and drop into the open space over the drawer (z 63–87)
# and across to the left PSU rail's inner slot. 16.5 mm between the block's back and the cradle arm for the bend. Pull
# the pixel out backwards to change it. Both bores are vertical in the front-face-down print; the counterbores open
# upward (the back face is the top of the print). The bottom slots are gone; the button's wire channel stays.
#
# v4 LEFT BLOCK ONLY (2026-10-14, from the v3 print, Gareth): (1) the head pocket was a 9.5 x 10 box with the bolt at y 10
# in a y 3-13 pocket - the head could not sit flat on the wall and the bolt went in at an angle. v4 seats the head in a
# round counterbore CBORE_D (10, takes the ISO 7380 M5 head at 9.5) coaxial with the hole, open to the front (a U: the
# round half behind the bolt line, a box in front of it), so the head bears square on the 2.2 wall. (2) No room for a key
# in front of the head: a KEY_D (3.6, passes a 3 mm key - a 2.5 key too) hole runs from the counterbore along the bolt
# axis through the block and out of its RIGHT end, so the key goes in from the right, under the PSU, before the button and
# panel go on. Both holes are teardrops (axis along x, apex toward +y = print up). Panel, window, right block unchanged (v3). the grey strip that fills the reveal between the bottom-drawer
# facia (top z 86) and the PSU's front (bottom z 100), carrying the lighting button and its halo. Frame coordinates.
#
# v3 (2026-10-13, from the v2 print): Gareth measured 233.7 between the left upright's inner face and the sub-frame
# upright's left face — the sub-frame sits 2.7 right of the model's x 251 (its left face is at x 253.7; the mini slot and
# column are modelled relative to that rail, so only this panel, which bridges from the main frame, sees it). Panel
# x 20–253.4 (233.4 long). And v2's left block could slide up and down in the upright's slot — the tongue only located it
# fore-aft — so the M5 is back: a head pocket LEFT of the button (x 22.5–32, open to the front), bolt along x through
# the 2.2 wall into the left upright's inner-face slot (y 10, z 93), driven with a ball-end 4 mm key from the front
# before the panel goes on. Button at x 45 (bezel 20 from the upright). The pixel bores no longer exit the back face
# (the PSU cradle is 0.5 behind it): each pixel drops into a slot open to the block's BOTTOM, pointing forward into the
# cavity, legs hanging down; the button's wires leave through a channel under its bore, also open to the bottom. All
# wires then drop to the left PSU rail's inner-face slot (z 78) — the space under the block, z 67–87 at y 3–20, is free.
#
# Parts:
#   PANEL   x 20–253.4 × y 0–3 × z 87–99, dark grey PETG; Ø8.4 button hole at (45, 93) in a 26 × 12 natural/clear PETG
#           WINDOW (x 32–58, separate STL, same origin). Pegs Ø3.2 × 7 on the back at x 64 and 227.5 (z 93), press fit
#           (Ø3.3 holes); the button's nut clamps the panel to the left block as well. Standing on its bottom edge.
#   LEFT BLOCK  x 20.3–68 × y 3–19.5 × z 87–99 against the left upright's inner face: M5 × 10 along x at (y 10, z 93)
#           through the 2.2 left wall, head in a pocket x 22.5–32 × y 3–13 open to the front. Captive hex nut pocket
#           10.6 AF (flats top/bottom) y 3–6 on the window's back round the Ø8.4 bore; body bore Ø9 y 6–19.5; light
#           cavity x 32–58 × y 3–9 × z 88–98 minus the hex boss; pixel slots 5.3 wide × y 9–19.5 open to the bottom at
#           x 34.6 / 55.3; wire channel 6 × 5 under the body bore, y 13.5–19.5, open to the bottom. FRONT FACE DOWN.
#   RIGHT BLOCK x 223.4–253.4 × y 3–19 × z 87–99 against the sub-frame upright's left face (x 253.7): M5 × 10 along x
#           at z 93 through a y 8.5–14.5 slot in its 7.7 right wall into that face's slot; head pocket x 231.7–245.7
#           open to the front; peg hole at x 227.5. FRONT FACE DOWN.
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from parts.drawer_quarters import box, teardrop_y

Z0, Z1, T = 87.0, 99.0, 3.0
PX0, PX1 = 20.0, 253.4
BTN_X, BTN_Z, BTN_HOLE_D = 45.0, 93.0, 8.4
WIN_X0, WIN_X1 = 32.0, 58.0
PEG_XS, PEG_Z, PEG_D, PEG_L, PEG_HOLE_D, PEG_HOLE_L = (64.0, 227.5), 93.0, 3.2, 7.0, 3.3, 7.5
LB_X0, LB_X1, LB_Y1 = 20.3, 68.0, 19.5
LB_POCKET = (22.5, 31.0, 3.0, 13.0, 88.0, 98.0)           # v3 box pocket, now only its x range is used: the head seat runs x 22.5-31
NUT_AF, NUT_T, HEX_WALL = 10.6, 3.0, 1.2            # captive nut pocket: 10 AF nut + 0.6, pocket depth, boss wall
BODY_D = 9.0
BOLT_Y, BOLT_Z, HOLE_D, CBORE_D, CBORE_H = 10.0, 93.0, 5.5, 10.0, 5.0
KEY_D = 3.6                                              # v4: key access along the bolt axis from the block's right end (3 mm key corners 3.46)
CAV = (32.0, 58.0, 3.0, 9.0, 88.0, 98.0)
LED_XS, LED_W, LED_Y0 = (34.6, 55.3), 5.3, 9.0          # pixel positions; v3/v4: slots 5.3 wide from y 9 to the back, open to the bottom
LED_BORE_D, LED_FLANGE_D, LED_FLANGE_H = 5.7, 6.6, 6.0   # v7 2026-10-27: seat 6 deep (Gareth: further through) -> dome 4.1 into the cavity, 1.9 short of the window
                                                         # v6 2026-10-27 (Gareth: the v5 LED would not push all the way in): bore 5.3 -> 5.7 — a small
                                                         # vertical bore prints ~0.3 under size (fit.HOLE_SHRINK) and a 5 mm LED body is Ø5.0 —
                                                         # and the flange seat 2.5 -> 4.0 deep so the dome stands 2.1 into the cavity, not 0.6.
                                                         # (5 mm LED: body Ø5, flange Ø5.8, 8.6 flange to dome tip)
WIRE_CH = (6.0, 5.0, 13.5)                               # button wire channel under the bore: width, height above the bottom, from y
CLIP = dict(x0=22.0, x1=30.0, h=5.5, post=1.8, reach=2.2, tip=1.5, z_lo=88.0, z_hi=98.0)   # v8: two clip rails on the back face (see header)
SLIT_W = 3.2                                              # v10: the button's wire slit, bottom face up to the axis, front face through to the back; window notched the same
RB_X0, RB_X1, RB_Y1 = 223.4, 253.4, 19.0
RB_WALL = 2.5                                            # v4: the right wall (v3 was 7.7 — an M5 x 10 through it reached only 2.3 into the T-nut)
RB_POCKET, RB_SLOT_Y = (RB_X1 - RB_WALL - 14.0, RB_X1 - RB_WALL, 3.0, 17.5, 88.0, 98.0), (8.5, 14.5)   # head pocket x 236.9–250.9, open to the front; slotted hole: the upright's slot centre is y 10 or 13
RB_KEY_D = 3.8                                           # v4: key access along the bolt axis from the block's LEFT end, a slot over the same y 8.5–14.5
RB_PEG_HOLE_D = PEG_HOLE_D + 0.1                         # v4: 3.4 — Gareth 2026-10-16, the peg was tight

def teardrop_x(yc, zc, r, x0, x1):
    """Round hole along x with a 45° peak toward +y (print 'up' when the block prints front face down)."""
    a = r / 2 ** 0.5
    tri = cq.Workplane("YZ").polyline([(yc + a, zc - a), (yc + r * 2 ** 0.5, zc), (yc + a, zc + a)]).close().extrude(x1 - x0)
    cyl = cq.Workplane("YZ").center(yc, zc).circle(r).extrude(x1 - x0)
    return cyl.union(tri).translate((x0, 0, 0))

def panel():
    p = box(PX0, PX1, 0, T, Z0, Z1)
    p = p.cut(box(WIN_X0, WIN_X1, -1, T + 1, Z0 - 1, Z1 + 1))
    for x in PEG_XS:
        p = p.union(cq.Workplane("XZ", origin=(x, T, PEG_Z)).circle(PEG_D / 2).extrude(-PEG_L))      # +y, into the block
    return p

def window():
    w = box(WIN_X0, WIN_X1, 0, T, Z0, Z1)
    w = w.cut(cq.Workplane("XZ", origin=(BTN_X, T + 1, BTN_Z)).circle(BTN_HOLE_D / 2).extrude(T + 2))
    return w.cut(box(BTN_X - SLIT_W / 2, BTN_X + SLIT_W / 2, -1, T + 1, Z0 - 1, BTN_Z))        # v4 (v10): wire notch from the hole to the bottom edge

def hex_prism(af, y0, y1, xc, zc):
    """Hexagon (flats top and bottom) of across-flats af, along y."""
    r = af / 3 ** 0.5           # circumradius
    pts = [(xc + r * math.cos(math.radians(a)), zc + r * math.sin(math.radians(a))) for a in (0, 60, 120, 180, 240, 300)]
    return cq.Workplane("XZ").polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))

def left_block():
    b = box(LB_X0, LB_X1, T, LB_Y1, Z0, Z1)
    x0, x1, y0, y1, z0, z1 = LB_POCKET
    b = b.cut(teardrop_x(BOLT_Y, BOLT_Z, CBORE_D / 2, x0, x1))                                        # v4: round head seat on the bolt axis (teardrop: apex is print-up)
    b = b.cut(box(x0, x1, y0 - 1, BOLT_Y, BOLT_Z - CBORE_D / 2, BOLT_Z + CBORE_D / 2))                 # ... opened to the front so the bolt drops in
    b = b.cut(teardrop_x(BOLT_Y, BOLT_Z, HOLE_D / 2, LB_X0 - 1, x0 + 1))                              # M5 through the left wall to the upright
    b = b.cut(teardrop_x(BOLT_Y, BOLT_Z, KEY_D / 2, x1 - 1, LB_X1 + 1))                                # v4: key hole along the bolt axis out of the right end
    x0, x1, y0, y1, z0, z1 = CAV
    cav = box(x0, x1, y0 - 1, y1, z0, z1)
    boss = hex_prism(NUT_AF + 2 * HEX_WALL, y0 - 1, y1 + 1, BTN_X, BTN_Z)                      # the hex boss stays solid inside the cavity
    b = b.cut(cav.cut(boss))                                                                  # light cavity either side of the boss
    b = b.cut(hex_prism(NUT_AF, T - 1, T + NUT_T, BTN_X, BTN_Z))                              # captive nut pocket on the window's back
    b = b.cut(cq.Workplane("XZ", origin=(BTN_X, LB_Y1 + 1, BTN_Z)).circle(BODY_D / 2).extrude(LB_Y1 + 2))      # body bore, through
    for x in LED_XS:                                                                          # v5–v8: pixel bores from the REAR
        b = b.cut(cq.Workplane("XZ", origin=(x, LB_Y1 + 1, BTN_Z)).circle(LED_BORE_D / 2).extrude(LB_Y1 + 1 - LED_Y0 + 1))       # Ø5.7, y 9 -> back face
        b = b.cut(cq.Workplane("XZ", origin=(x, LB_Y1 + 1, BTN_Z)).circle(LED_FLANGE_D / 2).extrude(LED_FLANGE_H + 1))         # flange seat Ø6.6 x 6
    b = b.union(clip_rails())                                                                  # v8: wire clips on the back face
    w, h, y0 = WIRE_CH                                                                        # button wires: channel under the bore, open to the bottom
    b = b.cut(box(BTN_X - w / 2, BTN_X + w / 2, y0, LB_Y1 + 1, Z0 - 1, Z0 + h))
    b = b.cut(box(BTN_X - SLIT_W / 2, BTN_X + SLIT_W / 2, T - 1, LB_Y1 + 1, Z0 - 1, BTN_Z))   # v10: the button's wire slit, front to back, open to the bottom
    for x in PEG_XS[:1]:
        b = b.cut(cq.Workplane("XZ", origin=(x, T - 1, PEG_Z)).circle(PEG_HOLE_D / 2).extrude(-(PEG_HOLE_L + 1)))
    return b

def clip_rail(z_post0, z_post1, down):
    """One clip rail on the back face: a post x0–x1 by z_post0–z_post1 rising CLIP['h'] off y LB_Y1, with a lip at its top
    reaching CLIP['reach'] toward -z (down=True) or +z, tip CLIP['tip'] thick, underside a 45° slope back to the post."""
    c = CLIP; y_top = LB_Y1 + c["h"]
    post = box(c["x0"], c["x1"], LB_Y1 - 0.01, y_top, z_post0, z_post1)
    zi = z_post0 if down else z_post1; sgn = -1 if down else 1               # the post's inner face and the lip direction
    tip = zi + sgn * c["reach"]
    lip = (cq.Workplane("YZ").polyline([(y_top, zi), (y_top, tip), (y_top - c["tip"], tip), (y_top - c["tip"] - c["reach"], zi)])
           .close().extrude(c["x1"] - c["x0"]).translate((c["x0"], 0, 0)))
    return post.union(lip)

def clip_rails():
    c = CLIP
    return clip_rail(c["z_hi"] - c["post"], c["z_hi"], True).union(clip_rail(c["z_lo"], c["z_lo"] + c["post"], False))

def right_block():
    b = box(RB_X0, RB_X1, T, RB_Y1, Z0, Z1)
    x0, x1, y0, y1, z0, z1 = RB_POCKET
    b = b.cut(box(x0, x1, y0 - 1, y1, z0, z1))                                                       # bolt-head pocket, open at the front
    for yc in RB_SLOT_Y:                                                                          # slotted M5 hole y 8.5–14.5
        b = b.cut(teardrop_x(yc, BOLT_Z, HOLE_D / 2, x1 - 1, RB_X1 + 1))
    b = b.cut(box(x1 - 1, RB_X1 + 1, RB_SLOT_Y[0], RB_SLOT_Y[1], BOLT_Z - HOLE_D / 2, BOLT_Z + HOLE_D / 2))
    for yc in RB_SLOT_Y:                                                                          # v4: key slot from the left end into the pocket
        b = b.cut(teardrop_x(yc, BOLT_Z, RB_KEY_D / 2, RB_X0 - 1, x0 + 1))
    b = b.cut(box(RB_X0 - 1, x0 + 1, RB_SLOT_Y[0], RB_SLOT_Y[1], BOLT_Z - RB_KEY_D / 2, BOLT_Z + RB_KEY_D / 2))
    for x in PEG_XS[1:]:
        b = b.cut(cq.Workplane("XZ", origin=(x, T - 1, PEG_Z)).circle(RB_PEG_HOLE_D / 2).extrude(-(PEG_HOLE_L + 1)))
    return b

def frame_bits():
    bits = [box(0, 20, 0, 20, 0, 510), box(0, 20, 20, 330, 68, 88),                 # left upright, left PSU rail
            box(0, 23, 31, 71, 82, 96), box(20, 65, 36, 66, 88, 96), box(20, 38, 36, 60, 91, 100),   # left front PSU cradle (v8: saddle y 31–71 + arm from y 36, as psu_cradle.py — the old y-20 envelope was wrong), PSU front feet
            box(23, 248, 3, 300, 100, 243),                                         # PSU body
            box(23, 338, 0, 3, 3, 86),                                              # bottom-drawer facia
            box(253.7, 273.7, 0, 23, 68, 247.5), box(273.7, 341, 3, 23, 68, 88), box(222.7, 253.7, 20, 60, 88, 96),   # sub-frame front upright AS MEASURED (left face x 253.7), tie, right PSU cradle reach
            box(273, 338, 0, 3, 91, 336), box(242, 268, 0, 3, 248, 336)]            # column facia, mini facia
    s = bits[0]
    for b in bits[1:]: s = s.union(b)
    return s

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "sill")); os.makedirs(OUT, exist_ok=True)
    P, W, L, R, FR = panel(), window(), left_block(), right_block(), frame_bits()
    def vol(a, b): return a.intersect(b).val().Volume()
    print("--- proofs (mm3; 0 = clear) ---")
    print(f"panel vs frame {vol(P, FR):.3f}  window vs frame {vol(W, FR):.3f}  left block vs frame {vol(L, FR):.3f}  right block vs frame {vol(R, FR):.3f}")
    print(f"panel vs blocks (pegs in holes) {vol(P, L):.3f} / {vol(P, R):.3f}   window vs panel {vol(W, P):.3f}   blocks vs each other {vol(L, R):.3f}")
    print(f"pegs locate: panel shifted 0.5 x / z vs blocks {vol(P.translate((0.5, 0, 0)), L) + vol(P.translate((0.5, 0, 0)), R):.1f} / {vol(P.translate((0, 0, 0.5)), L) + vol(P.translate((0, 0, 0.5)), R):.1f}  (> 0)")
    print(f"left block: M5 at (y {BOLT_Y}, z {BOLT_Z}) through x {LB_X0}..{LB_POCKET[0]}, head seat Ø{CBORE_D} x {LB_POCKET[0]}..{LB_POCKET[1]} open to the front, key hole Ø{KEY_D} x {LB_POCKET[1]}..{LB_X1}; block back at y {LB_Y1}, cradle arm from y 20 -> button must fit in {LB_Y1 - 3:.1f} behind the panel's back")
    # v4 proofs: an M5 button head (Ø9.5 x 2.7) seated on the wall at x 22.5, a 3 mm key (corners 3.46) along the axis from x 70 to the head
    head = cq.Workplane("YZ", origin=(LB_POCKET[0], 0, 0)).center(BOLT_Y, BOLT_Z).circle(9.5 / 2).extrude(2.7)
    key = cq.Workplane("YZ", origin=(LB_POCKET[0] + 2.7, 0, 0)).center(BOLT_Y, BOLT_Z).circle(3.46 / 2).extrude(LB_X1 + 10 - LB_POCKET[0] - 2.7)
    print(f"v4: head seated vs left block {vol(head, L):.3f} (0), head shifted 0.5 in y {vol(head.translate((0, 0.5, 0)), L):.3f} / z {vol(head.translate((0, 0, 0.5)), L):.3f} (>0: located); "
          f"key through to the head {vol(key, L):.3f} (0); head + key vs frame {vol(head, FR) + vol(key, FR):.3f} (0)")
    for yc in (10.0, 13.0):   # right v4 (the two real bolt positions): a Ø7.5 head seated on the 2.5 wall at either slot position, a 3.46 key from x 200 to the head
        headR = cq.Workplane("YZ", origin=(RB_POCKET[0], 0, 0)).center(yc, BOLT_Z).circle(7.5 / 2).extrude(RB_POCKET[1] - RB_POCKET[0]).translate((0, 0, 0))
        headR = cq.Workplane("YZ", origin=(RB_POCKET[1] - 2.7, 0, 0)).center(yc, BOLT_Z).circle(7.5 / 2).extrude(2.7)
        keyR = cq.Workplane("YZ", origin=(200.0, 0, 0)).center(yc, BOLT_Z).circle(3.46 / 2).extrude(RB_POCKET[1] - 2.7 - 200.0)
        print(f"right v4, bolt at y {yc}: head vs block {vol(headR, R):.3f} (0), shifted 0.5 up/down {vol(headR.translate((0, 0, 0.5)), R):.3f}/{vol(headR.translate((0, 0, -0.5)), R):.3f} (0: the pocket clears a 7.5 head); "
              f"key through to the head {vol(keyR, R):.3f} (0); head + key vs frame {vol(headR, FR) + vol(keyR, FR):.3f} (0); M5 x 10 in the T-nut: {10 - RB_WALL:.1f} mm")
    print(f"gaps: panel bottom {Z0} vs facia top 86 -> 1.0; panel top {Z1} vs PSU bottom 100 -> 1.0; panel right end {PX1} vs sub-frame upright 253.7 -> 0.3")
    # v5: the pixels behind the block vs the REAL left front PSU cradle (psu_cradle v3 at the front-left position: saddle centre
    # frame (10, 51), rail top 88) and the PSU's front-left foot
    import parts.psu_cradle as pc
    cradle = pc.cradle(pc.REACH_V3).rotate((0, 0, 0), (0, 0, 1), -90).translate((10.0, 51.0, 88.0))
    foot = cq.Workplane("XY", origin=(61.75, 51.0, 92.0)).circle(10.75).extrude(12)
    cb = cradle.val().BoundingBox(); print(f"left front PSU cradle as modelled: x {cb.xmin:.1f}–{cb.xmax:.1f}, y {cb.ymin:.1f}–{cb.ymax:.1f}, z {cb.zmin:.1f}–{cb.zmax:.1f} (its arm starts at y 36, not 20)")
    for x in LED_XS:
        led = box(x - 3.1, x + 3.1, LED_Y0 - 0.6, LB_Y1 + 3.0, BTN_Z - 3.1, BTN_Z + 3.1)                 # body + flange + 3 of leg before the bend
        legs = box(x - 3.5, x + 3.5, LB_Y1 + 0.5, LB_Y1 + 5.0, 70.0, BTN_Z + 3.1)                     # the four legs bent down behind the block
        print(f"pixel at x {x}: flange + leg bend behind the block vs block {vol(box(x - 3.1, x + 3.1, LB_Y1 + 0.01, LB_Y1 + 3.0, BTN_Z - 3.1, BTN_Z + 3.1), L):.4f}, legs vs block {vol(legs, L):.4f}, LED + legs vs cradle {vol(led, cradle) + vol(legs, cradle):.4f}, vs PSU foot {vol(led, foot) + vol(legs, foot):.4f} (all 0); "
              f"room behind the block to the cradle's arm: {36.0 - LB_Y1:.1f} mm")
    # v8 proofs: the clip rails; v10 proofs: the button's wire slit
    c = CLIP; mouth_z0, mouth_z1 = c["z_lo"] + c["post"] + c["reach"], c["z_hi"] - c["post"] - c["reach"]
    bundle = box(c["x0"] + 0.5, c["x1"] - 0.5, LB_Y1 + 0.2, LB_Y1 + 1.6, c["z_lo"] + c["post"] + 0.2, c["z_hi"] - c["post"] - 0.2)   # a 1.4-thick layer of wires lying flat on the face between the posts, under both lips
    wire = box(c["x0"] + 0.5, c["x1"] - 0.5, LB_Y1 + 0.01, LB_Y1 + c["h"] + 1, mouth_z0 + 0.3, mouth_z1 - 0.3)               # a 1.4 wire pushed in through the mouth
    rails = clip_rails()
    print(f"clip rails: x {c['x0']}–{c['x1']}, {c['h']} off the back face (y {LB_Y1}–{LB_Y1 + c['h']}), posts z {c['z_lo']}–{c['z_lo'] + c['post']} and {c['z_hi'] - c['post']}–{c['z_hi']}, "
          f"mouth z {mouth_z0:.1f}–{mouth_z1:.1f} ({mouth_z1 - mouth_z0:.1f}); a {bundle.val().BoundingBox().zlen:.1f} x 1.4 layer of wires under the lips vs block {vol(bundle, L):.4f} (0); "
          f"pulled 1.5 off the face {vol(bundle.translate((0, 1.5, 0)), L):.4f} (>0: the lips hold it); a 1.4 wire through the mouth {vol(wire, L):.4f} (0); "
          f"rails vs cradle {vol(rails, cradle):.4f} / PSU foot {vol(rails, foot):.4f} / frame {vol(rails, FR):.4f} (0); rails to the left pixel's counterbore: {LED_XS[0] - LED_FLANGE_D / 2 - c['x1']:.1f}")
    led_real = cq.Workplane("XZ", origin=(LED_XS[0], LB_Y1 - LED_FLANGE_H, BTN_Z)).circle(2.5).extrude(8.6)          # body from the flange seat forward
    lb = led_real.val().BoundingBox(); print(f"LED seated on its flange: body y {lb.ymin:.1f}–{lb.ymax:.1f}, cavity back wall at y {LED_Y0}: dome {LED_Y0 - lb.ymin:.1f} into the cavity")
    # v10: four Ø1.2 wires as a 2.4 x 2.4 bundle hanging through the notch and the slit, at every stage of the button going in
    wires = box(BTN_X - 1.2, BTN_X + 1.2, -0.5, LB_Y1 + 0.5, Z0 - 0.6, Z0 + 1.8)                                      # z 86.4–88.8: through the notch (top 88.8) and under the bore (88.5)
    nut = hex_prism(10.0, T, T + 2.5, BTN_X, BTN_Z).cut(cq.Workplane("XZ", origin=(BTN_X, T + 3, BTN_Z)).circle(4.0).extrude(4))   # an M8 nut, 10 AF x 2.5, in its pocket
    under_nut = box(BTN_X - 1.2, BTN_X + 1.2, T + 0.01, T + 3.5, BTN_Z - 5.0 - 2.4, BTN_Z - 5.0)                       # the same bundle dipping to z 85.6–88 where it passes under the nut (free air below the block)
    print(f"v10 wire slit {SLIT_W} wide: a 2.4 x 2.4 bundle along the whole slit vs window {vol(wires, W):.4f} / block {vol(wires, L):.4f} / panel {vol(wires, P):.4f} (0); "
          f"where it passes the nut it dips under the nut's bottom flat (z {BTN_Z - 5.0:.1f}): that bundle vs nut {vol(under_nut, nut):.4f} / block {vol(under_nut, L):.4f} / facia (y 0–3, top 86) {vol(under_nut, FR):.4f} (0); "
          f"nut vs block {vol(nut, L):.4f} (0), nut pulled down 0.5 {vol(nut.translate((0, 0, -0.5)), L):.4f} (>0: still captive — the slit takes {SLIT_W} of the pocket's 10.6 floor); "
          f"notch in the window: {SLIT_W} wide x {BTN_Z - BTN_HOLE_D / 2 - Z0:.1f} tall under the Ø{BTN_HOLE_D} hole; facia top 86 is 1.0 below the window's bottom edge")
    # exports
    def export(part, name, rot=None, **kw):
        p = part if rot is None else part.rotate((0, 0, 0), rot[0], rot[1])
        bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin)); path = os.path.join(OUT, name + ".stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:22s} {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {part.val().Volume()/1000:.1f} cm3"); check(path, **kw)
    # panel + window standing on the bottom edge (frame z up stays up): as modelled
    # panel + window share ONE origin so they load as a multi-part object with the window in its cut-out
    bb = P.val().BoundingBox(); shift = (-bb.xmin, -bb.ymin, -bb.zmin)
    for part, name in ((P, "sill-panel-v3"), (W, "sill-panel-window-v4")):
        p = part.translate(shift); path = os.path.join(OUT, name + ".stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        b2 = part.val().BoundingBox(); print(f"{name:22s} {b2.xlen:.1f} x {b2.ylen:.1f} x {b2.zlen:.1f}  {part.val().Volume()/1000:.1f} cm3"); check(path, min_rest_frac=0.2, max_down_frac=1.0)
    export(L, "sill-block-left-v10", rot=((1, 0, 0), 90), min_rest_frac=0.3, max_down_frac=2.5)     # front face down; the cavity roof and hex-to-bore step are short bridges
    export(R, "sill-block-right-v4", rot=((1, 0, 0), 90), min_rest_frac=0.3, max_down_frac=1.2)    # front face down; the pocket roof is a 14 mm bridge
