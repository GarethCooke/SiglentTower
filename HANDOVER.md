# Bench stack — design handover (v18, 2026-09-15)

Owner: Gareth Cooke (IguanaWare). Purpose: aluminium-extrusion stacking rig with 3D-printed parts for three Siglent bench instruments, on a 350 mm-wide bench with shelves directly above, 60 mm free behind, 350 mm free to the right along the front 250 mm of depth (rear 100 mm blocked on the right).

Files in this bundle: `bench-stack-layout-v15.pdf` (layout sheet, page 1 current except scope rails — see §4), `sled-mechanism-v2.pdf` (current sled design, supersedes page 2 of the layout), `bench-stack-3d-v18.html` (interactive 3D model, self-contained, current geometry and colours), `psu-cradle-v2.stl/.py` (first printed part, CadQuery source), `src/` (generator scripts for every sheet and the viewer), `Iguana.svg` (logo).

Status: design frozen; hardware on order; first test print ready. Next: STLs.

---

## 1. Instruments (measured)

| | Front frame W×H | Body W×H×D | Feet | Notes |
|---|---|---|---|---|
| Siglent SDS1104X-E scope | 315 × 152 | body 108 deep; 135 deep incl. rear bumpers | rear bumpers Ø32 × 14 (centre 39 from side, at rear edge); front fold-flat stands 44 × 43 × 11.5 (outer corner 24 from side, 10 from front) | 166 tall flat on feet. Side vent right side; rear vents; IEC bottom-left (front view). 2.6–3 kg |
| Siglent SDG2082X AWG | 214 × 88 (frame 3.5 proud each side, 3 top/bottom) | 207 × 82 × 260 bumpers off | none (stripped) | Handle and 4 corner bumpers removed (Torx). Vent: one Ø80 perforated patch per side, centred. IEC bottom-left (front view). 3.4 kg |
| Siglent SPD3303X-E PSU | 225 × 143 (frame 2.75 proud each side, 3 top/bottom, 3.5 deep) | 219.5 × 137 × 284.5 (301.5 to front knobs) | Ø21 × 11.5, centres 33 from side, 34 from rear, 48 from front | Fan exhaust centre rear (keep ≥50 clear). Side vents 35–155 from front, both sides. IEC bottom-left (front view). 7.5 kg |

Also stored: Brymen BM867s in holster 208.5 × 103.5 × 66; Brymen BM22s 115 × 53 × 12; Siglent SLA1016 logic analyser (intended purchase, ~125 × 60 × 28 + leads); four PP510 probes (barrel Ø6.25, grip Ø10, 183 tip-to-cable); AWG handle + bumpers.

## 2. Frame (2020 extrusion, black, 6.2 mm slot)

Overall 361 W × 350 D × 510 H (+6 TPU feet, +6 caps = 522). Clear width between uprights 321. Coordinates below: x from outside of left upright, y from front face of front uprights, z from bench (feet excluded).

- 4 uprights 510 at the corners.
- 5 pairs of side rails (front–rear, 310): z 0–20 base, 68–88 PSU, 227.5–247.5 AWG, **311–331 scope**, 490–510 top.
- 2 rear cross rails 321: base and top.
- Inner sub-frame (option B): inner rails 307 at x 251–271, PSU and AWG levels, y 23–330; inner uprights 179.5 at y 3–23 and 330–350 between them; ties 70 to the outer right rails: PSU level front and rear, AWG level rear only.
- Cut list: 4 × 510, 10 × 310, 4 × 307, 2 × 321, 2 × 179.5, 3 × 70 → 7,579 mm; bought 8 × 1 m (Amazon CNCMANS, incl. 8 cast brackets + 100 T-nuts). Joints: 40 hidden L-connectors (AliExpress) with the 8 cast brackets doubled on the scope-rail and PSU-rail joints. Screws M5×8 (brackets) and M5×10 (printed parts).
- Everything inside the frame (instruments, sub-frame, drawers) sits 3 mm behind the front plane; drawer facias fill 0–3, flush with the uprights.

## 3. Levels (z)

| Item | z | Notes |
|---|---|---|
| Bottom drawer | body 3–63, facia 3–86 | 315 × 60 × 300, PETG; housing top 64–67 |
| PSU | frame 100–243, feet in cups at 91 | cups 4 mm above rail top |
| AWG | frame 248–336, body 251.5–333.5 on 3.5 pads | pads behind the front frame |
| Column drawer | 91–336 (body to 331) | x 273–338, 65 × 240 × 300 |
| Mini slot | 248–336 | x 242–268, 26 × 83 × 180, rides inner AWG rail |
| Housing top over column + slot | 333–336 | x 242–338 |
| Scope | feet 341–355, body 355–507 | on the sled |
| Top panel | 510–513 | on the top rails, solid |
| Reveals | 5 mm everywhere; 3 to the uprights (set by the scope) | |

Layout: PSU and AWG hard left (3 mm); scope centred; column drawer right. Screens' left edges align.

## 4. Scope sled (current = sled-mechanism-v2.pdf, viewer v18)

- Two beams 40 × 9 at x 20.5–60 and 301–340.5, z 337–346, y 3–330, joined by a front bar (315 × 18 × 12, z 337–355, J-pull opening 120 × 6) and two rear cross bars (x 20–341, z 337–346, at y 190–210 and 310–330).
- Each beam has a 2.5 mm web down the 3 mm gap to a printed T-foot (10.6 × 3.8, 210 long, y 120–330) running in the scope rail's **inner side slot**. Travel 100 (not 140 — beam height limited by the AWG frame 1 mm below). Sag ≈ 1 mm at the front when out. Stops: T-nut behind the foot (push-in); T-nut + TPU cap at the slot front (pull-out). PTFE dry lube; UHMW tape on the foot is the upgrade if it drags.
- Scope cradles on the beams: rear bumper cups Ø32.6 × 5 on arms reaching to x 62/299; front pads with 5 mm lips. Front pads 5.5 tall (front stands 11.5 vs bumpers 14) so the scope sits level.
- Rear box rides the sled on the two cross bars: 291 × 135 × 110 (x 50–341, y 195–330), floor at 346, 20 mm front lip, full rear/side walls, two halves dovetailed (bed limit). Guide lips 10 tall on the front and rear bars (front lip chamfered at the exit end; rear lip square), inner channel wall doubles as the left end stop. Box exits to the RIGHT over the right beam once the sled is out (box then at y 95–230, inside the clear zone).
- Cable channel on the sled, left of the box: x 20–46, y 140–334, floor at 346; outer wall 20–23 to z 366 (front top corner chamfered 10); inner wall 47–50 to 366 with a 45° ramp down to 356 at the rear end only (front top corner chamfered 10); three staggered wedge tabs 5 wide, 18 reach, 45° solid support: outer wall at y 190 and 280, inner wall at y 235. Scope mains + LAN/USB run rearward in it; loop behind the frame absorbs the 100 mm travel.

## 5. Panels and door

- Side tiles 3 mm PETG, 4 mm solid border, hex 8.4 mm / 2.5 mm webs (~55 % open), clip into the rail slots, one tile per band between rails: 20–68, 88–227.5, 247.5–311, 347–490. Band 331–346 left open (sled). Left side 4 tiles × 310 long; right side 3 lower tiles + top band split at y 250: front 230 × 143 = **fold-down door**, rear 80 fixed.
- Door: bottom hinge, two printed knuckles at the ends (3 mm pin), axis z 341 outboard of the upright (knuckles top out at 345, under the box floor), opens to 180 (hangs ~20 proud of the tile below). Catch: 2 pairs Ø10 × 2 magnets at the top corners — door side in 12 × 12 × 3 bosses on the inside face; frame side: front = rounded L-bracket (6 thick, 22 tall, y 20–49, r8 exposed corners) bolted to the front upright's inner slot and hung in the top rail's slot; rear = tab grown from the fixed tile's front border (y 228–250) with a web into the tile. Faces 0.5 apart, pull-apart in the opening direction. Pockets 10.4 × 2.2, CA glue, mark polarity. 40 mm finger notch in the door's top border.
- Top panel 321 × 310 × 3 solid, two tiles 160.5 wide, lying on the top rails, caps 6 mm at the corners.
- Access sequence: pull sled 100 → fold door → slide box out right → reverse.

## 6. Storage and pulls

- Bottom drawer: probes ×4, BNC ×2, banana ×4, SLA1016, AWG handle + bumpers (or those to the box). Printed runners on the base rails' inner faces; rear stop; lift-to-remove.
- Column: 4.7 L bits and bobs; guide strips on inner and outer rails at PSU and AWG levels (four points, no tipping). Mini slot: USB/SD/probe tips.
- Rear box: BM867s on edge + BM22s + spare leads.
- Pulls: J-pull pockets behind a 10 mm-tall opening (bottom 100 wide, column 40, slot 16, sled bar 120 × 6), 12 deep, 15 tall inside, floor sloped ~30°, lip r1.5, closed 2 mm walls.
- Logo: iguana debossed two-colour in the bottom facia, top-right, rotated 90° clockwise (head right), 60 × 30.
- Probe hanger: bar 110 × 12 with four keyhole slots (7 neck → 11) at 25 pitch on the LEFT face of the front-left upright at z 443–455; probes hang tip-down outside the frame.

## 7. Cable management and power

- Strip: Addtam 4-way individually switched, surge, 350 × 76 × ~30, two keyholes — mounted vertically on the rear-left, sockets facing the wall, on two printed brackets in the rear uprights' rear slots with keyhole pegs (spacing TBC when it arrives). Three 0.5 m IEC leads with slim/right-angle plugs. Mains down the rear-left post, LAN/USB down the rear-right, PSU fan centre clear. No front switch; smart plug on the strip if a master-off is wanted later.

## 8. Materials and colours (decided)

- Black ASA or ABS: cradles, sled (feet, beams, bars, arms, channel), catches, hinge knuckles, magnet bosses, strip brackets, hanger, caps (caps are BLUE).
- Black PETG: side tiles, door, top tiles, drawer bodies, housing tops.
- Dark grey PETG: three drawer fronts, sled bar, rear box.
- Blue TPU: feet (24 × 24 × 6, 5 mm spigot into the extrusion bore), AWG pads, sled-stop caps.
- Blue PETG: logo inlay, pull recesses.
- Instruments are cream in the viewer.
- Print notes: cradles cup-up, 0.2 mm, 4 walls, 40 % gyroid, no supports; fronts face-down on textured plate; sled feet with layers along the slide, 0.4 under channel width, rounded flanks.

## 9. Open items

1. Strip keyhole spacing (measure on arrival).
2. Test-fit psu-cradle-v2 on a cut rail: foot seats in cup, saddle doesn't rock. Then print ×4.
3. Layout PDF page 1 still shows scope rails at 318–338; correct is 311–331 (v18). Everything else on the sheet is current.
4. Confirm AWG and PSU LAN/USB port positions before the rear-right cable clips are placed.

## 10. Next work (in order)

1. Sled STLs: feet (2), beams with arms/cups/pads/channel (2, print diagonal or split), front bar, two cross bars with guide lips, box halves.
2. AWG cradles ×4 (left reach 6.5, right reach 17.5, pads 3.5, corner lips) with TPU pad inserts.
3. PSU cradle ×4 (done, v2).
4. Drawer runners → test on the frame → drawer bodies, fronts, housing tops.
5. Side tiles, door, hinges, catches, top tiles.
6. Feet, caps, hanger, strip brackets, stop caps.

All parts must fit a 256 × 256 × 256 bed; anything longer splits with a dovetail or prints on the diagonal.

## 11. Prototype before committing filament

Each of these is a small test print against a cut rail or the real part; nothing in §10 gets printed full-size until its test passes.

1. **Sled foot + web sample** — 50 mm of foot in the scope rail's inner side slot with the 2.5 web and a stub of beam. Tests: sliding fit (0.4 under channel), no rock, web clears the AWG frame in the 3 mm gap, foot can't lift out. Iterate width in 0.1 steps. This gates the whole sled.
2. **PSU cradle v2** — one part on a rail: foot seats in cup, saddle sits flat, T-nut screws pull it down without cracking the counterbore. Gates the other 11 cradles (AWG cradles share the saddle/clamp).
3. **Drawer runner sample** — 80 mm of runner on a base rail and a 100 mm drawer-side stub with the groove: slide, side play, PETG-on-ASA friction with and without PTFE. Gates all three drawers.
4. **Slot-clip coupon** — a 60 × 60 hex tile with the rail-slot clips: snap force, retention, whether 3 mm PETG clips survive ten cycles. Gates all tiles and the door.
5. **Hinge + magnet coupon** — one knuckle pair with a 3 mm pin and one magnet pocket (10.4 × 2.2): pin fit, free swing, magnet glue-fit and pull force. Gates the door.
6. **J-pull sample** — a 60 mm section of drawer front with the pocket: finger comfort, overhang prints clean without support. Gates the fronts and sled bar.
7. **Dovetail joint coupon** — the split used for the box halves, bottom drawer halves and 327 beams if split rather than diagonal: fit and alignment. Gates every split part.
8. **TPU foot** — one, checked for spigot fit in the extrusion's centre bore and for how it sits on the bench.
9. **Bumper cup coupon** — a 40 × 40 pad with the Ø32.6 × 5 cup and a front pad with 5 mm lip: scope bumper drops in and locates, no rattle.

Order of printing after the prototypes: cradles → drawer runners and drawers → sled → box and channel → tiles, door and top → feet, caps, hanger, brackets.
