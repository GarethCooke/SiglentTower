# fit.py — every tuned clearance in one place (mm). Coupons P1–P9 exist to set these numbers; every part script imports
# them. Change a value here only when the coupon that owns it has passed (ROADMAP §3). Start values from ROADMAP v2.2.
# Each entry: value, then the coupon that owns it and what PASS looks like.

# P1 sled foot + web (src/parts/sled_foot.py)
SLOT_FOOT_W    = 5.8    # neck width in the 6.2 slot mouth (6.2 - 0.4); slides by hand, no rock
SLOT_FOOT_T    = 3.8    # flange thickness inside the slot cavity
FOOT_FLANGE_W  = 10.6   # flange width inside the ~11 cavity; undersides 45° to the neck
SLOT_LIP_T     = 1.8    # 2020 lip thickness, rail face -> inside of the lip (CNCMANS European 6.2 slot; P1 confirms)
FOOT_STANDOFF  = 2.2    # web outer face stands 2.2 off the rail face (x 20 -> 22.2) so the beam keeps a 1.5 outer wall
                        # outside the web (x 20.5-22.0) and its groove is closed on both sides -> beams print flat
FLANGE_GAP     = 0.2    # flange face -> inside of the lip; neck length = LIP + STANDOFF + GAP = 4.2
WEB_T          = 2.5    # web down the 3 mm gap between upright and AWG frame; must pass the 3.0 gauge
RIB_H          = 4.0    # rib on the web's top edge, inside the beam (z 337-341)
RIB_W          = 5.0    # rib widens from WEB_T to this toward +x at 45° (dovetail on the inboard side only)
BEAM_WALL      = 1.5    # beam material outside the groove (x 20.5-22.0); groove mouth = web + WEB_RIB_CLR each side
WEB_RIB_CLR    = 0.2    # beam rebate grown by this on the rib's fit faces (45° faces are layer-stepped: more than DOVETAIL_CLR)

# P2 PSU cradle (also AWG cradles: same saddle/clamp)
RAIL_CLR       = 0.4    # saddle channel = 20 + RAIL_CLR across the rail — PASSED 2026-09-17 (flat, no rock, M5x10 ok)
CUP_CLR        = 0.1    # radial, on the foot nominal, NO shrink allowance: conical cups do not close up like bores.
                        # Set by coupon rounds A/B 2026-09-17: 0.5/0.6/0.7 net all loose; 0.1 net best, -0.1 and -0.3 too tight.
PSU_FOOT_PAD_D = 16.8   # measured 2026-09-17: pad face 16.8, 19.5 at 4 mm above the pad, 21.5 at the chassis flange
PSU_FOOT_D4    = 19.5   # diameter 4 mm above the pad = at the cup rim (cup depth 4)
HOLE_SHRINK    = 0.3    # radial: a straight Ø22.2 bore in black ASA printed Ø21.6 (2026-09-17). Add to straight printed bores;
                        # NOT to conical cups (see CUP_CLR).

# P3 drawer runners / guide strips
RUNNER_CLR     = 0.3    # groove-to-runner clearance per side; side play < 0.5 total, no stick-slip

# P4 slot-clip tiles (side tiles, door, top tiles, housing-top tiles)
CLIP_T         = 3.0    # clip leg thickness (3 mm PETG)
CLIP_BARB      = 0.6    # barb interference into the 6.2 slot; thumb-snap in, tool out, 10 cycles

# P5 hinge + magnet
PIN_HOLE_D     = 3.2    # knuckle bore for the 3 mm pin
MAG_POCKET_D   = 10.4   # Ø10 x 2 magnets
MAG_POCKET_H   = 2.2

# P6 pull insert (src/coupons/p6_pull.py) — the pull is a SEPARATE part in the accent colour, printed face-down, glued
# into a notch in the facia's top edge. A slot cut straight into a standing facia leaves its top edge as a 100-120 mm
# bridge; a top-edge notch has no bridge, and the insert restores the top edge and carries the pocket.
JPULL_OPEN_H   = 10.0   # slot height in the insert's face
JPULL_HOOK     = 5.0    # face strip above the slot that the fingertip hooks up behind; cavity runs up behind it
JPULL_DEPTH    = 17.0   # cavity depth behind the face
JPULL_FLOOR_DEG = 30.0  # floor rises toward the back (a leaning wall in the face-down print — any angle prints)
JPULL_WALL     = 2.0
JPULL_INSERT_CLR = 0.15 # insert-to-notch clearance per side (P7 dovetail figure; glued)

# P7 quarter joint (drawer quarters, split sled beams, box halves)
DOVETAIL_CLR   = 0.15   # all-round clearance on every dovetail / puzzle tab — PASSED P7 2026-09-17 (cross, wall, beam all good)

# P8 TPU foot
SPIGOT_D       = 5.0    # spigot into the 2020 centre bore (~4.2 nominal); expect ~4.6

# P9 scope bumper cup / front-stand pocket — src/coupons/p9_bumper_cup.py
BUMPER_CUP_CLR = 0.3    # radial clearance on the Ø32 rear bumper; cup 5 deep in the beam top (bumper base z 341)
STAND_POCKET_D = 2.5    # front stand (44 x 43 x 11.5) sits in a pocket, not on a lipped pad: 14 - 11.5 = 2.5 keeps the scope level
STAND_CLR      = 0.3    # per side on the 44 x 43 stand footprint

# ---- measured hardware (not clearances; single source for part scripts) ----
STRIP_KEYHOLE_PITCH = 249.5   # Addtam 4-way strip, measured 2026-09-17
STRIP_KEYHOLE_D     = 6.5     # large hole
STRIP_KEYHOLE_SLOT  = 3.5     # slot width
STRIP_KEYHOLE_END   = 20.0    # cable end -> nearest keyhole centre
STRIP_KEYHOLE_FAR   = 81.5    # far end -> its keyhole centre (20 + 249.5 + 81.5 = 351 ≈ 350 body)
                              # keyhole slots run ACROSS the body -> the strip hangs HORIZONTALLY (D8: on the base rear cross rail)
STRIP_KEYHOLE_DEPTH = 6.5     # pocket depth behind the back face (peg head lives in here)
STRIP_BODY_W        = 78.1
STRIP_KEYHOLE_OFF   = 29.2    # keyhole line from one long edge (not centred; 48.9 from the other)
