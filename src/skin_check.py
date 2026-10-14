# skin_check.py — the side skin assembled against the frame AS MEASURED (side_tile.GAPS) with the cradle saddles that
# stand on the left rails: every tile vs its rails (fingers inside the outer slot, nothing else touching), vs the saddle
# walls (v2's notches), tiles sharing a slot vs each other (interleaved fingers), and each tile pulled 0.5 off the rail
# face (the barbs hook the lips). Right side: band 2 is the v1 tile at the model height.
# python src/skin_check.py
import os, sys, cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "parts"))
from fit import SLOT_MOUTH, SLOT_LIP_T, SLOT_CAVITY_W, SLOT_THROAT_D, SLOT_DEPTH, SLOT_BOTTOM_W, RAIL_CLR
import side_tile as st

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def rail_with_outer_slot(y0, y1, z0, z1):
    """Rail x 0–20 (outer face at x 0) with the outer slot cut; the other three slots do not matter here."""
    r = box(0, 20, y0, y1, z0, z1)
    zc = (z0 + z1) / 2
    hm, hc, hb = SLOT_MOUTH / 2, SLOT_CAVITY_W / 2, SLOT_BOTTOM_W / 2
    pts = [(-1, zc - hm), (SLOT_LIP_T, zc - hm), (SLOT_LIP_T, zc - hc), (SLOT_THROAT_D, zc - hc), (SLOT_DEPTH, zc - hb),
           (SLOT_DEPTH, zc + hb), (SLOT_THROAT_D, zc + hc), (SLOT_LIP_T, zc + hc), (SLOT_LIP_T, zc + hm), (-1, zc + hm)]
    void = cq.Workplane("XZ").polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))
    return r.cut(void)

def vol(a, b):
    try: return a.intersect(b).val().Volume() / 1000
    except Exception: return 0.0

def side(sidetag):
    g = st.GAPS[sidetag]
    z = {"base": (0.0, 20.0)}
    z["psu"] = (20.0 + g[1], 40.0 + g[1]); z["awg"] = (z["psu"][1] + g[2], z["psu"][1] + g[2] + 20)
    z["scope"] = (z["awg"][1] + g[3], z["awg"][1] + g[3] + 20)
    rails = {k: rail_with_outer_slot(20, 330, *v) for k, v in z.items()}
    cl = {k: (v[0] + v[1]) / 2 for k, v in z.items()}
    P = st.production()
    if sidetag == "R": P.update(st.production_v1_right_band2())
    # saddles (left only): U walls 3 thick outside the rail face, rail top - 6 to rail top + 8 (Gareth: ~10)
    sad = []
    if sidetag == "L":
        for (a, b) in st.PSU_SADDLES: sad.append(box(-3.2, -0.2, a, b, z["psu"][1] - 6, z["psu"][1] + 10))
        for (a, b) in st.AWG_SADDLES: sad.append(box(-3.0, -0.2, a, b, z["awg"][1] - 6, z["awg"][1] + 10))
    # placement: (name, frame y of local 0, direction, band)
    if sidetag == "L":
        place = [("tile-band1-LF", 20, 1, 1), ("tile-band1-LR", 175, 1, 1), ("tile-band2-LF", 20, 1, 2), ("tile-band2-LR", 175, 1, 2),
                 ("tile-band3-LF", 20, 1, 3), ("tile-band3-LR", 175, 1, 3)]
    else:
        place = [("tile-band1-R", 175, -1, 1), ("tile-band1-R", 330, -1, 1), ("tile-band2-RF", 175, -1, 2), ("tile-band2-RR", 330, -1, 2),
                 ("tile-band3-RF", 175, -1, 3), ("tile-band3-RR", 330, -1, 3)]
    placed = []
    for name, y0, d, band in place:
        zlo = cl[st.BANDS[band][0]]
        t = P[name]
        # right tiles are turned 180 about z on the frame; seen in the rail's own frame (outer face at x 0) that is a mirror in y
        t = (t.mirror("XZ") if d < 0 else t).translate((0, y0, zlo))
        placed.append((name, band, t))
    return rails, sad, placed, cl

if __name__ == "__main__":
    for sidetag in ("L", "R"):
        rails, sad, placed, cl = side(sidetag)
        print(f"== {sidetag} side, slot centrelines {', '.join(f'{k} {v:.1f}' for k, v in cl.items())}")
        worst_rail = worst_sad = worst_pair = 0.0; hold_min = 1e9
        for name, band, t in placed:
            rv = sum(vol(t, r) for r in rails.values())
            sv = sum(vol(t, s) for s in sad)
            hold = sum(vol(t.translate((-0.5, 0, 0)), r) for r in rails.values())   # pulled off the face: barbs vs lips
            worst_rail = max(worst_rail, rv); worst_sad = max(worst_sad, sv); hold_min = min(hold_min, hold)
            print(f"  {name:14s} band {band}: vs rails {rv:.4f} cm3, vs saddles {sv:.4f}, pulled 0.5 off the face {hold:.4f} (>0 = held)")
        for i, (n1, b1, t1) in enumerate(placed):
            for (n2, b2, t2) in placed[i + 1:]:
                v = vol(t1, t2); worst_pair = max(worst_pair, v)
                if v > 1e-6: print(f"  CLASH {n1} x {n2}: {v:.4f} cm3")
        print(f"  worst: vs rails {worst_rail:.4f}, vs saddles {worst_sad:.4f}, tile-tile {worst_pair:.4f} (all 0); weakest hold {hold_min:.4f} (>0)")
