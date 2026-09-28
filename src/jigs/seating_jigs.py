# Seating jigs for the PSU and AWG cradles (Stage 3), yellow PETG, one plate. 2026-09-28.
#
# The rails fix every cradle across the frame (x); these bars set them front-to-back (y) and hold each front/rear pair
# at the instrument's spacing, so the instrument drops straight in.
#
# PSU L / PSU R — a bar with two replica PSU feet under it (same taper as the real foot: Ø16.8 at the pad, Ø19.5 at 4 up,
# 3.5 long so the bar rests on the cradle arms and the cone walls do the locating). Foot centres at frame y 51 and 253.5
# (PSU front face at y 3, feet 48 from the front, 34 from the rear of a 284.5 body). A nose arm reaches sideways to an
# upright and its front face is the stop: PSU L noses the front-left upright's rear face (y 20), PSU R the front inner
# upright's rear face (y 23). The arm is 52 long so it still reaches the upright if the cups move 3 mm (cradle v4).
# AWG L / AWG R — a bar with two 20 x 20 bosses that drop into the cradles' 20.4 pad pockets: 203 apart on the left
# (cradles at y 20 / 223), 200 on the right (y 23 / 223). The front cradle is set first (left: against the front
# upright; right: flush with the inner rail's front end), the bar sets the rear one.
# AWG pads ×4 — rigid PETG stand-ins for the TPU pads (20 x 20 x 5.5: 1.5 in the pocket, 4 proud) so the AWG can sit
# in its cradles before the Stage 8 TPU session.
#
# Print: everything as exported — bars upside down (their top face on the bed, feet/bosses rising, narrowing upward), no
# brim, no support, 2 walls, 15 % infill, `SiglentTower fit 0.20`.
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, SRC); sys.path.insert(0, os.path.join(SRC, "parts"))
from fit import PSU_FOOT_PAD_D, PSU_FOOT_D4, CUP_CLR

BAR_W, BAR_T = 8.0, 3.5          # bar section: stiff enough along its length, little plastic
DISC_D = 25.0                    # bar widens round each foot
PSU_TOP = 88.0 + 8.0             # cradle arm top = cup rim (PSU rail top 88 + TOP_T 8)
PSU_Y = (51.0, 253.5)            # PSU foot centres, frame y
PEG_L = 3.5                      # replica foot length below the bar (cup is 4 deep: tip stops 0.5 short of the floor)
ARM_REACH, ARM_W = 52.0, 7.0     # nose arm: from the foot line to past the upright; 7 wide stops short of the saddle at y 31
AWG_TOP = 247.5                  # AWG cradle arm tops, flush with the rail top
BOSS, BOSS_H = 20.0, 1.4         # into the 20.4 x 1.5 pad pocket
PAD_H = 5.5

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def peg(x, y):
    """Replica PSU foot, pad down: Ø16.8 at the pad, tapering out at the real foot's rate to the bar underside."""
    r_top = PSU_FOOT_D4 / 2                                   # 9.75 at 4 up on the real foot
    r_tip = r_top - (PSU_FOOT_D4 - PSU_FOOT_PAD_D) / 2 * PEG_L / 4.0
    return cq.Workplane("XY").add(cq.Solid.makeCone(r_tip, r_top, PEG_L, pnt=cq.Vector(x, y, PSU_TOP - PEG_L), dir=cq.Vector(0, 0, 1)))

def psu_jig(cup_x, side, nose_y):
    """side -1: nose arm to the left (PSU L), +1: to the right (PSU R). Frame coordinates."""
    z0, z1 = PSU_TOP, PSU_TOP + BAR_T
    j = box(cup_x - BAR_W / 2, cup_x + BAR_W / 2, nose_y, PSU_Y[1] + DISC_D / 2, z0, z1)
    for y in PSU_Y:
        j = j.union(cq.Workplane("XY").circle(DISC_D / 2).extrude(BAR_T).translate((cup_x, y, z0))).union(peg(cup_x, y))
    xa = sorted((cup_x, cup_x + side * ARM_REACH))
    j = j.union(box(xa[0], xa[1], nose_y, nose_y + ARM_W, z0, z1))
    # brace from the arm back to the front disc so the nose can't swing
    j = j.union(cq.Workplane("XY").polyline([(cup_x + side * ARM_REACH * 0.6, nose_y + ARM_W), (cup_x, nose_y + ARM_W),
                (cup_x, PSU_Y[0] - DISC_D / 2 + 2)]).close().extrude(BAR_T).translate((0, 0, z0)))
    return j

def awg_jig(bx, by):
    z0 = AWG_TOP
    j = box(bx - BAR_W / 2, bx + BAR_W / 2, by[0] - BOSS / 2, by[1] + BOSS / 2, z0, z0 + BAR_T)
    for y in by:
        j = j.union(box(bx - BOSS / 2, bx + BOSS / 2, y - BOSS / 2, y + BOSS / 2, z0 - BOSS_H, z0 + BAR_T))
    return j

def label(part, text):
    """Deboss the name 0.5 into the print's top face, along the bar's middle (part already in print orientation)."""
    bb = part.val().BoundingBox()
    return part.cut(cq.Workplane("XY").text(text, 5.0, 0.6, halign="center", valign="center", kind="bold")
                    .rotate((0, 0, 0), (0, 0, 1), 90).translate((cx_bar(part), (bb.ymin + bb.ymax) / 2, BAR_T - 0.5)))

_bar_x = {}
def cx_bar(part): return _bar_x[id(part)]

def for_print(part, bar_x):
    """Flip about y (x -> -x, z -> -z): the bar's top face goes on the bed, feet/bosses rise. Returns part and the bar's
    centreline x in print coordinates."""
    p = part.rotate((0, 0, 0), (0, 1, 0), 180)
    bb = p.val().BoundingBox()
    p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
    return p, -bar_x - bb.xmin

# ---- cradles in frame coordinates, for the fit check ----
def psu_cradle_frame(left, y0):
    src = open(os.path.join(SRC, "parts", "psu_cradle.py")).read().split("# ---------- export")[0]
    ns = {"__file__": os.path.join(SRC, "parts", "psu_cradle.py")}; exec(src, ns)
    b = ns["body"]                                           # local: x along rail, y across (arm +y), z up from rail top
    cup_local = ns["RAIL"] / 2 + ns["LIP_T"] + ns["REACH"]
    b = b.rotate((0, 0, 0), (0, 0, 1), 90)                   # local y -> -x, local x -> y
    if left: b = b.mirror("YZ"); xc = 10.0; cup_x = xc + cup_local
    else: xc = 261.0; cup_x = xc - cup_local
    return b.translate((xc, y0 + 20, 88.0)), cup_x

if __name__ == "__main__":
    import awg_cradle as ac
    from printcheck import check
    OUT = os.path.normpath(os.path.join(SRC, "..", "jigs")); os.makedirs(OUT, exist_ok=True)

    # frame reference geometry
    upright_FL = box(0, 20, 0, 20, 0, 510); upright_inner_F = box(251, 271, 3, 23, 68, 247.5)
    rail_L_psu = box(0, 20, 20, 330, 68, 88); rail_in_psu = box(251, 271, 23, 330, 68, 88)
    cr = {}
    for left in (True, False):
        for k, y in enumerate(PSU_Y):
            cr[(left, k)], cx = psu_cradle_frame(left, y - 20)
        cr[("cupx", left)] = cx
    jL = psu_jig(cr[("cupx", True)], -1, 20.0); jR = psu_jig(cr[("cupx", False)], +1, 23.0)
    aL = [ac.left_cradle().translate((0, y, 0)) for y in (20, 223)]; aR = [ac.right_bracket().translate((0, y, 0)) for y in (23, 223)]
    bL = awg_jig(ac.BODY_L + 0.5 + ac.PAD / 2 + ac.PAD_CLR, (40.0, 243.0)); bR = awg_jig(ac.BODY_R - ac.UNDER - ac.PAD_CLR + ac.PAD / 2, (43.0, 243.0))

    def vol(a, b): return a.intersect(b).val().Volume() if a.intersect(b).solids().size() else 0.0
    print("cup x: left", round(cr[("cupx", True)], 2), " right", round(cr[("cupx", False)], 2))
    report = []
    for name, j, others in (("PSU L", jL, [cr[(True, 0)], cr[(True, 1)], upright_FL, rail_L_psu]),
                            ("PSU R", jR, [cr[(False, 0)], cr[(False, 1)], upright_inner_F, rail_in_psu]),
                            ("AWG L", bL, aL), ("AWG R", bR, aR)):
        v = sum(vol(j, o) for o in others); report.append((name, v))
        # shift test: 0.5 forward must collide (the nose / bosses really locate)
        vs = sum(vol(j.translate((0, -0.5, 0)), o) for o in others)
        print(f"{name}: in place {v:.4f} cm3-ish (mm3 {v:.2f}), shifted 0.5 forward {vs:.2f} mm3")
        assert v < 0.01, name; assert vs > 0.01, name + " does not locate"
    # the nose really touches the upright: gap 0
    for name, j, up, yf in (("PSU L", jL, upright_FL, 20.0), ("PSU R", jR, upright_inner_F, 23.0)):
        bb = j.val().BoundingBox(); print(f"{name} nose face y {bb.ymin:.2f} (upright rear face {yf})")

    # ---- export, print orientation, labels, one plate ----
    parts = []
    for name, j, bx in (("psu-L", jL, cr[("cupx", True)]), ("psu-R", jR, cr[("cupx", False)]),
                        ("awg-L", bL, ac.BODY_L + 0.5 + ac.PAD / 2 + ac.PAD_CLR), ("awg-R", bR, ac.BODY_R - ac.UNDER - ac.PAD_CLR + ac.PAD / 2)):
        p, px = for_print(j, bx)
        _bar_x[id(p)] = px
        p = label(p, name.upper().replace("-", " "))
        path = os.path.join(OUT, f"seat-jig-{name}.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        check(path, min_rest_frac=0.1)   # a flat L-bar: its whole top face is on the bed (100 % of its own area), but
                                          # only ~20 % of its bounding box — the 30 % rule is for blocks, not open frames
        parts.append(p)
    pad = box(0, 20, 0, 20, 0, PAD_H).edges("|Z").chamfer(1.0)
    cq.exporters.export(pad, os.path.join(OUT, "awg-pad-standin.stl"), tolerance=0.01, angularTolerance=0.1)
    check(os.path.join(OUT, "awg-pad-standin.stl"))

    # plate: bars side by side, pads in a column
    plate = None; x = 0.0
    for p in parts:
        bb = p.val().BoundingBox(); q = p.translate((x, 0, 0)); plate = q if plate is None else plate.add(q); x += bb.xlen + 6
    for k in range(4): plate = plate.add(pad.translate((x, k * 26, 0)))
    plate_path = os.path.join(OUT, "seating-jigs-plate.stl")
    cq.exporters.export(plate, plate_path, tolerance=0.01, angularTolerance=0.1)
    import trimesh; m = trimesh.load(plate_path)
    print("plate extents", m.extents.round(1), " volume", round(m.volume / 1000, 1), "cm3")
