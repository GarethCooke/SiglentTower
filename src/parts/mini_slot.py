# Mini-slot drawer (HANDOVER §6, ROADMAP D7, Stage 4): the 26-wide slot beside the AWG, riding ON the inner AWG-level rail
# (x 251–271, top z 247.5). Frame coordinates throughout: x from the left upright's outer face, y from the front plane,
# z from the bench. Three printed parts + the mini pull insert (pull_inserts.py, already printed):
#   RUNNER  (black ABS+) a 12-wide bar on the rail top, x 255–267, y 23–330, three M5 button heads down into the rail's
#           top slot (x 261; counterbored, 2 mm under the head). On it a DOVETAIL rib: neck 5 wide × 3 tall, flaring 45°
#           to an 8-wide head, 6 tall in all. One rib, not the P3 side pair — 26 mm of drawer cannot hold two P3 bosses.
#           A 2 × 10 × 2.5 STOP BUMP on the plate top at y 27–37 (left of the rib) sets the 250 travel.
#   BODY    (black PETG) 26 × 285 × 78.2 at x 242–268, y 3–288, z 252.8–331. Its bottom block (8.2 thick) carries the
#           GROOVE: the rib's profile + RUNNER_CLR on every face. The body's flat bottom (a bed-printed face) rides on
#           the runner's plate top (an ironed top surface) — the bearing; the flares hold the drawer down, 0.3 play,
#           when it is out 250 and cantilevered. A 2.6 × 2.8 channel beside the groove, open at the front, ends 8 from the rear: the runner's bump
#           rides in it and the channel's end hits the bump at full travel. The drawer goes on from the FRONT (groove and
#           channel open at the rear end? no — open at the REAR for the rib, the channel open at the FRONT for the bump:
#           thread the body onto the runner's front end and push home). Removal = undo the runner's three M5 with the
#           drawer fully out (all three heads are then exposed) and slide drawer + runner forward together.
#           D7 vent neck: over y 81–171 the left wall steps from x 242 to x 252 (body 16 wide) — a 15 mm air channel
#           beside the AWG's fan vent. Front wall 2.4 with its top at z 302 (the pull insert's lip and leg hook over it:
#           29 below the body top) and the side walls' front 5 mm rebated above z 282 for the insert's 25-wide flange.
#           Two peg holes through the front wall + pads at x 249 / 261, z 275 (the facia's pegs).
#   FACIA   (dark grey PETG) 26 × 3 × 88 at x 242–268, y 0–3, z 248–336, flush with the uprights: top-edge notch
#           22.3 × 23.15 for the mini insert (22 wide, slot 16), two Ø3.2 × 7 pegs on the back. No holes through the front.
# Home = the facia's back against the sub-frame's front upright (x 251–271, y 3). Nothing under the body rises above the
# rail top (right AWG cradle plate x 247–251 ends at z 247.5; the bezel is at x ≤ 237).
# Housing-top tile constraints (not yet modelled): notch x 242–268, y ≤ 22 at z 313–336 for the insert's pocket; the
# vent channel notch x 252–338 over y 81–171 (D7).
# Print: BODY floor down on the diagonal (groove = a tunnel in the bottom: neck opening on the bed, 45° flares, 8.6 roof
# bridge); RUNNER plate down on the diagonal (counterbores open upward, flares 45°); FACIA standing on its long edge.
import os, sys, math, cadquery as cq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fit import RUNNER_CLR, JPULL_OPEN_H, JPULL_HOOK, JPULL_WALL, JPULL_INSERT_CLR
from parts.drawer_quarters import box, teardrop_y

# ---- frame placement ----
RAIL_X0, RAIL_X1, RAIL_TOP = 251.0, 271.0, 247.5
SLOT_X = 261.0                                   # the rail's top slot centre
BX0, BX1, BY0, BY1, BZ1 = 242.0, 268.0, 3.0, 288.0, 331.0
FACIA_Z0, FACIA_Z1 = 248.0, 336.0
NECK_Y0, NECK_Y1, NECK_X0 = 81.0, 171.0, 252.0   # D7 vent channel: left wall steps to x 252 over y 81–171
# ---- runner ----
RUN_X0, RUN_X1, RUN_Y0, RUN_Y1 = 255.0, 267.0, 23.0, 330.0
PLATE_T = 5.0                                    # 2 under the M5 head after a 3 mm counterbore
NECK_W, NECK_H, HEAD_W, RIB_H = 5.0, 3.0, 8.0, 6.0   # rib: neck 258.5–263.5 z 252.5–255.5, 45° flare to 8 wide, head to 258.5
BOLT_YS = (40.0, 176.0, 312.0)
HOLE_D, CBORE_D, CBORE_H = 5.5, 9.0, 3.0
BUMP_X0, BUMP_X1, BUMP_Y0, BUMP_Y1, BUMP_H = 255.0, 257.0, 27.0, 37.0, 2.5
TRAVEL = 250.0
# ---- body ----
WALL, BLOCK_T = 2.4, 8.5                         # bottom block: from the body bottom (on the plate) to the floor top (2.2 over the groove roof)
BZ0 = RAIL_TOP + PLATE_T                         # 252.5: the body's BOTTOM FACE rides on the runner's plate top (bed-printed face on an
                                                 # ironed top surface); the groove roof clears the rib top by RUNNER_CLR, the flares hold it down
FLOOR_Z = BZ0 + BLOCK_T                          # 261
CHAN_W, CHAN_D, CHAN_END = 2.6, 2.8, 8.0         # stop channel in the bottom: bump + 0.3 each side, ends 8 from the rear
FRONT_WALL_TOP = 302.0                           # pull insert v2: wall top 11 below the insert's bottom (313)
REBATE_Y, REBATE_Z = 5.0, 282.0                  # side walls' front 5 mm removed above z 282 (flange 25 wide, leg to 282)
PAD_W, PAD_T, PAD_XS, PEG_Z = 8.0, 5.6, (249.0, 261.0), 275.0
PEG_D, PEG_L, PEG_HOLE_D = 3.2, 7.0, 3.4
# ---- facia ----
FT = 3.0
PULL_W, SLOT_W = 22.0, 16.0
H = 4.0 + JPULL_OPEN_H + JPULL_HOOK
NOTCH_W, NOTCH_H = PULL_W + 2 * JPULL_INSERT_CLR, H + JPULL_WALL + JPULL_INSERT_CLR     # 22.3 × 23.15
XM = (BX0 + BX1) / 2

def rib_profile(grow):
    """Dovetail section in XZ (x across, z up), grown by `grow` on every face; neck bottom at the plate top."""
    z0 = RAIL_TOP + PLATE_T
    n, h = NECK_W / 2 + grow, HEAD_W / 2 + grow
    f = (HEAD_W - NECK_W) / 2                   # 1.5: the 45° flare height
    # the flares keep their z: with the neck/head half-widths grown by 0.3 the 45° faces sit 0.3 below the rib's
    # (0.21 normal) — vertical play 0.3 exactly as P3's groove roof, not 0.6
    pts = [(SLOT_X - n, z0 - grow - 0.01), (SLOT_X + n, z0 - grow - 0.01),
           (SLOT_X + n, z0 + NECK_H), (SLOT_X + h, z0 + NECK_H + f),
           (SLOT_X + h, z0 + RIB_H + grow), (SLOT_X - h, z0 + RIB_H + grow),
           (SLOT_X - h, z0 + NECK_H + f), (SLOT_X - n, z0 + NECK_H)]
    return pts

def prism_y(pts, y0, y1):
    return cq.Workplane("XZ").polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))

def runner():
    r = box(RUN_X0, RUN_X1, RUN_Y0, RUN_Y1, RAIL_TOP, RAIL_TOP + PLATE_T)
    r = r.union(prism_y(rib_profile(0.0), RUN_Y0, RUN_Y1))
    r = r.union(box(BUMP_X0, BUMP_X1, BUMP_Y0, BUMP_Y1, RAIL_TOP + PLATE_T - 0.01, RAIL_TOP + PLATE_T + BUMP_H))
    for y in BOLT_YS:
        r = r.cut(cq.Workplane("XY", origin=(SLOT_X, y, RAIL_TOP - 1)).circle(HOLE_D / 2).extrude(PLATE_T + RIB_H + 2))
        r = r.cut(cq.Workplane("XY", origin=(SLOT_X, y, RAIL_TOP + PLATE_T - CBORE_H)).circle(CBORE_D / 2).extrude(RIB_H + CBORE_H + 1))
    return r

def outline(inset=0.0):
    """Body plan outline (XY) with the D7 neck step, inset by `inset` on every edge (the tray cavity at inset = WALL)."""
    pts = [(BX0, BY0), (BX1, BY0), (BX1, BY1), (BX0, BY1), (BX0, NECK_Y1), (NECK_X0, NECK_Y1), (NECK_X0, NECK_Y0), (BX0, NECK_Y0)]
    wp = cq.Workplane("XY").polyline(pts).close()
    return wp.offset2D(-inset, "intersection") if inset else wp

def body():
    d = outline().extrude(BZ1 - BZ0).translate((0, 0, BZ0))
    d = d.cut(outline(WALL).extrude(BZ1 - FLOOR_Z + 1).translate((0, 0, FLOOR_Z)))                     # the tray
    d = d.cut(box(BX0 - 1, BX1 + 1, BY0 - 1, BY0 + WALL + 1, FRONT_WALL_TOP, BZ1 + 1))               # front wall top at 302 (insert hooks over it)
    d = d.cut(box(BX0 - 1, BX1 + 1, BY0 - 1, BY0 + REBATE_Y, REBATE_Z, BZ1 + 1))                      # side walls' front rebate for the flange
    d = d.cut(prism_y(rib_profile(RUNNER_CLR), BY0 - 1, BY1 + 1))                                     # the groove: open both ends
    d = d.cut(box(BUMP_X0 - 0.3, BUMP_X1 + 0.3, BY0 - 1, BY1 - CHAN_END, BZ0 - 1, BZ0 + CHAN_D))     # stop channel, open at the front
    for xc in PAD_XS:                                                                                  # peg pads + holes
        d = d.union(box(xc - PAD_W / 2, xc + PAD_W / 2, BY0 + WALL, BY0 + WALL + PAD_T, FLOOR_Z - 1, PEG_Z + 7))
        d = d.cut(teardrop_y(xc, PEG_Z, PEG_HOLE_D / 2, BY0 - 1, BY0 + WALL + PAD_T + 1))
    return d

def facia():
    f = box(BX0, BX1, 0.0, FT, FACIA_Z0, FACIA_Z1)
    f = f.cut(box(XM - NOTCH_W / 2, XM + NOTCH_W / 2, -1, FT + 1, FACIA_Z1 - NOTCH_H, FACIA_Z1 + 1))
    for xc in PAD_XS:
        f = f.union(cq.Workplane("XZ", origin=(xc, FT, PEG_Z)).circle(PEG_D / 2).extrude(-PEG_L))     # +y, into the body
    return f

def insert_in_frame():
    from parts.pull_inserts import insert, INSERTS, H as IH, w as iw
    W, SW, ear, lip, wt, gaps = INSERTS["mini"]
    return insert(W, SW, ear, lip, wt, gaps).translate((XM - W / 2, 0, FACIA_Z1 - IH - iw))

def frame_bits():
    """What the slot must clear: the inner rail, the sub-frame's two uprights, the right AWG cradle plates, the column body."""
    bits = [box(RAIL_X0, RAIL_X1, 23, 330, 227.5, RAIL_TOP), box(RAIL_X0, RAIL_X1, 3, 23, 68, RAIL_TOP), box(RAIL_X0, RAIL_X1, 330, 350, 68, RAIL_TOP),
            box(247, 251, 20, 60, 227.5, RAIL_TOP), box(247, 251, 223, 263, 227.5, RAIL_TOP), box(273, 338, 3, 303, 91, 331),
            box(23, 237, 0, 20, 248, 340)]    # AWG bezel (x ≤ 237)
    s = bits[0]
    for b in bits[1:]: s = s.union(b)
    return s

def on_diagonal(p):
    p = p.rotate((0, 0, 0), (0, 0, 1), 45); bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin)), bb

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "mini")); os.makedirs(OUT, exist_ok=True)
    R, B, F, I, FR = runner(), body(), facia(), insert_in_frame(), frame_bits()
    def vol(a, b): return a.intersect(b).val().Volume()
    print("--- proofs (mm3; 0 = clear) ---")
    print(f"body vs runner {vol(B, R):.3f}   body vs frame {vol(B, FR):.3f}   runner vs frame {vol(R, FR):.3f}   facia vs frame/body {vol(F, FR):.3f} / {vol(F, B):.3f}")
    print(f"insert vs facia {vol(I, F):.3f}   insert vs body {vol(I, B):.3f}   insert fwd 0.5 {vol(I.translate((0, -0.5, 0)), F):.1f}  left 0.5 {vol(I.translate((-0.5, 0, 0)), F):.1f}")
    print(f"body held: up 0.5 {vol(B.translate((0, 0, 0.5)), R):.1f}  down 0.5 {vol(B.translate((0, 0, -0.5)), R):.1f}  left 0.5 {vol(B.translate((-0.5, 0, 0)), R):.1f}  right 0.5 {vol(B.translate((0.5, 0, 0)), R):.1f}   (all > 0)")
    print(f"body sideways 0.2 {vol(B.translate((0.2, 0, 0)), R):.1f} / up 0.2 {vol(B.translate((0, 0, 0.2)), R):.1f}   (free)")
    for t in (100.0, TRAVEL - 0.5, TRAVEL + 0.5):
        print(f"drawer out {t:5.1f}: vs runner {vol(B.translate((0, -t, 0)), R):.1f}  vs frame {vol(B.translate((0, -t, 0)), FR):.1f}   ({'bump stops it' if t > TRAVEL else 'free'})")
    print(f"facia pegs in the body's holes: pegs vs body {vol(F, B):.3f}; facia shifted 0.5 x / z: {vol(F.translate((0.5, 0, 0)), B):.1f} / {vol(F.translate((0, 0, 0.5)), B):.1f} (> 0: located)")
    print(f"facia home: back face y {FT} vs upright front y {BY0}; body front at y {BY0}; body bottom {BZ0}, floor top {FLOOR_Z}, inside {BX1 - BX0 - 2 * WALL:.1f} wide x {BZ1 - FLOOR_Z:.0f} tall")
    # exports
    # exported axis-aligned (as the column drawer): rotate 45° on the plate in the slicer — both are longer than the bed
    for part, name, mdf in ((B, "mini-slot-body-v1", 1.0), (R, "mini-slot-runner-v1", 0.6)):      # body: 8.6 + 2.6 wide bridges in the bottom
        bb = part.val().BoundingBox(); p = part.translate((-bb.xmin, -bb.ymin, -bb.zmin)); path = os.path.join(OUT, name + ".stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:20s} {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {part.val().Volume()/1000:.0f} cm3  diag {(bb.xlen + bb.ylen) / 2 ** 0.5:.0f}"); check(path, max_down_frac=mdf)
    p = F.rotate((0, 0, 0), (0, 1, 0), -90); bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))   # long edge down: z -> x
    path = os.path.join(OUT, "mini-slot-facia-v1.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
    print(f"mini-slot-facia-v1  {F.val().Volume()/1000:.1f} cm3"); check(path, min_rest_frac=0.2, max_down_frac=1.0)
