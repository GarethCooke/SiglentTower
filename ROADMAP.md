# Bench stack — build roadmap (v2.4, 2026-09-15)

Companion to `HANDOVER.md` (v18). Rule for the whole build: **nothing in HANDOVER §10 prints full-size until the coupon that gates it (§11, P1–P9) has passed.** Coupon numbers below are the handover's.

Stages run in order. Stage 2 (frame) overlaps Stage 1 (coupons) because the coupons only need rail offcuts.

v2: decisions D1–D6 answered (§0), cut plan redone for the 300 mm pack (§2), P7 redefined (§3), viewer v19 and `drawer-quarters-v1.pdf` issued. v2.1: D7 (mini slot 285 with vent channel), viewer v20. v2.2: Done columns and the progress checklist below; viewer versions collapsed into `bench-stack-3d.html`. v2.3: D5 confirmed, pack ordered, `fit.py` and the P7 coupon issued; sheet v1.1 (tabs start 25 from the wall, not 15 — 15 fouled the wall-crossing boss). v2.4: D4 confirmed — §0 closed. — tick ☐ → ☑ as things pass.

## Progress

- [x] §0 decisions D1–D10 all ☑
- [ ] Stage 0 — coupons modelled and sliced, spacer set printed
- [ ] Stage 1 — extrusion cut ☑ (2026-09-19); P1–P9 all ☑ in §3, values in `fit.py`
- [ ] Stage 2 — frame assembled, sled feet on the scope rails, instruments trial-fitted
- [ ] Stage 3 — cradles
- [ ] Stage 4 — drawers (incl. D7 thermal check)
- [ ] Stage 5 — sled
- [ ] Stage 6 — box + channel
- [ ] Stage 7 — skin
- [ ] Stage 8 — trim
- [ ] Stage 9 — close-out (HANDOVER v19, viewer/layout regenerated, STLs archived)

**Status 2026-09-19:** all extrusion cut. P9 v1 cup failed (bumper measured 25.9 × 24 at 5 mm up, D-shaped, not Ø32) — stand pocket v1 width passed, length failed (main leg is 23.1, not 43) — **print `coupons/p9/p9-v2-plate.stl` (cups + stand pad v2), yellow PETG, flat**. Awaiting test results: P6 (`pull-60` + `facia-80`), P1 v3 (`coupons/p1/p1-plate.stl`, yellow PETG — test per `coupons/p1/p1-howto.png` in bar Z). PSU cradles: v3 passed, remaining three to print. P3 modelled 2026-09-19 (`coupons/p3/runner-80.stl` black ASA + `stub-100.stl` yellow PETG, section `coupons/p3/p3-section.png`) — print after P1. Frame 2.1–2.5 may proceed (load the runner T-nuts first if they are the slide-in type — see 2.1); 2.6 (scope rails) waits for P1. Next models from Claude: P4 clip tile, AWG cradles, P8, P5, strip brackets, light bar (D10).

Tick a stage here only when its "Done when" line in the section below is met and every row in its table is ☑.

---

## 0. Decisions D1–D7 — status

Found by checking the handover against the 1 m bars and the 256 × 256 bed.

| Done | # | Finding | Decision | Status |
|---|---|---|---|---|
| ☑ | D1 | Cut list (7,579 mm) does not pack into 8 × 1 m at a 2 mm kerf — the two 179.5 inner uprights are what don't fit. | **Buy the CNCMANS 300 mm 4-pack (£13.99).** The 179.5s and 70s move to the 300s; the 8 × 1 m then take every 3xx and 510 piece with room. Two of the 300s are left whole as coupon rail. The pack's extra 4 brackets + 50 T-nuts also cover the 42-joint count. | **Decided.** Order it. |
| ☑ | D2 | Bottom drawer 315 × 300 cannot split into two bed-size pieces. | **Four quarters 157.5 × 150, full size kept.** Joint design in `drawer-quarters-v1.pdf`: floor puzzle-dovetail tabs (12 neck / 18 head / 8 long, pitch 30) alternating along both seams, none within 15 of the cross; vertical sliding dovetail (4/6 × 3) at the four wall crossings in a 12 × 8 boss; facia screwed across Q1–Q2; every joint assembles vertically (Q2 → Q1, Q3 → Q1, Q4 last). Housing top above = four loose clipped tiles. P7 is now this joint (§3). | **Decided.** Coupon P7 verifies before any quarter prints. |
| ☑ | D3 | Drawer fronts can't print face-down (315 × 86 fails flat and diagonal). | **All three fronts + sled bar standing on the long edge on the diagonal** (315 × ~15 → 233). No seam. P6 prints in that orientation. | **Decided.** |
| ☑ | D4 | Side tiles 310 long and top tiles 160.5 × 310 don't fit in one piece. | **Two 155 tiles per band, each clipped; top panel four tiles 160.5 × 155 on a printed H-spline** (two 10 × 3 strips under the seams at x 180.5 and y 175). Shown in `bench-stack-3d.html`. | **Decided** — confirmed from the viewer, pending the P4 clip-tile coupon before any tile prints. |
| ☑ | D5 | Column drawer 65 × 240 × 300 fails the diagonal by 2 mm. | **Shorten to 285** (diag 247.5). Body y 3–288 in `bench-stack-3d.html`; housing top over column + slot stays 300 deep as two loose tiles. | **Decided** (confirmed from the viewer). |
| ☑ | D6 | Sled beams 327 × 40 with arms fail the diagonal. | **Split each beam at y 165** (between the rear-bumper cup arms at 106–138 and the front cross bar at 190); the 210 T-foot bridges the seam. Cable channel is a separate 194 part keyed to the left beam. Shown in `bench-stack-3d.html`. | **Decided.** Joint coupon is part of P7. |
| ☑ | D7 | Mini slot was 180 deep only because it sits 5 mm off the AWG's right side, and the AWG's fan vent is on that side (measured: Ø80 centred 123 from the AWG front → frame y 126, vent y 86–166). | **Slot 285 deep (y 3–288), same as the column, with a 15 mm air channel beside the vent:** the slot's inner wall steps from x 242 to x 252 over y 81–171, so the body is a 26-wide front pocket (78 deep), a 16-wide neck (90) and a 26-wide rear pocket (117). The housing top over column + slot is notched the same (x 252–338 over y 81–171) so the channel is open upward into the 19 mm layer under the scope and downward past the inner rail. Shown in `bench-stack-3d.html`; slot travel now 250. | **Decided.** Gates: P3 (rides the inner AWG rail). Prints flat on the diagonal (285 + 26 → 220). |
| ☑ | D8 | The strip's keyholes run **horizontally** (slots across the body), so its keyholes alone cannot hold it vertical; and a horizontal mount needs ~380 (350 body + cable exit) against a 361 frame with nothing free either side at the rear. | **Vertical on the rear face of the rear-left upright, cable end down, on two printed L-brackets in that upright's rear slot** (back to HANDOVER §7's position): peg line x 30.2 → body x 1–79 (78.1 wide, 29.2 edge outboard, inside the frame), z 25–375, y 350–380 (30 thick inside the 60 behind), sockets facing the wall. Pegs at z 45 and 294.5 (keyholes 20 and 269.5 from the cable end, 249.5 c-c). The lower bracket carries a shelf under the strip's end (z 21–25, 10 mm cable notch) that takes the weight; the pegs only hold it against the frame. Cable drops to the bench at the rear-left post. Body edge 56 from the PSU fan centre (x ≈135.5), beside it not behind it. Diagonal rejected: at 45° the body crosses the PSU fan zone, neither keyhole lands on a rail or upright (the rear face has only the base and top cross rails), and it still needs the shelf. | **Decided 2026-09-17** (replaces the horizontal base-rail mount decided earlier the same day). |
| ☑ | D9 | A pull slot cut into a standing front (D3) leaves the slot's top edge as a bridge the width of the opening — 100 on the bottom drawer, 120 on the sled bar — with no way to support it. | **Pulls are separate inserts**: a notch in the front's top edge (no bridge) takes a face-down-printed insert in the accent colour (dark blue, per the HANDOVER colour scheme) carrying the slot, the 5 mm hook strip and the pocket (17 deep, floor 30°, walls 2); glued in, flush front and top. Same on the column front, the mini-slot front and the sled bar. | **Decided 2026-09-19** from modelling P6; the coupon prints the insert and a notched facia stub. |
| ☑ | D10 | Bench task light wanted (12 V RGB 5050 strip, analogue 4-wire, own controller). | **Light bar under the top panel's front edge**: printed pelmet 361 × 12 × 12 (z 498–510, y −12–0) with a 10.4 mm channel for the 10 mm tape, 1 mm diffuser lip, face tilted ~30° toward the bench; two halves joined by a P7 puzzle tab (361 is over the diagonal limit), end clips into the front uprights' front slots with T-nuts. 20 LEDs ≈ 5 W: 12 V 1 A adaptor on the Addtam, RGB controller inline, 4-wire flat cable down the front-left upright's inner slot behind the scope and AWG to the base, across to the strip. | **Decided 2026-09-19.** Stage 8 trim; nothing in the frame or cut sheet changes. |

**Sled-foot assembly constraint (terse):** the T-feet enter the scope rails' side slots from the rail end. Once a rail is bolted between the uprights, both ends are blocked. So: feet onto the rails first, then bolt those two rails in. Beam bottom 337 vs AWG top 336 is 1 mm — set the scope-rail height with the 63.5 spacer, not a tape.

Bed-fit audit for every printed part is in §8. **Print-orientation rules and the design-for-print review of every production part are in `PRINT-RULES.md`** — read it before modelling any part; every export runs `src/printcheck.py`.

---

## 1. Stage 0 — before the hardware arrives

Done when: D1–D7 ticked, coupon STLs sliced, spacer set printed.

| Done | Step | Output |
|---|---|---|
| ☑ | 0.1a Order the 300 mm 4-pack (D1). | ordered 2026-09-15 |
| ☑ | 0.1b D4, D5, D7 confirmed from `bench-stack-3d.html`; `drawer-quarters-v1.pdf` approved pending P7. | §0 all ☑ |
| ☑ | 0.2 Create `src/fit.py` — one module holding every tuned clearance (table in §3), imported by every part script. Coupons exist to set these numbers; production parts read them. | `src/fit.py` |
| ☐ | 0.3 Model the coupons in CadQuery, one script each under `src/coupons/`: **`p1_sled_foot.py` ☑** (v3 2026-09-19: T-nut flange from the measured slot; v2: web at x 22.2, closed beam groove; from `src/parts/sled_foot.py`, STLs in `coupons/p1/`), **`p3_runner.py` ☑** (2026-09-19: L-runner into the base rail's top slot + drawer-wall groove stub, from `src/parts/drawer_runner.py`, STLs in `coupons/p3/`), `p4_clip_tile.py`, `p5_hinge_magnet.py`, **`p6_pull.py` ☑** (`coupons/p6/`), **`p7_quarter_joint.py` ☑** (cropped from `src/parts/drawer_quarters.py`, STLs in `coupons/p7/`), `p8_tpu_foot.py`, **`p9_bumper_cup.py` ☑** (`coupons/p9/`). P2 is `psu_cradle.py` already. Each coupon is a literal section of the production part, in the production orientation, not a generic block. | STLs in `coupons/pN/` |
| ☑ | 0.4 Print the rail-height spacer set, any PETG: **48** (base top 20 → PSU rail 68), **139.5** (88 → 227.5), **63.5** (247.5 → 311), **159** (331 → 490), two of each, plus the 3.0 mm web gauge — `coupons/spacers/spacers-plate.stl`, flat as laid out, 2 walls, 10 % infill (`src/coupons/spacers.py`). | 9 small prints |
| ☐ | 0.5 Fix HANDOVER open item 3: `layout_gen.py` scope rails 318–338 → 311–331, regenerate page 1. | `bench-stack-layout-v16.pdf` |
| ☐ | 0.6 Slice coupon plates (§3): A = black ASA, B/C = yellow PETG, D = blue TPU. P1 and P9 sliced and printed (`bambu/01-coupons/`). | 4 `.3mf` |

---

## 2. Stage 1 — cut and coupon

Done when: every row in §3 is PASS and its number is in `fit.py`.

**Cut sheet — by jig setting** (`CUT-TABLE.md` is the same sheet for the workshop). Tape-label the 1000s A–H and the 300s W–Z, the labelled end never goes to the stop (feed the fresh end against it, so the label stays on the remainder), set the jig once per step and cut every bar listed before moving on. Every finished piece is the one between the stop and the blade; the remainder is stock for the next step, never a finished piece (it is short by the kerf). Kerf is allowed for.

**Accuracy:** ±0.5 mm on every length is fine and ±1 mm is survivable — the frame's critical dimensions are the rail heights, and those come from the printed spacers at assembly, not from the cuts. What does matter: (1) pieces of one length must match each other (within ~0.3) — cutting a whole set on one jig setting gives you that for free; (2) ends square to the bar, because a crooked end seats the hidden connector crooked and racks the frame; (3) err short, never long — a 510 at 509 costs 1 mm of reveal over the scope, at 511 it fouls the shelf plan; 179.5 can be 179. Nothing here needs 0.5 mm measured.

| Done | Step | Jig | Cut from | Cuts | Pieces made | Bar left after |
|---|---|---|---|---|---|---|
| ☑ | 1 | 200 | W | 1 | 1 × 200 — coupon rail (P2, P3, P8) | W ≈ 98 |
| ☑ | 2 | 179.5 | X, Y | 1 each | 2 × 179.5 — inner uprights | X, Y ≈ 118 |
| ☑ | 3 | 70 | W, X, Y | 1 each | 3 × 70 — ties | scrap |
| ☑ | — | — | Z | none | 1 × 300 whole — coupon rail (P1, P4) | — |
| ☑ | 4 | 510 | A, B, C, D | 1 each | 4 × 510 — uprights | A–D ≈ 488 |
| ☑ | 5 | 321 | A, B | 1 each | 2 × 321 — rear cross rails | scrap |
| ☑ | 6 | 310 | C, D (1 each), E, F (3 each), G (2) | 10 | 10 × 310 — side rails | G ≈ 376, rest scrap |
| ☑ | 7 | 307 | G (1), H (3) | 4 | 4 × 307 — inner sub-frame rails | scrap |

Check: 510 × 4, 321 × 2, 310 × 10, 307 × 4, 179.5 × 2, 70 × 3. Deburr every end as you go; the T-foot and clips will find any burr. Bundle each length with tape, length written on it.

**Coupon plates.**

| Done | Plate | Material | Parts |
|---|---|---|---|
| ☐ | A | black ASA (production material — these are sliding pairs, friction and shrink matter) | P1 `coupons/p1/foot-40.stl` (T-foot + web + rib, prints standing; v3 T-nut flange) + `beam-40.stl` (grooved stub, prints flat) — `p1-plate.stl` has both; yellow PETG is fine for the fit test, confirm in ASA before the 210 feet · **P3 `coupons/p3/runner-80.stl`** leg-top down, counterbore opens onto the bed (Bridge counterbore holes → Sacrificial layer, as the cradles) |
| ☑ | B | **yellow PETG** (house rule from 2026-09-17: every test and prototype part is yellow PETG unless the test depends on the production material) | **P3 `coupons/p3/stub-100.stl`** (outer wall + 10 × 20 boss + groove, floor down) · P4 60 × 60 hex tile with clips · P5 knuckle pair + 3 mm pin + magnet boss · **P9 `coupons/p9/p9-plate.stl`** (cup pad + stand-pocket pad, flat) · P7 (done — printed in black PETG before the rule) |
| ☐ | C | yellow PETG | **P6 `coupons/p6/pull-60.stl` face down + `facia-80.stl` standing** (D9) — geometry test, colour irrelevant |
| ☐ | D | blue TPU | P8 foot · one AWG pad · one sled-stop cap — proves all the TPU parts in one go |

Iterate width/clearance in 0.1 mm steps; re-print only the failing coupon. Budget three rounds for P1 and P4, one for the rest.

**Print settings — X1C, coupons and every fit-critical part (PETG; ASA the same except temperatures).**

| Setting | PETG | Why it matters here |
|---|---|---|
| Filament | dried first: 65 °C, 6–8 h (dryer or AMS with fresh desiccant) | wet PETG strings and blobs on the tab flanks — reads as "binds" |
| Calibration | Bambu Studio → Calibration → Flow Dynamics, then Flow Rate, for the exact spool; Bambu-branded spools: Lidar auto is enough | over-extrusion closes every 0.15 clearance |
| Process profile | 0.20 mm Standard @BBL X1C, first layer 0.20 | 3 mm floor = 15 layers exactly |
| Precise Z height | ON (Precise wall is built in on current Bambu Studio — no toggle) | dimensional accuracy of walls and tab widths |
| X-Y contour / hole compensation | 0 / 0 | clearance is tuned in `fit.py`, not in the slicer |
| Walls / top / bottom | 4 / 5 / 4 | HANDOVER spec; coupons the same as production |
| Infill | 40 % gyroid (spacers: 10 %, 2 walls) | |
| Nozzle / bed / fans | from the filament preset (Bambu PETG Basic or Generic PETG; Generic ASA/ABS), textured PEI, no glue | |
| Fans (check in the filament preset) | PETG: aux 0 %, part ≤ 50 % | aux fan on PETG chills the wall and hurts layer bond |
| Outer wall speed | 80 mm/s max (inner 150) | accuracy on the tab flanks |
| Brim / skirt | No-brim, skirt loops 1 | brim on a tab flank fakes the fit |
| Seam | Back / Aligned, scarf ON | keeps the seam blob off the joints |
| Supports | enabled (house rule), tree(auto), threshold 30°, **On build plate only** ticked | fit surfaces never get support residue; a part that shows internal support in the preview is a design fault, not a slicer setting |
| Ironing | off | |
| Elephant-foot compensation | 0.15 (default) | first layer of every tab is a fit surface |

ASA/ABS: filament preset, door closed, everything else as above. Saved in Bambu Studio as process profile `SiglentTower fit 0.20`.

---

## 3. Gates

| Done | Coupon | Pass when | Sets in `fit.py` | Gates (nothing here prints until PASS) | Start value |
|---|---|---|---|---|---|
| ☐ | **P1** sled foot + web | Foot slides in the inner side slot of a 2020 offcut by hand, no rock, can't lift out; web passes the 3.0 gauge; beam stub threads onto the rib from the end, no lift, side play < 0.3; beam underside 6.0 ± 0.3 above the rail's top face. | `SLOT_CLR` (neck and flange), `WEB_T`, `WEB_RIB_CLR` | Sled feet ×2, beams ×2, front bar, cross bars ×2, cable channel — the whole of §10.1 | slot measured 2026-09-19: mouth 5.9, lip 1.75, cavity 10.6, throat at 4.45, bottom 6.5 at 6.15 → neck 5.5, T-nut flange 10.2 (v3) |
| ☑ | **P2** PSU cradle | Saddle flat on the rail, foot seats in cup, M5×10 into T-nut pulls down, counterbore intact. **v2 (2026-09-17): saddle, bolts, counterbore PASS; cup FAIL** — printed Ø21.6 against a foot that is Ø16.8 at the pad, 19.5 at 4 mm up, 21.5 at the flange — 2 mm of slop. v3: conical cup matching the foot taper; coupon rounds A (0.5/0.6/0.7 net: all loose) and B (0.1/−0.1/−0.3 net: 0.1 best) set the cup at floor Ø17.0 / rim Ø19.7 with no shrink allowance, 1 mm 45° lead-in; self-centres. | `RAIL_CLR` ☑ 0.4, `CUP_CLR` ☑ 0.1 (cone, no shrink), `PSU_FOOT_PAD_D` 16.8, `PSU_FOOT_D4` 19.5 | PSU cradles ×3 more, AWG cradles ×4 (same saddle/clamp) | **PASSED 2026-09-17** — v3 perfect fit, sits on the rail perfectly. Releases PSU cradles ×3 and the AWG cradles. |
| ☐ | **P3** drawer runner | Runner bolted to the 200 coupon rail through the **top** slot (M5×10 + T-nut), rib over the side face; stub slides the runner's full length by hand, side play < 0.5, no stick-slip dry or with PTFE, no support in the preview. | `RUNNER_CLR` | Bottom-drawer runners, column guide strips ×4, mini-slot runner, all three drawer bodies | 0.3 — runner: L on the rail top (leg x 3–22.7, z 20–30, three M5 counterbores), 2.7 plate down the inner face, 7 mm rib z 6–20 with a 45° top; drawer: 10 × 20 boss on each outer wall, groove flank at the floor top (rests on the rib), back 7.3, 45° roof to 17.3. Modelled 2026-09-19 (`coupons/p3/p3-section.png`) |
| ☐ | **P4** slot-clip tile | Snaps in by thumb, pulls out only with a tool, 10 cycles no cracks. | `CLIP_T`, `CLIP_BARB` | All 16 side pieces, door tile, 4 top tiles, 6 housing-top tiles (D2/D5) | 3 mm PETG, barb 0.6 |
| ☐ | **P5** hinge + magnet | Pin pushes in, knuckle swings free through 180, magnet CA-glues flush in 10.4 × 2.2, pair pulls apart cleanly at 0.5 gap. | `PIN_HOLE_D`, `MAG_POCKET` | Door knuckles ×2, magnet bosses ×2, L-bracket, rear-tile tab | 3.2, 10.4 × 2.2 |
| ☐ | **P6** pull insert | Insert drops into the facia stub's notch flush front and top; fingertip goes in the slot, hooks up behind the 5 mm strip and pulls comfortably; no support in the preview. | `JPULL_*` | Three drawer fronts + inserts, sled front bar + insert | slot 10, hook 5, pocket 17, floor 30°, insert clr 0.15 |
| ☑ | **P7** quarter joint | Centre cross, wall crossing and beam pair all assemble by hand, hold without glue, faces flush within 0.2. | `DOVETAIL_CLR` ☑ 0.15 | Bottom drawer quarters ×4 (D2), split beams (D6), rear box halves | **PASSED 2026-09-17** at 0.15 — cross, wall crossing and beam pair all good |
| ☐ | **P8** TPU foot | Spigot holds in the 2020 centre bore (nominal ~4.2, spec says 5 — expect to trim to ~4.6), foot sits flat, no wobble. | `SPIGOT_D` | Feet ×4, AWG pads ×4, sled-stop caps ×2 | 5.0 |
| ☐ | **P9** bumper cup + stand pocket | **v1 cup FAIL (2026-09-19): Ø32.6 sized on the handover's Ø32, which the bumper never is.** Calipers (width = scope width): pad patch 20 × 9.5, at 5 mm up 25.9 × 24.0, at the chassis 25.9 × 26.4, ~14 tall — a D (flat one side, half-round the other, along the depth) with a bullnosed bottom 5 mm. v2 `coupons/p9/p9-cups-v2.stl`: six **straight-walled** D cups 25.9 × 24 + net −0.1 / +0.1 / +0.3 / +0.5 / +0.7 / +1.0, 5 straight + 1 mm 45° lead-in (6 deep, 3 mm floor), value stamped by each — the cup can only locate the bumper at its 5 mm section, so no lead-in inside that height. Pass: bumper seats fully, no rattle, lifts straight out; note which way the D's flat faces on the scope. **Stand pocket v1: width 44.6 PASS, length FAIL** — 43.6 was the stand's overall, but the folded flap tucks under the main leg and never reaches a 2.5 pocket; the main leg is 23.1 front-to-back. v2 `coupons/p9/stand-pad-v2.stl`: 44.6 × 23.7 × 2.5 (on `p9-v2-plate.stl` with the cups). Pass: main leg sits flat in it, no rock. For the beam: still need where the 23.1 sits within the stand's 43 (front or rear end) relative to the scope's front face. | `BUMPER_CUP_CLR` (v2 winner), `BUMPER_PAD_*` measured, `STAND_CLR`, `STAND_POCKET_D` | Sled beams (cups ×2, stand pockets ×2) | 0.3 / 0.3 / 2.5 |

Dependency chains: P1 + P7 + P9 + P6 → sled complete. P2 → all 12 cradles. P3 + P6 + P7 + P4 → drawers. P4 + P5 → skin. P8 → trim.

---

## 4. Stage 2 — frame (parallel with Stage 1)

Done when: PSU and AWG sit in the frame on temporary blocks at the right heights and the sled feet are on the scope rails.

- [ ] 2.1 Base: two base side rails + rear cross rail + four uprights, hidden L-connectors, square on the bench (diagonals equal within 1 mm), 321 clear width. **T-nuts first if they are the slide-in type:** three in each base side rail's TOP slot (drawer runners, P3) and the cradle nuts in the PSU/AWG rails' top slots — once a rail is between the uprights nothing enters its slots from the end.
- [ ] 2.2 Top: top side rails + rear cross rail. Check 510 overall.
- [ ] 2.3 PSU rails at 68 using the 48 spacers; cast brackets doubled here.
- [ ] 2.4 Inner sub-frame: PSU-level inner rails, inner uprights, AWG-level inner rails, three 70 ties.
- [ ] 2.5 AWG rails at 227.5 using the 139.5 spacers.
- [ ] 2.6 **Scope rails last**, with a sled T-foot already threaded into each inner side slot; set at 311 using the 63.5 spacers; cast brackets doubled here. Check the beam clearance with the 3.0 gauge against a 336 reference before tightening.
- [ ] 2.7 Place PSU and AWG on blocks at 91 and 251.5; check 3 mm reveals, screen-edge alignment, PSU fan clear, AWG side vents uncovered.

Joint count is 42; 40 hidden connectors + 8 cast brackets is enough only if two of the doubled joints are cast-only. Check on the bench.

---

## 5. Stages 3–7 — production printing

Order follows the handover: cradles → drawers → sled → box and channel → skin → trim. Each stage lists its gates; a stage may start modelling before its gates pass but not printing.

| Done | Stage | Gates | Parts | Done when |
|---|---|---|---|---|
| ☐ | **3 Cradles** | P2 ☑ | PSU cradle ×3 more (`parts/psu-cradle-v3.stl`, print now), AWG cradle ×4 (left reach 6.5, right 17.5, pads 3.5, corner lips), AWG TPU pads ×4 (P8 also) | PSU and AWG sit level, 3 mm behind the front plane, screens' left edges aligned, no rock. |
| ☐ | **4 Drawers** | P3, P6, P7, P4 | Bottom runners ×2 (300, three M5 into the base rails' top slots, stop block behind the drawer) → **test on the frame** → bottom drawer quarters ×4 (D2, assemble per the sheet, no glue) → runner test → CA the wall dovetails → column drawer (285, D5) → mini slot (285 with the vent neck, D7) → three fronts (on edge, D3) → housing-top tiles ×6 → column guide strips ×4, rear stops | All three run full travel, lift-to-remove works, fronts flush with the uprights, logo inlay reads. **Thermal check (D7):** AWG on for 1 h in the assembled stack, slot in, side tiles on; exhaust temperature and fan note compared with the AWG alone on the open bench. Fallback if it runs noticeably hotter: reprint the slot at 85 deep (ends 5 mm before the vent); nothing else changes. |
| ☐ | **5 Sled** | P1, P7, P9, P6 | Feet ×2 (layers along the slide) → beams (split, D6) with arms, cups, pads → front bar → cross bars with guide lips → cable channel → stops (T-nut behind foot; T-nut + TPU cap at front) | Scope rides level, 100 travel, sag ≤ 1 mm out, stops hold, beam clears the AWG frame along the whole travel. |
| ☐ | **6 Box + channel** | P7 | Box halves (dovetailed), 20 lip, guide-lip engagement on the cross bars; cable channel wedge tabs | Full access sequence works: pull sled 100 → fold door (skin not yet on: check the box exits right into the clear zone) → slide box out → reverse. Meters fit. |
| ☐ | **7 Skin** | P4, P5 | 14 side tiles (155 long) → door + knuckles + magnet bosses + L-bracket → fixed rear tile with tab → top tiles ×4 + H-spline | Door swings 180 and catches; every tile snaps in; sled band 331–346 open; nothing fouls the sled or the box exit. |
| ☐ | **8 Trim** | P8 | TPU feet ×4, blue caps ×4, probe hanger, strip brackets ×2 in the rear-left upright's rear slot per D8 (open item 1 closed 2026-09-17 — Addtam strip measured: keyholes 249.5 c-c, large hole Ø6.5, slot 3.5, nearest keyhole centre 20 from the cable end, keyhole pocket 6.5 deep, keyhole line 29.2 from one edge of the 78.1 body; bracket = 20 × 40 × 4 plate on the upright's rear face (one M5 into the rear slot) with a 4 mm arm inboard to the peg at x 30.2, peg shaft Ø3.2 × 3, head Ø6.0 × 2.5 with a 45° cone under it; the lower bracket adds a 79 × 30 × 4 shelf at z 21–25 with a 10 mm cable notch; both print plate-face down with peg and shelf rising), stop caps, rear-right cable clips (**confirm AWG/PSU LAN/USB positions first — open item 4**), light bar halves ×2 + end clips ×2 per D10 (12 V RGB 5050 tape, controller and adaptor to buy) | Strip mounted, three IEC leads routed, LAN/USB down the rear-right, scope loop absorbs 100 travel, probes hang clear of the door. |

---

## 6. Files issued with this roadmap

`bench-stack-3d.html` — the one viewer, edited in place; history is in git (the v18 → v19 → v20 patch scripts that applied D2–D7 live in the git history, not the tree). D2/D4/D5/D6/D7 are all in it. `drawer-quarters-v1.pdf/.svg` — D2 joint sheet (`src/drawer_quarters_gen.py`).

## 7. Stage 9 — close-out

- [ ] HANDOVER → v19: fold in D1–D7, final `fit.py` values, tile count, drawer depths.
- [ ] Regenerate the viewer and layout from the final dimensions (`layout_gen.py`, `viewer_boxes.json`).
- [ ] Every final STL lives in `parts/` with its script in `src/parts/`, named `<part>-v<N>.stl` matching the script version (coupons stay in `coupons/`).
- [ ] MakerWorld pack: `publish/` with the final STLs, one Bambu project (.3mf) per plate from `bambu/`, photos of the printed parts, the cut list and hardware BOM, and the assembly sequence (HANDOVER §5 access sequence + Stage 2 frame order).
- [ ] **Write-up** (after everything above): a finished build story, not a spec — the bench constraints and why an extrusion frame, the level stack, the three focal points (the scope sled and rear box access sequence; the four-quarter drawer joint; the vent-channel slot), the coupon-first method and what each coupon changed, the print rules that came out of it, and the finished result with photos. Diagrams drawn to the point (front and side elevations with the levels, the sled/box access sequence as a three-frame strip, the quarter-drawer joint exploded), the interactive `bench-stack-3d.html` embedded or linked, and the MakerWorld and repo links. Long-form, one page for garethcooke.com; the MakerWorld description is a cut-down of it. Owner: Claude, draft for Gareth's edit.

**Bambu project files.** Save Bambu Studio projects (File → Save project, `.3mf`) under `bambu/<stage>/<plate>.3mf` — e.g. `bambu/coupons/p7-plate.3mf`, later `bambu/03-cradles/psu-cradles.3mf`. Commit the project file, not the sliced `.gcode.3mf`. The STL + CadQuery script stay the source of truth; the .3mf is the build artefact that carries plate layout and the `SiglentTower fit 0.20` profile, and it is what MakerWorld takes as a print profile.

---

## 8. Bed-fit audit (256 × 256; diagonal fits if (L + W)/√2 ≤ 250)

| Part | Footprint | Fits | Route |
|---|---|---|---|
| Bottom drawer body | 315 × 300 | no | D2: four quarters 157.5 × 150 |
| Bottom facia | 315 × 86 | no flat / 284 diag | D3: on edge, diag 233 |
| Bottom housing top | 315 × 300 | no | four loose tiles 157.5 × 150 |
| Bottom runners | 300 × 10 | diag 219 | diagonal |
| PSU / AWG cradles | < 100 | flat | — |
| Column drawer | 65 × 300 | 258 diag | D5: 285 → 247.5 diag |
| Column facia | 245 × 65 | flat | on edge to match D3 |
| Column guide strips | 300 × 10 | diag 219 | diagonal |
| Mini slot | 285 × 26 (83 tall) | diag 220 | D7: diagonal, flat |
| Housing top, column + slot | 96 × 300 | 280 diag | two tiles 96 × 150 |
| Sled T-feet | 210 × 10.6 | flat | — |
| Sled beams + arms | 327 × 42 | 261 diag | D6: split (P7) |
| Cable channel (separate) | 194 × 26 | flat | — |
| Front bar | 315 × 18 | diag 235 | diagonal, on edge (D3) |
| Rear cross bars | 321 × 23 | diag 243 | diagonal |
| Rear box halves | 145.5 × 135 | flat | as designed |
| Side tiles, all bands | 310 × 48…143 | 253…320 diag | D4: 155 long |
| Door | 230 × 143 | flat | face-down |
| Fixed rear tile | 80 × 143 | flat | — |
| Top tiles | 160.5 × 310 | 333 diag | D4: 160.5 × 155 ×4 |
| Feet, caps, hanger, brackets, knuckles, bosses | small | flat | — |

Rough filament, ±30 %: black PETG ~1.2 kg (tiles, top, drawer bodies, housing tiles), dark grey PETG ~0.4 kg (fronts, box, bar), black ASA ~0.6 kg (cradles, sled, feet, brackets), TPU and blue PETG < 150 g between them.
