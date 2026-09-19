# Sled T-foot + web (HANDOVER §4, PRINT-RULES §2) — one inverted-T part per side, 210 long, running in the scope
# rail's INNER side slot (rail z 311–331, slot centre z 321, mouth open toward +x at the rail face x 20).
#
# Section, world coordinates (left side; the right side is the same part turned end for end):
#   flange  x 14.2–18.0 (3.8 thick) × z 315.7–326.3 (10.6 tall)   inside the slot cavity, 0.2 behind the lip
#   neck    x 18.0–22.2 (4.2 long)  × z 318.1–323.9 (5.8 wide)    through the 6.2 mouth (1.8 lip + 2.2 stand-off + 0.2)
#   web     x 22.2–24.7 (2.5 thick) × z 315.7–341                 beside the upright; the AWG body is at x 26.5 (its 3.5 proud
#                                                               front bezel at x 23 is only ~10 deep — the foot never reaches it)
#   rib     x 22.2–27.2 × z 337–341 (top 4 mm of the web, inside the beam): widens 2.5 → 5.0 toward +x at 45°.
# The beam (z 337–346, outer face x 20.5) carries a closed dovetail groove in its underside (beam_groove()): 1.5 wall outside
# the web, 45° flank inboard, 5.4 mm ceiling — a bridge when the beam prints flat. Each beam half threads on from the FRONT.
#
# Print orientation: STANDING on the flange and web bottom edges (world z up), layers along the slide. The neck and flange
# grow toward −x and the rib toward +x, so neither web face can be the bed (rule 3); standing, the flange and web are plain
# vertical walls, the rib flank is a 45° face, and the only downward face is the neck's underside — a 2.5 mm bridge between
# flange and web (rule 4 allows < 12). Neck width 5.8 = 29 layers exactly. Bed edges get the 0.4 chamfer (rule 7).
# Print frame: X = world y (length), Y = world x − 14.2 (flange back face), Z = world z − 315.7 (flange bottom).
import os, sys, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import SLOT_FOOT_W, SLOT_FOOT_T, WEB_T, SLOT_LIP_T, FOOT_STANDOFF, FLANGE_GAP, FOOT_FLANGE_W, RIB_H, RIB_W, WEB_RIB_CLR, BEAM_WALL

NECK_L   = SLOT_LIP_T + FOOT_STANDOFF + FLANGE_GAP          # 4.2: x 18.0–22.2
Y_NECK1  = SLOT_FOOT_T + NECK_L                             # 8.0: web outer face (world x 22.2)
Y_WEB1   = Y_NECK1 + WEB_T                                  # 10.5: web inner face (world x 24.7)
Y_RIB    = Y_NECK1 + RIB_W                                  # 13.0 (world x 27.2)
Z_NECK0  = (FOOT_FLANGE_W - SLOT_FOOT_W) / 2                # 2.4  (world z 318.1)
Z_NECK1  = Z_NECK0 + SLOT_FOOT_W                            # 8.2  (world z 323.9)
Z_BEAM   = 337.0 - 315.7                                    # 21.3 (beam underside)
Z_TOP    = Z_BEAM + RIB_H                                   # 25.3 (web/rib top, world z 341)
RIB_GROW = RIB_W - WEB_T                                    # 2.5, at 45° over the first 2.5 of the rib

def foot_section():
    """(Y, Z) polygon of the foot in the print frame, counter-clockwise."""
    return [(0, 0), (SLOT_FOOT_T, 0), (SLOT_FOOT_T, Z_NECK0), (Y_NECK1, Z_NECK0),        # flange bottom, neck underside (bridge)
            (Y_NECK1, 0), (Y_WEB1, 0), (Y_WEB1, Z_BEAM), (Y_RIB, Z_BEAM + RIB_GROW),        # web bottom, inner face, rib flank
            (Y_RIB, Z_TOP), (Y_NECK1, Z_TOP), (Y_NECK1, Z_NECK1), (SLOT_FOOT_T, Z_NECK1),  # rib top, web outer face, neck top
            (SLOT_FOOT_T, FOOT_FLANGE_W), (0, FOOT_FLANGE_W)]                                # flange front and back

def foot(length):
    """T-foot + web, `length` along X, standing (z = 0 on the bed), 0.4 chamfer on the bed edges."""
    f = cq.Workplane("YZ").polyline(foot_section()).close().extrude(length)
    return f.edges("|X and <Z").chamfer(0.4)

def beam_groove(length, clr=WEB_RIB_CLR):
    """Solid to CUT from a beam's underside so it threads onto the rib. Beam frame: X = length, Y = world x − 20.5 (0 at the
    outer face), Z = world z − 337 (0 at the underside). Mouth = web ± clr, 45° flank inboard, ceiling RIB_H + clr up."""
    y0 = 20.5 + BEAM_WALL - 20.5 - 0.0                     # outer wall inner face, beam frame (1.5)
    y_web0 = (14.2 + Y_NECK1) - 20.5                       # web outer face in the beam frame (1.7)
    assert y_web0 - clr >= y0 - 1e-6, "web collides with the beam's outer wall"
    g = RIB_GROW
    pts = [(y_web0 - clr, -1), (y_web0 + WEB_T + clr, -1), (y_web0 + WEB_T + clr, 0), (y_web0 + RIB_W + clr, g),
           (y_web0 + RIB_W + clr, RIB_H + clr), (y_web0 - clr, RIB_H + clr)]
    return cq.Workplane("YZ").polyline(pts).close().extrude(length)

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts")); os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "sled-foot-210.stl")
    cq.exporters.export(foot(210.0), p, tolerance=0.01, angularTolerance=0.1); check(p)
