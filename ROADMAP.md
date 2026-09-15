# Bench stack — build roadmap (v2, 2026-09-15)

Companion to `HANDOVER.md` (v18). Rule for the whole build: **nothing in HANDOVER §10 prints full-size until the coupon that gates it (§11, P1–P9) has passed.** Coupon numbers below are the handover's.

Stages run in order. Stage 2 (frame) overlaps Stage 1 (coupons) because the coupons only need rail offcuts.

v2: decisions D1–D6 answered (§0), cut plan redone for the 300 mm pack (§2), P7 redefined (§3), viewer v19 and `drawer-quarters-v1.pdf` issued. v2.1: D7 (mini slot 285 with vent channel), viewer v20.

---

## 0. Decisions D1–D6 — status

Found by checking the handover against the 1 m bars and the 256 × 256 bed.

| # | Finding | Decision | Status |
|---|---|---|---|
| D1 | Cut list (7,579 mm) does not pack into 8 × 1 m at a 2 mm kerf — the two 179.5 inner uprights are what don't fit. | **Buy the CNCMANS 300 mm 4-pack (£13.99).** The 179.5s and 70s move to the 300s; the 8 × 1 m then take every 3xx and 510 piece with room. Two of the 300s are left whole as coupon rail. The pack's extra 4 brackets + 50 T-nuts also cover the 42-joint count. | **Decided.** Order it. |
| D2 | Bottom drawer 315 × 300 cannot split into two bed-size pieces. | **Four quarters 157.5 × 150, full size kept.** Joint design in `drawer-quarters-v1.pdf`: floor puzzle-dovetail tabs (12 neck / 18 head / 8 long, pitch 30) alternating along both seams, none within 15 of the cross; vertical sliding dovetail (4/6 × 3) at the four wall crossings in a 12 × 8 boss; facia screwed across Q1–Q2; every joint assembles vertically (Q2 → Q1, Q3 → Q1, Q4 last). Housing top above = four loose clipped tiles. P7 is now this joint (§3). | **Decided.** Coupon P7 verifies before any quarter prints. |
| D3 | Drawer fronts can't print face-down (315 × 86 fails flat and diagonal). | **All three fronts + sled bar standing on the long edge on the diagonal** (315 × ~15 → 233). No seam. P6 prints in that orientation. | **Decided.** |
| D4 | Side tiles 310 long and top tiles 160.5 × 310 don't fit in one piece. | **Two 155 tiles per band, each clipped; top panel four tiles 160.5 × 155 on a printed H-spline** (two 10 × 3 strips under the seams at x 180.5 and y 175). Shown in viewer v19. | **Provisional** — confirm after viewing v19. |
| D5 | Column drawer 65 × 240 × 300 fails the diagonal by 2 mm. | **Shorten to 285** (diag 247.5). Body y 3–288 in v19; housing top over column + slot stays 300 deep as two loose tiles. | **Provisional** — confirm after viewing v19. |
| D6 | Sled beams 327 × 40 with arms fail the diagonal. | **Split each beam at y 165** (between the rear-bumper cup arms at 106–138 and the front cross bar at 190); the 210 T-foot bridges the seam. Cable channel is a separate 194 part keyed to the left beam. Shown in v19. | **Decided.** Joint coupon is part of P7. |
| D7 | Mini slot was 180 deep only because it sits 5 mm off the AWG's right side, and the AWG's fan vent is on that side (measured: Ø80 centred 123 from the AWG front → frame y 126, vent y 86–166). | **Slot 285 deep (y 3–288), same as the column, with a 15 mm air channel beside the vent:** the slot's inner wall steps from x 242 to x 252 over y 81–171, so the body is a 26-wide front pocket (78 deep), a 16-wide neck (90) and a 26-wide rear pocket (117). The housing top over column + slot is notched the same (x 252–338 over y 81–171) so the channel is open upward into the 19 mm layer under the scope and downward past the inner rail. Shown in v20; slot travel now 250. | **Decided.** Gates: P3 (rides the inner AWG rail). Prints flat on the diagonal (285 + 26 → 220). |

**Sled-foot assembly constraint (terse):** the T-feet enter the scope rails' side slots from the rail end. Once a rail is bolted between the uprights, both ends are blocked. So: feet onto the rails first, then bolt those two rails in. Beam bottom 337 vs AWG top 336 is 1 mm — set the scope-rail height with the 63.5 spacer, not a tape.

Bed-fit audit for every printed part is in §7.

---

## 1. Stage 0 — before the hardware arrives

Done when: D1–D6 answered, coupon STLs sliced, spacer set printed.

| Step | Output |
|---|---|
| 0.1 Order the 300 mm 4-pack (D1). Confirm D4/D5 from viewer v19. | — |
| 0.2 Create `src/fit.py` — one module holding every tuned clearance (table in §3), imported by every part script. Coupons exist to set these numbers; production parts read them. | `src/fit.py` |
| 0.3 Model the coupons in CadQuery, one script each: `src/coupons/p1_sled_foot.py`, `p3_runner.py`, `p4_clip_tile.py`, `p5_hinge_magnet.py`, `p6_jpull.py`, `p7_dovetail.py`, `p8_tpu_foot.py`, `p9_bumper_cup.py`. P2 is `psu_cradle.py` already. Each coupon is a literal section of the production part, in the production orientation, not a generic block. | 8 STLs |
| 0.4 Print the rail-height spacer set in PETG (hollow, any colour): **48** (base top 20 → PSU rail 68), **139.5** (88 → 227.5), **63.5** (247.5 → 311), **159** (331 → 490). Two of each. Plus a 3.0 mm gap gauge for the sled web. | 9 small prints |
| 0.5 Fix HANDOVER open item 3: `layout_gen.py` scope rails 318–338 → 311–331, regenerate page 1. | `bench-stack-layout-v16.pdf` |
| 0.6 Slice coupon plates (§3): A = black ASA, B = black PETG, C = dark grey PETG, D = blue TPU. | 4 `.3mf` |

---

## 2. Stage 1 — cut and coupon

Done when: every row in §3 is PASS and its number is in `fit.py`.

**Cut plan (2 mm kerf, 8 × 1000 + 4 × 300).** Cut the 300s first so the coupon rails exist before the frame does:

| Bar | Pieces | Used |
|---|---|---|
| 300 A | 179.5, 70 | 249.5 |
| 300 B | 179.5, 70 | 249.5 |
| 300 C | 70, then 200 **coupon rail** | 270 |
| 300 D | whole — **coupon rail** | 300 |
| 1000 × 1 | 510, 321 | 831 |
| 1000 × 2 | 510, 321 | 831 |
| 1000 × 3 | 510, 310 | 820 |
| 1000 × 4 | 510, 310 | 820 |
| 1000 × 5 | 310, 310, 310 | 930 |
| 1000 × 6 | 310, 310, 310 | 930 |
| 1000 × 7 | 310, 310, 307 | 927 |
| 1000 × 8 | 307, 307, 307 | 921 |

Check: 510 × 4, 321 × 2, 310 × 10, 307 × 4, 179.5 × 2, 70 × 3. Coupon rail use: 300 D = P1 (scope-rail inner slot) and P4 clips; 200 = P2 cradle saddle, P3 runner, P8 spigot in the centre bore. Deburr every end; the T-foot and clips will find any burr.

**Coupon plates.**

| Plate | Material | Parts |
|---|---|---|
| A | black ASA | P1 foot 50 mm + 2.5 web + beam stub · P2 psu-cradle-v2 · P3 runner 80 mm · P5 knuckle pair + 3 mm pin + magnet boss · P9 40 × 40 cup pad + front pad with 5 mm lip |
| B | black PETG | P3 drawer-side stub 100 mm with groove · P4 60 × 60 hex tile with clips · P7 per `drawer-quarters-v1.pdf`: centre cross (four 60 × 60 floor corners with the real tab pattern), one wall crossing (rib + boss, 60 tall), one 9 × 40 beam-section pair |
| C | dark grey PETG | P6 60 mm of front with J-pull pocket, **standing on edge on the diagonal** (D3) |
| D | blue TPU | P8 foot · one AWG pad · one sled-stop cap — proves all the TPU parts in one go |

Iterate width/clearance in 0.1 mm steps; re-print only the failing coupon. Budget three rounds for P1 and P4, one for the rest.

---

## 3. Gates

| Coupon | Pass when | Sets in `fit.py` | Gates (nothing here prints until PASS) | Start value |
|---|---|---|---|---|
| **P1** sled foot + web | Slides by hand with no rock; can't lift out; web passes the 3.0 gauge; stub sits 1 mm above a 336 reference. | `SLOT_FOOT_W`, `SLOT_FOOT_T`, `WEB_T` | Sled feet ×2, beams ×2, front bar, cross bars ×2, cable channel — the whole of §10.1 | foot 5.8 (6.2 − 0.4), web 2.5 |
| **P2** PSU cradle v2 | Saddle flat on the rail, foot seats in cup, M5×10 into T-nut pulls down, counterbore intact. | `RAIL_CLR` (saddle 20 + x), `CUP_CLR` | PSU cradles ×3 more, AWG cradles ×4 (same saddle/clamp) | 0.4, 0.6 |
| **P3** drawer runner | Stub slides full length, side play < 0.5, no stick-slip dry or with PTFE. | `RUNNER_CLR` | Bottom-drawer runners, column guide strips ×4, mini-slot runner, all three drawer bodies | 0.3 |
| **P4** slot-clip tile | Snaps in by thumb, pulls out only with a tool, 10 cycles no cracks. | `CLIP_T`, `CLIP_BARB` | All 16 side pieces, door tile, 4 top tiles, 6 housing-top tiles (D2/D5) | 3 mm PETG, barb 0.6 |
| **P5** hinge + magnet | Pin pushes in, knuckle swings free through 180, magnet CA-glues flush in 10.4 × 2.2, pair pulls apart cleanly at 0.5 gap. | `PIN_HOLE_D`, `MAG_POCKET` | Door knuckles ×2, magnet bosses ×2, L-bracket, rear-tile tab | 3.2, 10.4 × 2.2 |
| **P6** J-pull | Finger sits comfortably, overhang clean without support in the D3 orientation. | `JPULL` (opening, depth, floor angle) | Three drawer fronts, sled front bar | 10 tall, 12 deep, 30° |
| **P7** quarter joint | Centre cross, wall crossing and beam pair all assemble by hand, hold without glue, faces flush within 0.2. | `DOVETAIL_CLR` | Bottom drawer quarters ×4 (D2), split beams (D6), rear box halves | 0.15 (iterate 0.05) |
| **P8** TPU foot | Spigot holds in the 2020 centre bore (nominal ~4.2, spec says 5 — expect to trim to ~4.6), foot sits flat, no wobble. | `SPIGOT_D` | Feet ×4, AWG pads ×4, sled-stop caps ×2 | 5.0 |
| **P9** bumper cup | Scope rear bumper drops in and locates, no rattle; front stand sits on the 5.5 pad inside the lip. | `BUMPER_CUP_CLR`, `PAD_LIP` | Scope cradles on the sled beams (cups ×2, pads ×2) | 0.3 |

Dependency chains: P1 + P7 + P9 + P6 → sled complete. P2 → all 12 cradles. P3 + P6 + P7 + P4 → drawers. P4 + P5 → skin. P8 → trim.

---

## 4. Stage 2 — frame (parallel with Stage 1)

Done when: PSU and AWG sit in the frame on temporary blocks at the right heights and the sled feet are on the scope rails.

1. Base: two base side rails + rear cross rail + four uprights, hidden L-connectors, square on the bench (diagonals equal within 1 mm), 321 clear width.
2. Top: top side rails + rear cross rail. Check 510 overall.
3. PSU rails at 68 using the 48 spacers; cast brackets doubled here.
4. Inner sub-frame: PSU-level inner rails, inner uprights, AWG-level inner rails, three 70 ties.
5. AWG rails at 227.5 using the 139.5 spacers.
6. **Scope rails last**, with a sled T-foot already threaded into each inner side slot; set at 311 using the 63.5 spacers; cast brackets doubled here. Check the beam clearance with the 3.0 gauge against a 336 reference before tightening.
7. Place PSU and AWG on blocks at 91 and 251.5; check 3 mm reveals, screen-edge alignment, PSU fan clear, AWG side vents uncovered.

Joint count is 42; 40 hidden connectors + 8 cast brackets is enough only if two of the doubled joints are cast-only. Check on the bench.

---

## 5. Stages 3–7 — production printing

Order follows the handover: cradles → drawers → sled → box and channel → skin → trim. Each stage lists its gates; a stage may start modelling before its gates pass but not printing.

| Stage | Gates | Parts | Done when |
|---|---|---|---|
| **3 Cradles** | P2 | PSU cradle ×3 (v2 as passed), AWG cradle ×4 (left reach 6.5, right 17.5, pads 3.5, corner lips), AWG TPU pads ×4 (P8 also) | PSU and AWG sit level, 3 mm behind the front plane, screens' left edges aligned, no rock. |
| **4 Drawers** | P3, P6, P7, P4 | Bottom runners → **test on the frame** → bottom drawer quarters ×4 (D2, assemble per the sheet, no glue) → runner test → CA the wall dovetails → column drawer (285, D5) → mini slot (285 with the vent neck, D7) → three fronts (on edge, D3) → housing-top tiles ×6 → column guide strips ×4, rear stops | All three run full travel, lift-to-remove works, fronts flush with the uprights, logo inlay reads. |
| **5 Sled** | P1, P7, P9, P6 | Feet ×2 (layers along the slide) → beams (split, D6) with arms, cups, pads → front bar → cross bars with guide lips → cable channel → stops (T-nut behind foot; T-nut + TPU cap at front) | Scope rides level, 100 travel, sag ≤ 1 mm out, stops hold, beam clears the AWG frame along the whole travel. |
| **6 Box + channel** | P7 | Box halves (dovetailed), 20 lip, guide-lip engagement on the cross bars; cable channel wedge tabs | Full access sequence works: pull sled 100 → fold door (skin not yet on: check the box exits right into the clear zone) → slide box out → reverse. Meters fit. |
| **7 Skin** | P4, P5 | 14 side tiles (155 long) → door + knuckles + magnet bosses + L-bracket → fixed rear tile with tab → top tiles ×4 + H-spline | Door swings 180 and catches; every tile snaps in; sled band 331–346 open; nothing fouls the sled or the box exit. |
| **8 Trim** | P8 | TPU feet ×4, blue caps ×4, probe hanger, strip brackets ×2 (**measure keyhole spacing first — open item 1**), stop caps, rear-right cable clips (**confirm AWG/PSU LAN/USB positions first — open item 4**) | Strip mounted, three IEC leads routed, LAN/USB down the rear-right, scope loop absorbs 100 travel, probes hang clear of the door. |

---

## 6. Files issued with this roadmap

`bench-stack-3d-v20.html` — current viewer: D2/D4/D5/D6 (v19, `src/viewer_v19_patch.py` applied to v18) plus D7 (`src/viewer_v20_patch.py` applied to v19). Rebuild chain: v18 → v19 → v20. `drawer-quarters-v1.pdf/.svg` — D2 joint sheet (`src/drawer_quarters_gen.py`).

## 7. Stage 9 — close-out

1. HANDOVER → v19: fold in D1–D6, final `fit.py` values, tile count, drawer depths.
2. Regenerate the viewer and layout from the final dimensions (`layout_gen.py`, `viewer_boxes.json`).
3. Archive every final STL with its script under `src/parts/`, named `<part>-v<N>.stl` matching the script version.

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
