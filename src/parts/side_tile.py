# Side tiles — the hex panels that clip into the rails' outer slots (HANDOVER §5, D4, gated by P4 ☑).
# v1 2026-09-22.
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


def band_height(n):
    lo, hi = BANDS[n]
    return CENTRELINES[hi] - (CENTRELINES[lo] if lo else 347.0)


def hex_holes(length, height):
    """The viewer's pattern: pointy-top hexes, HEX_R across corners, staggered rows."""
    cuts = []
    z = BORDER_Z + HEX_R
    row = 0
    while z < height - BORDER_Z - HEX_R + 0.01:
        y = BORDER_Y + HEX_R + (HEX_DX / 2 if row % 2 else 0.0)
        while y < length - BORDER_Y - HEX_R + 0.01:
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


def tile(length, height, roots_lo, roots_hi, notches_lo=(), notches_hi=(), open_hi=False):
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
    h = hex_holes(length, height)
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
    print("band heights (centreline to centreline): " + ", ".join(f"{n}={band_height(n):.1f}" for n in BANDS))
