# Bench stack — as built (v19, 2026-11-03)

Owner: Gareth Cooke (IguanaWare). An aluminium-extrusion stacking frame with 3D-printed parts for three Siglent bench instruments, on a 350 mm-wide bench with shelves directly above, 60 mm free behind, 350 mm free to the right along the front 250 mm of depth.

Status: **built and working** (ROADMAP v2.35, 2026-11-03). This is the record of the tower as it stands and the source for the build guide and the write-up. History is in `ROADMAP.md`; every clearance and measured dimension in `src/fit.py`; print rules in `PRINT-RULES.md`; the cut sheet in `CUT-TABLE.md`; the lighting firmware brief in `SiglentGlow-BRIEF.md`. v18 (2026-09-15, the frozen design) is in git; where the build differs, the as-built value is given with "(v18: …)" after it. The sheet index is §13.

**Coordinates.** All mm. x across from the left upright's outer face, y back from the front plane (the front uprights' front faces), z up from the rail bottoms. The frame stands 6 mm above the bench on its TPU feet. Everything inside the frame sits 3 mm behind the front plane; the drawer facias fill 0–3, flush with the uprights.

---

## 1. Instruments (as measured and used)

| | Front | Body in the frame | Feet / rests | Notes |
|---|---|---|---|---|
| Siglent SDS1104X-E scope | 315 × 152; bezel x 23–338, face at y 3 | body inset 4.7 per side behind the bezel (x 27.7–333.3), underside z 355, top 507 | **Rear bumpers:** D-shaped, 25.9 across × 24.0 deep at 5 mm up (26.4 at the chassis), 14 tall, flat to the rear; centres 44.15 from the bezel side, flat face 116.9 behind the front face (v18: Ø32, 39 from the side, at the rear edge). **Front stands, folded:** main leg 44 × 23.1, 11.5 tall; outer edge 24.7 from the bezel side, leg front 10 behind the face (v18: 44 × 43, 24 from the side) | 2.6–3 kg. IEC bottom-left. On the sled (§4) |
| Siglent SDG2082X AWG | 214 × 88; bezel x 23–237 from z 248, 3.5 proud | 207 × 82 × 260, handle and bumpers off: x 26.5–233.5, y 3–263, z 251.5–333.5 | none: four 20 × 20 × 5.5 TPU pads in the cradle arms | 3.4 kg. Fan vent Ø80 per side centred 123 behind the front (frame y 86–166); the mini slot's vent neck sits beside it (D7) |
| Siglent SPD3303X-E PSU | 225 wide; face x 20–244.5, against the left PSU rail, 6.5 off the inner rail (v18: 3 mm gap) | 220 wide under the face (x 22.25–242.25), 284.5 deep, 301.5 to the knobs | Ø16.8 at the pad, 19.5 at 4 mm up, 21.5 at the flange; 155.5 apart across; 48 from the front, 34 from the rear (y 51 / 253.5); 150 tall on its feet (v18: 149) | 7.5 kg. Fan exhaust centre rear (x ≈ 135.5), kept clear |

Also stored: Brymen BM867s in holster 208.5 × 103.5 × 66 and BM22s 115 × 53 × 12 (rear box); four PP510 probes, BNC and banana leads, the AWG handle and bumpers (bottom drawer); USB sticks, SD cards, probe tips (mini slot); the column drawer is general storage.

## 2. Frame (2020 extrusion, black, 5.9 mm slot mouth)

Overall 362 × 350 × 510 by tape (v18: 361; the model stays 361 and only the top panel is made to 362), 6 of foot below and 6 of cap above. Clear width 321.

**Cut list as cut** (`CUT-TABLE.md`, 2026-09-19): 4 × 510 uprights; 10 × 310 side rails; 2 × 321 rear cross rails; 4 × 307 inner rails (two used, two spare); 2 × 179.5 inner uprights; 3 × 70 ties; one 200 and one whole 300 as coupon rail. From 8 × 1 m plus the CNCMANS 300 mm 4-pack (D1). ±0.5 was enough: the rail heights came from the printed spacers at assembly.

**Levels in the model:** side rails base z 0–20, PSU 68–88, AWG 227.5–247.5, scope 311–331, top 490–510; rear cross rails at base and top; the inner sub-frame of two 307 inner rails (PSU and AWG level) between two 179.5 inner uprights at x 251–271, three 70 ties to the right PSU rail (front, rear) and the right AWG rail (rear). Every part was modelled to these.

**As measured (2026-10-13/14) and what absorbed each difference:**
- Rail gaps by caliper, rail face to rail face — right: base→PSU 45.4, PSU→AWG 139.5, AWG→scope 65.8, scope→top 158; left: 51.2, 135, 65.5, 157 (spacers 48 / 139.5 / 63.5 / 159). The side tiles were reprinted to these bands (§5); the left scope rail's top reads 331.7. Nothing else depends on them.
- The sub-frame's front upright is flush with the front plane, and its left face is at x 253.7 (model 251, set 3 back). Only the sill panel bridges to it, so only the sill panel changed (233.4 long); the column drawer and mini slot are placed from the sub-frame's own rails. The viewer still shows the model position (Stage 9).
- Width 362 by tape: the top panel is 362 wide with 1.5 mm slotted corner holes.

**Connectors as fitted:** 40 hidden L-connectors on the faces that look into the frame (side rails ↔ uprights on the inner faces, rear cross rails on the front faces, inner rails on their right faces, ties on their front faces; never an outer face, where the tile fingers live), and the 8 cast brackets: four under the scope rails, one at each end in the rail's bottom slot at x 3–17 (the scope rails take no hidden connector: the sled feet own the inner slot and the tile fingers the outer), one lying flat between the front tie and the right PSU rail's inner face at y 23–43, three spare. M5 × 8 for every cast bracket, M5 × 10 for every printed part on a drop-in T-nut. **Build method:** each side built flat on the bench with all five rails at once — base and top flush with the upright ends, PSU / AWG / scope rails on the 48 / 139.5 / 63.5 spacers, a sled T-foot already in each scope rail's inner slot — then the sides stood up and joined by the rear cross rails, the sub-frame built as a ladder and slid in from the front (`frame-assembly-3d.html`). Checks 2026-10-01/02: diagonals equal, 321 at the front, 510 overall, no wobble.

**Instruments in the frame.** PSU on four cradles on the PSU rails: left pair v3 (cups at x 61.75), right rear v4 (217.25), right front v5 (213.25) — set on the bench 2026-10-03 to where the feet land, so the PSU sits very slightly skewed (accepted). AWG on four cradles at the AWG rails — left v2 saddles, right v2 brackets on the inner rail's left face — with 5 mm arms flush with the rail top (v1: 8, which touched the PSU) and TPU pads 4 proud; its underside is 3 over the PSU top. The seating jigs (§10) set every cradle front-to-back; fronts in line, no rock.

## 3. Levels (as built)

| Item | x | y | z | Notes |
|---|---|---|---|---|
| Feet, base rails | | | feet −6–0, rails 0–20 | TPU feet 24 × 24 × 6 glued into the uprights' bores |
| Bottom drawer | 23–338 | body 3–303, facia 0–3 | body 3–63, facia 3–86 | 315 × 60 × 300 in four quarters |
| Sill panel | 20–253.4 | 0–3 | 87–99 | button at x 45, window 32–58; blocks behind, y 3–19.5 (v18: 321 wide) |
| PSU | face 20–244.5 | 3–287.5 | feet in cups at 92, top ≈ 242 | cup floors 4 above the rail top; AWG arms' underside 242.5 |
| Column drawer | body 274–338, facia 273–338 | 3–288 | body 91–331, facia 91–336 | 64 × 285 × 240 (v18: 65 × 240 × 300) |
| AWG | body 26.5–233.5, bezel 23–237 | 3–263 | body 251.5–333.5, bezel from 248 | on pads 4 proud of the 5 mm arms |
| Mini slot | 242–268 | 3–288 | body 252.8–331, facia 248–336 | 26 wide, 285 deep (v18: 180); 16-wide neck over y 81–171 |
| Housing tops | — | — | — | none (D14; v18: 64–67 and 333–336) |
| Scope rails | 0–20 / 341–361 | 20–330 | 311–331 | T-feet in the inner slots; hinge frame leaves on the right rail's outer face |
| Sled beams, front bar | 20.5–60 / 301–340.5 | 12–330; bar 0–12 | 337–346; bar 337–355 | 1 mm over the AWG bezel at 336 |
| Scope | bezel 23–338 | face at 3 | cup floors 341, chassis 355, top 507 | stands in 2.5 pockets (floor 343.5); the cups locate it, the pockets level it |
| Rear box | 50–341 | 195–330 | 346–456 | on the cross bars between their lips |
| Cable channel | 20.5–47 | 201–334 | 346–366 | on the left beam |
| Door / fixed rear tile | face 361–364 | 20–250 / 250–330 | 338–499 / 334–500 | hinge axis x 369, z 341 (v18: door 347–490, axis x 362) |
| Side tiles | on the rails' outer faces | 20–175, 175–330 | rail centreline to rail centreline; band 4 left 335–500 | tiles cover the rails (v18: between them) |
| Top panel, caps | 0–362 | 0–350 | 510–513; caps 513–519 | on the uprights and the three top rails (v18: 321 × 310 between the caps) |

Reveals: 3 from the front plane to everything inside, 3 from the scope top to the panel. PSU and AWG left, scope centred, column right.

## 4. Scope sled (as built)

- **T-feet:** two 210-long inverted-T feet, black ABS+, in the scope rails' inner side slots at y 119.5–329.5 (home). Neck 5.3 in the 5.9 mouth, flange 10.0 in the 10.6 cavity (0.3 a side, P1); a 2.5 web rises beside the upright with a 4 mm rib on its top edge that threads into a closed dovetail groove under the beam — the web belongs to the foot (v18: to the beam). Foot and beam bonded. Minor rock in the slot, accepted.
- **Beams:** two 39.5 × 9 bars at x 20.5–60 and 301–340.5, z 337–346, y 12–330, each split at y 165 into a front half (v2) and a rear half (v1) on a P7 tab, CA'd (D6). The front half carries the rear-bumper D cup (25.9 × 24 + 0.3, 6 deep, floor 341, flat to the rear) and the front-stand pocket (44 × 23.1 + 0.6 / 1.0, 2.5 deep, open at the front); the rear half the cross-bar sockets. Two Ø4 pegs on the left beam's top at (33, 150) and (33, 290) key the splice and the channel. (v18: Ø32.6 cups on arms, lipped front pads.)
- **Front bar v3:** 315 × 12 × 18 at y 0–12, z 337–355, dark grey PETG, 120 × 6 pull notch lined in blue. Each beam's front edge carries a 68 mm tongue (x 28–96 and mirror) that enters a closed pocket in the bar's rear face as the bar slides on from the front, so the stand pad's edge is held above and below; 25.5 × 76 saddles lie on the beams behind the bar, CA'd (the M3 holes unused). This stops the beams rolling inwards under the scope.
- **Cross bars v2:** between the beams at y 190–210 and 308–335, z 337–346, black ABS, P7 tabs CA'd; guide lips at y 189–194 (chamfered at the right end) and 331–336 hold the box with 2 mm of play.
- **Front rests v2:** a 3 mm plate on each scope rail's top at y 21–61, one M5 × 10 countersunk into the top slot, with a lip rising to z 337 beside the rail's inner edge; the beam's outer wall rides on it through the whole travel, so the front is carried under the stand as the rear is on the foot. Six STLs with the lip sized to a rail-to-beam gap of 0.5–3.0; **the 3.0 is fitted** on both rails (Gareth, 2026-11-03 — the largest, the measured gap at the front).
- **Splice bars v2:** 100 × 25.5 × 7.5 CA'd along each beam's outer strip at y 88.5–188.5, bridging the P7 joint and the span ahead of the foot (the front still sagged on the rests alone). The right one stands in the box's exit lane: the box is lifted 7.5 as it crosses the right beam.
- **Cable channel v1:** a U-trough on the left beam, x 20.5–47, y 201–334, floor 346, walls to 366, 20.5 inside for the scope's mains, LAN and USB; front top corners chamfered 10; rear end open into the loop behind the frame; keyed by the (33, 290) peg, CA'd. (v18: from y 140 with wedge tabs and a rear ramp, both dropped.)
- **Travel 92** (v18: 100): home is the foot against the rear upright; a TPU stop cap (8 mm of cover profile) pressed into the front end of each scope rail's inner slot takes the foot at full pull. No T-nut stops. Level, stops hold (2026-10-23). PTFE dry lube.
- **Rear box v1:** 291 × 135 × 110 (x 50–341, y 195–330, z 346–456), dark grey PETG, two halves split at x 195.5 and joined like the drawer quarters, 20 mm front lip, full rear and side walls; 15 × 15 × 4 × 100 corner braces CA'd into both front corners after the right wall cracked at the lip.

Access sequence, confirmed 2026-10-23: sled out to the stops → door down → box lifted over the splice and out to the right → reverse. The meters fit.

## 5. Panels and door

- **Side skin, 14 tiles:** 3 mm black PETG, 4 / 5 mm solid border, hexes 8.4 across corners on 2.5 webs, face down on the textured plate. Tiles run from one rail's slot centreline to the next and cover the rails (v18: between them), 155 long (y 20–175 and 175–330, D4), clipped into the rails' outer slots by P4 spring fingers — a 25 × 5.5 finger cut free by a 1 mm slit, a 5.1 peg with a 1.2 barb hooking the lip at 45°, a 5.7 root stub filling the mouth — two per shared edge interleaved with the neighbour's, three on band 1's base edge. Band heights as measured: left 71.2 / 155 / 85.5, right 65.4 / 159.5 / 85.8 (v18: 48 / 139.5 / 63.5 / 143). The left band-2 and band-3 tiles have notches, open to their bottom edges and 11 above the rail top, round the PSU and AWG cradle saddle walls; band 3 right has windows for the hinge plates; band 2 right keeps its v1 tiles (that gap matched the model). **Band 4 left** (z 335–500, v1): three fingers up into the top rail's slot and a 19 × 3 × 40 leg on each tile's upright end, one M5 × 10 + T-nut into the upright's face at z 361 (the sled band below has no rail).
- **Door set (band 4 right):** door v3, 230 × 161 × 3, y 20–250, z 338–499, edge 7 above the scope rail (v18: 347–490); two 12 × 12 × 3 magnet bosses printed on its back at (y 34 / 236, z 479); a 45 × 12 finger slot at (135, 482) to hook it open (v18: notch in the top border). **Hinge (D11):** axis x 369, z 341 (v18: x 362, through the panel); two frame leaves v2 — 6 mm plates on the right scope rail's outer face at y 23–47 / 223–247, one M5 × 12 + T-nut each into the outer slot at z 321, riser at x 364.3 — and two door leaves v2 CA'd to pads on the door's back with a shelf under its edge; Ø2.9 × 24 printed pins CA'd into the door leaf's segments, the frame leaf's middle segment turning on them. Opens past 180, hangs ~10 proud of the tile below. **Fixed rear tile v2:** 80 × 166 × 3, y 250–330, z 334–500, two fingers into the top rail and a leg on the rear-right upright's front face (M5 × 10 + T-nut at z 361). **Catch:** two Ø10 × 2 magnet pairs, CA'd, faces 0.5 apart — the door's bosses against a front bracket (an L on the front-right upright's rear face, M5 × 10 + T-nut at z 461, tongue into the top rail's bottom slot) and a rear tab CA'd to the fixed tile's back.
- **Top panel (D12):** 362 × 350 × 3 at z 510–513 over the whole frame top (v18: 321 × 310 between the caps, on nothing). Four 185.5 × 180 tiles printed standing meet on 10 mm half-laps (left / front tongue under, right / rear over), CA'd on the frame into one sheet; no H-spline. Four dark blue 20 × 20 × 6 caps on the corners, each with an M5 × 10 button head through the panel into the upright's centre bore.
- **No drawer lids** (D14; v18: housing tops). Rule of use: drawer contents stay below the wall tops — bottom drawer 63 under the PSU cradle arms at 68, column 331 under the right beam at 337.

## 6. Storage and pulls

- **Bottom drawer:** 315 × 60 × 300 in four quarters (D2) joined by floor puzzle-dovetail tabs and vertical sliding dovetails at the wall crossings (0.15, P7), the wall dovetails CA'd. It hangs on two 300 L-runners (black ABS+) bolted down into the base rails' top slots, four M5 × 10 each; a 7 mm rib on each rides in a house-shaped groove in a 10 × 20 boss along the drawer's outer walls (P3, 0.3). Facia 315 × 83 × 3 dark grey, four M3 × 10 from inside plus CA, the iguana inlaid 0.8 deep top-right in dark blue (58.7 × 21.1, head right). Removal = pull clean off the ribs at full travel (D15; v18: lift-off runners, rear stop).
- **Column drawer:** 64 × 285 × 240 (D5; v18: 65 × 240 × 300) at x 274–338, black PETG, on four 260 guide strips (black ABS+, y 45–305, four M5 × 10 each; the left lower one is a 140 short strip on two M5 between the right PSU cradles' lips): the PSU-level pair carries it on P3 ribs, the AWG-level pair only catches it if it tips. Facia 65 × 245 × 3 dark grey on two Ø3.2 pegs into the body's front-wall holes, CA, no screws. Comes out 215 (left) / 243 (right), then pulls clean off. The front wall's top 29 mm was cut out by hand on the printed v1 body for the insert's leg (the v3 STL has the window).
- **Mini slot:** 26 × 285 × 78 (D7; v18: 26 × 83 × 180) at x 242–268, black PETG, on a 12-wide ABS+ runner on the inner AWG rail's top (three M5 × 10 countersunk, heads sunk 1 below the plate top, v3) with a dovetail rib; the left wall steps in to x 252 over y 81–171, leaving a 15 mm air channel beside the AWG's vent. Travel 250 to a bump; removal = three M5 out, drawer and runner forward together. Facia 26 × 88 × 3 dark grey on pegs. Thermal check passed 2026-10-23: all three instruments on for over an hour, AWG fan normal, the slot's right wall slightly warm.
- **Pulls (D9, P6):** each facia has a notch in its top edge and a separate dark blue insert glued in flush — a 3 mm face with a 12-tall slot (v18: 10) 80 / 40 / 16 wide, a 5 mm hook strip above it, a 17-deep pocket with a 30° floor, 2 mm walls. v2 inserts carry a 2 mm flange behind the face that bears on the facia's back and hooks over the drawer body's front wall with a 20 mm leg, so a pull loads the facia, not the glue. The sled bar's 120 × 6 notch takes a 1.5 mm blue liner.
- **Probe hanger:** not built, by choice — add later only if use asks for it (v18: keyhole bar on the front-left upright).

## 7. Cable management, power and lighting

- **Power strip (D8):** the Addtam 4-way (350 × 78.1; keyholes 249.5 apart on a line 29.2 from one edge, measured 2026-09-17) hangs vertically on the rear face of the rear-left upright, sockets to the wall, cable end down: body x 1–79, y 355–385, z 75–425, on two brackets bolted into the upright's rear slot (M5 × 10 + T-nut each; pegs at z 95 and 344.5 into the keyholes; the lower bracket's U-shaped shelf takes the weight round the Ø15 mains cable). As fitted they are the yellow PETG prints of upper v1 / lower v4 with the bolt hole drilled by hand (Ø5.5 + Ø10 × 2.5 counterbore): no export before upper v2 / lower v5 (2026-10-23) had one. Three 0.5 m IEC leads run up the rear-left corner. No front mains switch.
- **Scope leads:** mains, LAN and USB rearward in the sled's channel, then a loop behind the frame that takes the travel. **AWG / PSU LAN and USB:** down the rear-right corner, loose — the rear-right cable clips (v18 open item 4) were not built, by choice.
- **Sill panel (D10):** a dark grey PETG strip 233.4 × 3 × 12 at x 20–253.4, z 87–99 (v18: 321 wide), standing between the drawer facia and the PSU, with a 26 × 12 natural PETG window at x 32–58 round the Ø8.4 button hole at x 45. It presses onto Ø3.2 pegs in two blocks: **left block v10** (x 20.3–68, white PETG; one M5 × 10 along x into the left upright's inner-face slot, driven through a key hole from the block's right end; a captive 10 AF nut pocket behind the window; two Ø5.7 pixel bores from the back face into a light cavity behind the window; two clip rails on the back face for the pixel wires; a 3.2 wire slit from the bottom face up to the button's axis, so the pre-wired button goes in from the front) and **right block v4** (x 223.4–253.4; M5 × 10 into the sub-frame upright's left face, key slot from the block's left end). The printed v3 window was notched 3.2 × 1.8 by hand under its hole to match; `sill_panel.py` regenerates that window as v4 (the STL is not kept). Everything behind the button's bezel fits in the 16.5 between the panel and the PSU cradle arm.
- **Lighting as built, D10 rev 5** (v18 / rev 2: XIAO + WLED in the end block; rev 3: D1 mini + WLED in a holder — both superseded). Sheets: `parts/wiring/wiring-4-connections.png`, `wiring-2-runs.png`, `perfboard-layout.png`, `board-enclosure-plan.png`.
  - **Controller:** a Seeed XIAO ESP32-S3 Plus running **SiglentGlow** (Gareth's own firmware on IguanaPlatform, the MorayGlow architecture; `C:\Development\Projects\SiglentGlow`, built 2026-10-25) on a 50 × 70 perfboard with an SN74AHCT125N level shifter on both data lines, an SR3200 Schottky feeding the XIAO's 5 V pin, a 1000 µF across 5 V / GND at the USB input and 330 Ω in each data line. The LEDs take 5 V straight from the pigtail, never through the XIAO. Four crimped 2.54 mm locking plugs: 2-pin PWR (USB pigtail, board top edge), 5-pin sill (5 V, data, data back, GND, switch), 3-pin L, 3-pin R. Colours: red 5 V, black GND, green data, blue data back, yellow switch.
  - **Pins:** D0 (GPIO1) = bus 1: sill pixel 1 → sill pixel 2 → left strip, 17 LEDs; D1 (GPIO2) = bus 2: right strip, 15; D4 (GPIO5) = button to GND. Short press on / off; hold 5 s = factory reset (the sill pixels count down in red). Current limit 1500 mA. Set-up: join `SiglentGlow-XXXXXX` (password `siglentglow`), pick the network, open `siglentglow.local`; MQTT / Home Assistant on `/settings.html`; updates over Wi-Fi.
  - **Strips:** two WS2812B strips of **15 LEDs each** (30/m; v18: 28 at 60/m) on the rear uprights' inner faces from z 20 upward, fed at the bottom, the top end bent under the top rail.
  - **Sill pixels and button:** two WS2812D-F5 5 mm pixels (legs DOUT, VDD, GND, DIN — the reverse of the APA106) pushed into the left block from the rear, pre-wired, wires in the clip rails; both light the window past the nut. The button is an 8 mm momentary with a blue LED, four pins: LED + to 5 V, LED − and switch 2 linked to GND, switch 1 to the yellow wire.
  - **Enclosure:** `board-enclosure-v1` + `board-lid-v1`, black PETG, on the rear base rail's rear face at x 90–150, z 0–111, one M5 × 10 + T-nut into the rail's rear slot at (120, 10). The board stands on a ledge at z 28 in slots in the side walls, components rearward, over a 25 mm wire bay; the hex-vented lid slides down behind it with a flange closing the top and a notch for the USB lead. To unplug anything: lid up, pull the housing off its header; the board lifts out past the leads.
  - **Runs** (every wire in a slot but the USB lead): the five-wire sill bundle (650) leaves the block's bottom at x 34–58, drops into the left PSU rail's inner-face slot (TPU cover A, y 45–305), down the rear-left upright's inner slot under the strip, under the rail at x 23–28, along the rear base rail's rear slot (cover B1, x 25–90) and through the enclosure's left passage to the 5-pin; the left strip feed (200) goes back the same way up to the strip's input at z 20; the right strip feed (320) runs along the rear base rail's rear slot (cover B2, x 150–336), under the rail at x 333–338 and up the rear-right upright's inner slot; the USB pigtail (550, red + braid) from the Addtam's top-end port runs down beside the strip, in the open, through the lid's notch. Plug or unplug only with the supply off.

## 8. Materials and colours (as used)

Bambu X1C, 0.2 mm, process profile `SiglentTower fit 0.20` (4 walls, 40 % gyroid, no X-Y compensation, supports on the build plate only), textured PEI. Cradles print saddle-top down with Bambu's sacrificial layer over the cup and counterbores; facias and the top tiles stand on a long edge with the thin-part settings (brim 15, skirt off, door closed, bed 80, fan ≤ 30 %); tiles and fronts face down; nothing is supported inside a part. (v18: ASA for the black parts, cradles cup-up, top tiles flat.)

| Material | Parts |
|---|---|
| Black ABS+ — one reserved spool, dried, 5 mm outer brim: sliding pairs and long thin bars | sled T-feet, four beam halves, bottom-drawer runners, four column guide strips, mini-slot runner |
| Black ABS — fixed black parts | PSU and AWG cradles, cross bars, cable channel, hinge leaves, magnet bracket and tab, splice bars (ABS or PETG) |
| Black PETG | side tiles, band 4 left, door, fixed rear tile, top tiles, drawer quarters, column drawer, mini-slot body, front rests, hinge pins, board enclosure and lid |
| Dark grey PETG | three facias, sled front bar, rear box, corner braces, sill panel |
| Dark blue PETG | pull inserts, sled-bar liner, logo inlay, upright caps |
| Natural PETG; white PETG | sill window; sill blocks |
| Blue TPU 95A — printed once, last, on one plate | frame feet, AWG pads, sled stop caps, slot covers |
| Yellow PETG | coupons, jigs, the strip brackets as fitted |

## 9. Known compromises

1. The PSU sits very slightly skewed: right front cup at x 213.25, right rear at 217.25, left pair at 61.75, set to where the feet land (accepted 2026-10-16).
2. The sub-frame upright is 2.7 right of the model and flush with the front; absorbed by the sill panel, still wrong in the viewer.
3. The rails are not at the spacer heights (§2); the tiles were reprinted to the measured bands, and the cradle saddles' walls, 10 above the rail top, needed notched left tiles.
4. The sled's front hangs 108 past the foot and bent under the scope; it is carried on the front rests and stiffened by the splice bars, and the travel is 92, not 100. The foot has minor rock in its slot.
5. The right splice stands in the rear box's exit lane: the box is lifted 7.5 over it on the way out.
6. The strips are 15 LEDs each, dimmer than the 28 planned; the slot covers' 7.4 flare leaves 3.65 under them for cable.
7. Hand work on the tower: the sill window's notch, the strip brackets' bolt holes, the column body's front-wall window, the splice bars cut to 100.
8. The rear box's right wall cracked at the lip and is braced; the front bar's saddle screws are unused (glued only); the hinge pins are 2.9 in a 3.2 bore, glued into the door leaves; the door hangs ~10 proud of the tile below at 180°.
9. No drawer lids and no drawer stops (D14, D15): contents stay below the wall tops, and a hard pull puts a drawer in the hand.
10. 1 mm between the beams' underside (337) and the AWG bezel (336): nothing can ever go under the beams.
11. Not built, by choice: the probe hanger and the rear-right cable clips.

## 10. Parts index

Every printed part on the tower. Orientation is as exported (z = 0 on the bed); "+ T" = with a drop-in M5 T-nut. Scripts are in `src/parts/`, STLs in `parts/`.

| Part | Fitted | Script | STL | Material | Qty | Orientation | Hardware |
|---|---|---|---|---|---|---|---|
| Frame foot | v1 | tpu_parts.py | tpu/frame-foot-v1 | blue TPU | 4 | pad down, spigot up | glued into the upright's bore |
| Upright cap | v1 | top_panel.py | top/upright-cap-v1 | dark blue PETG | 4 | closed face down | M5 × 10 into the bore |
| Slot cover 240 | v1 | tpu_parts.py | tpu/slot-cover-240-v1 | blue TPU | 6 (runs A 240 + 20, B1 65, B2 186) | flat, head up | press-fit |
| Strip bracket upper | v1 print; v2 STL | strip_bracket.py | strip-bracket-upper-v2 | yellow PETG | 1 | plate face down | M5 × 10 + T, rear-left upright rear slot, z 344.5 |
| Strip bracket lower | v4 print; v5 STL | strip_bracket.py | strip-bracket-lower-v5 | yellow PETG | 1 | plate face down | M5 × 10 + T, z 95 |
| PSU cradle left | v3 | psu_cradle.py | psu-cradle-v3 | black ABS | 2 | saddle top down, sacrificial layer | 2 × M5 × 10 + T each, left PSU rail top slot |
| PSU cradle right rear | v4 | psu_cradle.py | psu-cradle-right-v4 | black ABS | 1 | same | 2 × M5 × 10 + T, inner rail top slot |
| PSU cradle right front | v5 | psu_cradle.py | psu-cradle-right-front-v5 | black ABS | 1 | same | 2 × M5 × 10 + T |
| AWG cradle left | v2 | awg_cradle.py | awg-cradle-left-v2 | black ABS | 2 | standing on its end | 2 × M5 × 10 + T each, left AWG rail top slot |
| AWG cradle right | v2 | awg_cradle.py | awg-cradle-right-v2 | black ABS | 2 | arm top down | 2 × M5 × 10 countersunk + T each, inner AWG rail left face |
| AWG pad left / right | v1 | tpu_parts.py | tpu/awg-pad-left-v1, awg-pad-right-v1 | blue TPU | 2 + 2 | left pad down; right on its front face | in the arm pockets |
| Bottom drawer quarter | v1 | drawer_quarters.py | drawer/drawer-Q1-v1 … Q4 | black PETG | 4 | floor down, one per plate | CA on the wall dovetails |
| Bottom drawer runner | v1 | drawer_runner.py | drawer/drawer-runner-300-v1 | black ABS+ | 2 (one STL, turned) | leg top down, diagonal, ironing on | 4 × M5 × 10 + T each, base rail top slot |
| Bottom facia + logo | v1 | drawer_facia.py, logo.py | drawer/drawer-facia-v1 + drawer-facia-logo-v1 | dark grey + dark blue PETG | 1 | standing on its bottom edge, diagonal | 4 × M3 × 10 from inside + CA |
| Pull insert, bottom | v2 | pull_inserts.py | inserts/pull-insert-bottom-v2 | dark blue PETG | 1 | face down, supports on plate only | CA |
| Column drawer | v1 print (window cut by hand); v3 STL | column_drawer.py | column/column-drawer-v3 | black PETG | 1 | floor down, diagonal, 5 mm brim | none |
| Column guide strip upper | v1 | column_drawer.py | column/column-strip-upper-v1 | black ABS+ | 2 | rail face down, diagonal | 4 × M5 × 10 + T each, AWG-level side slots |
| Column guide strip lower right | v1 | column_drawer.py | column/column-strip-lower-v1 | black ABS+ | 1 | same | 4 × M5 × 10 + T, right PSU rail inner face |
| Column guide strip lower left (short) | v1 | column_drawer.py | column/column-strip-lower-short-v1 | black ABS+ | 1 | same | 2 × M5 × 10 + T, inner PSU rail right face |
| Column facia | v1 | column_facia.py | column/column-facia-v1 | dark grey PETG | 1 | standing on its long edge, thin-part settings | pegs + CA |
| Pull insert, column | v2 | pull_inserts.py | inserts/pull-insert-column-v2 | dark blue PETG | 1 | face down | CA |
| Mini-slot body | v1 | mini_slot.py | mini/mini-slot-body-v1 | black PETG | 1 | floor down, diagonal, 5 mm brim | none |
| Mini-slot runner | v3 | mini_slot.py | mini/mini-slot-runner-v3 | black ABS+ | 1 | plate down, diagonal, ironing on | 3 × M5 × 10 countersunk + T, inner AWG rail top slot |
| Mini-slot facia | v1 | mini_slot.py | mini/mini-slot-facia-v1 | dark grey PETG | 1 | standing on its long edge | pegs + CA |
| Pull insert, mini | v2 | pull_inserts.py | inserts/pull-insert-mini-v2 | dark blue PETG | 1 | face down | CA |
| Sled T-foot | 210 | sled_foot.py | sled-foot-210 | black ABS+ | 2 | standing, layers along the slide, outer brim | bonded into the beam |
| Sled beam front half | v2 | sled_beam.py | sled-beam-left-front-v2, sled-beam-right-front-v2 | black ABS+ | 1 + 1 | flat, top up, outer brim | CA at the P7 tab |
| Sled beam rear half | v1 | sled_beam.py | sled-beam-left-rear-v1, sled-beam-right-rear-v1 | black ABS+ | 1 + 1 | flat, top up | CA |
| Sled front bar | v3 | sled_bars.py | sled-front-bar-v3 | dark grey PETG | 1 | front face down, diagonal, brim | CA on tongues and saddles |
| Sled-bar pull liner | v1 | pull_inserts.py | inserts/sled-bar-pull-liner-v1 | dark blue PETG | 1 | as plated | CA |
| Cross bar front / rear | v2 | sled_bars.py | sled-cross-bar-front-v2, sled-cross-bar-rear-v2 | black ABS | 1 + 1 | flat, lips up, outer brim | CA on the tabs |
| Sled front rest | v2, gap 3.0 | sled_front_rest.py | sled-front-rest-v2-gap<g> | black PETG | 2 (one STL, turned) | bottom face down | M5 × 10 countersunk + T each, scope rail top slot |
| Sled splice bar | v2 | sled_splice.py | sled-splice-v2 | black ABS / PETG | 2 | flat | CA |
| Cable channel | v1 | cable_channel.py | cable-channel-v1 | black ABS | 1 | floor down | CA over the beam's peg |
| Sled stop cap | v1 | tpu_parts.py | tpu/sled-stop-cap-v1 | blue TPU | 2 | flat | press-fit in the slot's front end |
| Rear box half | v1 | rear_box.py | rear-box-left-v1, rear-box-right-v1 | dark grey PETG | 1 + 1 | floor down, outer brim | CA on the seam |
| Box corner brace | v1 | box_brace.py | box-brace-v1 | grey PETG | 2 | lying on the wall leg | CA |
| Side tile band 1 | v2 | side_tile.py | tiles/tile-band1-LF-v2, -LR-v2, -R-v2 (×2) | black PETG | 4 | face down | clips |
| Side tile band 2 | left v2, right v1 | side_tile.py | tiles/tile-band2-LF-v2, -LR-v2, -RF-v1, -RR-v1 | black PETG | 4 | face down | clips |
| Side tile band 3 | v2 | side_tile.py | tiles/tile-band3-LF-v2, -LR-v2, -RF-v2, -RR-v2 | black PETG | 4 | face down | clips |
| Side tile band 4 left | v1 | band4_left.py | tiles/tile-band4-LF-v1, -LR-v1 | black PETG | 2 | face down, one per plate | top fingers; M5 × 10 + T per leg |
| Door | v3 | door_set.py | door/door-v3 | black PETG | 1 | face down | 2 magnets; CA to the door leaves |
| Fixed rear tile | v2 | door_set.py | door/rear-tile-v2 | black PETG | 1 | face down | top fingers; M5 × 10 + T (leg) |
| Front magnet bracket | v2 | door_set.py | door/magnet-bracket-front-v2 | black ABS | 1 | plate face down | M5 × 10 + T at z 461; magnet |
| Rear magnet tab | v2 | door_set.py | door/magnet-tab-rear-v2 | black ABS | 1 | on its back | CA; magnet |
| Hinge door leaf | v2 | door_hinge.py | hinge-door-v2 | black ABS | 2 | standing | CA to the door; pins |
| Hinge frame leaf | v2 | door_hinge.py | hinge-frame-v2 | black ABS | 2 | standing | M5 × 12 + T each, scope rail outer slot, z 321 |
| Hinge pin | v1 | hinge_pins.py | door/hinge-pins-v1 (two) | black PETG | 2 | standing on the disc | CA into the door leaf |
| Top tile FL / FR / RL / RR | v1 | top_panel.py | top/top-tile-FL-v1 … RR | black PETG | 4 | standing on the front / rear edge, thin-part settings | CA on the laps |
| Sill panel + window | v3 (window hand-notched to v4) | sill_panel.py | sill/sill-panel-v3; window regenerated by the script | dark grey + natural PETG | 1 | standing on its bottom edge, brim | pegs; the button's nut |
| Sill block left | v10 | sill_panel.py | sill/sill-block-left-v10 | white PETG | 1 | front face down | M5 × 10 + T; button + 10 AF nut; 2 pixels |
| Sill block right | v4 | sill_panel.py | sill/sill-block-right-v4 | white PETG | 1 | front face down | M5 × 10 + T |
| Board enclosure | v1 | board_enclosure.py | wiring/board-enclosure-v1 | black PETG | 1 | plate face down | M5 × 10 + T, rear base rail rear slot |
| Board lid | v1 | board_enclosure.py | wiring/board-lid-v1 | black PETG | 1 | outer face down | gravity (CA if it walks) |

Counted from this table: 47 M5 × 10 button / cap head (4 into the uprights' bores, no T-nut), 9 M5 × 10 countersunk, 2 M5 × 12, 54 T-nuts, M5 × 8 for the cast brackets, 4 M3 × 10, 4 Ø10 × 2 magnets, the button and its nut.

**Plates** (STLs that bundle parts for one print): `cradles-v2-plate` (src/cradle_plate.py), `sled-absplus-plate` (src/sled_plate.py), `inserts/pull-inserts-plate-v3`, `tiles/tiles-plate-A2…E2` (src/tiles_plates.py) and `tiles-plate-D` / `E` (v1, kept for the band-2 right tiles), `top/top-plate-v1`, `tpu/tpu-plate-v1`. Per-night Bambu projects are under `bambu/`.

**Withdrawn** (superseded files; † = still in the tree):

| File | Replaced by |
|---|---|
| awg-cradle-left-v1 †, awg-cradle-right-v1 † | the v2 cradles (arms 5, plate 4) |
| psu-cradle-v3 as the right pair † (stays as the left pair) | psu-cradle-right-v4 (rear), psu-cradle-right-front-v5 (front) |
| column/column-drawer-v1 †, column-drawer-v2 | column-drawer-v3 (the v1 print stands, window cut by hand) |
| column/column-pull-insert-v1 †, drawer/drawer-pull-insert-v1 †, inserts/pull-insert-column-v1, pull-insert-mini-v1, pull-inserts-plate-v1 / v2 | inserts/pull-insert-*-v2, pull-inserts-plate-v3 |
| door/door-v1 † (printed and fitted first), door-v2 | door/door-v3 |
| door/rear-tile-v1, magnet-bracket-front-v1, magnet-tab-rear-v1 (printed as the wrong hand); door/rear-tile-v2.3mf † | the v2 STLs |
| hinge-door-v1, hinge-frame-v1 | hinge-door-v2, hinge-frame-v2 |
| mini/mini-slot-runner-v1, -v2 | mini-slot-runner-v3 |
| sled-beam-left-front-v1 †, sled-beam-right-front-v1 † | the v2 front halves |
| sled-front-bar-v1, sled-front-bar-v2 † | sled-front-bar-v3 |
| sled-cross-bar-front-v1, -rear-v1 | the v2 bars |
| sled-skid-v1 and its plan; front rest v1 (never exported) | sled-front-rest-v2 |
| sled-splice-v1 (111.5 long) | sled-splice-v2 (the printed pair cut to 100) |
| sled-front-rest-v2-gap0.5 … gap2.5, the five unused gaps † | sled-front-rest-v2-gap3.0 |
| sill-panel-v1, -v2; sill-panel-window-v1…v4; sill-block-left-v1…v9; sill-block-right-v1…v3 | sill-panel-v3, left block v10, right block v4 |
| strip-bracket-upper-v1, lower-v2 / v3 / v4, strip-brackets-plate | upper-v2, lower-v5 (with the bolt hole) |
| tile-band1-v1, band2-LF / LR-v1, band3-LF / LR / RF / RR-v1; tiles-plate-A / B / C / F | the v2 tiles; plates A2–E2 |
| wiring/board-holder-v1, wiring-1-schematic.png, wiring-3-board.png, breadboard-test.png | board-enclosure-v1 + lid; wiring-4-connections, perfboard-layout, board-enclosure-plan |
| tpu/spigots-sweep-v1 †, cover-sweep-7.0 / 7.4 / 8.0-v1 † | test pieces on the TPU plate, not fitted (4.6 and 7.4 held) |
| scope-tray-plan.png † (D13); sled-mechanism-v2.pdf; page 2 of bench-stack-layout-v15.pdf | withdrawn 2026-10-15; the sled sheets (§13) and this document |

**Jigs** (tooling, all printed in yellow PETG):

| Jig | Script | File | Use |
|---|---|---|---|
| Rail-height spacers 48 / 139.5 / 63.5 / 159 (two each) + the 3.0 web gauge | src/coupons/spacers.py | coupons/spacers/spacers-plate | set the rail gaps in the flat side build; the gauge checks the 3 mm sled-web gap |
| Seating jigs PSU L / R, AWG L / R + four PETG AWG pad stand-ins | src/jigs/seating_jigs.py | jigs/seating-jigs-plate | set each cradle front-to-back at the instrument's foot spacing |
| P9 position jigs (bumper, stand) | src/coupons/p9_position_jig.py | coupons/p9/p9-jigs-plate | measured where the scope's feet sit (`fit.py` BUMPER_X_FROM_SIDE 44.15, BUMPER_REAR_FROM_FACE 116.9, STAND_X_FROM_SIDE 24.7, STAND_FRONT_FROM_FACE 10) |
| Band-3 right sweep +4 / +5 / +6 | src/parts/side_tile.py --band3-sweep | coupons/p4/band3-right-sweep | test strips for the right band-3 height; the caliper readings replaced it |

## 11. Coupon results (P1–P9)

| Coupon | Tested | Rounds | Pass | Sets in `fit.py` |
|---|---|---|---|---|
| **P1** sled foot + web | 40 mm of T-foot in the scope rail's inner slot, the web through the 3.0 gauge, a beam stub on the rib | v1–v3 from the slot measured 2026-09-19 (mouth 5.9, lip 1.75, cavity 10.6, throat 4.45, depth 6.15), v3 at 0.2 tight; v4 sweep 0.3 / 0.4 / 0.5 in yellow PETG (2026-09-20); ABS+ confirm 2026-09-21 | 0.3: slides the length of the slot, cannot lift out, minor rock | SLOT_CLR 0.3, FLANGE_GAP 0.3, SLOT_FOOT_W 5.3, FOOT_FLANGE_W 10.0, WEB_T 2.5, WEB_RIB_CLR 0.2, FOOT_STANDOFF 2.2 |
| **P2** PSU cradle | saddle on the rail, foot in the cup, M5 × 10 into a T-nut | v2 2026-09-17: saddle and bolts pass, straight Ø21.6 cup 2 mm loose; v3 conical cup, rounds A (0.5 / 0.6 / 0.7, all loose) and B (0.1 / −0.1 / −0.3) | 2026-09-17: 0.1 net, no shrink allowance | RAIL_CLR 0.4, CUP_CLR 0.1, PSU_FOOT_PAD_D 16.8, PSU_FOOT_D4 19.5, HOLE_SHRINK 0.3 (straight bores only) |
| **P3** drawer runner | 80 mm L-runner bolted into a rail's top slot, a 100 mm drawer-wall stub on its rib | yellow coupon 2026-09-20: geometry passes, sticks in places (warped, one bolt); friction verdict taken on the 300 ABS+ runners on the frame | 2026-10-01: both runners on four M5 each, the drawer fits and slides well | RUNNER_CLR 0.3 (also the column strips and the mini runner) |
| **P4** slot-clip tile | a tile's spring finger and barb in the rail's outer slot | v1 60 × 60 tiles, barb 0.6 / 0.9: loose, nothing located the tile; v2 four 66 × 14 strips A–D (stub 5.7 / 5.5, barb 1.2 at 45°, 7 mm finger); real band-1 tiles on the yellow run 2026-09-26 | 2026-09-20: C — barb 1.2, 45° hook, root stub 5.7; snaps in by thumb, no rock | CLIP_T 3.0, CLIP_BARB 1.2, CLIP_HOOK_DEG 45, CLIP_STUB_CLR 0.1 |
| **P5** hinge + magnet | a knuckle pair on a pin through 180°, a magnet pocket | v1 2026-09-22 failed (generic block, bores a pad apart); v2 cut from the production leaves (D11), pins 3.0 / 2.9 | 2026-09-27: the 2.9 pin passes both leaves (3.0 binds), free past 180; magnets glued and catching 2026-10-23 | PIN_HOLE_D 3.2 (pin 2.9), MAG_POCKET_D 10.4, MAG_POCKET_H 2.2 |
| **P6** pull insert | a face-down insert in a notched 80 mm facia stub (D9) | v1 slot 10: fits, too small for a thick finger; v2 slots 12 and 14 (14 is the bridge ceiling) | 2026-09-20: 12 | JPULL_OPEN_H 12, JPULL_HOOK 5, JPULL_DEPTH 17, JPULL_FLOOR_DEG 30, JPULL_WALL 2, JPULL_INSERT_CLR 0.15 |
| **P7** quarter joint | the drawer's floor tabs, a wall-crossing dovetail and the split-beam tab | one round, black PETG | 2026-09-17: all three assemble by hand, hold, flush | DOVETAIL_CLR 0.15 |
| **P8** TPU foot | spigot in the upright's centre bore; cover flare in the slot | sweeps 4.2 / 4.6 / 5.0 / 5.4 and 7.0 / 7.4 / 8.0 on the single TPU plate (rule 12) | 2026-10-16: the 4.6 feet push in and hold (glued), the 7.4 covers stay in by thumb | SPIGOT_D 4.6; cover flare 7.4 (`tpu_parts.py`) |
| **P9** bumper cup + stand pocket | the scope's rear bumper in a cup, the front stand in a pocket | v1 Ø32.6 cup failed (the bumper is a 25.9 × 24 D, measured 2026-09-19); v2 six straight D cups −0.1…+1.0, only +1.0 fitted; v3 sides 13 with a flatter arc, +0.1…+1.3; stand pocket v1 44.6 wide passes, 43.6 long fails; v2 23.7 long | cup +0.3 (2026-09-19, perfect fit); pocket 44.6 × 23.7 × 2.5 (2026-09-20); feet positioned by the jigs 2026-09-24 | BUMPER_W 25.9, BUMPER_D5 24.0, BUMPER_SIDE_L 13, BUMPER_CUP_CLR 0.3, BUMPER_CUP_D 6, STAND_W 44, STAND_L 23.1, STAND_CLR 0.3, STAND_POCKET_D 2.5 (0.6 / 1.0 in the beam), the four position constants |

## 12. Decisions D1–D15

| # | Decision | Choice | Date |
|---|---|---|---|
| D1 | The cut list did not pack into 8 × 1 m | Buy the CNCMANS 300 mm 4-pack; the 179.5s and 70s come from it | 2026-09-15 |
| D2 | The bottom drawer does not fit the bed | Four quarters joined by floor puzzle-dovetail tabs and sliding wall dovetails; P7 proves the joint | 2026-09-15 |
| D3 | Fronts cannot print face down | Every facia and the sled bar prints standing on its long edge on the diagonal | 2026-09-15 |
| D4 | 310 side tiles do not fit | Two 155 tiles per band, each clipped (the H-spline top went to D12) | by 2026-09-17 |
| D5 | The column drawer missed the diagonal by 2 | Shortened to 285 deep | by 2026-09-17 |
| D6 | The sled beams do not fit | Split at y 165 on a P7 tab; the cable channel a separate part | 2026-09-15 |
| D7 | The mini slot was short only because of the AWG's vent | 285 deep with a 15 mm vent neck over y 81–171 | by 2026-09-17; thermal check 2026-10-23 |
| D8 | The strip's keyholes run across its body | Vertical on the rear-left upright's rear face on two brackets, z 75–425 (raised round its mains cable) | 2026-09-17 / 09-27 |
| D9 | A pull slot in a standing front is an unsupportable bridge | Pulls are separate inserts glued into a top-edge notch; v2 flanged and hooked over the body wall | 2026-09-19 / 10-09 |
| D10 | Lighting from the Addtam's USB, no 12 V | Rev 2: strips inside the frame, button in a sill panel; rev 3: D1 mini + WLED on the rear base rail; **rev 5 as built: XIAO ESP32-S3 Plus + SiglentGlow, level shifter, 15-LED strips, two WS2812D-F5 sill pixels** | 2026-09-20 / 10-16 / 10-25 |
| D11 | The hinge axis at x 362 ran through the panel | Axis x 369, z 341; both leaves are brackets, reach 30 each way | 2026-09-22 |
| D12 | The top panel rested on nothing | 362 × 350 in four standing tiles on glued half-laps, caps screwed into the uprights' bores | 2026-10-14; on the frame 2026-10-23 |
| D13 | A second tray behind the scope | Withdrawn: it would choke the AWG's side vents | 2026-10-15 |
| D14 | The drawer housing tops carried nothing | No drawer lids; contents stay below the wall tops | 2026-10-16 |
| D15 | A stop would make removal "undo its M5, then pull" | No drawer stops; pulling clean off is the removal path (the mini slot keeps its bump) | 2026-10-16 |

## 13. Sheets and viewers

| File | Shows | Script |
|---|---|---|
| `bench-stack-3d.html` | interactive 3D model of the whole stack, design geometry and colours (the sub-frame still at the model position) | boxes in `src/viewer_boxes.json`, edited in place |
| `frame-assembly-3d.html` | the frame going together step by step, spacers and feet where they are used | `src/frame_assembly_viewer.py` |
| `bench-stack-layout-v15.pdf`; `bench-stack-impression.png` | dimensioned layout, design stage (page 1 current for the frame); isometric impression | `src/layout_gen.py`; `src/impression_gen.py` |
| `sled-mechanism-v2.pdf`, `drawer-quarters-v1.pdf/.svg`, `front-options-A-vs-B.pdf`, `front-switch-options.pdf` | design-stage sheets, superseded by the part sheets below | `src/sled_mechanism_gen.py`, `src/drawer_quarters_gen.py`, `src/switch_options_gen.py` |
| `parts/awg-mount-sheet.png` | the AWG on its cradles: elevation at the front pair and plan | `src/awg_mount_sheet.py` |
| `parts/column/column-plan.png` | section through the column bay: drawer, four strips, rails | `src/column_plan.py` |
| `parts/door/door-plan.png`; `hinge-how.png` | band 4 right from outside, magnet and leg sections, fitting order and polarity; one knuckle at 0 / 90 / 180° | `src/door_plan.py`; `src/hinge_how.py` |
| `parts/drawer/drawer-quarters-plan.png`; `drawer-facia-plan.png` | the four quarters reassembled with sections and the groove; the facia with insert and logo | `src/drawer_plan.py`; `src/facia_plan.py` |
| `parts/mini/mini-slot-plan.png` | runner / body section and plan with the vent neck | `src/mini_plan.py` |
| `parts/rear-box-plan.png`; `parts/sled-crossbar-fit.png` | the box halves and joints; the cross-bar lips against the box | `src/parts/rear_box.py`; `src/box_check.py` |
| `parts/sill/sill-panel-plan.png` | sill panel, window and blocks in the reveal | `src/parts/sill_panel.py` |
| `parts/sled-beam-plan.png`; `sled-ladder-plan.png`; `sled-absplus-plate.png` | the left beam in plan with the scope's feet, bars and channel overlaid; beams and bars at z 341 / 350; the ABS+ plate | `src/sled_beam_plan.py`; `src/sled_plan.py`; `src/sled_plate.py` |
| `parts/sled-front-rest-plan.png`; `parts/strip-bracket-v4.png` | the rest on the rail under the beam; the lower strip bracket round the mains cable | `src/parts/sled_front_rest.py`; `src/parts/strip_bracket.py` |
| `parts/tiles/skin-sheet.png` | where every side tile goes and where each finger lands, both sides | `src/skin_sheet.py` |
| `parts/top/top-panel-plan.png` | the top plate as laid out, the panel in plan, the lap section, a corner with its cap | `src/top_plan.py` |
| `parts/tpu/tpu-plate-plan.png`; `tpu-where.png`, `tpu-where-1…4` | the TPU plate, the cover in the slot, the pad, the foot; where each TPU part goes | `src/tpu_plan.py`; `src/tpu_where.py` |
| `parts/wiring/wiring-4-connections.png`; `wiring-2-runs.png` | every lighting connection, the pin map and set-up; where every wire runs, lengths and covers | `src/wiring_connections.py`; `src/wiring_sheet.py` |
| `parts/wiring/perfboard-layout.png`; `board-enclosure-plan.png`; `board-enclosure-sketch.png` | the perfboard hole by hole with the solder order; the enclosure's section, lid, plan and assembly; the sketch that preceded it | `src/perfboard_layout.py`; `src/enclosure_plan.py`; `src/enclosure_sketch.py` |
| `parts/scope-tray-plan.png` | D13 proposal, withdrawn | `src/tray_plan.py` |
| `coupons/p1/p1-howto.png`, `p1-section.png`; `p3/p3-section.png`; `p4/p4-sections.png`, `band3-right-sweep.png`; `p5/p5-plan.png`, `p5-v2-plan.png`, `hinge-section.png`; `p6/p6-section.png`; `p8/p8-plan.png`; `yellow-run/yellow-run-plan.png` | each coupon as printed and how to test it | `src/coupons/p*.py`, `src/parts/side_tile.py`, `src/yellow_run_plate.py` |
| Check scripts (no sheet) | every export through `printcheck.py`; fits proven by boolean intersection and shift tests | `src/drawer_check.py`, `column_check.py`, `box_check.py`, `sled_check.py`, `skin_check.py`, `cradle_check.py` |
