# tiles_plates.py — the black PETG side-tile plates (parts/tiles/tiles-plate-*.stl), from the production tiles that
# parts/side_tile.py exports. Every tile face down as exported, no brim, no support, SiglentTower fit 0.20.
# v2 (2026-10-14, rails as measured — side_tile.GAPS): A2: band2-LF + band1-LF   B2: band2-LR + band1-LR   C2: band3-LF + band3-LR
#   D2: band3-RF + band1-R   E2: band3-RR + band1-R.  Band 2 RIGHT keeps the v1 tiles (plates D/E of v1) — its gap is unchanged.
# v1 (2026-09-26, spacer heights, all printed by 09-28): A: band2-LF + band1  B: band2-LR + band1  C: band3-LF + band3-LR
#   D: band2-RF + band1  E: band2-RR + band1  F: band3-RF + band3-RR — withdrawn except D/E's band-2 tiles.
import os, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); TILES = os.path.normpath(os.path.join(HERE, "..", "parts", "tiles"))
GAP = 8.0
PLATES = {"A2": ("tile-band2-LF-v2", "tile-band1-LF-v2"), "B2": ("tile-band2-LR-v2", "tile-band1-LR-v2"),
          "C2": ("tile-band3-LF-v2", "tile-band3-LR-v2"), "D2": ("tile-band3-RF-v2", "tile-band1-R-v2"), "E2": ("tile-band3-RR-v2", "tile-band1-R-v2")}
for tag, names in PLATES.items():
    meshes, x = [], 0.0
    for n in names:
        m = trimesh.load(os.path.join(TILES, f"{n}.stl")); m.apply_translation(-m.bounds[0]); m.apply_translation([x, 0, 0])
        meshes.append(m); x += m.extents[0] + GAP
    plate = trimesh.util.concatenate(meshes); out = os.path.join(TILES, f"tiles-plate-{tag}.stl"); plate.export(out)
    ok = plate.extents[0] <= 250 and plate.extents[1] <= 250
    print(f"plate {tag}: {' + '.join(names):36s} {plate.extents.round(1)}  {plate.volume/1000:5.1f} cm3  {'fits' if ok else 'TOO BIG'}")
    assert ok
