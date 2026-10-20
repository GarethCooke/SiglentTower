# hinge_how.py — six renders of ONE door-hinge knuckle assembled with a stub of scope rail and the door's bottom edge, at
# 0 / 90 / 180 degrees, end-on and from outside: parts/door/hinge-how.png. Made for Gareth 2026-10-19 when the printed
# pair did not read as a hinge on the bench. python src/hinge_how.py   (needs cairosvg + Pillow)
import os, sys, cadquery as cq, cairosvg
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "parts"))
import door_hinge as dh
from drawer_quarters import box
OUT = os.path.normpath(os.path.join(HERE, "..", "parts", "door"))

def swing(p, deg): return p.rotate((dh.AXIS_X, 0, dh.AXIS_Z), (dh.AXIS_X, 1, dh.AXIS_Z), +deg)   # +deg opens OUTWARD in frame coordinates (door_set.py works in the mirrored rail frame, where it is -deg)

def render(deg, kind):
    dl, fl = dh.door_leaf(), dh.frame_leaf()
    rail = box(341, 361, -6, 30, 311, 331); door = box(361, 364, 0, 24, dh.TILE_Z0, dh.TILE_Z0 + 53)
    pin = cq.Workplane("XZ").center(dh.AXIS_X, dh.AXIS_Z).circle(1.45).extrude(-24)
    comp = cq.Workplane().add(cq.Compound.makeCompound([p.val() for p in (rail, fl, swing(dl, deg), swing(door, deg), pin)]))
    if kind == "end":
        comp = comp.rotate((0, 0, 0), (0, 1, 0), 90)            # so z is up in the SVG
        opt = {"projectionDir": (0, -1, 0), "width": 520, "height": 520, "showHidden": False, "strokeWidth": 0.6}
    else:
        opt = {"projectionDir": (1.2, -1.0, 0.8), "width": 700, "height": 520, "showHidden": False, "strokeWidth": 0.6, "marginLeft": 20, "marginTop": 20}
    svg = os.path.join(OUT, f"_hinge-{kind}-{deg}.svg"); png = svg[:-4] + ".png"
    cq.exporters.export(comp, svg, opt=opt); cairosvg.svg2png(url=svg, write_to=png, background_color="white"); os.remove(svg)
    return png

def main():
    tiles = [(render(0, "end"), "1. CLOSED — end view along the pin, from the front (frame z up, outboard to the right)"),
             (render(90, "end"), "2. OPEN 90°"), (render(180, "end"), "3. OPEN 180° — the door hangs 10 proud of the tile below"),
             (render(0, "iso"), "4. CLOSED — from outside, above and in front"), (render(90, "iso"), "5. OPEN 90°"), (render(180, "iso"), "6. OPEN 180°")]
    ims = [Image.open(f).convert("RGB") for f, _ in tiles]
    W = max(i.width for i in ims); H = max(i.height for i in ims); pad = 40
    sheet = Image.new("RGB", (3 * W + 4 * pad, 2 * H + 3 * pad + 130), "white"); d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20); small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font = small = ImageFont.load_default()
    d.text((pad, 10), "How the door hinge works (v2 leaves, door edge at z 338) — ONE knuckle: FRAME leaf (bolted to the scope rail's outer face, BELOW the axis) + DOOR leaf (glued inside the door, its shelf under the door's edge) + a Ø2.9 pin.", fill="black", font=font)
    d.text((pad, 40), "The barrel sits OUTBOARD of both leaves (axis x 369, z 341): the frame leaf reaches 30 down from it to the rail, the door leaf 30 up to the door. It is a cranked hinge, not a flat butt hinge —", fill="black", font=small)
    d.text((pad, 64), "the two leaves are never in one plane. Block = 36 mm of scope rail (outer face x 361). Slab = 53 mm of the door's bottom edge (x 361–364). The frame leaf never moves; door, door leaf and pin turn together.", fill="black", font=small)
    for k, (im, (f, cap)) in enumerate(zip(ims, tiles)):
        r, c = divmod(k, 3); x = pad + c * (W + pad); y = 130 + pad + r * (H + pad)
        sheet.paste(im, (x, y)); d.text((x, y - 26), cap, fill="black", font=small); os.remove(f)
    sheet.save(os.path.join(OUT, "hinge-how.png")); print("wrote", os.path.join(OUT, "hinge-how.png"))

if __name__ == "__main__":
    main()
