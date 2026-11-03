# HANDOVER v19 — brief for Claude Code

**Repo:** `C:\Development\3DPrinting\SiglentTower` · **Owner:** Gareth Cooke · **Written:** 2026-11-03

## 1. Goal

Rewrite `HANDOVER.md` from v18 (the frozen design of 2026-09-15, before anything was printed) into **v19: the as-built record of the finished tower.** The build is complete and working (ROADMAP v2.35, 2026-11-03). v19 is the document someone opens to understand what was built, with every number matching the bench, and it is the source the build guide and the write-up (ROADMAP Stage 9) will be written from.

Read, in this order, before writing anything:

1. `HANDOVER.md` (v18) — the structure to keep and the design intent.
2. `ROADMAP.md` (v2.35) — **the authority for everything that changed.** §0 decisions D1–D15, the Progress block, every "Print job" and "Status" paragraph (they record what was printed, what failed, what was measured and what replaced what), §3 the coupon results, §Stage 2 the frame build method.
3. `src/fit.py` — every tuned clearance and every measured dimension, with the coupon that set it.
4. `PRINT-RULES.md` — the print rules and the design-for-print review of every part.
5. `src/parts/*.py` — the header comment of each script says what the part is, its version history and where it sits; `parts/**/*.stl` are the exports; `parts/**/*.png` the check sheets.
6. `parts/wiring/wiring-4-connections.png`, `wiring-2-runs.png`, `perfboard-layout.png`, `board-enclosure-plan.png`, `SiglentGlow-BRIEF.md` — the lighting as built.

**Do not change any part script, STL, sheet or `fit.py`.** This job writes documentation only. If you find a contradiction between sources, ROADMAP's latest dated entry wins over HANDOVER v18, `fit.py` wins over prose for a number, and you list every contradiction you resolved in your summary.

## 2. What v19 is

Keep v18's shape so it stays recognisable, and update every section to the tower as it stands:

- **Header:** v19, 2026-11-03, "as built". The file list becomes the sheet index (see §3 below).
- **§1 Instruments** — the measured values that were used (`fit.py` has the scope bumper, stand and PSU figures; ROADMAP has the AWG vent and the instrument dimensions).
- **§2 Frame** — the cut list as cut (ROADMAP §2 cut sheet), the connector plan as used (ROADMAP §Stage 2: hidden L-connectors on the inward faces, cast brackets under the scope rails, the flat-side build method with spacers), **the measured corrections**: rail heights per side (ROADMAP 2026-10-14: right 45.4 / 139.5 / 65.8 / 158, left 51.2 / 135 / 65.5 / 157), the sub-frame upright at x 253.7 and flush with the front, the frame 362 × 350 by tape, PSU position (`fit.py` PSU_FACE_X, PSU_FEET_CC).
- **§3 Levels** — the final z table.
- **§4 Scope sled** — as built: T-feet in the scope rails' inner slots, split beams on the P7 tab, front bar v3 with the tongue-in-pocket, cross bars v2, front rests v2 on the rail tops, splice bars v2, cable channel v1, TPU stop caps (travel 92), the box lift over the right splice. Drop v18's wedge tabs and anything else ROADMAP records as withdrawn.
- **§5 Panels and door** — the side skin as built (14 tiles, P4 clips, bands at the measured heights with saddle notches, band 4 left with bolted legs), the door set (door v3, hinge v2 at axis x 369 / z 341, the edge at 338, magnets), the top panel (D12: four standing tiles, glued half-laps, caps screwed into the bores). D14: no drawer lids.
- **§6 Storage and pulls** — the three drawers as built (quarters + runners, column + strips, mini slot + runner v3 with the D7 vent neck), the pull inserts v2 with the flange-and-leg hook, facias with pegs, D15: no stops, removal = pull clean off.
- **§7 Cable management and power** — the Addtam vertical on the rear-left upright on brackets upper v2 / lower v5 (and the bolt-hole bug), the three IEC leads, the scope loop, the sill panel + blocks (left v10, right v4, window v4) and **the lighting as built, D10 rev 5**: SiglentGlow firmware on the XIAO ESP32-S3 Plus, the perfboard, the enclosure, the strips, the WS2812D-F5 sill pixels (legs DOUT, VDD, GND, DIN), the button, the plugs and runs. Open item 4 (rear-right cable clips) and the probe hanger: **not built, by choice** — say so.
- **§8 Materials and colours** — as used (ROADMAP §2 "Black spools" and the colour scheme; ABS+ for sliding pairs, ABS for fixed black parts, PETG elsewhere, TPU once at the end).
- **§9 Open items** — none open. Replace with a short "Known compromises" list: the slight PSU skew accepted, the 2.7 mm sub-frame offset, the sled front carried on the rests, the box lift over the splice, the 15-LED strips (dimmer than the 28 planned), anything else ROADMAP records as "accepted".
- **§10 Next work** → **§10 Parts index**: one table, every printed part in the tower: part, version as fitted, script (`src/parts/…`), STL path, material/colour, quantity, print orientation in one phrase, hardware it takes. Build it from the ROADMAP print-job paragraphs and the `parts/` tree; list superseded STLs in a separate "Withdrawn" table (file, replaced by). The jigs (`jigs/`, `coupons/spacers`) get their own short table.
- **§11 Prototype before committing filament** → **§11 Coupon results**: P1–P9, each with what it tested, the rounds, the pass value, and the `fit.py` constant it set (ROADMAP §3 has all of it).
- **§12 Decisions D1–D15** (new): a table of decision, choice, date, in one line each, from ROADMAP §0.
- **§13 Sheets and viewers** (new): every check sheet and plan PNG, the two HTML viewers, what each shows and the script that makes it.

## 3. Rules for the writing

- Plain words, no invented terms; Gareth does not read code. Numbers in mm, with the frame coordinate convention stated once at the top (x from the left upright's outer face, y from the front plane, z from the rail bottoms; the frame stands 6 mm above the bench on its feet).
- Every number traceable to `fit.py`, ROADMAP or a script comment. Where v18 and the build differ, state the as-built value and, in brackets, "(v18: …)" so the change is visible.
- Dated history belongs in ROADMAP; v19 states the result, with at most a clause of why.
- Keep it under ~25 000 characters. The parts index may be long; the prose should not be.

## 4. Also

- Tick ROADMAP's Stage 9 first bullet ("HANDOVER → v19 …") and bump the ROADMAP header to v2.36 with a one-line changelog entry in the v2.x list.
- Commit in the repo's style (a subject line, a short body; end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`), message written to `.git/handover-v19-commit-msg.txt` and committed with `git commit -F`.

## 5. Done when

1. `HANDOVER.md` is v19 with §1–§13 as above, no open item that ROADMAP shows closed, and no part or value that ROADMAP shows withdrawn.
2. The parts index lists every STL under `parts/` that is fitted on the tower, and every withdrawn STL appears in the Withdrawn table (cross-check against the ROADMAP "withdrawn" mentions).
3. ROADMAP Stage 9 bullet 1 ticked, header v2.36.
4. Your summary lists the contradictions you resolved and anything you could not settle from the sources.
