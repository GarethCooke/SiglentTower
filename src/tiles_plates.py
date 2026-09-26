# tiles_plates.py — the six black PETG side-tile plates (parts/tiles/tiles-plate-A..F.stl), from the production tiles that
# parts/side_tile.py exports. Every tile face down as exported, no brim, no support, SiglentTower fit 0.20.
#   A: band2-LF + band1     B: band2-LR + band1     C: band3-LF + band3-LR      (left side complete after A-C)
#   D: band2-RF + band1     E: band2-RR + band1     F: band3-RF + band3-RR      (right side)
# Band-1 tiles are identical on both sides; the right-side band 2/3 tiles are the left ones turned 180 about z with their
# windows placed for that orientation — mount them local-y rearward (see side_tile.py).
import os, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); TILES = os.path.normpath(os.path.join(HERE, "..", "parts", "tiles"))
GAP = 8.0
PLATES = {"A": ("tile-band2-LF", "tile-band1"), "B": ("tile-band2-LR", "tile-band1"), "C": ("tile-band3-LF", "tile-band3-LR"),
          "D": ("tile-band2-RF", "tile-band1"), "E": ("tile-band2-RR", "tile-band1"), "F": ("tile-band3-RF", "tile-band3-RR")}
for tag, names in PLATES.items():
    meshes, x = [], 0.0
    for n in names:
        m = trimesh.load(os.path.join(TILES, f"{n}-v1.stl")); m.apply_translation(-m.bounds[0]); m.apply_translation([x, 0, 0])
        meshes.append(m); x += m.extents[0] + GAP
    plate = trimesh.util.concatenate(meshes); out = os.path.join(TILES, f"tiles-plate-{tag}.stl"); plate.export(out)
    ok = plate.extents[0] <= 250 and plate.extents[1] <= 250
    print(f"plate {tag}: {' + '.join(names):32s} {plate.extents.round(1)}  {plate.volume/1000:5.1f} cm3  {'fits' if ok else 'TOO BIG'}")
    assert ok
