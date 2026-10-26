# enclosure_plan.py — check sheet for the lighting board enclosure (src/parts/board_enclosure.py).
# Three views from the model's own constants plus a 3D render of the exported STLs in place: a side section at
# x 120, the lid from behind (hexes, flange notch and vents), and the holder from above with the board and plugs.
# Output: parts/wiring/board-enclosure-plan.png
import os, sys, math, tempfile, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "parts"))
import board_enclosure as be
OUT = os.path.join(HERE, "..", "parts", "wiring")
RED, BLU, ORG, GRY = "#c0392b", "#2b6cb0", "#f2b84a", "#999"

fig = plt.figure(figsize=(18, 10))
fig.text(0.02, 0.965, "Lighting board enclosure v1 — holder + lid on the rear base rail (frame x 90-150, y 350-390.5, z 0-111)", fontsize=14, weight="bold")
fig.text(0.02, 0.937, "board-enclosure-v1.stl (68 cm³) and board-lid-v1.stl (13 cm³), black PETG. Orange = holder, grey = lid, blue = board, white = plugs.", fontsize=10)

# ---------------------------------------------------------------- 1. side section at x 120 (y right, z up)
ax = fig.add_axes([0.03, 0.09, 0.30, 0.81]); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(326, 404); ax.set_ylim(-12, 122)
ax.text(365, 118, "1. Side section at x 120", ha="center", fontsize=11, weight="bold")
ax.add_patch(Rectangle((330, 0), 20, 20, fc=GRY, ec="#333")); ax.text(340, 10, "rail", ha="center", va="center", fontsize=8, color="w")
ax.add_patch(Rectangle((be.Y0, 0), be.PLATE_T, be.Z_TOP, fc=ORG, ec="#333"))                                  # plate
ax.add_patch(Rectangle((be.Y0 + be.PLATE_T, 0), be.WALL_Y1 - be.Y0 - be.PLATE_T, be.FLOOR_T, fc=ORG, ec="#333"))  # floor
ax.add_patch(Rectangle((be.Y0 + be.PLATE_T, be.LEDGE_Z0), 360.0 - be.Y0 - be.PLATE_T, 3, fc=ORG, ec="#333"))     # ledge
# the wall behind the section plane, drawn faint with its two slots and the step
wall = Polygon([(355, 0), (be.WALL_Y1, 0), (be.WALL_Y1, be.Z_TOP), (355, be.Z_TOP)], fc=ORG, ec="#333", alpha=0.25)
ax.add_patch(wall)
for y0, y1 in ((be.SLOT_Y0, be.SLOT_Y1), (be.LSLOT_Y0, be.LSLOT_Y1)):
    ax.add_patch(Rectangle((y0, be.FLOOR_T if y0 > 380 else be.LEDGE_Z1 - 1), y1 - y0, be.Z_TOP, fc="w", ec="#333", lw=0.6, alpha=0.9))
ax.add_patch(Rectangle((be.Y0 + be.PLATE_T, be.BOLT_Z - 3.25), 0.01, 6.5, ec=RED, lw=0))
ax.add_patch(Rectangle((be.Y0, be.WIRE_Z0), be.PLATE_T, be.WIRE_Z1 - be.WIRE_Z0, fc="w", ec=RED, lw=0.8))   # wire passage (section through one)
ax.text(343, be.BOLT_Z + 7, "16 × 8 passage", ha="center", va="center", fontsize=6.5, color=RED)
ax.add_patch(Rectangle((358.5, be.LEDGE_Z1), be.BOARD_T, be.BOARD_H, fc=BLU, ec="#111", zorder=5))               # board
for z0, z1 in ((be.LEDGE_Z1 + 1.5, be.LEDGE_Z1 + 9), (be.LEDGE_Z1 + be.BOARD_H - 9, be.LEDGE_Z1 + be.BOARD_H - 1.5)):  # plugs, 20 off the board
    ax.add_patch(Rectangle((360.1, z0), 20, z1 - z0, fc="#f4f4f4", ec="#111", zorder=6))
ax.text(370, be.LEDGE_Z1 + 13, "plug + cable 20", ha="center", fontsize=6.5, zorder=7)
ax.add_patch(Rectangle((360.1, 55), 20, 10, fc="#345", ec="#111", zorder=6)); ax.text(370, 60, "1000 µF", color="w", fontsize=6.5, ha="center", va="center", zorder=7)
ax.add_patch(Rectangle((be.LID_Y0, be.LID_Z0), be.LID_T, be.Z_TOP - be.LID_Z0, fc=GRY, ec="#333", zorder=4))      # lid plate
ax.add_patch(Rectangle((be.FLANGE_Y0, be.Z_TOP), be.LID_Y1 - be.FLANGE_Y0, be.FLANGE_T, fc=GRY, ec="#333", zorder=4))  # flange
# wire paths: bottom plugs' leads leave rearward, turn down beside the board's bottom edge, forward to the plate hole;
# the USB lead leaves the top plug straight rearward through the lid's notch
ax.plot([380.1, 381, 378, 370, 360, 353], [be.LEDGE_Z1 + 5, be.LEDGE_Z1 - 2, be.LEDGE_Z1 - 10, be.BOLT_Z + 3, be.BOLT_Z, be.BOLT_Z], color="#444", lw=2, zorder=7)
ax.plot([380.1, 400], [be.LEDGE_Z1 + be.BOARD_H - 5, be.LEDGE_Z1 + be.BOARD_H - 5], color="#444", lw=2, zorder=7)
ax.add_patch(Rectangle((be.LID_Y0 - 0.5, be.USB_NOTCH_Z0), be.LID_T + 1, be.Z_TOP - be.USB_NOTCH_Z0, fc="w", ec=RED, lw=0.8, zorder=5))
ax.text(392, be.USB_NOTCH_Z0 + 4, "USB lead out\nthrough the\nlid notch", fontsize=6.5, color=RED, va="center")
def dz(y, z0, z1, s, col=RED, dx=1.2):
    ax.annotate("", (y, z0), (y, z1), arrowprops=dict(arrowstyle="<->", color=col, lw=0.9)); ax.text(y + dx, (z0 + z1) / 2, s, fontsize=7.5, color=col, va="center")
dz(393, 0, be.LEDGE_Z1, "wire bay 28", dx=0.8); dz(393, be.LEDGE_Z1, be.LEDGE_Z1 + be.BOARD_H, "board 70", dx=0.8); dz(393, be.LEDGE_Z1 + be.BOARD_H, be.Z_TOP, "10", dx=0.8)
dz(400, 0, be.Z_TOP + be.FLANGE_T, "111 overall", dx=0.8)
def dy(y0, y1, z, s, col=RED):
    ax.annotate("", (y0, z), (y1, z), arrowprops=dict(arrowstyle="<->", color=col, lw=0.9)); ax.text((y0 + y1) / 2, z - 3, s, fontsize=7.5, color=col, ha="center")
dy(be.Y0, be.WALL_Y1, -4, f"{be.WALL_Y1 - be.Y0:.1f} deep")
fig.text(0.03, 0.02, "Lid slides DOWN its slots behind the board; the flange rests on the walls' tops. Board slides down its slots onto the ledge; plugs stay on, inside the box.\n"
         "Wires: the bottom plugs' leads turn down into the bay and forward through the two 16 × 8 plate passages (z 6-14, a crimped housing fits through) into the rail slot —\n"
         "sill bundle and L strip left, R strip right; the USB lead goes straight out through the lid notch. To unplug: lid up, pull the housing off its header; the leads stay put (leave ~25 mm of slack inside the box) and the board lifts out past them.", fontsize=8.5)

# ---------------------------------------------------------------- 2. lid from behind (x right, z up) — as it sits on the frame
bx = fig.add_axes([0.35, 0.06, 0.30, 0.84]); bx.set_aspect("equal"); bx.axis("off")
bx.set_xlim(82, 158); bx.set_ylim(-12, 122)
bx.text(120, 118, "2. Lid from behind (its printed face)", ha="center", fontsize=11, weight="bold")
bx.add_patch(Rectangle((be.X0, be.Z_TOP), 60, be.FLANGE_T, fc=GRY, ec="#333"))
bx.add_patch(Rectangle((be.LID_X0, be.LID_Z0), be.LID_X1 - be.LID_X0, be.Z_TOP - be.LID_Z0, fc=GRY, ec="#333"))
w, hgt = be.LID_X1 - be.LID_X0, be.Z_TOP - be.LID_Z0
z = be.HEX_BORDER + be.HEX_R; row = 0; n = 0
while z < hgt - be.HEX_BORDER - be.HEX_R + 0.01:
    x = be.HEX_BORDER + be.HEX_R + (be.HEX_DX / 2 if row % 2 else 0.0)
    while x < w - be.HEX_BORDER - be.HEX_R + 0.01:
        if (be.LID_X0 + x + be.HEX_R + 1.5 > be.USB_X - be.USB_NOTCH_W / 2 and be.LID_X0 + x - be.HEX_R - 1.5 < be.USB_X + be.USB_NOTCH_W / 2
                and be.LID_Z0 + z + be.HEX_R + 1.5 > be.USB_NOTCH_Z0):
            x += be.HEX_DX; continue
        pts = [(be.LID_X0 + x + be.HEX_R * math.cos(math.pi / 6 + k * math.pi / 3), be.LID_Z0 + z + be.HEX_R * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
        bx.add_patch(Polygon(pts, fc="w", ec="#333", lw=0.5)); n += 1; x += be.HEX_DX
    z += be.HEX_DY; row += 1
bx.add_patch(Rectangle((be.USB_X - be.USB_NOTCH_W / 2, be.USB_NOTCH_Z0), be.USB_NOTCH_W, be.Z_TOP + be.FLANGE_T - be.USB_NOTCH_Z0 + 0.5, fc="w", ec=RED, lw=1, zorder=6))
bx.text(be.USB_X, be.Z_TOP + 6, "USB lead notch — down\nto z 88, open at the top", ha="center", fontsize=7.5, color=RED)
for x in be.VENT_XS: bx.plot([x, x], [be.Z_TOP, be.Z_TOP + be.FLANGE_T], color="#333", lw=1.2)
bx.text(125, be.Z_TOP + 6, "7 vent slots in the top", ha="center", fontsize=7.5)
bx.text(120, -3, f"{n} hexes, R {be.HEX_R} (the side-tile pattern); plate {be.LID_T} thick, {w:.0f} wide, in 0.2 slots", ha="center", fontsize=8)
bx.annotate("", (be.X0, -8), (be.X1, -8), arrowprops=dict(arrowstyle="<->", color=RED, lw=0.9)); bx.text(120, -11, "60 (flange)", ha="center", fontsize=7.5, color=RED)
bx.text(86, 55, "frame x →", rotation=90, fontsize=7, color="#777", ha="center", va="center")

# ---------------------------------------------------------------- 3. holder from above (x right, y up) with the board
cx = fig.add_axes([0.67, 0.06, 0.31, 0.42]); cx.set_aspect("equal"); cx.axis("off")
cx.set_xlim(84, 156); cx.set_ylim(344, 398)
cx.text(120, 396, "3. From above — walls, slots, board, plugs", ha="center", fontsize=11, weight="bold")
cx.add_patch(Rectangle((be.X0, 330), 60, 20, fc=GRY, ec="#333", clip_on=True)); cx.text(120, 347, "rail", ha="center", va="center", fontsize=7, color="w")
cx.add_patch(Rectangle((be.X0, be.Y0), 60, be.PLATE_T, fc=ORG, ec="#333"))
for x0, x1 in be.WIRE_SLOTS: cx.add_patch(Rectangle((x0, be.Y0), x1 - x0, be.PLATE_T, fc="w", ec=RED, lw=0.8, zorder=3))
cx.add_patch(Rectangle((be.BOLT_X - be.CBORE_D / 2, be.Y0 + be.PLATE_T - be.CBORE_H), be.CBORE_D, be.CBORE_H, fc="w", ec=RED, lw=0.8, zorder=3)); cx.text(be.BOLT_X, 352.3, "M5", ha="center", va="center", fontsize=6, color=RED, zorder=4)
cx.text(100, 357.5, "passage", ha="center", fontsize=6, color=RED); cx.text(140, 357.5, "passage", ha="center", fontsize=6, color=RED)
for x_in, x_out, sgn in ((be.X0 + be.WALL_T, be.X0 + be.SKIN_T, 1), (be.X1 - be.WALL_T, be.X1 - be.SKIN_T, -1)):
    xo = be.X0 if sgn > 0 else be.X1
    ramp = abs(x_in - x_out)
    poly = [(xo, 355), (x_in, 355), (x_in, be.STEP_Y0), (x_out, be.STEP_Y0), (x_out, be.STEP_Y1 - ramp), (x_in, be.STEP_Y1), (x_in, be.WALL_Y1), (xo, be.WALL_Y1)]
    cx.add_patch(Polygon(poly, fc=ORG, ec="#333"))
    for y0, y1 in ((be.SLOT_Y0, be.SLOT_Y1), (be.LSLOT_Y0, be.LSLOT_Y1)):   # slots (section at mid height)
        xb = be.SLOT_X0 if sgn > 0 else be.SLOT_X1
        roof = [(xb, y0), (x_in + sgn * 0.01, y0), (x_in + sgn * 0.01, min(y1 + be.SLOT_DEPTH - be.ROOF_FLAT, be.STEP_Y0 if y0 < 370 else 999)), (xb + sgn * be.ROOF_FLAT, y1), (xb, y1)]
        cx.add_patch(Polygon(roof, fc="w", ec="#333", lw=0.6))
cx.add_patch(Rectangle((be.SLOT_X0 + be.SLOT_FLOAT, 358.5), be.BOARD_W, be.BOARD_T, fc=BLU, ec="#111", zorder=5))
hx = lambda n: be.BOARD_X0 + 3.41 + (n - 1) * 2.54
for a, b_, t in ((2, 4, "3"), (7, 9, "3"), (13, 17, "5")):
    cx.add_patch(Rectangle((hx(a) - 2.45, 360.1), hx(b_) - hx(a) + 4.9, 20, fc="#f4f4f4", ec="#111", zorder=6)); cx.text((hx(a) + hx(b_)) / 2, 370, t, ha="center", va="center", fontsize=6.5, zorder=7)
cx.add_patch(Rectangle((be.LID_X0, be.LID_Y0), be.LID_X1 - be.LID_X0, be.LID_T, fc=GRY, ec="#333", zorder=4))
cx.text(120, 383, "cavity 56 wide, 25 deep behind the board (walls thin to 2 at y 361); plugs 20, lid 5 clear", ha="center", va="center", fontsize=6.8)
cx.text(120, 392.5, "lid plate in its slots, 1.6 behind the ramps' foot", ha="center", fontsize=7)
cx.annotate("", (be.X0, 352.5), (be.X1, 352.5), arrowprops=dict(arrowstyle="<->", color=RED, lw=0.9)); cx.text(120, 350.5, "60", ha="center", fontsize=7, color=RED)

# ---------------------------------------------------------------- 4. 3D render of the STLs in place
import trimesh
dx3 = fig.add_axes([0.66, 0.48, 0.33, 0.44], projection="3d"); dx3.set_axis_off()
dx3.set_title("4. Assembled (holder, lid lifted 30 for clarity, board)", fontsize=10, weight="bold")
def mesh_of(part):
    tmp = os.path.join(tempfile.gettempdir(), "board-enclosure-render.stl"); import cadquery as cq   # outside the repo
    cq.exporters.export(part, tmp, tolerance=0.05, angularTolerance=0.2); m = trimesh.load(tmp); os.remove(tmp); return m
for part, col, alpha in ((be.holder(), ORG, 1.0), (be.lid().translate((0, 0, 30)), GRY, 0.55), (be.board(), BLU, 1.0)):
    m = mesh_of(part)
    dx3.plot_trisurf(m.vertices[:, 0], m.vertices[:, 1], m.vertices[:, 2], triangles=m.faces, color=col, alpha=alpha, edgecolor="none", shade=True)
dx3.set_xlim(85, 155); dx3.set_ylim(345, 415); dx3.set_zlim(0, 145); dx3.view_init(elev=22, azim=-130)
dx3.set_box_aspect((70, 70, 145))

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "board-enclosure-plan.png"), dpi=100)
print("ok")
