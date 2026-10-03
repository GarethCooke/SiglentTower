# cradle_plate.py — the 2026-10-02 cradle reprint on one plate (parts/cradles-v2-plate.stl): 2 × PSU right v4 (cup face down,
# sacrificial layer over the cup and counterbores), 2 × AWG left v2 (standing on end), 2 × AWG right v2 (arm-top down). Black ABS.
import os, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.normpath(os.path.join(HERE, "..", "parts"))
items = [("psu-cradle-right-v4", 2), ("awg-cradle-left-v2", 2), ("awg-cradle-right-v2", 2)]   # as printed 2026-10-03; the right FRONT PSU cradle is then replaced by v5
meshes, x, y, row_h, GAP = [], 0.0, 0.0, 0.0, 8.0          # two rows: PSU cradles in the back row, AWG parts in the front
for name, n in items:
    for i in range(n):
        m = trimesh.load(os.path.join(PARTS, f"{name}.stl")); m.apply_translation(-m.bounds[0])
        if x + m.extents[0] > 240: x, y, row_h = 0.0, y + row_h + GAP, 0.0
        m.apply_translation([x, y, 0]); meshes.append(m); x += m.extents[0] + GAP; row_h = max(row_h, m.extents[1])
plate = trimesh.util.concatenate(meshes); plate.export(os.path.join(PARTS, "cradles-v2-plate.stl"))
print(f"plate {plate.extents.round(1)}  {plate.volume/1000:.1f} cm3  {'fits' if plate.extents[0] <= 250 and plate.extents[1] <= 250 else 'TOO BIG'}")
