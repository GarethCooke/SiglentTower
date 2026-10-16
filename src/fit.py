# fit.py — every tuned clearance in one place (mm). Coupons P1–P9 exist to set these numbers; every part script imports
# them. Change a value here only when the coupon that owns it has passed (ROADMAP §3). Start values from ROADMAP v2.2.
# Each entry: value, then the coupon that owns it and what PASS looks like.

# P1 sled foot + web (src/parts/sled_foot.py). Slot measured on the CNCMANS 2020, 2026-09-19 (bar Z):
SLOT_MOUTH     = 5.9    # between the lips
SLOT_LIP_T     = 1.75   # outer face -> lip underside
SLOT_CAVITY_W  = 10.6   # widest, just behind the lips
SLOT_THROAT_D  = 4.45   # outer face -> where the cavity walls start angling in (full-width pocket ends)
SLOT_DEPTH     = 6.15   # outer face -> cavity bottom
SLOT_BOTTOM_W  = 6.5    # flat at the cavity bottom
SLOT_CLR       = 0.3    # per side, foot to slot, everywhere (neck in the mouth, flange in the cavity) — P1 v4 2026-09-20: of 0.3/0.4/0.5
                        # the 40 mm foot (0.3) slid best, yellow PETG. P1 PASSED 2026-09-21: 40 mm foot in black ABS+ slides the
                        # length of bar Z's inner slot, can't lift out, minor rock (accepted: the pair is tied by the bars and loaded)
SLOT_FOOT_W    = SLOT_MOUTH - 2 * SLOT_CLR      # 5.3 neck width (5.5 at v3's 0.2); slides by hand, no rock
FOOT_FLANGE_W  = SLOT_CAVITY_W - 2 * SLOT_CLR   # 10.0 flange (10.2 at v3), full width from the lip gap to the throat, then ~45 deg to the bottom
FLANGE_GAP     = 0.3    # flange top face -> lip underside (moves with SLOT_CLR; v4 tied them)
FOOT_STANDOFF  = 2.2    # web outer face stands 2.2 off the rail face (x 20 -> 22.2) so the beam keeps a 1.5 outer wall
                        # outside the web (x 20.5-22.0) and its groove is closed on both sides -> beams print flat
WEB_T          = 2.5    # web beside the upright; must pass the 3.0 gauge
RIB_H          = 4.0    # rib on the web's top edge, inside the beam (z 337-341)
RIB_W          = 5.0    # rib widens from WEB_T to this toward +x at 45° (dovetail on the inboard side only)
BEAM_WALL      = 1.5    # beam material outside the groove (x 20.5-22.0); groove mouth = web + WEB_RIB_CLR each side
WEB_RIB_CLR    = 0.2    # beam groove grown by this on the rib's fit faces (45° faces are layer-stepped: more than DOVETAIL_CLR)

# P2 PSU cradle (also AWG cradles: same saddle/clamp)
RAIL_CLR       = 0.4    # saddle channel = 20 + RAIL_CLR across the rail — PASSED 2026-09-17 (flat, no rock, M5x10 ok)
CUP_CLR        = 0.1    # radial, on the foot nominal, NO shrink allowance: conical cups do not close up like bores.
                        # Set by coupon rounds A/B 2026-09-17: 0.5/0.6/0.7 net all loose; 0.1 net best, -0.1 and -0.3 too tight.
PSU_FOOT_PAD_D = 16.8   # measured 2026-09-17: pad face 16.8, 19.5 at 4 mm above the pad, 21.5 at the chassis flange
PSU_FOOT_D4    = 19.5   # diameter 4 mm above the pad = at the cup rim (cup depth 4)
HOLE_SHRINK    = 0.3    # radial: a straight Ø22.2 bore in black ASA printed Ø21.6 (2026-09-17). Add to straight printed bores;
                        # NOT to conical cups (see CUP_CLR).

# P3 drawer runners / guide strips (src/parts/drawer_runner.py) — L-runner bolted into the base rail's TOP slot (a 3 mm gap
# cannot hide an M5 head), 7 mm rib into a house-shaped groove in a 10 x 20 boss on the drawer's outer wall. The drawer's
# floor top rests on the rib (no clearance there); RUNNER_CLR grows the groove's back and 45° roof and is the plate's
# stand-off from the drawer wall.
RUNNER_CLR     = 0.3    # groove back/roof over the rib, plate to drawer wall — geometry PASSED 2026-09-20 (little rock, slides);
                        # the 80 mm PETG coupon stuck in places (warped, one bolt). P3 PASSED 2026-10-01: both 300 ABS+ runners on
                        # four M5 each in the base rails, ironing on the rib, the dry-fitted drawer fits and slides well. FINAL —
                        # the column guide strips and the mini-slot runner use this value.

# P4 slot-clip tiles (src/parts/slot_clip.py) — the spring is a 25 x 5.5 finger cut free from the tile by a 1 mm U-slit,
# bending sideways in the tile plane; a 5.1 x 6 peg on its free end enters the 5.9 mouth (0.7 slack on the far side,
# 0.1 on the barb side) and a barb hooks the lip by CLIP_BARB with a 60° face (45° ramp in). Tiles meet on the slot
# centreline; each hooks its own lip; fingers staggered along the rail. P4 v1 plate: barb 0.6 and 0.9.
CLIP_T         = 3.0    # tile = finger thickness (3 mm PETG)
CLIP_BARB      = 1.2    # barb past the mouth edge, under the lip — PASSED P4 v2 2026-09-20 (variant C: barb 1.2, 45° hook, root stub 5.7)
CLIP_HOOK_DEG  = 45.0   # hook face angle from the tile plane that fits a 1.2 barb under the slot throat (60° only fits 0.9)
CLIP_STUB_CLR  = 0.1    # root stub to each mouth edge (5.7 in the 5.9 mouth) — lateral location, passed with C

# P5 hinge + magnet
PIN_HOLE_D     = 3.2    # knuckle bore for the 3 mm pin
MAG_POCKET_D   = 10.4   # Ø10 x 2 magnets
MAG_POCKET_H   = 2.2

# P6 pull insert (src/coupons/p6_pull.py) — the pull is a SEPARATE part in the accent colour, printed face-down, glued
# into a notch in the facia's top edge. A slot cut straight into a standing facia leaves its top edge as a 100-120 mm
# bridge; a top-edge notch has no bridge, and the insert restores the top edge and carries the pocket.
JPULL_OPEN_H   = 12.0   # slot height in the insert's face — PASSED P6 v2 2026-09-20 (10 / 12 / 14 tried, 12 best; 14 is the bridge ceiling)
JPULL_HOOK     = 5.0    # face strip above the slot that the fingertip hooks up behind; cavity runs up behind it
JPULL_DEPTH    = 17.0   # cavity depth behind the face
JPULL_FLOOR_DEG = 30.0  # floor rises toward the back (a leaning wall in the face-down print — any angle prints)
JPULL_WALL     = 2.0
JPULL_INSERT_CLR = 0.15 # insert-to-notch clearance per side (P7 dovetail figure; glued)

# P7 quarter joint (drawer quarters, split sled beams, box halves)
DOVETAIL_CLR   = 0.15   # all-round clearance on every dovetail / puzzle tab — PASSED P7 2026-09-17 (cross, wall, beam all good)

# P8 TPU foot
SPIGOT_D       = 4.6    # spigot into the 2020 centre bore (~4.2 nominal) — PASSED P8 2026-10-16: the TPU plate's feet at 4.6 push
                        # into the uprights and hold (glued in); the sweep was not needed. Cover flare 7.4 held too (tpu_parts.py)

# P9 scope bumper cup / front-stand pocket — src/coupons/p9_cups_v2.py
# v1 cup Ø32.6 was sized on the handover's "Ø32" — wrong. Calipers 2026-09-19 (width = scope width direction, depth =
# front-back): pad contact patch 20 x 9.5; at 5 mm up 25.9 x 24.0; at the chassis 25.9 x 26.4; ~14 tall. So the width is
# constant from 5 mm up, the depth grows ~0.27/mm, and the bottom 5 mm is a bullnose. Photos: D-shaped (flat one side,
# half-round the other, along the depth). A cup can only locate it at the 5 mm section, so v2 cups are STRAIGHT-walled
# 25.9 x 24 (+ clr) for 5 mm with a 1 mm 45° lead-in above (cup 6 deep, 3 mm floor in the 9 mm beam) — no lead-in inside
# the locating height, or nothing touches. Straight walls shrink in print (HOLE_SHRINK) so the plate runs to +1.0.
BUMPER_W       = 25.9   # across, at 5 mm up and above
BUMPER_D5      = 24.0   # flat -> arc at 5 mm up (the cup rim)
BUMPER_D_BASE  = 26.4   # at the chassis
BUMPER_PAD     = (20.0, 9.5)   # contact patch on the bench
BUMPER_H       = 14.0
BUMPER_CUP_D   = 6.0    # 5 straight + 1 lead-in
BUMPER_FLAT    = "rear" # the D's flat faces the scope's rear edge, the arc faces forward (2026-09-19)
BUMPER_SIDE_L  = 13.0   # straight side from the flat before the end arc starts, at the 5 mm section. v2 used a true
                        # semicircle (side 11.05, r 12.95) and only the +1.0 cup fitted: the foot's shoulders are fuller
                        # than that, so v3 lengthens the sides 2 mm and closes the end with a flatter three-point arc.
BUMPER_CUP_CLR = 0.3    # net per side on the 25.9 x 24 section, sides 13, flat arc — PASSED P9 v3 2026-09-19 ("perfect fit")
BUMPER_CUP_V3  = (0.1, 0.3, 0.5, 0.7, 1.0, 1.3)    # v3 plate, one row, value stamped by each (1.3 backs up v2's +1.0)
STAND_POCKET_D = 2.5    # front stand sits in a pocket, not on a lipped pad: 14 - 11.5 = 2.5 keeps the scope level
STAND_W        = 44.0   # across the scope — v1 pocket 44.6 PASSED 2026-09-19 (width perfect)
STAND_L        = 23.1   # front-to-back of the MAIN leg at the bench: v1 used the 43 overall, which includes the folded flap
                        # that tucks under the main leg and never reaches a 2.5 pocket -> v1 length FAIL; v2 pocket 23.7 PASSED 2026-09-20
STAND_CLR      = 0.3    # per side on the 44 x 23.1 main-leg footprint — PASSED (width v1, length v2): perfect fit (the coupon)
STAND_POCKET_CLR_X    = 0.6    # in the BEAM the pocket is looser than the coupon: the two rear cups (0.3) locate the scope in x and y,
STAND_POCKET_CLR_REAR = 1.0    # the pocket only levels it and stops it sliding — four 0.3 locators on three separate readings would bind
STAND_H        = 11.5   # front stand height, folded flat (HANDOVER §1)
STAND_X_FROM_SIDE     = 24.7   # stand's outer edge from the bezel's side face — P9 position jig 2026-09-24: skirt gap 5 -> 30 - 5 - 0.3
                               # (HANDOVER §1 had 24)
STAND_FRONT_FROM_FACE = 10.0   # scope front face -> front edge of the 23.1 main leg — MEASURED 2026-09-21 (the leg is at the
                               # front of the stand's 43; the flap folds rearward under it)
BUMPER_X_FROM_SIDE    = 44.15  # bezel side face -> bumper centre across — P9 position jigs 2026-09-24: the rear jig's skirt sits
                               # 3.5 further out than the front jig's, so centre = stand centre (24.7 + 22 = 46.7) + (56.25 - 55.3)
                               # - 3.5. Cross-check: rear skirt gap 13.5 -> outer side 26.5 from the BLUE BODY, i.e. the body is
                               # inset 4.7 per side behind the bezel (44.15 - 12.95 - 26.5). HANDOVER's 39 was 5 out.
BUMPER_REAR_FROM_FACE = 116.9  # scope front face -> the D's flat (rear) face: apex 92.9 + 24. The apex comes from the jig chain (stand
                               # pocket centre 24.55 + front jig rear edge 16.85 + 21.5 caliper gap between the jigs + 30) so the cup and the
                               # stand pocket are placed from ONE measurement and cannot fight; the rule read of 91 (2026-09-21) is ~2 low.
                               # Any error in the 10 (leg from face) moves cup and pocket together. HANDOVER's 135 was 18 out.
# scope placement in the frame (HANDOVER §2/§3): front frame x 23–338 (315), front face at y 3, chassis underside z 355
SCOPE_X0, SCOPE_W, SCOPE_Y0, SCOPE_Z0 = 23.0, 315.0, 3.0, 355.0

# ---- measured hardware (not clearances; single source for part scripts) ----
STRIP_KEYHOLE_PITCH = 249.5   # Addtam 4-way strip, measured 2026-09-17
STRIP_KEYHOLE_D     = 6.5     # large hole
STRIP_KEYHOLE_SLOT  = 3.5     # slot width
STRIP_KEYHOLE_END   = 20.0    # cable end -> nearest keyhole centre
STRIP_KEYHOLE_FAR   = 81.5    # far end -> its keyhole centre (20 + 249.5 + 81.5 = 351 ≈ 350 body)
                              # keyhole slots run ACROSS the body -> the strip hangs HORIZONTALLY (D8: on the base rear cross rail)
STRIP_KEYHOLE_DEPTH = 6.5     # pocket depth behind the back face (peg head lives in here)
STRIP_BODY_W        = 78.1
STRIP_KEYHOLE_OFF   = 29.2    # keyhole line from the strip's near long edge (measured 2026-09-17; the +8 tried on 2026-09-26 was
                              # withdrawn the next day — the shelf fouling the mains cable was the real problem)

# ---- PSU as seated in the frame (measured 2026-10-02, Stage 2.7) ----
PSU_FACE_X   = (20.0, 244.5)   # front face (225 wide) against the left PSU rail's inner face, 6.5 off the inner rail's left face
PSU_BODY_W   = 220.0           # body, centred under the face: x 22.25–242.25
PSU_FEET_CC  = 155.5           # foot centres across from a caliper reading (174.5 outer-to-outer, Ø19). Cups that fit on the bench (2026-10-03):
                               # left v3 at x 61.75, right rear v4 at 217.25 (= 155.5 apart), right front v5 at 213.25 — the PSU sits slightly skewed
PSU_H_FEET   = 150.0           # bench to case top standing on its feet (HANDOVER had 149)
