# top_panel.py — the top panel (HANDOVER §3/§5: z 510–513 on the top rails) as FOUR tiles printed STANDING on one plate,
# plus the four upright caps that screw the panel's corners down. Black PETG tiles, dark blue PETG caps. Stage 7 skin.
#
# Why this shape (ROADMAP v2.17, D12):
#   * The panel covers the whole frame top — x 0–362 (tape, 2026-10-14; model 361), y 0–350 — corner holes slotted 1.5 along x so 361–363 all fit — so it lies on the four uprights' top faces and the three
#     top rails (both sides, rear). HANDOVER's "321 × 310 between the caps" would have rested on nothing. The caps now
#     sit ON the panel's corners: 20 × 20 × 6 with an M5 × 10 button head through a Ø5.5 hole in the panel into the
#     upright's centre bore (an M5 self-taps a 2020 bore). Four screws hold the panel down; nothing else is needed.
#   * Nothing can go UNDER the panel: the scope top is at 507, 3 mm below (and it slides forward under the front edge).
#     So D4's H-spline under the seams is dropped. The four tiles meet on 10 mm wide HALF-LAPS instead and are CA'd
#     into one 361 × 350 sheet on the frame: the left and front tiles carry the LOWER tongue (z 0–1.5), the right and
#     rear tiles the UPPER tongue (z 1.6–3.0, a 0.1 glue line); the tongue ends have 0.1 clearance so the top-face seam
#     is a hairline at x 175.5 and y 170. A one-sided lap only stops one tile dropping below the other, which is why
#     the laps are glued — glued, the seam is as stiff as the sheet.
#   * Each tile prints STANDING on its outer front/rear edge (D3, as the facias): both faces are wall finish, the laps
#     are 1.5 / 1.4 mm fins at the top or at a vertical end (nothing hangs below the bed face), the corner hole is a
#     teardrop because its axis is horizontal in the print. The tiles stand side by side, flat on the bed (185.5 long,
#     175 tall), so ALL FOUR go on one plate with the caps: ~380 cm³, the biggest single plate in the build.
#     Thin-part settings as the column facia: brim outer 15 gap 0, skirt off, door closed, bed 80, fan 30 % max,
#     outer wall 60. Trim the brim off the front edge (it is the visible edge).
#   * Sag: the panel is held on three rails and four screwed corners; only the front edge spans free between the
#     uprights (321). Self-weight sag of a 3 mm sheet there is ~0.5 mm — inside the 3 mm reveal to the scope.
#
# Proofs (python src/parts/top_panel.py): four tiles assembled 0 cm³ with every lap engaged (any tile lifted or
# lowered 0.5 collides with a neighbour; shifted 0.3 along either seam collides); panel on the frame 0 cm³, lowered
# 0.5 collides (sits on the uprights and rails); 3.0 mm to the scope at home and pulled out 100; corner holes centred on
# the uprights' bores; caps on the corners 0 cm³ against the frame and the side tiles; every STL through printcheck.
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))

# ---- panel ----
PX0, PX1, PY0, PY1 = 0.0, 362.0, 0.0, 350.0     # frame outer faces AS MEASURED 2026-10-14 (tape: 362 x 350; model 361 x 350)
Z0, T = 510.0, 3.0                             # on the rail / upright tops (490–510), 3 thick -> z 510–513
SEAM_X, SEAM_Y = 181.0, 175.0                  # the two seams; four tiles 181 x 175 nominal
LAP = 10.0                                     # lap width (±5 about the seam)
LOWER_T = 1.5                                  # lower tongue thickness (left / front tiles)
GLUE = 0.1                                     # glue line: upper tongue from z 1.6
END_CLR = 0.1                                  # between tongue ends and the facing tile (0.05 each)
HOLE_D = 5.5                                   # M5 clearance, teardrop in the standing print
HOLE_IN = 10.0                                 # hole centre = the upright's centre bore, 10 in from both outer faces
HOLE_SLOT = 1.5                                # the holes are slots this long ALONG X: the 362 is a tape reading, so the panel tolerates 361–363
BED_CHAMFER = 0.4                              # rule 7, on the standing edge

# ---- cap ----
CAP_W, CAP_H = 20.0, 6.0                       # on the upright's 20 x 20 top, over the panel: z 513–519
CAP_CBORE_D, CAP_CBORE_H = 9.5, 4.0            # M5 button head Ø8.5 x 2.7 sits 1.3 below the cap top
SCREW = "M5 x 10 button head"                  # 6 - 4 + 3 = 5 under the head -> 5 mm into the bore

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def teardrop(cx, cy, d, apex_dir, z0, z1):
    """Through-hole along z: one wire — a 270° arc plus two 45° tangents meeting at an apex r√2 from the centre in the
    apex_dir = (ax, ay) direction (unit, in-plane). Drawn as one closed sketch so the fuse leaves no arc above the tangents."""
    r = d / 2; ax, ay = apex_dir; px, py = -ay, ax; s = r / math.sqrt(2)
    def P(u, v): return (cx + px * u + ax * v, cy + py * u + ay * v)          # u across, v along the apex direction
    w = (cq.Workplane("XY").workplane(offset=z0).moveTo(*P(s, s)).threePointArc(P(0, -r), P(-s, s))
         .lineTo(*P(0, r * math.sqrt(2))).close().extrude(z1 - z0))
    return w

def regions(c, r):
    """Lower-layer (L) and upper-layer (U) rectangles of tile (col c, row r) in frame x/y, with the end clearances."""
    e = END_CLR / 2; h = LAP / 2
    lx = (PX0, SEAM_X + h - e) if c == 0 else (SEAM_X + h + e, PX1)
    ux = (PX0, SEAM_X - h - e) if c == 0 else (SEAM_X - h + e, PX1)
    ly = (PY0, SEAM_Y + h - e) if r == 0 else (SEAM_Y + h + e, PY1)
    uy = (PY0, SEAM_Y - h - e) if r == 0 else (SEAM_Y - h + e, PY1)
    return (lx, ly), (ux, uy)

def tile(c, r):
    """Tile in frame coords with z 0 = panel underside (frame 510). core = L∩U full thickness; L\\U is the lower
    tongue (z 0–1.5); U\\L the upper tongue (z 1.6–3)."""
    (lx, ly), (ux, uy) = regions(c, r)
    L = box(lx[0], lx[1], ly[0], ly[1], -1, T + 1); U = box(ux[0], ux[1], uy[0], uy[1], -1, T + 1)
    core = box(max(lx[0], ux[0]), min(lx[1], ux[1]), max(ly[0], uy[0]), min(ly[1], uy[1]), 0, T)
    low = box(lx[0], lx[1], ly[0], ly[1], 0, LOWER_T).cut(U)
    up = box(ux[0], ux[1], uy[0], uy[1], LOWER_T + GLUE, T).cut(L)
    t = core
    for piece in (low, up):                    # a corner tile has only one kind of tongue; the other piece is empty
        if piece.solids().vals(): t = t.union(piece)
    # bed edge (front edge y 0 for the front tiles, rear edge y 350 for the rear) chamfered 0.4 on both faces
    t = t.faces("<Y" if r == 0 else ">Y").edges("|X").chamfer(BED_CHAMFER)
    # corner hole over the upright's bore, apex away from the bed edge
    hx = PX0 + HOLE_IN if c == 0 else PX1 - HOLE_IN
    hy = PY0 + HOLE_IN if r == 0 else PY1 - HOLE_IN
    apex = (0, 1) if r == 0 else (0, -1)
    v_far = hy + apex[1] * HOLE_D / 2 * math.sqrt(2)                    # the teardrop apex
    hole = (teardrop(hx - HOLE_SLOT / 2, hy, HOLE_D, apex, -1, T + 1)
            .union(teardrop(hx + HOLE_SLOT / 2, hy, HOLE_D, apex, -1, T + 1))
            .union(box(hx - HOLE_SLOT / 2, hx + HOLE_SLOT / 2, min(hy - HOLE_D / 2, v_far), max(hy + HOLE_D / 2, v_far), -1, T + 1)))
    return t.cut(hole)

def tile_print(c, r):
    """Standing on its front (r 0) or rear (r 1) edge: frame y becomes print z."""
    t = tile(c, r).rotate((0, 0, 0), (1, 0, 0), 90 if r == 0 else -90)
    bb = t.val().BoundingBox(); return t.translate((-bb.xmin, -bb.ymin, -bb.zmin))

def cap():
    c = cq.Workplane("XY").box(CAP_W, CAP_W, CAP_H, centered=(True, True, False)).edges("|Z").fillet(2.0)
    c = c.cut(cq.Workplane("XY").circle(HOLE_D / 2).extrude(CAP_H))
    return c.cut(cq.Workplane("XY").workplane(offset=CAP_H - CAP_CBORE_H).circle(CAP_CBORE_D / 2).extrude(CAP_CBORE_H + 1))

NAMES = {(0, 0): "top-tile-FL", (1, 0): "top-tile-FR", (0, 1): "top-tile-RL", (1, 1): "top-tile-RR"}

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

if __name__ == "__main__":
    import json
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "top")); os.makedirs(OUT, exist_ok=True)

    # ---------------- proofs ----------------
    tiles = {k: tile(*k).translate((0, 0, Z0)) for k in NAMES}
    keys = list(NAMES)
    worst = 0.0
    for i, a in enumerate(keys):
        for b in keys[i + 1:]: worst = max(worst, vol(tiles[a], tiles[b]))
    print(f"four tiles assembled: worst pairwise intersection {worst:.4f} cm3 (0)")
    for k in keys:
        others = [tiles[o] for o in keys if o != k]
        up = max(vol(tiles[k].translate((0, 0, 0.5)), o) for o in others)
        dn = max(vol(tiles[k].translate((0, 0, -0.5)), o) for o in others)
        sx = max(vol(tiles[k].translate((0.3 if k[0] == 0 else -0.3, 0, 0)), o) for o in others)
        sy = max(vol(tiles[k].translate((0, 0.3 if k[1] == 0 else -0.3, 0)), o) for o in others)
        print(f"  {NAMES[k]}: lifted 0.5 {up:.4f} / lowered 0.5 {dn:.4f} (lap engaged: one of these > 0); "
              f"shifted 0.3 along x {sx:.4f} (>0), y {sy:.4f} (>0)")
    panel = tiles[keys[0]]
    for k in keys[1:]: panel = panel.union(tiles[k])
    pb = panel.val().BoundingBox()
    print(f"panel {pb.xmin:.1f}–{pb.xmax:.1f} x {pb.ymin:.1f}–{pb.ymax:.1f} x {pb.zmin:.1f}–{pb.zmax:.1f}")
    # frame + caps + side tiles + scope
    boxes = json.load(open(os.path.join(HERE, "..", "viewer_boxes.json")))
    frame = None
    for (x0, x1, y0, y1, z0, z1, col, grp) in boxes:
        if grp == "frame" and z1 > 400 and 0 <= z0 < 510:      # uprights and top rails (the viewer's caps are replaced here)
            if x0 >= 341: x0, x1 = x0 + (PX1 - 361), x1 + (PX1 - 361)      # right-hand members at the measured width
            if x1 > 300 and x0 < 341: x1 = x1 + (PX1 - 361)                  # the rear cross rail spans the full width
            b = box(x0, x1, y0, y1, z0, min(z1, 510))
            frame = b if frame is None else frame.union(b)
    sidetiles = box(-3, 0, 20, 330, 347, 500).union(box(PX1, PX1 + 3, 20, 330, 347, 500))
    scope = box(23, 338, 3, 111, 355, 507); scope_out = scope.translate((0, -100, 0))
    print(f"panel vs frame {vol(panel, frame):.4f} cm3 (0, sits on it); lowered 0.5 {vol(panel.translate((0, 0, -0.5)), frame):.4f} (>0); "
          f"vs side tiles {vol(panel, sidetiles):.4f} (0)")
    print(f"scope reveal: home {pb.zmin - 507:.1f} mm, pulled out 100 {pb.zmin - 507:.1f} mm; panel vs scope {vol(panel, scope):.4f} / {vol(panel, scope_out):.4f} (0)")
    caps = None
    for (cx, cy) in [(10, 10), (PX1 - 10, 10), (10, 340), (PX1 - 10, 340)]:
        c = cap().translate((cx, cy, Z0 + T))
        caps = c if caps is None else caps.union(c)
        # a Ø4.2 bore pin through the cap and the panel into the upright: 0 against both = the holes line up
        pin = cq.Workplane("XY").workplane(offset=Z0 - 5).center(cx, cy).circle(2.1).extrude(T + CAP_H + 5)
        print(f"  cap at ({cx}, {cy}): vs panel {vol(c, panel):.4f} (0); bore pin vs panel {vol(pin, panel):.4f} / vs cap {vol(pin, c):.4f} (0, 0: holes on the bore)")
    print(f"caps vs frame {vol(caps, frame):.4f} (0)")
    # sag estimate, front edge: a 350-wide 3 mm sheet as a beam clamped at the uprights (321 span), self-weight
    w = 350 * T * 1.27e-3 * 9.81e-3; I = 350 * T ** 3 / 12; E = 2000.0
    print(f"front-edge sag estimate (clamped 321 span, self-weight): {w * 321 ** 4 / (384 * E * I):.2f} mm; simply supported {5 * w * 321 ** 4 / (384 * E * I):.2f} mm")

    # ---------------- parts ----------------
    parts = {NAMES[k]: tile_print(*k) for k in keys}; parts["upright-cap-v1"] = cap()
    layout = {"top-tile-FL": [(0, 0)], "top-tile-FR": [(0, 40)], "top-tile-RL": [(0, 80)], "top-tile-RR": [(0, 120)],
              "upright-cap-v1": [(200, 0), (226, 0), (200, 26), (226, 26)]}
    placed, total, dims = [], 0.0, {}
    for name, p in parts.items():
        bb = p.val().BoundingBox(); p = p.translate((-bb.xmin, -bb.ymin, -bb.zmin))
        fname = f"{name}-v1.stl" if not name.endswith("-v1") else f"{name}.stl"
        path = os.path.join(OUT, fname)
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        v = p.val().Volume() / 1000; dims[name] = (bb.xlen, bb.ylen, bb.zlen, v)
        print(f"{name:16s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f}   {v:6.1f} cm3  x{len(layout[name])}")
        check(path)
        for (x, y) in layout[name]:
            placed.append(p.val().moved(cq.Location(cq.Vector(x, y, 0)))); total += v
    plate = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(OUT, "top-plate-v1.stl")
    cq.exporters.export(plate, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate.val().BoundingBox()
    print(f"\ntop-plate-v1 {pb.xlen:.1f} x {pb.ylen:.1f} x {pb.zlen:.1f} mm, {total:.0f} cm3, {len(placed)} parts "
          f"({'FITS' if pb.xlen <= 250 and pb.ylen <= 250 else 'TOO BIG'} — 250 rule), brims 15 each side of each tile")
    json.dump({"layout": layout, "dims": dims}, open(os.path.join(OUT, "top-plate-layout.json"), "w"))
