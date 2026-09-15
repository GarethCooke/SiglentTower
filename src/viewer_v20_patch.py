# Bench stack viewer v19 -> v20: D7 — mini slot deepened from 180 to 285 with a 15 mm air channel beside the AWG's right-hand
# (fan) vent. Vent centre measured 123 from the AWG front face -> frame y 126, Ø80 -> y 86-166; channel zone y 81-171.
# Slot inner wall steps from x 242 to x 252 over the channel zone; housing top over column + slot is notched to match so the
# channel is open upward into the 19 mm layer under the scope (z 336-355) as well as downward past the inner rail.
import re, sys, json

src = open(sys.argv[1], encoding="utf-8").read()
dst = sys.argv[2]
VENT_Y0, VENT_Y1 = 81, 171      # channel zone (vent 86-166 plus 5 each side)
SLOT_D = 288                    # slot body rear face (285 deep from y 3)
NECK_X = 252                    # inner wall x over the channel zone (15 mm clear of the AWG side at 237)

m = re.search(r"const BOXES = (\[\[.*?\]\]);", src, re.S)
boxes = json.loads(m.group(1))
out = []
for b in boxes:
    key = tuple(b[:6])
    if key == (242, 268, 3, 183, 248, 331):                       # slot body -> front pocket, neck, rear pocket
        col, grp = b[6], b[7]
        out += [[242, 268, 3, VENT_Y0, 248, 331, col, grp],
                [NECK_X, 268, VENT_Y0, VENT_Y1, 248, 331, col, grp],
                [242, 268, VENT_Y1, SLOT_D, 248, 331, col, grp]]
    elif key == (242, 338, 3, 152.5, 333, 336):                   # housing top, front tile -> notched
        col, grp = b[6], b[7]
        out += [[242, 338, 3, VENT_Y0, 333, 336, col, grp], [NECK_X, 338, VENT_Y0, 152.5, 333, 336, col, grp]]
    elif key == (242, 338, 153.5, 303, 333, 336):                 # housing top, rear tile -> notched
        col, grp = b[6], b[7]
        out += [[NECK_X, 338, 153.5, VENT_Y1, 333, 336, col, grp], [242, 338, VENT_Y1, 303, 333, 336, col, grp]]
    else:
        out.append(b)
assert len(out) == len(boxes) + 2 + 1 + 1, len(out)
src = src[:m.start(1)] + json.dumps(out) + src[m.end(1):]

def replace_once(s, old, new):
    assert s.count(old) == 1, old[:60]
    return s.replace(old, new)
src = replace_once(src, '<input type="range" id="drawer_mini" min="0" max="150"', '<input type="range" id="drawer_mini" min="0" max="250"')
src = replace_once(src, "<title>Bench stack v19 — 3D</title>", "<title>Bench stack v20 — 3D</title>")
src = replace_once(src, "<b>Bench stack v19 — D2 quarters · D4 split tiles · D5 column 285 · D6 split beams</b>",
    "<b>Bench stack v20 — D2 quarters · D4 split tiles · D5 column 285 · D6 split beams · D7 slot 285 + vent channel</b>")
# mark the vent on the AWG's right side so the channel reads: a dark disc, Ø80, centred y 126, z 292 (AWG body 251.5-333.5)
src = replace_once(src, "scene.add(new THREE.AmbientLight(0xffffff,0.55));",
    "{ const v=new THREE.Mesh(new THREE.CylinderGeometry(40,40,0.6,40), new THREE.MeshLambertMaterial({color:0x555555})); v.rotation.z=Math.PI/2; v.position.set(237.3,292.5,-126); groups['inst'].add(v); }  // D7: AWG right-side fan vent, Ø80 at y 126\n"
    "scene.add(new THREE.AmbientLight(0xffffff,0.55));")
open(dst, "w", encoding="utf-8").write(src)
print("wrote", dst, len(src))
