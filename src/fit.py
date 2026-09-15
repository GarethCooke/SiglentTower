# fit.py — every tuned clearance in one place (mm). Coupons P1–P9 exist to set these numbers; every part script imports
# them. Change a value here only when the coupon that owns it has passed (ROADMAP §3). Start values from ROADMAP v2.2.
# Each entry: value, then the coupon that owns it and what PASS looks like.

# P1 sled foot + web
SLOT_FOOT_W    = 5.8    # T-foot width in the 6.2 slot mouth (6.2 - 0.4); slides by hand, no rock
SLOT_FOOT_T    = 3.8    # T-foot thickness (flange) inside the slot
WEB_T          = 2.5    # web down the 3 mm gap between upright and AWG frame; must pass the 3.0 gauge

# P2 PSU cradle (also AWG cradles: same saddle/clamp)
RAIL_CLR       = 0.4    # saddle channel = 20 + RAIL_CLR across the rail
CUP_CLR        = 0.6    # radial clearance in the PSU foot cup

# P3 drawer runners / guide strips
RUNNER_CLR     = 0.3    # groove-to-runner clearance per side; side play < 0.5 total, no stick-slip

# P4 slot-clip tiles (side tiles, door, top tiles, housing-top tiles)
CLIP_T         = 3.0    # clip leg thickness (3 mm PETG)
CLIP_BARB      = 0.6    # barb interference into the 6.2 slot; thumb-snap in, tool out, 10 cycles

# P5 hinge + magnet
PIN_HOLE_D     = 3.2    # knuckle bore for the 3 mm pin
MAG_POCKET_D   = 10.4   # Ø10 x 2 magnets
MAG_POCKET_H   = 2.2

# P6 J-pull (fronts printed on edge, D3)
JPULL_OPEN_H   = 10.0   # opening height
JPULL_DEPTH    = 12.0
JPULL_FLOOR_DEG = 30.0

# P7 quarter joint (drawer quarters, split sled beams, box halves)
DOVETAIL_CLR   = 0.15   # all-round clearance on every dovetail / puzzle tab; iterate in 0.05 steps, expect 0.15–0.25

# P8 TPU foot
SPIGOT_D       = 5.0    # spigot into the 2020 centre bore (~4.2 nominal); expect ~4.6

# P9 scope bumper cup / front pad
BUMPER_CUP_CLR = 0.3    # radial clearance on the Ø32 rear bumper
PAD_LIP        = 5.0    # front pad lip height
