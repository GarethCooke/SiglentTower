# publish_3mf.py — builds publish/SiglentTower-complete.3mf: every part the tower needs as ONE Bambu Studio project, one plate
# per print, grouped by filament, each plate named "NN material colour — parts", each object named after its STL, the
# print profile `SiglentTower fit 0.20` on every plate (lifted from a project Bambu Studio saved: TEMPLATE). The jigs ride
# on their own plates at the end. Coupons stay out (ROADMAP §7). Also writes publish/PLATES.md, the plate list with the
# per-plate settings that are not in the file (filament temperatures, skirt, the sacrificial layer) and the hardware.
#
# Run from the repo root:  python src/publish_3mf.py   (needs only the standard library)
#
# How the file is put together (the layout Bambu Studio writes, 02.08): each STL becomes one mesh object in
# 3D/Objects/object_N.model with its vertices CENTRED on the part's bounding box; 3D/3dmodel.model lists the objects as
# components and places every instance with a 3 x 4 transform (rotation about z for the diagonal parts, translation to
# the plate position, z = half the height so the part sits on the bed); Metadata/model_settings.config names the objects,
# gives each its filament ("extruder") and per-object print settings (brim, ironing, supports), and lists which instances
# are on which plate; Metadata/project_settings.config is the template project's, i.e. the SiglentTower profile with the
# five filaments Gareth's AMS held. Plates sit on Bambu's logical grid: 256 mm beds on a 307.2 mm stride, ceil(sqrt(n))
# columns, rows downward.
#
# Filament slots (the template's, kept): 1 black ABS+ (eSUN; the sliding pairs), 2 dark blue PETG (Bambu PETG HF —
# the accents, and the stand-in for the clear sill window), 3 black ABS (Bambu), 4 PETG in the colour the plate name
# says (SUNLU PETG profile; black, dark grey, white or yellow), 5 blue TPU 95A (Geeetech). Two-colour plates use 4 + 2.
import os, re, io, json, math, struct, zipfile, uuid, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "bambu", "parts", "sled-cross-bar-front-and-rear-v2.3mf")
OUT_DIR = os.path.join(ROOT, "publish")
OUT = os.path.join(OUT_DIR, "SiglentTower-complete.3mf")
BED, MARGIN, GAP = 256.0, 2.0, 4.0
EXCLUDE = (18.0, 28.0)                  # the X1C's bed exclusion corner at x 0-18, y 0-28 (project_settings bed_exclude_area)
STRIDE = BED * 1.2                      # Bambu's logical plate gap (LOGICAL_PART_PLATE_GAP = 1/5)

# ---------------------------------------------------------------- the plan ----------------------------------------------
ABSP = dict(brim_type="outer_only", brim_width="5", brim_object_gap="0.1")                     # the ABS+ profile (ROADMAP §2)
BRIM5 = dict(brim_type="outer_only", brim_width="5")
THIN = dict(brim_type="outer_only", brim_width="15", brim_object_gap="0", outer_wall_speed="60")   # thin standing parts
NOBRIM = dict(brim_type="no_brim")
IRON = dict(ironing_type="top")
NOSUP = dict(enable_support="0")
JIG = dict(wall_loops="2", sparse_infill_density="15%", brim_type="no_brim")

def P(stl, n=1, rot=0, at=None, ext=4, brim=0, **cfg):
    """one item on a plate: STL path under parts/ (or jigs/, coupons/), count, rotation about z in degrees, an explicit
    (x, y) centre in plate mm (else auto-packed), filament slot, brim width to keep clear when packing, per-object config"""
    return dict(stl=stl, n=n, rot=rot, at=at, ext=ext, brim=brim, cfg=cfg)

def diag(*items):
    """parallel bars on the 45° diagonal from the plate's top-left to its bottom-right (so no bar end lands in the X1C's
    exclusion corner at the bottom-left), centred, spaced by their widths + GAP. Each bar's long axis is read from its
    mesh: an x-long bar is turned -45°, a y-long bar +45°; either way the bars step across each other along (1, 1)."""
    dims = []
    for it in items:
        rels = it["stl"] if isinstance(it["stl"], tuple) else (it["stl"],)
        ms = [Mesh.get(r) for r in rels]
        w = max(m.hi[0] for m in ms) - min(m.lo[0] for m in ms); d = max(m.hi[1] for m in ms) - min(m.lo[1] for m in ms)
        dims.append((min(w, d), w >= d))
    total = sum(w for w, _ in dims) + GAP * (len(items) - 1); t = -total / 2
    for it, (w, xlong) in zip(items, dims):
        c = t + w / 2; it["rot"] = -45 if xlong else 45
        it["at"] = (BED / 2 + c / math.sqrt(2), BED / 2 + c / math.sqrt(2))
        t += w + GAP
    return list(items)

# ---------------------------------------------------------------- meshes ------------------------------------------------
def read_stl(path):
    data = open(path, "rb").read()
    tris = []
    if data[:5] == b"solid" and b"facet" in data[:600]:
        cur = []
        for line in data.decode("ascii", "ignore").splitlines():
            t = line.split()
            if t and t[0] == "vertex":
                cur.append((float(t[1]), float(t[2]), float(t[3])))
                if len(cur) == 3: tris.append(tuple(cur)); cur = []
    else:
        n = struct.unpack("<I", data[80:84])[0]; off = 84
        for _ in range(n):
            v = struct.unpack("<12fH", data[off:off + 50]); off += 50
            tris.append(((v[3], v[4], v[5]), (v[6], v[7], v[8]), (v[9], v[10], v[11])))
    verts, index, faces = [], {}, []
    for tri in tris:
        f = []
        for v in tri:
            k = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
            if k not in index: index[k] = len(verts); verts.append(k)
            f.append(index[k])
        if len(set(f)) == 3: faces.append(tuple(f))
    return verts, faces

class Mesh:
    cache = {}
    def __init__(self, rel):
        self.rel = rel; self.name = os.path.basename(rel)
        self.verts, self.faces = read_stl(os.path.join(ROOT, "parts", rel))
        xs, ys, zs = zip(*self.verts)
        self.lo = (min(xs), min(ys), min(zs)); self.hi = (max(xs), max(ys), max(zs))
    @classmethod
    def get(cls, rel):
        if rel not in cls.cache: cls.cache[rel] = cls(rel)
        return cls.cache[rel]

def footprint(w, d, rot):
    a = math.radians(rot); c, s = abs(math.cos(a)), abs(math.sin(a))
    return w * c + d * s, w * s + d * c

def plates():
  return [
 ("01 ABS+ black — sled T-feet ×2, beam halves ×4 (feet standing; outer brim 5)",
  [P("sled-foot-210.stl", 2, ext=1, **ABSP), P("sled-beam-left-front-v2.stl", ext=1, **ABSP), P("sled-beam-right-front-v2.stl", ext=1, **ABSP),
   P("sled-beam-left-rear-v1.stl", ext=1, **ABSP), P("sled-beam-right-rear-v1.stl", ext=1, **ABSP)]),
 ("02 ABS+ black — bottom drawer runner (1 of 2; leg top down, ironing on top)", [P("drawer/drawer-runner-300-v1.stl", ext=1, **ABSP, **IRON)]),
 ("03 ABS+ black — bottom drawer runner (2 of 2)", [P("drawer/drawer-runner-300-v1.stl", ext=1, **ABSP, **IRON)]),
 ("04 ABS+ black — column guide strips upper ×2 (rail face down, diagonal)",
  diag(P("column/column-strip-upper-v1.stl", ext=1, **ABSP), P("column/column-strip-upper-v1.stl", ext=1, **ABSP))),
 ("05 ABS+ black — column guide strips lower right + lower left short",
  diag(P("column/column-strip-lower-v1.stl", ext=1, **ABSP), P("column/column-strip-lower-short-v1.stl", ext=1, **ABSP))),
 ("06 ABS+ black — mini-slot runner v3 (plate down, diagonal, ironing on top)", diag(P("mini/mini-slot-runner-v3.stl", ext=1, **ABSP, **IRON))),
 ("07 ABS black — cradles — PSU left v3 ×2, right rear v4, right front v5, AWG left v2 ×2, right v2 ×2 (sacrificial layer in the cups)",
  [P("psu-cradle-v3.stl", 2, ext=3, **BRIM5), P("psu-cradle-right-v4.stl", ext=3, **BRIM5), P("psu-cradle-right-front-v5.stl", ext=3, **BRIM5),
   P("awg-cradle-left-v2.stl", 2, ext=3, **BRIM5), P("awg-cradle-right-v2.stl", 2, ext=3, **BRIM5)]),
 ("08 ABS black — sled cross bars front + rear v2 (flat, lips up, diagonal)",
  diag(P("sled-cross-bar-front-v2.stl", ext=3, **BRIM5), P("sled-cross-bar-rear-v2.stl", ext=3, **BRIM5))),
 ("09 ABS black — cable channel, splices ×2, hinge leaves 2 + 2, magnet bracket, magnet tab",
  [P("cable-channel-v1.stl", ext=3, **NOBRIM), P("sled-splice-v2.stl", 2, ext=3, **NOBRIM), P("hinge-door-v2.stl", 2, ext=3, **NOBRIM), P("hinge-frame-v2.stl", 2, ext=3, **NOBRIM),
   P("door/magnet-bracket-front-v2.stl", ext=3, **NOBRIM), P("door/magnet-tab-rear-v2.stl", ext=3, **NOBRIM)]),
 ("10 PETG black — bottom drawer quarter Q1", [P("drawer/drawer-Q1-v1.stl")]),
 ("11 PETG black — bottom drawer quarter Q2", [P("drawer/drawer-Q2-v1.stl")]),
 ("12 PETG black — bottom drawer quarter Q3", [P("drawer/drawer-Q3-v1.stl")]),
 ("13 PETG black — bottom drawer quarter Q4", [P("drawer/drawer-Q4-v1.stl")]),
 ("14 PETG black — column drawer v3 (floor down, diagonal, outer brim 5; ~24 h)", diag(P("column/column-drawer-v3.stl", **BRIM5))),
 ("15 PETG black — mini-slot body (diagonal, outer brim 5) + sled front rests ×2 + hinge pins",
  diag(P("mini/mini-slot-body-v1.stl", **BRIM5)) + [P("sled-front-rest-v2-gap3.0.stl", at=(40, 42)), P("sled-front-rest-v2-gap3.0.stl", at=(72, 42)), P("door/hinge-pins-v1.stl", at=(40, 78))]),
 ("16 PETG black — tiles A2 — band2-LF + band1-LF", [P("tiles/tile-band2-LF-v2.stl"), P("tiles/tile-band1-LF-v2.stl")]),
 ("17 PETG black — tiles B2 — band2-LR + band1-LR", [P("tiles/tile-band2-LR-v2.stl"), P("tiles/tile-band1-LR-v2.stl")]),
 ("18 PETG black — tiles C2 — band3-LF + band3-LR", [P("tiles/tile-band3-LF-v2.stl"), P("tiles/tile-band3-LR-v2.stl")]),
 ("19 PETG black — tiles D2 — band3-RF + band1-R", [P("tiles/tile-band3-RF-v2.stl"), P("tiles/tile-band1-R-v2.stl")]),
 ("20 PETG black — tiles E2 — band3-RR + band1-R", [P("tiles/tile-band3-RR-v2.stl"), P("tiles/tile-band1-R-v2.stl")]),
 ("21 PETG black — tile band2-RF + door set fixed rear tile v2", [P("tiles/tile-band2-RF-v1.stl"), P("door/rear-tile-v2.stl", rot=90)]),
 ("22 PETG black — tile band2-RR + lighting board enclosure + lid", [P("tiles/tile-band2-RR-v1.stl"), P("wiring/board-enclosure-v1.stl"), P("wiring/board-lid-v1.stl")]),
 ("23 PETG black — tile band4-LF (legs stand 19)", [P("tiles/tile-band4-LF-v1.stl")]),
 ("24 PETG black — tile band4-LR", [P("tiles/tile-band4-LR-v1.stl")]),
 ("25 PETG black — door v3 (face down)", [P("door/door-v3.stl")]),
 ("26 PETG black — top panel — four tiles standing (thin-part settings)",
  [P("top/top-tile-FL-v1.stl", brim=15, **THIN), P("top/top-tile-FR-v1.stl", brim=15, **THIN), P("top/top-tile-RL-v1.stl", brim=15, **THIN), P("top/top-tile-RR-v1.stl", brim=15, **THIN)]),
 ("27 PETG dark grey + dark blue logo inlay — bottom drawer facia (standing, diagonal, thin-part settings)",
  diag(P(("drawer/drawer-facia-v1.stl", "drawer/drawer-facia-logo-v1.stl"), ext=(4, 2), **THIN))),
 ("28 PETG dark grey + natural window — sill panel (standing, diagonal, brim 5)",
  diag(P(("sill/sill-panel-v3.stl", "sill/sill-panel-window-v4.stl"), ext=(4, 2), **BRIM5))),
 ("29 PETG dark grey — column facia + mini-slot facia (standing, thin-part settings)",
  diag(P("column/column-facia-v1.stl", **THIN)) + [P("mini/mini-slot-facia-v1.stl", at=(70, 30), **THIN)]),
 ("30 PETG dark grey — sled front bar v3 (front face down, diagonal, outer brim 5)", diag(P("sled-front-bar-v3.stl", **BRIM5))),
 ("31 PETG dark grey — rear box left half (floor down, outer brim 5)", [P("rear-box-left-v1.stl", **BRIM5)]),
 ("32 PETG dark grey — rear box right half", [P("rear-box-right-v1.stl", **BRIM5)]),
 ("33 PETG dark blue — pull inserts bottom, column, mini v2 + sled-bar liner + upright caps ×4 (supports on, build plate only)",
  [P("top/upright-cap-v1.stl", 4, ext=2), P("inserts/pull-insert-bottom-v2.stl", ext=2), P("inserts/pull-insert-column-v2.stl", ext=2), P("inserts/pull-insert-mini-v2.stl", ext=2), P("inserts/sled-bar-pull-liner-v1.stl", ext=2)]),
 ("34 PETG any colour (hidden parts) — box braces ×2, strip brackets upper v2 + lower v5, sill blocks left v10 + right v4",
  [P("box-brace-v1.stl", 2, **NOBRIM), P("strip-bracket-upper-v2.stl", **NOBRIM), P("strip-bracket-lower-v5.stl", **NOBRIM), P("sill/sill-block-left-v10.stl", **NOBRIM), P("sill/sill-block-right-v4.stl", **NOBRIM)]),
 ("35 TPU blue 95A — frame feet ×4, AWG pads 2 + 2, sled stop caps ×2, slot covers ×6 (no brim, no support; dried, external spool)",
  [P("tpu/slot-cover-240-v1.stl", 6, ext=5, **NOBRIM, **NOSUP), P("tpu/frame-foot-v1.stl", 4, ext=5, **NOBRIM, **NOSUP), P("tpu/awg-pad-left-v1.stl", 2, ext=5, **NOBRIM, **NOSUP),
   P("tpu/awg-pad-right-v1.stl", 2, ext=5, **NOBRIM, **NOSUP), P("tpu/sled-stop-cap-v1.stl", 2, ext=5, **NOBRIM, **NOSUP)]),
 ("36 JIG — any colour, any PETG or PLA — rail spacers 48, 63.5, 139.5, 159 ×2 each + the 3.0 web gauge",
  [P("../coupons/spacers/spacer-159.stl", 2, **JIG), P("../coupons/spacers/spacer-139.5.stl", 2, **JIG), P("../coupons/spacers/spacer-63.5.stl", 2, **JIG), P("../coupons/spacers/spacer-48.stl", 2, **JIG), P("../coupons/spacers/gauge-3.0.stl", **JIG)]),
 ("37 JIG — any colour, any PETG or PLA — seating jigs PSU L, PSU R, AWG L, AWG R + AWG pad stand-ins ×4",
  [P("../jigs/seat-jig-psu-L.stl", **JIG), P("../jigs/seat-jig-psu-R.stl", **JIG), P("../jigs/seat-jig-awg-L.stl", **JIG), P("../jigs/seat-jig-awg-R.stl", **JIG), P("../jigs/awg-pad-standin.stl", 4, **JIG)]),
]

# ---------------------------------------------------------------- packing (max-rects, best short side) -------------------
def pack(items):
    """items: list of dicts with w, d (footprint incl. brim); sets x, y (lower-left). Explicitly placed items are
    subtracted from the free space first."""
    free = [[MARGIN, EXCLUDE[1] + GAP, BED - 2 * MARGIN, BED - MARGIN - EXCLUDE[1] - GAP],          # two overlapping free rects:
            [EXCLUDE[0] + GAP, MARGIN, BED - MARGIN - EXCLUDE[0] - GAP, BED - 2 * MARGIN]]           # the bed minus the exclusion corner
    def split(fr, x, y, w, d):
        out = []
        for f in fr:
            fx, fy, fw, fd = f
            if x >= fx + fw or x + w <= fx or y >= fy + fd or y + d <= fy: out.append(f); continue
            if x > fx: out.append([fx, fy, x - fx, fd])
            if x + w < fx + fw: out.append([x + w, fy, fx + fw - x - w, fd])
            if y > fy: out.append([fx, fy, fw, y - fy])
            if y + d < fy + fd: out.append([fx, y + d, fw, fy + fd - y - d])
        # drop rects contained in others
        out = [a for i, a in enumerate(out) if not any(j != i and b[0] <= a[0] and b[1] <= a[1] and b[0] + b[2] >= a[0] + a[2] and b[1] + b[3] >= a[1] + a[3] for j, b in enumerate(out))]
        return out
    for it in items:
        if it["at"] is not None:
            it["x"], it["y"] = it["at"][0] - it["w"] / 2, it["at"][1] - it["d"] / 2
            free = split(free, it["x"] - GAP, it["y"] - GAP, it["w"] + 2 * GAP, it["d"] + 2 * GAP)
    for it in sorted([i for i in items if i["at"] is None], key=lambda i: (-max(i["w"], i["d"]), -(i["w"] * i["d"]))):   # longest side first
        best = None
        for f in free:
            if it["w"] <= f[2] and it["d"] <= f[3]:
                score = min(f[2] - it["w"], f[3] - it["d"]) + 0.01 * (f[0] + f[1])   # best short-side fit, nearest the origin on a tie
                if best is None or score < best[0]: best = (score, f)
        if best is None: raise SystemExit(f"does not fit: {it['name']} {it['w']:.1f} x {it['d']:.1f}")
        f = best[1]; it["x"], it["y"] = f[0], f[1]
        free = split(free, it["x"] - GAP, it["y"] - GAP, it["w"] + 2 * GAP, it["d"] + 2 * GAP)   # GAP clear on every side

# ---------------------------------------------------------------- build the project -----------------------------------
def build():
    with zipfile.ZipFile(TEMPLATE) as z:
        project_settings = z.read("Metadata/project_settings.config")
    ps = json.loads(project_settings)
    assert ps.get("print_settings_id") == "SiglentTower fit 0.20", "template is not on the SiglentTower profile"
    today = datetime.date.today().isoformat()
    PLATES = plates()
    cols = math.ceil(math.sqrt(len(PLATES)))

    objects, instances, plates_xml, plan_rows = [], [], [], []
    obj_id = 0; ident = 100
    for pi, (pname, items) in enumerate(PLATES):
        origin = ((pi % cols) * STRIDE, -(pi // cols) * STRIDE)
        placed = []
        for it in items:
            rels = it["stl"] if isinstance(it["stl"], tuple) else (it["stl"],)
            meshes = [Mesh.get(r) for r in rels]
            lo = tuple(min(m.lo[k] for m in meshes) for k in range(3)); hi = tuple(max(m.hi[k] for m in meshes) for k in range(3))
            w, d, h = hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]
            fw, fd = footprint(w, d, it["rot"])
            for k in range(it["n"]):
                placed.append(dict(it, meshes=meshes, lo=lo, hi=hi, h=h, w=fw + 2 * it["brim"], d=fd + 2 * it["brim"], name=meshes[0].name, at=it["at"] if k == 0 else None))
        pack(placed)
        inst_xml = []
        for it in placed:
            cx, cy = it["x"] + it["w"] / 2, it["y"] + it["d"] / 2
            assert MARGIN - 0.01 <= it["x"] and it["x"] + it["w"] <= BED - MARGIN + 0.01 and MARGIN - 0.01 <= it["y"] and it["y"] + it["d"] <= BED - MARGIN + 0.01, (pname, it["name"])
            assert it["x"] >= EXCLUDE[0] or it["y"] >= EXCLUDE[1] or it["rot"] % 90, ("in the exclusion corner", pname, it["name"])
            obj_id += 1; oid = obj_id
            objects.append(dict(id=oid, it=it, plate=pi + 1))
            a = math.radians(it["rot"]); c, s = math.cos(a), math.sin(a)
            tf = f"{c:.9g} {s:.9g} 0 {-s:.9g} {c:.9g} 0 0 0 1 {origin[0] + cx:.4f} {origin[1] + cy:.4f} {it['h'] / 2:.4f}"
            instances.append((oid, tf)); ident += 1
            inst_xml.append(f'    <model_instance>\n      <metadata key="object_id" value="{2 * oid}"/>\n      <metadata key="instance_id" value="0"/>\n      <metadata key="identify_id" value="{ident}"/>\n    </model_instance>')
            plan_rows.append((pi + 1, it["name"] + (" + " + it["meshes"][1].name if len(it["meshes"]) > 1 else ""), it["rot"], round(cx, 1), round(cy, 1), it["ext"], it["cfg"]))
        assert not any(c in pname for c in '<>:/\\|?*"'), f"Bambu Studio rejects the character in the plate name: {pname}"
        plates_xml.append(f'  <plate>\n    <metadata key="plater_id" value="{pi + 1}"/>\n    <metadata key="plater_name" value="{xml(pname)}"/>\n    <metadata key="locked" value="false"/>\n    <metadata key="filament_map_mode" value="Auto For Flush"/>\n' + "\n".join(inst_xml) + "\n  </plate>")

    # --- 3D/Objects/object_N.model (one file per object, the meshes centred on the object's bounding box) ---
    files = {}
    comp_xml, settings_xml, rels = [], [], []
    for o in objects:
        it, oid = o["it"], o["id"]
        centre = tuple((it["lo"][k] + it["hi"][k]) / 2 for k in range(3))
        mesh_objs, comps, parts = [], [], []
        for mi, m in enumerate(it["meshes"]):
            mid = 2 * oid - 1 + mi * 1000          # unique ids inside the object file
            vs = "\n".join(f'     <vertex x="{v[0] - centre[0]:.4f}" y="{v[1] - centre[1]:.4f}" z="{v[2] - centre[2]:.4f}"/>' for v in m.verts)
            ts = "\n".join(f'     <triangle v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>' for f in m.faces)
            mesh_objs.append(f'  <object id="{mid}" p:UUID="{uuid.uuid4()}" type="model">\n   <mesh>\n    <vertices>\n{vs}\n    </vertices>\n    <triangles>\n{ts}\n    </triangles>\n   </mesh>\n  </object>')
            comps.append(f'    <component p:path="/3D/Objects/object_{oid}.model" objectid="{mid}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>')
            ext = it["ext"][mi] if isinstance(it["ext"], tuple) else it["ext"]
            parts.append(f'    <part id="{mid}" subtype="normal_part" uuid="{uuid.uuid4()}">\n      <metadata key="name" value="{xml(m.name)}"/>\n      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n      <metadata key="source_file" value="{xml(m.name)}"/>\n      <metadata key="extruder" value="{ext}"/>\n      <metadata face_count="{len(m.faces)}"/>\n    </part>')
        files[f"3D/Objects/object_{oid}.model"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n' + "\n".join(mesh_objs) + '\n </resources>\n <build/>\n</model>\n').encode()
        rels.append(f' <Relationship Target="/3D/Objects/object_{oid}.model" Id="rel-{oid}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>')
        comp_xml.append(f'  <object id="{2 * oid}" p:UUID="{uuid.uuid4()}" type="model">\n   <components>\n' + "\n".join(comps) + '\n   </components>\n  </object>')
        ext0 = it["ext"][0] if isinstance(it["ext"], tuple) else it["ext"]
        name = it["meshes"][0].name if len(it["meshes"]) == 1 else it["meshes"][0].name.replace(".stl", "") + " + " + it["meshes"][1].name
        cfg = "".join(f'\n    <metadata key="{k}" value="{xml(v)}"/>' for k, v in it["cfg"].items())
        settings_xml.append(f'  <object id="{2 * oid}">\n    <metadata key="name" value="{xml(name)}"/>\n    <metadata key="extruder" value="{ext0}"/>{cfg}\n    <metadata face_count="{sum(len(m.faces) for m in it["meshes"])}"/>\n' + "\n".join(parts) + "\n  </object>")

    build_items = "\n".join(f'  <item objectid="{2 * oid}" p:UUID="{uuid.uuid4()}" transform="{tf}" printable="1"/>' for oid, tf in instances)
    files["3D/3dmodel.model"] = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n <metadata name="Application">BambuStudio-02.08.02.61</metadata>\n <metadata name="BambuStudio:3mfVersion">1</metadata>\n <metadata name="Copyright">Gareth Cooke — CC BY 4.0 (LICENSE-DESIGN.md)</metadata>\n <metadata name="CreationDate">{today}</metadata>\n <metadata name="Description">SiglentTower — every printed part of the bench tower, one plate per print, grouped by filament; jigs last. Built by src/publish_3mf.py from the fitted STLs in parts/.</metadata>\n <metadata name="Designer">Gareth Cooke (IguanaWare)</metadata>\n <metadata name="DesignerCover"></metadata>\n <metadata name="DesignerUserId"></metadata>\n <metadata name="License">CC BY 4.0</metadata>\n <metadata name="ModificationDate">{today}</metadata>\n <metadata name="Origin"></metadata>\n <metadata name="Title">SiglentTower — complete</metadata>\n <resources>\n' + "\n".join(comp_xml) + f'\n </resources>\n <build p:UUID="{uuid.uuid4()}">\n{build_items}\n </build>\n</model>\n').encode()
    files["3D/_rels/3dmodel.model.rels"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n' + "\n".join(rels) + "\n</Relationships>").encode()
    files["Metadata/model_settings.config"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n' + "\n".join(settings_xml) + "\n" + "\n".join(plates_xml) + "\n</config>\n").encode()
    files["Metadata/project_settings.config"] = project_settings
    files["Metadata/slice_info.config"] = b'<?xml version="1.0" encoding="UTF-8"?>\n<config>\n  <header>\n    <header_item key="X-BBL-Client-Type" value="slicer"/>\n    <header_item key="X-BBL-Client-Version" value="02.08.02.61"/>\n  </header>\n</config>\n'
    files["[Content_Types].xml"] = b'<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n <Default Extension="png" ContentType="image/png"/>\n <Default Extension="gcode" ContentType="text/x.gcode"/>\n</Types>'
    files["_rels/.rels"] = b'<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n</Relationships>'

    os.makedirs(OUT_DIR, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ["[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model", "3D/_rels/3dmodel.model.rels"] + sorted(k for k in files if k.startswith("3D/Objects")) + ["Metadata/model_settings.config", "Metadata/project_settings.config", "Metadata/slice_info.config"]:
            z.writestr(name, files[name])
    write_plan(plan_rows, today, PLATES)
    print(f"{OUT}: {len(PLATES)} plates, {len(objects)} objects, {os.path.getsize(OUT) / 1e6:.1f} MB")

def xml(s): return str(s).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def write_plan(rows, today, PLATES):
    slots = {1: "black ABS+", 2: "dark blue PETG", 3: "black ABS", 4: "PETG (colour per plate)", 5: "blue TPU"}
    lines = [f"# SiglentTower-complete.3mf — the plates ({today})", "",
             "One Bambu Studio project with every printed part of the tower, one plate per print, in filament order; the jigs last. Made by `src/publish_3mf.py` from the fitted STLs in `parts/` (and `jigs/`, `coupons/spacers/`); re-run it after any part changes. Print profile `SiglentTower fit 0.20` on every plate (ROADMAP §2 has the settings). Coupons are not in it.",
             "", "**Filament slots** (the project has five; set your own spools against them): 1 black ABS+ (eSUN — the sliding pairs and long thin bars), 2 dark blue PETG (the accents; it also stands in for the clear window on plate 28), 3 black ABS, 4 PETG in the colour the plate name says (black, dark grey, white, yellow — any PETG profile), 5 blue TPU 95A.",
             "", "**One material per plate** (Gareth, 2026-11-06): no plate mixes filaments, so no purge tower — except the two objects that are two-colour by design, each on its own plate: the bottom facia with its logo inlay (27) and the sill panel with its clear window (28).",
             "", "**Settings that are in the file, per object:** outer brim 5 mm with 0.1 gap on every ABS+ and ABS part that had one; outer brim 15 mm, gap 0 and outer wall 60 mm/s on the thin standing parts (the three facias and the four top tiles); ironing on the top surfaces of the runners; no brim and no support on the TPU; 2 walls and 15 % infill on the jigs.",
             "**Settings that are NOT in the file** (filament- or plate-level — set them when you slice): dry ABS+ and TPU first; ABS and ABS+ with the door closed; the thin-part plates (26, 27, 28, 29) with the skirt off, bed 80 °C, part fan 30 % max; the cradle plate (07) and the runner plates (02, 03, 05) with Quality → Bridge counterbore holes → Sacrificial layer; TPU from the external spool holder with the Generic TPU preset.",
             "", "| Plate | Object | Turned | Centre x, y | Slot | Per-object settings |", "|---|---|---|---|---|---|"]
    for p, name, rot, cx, cy, ext, cfg in rows:
        lines.append(f"| {p:02d} | {name} | {rot}° | {cx}, {cy} | {ext if not isinstance(ext, tuple) else ' + '.join(map(str, ext))} | {', '.join(f'{k} {v}' for k, v in cfg.items()) or '—'} |")
    lines += ["", "Plate names in the project: " + "; ".join(n for n, _ in PLATES) + ".", "",
              "Hardware the plates need, from HANDOVER §10: 47 M5 × 10 button head (4 into the uprights' bores, no T-nut), 9 M5 × 10 countersunk, 2 M5 × 12, 54 drop-in T-nuts, M5 × 8 for the 8 cast brackets, 4 M3 × 10, 4 Ø10 × 2 magnets, the 8 mm button and its nut, CA glue."]
    open(os.path.join(OUT_DIR, "PLATES.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

if __name__ == "__main__":
    build()
