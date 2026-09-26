# yellow_run_plate.py — the yellow PETG check plate, rebuilt 2026-09-25 from the regenerated parts after the geometry
# review (coupons/yellow-run/yellow-run-2026-09-25.stl): band-1 tile + band-2 crop (face down, shared edges facing each
# other), hinge door + frame leaves (standing), strip brackets upper + lower (plate face down). Everything as exported,
# no brim, no support. Run after parts/side_tile.py, parts/door_hinge.py and parts/strip_bracket.py.
import os, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "coupons", "yellow-run"); os.makedirs(OUT, exist_ok=True)
GAP = 8.0
items = [("coupons/p4/tile-band2-crop.stl", 0, 0), ("coupons/p4/tile-band1-155.stl", 62.8 + GAP, 0),   # band 2 first: its shared edge (x-max) faces band 1's (x-min)
         ("parts/strip-bracket-lower-v1.stl", 0, 155 + GAP), ("parts/strip-bracket-upper-v1.stl", 80 + GAP, 155 + GAP),
         ("parts/hinge-door-v1.stl", 80 + GAP + 34.2 + GAP, 155 + GAP), ("parts/hinge-frame-v1.stl", 80 + GAP + 34.2 + GAP + 19 + GAP, 155 + GAP)]
meshes = []
for rel, dx, dy in items:
    m = trimesh.load(os.path.join(ROOT, rel)); m.apply_translation(-m.bounds[0]); m.apply_translation([dx, dy, 0]); meshes.append(m)
    print(f"{rel:40s} {m.extents.round(1)}  {m.volume/1000:5.1f} cm3")
plate = trimesh.util.concatenate(meshes)
out = os.path.join(OUT, "yellow-run-2026-09-25.stl"); plate.export(out)
print(f"{out}: {plate.extents.round(1)} mm, {plate.volume/1000:.0f} cm3, {len(meshes)} parts")
assert plate.extents[0] <= 250 and plate.extents[1] <= 250
