# Side tiles — the hex panels that clip into the rails' outer slots (HANDOVER §5, D4, gated by P4 ☑).
# v1 2026-09-22; production set 2026-09-26 (windows for the cradle lips and the hinge plates, left/right variants —
# see production() and the note at the end of this header).
#
# BAND HEIGHTS ARE NOT THE VIEWER'S. `bench-stack-3d.html` draws the tiles between the rails (20–68, 88–227.5,
# 247.5–311, 347–490) and ROADMAP §8's bed-fit audit copies those numbers. But `slot_clip.py` — the geometry P4 passed
# — puts each tile's edge ON the rail's slot centreline, with the two tiles that meet there sharing the slot, the upper
# one hooking the upper lip and the lower one the lower lip. A tile that stopped at the rail's inner face would have to
# reach 10 mm to get a barb into the slot; the clip's finger straddles its edge by 2.25. So the tiles run CENTRELINE TO
# CENTRELINE and cover the rails. Rail centrelines: base 10, PSU 78, AWG 237.5, scope 321, top 500.
#   band 1   z  10  –  78    68.0 tall      band 3   z 237.5 – 321     83.5
#   band 2   z  78  – 237.5  159.5          band 4   z 347   – 500    153.0  (see below)
# Each band is two tiles of 155 along y (D4), y 20–175 and 175–330.
# Band 4 is the odd one: the sled band 331–346 is left open, so that tile's BOTTOM edge has no rail to clip to — it can
# only hang from the top rail at 500. On the right side it is the fold-down door and the fixed rear tile, which are
# held by the hinge and the magnets instead, so this only bites on the LEFT side and is left open here.
#
# Print: face down, textured plate against the visible face (PRINT-RULES §2). Clips rise from the back; the barb's
# underside is CLIP_HOOK_DEG, its ramp 45°. No support.
#
# Solid border is 4 mm along y (the short edges) and 5 mm at the clip edges: at 4 the hex grid's first row clips the
# U-slit by 0.25, and the slit is what makes the spring work.
#
# THINGS ON THE RAIL FACES (2026-09-26, found by assembling the whole skin in CadQuery): the PSU and left-AWG cradle
# saddles wrap their rails with 3 mm lips that hang 6 mm down the OUTER face — exactly where the tile lies — and the
# door hinge's frame leaves are 6 mm plates on the right scope rail's outer face. The tiles that meet them carry
# through-windows (see production()); the assembled skin — 12 tiles, 8 rails, 6 lips, 2 hinge plates — intersects
# nowhere, and every tile stays one solid.
import os, sys, math, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, HERE)
from fit import CLIP_T, SLOT_MOUTH
import slot_clip as sc

T        = CLIP_T          # 3.0
BORDER_Y = 4.0             # solid border on the short (y) edges
BORDER_Z = 5.0             # at the clip edges — keeps the hex grid off the U-slit
HEX_R    = 4.2             # across corners 8.4 (HANDOVER §5)
HEX_DX   = 2 * HEX_R + 2.5
HEX_DY   = HEX_DX * 0.866
TILE_L   = 155.0           # D4
NOTCH_D  = 2.8             # neighbour notch: the clip finger dips 2.25 past the edge, plus clearance
NOTCH_PAD = 1.0            # y either side of the neighbour's finger

CENTRELINES = {"base": 10.0, "psu": 78.0, "awg": 237.5, "scope": 321.0, "top": 500.0}
BANDS = {1: ("base", "psu"), 2: ("psu", "awg"), 3: ("awg", "scope"), 4: (None, "top")}

# v2 (2026-10-14): THE RAILS ARE NOT WHERE THE SPACERS PUT THEM. Gareth's calipers, rail face to rail face, per side:
#   gap                     model   left   right
#   base top -> PSU under    48     51.2   45.4
#   PSU top -> AWG under    139.5  135.0  139.5
#   AWG top -> scope under   63.5   65.5   65.8
#   scope top -> top under  159    157    158     (band 4 hangs from the top rail only; not modelled)
# A band is centreline to centreline = gap + 20, and a tile's height has to match that to ~0.2 (the finger's root stub
# fills the slot mouth), so every band now has a height PER SIDE and the tiles are left/right parts. Band 2 right is
# unchanged (139.5) and its v1 tiles stay; everything else reprints as v2.
GAPS = {"L": {1: 51.2, 2: 135.0, 3: 65.5}, "R": {1: 45.4, 2: 139.5, 3: 65.8}}


def band_height(n, side=None):
    if side is None:                                   # model (spacer) heights — the v1 tiles and the coupons
        lo, hi = BANDS[n]
        return CENTRELINES[hi] - (CENTRELINES[lo] if lo else 347.0)
    return GAPS[side][n] + 20.0


def hex_holes(length, height, keep=(), web=1.5):
    """The viewer's pattern: pointy-top hexes, HEX_R across corners, staggered rows. `keep` = (y0, y1, z0, z1) windows
    that get a solid border: any hex within `web` of one is left out, so a window never leaves a hex sliver."""
    cuts = []
    z = BORDER_Z + HEX_R
    row = 0
    while z < height - BORDER_Z - HEX_R + 0.01:
        y = BORDER_Y + HEX_R + (HEX_DX / 2 if row % 2 else 0.0)
        while y < length - BORDER_Y - HEX_R + 0.01:
            near = any(y + HEX_R + web > y0 and y - HEX_R - web < y1 and z + HEX_R + web > z0 and z - HEX_R - web < z1
                       for (y0, y1, z0, z1) in keep)
            if not near:
                pts = [(y + HEX_R * math.cos(math.pi / 6 + k * math.pi / 3),
                        z + HEX_R * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
                cuts.append(pts)
            y += HEX_DX
        z += HEX_DY; row += 1
    if not cuts:
        return None
    wp = cq.Workplane("YZ").workplane(offset=-T - 1)
    for pts in cuts:
        wp = wp.polyline(pts).close()
    return wp.extrude(T + 2)


def plate(length, height):
    return cq.Workplane("XY").box(T, length, height, centered=False).translate((-T, 0, 0))


def notch(y_lo, y_hi):
    """Relief in this tile's edge for the neighbour's finger, which dips NOTCH_D past the shared centreline."""
    return sc.box(-T - 1, 1, y_lo - NOTCH_PAD, y_hi + NOTCH_PAD, -1, NOTCH_D)


def tile(length, height, roots_lo, roots_hi, notches_lo=(), notches_hi=(), open_hi=False, cutouts=(), hexes=True):
    """Tile in slot_clip's frame: face at x = -T, back at 0, y along the rail, z across it with z = 0 the LOWER shared
    slot centreline and z = height the upper one. `roots_*` are finger roots on each edge (all running +y); `notches_*`
    are the NEIGHBOUR's finger spans on that edge, relieved. `open_hi` leaves the top edge plain.

    Order matters: an edge's own fingers go on FIRST and its notches are cut LAST, because where the two overlap the
    neighbour's finger physically needs the space. They must not overlap at all, which the assert below enforces — v1
    cut the notch first and then re-filled it with its own finger, so the neighbour had no relief."""
    for r in roots_lo:
        for n0, n1 in notches_lo:
            assert r + sc.FINGER_L <= n0 - NOTCH_PAD or r >= n1 + NOTCH_PAD, \
                f"lower-edge finger at {r} overlaps the neighbour's {n0}-{n1}: they would occupy the same slot"
    for r in roots_hi:
        for n0, n1 in notches_hi:
            assert r + sc.FINGER_L <= n0 - NOTCH_PAD or r >= n1 + NOTCH_PAD, \
                f"upper-edge finger at {r} overlaps the neighbour's {n0}-{n1}: they would occupy the same slot"
    t = plate(length, height)
    h = hex_holes(length, height, keep=cutouts) if hexes else None
    if h is not None:
        t = t.cut(h)
    for r in roots_lo:
        t = sc.add_finger(t, r, +1)
    t = t.mirror("XY", (0, 0, height / 2))          # top edge becomes the z = 0 edge
    if not open_hi:
        for r in roots_hi:
            t = sc.add_finger(t, r, +1)
    for y0, y1 in notches_hi:
        t = t.cut(notch(y0, y1))
    t = t.mirror("XY", (0, 0, height / 2))
    for y0, y1 in notches_lo:
        t = t.cut(notch(y0, y1))
    for y0, y1, z0, z1 in cutouts:                       # through-windows for things that sit on the rail face (cradle lips, hinge plates)
        t = t.cut(sc.box(-T - 1, 1, y0, y1, z0, z1))
    return t


def printable(t):
    """Face down: the tile's visible face (x = -T) goes on the textured plate, clips rise. x -> z."""
    p = t.rotate((0, 0, 0), (0, 1, 0), -90)
    bb = p.val().BoundingBox()
    return p.translate((-bb.xmin, -bb.ymin, -bb.zmin))


# ---- clip layout on a SHARED rail ----
# Two tiles meeting on one slot centreline both put material past that line: slot_clip's finger strip runs the finger's
# whole 30 mm and dips 2.25 into the neighbour. So their fingers cannot overlap in y AT ALL — it is not enough to
# stagger the pegs. v1 put three on one edge and two on the other and they collided; at 155 long, 30 per finger plus a
# slit and a little air means two per tile per shared edge, interleaved.
SHARE_A = (6.0, 84.0)        # band 1's top edge
SHARE_B = (43.0, 121.0)      # band 2's bottom edge, dropped between them
BASE_ROOTS = (10.0, 62.0, 114.0)   # band 1's bottom edge sits on the BASE rail with no partner, so it can have three


def spans(roots):
    return tuple(sc.finger_span(r, +1) for r in roots)


# ---- production set v2 (2026-10-14; v1 2026-09-26) ----
# Left tiles have local y = frame y - 20 (front tile) or - 175 (rear tile). RIGHT tiles are the left ones turned 180 about z
# to face outward, so their local y runs REARWARD: local = 175 - frame y (front) or 330 - frame y (rear).
#
# WINDOWS, v2: the cradle saddles are U-channels round the rail — LIP_T 3 walls, LIP_H 6 below the rail top AND TOP_T 8
# above it (psu_cradle.py / awg_cradle.py). v1 cut windows for the 6 mm lips only (local z 3.5–10.5) and the printed
# band-2 and band-3 left tiles hit the walls above the rail top. Gareth measured the saddles standing 10 above the rail
# top, so v2's windows are NOTCHES open to the tile's bottom edge, up to local z 21 (rail top 10 + 10 + 1), and the hex
# grid keeps a 1.5 web round them. Saddle positions along the rail are the model's (the seating jigs set them from the
# front upright: PSU feet at frame y 51 / 253.5 -> saddles 31–71 / 233.5–273.5; AWG left saddles 20–60 / 223–263),
# with 4 mm of air at each end. Only the LEFT rails carry saddles: the right PSU cradles sit on the inner rail and the
# right AWG cradles are brackets on it, so the right tiles have no windows (v1's right band-2 PSU windows were harmless
# holes for nothing; band 2 right keeps v1 anyway). The hinge plates on the right scope rail are as v1.
#
# FINGERS, v2: a finger rooted inside a notch would hang off nothing, so on the left every shared edge is re-scheduled
# round the notches — the lower tile's fingers stay out of its notches (with the 1 mm pad), the upper tile's fingers
# interleave with them. The right side keeps v1's SHARE_A / SHARE_B schedule (band 2 right is a v1 tile).
SADDLE_Z = (-1.0, 21.0)
def win(y0, y1, z0, z1): return (max(y0, -1.0), min(y1, TILE_L + 1.0), z0, z1)
PSU_SADDLES = ((31.0, 71.0), (233.5, 273.5)); AWG_SADDLES = ((20.0, 60.0), (223.0, 263.0)); HINGES = ((23.0, 47.0), (223.0, 247.0))
SADDLE_CLR = 4.0
def local_front_L(y): return y - 20.0
def local_rear_L(y): return y - 175.0
def local_front_R(y): return 175.0 - y
def local_rear_R(y): return 330.0 - y
def windows(spans, to_local, z0, z1, clr=1.0):
    out = []
    for a, b in spans:
        la, lb = sorted((to_local(a), to_local(b)))
        if lb < 0 or la > TILE_L: continue
        out.append(win(la - clr, lb + clr, z0, z1))
    return tuple(out)

# left-side finger roots per shared slot (local y, fingers run +y, 30 long): (lower tile's bottom-edge roots, upper tile's top-edge roots)
#   PSU slot, front: notch 7–55   -> band 2 bottom 56 / 121, band 1 top 6 / 88
#   PSU slot, rear:  notch 54.5–102.5 -> band 2 bottom 6 / 104, band 1 top 38 / 70
#   AWG slot, front: notch -1–44  -> band 3 bottom 46 / 121, band 2 top 6 / 78
#   AWG slot, rear:  notch 44–92  -> band 3 bottom 6 / 121,  band 2 top 38 / 70
L_PSU = {"F": ((56.0, 121.0), (6.0, 88.0)), "R": ((6.0, 104.0), (38.0, 70.0))}
L_AWG = {"F": ((46.0, 121.0), (6.0, 78.0)), "R": ((6.0, 121.0), (38.0, 70.0))}

def production():
    H1L, H2L, H3L = band_height(1, "L"), band_height(2, "L"), band_height(3, "L")
    H1R, H3R = band_height(1, "R"), band_height(3, "R")
    hz = (H3R - 10.0 - 0.5, H3R + 1.0)                   # hinge plate window: the tile's top 10 mm (+0.5)
    P = {}
    # LEFT
    for tag, f in (("F", local_front_L), ("R", local_rear_L)):
        psu_lo, psu_hi = L_PSU[tag]; awg_lo, awg_hi = L_AWG[tag]
        P[f"tile-band1-L{tag}"] = tile(TILE_L, H1L, roots_lo=BASE_ROOTS, roots_hi=psu_hi, notches_hi=spans(psu_lo))
        P[f"tile-band2-L{tag}"] = tile(TILE_L, H2L, roots_lo=psu_lo, roots_hi=awg_hi, notches_lo=spans(psu_hi),
                                       notches_hi=spans(awg_lo), cutouts=windows(PSU_SADDLES, f, *SADDLE_Z, clr=SADDLE_CLR))
        P[f"tile-band3-L{tag}"] = tile(TILE_L, H3L, roots_lo=awg_lo, roots_hi=BASE_ROOTS, notches_lo=spans(awg_hi),
                                       cutouts=windows(AWG_SADDLES, f, *SADDLE_Z, clr=SADDLE_CLR))
    # RIGHT (band 2 right = v1 tiles, schedule SHARE_B bottom / SHARE_A top, unchanged)
    P["tile-band1-R"] = tile(TILE_L, H1R, roots_lo=BASE_ROOTS, roots_hi=SHARE_A, notches_hi=spans(SHARE_B))
    P["tile-band3-RF"] = tile(TILE_L, H3R, roots_lo=SHARE_B, roots_hi=SHARE_A, notches_lo=spans(SHARE_A),
                              cutouts=windows(HINGES, local_front_R, *hz, clr=0.5))           # hinge at local 127.5-152.5
    P["tile-band3-RR"] = tile(TILE_L, H3R, roots_lo=SHARE_B, roots_hi=(6.0, 118.0), notches_lo=spans(SHARE_A),
                              cutouts=windows(HINGES, local_rear_R, *hz, clr=0.5))            # hinge at local 82.5-107.5
    return P


def production_v1_right_band2():
    """The two right band-2 tiles as printed (v1, model height 159.5) — kept for the skin check only."""
    return {f"tile-band2-R{tag}": tile(TILE_L, band_height(2), roots_lo=SHARE_B, roots_hi=SHARE_A, notches_lo=spans(SHARE_A),
                                       notches_hi=spans(SHARE_B), cutouts=windows(PSU_SADDLES, f, 3.5, 10.5))
            for tag, f in (("F", local_front_R), ("R", local_rear_R))}


# ---- band-height test strips (2026-10-12) ----
# Gareth, right side, band 3: the printed tile's top tabs sit with their tops level with the BOTTOM of the scope rail's
# slot — the tile is short by several mm on that side (the left is fine). Before reprinting tiles, a strip tests the
# height: 3 mm, STRIP_W wide along the rail (one 30 mm finger plus its slit and a border — a clip cannot be narrower),
# one finger on each edge, no hexes (rule 9), the height added stamped on the back (rule 11). Clip the bottom finger
# into the AWG rail's slot where the band-3 tile's own tabs went (between the band-2 tile's top tabs), push the top
# finger into the scope rail's slot: the winner snaps in at both edges and sits flat. Try it at the front and the rear of
# the band — if different strips win there, the rail is tilted, not just high.
STRIP_W = 42.0
STRIP_ROOT = 6.0                              # finger y 6-36, slit to 37, 5 mm border beyond it

def test_strip(band, extra):
    return tile(STRIP_W, band_height(band) + extra, roots_lo=(STRIP_ROOT,), roots_hi=(STRIP_ROOT,), hexes=False)

def stamp_back(p, text, size=5.0, depth=0.5):
    """Deboss into the tile's back (the print's top face at z = T); the fingers and pegs stand above it, so pass z."""
    bb = p.val().BoundingBox()
    cut = (cq.Workplane("XY").workplane(offset=T - depth).center((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2)
           .text(text, size, depth + 1, combine=False, halign="center", valign="center"))
    return p.cut(cut)

def band_sweep(band, extras, out_dir, name):
    from printcheck import check
    os.makedirs(out_dir, exist_ok=True)
    placed, x, total = [], 0.0, 0.0
    for e in extras:
        p = stamp_back(printable(test_strip(band, e)), f"+{e:g}")
        bb = p.val().BoundingBox(); path = os.path.join(out_dir, f"strip-band{band}-plus{e:g}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        v = p.val().Volume() / 1000; total += v
        print(f"strip band {band} +{e:g}: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {v:.1f} cm3  (height {band_height(band) + e:.1f})")
        check(path, min_rest_frac=0.25, max_down_frac=0.25)
        placed.append(p.val().moved(cq.Location(cq.Vector(0, x, 0)))); x += bb.ylen + 8.0      # stacked along y: 95 x 142
    plate_all = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(out_dir, f"{name}.stl"); cq.exporters.export(plate_all, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate_all.val().BoundingBox()
    print(f"{name}: {pb.xlen:.0f} x {pb.ylen:.0f} x {pb.zlen:.1f} mm, {total:.1f} cm3, face down as exported, no brim, no support")


if __name__ == "__main__" and "--band3-sweep" in sys.argv:
    band_sweep(3, (4, 5, 6), os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p4")), "band3-right-sweep")
    sys.exit(0)

if __name__ == "__main__":
    from printcheck import check
    OUT = os.path.normpath(os.path.join(HERE, "..", "..", "coupons", "p4")); os.makedirs(OUT, exist_ok=True)
    H1, H2 = band_height(1), 60.0          # band 1 full; band 2 cropped to 60 — enough to carry its edge and the hexes
    parts = {
        # band 2 first, so on the plate the two SHARED edges face each other across the gap and the interleave is
        # obvious at a glance (band 1's shared edge lands at its x-min, band 2's at its x-max)
        "tile-band2-crop": tile(TILE_L, H2, roots_lo=SHARE_B, roots_hi=(),
                                notches_lo=spans(SHARE_A), open_hi=True),
        "tile-band1-155": tile(TILE_L, H1, roots_lo=BASE_ROOTS, roots_hi=SHARE_A,
                               notches_hi=spans(SHARE_B)),
    }
    placed, x, total = [], 0.0, 0.0
    for name, t in parts.items():
        p = printable(t)
        bb = p.val().BoundingBox()
        path = os.path.join(OUT, f"{name}.stl")
        cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        v = p.val().Volume() / 1000; total += v
        print(f"{name:18s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {v:5.1f} cm3")
        check(path, min_rest_frac=0.25, max_down_frac=0.25)
        placed.append(p.val().moved(cq.Location(cq.Vector(x, 0, 0)))); x += bb.xlen + 8.0
    plate_all = cq.Workplane("XY").newObject([cq.Compound.makeCompound(placed)])
    pp = os.path.join(OUT, "p4-tiles-plate.stl")
    cq.exporters.export(plate_all, pp, tolerance=0.01, angularTolerance=0.1)
    pb = plate_all.val().BoundingBox()
    print(f"\np4-tiles-plate {pb.xlen:.0f} x {pb.ylen:.0f} x {pb.zlen:.0f} mm, {total:.1f} cm3 "
          f"({'FITS' if pb.xlen < 250 and pb.ylen < 250 else 'TOO BIG'} the 256 bed)")
    print("band heights (centreline to centreline), model: " + ", ".join(f"{n}={band_height(n):.1f}" for n in BANDS)
          + "; LEFT " + ", ".join(f"{n}={band_height(n, 'L'):.1f}" for n in (1, 2, 3))
          + "; RIGHT " + ", ".join(f"{n}={band_height(n, 'R'):.1f}" for n in (1, 2, 3)))
    # production tiles -> parts/tiles/ (black PETG, face down as exported; plates in src/tiles_plates.py)
    POUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts", "tiles")); os.makedirs(POUT, exist_ok=True)
    for name, t in production().items():
        p = printable(t); bb = p.val().BoundingBox()
        path = os.path.join(POUT, f"{name}-v2.stl"); cq.exporters.export(p, path, tolerance=0.01, angularTolerance=0.1)
        print(f"{name:16s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}   {p.val().Volume()/1000:5.1f} cm3")
        check(path, min_rest_frac=0.25, max_down_frac=0.25)
