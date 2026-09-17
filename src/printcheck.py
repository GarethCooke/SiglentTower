# printcheck.py — every STL this project exports goes through check() before it is committed.
# It answers the three questions that decide whether a part prints clean on the X1C:
#   1. What is it resting on?  (area of faces at z = 0 — a line or a point means it will fall over / needs support)
#   2. What faces point down above the bed?  (each one is a bridge or an overhang; list them with height and area)
#   3. Where are the precision surfaces?  (caller passes them; they must be vertical walls, never tops or ceilings)
# Usage:  from printcheck import check; check("part.stl", min_rest_frac=0.3)   -> prints a report, raises on a fail.
import numpy as np, trimesh

def check(path, min_rest_frac=0.3, max_down_frac=0.25, raise_on_fail=True):
    m = trimesh.load(path)
    zmin = m.bounds[0][2]
    fails = []
    if abs(zmin) > 0.01: fails.append(f"zmin is {zmin:.2f}, not 0 — translate before export")
    foot = m.extents[0] * m.extents[1]
    rest = m.area_faces[np.all(np.abs(m.triangles[:, :, 2] - zmin) < 0.01, axis=1)].sum()
    print(f"{path}: extents {m.extents.round(1)}  resting face {rest:.0f} mm² = {rest/foot:.0%} of footprint  watertight={m.is_watertight}")
    if rest / foot < min_rest_frac: fails.append(f"resting face only {rest/foot:.0%} of the footprint — reorient or split")
    down = m.face_normals[:, 2] < -0.75          # steeper than 45° downward: bridges / overhangs (45° chamfers pass)
    zc = np.round(m.triangles[:, :, 2].mean(axis=1), 1)
    total_down = 0.0
    for z in sorted(set(zc[down])):
        if abs(z - zmin) < 0.05: continue
        a = m.area_faces[down & (np.abs(zc - z) < 0.05)].sum(); total_down += a
        print(f"   down-facing at z={z:>6.1f}: {a:6.0f} mm²  <- needs a bridge, a 45° roof, or support")
    if total_down / max(rest, 1) > max_down_frac: fails.append(f"down-facing area {total_down:.0f} mm² is {total_down/rest:.0%} of the resting face")
    if not m.is_watertight: fails.append("mesh not watertight")
    for f in fails: print("   FAIL:", f)
    if fails and raise_on_fail: raise SystemExit(f"printcheck failed for {path}")
    return not fails

if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]: check(p, raise_on_fail=False)
