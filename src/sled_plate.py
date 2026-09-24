# sled_plate.py — one black ABS+ plate for the whole sled slide: four beam halves flat + two 210 feet standing
# (parts/sled-absplus-plate.stl). Run after parts/sled_beam.py and parts/sled_foot.py. Bed 256 x 256; the layout below
# is 245 x 206. Feet stand on two narrow edges and want a brim; the beams' groove mouths and tab flanks are fit surfaces
# on the bed, so slice with the brim OUTER ONLY (5 mm) and trim it off the tab flanks before assembly.
import os, trimesh, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.normpath(os.path.join(HERE, "..", "parts"))
GAP = 5.0
layout = [("sled-beam-left-front-v1", 0, 0), ("sled-beam-right-front-v1", 75.5 + GAP, 0),
          ("sled-beam-left-rear-v1", 2 * (75.5 + GAP), 0), ("sled-beam-right-rear-v1", 2 * (75.5 + GAP) + 39.5 + GAP, 0),
          ("sled-foot-210", 0, 169 + GAP + 1), ("sled-foot-210", 0, 169 + GAP + 1 + 13.1 + GAP)]
meshes = []
for name, dx, dy in layout:
    m = trimesh.load(os.path.join(PARTS, f"{name}.stl")); m.apply_translation(-m.bounds[0]); m.apply_translation([dx, dy, 0]); meshes.append(m)
plate = trimesh.util.concatenate(meshes)
out = os.path.join(PARTS, "sled-absplus-plate.stl"); plate.export(out)
print(f"{out}: {plate.extents.round(1)} mm, {plate.volume / 1000:.0f} cm3 solid, {len(meshes)} parts")
assert plate.extents[0] <= 250 and plate.extents[1] <= 250, "does not fit the bed"
