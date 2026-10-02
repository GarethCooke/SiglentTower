# logo.py — the IguanaWare iguana (Iguana.svg, a potrace trace: one compound path with holes) as a CadQuery solid for the
# two-colour inlay on the bottom-drawer facia. logo_solid(w, h, depth) returns the iguana scaled to fit w x h (keeping
# its aspect), rotated 90° clockwise (head to the right), lying in XY with z 0..depth, bounding box from (0, 0).
import os, numpy as np
from svgpathtools import svg2paths
from shapely.geometry import Polygon
from shapely.ops import unary_union
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); SVG = os.path.join(HERE, "..", "Iguana.svg")

def _rings(n_per_seg=6):
    paths, _ = svg2paths(SVG)
    rings = []
    for path in paths:
        for sub in path.continuous_subpaths():
            pts = []
            for seg in sub:
                for t in np.linspace(0, 1, n_per_seg, endpoint=False):
                    z = seg.point(t); pts.append((z.real, z.imag))       # potrace path coords are already y-up (its transform flips them)
            if len(pts) >= 3: rings.append(pts)
    return rings

def logo_polygon():
    """Even-odd fill of the potrace rings -> a (multi)polygon with holes, unit: SVG px."""
    polys = [Polygon(r).buffer(0) for r in _rings()]
    polys = [p for p in polys if not p.is_empty]
    polys.sort(key=lambda p: p.area, reverse=True)
    result = None
    for p in polys:                                                    # even-odd: alternate add / subtract by containment depth
        depth = sum(1 for q in polys if q.area > p.area and q.contains(p.representative_point()))
        result = p if result is None else (result.union(p) if depth % 2 == 0 else result.difference(p))
    return result

def logo_solid(w=60.0, h=30.0, depth=0.8, min_feature=0.9):
    poly = logo_polygon()
    minx, miny, maxx, maxy = poly.bounds
    # rotate 90° cw: (x, y) -> (y, -x); then scale to fit w x h
    from shapely.affinity import rotate, scale, translate
    poly = rotate(poly, -90, origin=(0, 0))
    minx, miny, maxx, maxy = poly.bounds
    s = min(w / (maxx - minx), h / (maxy - miny))
    poly = scale(poly, s, s, origin=(0, 0)); minx, miny, maxx, maxy = poly.bounds
    poly = translate(poly, -minx, -miny)
    poly = poly.buffer(-min_feature / 2).buffer(min_feature / 2).simplify(0.05)   # drop features thinner than the nozzle can print
    solid = None
    geoms = list(poly.geoms) if poly.geom_type == "MultiPolygon" else [poly]
    for g in geoms:
        if g.area < 1.0: continue
        outer = cq.Workplane("XY").polyline(list(g.exterior.coords)[:-1]).close().extrude(depth)
        for hole in g.interiors:
            if Polygon(hole).area < 0.5: continue
            outer = outer.cut(cq.Workplane("XY").polyline(list(hole.coords)[:-1]).close().extrude(depth + 2).translate((0, 0, -1)))
        solid = outer if solid is None else solid.union(outer)
    return solid

if __name__ == "__main__":
    s = logo_solid(); bb = s.val().BoundingBox()
    print(f"logo {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}  {s.val().Volume():.0f} mm3")
    cq.exporters.export(s, "/tmp/logo.stl")
