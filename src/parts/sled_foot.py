# Sled T-foot + web (HANDOVER §4, PRINT-RULES §2) — one hammer-nut-shaped part per side, 210 long, running in the scope
# rail's INNER side slot (rail z 311–331, slot centre z 321, mouth open toward +x at the rail face x 20).
# Slot as measured (fit.py SLOT_*): mouth 5.9, lip 1.75, cavity 10.6 wide down to 4.45 from the face, then ~45° walls to a
# 6.5 flat at 6.15. The flange is a T-nut section: full width behind the lips, chamfered to the bottom.
#
# Section, world coordinates (left side; the right side is the same part turned end for end):
#   flange  x 14.15–18.05: 6.8 wide at the bottom (x 14.15) widening at ~47° to 10.2 at x 15.75, full width to x 18.05
#           (0.2 off the lip underside at 18.25); z centred on 321
#   neck    x 18.05–22.2 (4.15 long) × z 318.25–323.75 (5.5 wide)  through the 5.9 mouth
#   web     x 22.2–24.7 (2.5 thick) × z 315.9–341                  beside the upright; AWG body at x 26.5
#   rib     x 22.2–27.2 × z 337–341 (top 4 mm of the web, inside the beam): widens 2.5 → 5.0 toward +x at 45°.
# The beam (z 337–346, outer face x 20.5) carries a closed dovetail groove in its underside (beam_groove()): 1.5 wall outside
# the web, 45° flank inboard, 5.4 mm ceiling — a bridge when the beam prints flat. Each beam half threads on from the FRONT.
#
# Print orientation: STANDING on the flange and web bottom edges (world z up), layers along the slide. Flange faces and web
# are vertical walls, the flange chamfers and rib flank are ≥45° faces, the only downward face is the neck's underside —
# a 4.15 mm bridge between flange and web. Bed edges get the 0.4 chamfer (rule 7).
# Print frame: X = world y (length), Y = world x − 14.15 (flange bottom), Z = world z − 315.9 (flange lower edge).
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import (SLOT_MOUTH, SLOT_LIP_T, SLOT_CAVITY_W, SLOT_THROAT_D, SLOT_DEPTH, SLOT_BOTTOM_W, SLOT_CLR, SLOT_FOOT_W,
                 FOOT_FLANGE_W, FLANGE_GAP, FOOT_STANDOFF, WEB_T, RIB_H, RIB_W, BEAM_WALL, WEB_RIB_CLR)

X_BOTTOM  = 20.0 - (SLOT_DEPTH - 0.3)                    # 14.15: flange bottom, 0.3 off the cavity floor
Y_TOP     = (20.0 - SLOT_LIP_T - FLANGE_GAP) - X_BOTTOM  # 3.9: flange top face (lip side)
Y_CH      = (20.0 - SLOT_THROAT_D + SLOT_CLR) - X_BOTTOM # 1.75: full width ends here, chamfer runs down to Y 0
W_BOT     = SLOT_BOTTOM_W + 2 * (0.3 * (SLOT_CAVITY_W - SLOT_BOTTOM_W) / 2 / (SLOT_DEPTH - SLOT_THROAT_D)) - 2 * SLOT_CLR  # 6.8
HALF, HALF_B = FOOT_FLANGE_W / 2, W_BOT / 2              # 5.1, 3.4
ZC        = HALF                                         # slot centre (world z 321) in the print frame
Z_NECK0, Z_NECK1 = ZC - SLOT_FOOT_W / 2, ZC + SLOT_FOOT_W / 2   # 2.35 / 7.85
Y_NECK1   = Y_TOP + SLOT_LIP_T + FLANGE_GAP + FOOT_STANDOFF     # 8.05: web outer face (world x 22.2)
Y_WEB1    = Y_NECK1 + WEB_T                                     # 10.55
Y_RIB     = Y_NECK1 + RIB_W                                     # 13.05
Z0_WORLD  = 321.0 - ZC                                          # 315.9
Z_BEAM    = 337.0 - Z0_WORLD                                    # 21.1 (beam underside)
Z_TOP     = Z_BEAM + RIB_H                                      # 25.1 (web/rib top, world z 341)
RIB_GROW  = RIB_W - WEB_T

def foot_section():
    """(Y, Z) polygon of the foot in the print frame, counter-clockwise from the flange's bottom bed edge."""
    return [(Y_CH, 0), (Y_TOP, 0), (Y_TOP, Z_NECK0), (Y_NECK1, Z_NECK0),                 # flange bottom edge, neck underside (bridge)
            (Y_NECK1, 0), (Y_WEB1, 0), (Y_WEB1, Z_BEAM), (Y_RIB, Z_BEAM + RIB_GROW),       # web bottom, inner face, rib flank
            (Y_RIB, Z_TOP), (Y_NECK1, Z_TOP), (Y_NECK1, Z_NECK1), (Y_TOP, Z_NECK1),       # rib top, web outer face, neck top
            (Y_TOP, FOOT_FLANGE_W), (Y_CH, FOOT_FLANGE_W),                                 # flange top face, full width
            (0, ZC + HALF_B), (0, ZC - HALF_B)]                                            # chamfers to the 6.8 bottom

def foot(length):
    """T-foot + web, `length` along X, standing (z = 0 on the bed), 0.4 chamfer on the bed edges."""
    f = cq.Workplane("YZ").polyline(foot_section()).close().extrude(length)
    return f.edges("|X and <Z").chamfer(0.4)

def beam_groove(length, clr=WEB_RIB_CLR):
    """Solid to CUT from a beam's underside so it threads onto the rib. Beam frame: X = length, Y = world x − 20.5 (0 at the
    outer face), Z = world z − 337 (0 at the underside). Mouth = web ± clr, 45° flank inboard, ceiling RIB_H + clr up."""
    y_web0 = (X_BOTTOM + Y_NECK1) - 20.5                   # web outer face in the beam frame (1.7)
    assert y_web0 - clr >= BEAM_WALL - 1e-6, "web collides with the beam's outer wall"
    g = RIB_GROW
    pts = [(y_web0 - clr, -1), (y_web0 + WEB_T + clr, -1), (y_web0 + WEB_T + clr, 0), (y_web0 + RIB_W + clr, g),
           (y_web0 + RIB_W + clr, RIB_H + clr), (y_web0 - clr, RIB_H + clr)]
    return cq.Workplane("YZ").polyline(pts).close().extrude(length)

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "sled-foot-210.stl")
    cq.exporters.export(foot(210.0), p, tolerance=0.01, angularTolerance=0.1); check(p, max_down_frac=1.0)
