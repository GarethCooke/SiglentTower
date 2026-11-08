# SiglentTower — the MakerWorld listing

Paste the parts below into the MakerWorld upload form. `UPLOAD.md` beside this file says what goes in which box and which files to attach.

---

## Title

SiglentTower — a bench tower for three Siglent instruments: 2020 extrusion, 100 printed parts, a sliding scope, three drawers, a clip-on hex skin and backlighting

## Summary (one line)

An extrusion-and-print bench tower for an SDS1104X-E scope, SDG2082X AWG and SPD3303X-E PSU. Designed in CadQuery with Claude, proven by coupons and boolean checks, built in seven weeks on an X1C. Shared for the ideas and the parts — read "Before you print" first.

## Description

### Read this first — ideas, not a kit

This is **not a model that prints and fits out of the box**. Every printed part on the tower fits a frame of 2020 aluminium extrusion that I cut on a jig and bolted together on the bench, and the parts were fitted to *that* frame as it came out: my rails ended up as much as 6 mm away from the spacer heights, the inner sub-frame sat 2.7 mm right of the model, the PSU's feet were 155.5 mm apart rather than the catalogue figure, and there are small gaps at joints that the connectors could not close. The side tiles were cut to the measured gap on each side; two cradles were reprinted to where the feet actually landed; the sill panel was shortened to the sub-frame as built.

So if you build one, expect your frame to come out differently from mine — by how accurately you cut, how square you pull the joints, which connectors you use — and expect to adjust. The good news is that every part is a Python script with its numbers in one place, so the adjustment is a measurement and a re-export, not a redesign. The GitHub repository (link below) is the real deliverable; this listing is the printable parts, the print profile and the story. Take the ideas: the scope sled with the storage box behind it, the four-quarter drawer joint, the clip-in tiles, the vent-channel drawer, the coupon-first method.

### What it is

Three Siglent instruments on a bench 350 mm wide with shelves directly above and 60 mm free behind — nothing can be lifted out, so everything comes out forwards or sideways:

- **The scope rides a sled.** Printed T-feet in the scope rails' slots carry two split beams; the scope pulls forward 92 mm on them.
- **A storage box rides behind it** on the same sled, for two multimeters and leads, and comes out sideways through a fold-down door in the right-hand skin.
- **Three drawers** on printed runners: a full-width bottom drawer 315 × 300 mm (printed as four dovetailed quarters because the bed is 256 mm), a column drawer beside the PSU and AWG, and a slim slot beside the AWG that leaves its fan a 15 mm air channel.
- **A clip-on skin** of hex-perforated tiles that spring into the extrusion slots, a top panel of four glued half-lapped tiles, and a door on printed hinges with magnet catches.
- **Backlighting**: two addressable LED strips on the rear uprights and two pixels in the front sill with a push button, on my own ESP32-S3 firmware (SiglentGlow, with a web page and Home Assistant over MQTT). Any WS2812 controller would do.

Frame 362 × 350 × 510 mm (525 on its feet with the caps), black 2020, 8 × 1 m plus a pack of four 300 mm. 76 printed designs, 103 pieces, on 36 plates.

### What is in the download

- **SiglentTower-complete.3mf** — every printed part as one Bambu Studio project: 36 plates in filament order (black ABS+ sliding parts first, then ABS, black PETG, dark grey, dark blue, the hidden odds and ends, TPU last), two jig plates at the end, **one material per plate** so there is no purge tower, each plate named for what is on it, each object named after its STL. The print profile is on every plate: 0.2 mm layers, 4 walls, 5 top / 4 bottom, 40 % gyroid, precise Z, no X-Y compensation (clearances are in the parts, not the slicer), outer wall 80 mm/s, scarf seams, supports on but "on build plate only". Brims, ironing and supports are set per object where a part needs them.
- **The STLs**, one per part, in the repository under `parts/` (and the jigs under `jigs/` and `coupons/spacers/`).
- **The paperwork**, in the repository: the as-built record (`HANDOVER.md`, with an index of every part, its material, orientation and hardware), the build log (`ROADMAP.md`), the print rules, the cut sheet, and a check sheet for every assembly.

### Materials

| Filament | Parts | Roughly |
|---|---|---|
| Black ABS+ (one spool for every sliding pair and long thin bar — same shrink on both halves of a pair) | sled T-feet and beams, drawer runners, column guide strips, mini-slot runner | 0.4 kg |
| Black ABS | cradles, cross bars, cable channel, splices, hinges, magnet bracket and tab | 0.3 kg |
| Black PETG | side tiles, door, drawer bodies, top panel, board enclosure | 1.2 kg |
| Dark grey PETG | the three drawer fronts, sled front bar, rear box, sill panel | 0.4 kg |
| Dark blue PETG | pull inserts, upright caps, the logo inlay | under 100 g |
| Natural PETG | the sill window | a few grams |
| Any PETG | strip brackets, box braces, sill blocks (hidden) | under 100 g |
| Blue TPU 95A | four feet, four AWG pads, two sled stop caps, 1.4 m of slot cover | under 60 g |

### Print notes — what actually gave trouble

- **Thin standing parts warp.** The drawer fronts and the four top tiles are 3 mm sheets printed standing on edge (so both faces are wall finish and there is nothing to support). The big bottom-drawer front — 315 × 83 mm, on the diagonal — gave me bed-adhesion trouble: warping at the ends and one spaghetti failure. What fixed it: **more heat and slower speeds** — bed 80 °C, outer wall 60 mm/s, part fan capped at 30 %, a 15 mm outer brim with 0 gap, skirt off, door closed. Those are in the profile per object where the file can carry them (brim, speed); the bed and fan are filament settings you set yourself.
- **Dry the ABS+ and the TPU** before printing; print ABS and ABS+ with the door closed.
- **Counterbores that face the bed** (the cradle cups, the runner bolt holes) use Bambu Studio's *Bridge counterbore holes → Sacrificial layer* — no support inside any fit surface. If the preview shows support on a sliding face, something is wrong.
- **Skirt loops are 0** in the profile: the column drawer, 285 mm on the diagonal, leaves no room for one. Every part that needs first-layer help has a brim.
- **TPU prints last, in one session**, from the external spool holder, no brim, no support, Generic TPU preset.
- **One drawer quarter per plate; the column drawer is about 24 hours.**

### Hardware

- 2020 extrusion, black, 6 mm slot: 8 × 1000 mm + 4 × 300 mm. Cut: 4 × 510, 10 × 310, 2 × 321, 4 × 307 (two used), 2 × 179.5, 3 × 70; ±0.5 mm is fine — the rail heights come from the printed spacers at assembly, not from the cuts.
- 40 hidden L-connectors (inside-corner, grub screw) + 8 cast corner brackets with M5 × 8.
- 54 drop-in (spring) M5 T-nuts; 47 × M5 × 10 button head (4 of them into the uprights' bores for the caps), 9 × M5 × 10 countersunk, 2 × M5 × 12.
- 4 × M3 × 10 (drawer front), 4 × Ø10 × 2 magnets, CA glue (every sled tab, the drawer dovetails, the pull inserts, the top-panel laps).
- Power: a switched 4-way strip with keyhole mounts (mine is an Addtam, 350 × 76 mm), three IEC leads.
- Lighting, if you want it: a WS2812 controller of your choice (mine: XIAO ESP32-S3 Plus, SN74AHCT125 level shifter, SR3200 diode, 1000 µF, 2 × 330 Ω, on 50 × 70 perfboard), 2 × 15-LED WS2812 strips, 2 × 5 mm WS2812D-F5 pixels, an 8 mm momentary button with LED, a USB-A pigtail.

### Build order

Each side of the frame is built flat on the bench with all five of its rails at once, the heights set by the printed spacers and a sled foot already in each scope rail; then the two sides are joined with the rear cross rails and the inner sub-frame slides in from the front. Then: cradles (the seating jigs set them front-to-back), the instruments, the drawers, the sled and its box, the skin, the trim (feet, covers, caps, sill, brackets), the lighting. The repository's `HANDOVER.md` has every level and every part; the `parts/` sheets show each assembly.

### How it was designed

Every part is a CadQuery script, and every script reads its clearances from one file, `fit.py`. Before anything printed full size, nine small coupons set those numbers on rail offcuts: the sliding foot, the cradle cup, the drawer runner, the tile clip, the hinge, the pull, the dovetail joint, the TPU foot, the scope's bumper cup. Three of them changed the design — the cup became a cone, the tile barb doubled and got a 45° hook, the bumper cup turned out to be a D rather than a circle. Every part was then checked against the frame and its neighbours by boolean intersection (0 cm³ in place, then shifted 0.5 mm each way to show it is held) before it went to the printer, and exported in its print orientation with the bed face chosen before modelling, precision surfaces as vertical walls, and overhangs designed out rather than supported.

Claude did the CAD, the proofs and the paperwork — Claude's Cowork for the design and the sheets, Claude Code for the firmware and the as-built record; I measured, decided, printed, assembled and reported back from the bench, and the roadmap was the shared to-do list between us. It worked because the bench's measurements went straight into `fit.py` and the coupons gated the printing. It also made real mistakes that the checks did not catch and the bench did: a bracket drawn with its bolt hole in empty space, a door-set part exported from a mirrored check frame and printed as the wrong hand, three cradle clashes that only showed when the instruments went in. Each became a rule in `PRINT-RULES.md`.

### Links

- Repository (scripts, STLs, sheets, the as-built record): https://github.com/GarethCooke/SiglentTower
- Project page with photos and the interactive 3D model (drag to rotate; sliders move the drawers, sled, box and door): https://garethcooke.com/projects/siglenttower
- Licence: design, documents and media CC BY 4.0; code MIT.

---

## Tags

2020 extrusion, bench, oscilloscope, Siglent, lab equipment, instrument stack, drawer, dovetail, CadQuery, parametric, PETG, ABS, TPU, WS2812, ESP32, Claude

## Category

Tools › Organizers (or Electronics › Enclosures, if that fits the current tree better)
