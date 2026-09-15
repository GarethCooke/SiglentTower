# Bench stack viewer v18 -> v19: applies decisions D2, D4, D5, D6 (ROADMAP.md §0).
# D2  bottom drawer stays 315 x 300, printed as four quarters (seams at x 180.5, y 153); housing top = four loose tiles
# D4  side tiles two per band (155 long each, own 4 mm border); top panel four tiles 160.5 x 155 on an H-spline
# D5  column drawer 285 deep (was 300); housing top over column + slot = two loose tiles
# D6  sled beams split at y 165 (foot bridges the seam); cable channel already a separate part
# D3  (fronts printed on edge) has no geometry change.
import re, sys, json

src = open(sys.argv[1], encoding="utf-8").read()
dst = sys.argv[2]

def replace_once(s, old, new):
    assert s.count(old) == 1, f"expected exactly one match for: {old[:60]}"
    return s.replace(old, new)

# ---- BOXES ----------------------------------------------------------------
m = re.search(r"const BOXES = (\[\[.*?\]\]);", src, re.S)
boxes = json.loads(m.group(1))
GAP = 0.5   # half-gap either side of a seam, so seams read as 1 mm lines in the viewer

def split_x(b, x):  # split one box at x into two
    a = list(b); c = list(b); a[1] = x - GAP; c[0] = x + GAP; return [a, c]
def split_y(b, y):
    a = list(b); c = list(b); a[3] = y - GAP; c[2] = y + GAP; return [a, c]

out = []
for b in boxes:
    key = tuple(b[:6])
    if key == (23, 338, 3, 303, 3, 63):          # D2 bottom drawer body -> four quarters
        for h in split_x(b, 180.5): out += split_y(h, 153)
    elif key == (23, 338, 3, 303, 64, 67):       # D2 housing top over bottom drawer -> four tiles
        for h in split_x(b, 180.5): out += split_y(h, 153)
    elif key == (273, 338, 3, 303, 91, 331):     # D5 column drawer 285 deep
        b = list(b); b[3] = 288; out.append(b)
    elif key == (242, 338, 3, 303, 333, 336):    # D5 housing top over column + slot -> two tiles
        out += split_y(b, 153)
    elif key in ((20, 60, 3, 330, 337, 346), (301, 341, 3, 330, 337, 346),      # D6 beams
                 (20.5, 23, 3, 330, 326, 337), (338, 340.5, 3, 330, 326, 337)):   # and their webs
        out += split_y(b, 165)
    else:
        out.append(b)
assert len(out) == len(boxes) + 3 + 3 + 0 + 1 + 4, len(out)
src = src[:m.start(1)] + json.dumps(out) + src[m.end(1):]

# ---- D4 side tiles: two per band ------------------------------------------
src = replace_once(src,
    "for(const [z0,z1] of bands){ groups['panels'].add(tile(7, 20,330, z0,z1)); }       // left side, full length",
    "for(const [z0,z1] of bands){ groups['panels'].add(tile(7, 20,175, z0,z1)); groups['panels'].add(tile(7, 175,330, z0,z1)); }       // left side, two 155 tiles per band (D4)")
src = replace_once(src,
    "for(const [z0,z1] of bands.slice(0,3)){ groups['panels'].add(tile(351, 20,330, z0,z1)); } // right side lower bands",
    "for(const [z0,z1] of bands.slice(0,3)){ groups['panels'].add(tile(351, 20,175, z0,z1)); groups['panels'].add(tile(351, 175,330, z0,z1)); } // right side lower bands, two 155 tiles each (D4)")

# ---- D4 top panel: four tiles 160.5 x 155 on an H-spline ------------------
old_top = src[src.index("const topPanel=new THREE.Mesh"):src.index("document.getElementById('tophex')")]
new_top = """// D4: top panel = four tiles 160.5 x 155 (seams at x 180.5 and y 175), lying on the top rails, on a printed H-spline (10 wide x 3, z 507-510) under the seams
const topPanel=new THREE.Group(); const topHex=new THREE.Group(); topHex.visible=false;
const topMat=new THREE.MeshLambertMaterial({color:0x1f2226}); const edgeMat=new THREE.LineBasicMaterial({color:0x111111,transparent:true,opacity:0.35});
for(const [x0,x1] of [[20,180],[181,341]]) for(const [y0,y1] of [[20,174.5],[175.5,330]]){
  const g=new THREE.BoxGeometry(x1-x0,3,y1-y0); const m=new THREE.Mesh(g,topMat); m.position.set((x0+x1)/2,511.5,-(y0+y1)/2); m.add(new THREE.LineSegments(new THREE.EdgesGeometry(g),edgeMat)); topPanel.add(m);
  const hm=new THREE.Mesh(hexPlate(x1-x0,y1-y0,3,4),plateMat); hm.rotation.x=-Math.PI/2; hm.position.set((x0+x1)/2,510,-(y0+y1)/2); topHex.add(hm);
}
for(const grp of [topPanel,topHex]){
  const sA=new THREE.Mesh(new THREE.BoxGeometry(10,3,310),topMat); sA.position.set(180.5,508.5,-175); grp.add(sA);   // spline along the x seam, y 20-330
  const sB=new THREE.Mesh(new THREE.BoxGeometry(321,3,10),topMat); sB.position.set(180.5,508.5,-175); grp.add(sB);   // spline along the y seam, x 20-341
}
groups["panels"].add(topPanel); groups["panels"].add(topHex);
"""
src = src.replace(old_top, new_top)

# ---- labels ----------------------------------------------------------------
src = replace_once(src, "<title>Bench stack v5 — 3D</title>", "<title>Bench stack v19 — 3D</title>")
src = replace_once(src, "<b>Bench stack v18b — sled rebuilt — black / dark grey / blue</b>",
    "<b>Bench stack v19 — D2 quarters · D4 split tiles · D5 column 285 · D6 split beams</b>")
open(dst, "w", encoding="utf-8").write(src)
print("wrote", dst, len(src))
