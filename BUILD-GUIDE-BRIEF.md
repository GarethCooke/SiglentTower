# Build guide — brief for Claude Code

**Repo:** `C:\Development\3DPrinting\SiglentTower` · **Owner:** Gareth Cooke · **Written:** 2026-11-08 · **Output:** `docs/BUILD-GUIDE.md`

## 1. Goal

Write the document that takes someone from nothing to the finished tower (ROADMAP Stage 9, "Full build guide", Gareth 2026-09-28): what to buy, what to cut, what to print, and then the build in order, each step with the jig it uses, the check that says it is right, and the glue and screw notes. It is **how to build it**; the write-up (a separate Stage 9 item, not this job) is the story of designing it.

Its reader has a Bambu printer and the 2020 extrusion, has downloaded the repository or the MakerWorld pack, and has not read any other document. They may well have different instruments: say what is specific to the three Siglents (cradle cups, the AWG vent channel, the scope's bumper and stand positions) and what is not.

Read, in this order, before writing anything:

1. `HANDOVER.md` (v19) — the as-built record: levels, every part, the parts index (§10) with material, orientation and hardware, the coupon results, the decisions, the sheet index (§13). **This is the authority for every number.**
2. `publish/PLATES.md` and `publish/plates-sheet.png` — the 36 plates of `publish/SiglentTower-complete.3mf`, the settings the file carries and the ones it cannot.
3. `publish/makerworld/MAKERWORLD.md` — the listing; the guide must agree with it (the "ideas, not a kit" position, the hardware list, the print notes) and go deeper.
4. `CUT-TABLE.md` — the cut sheet by jig setting, and ROADMAP §2's notes on accuracy.
5. `ROADMAP.md` §Stage 2 — the frame build method (each side flat on the bench with all five rails at once, spacers, a sled foot in each scope rail before the ends close, connectors on the inward faces, cast brackets under the scope rails, T-nut counts) and the assembly viewer `frame-assembly-3d.html`.
6. The check sheets under `parts/` (HANDOVER §13 lists them): `drawer/drawer-quarters-plan.png`, `drawer/drawer-facia-plan.png`, `column/column-plan.png`, `mini/mini-slot-plan.png`, `sled-beam-plan.png`, `sled-ladder-plan.png`, `sled-front-rest-plan.png`, `rear-box-plan.png`, `door/door-plan.png`, `door/hinge-how.png`, `tiles/skin-sheet.png`, `top/top-panel-plan.png`, `sill/sill-panel-plan.png`, `tpu/tpu-where*.png`, `wiring/wiring-4-connections.png`, `wiring/wiring-2-runs.png`, `wiring/perfboard-layout.png`, `wiring/board-enclosure-plan.png`, `awg-mount-sheet.png`, `strip-bracket-v4.png`. Look at each one: the guide points the reader at them at the step where they help.
7. `PRINT-RULES.md` §1 and ROADMAP §2's print-settings table — for the printing chapter.
8. `src/jigs/seating_jigs.py` and `src/coupons/spacers.py` headers — what the jigs do and how they are used.

**Do not change any part script, STL, sheet, `fit.py`, HANDOVER or the .3mf.** This job writes one document (and may add diagrams under `docs/`). Where sources disagree, HANDOVER wins over ROADMAP prose, ROADMAP's latest dated entry wins over an earlier one, and you list what you resolved in your summary.

## 2. Shape

Markdown, in `docs/BUILD-GUIDE.md`, with the images referenced by relative path so it reads on GitHub. Chapters, in this order:

0. **Before you start** — what this is and is not (the parts fit a frame as it was cut and assembled; expect to measure your frame and re-export tiles and cradles; the scripts make that a measurement, not a redesign); what you need to know about your own instruments; time and cost in round figures (seven weeks of evenings, ~2.5 kg of filament, the extrusion pack).
1. **Shopping list** — tables with quantities: extrusion and connectors (from HANDOVER §2 and the MakerWorld hardware list), screws and T-nuts (HANDOVER §10's count), magnets, pins, glue, the power strip, the lighting parts (optional chapter), filament by colour and type with rough weights (MAKERWORLD.md's table).
2. **Tools** — what was actually used: the cutting jig and saw, deburring, calipers, hex keys (sizes), a 3 mm ball-end key for the sill bolt, drill bits named in the record (5.5 for the strip brackets), files, CA glue, a soldering iron and crimper only for the lighting.
3. **Cutting the extrusion** — the cut sheet by jig setting, the labelling rule, the accuracy note (±0.5 fine, match within a set, square ends, err short), deburring.
4. **Printing** — the complete .3mf: how to open it, the five filament slots, the profile, one material per plate, the order to print in (it is the plate order), the settings the file cannot carry (dry, door, skirt 0, thin-part bed and fan, sacrificial layer, TPU from the external spool), the two jig plates, how long the big plates take. The thin-part warping note from MAKERWORLD.md, in full.
5. **The frame** — the flat-side method step by step with the spacers and the connector plan; the T-nuts that must go in before a rail closes a slot; the sled foot in each scope rail; joining the sides; the sub-frame; the checks (diagonals equal within 1 mm, 321 clear front and rear, 510 overall, no wobble); the feet. Point at `frame-assembly-3d.html`.
6. **Measuring your frame** — the step this build added: caliper the rail gaps on each side, the sub-frame position, the frame width; what each reading changes (tile bands per side via `side_tile.GAPS`, the sill panel length, the top panel width) and the command to re-export. Plain words; say what to type.
7. **Cradles and instruments** — PSU cradles with the seating jigs, AWG cradles, the pads, seating the instruments, what "right" looks like (fronts in line, level, no rock, 3 mm reveals, vents clear).
8. **Drawers** — runners (four M5 each, pulled flat), the four quarters assembled in order and glued, the facia and pull insert, the column drawer and its four strips (the short one on the left), the mini slot and its runner, removal (pull clean off; the mini unbolts).
9. **The sled and the box** — feet into the rails (already done in the frame step), beam halves glued at the tab and threaded onto the feet, front bar slid on over the tongues, cross bars, front rests set with the sled moving, splices, cable channel, stop caps; the box halves joined and braced; the access sequence and the 7.5 mm lift over the right splice.
10. **The skin** — which tile goes where (the skin sheet), how a tile snaps in and comes out (a blade against a finger's free end), band 4 left's legs, the door set in fitting order with the hinge pins CA'd into the door leaf only and the magnet polarity trick (door-plan.png), the top panel's tile order and glue.
11. **Trim** — TPU feet (glued into the bores), AWG pads, stop caps, slot covers cut to length, upright caps, strip brackets and the power strip, sill panel with its blocks (the bolt from the key hole, the panel pressed on, the button fitted with its wires through the slit), IEC leads and the scope's cable loop.
12. **Lighting (optional)** — the parts, the perfboard (point at the layout sheet), the enclosure, the runs under the covers, the connections sheet, first power-up; SiglentGlow as the firmware used, with the note that any WS2812 controller works.
13. **Checks before you call it done** — the Stage "Done when" lines from ROADMAP §5 turned into a checklist.
14. **If something does not fit** — the record's own fixes, as a table: symptom → what it was → what to do (tiles short at the top → rail gap, re-read with calipers, re-export; cradle cups off the feet → measure foot spacing, cradle reach constants; drawer binds → runner flat on four bolts, ironing; sled front sags → rests gap variant; printed as the wrong hand → export from the real frame).

Each build step: **a numbered list of actions** (one action per number, the exact part name from the parts index, the screw and the jig), then the check, then any note. Diagrams: reference the existing sheets; where a step has no sheet and needs one (the frame flat-side layout; the drawer-quarter assembly order; the sled assembly order), draw it as an SVG under `docs/` with a small script in `src/` the same way the other sheets are made, or describe it in words if a drawing adds nothing.

## 3. Rules for the writing

- Plain words, no invented terms (Gareth: he had to ask what "bezel" and "CA" meant — say "superglue (CA)" the first time, then "CA"). Metric. Numbers in mm. Every number from HANDOVER or `fit.py`.
- The reader does the work with the document open on a phone at the bench: short steps, one action each, the part named as its STL is named.
- Say what to check after each stage and what a failure looks like, with the record's example when there is one.
- Length: whatever the content needs; this is the long document. Chapters 0–4 under ~2,000 words together; the build chapters as long as the steps need.
- Nothing in this document is a sales pitch; the listing does that.

## 4. Also

- Add `docs/BUILD-GUIDE.md` to the README's repository map and to `publish/makerworld/MAKERWORLD.md` → Links; tick ROADMAP Stage 9's "Full build guide" bullet with the date and add a one-line v2.x changelog entry; keep `claude/ROADMAP.md` in the project in step if you have the Projects tool, otherwise say so.
- Commit in the repo's style: subject line, short body, `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`; message written to `.git/build-guide-commit-msg.txt`, committed with `git commit -F`; give Gareth the `cd` and `git commit -F` lines as numbered steps.

## 5. Done when

1. `docs/BUILD-GUIDE.md` has chapters 0–14 above, every build step as numbered actions with its check, every number traceable, every referenced image present at the path given.
2. A reader could cut, print, assemble and wire the tower from it without opening HANDOVER — and knows where HANDOVER is when they want the why.
3. README, MAKERWORLD.md and ROADMAP updated; the summary lists anything the sources did not settle.
