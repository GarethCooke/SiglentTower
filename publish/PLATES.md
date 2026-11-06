# SiglentTower-complete.3mf — the plates (2026-11-05)

One Bambu Studio project with every printed part of the tower, one plate per print, in filament order; the jigs last. Made by `src/publish_3mf.py` from the fitted STLs in `parts/` (and `jigs/`, `coupons/spacers/`); re-run it after any part changes. Print profile `SiglentTower fit 0.20` on every plate (ROADMAP §2 has the settings). Coupons are not in it.

**Filament slots** (the project has five; set your own spools against them): 1 black ABS+ (eSUN — the sliding pairs and long thin bars), 2 dark blue PETG (the accents; it also stands in for the clear window on plate 28), 3 black ABS, 4 PETG in the colour the plate name says (black, dark grey, white, yellow — any PETG profile), 5 blue TPU 95A.

**Settings that are in the file, per object:** outer brim 5 mm with 0.1 gap on every ABS+ and ABS part that had one; outer brim 15 mm, gap 0 and outer wall 60 mm/s on the thin standing parts (the three facias and the four top tiles); ironing on the top surfaces of the runners; no brim and no support on the TPU; 2 walls and 15 % infill on the jigs.
**Settings that are NOT in the file** (filament- or plate-level — set them when you slice): dry ABS+ and TPU first; ABS and ABS+ with the door closed; the thin-part plates (26, 27, 28) with the skirt off, bed 80 °C, part fan 30 % max; the cradle plate (07) and the runner plates (02, 03, 05) with Quality → Bridge counterbore holes → Sacrificial layer; TPU from the external spool holder with the Generic TPU preset.

| Plate | Object | Turned | Centre x, y | Slot | Per-object settings |
|---|---|---|---|---|---|
| 01 | sled-foot-210.stl | 0° | 107.0, 181.5 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-foot-210.stl | 0° | 107.0, 198.6 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-left-front-v2.stl | 0° | 39.8, 86.5 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-right-front-v2.stl | 0° | 119.2, 86.5 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-left-rear-v1.stl | 0° | 180.8, 84.5 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-right-rear-v1.stl | 0° | 224.2, 84.5 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 02 | drawer-runner-300-v1.stl | 0° | 117.3, 117.3 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1, ironing_type top |
| 03 | drawer-runner-300-v1.stl | 0° | 117.3, 117.3 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1, ironing_type top |
| 04 | column-strip-upper-v1.stl | 45° | 117.4, 117.4 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 04 | column-strip-upper-v1.stl | 45° | 138.6, 138.6 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 05 | column-strip-lower-v1.stl | 45° | 112.4, 112.4 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 05 | column-strip-lower-short-v1.stl | 45° | 143.6, 143.6 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 06 | mini-slot-runner-v3.stl | 45° | 128.0, 128.0 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1, ironing_type top |
| 07 | psu-cradle-v3.stl | 0° | 22.0, 40.8 | 3 | brim_type outer_only, brim_width 5 |
| 07 | psu-cradle-v3.stl | 0° | 22.0, 122.4 | 3 | brim_type outer_only, brim_width 5 |
| 07 | psu-cradle-right-v4.stl | 0° | 66.0, 36.8 | 3 | brim_type outer_only, brim_width 5 |
| 07 | psu-cradle-right-front-v5.stl | 0° | 22.0, 202.0 | 3 | brim_type outer_only, brim_width 5 |
| 07 | awg-cradle-left-v2.stl | 0° | 200.0, 9.0 | 3 | brim_type outer_only, brim_width 5 |
| 07 | awg-cradle-left-v2.stl | 0° | 200.0, 27.0 | 3 | brim_type outer_only, brim_width 5 |
| 07 | awg-cradle-right-v2.stl | 0° | 109.2, 22.0 | 3 | brim_type outer_only, brim_width 5 |
| 07 | awg-cradle-right-v2.stl | 0° | 151.6, 22.0 | 3 | brim_type outer_only, brim_width 5 |
| 08 | sled-cross-bar-front-v2.stl | 45° | 116.7, 139.3 | 3 | brim_type outer_only, brim_width 5 |
| 08 | sled-cross-bar-rear-v2.stl | 45° | 136.8, 119.2 | 3 | brim_type outer_only, brim_width 5 |
| 09 | cable-channel-v1.stl | 0° | 15.2, 68.5 | 3 | brim_type no_brim |
| 09 | sled-splice-v2.stl | 0° | 14.8, 189.0 | 3 | brim_type no_brim |
| 09 | sled-splice-v2.stl | 0° | 44.2, 189.0 | 3 | brim_type no_brim |
| 09 | hinge-door-v2.stl | 0° | 66.0, 20.0 | 3 | brim_type no_brim |
| 09 | hinge-door-v2.stl | 0° | 42.0, 100.0 | 3 | brim_type no_brim |
| 09 | hinge-frame-v2.stl | 0° | 61.5, 99.0 | 3 | brim_type no_brim |
| 09 | hinge-frame-v2.stl | 0° | 63.5, 59.0 | 3 | brim_type no_brim |
| 09 | magnet-bracket-front-v2.stl | 0° | 42.5, 21.0 | 3 | brim_type no_brim |
| 09 | magnet-tab-rear-v2.stl | 0° | 43.0, 61.0 | 3 | brim_type no_brim |
| 10 | drawer-Q1-v1.stl | 0° | 84.8, 81.0 | 4 | — |
| 11 | drawer-Q2-v1.stl | 0° | 84.8, 81.0 | 4 | — |
| 12 | drawer-Q3-v1.stl | 0° | 84.8, 81.0 | 4 | — |
| 13 | drawer-Q4-v1.stl | 0° | 84.8, 81.0 | 4 | — |
| 14 | column-drawer-v3.stl | 45° | 128.0, 128.0 | 4 | brim_type outer_only, brim_width 5 |
| 15 | mini-slot-body-v1.stl | 45° | 128.0, 128.0 | 4 | brim_type outer_only, brim_width 5 |
| 15 | sled-front-rest-v2-gap3.0.stl | 0° | 30.0, 30.0 | 4 | — |
| 15 | sled-front-rest-v2-gap3.0.stl | 0° | 62.0, 30.0 | 4 | — |
| 15 | hinge-pins-v1.stl | 0° | 30.0, 66.0 | 4 | — |
| 16 | tile-band2-LF-v2.stl | 0° | 82.3, 79.5 | 4 | — |
| 16 | tile-band1-LF-v2.stl | 0° | 205.1, 79.5 | 4 | — |
| 17 | tile-band2-LR-v2.stl | 0° | 82.3, 79.5 | 4 | — |
| 17 | tile-band1-LR-v2.stl | 0° | 205.1, 79.5 | 4 | — |
| 18 | tile-band3-LF-v2.stl | 0° | 47.6, 79.5 | 4 | — |
| 18 | tile-band3-LR-v2.stl | 0° | 142.8, 79.5 | 4 | — |
| 19 | tile-band3-RF-v2.stl | 0° | 47.8, 79.5 | 4 | — |
| 19 | tile-band1-R-v2.stl | 0° | 133.1, 79.5 | 4 | — |
| 20 | tile-band3-RR-v2.stl | 0° | 47.8, 79.5 | 4 | — |
| 20 | tile-band1-R-v2.stl | 0° | 133.1, 79.5 | 4 | — |
| 21 | tile-band2-RF-v1.stl | 0° | 84.6, 79.5 | 4 | — |
| 21 | rear-tile-v2.stl | 90° | 211.2, 86.4 | 4 | — |
| 22 | tile-band2-RR-v1.stl | 0° | 84.6, 79.5 | 4 | — |
| 22 | board-enclosure-v1.stl | 0° | 201.2, 56.0 | 4 | — |
| 22 | board-lid-v1.stl | 0° | 201.2, 167.8 | 4 | — |
| 23 | tile-band4-LF-v1.stl | 0° | 85.9, 79.5 | 4 | — |
| 24 | tile-band4-LR-v1.stl | 0° | 85.9, 79.5 | 4 | — |
| 25 | door-v3.stl | 0° | 82.5, 117.0 | 4 | — |
| 26 | top-tile-FL-v1.stl | 0° | 110.0, 18.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 26 | top-tile-FR-v1.stl | 0° | 110.0, 55.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 26 | top-tile-RL-v1.stl | 0° | 110.0, 92.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 26 | top-tile-RR-v1.stl | 0° | 110.0, 129.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 26 | upright-cap-v1.stl | 0° | 231.9, 12.0 | 2 | — |
| 26 | upright-cap-v1.stl | 0° | 231.9, 36.0 | 2 | — |
| 26 | upright-cap-v1.stl | 0° | 231.9, 60.0 | 2 | — |
| 26 | upright-cap-v1.stl | 0° | 231.9, 84.0 | 2 | — |
| 27 | drawer-facia-v1.stl + drawer-facia-logo-v1.stl | 45° | 128.0, 128.0 | 4 + 2 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 28 | column-facia-v1.stl | 45° | 123.1, 132.9 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 28 | sill-panel-v3.stl + sill-panel-window-v4.stl | 45° | 132.9, 123.1 | 4 + 2 | brim_type outer_only, brim_width 5 |
| 28 | mini-slot-facia-v1.stl | 0° | 52.0, 232.0 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 29 | sled-front-bar-v3.stl | 45° | 128.0, 128.0 | 4 | brim_type outer_only, brim_width 5 |
| 30 | rear-box-left-v1.stl | 0° | 78.8, 69.5 | 4 | brim_type outer_only, brim_width 5 |
| 31 | rear-box-right-v1.stl | 0° | 78.8, 69.5 | 4 | brim_type outer_only, brim_width 5 |
| 32 | pull-insert-bottom-v2.stl | 0° | 62.0, 23.5 | 2 | — |
| 32 | pull-insert-column-v2.stl | 0° | 153.5, 29.0 | 2 | — |
| 32 | pull-insert-mini-v2.stl | 0° | 197.5, 29.0 | 2 | — |
| 32 | sled-bar-pull-liner-v1.stl | 0° | 61.9, 54.9 | 2 | — |
| 33 | box-brace-v1.stl | 0° | 136.0, 9.5 | 4 | brim_type no_brim |
| 33 | box-brace-v1.stl | 0° | 136.0, 28.5 | 4 | brim_type no_brim |
| 33 | strip-bracket-upper-v2.stl | 0° | 207.1, 22.0 | 4 | brim_type no_brim |
| 33 | strip-bracket-lower-v5.stl | 0° | 42.0, 34.0 | 4 | brim_type no_brim |
| 33 | sill-block-left-v10.stl | 0° | 109.8, 46.0 | 4 | brim_type no_brim |
| 33 | sill-block-right-v4.stl | 0° | 152.7, 46.0 | 4 | brim_type no_brim |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 5.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 17.1 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 28.5 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 39.9 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 51.3 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 62.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 14.0, 82.4 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 14.0, 110.4 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 14.0, 138.4 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 14.0, 166.4 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-left-v1.stl | 0° | 12.0, 192.4 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-left-v1.stl | 0° | 12.0, 216.4 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-right-v1.stl | 0° | 14.3, 234.2 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-right-v1.stl | 0° | 14.3, 245.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | sled-stop-cap-v1.stl | 0° | 250.0, 5.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | sled-stop-cap-v1.stl | 0° | 250.0, 17.1 | 5 | brim_type no_brim, enable_support 0 |
| 35 | spacer-159.stl | 0° | 81.5, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-159.stl | 0° | 81.5, 36.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-139.5.stl | 0° | 71.8, 60.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-139.5.stl | 0° | 71.8, 84.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-63.5.stl | 0° | 196.8, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-63.5.stl | 0° | 196.8, 36.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-48.stl | 0° | 169.5, 84.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-48.stl | 0° | 221.5, 84.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | gauge-3.0.stl | 0° | 175.5, 60.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-psu-L.stl | 0° | 34.2, 125.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-psu-R.stl | 0° | 102.8, 123.5 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-awg-L.stl | 0° | 149.0, 113.5 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-awg-R.stl | 0° | 173.0, 112.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 149.0, 239.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 173.0, 236.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 197.0, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 221.0, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |

Plate names in the project: 01 ABS+ black — sled T-feet ×2, beam halves ×4 (feet standing; outer brim 5); 02 ABS+ black — bottom drawer runner (1 of 2; leg top down, ironing on top); 03 ABS+ black — bottom drawer runner (2 of 2); 04 ABS+ black — column guide strips upper ×2 (rail face down, diagonal); 05 ABS+ black — column guide strips lower right + lower left short; 06 ABS+ black — mini-slot runner v3 (plate down, diagonal, ironing on top); 07 ABS black — cradles: PSU left v3 ×2, right rear v4, right front v5, AWG left v2 ×2, right v2 ×2 (sacrificial layer in the cups); 08 ABS black — sled cross bars front + rear v2 (flat, lips up, diagonal); 09 ABS black — cable channel, splices ×2, hinge leaves 2 + 2, magnet bracket, magnet tab; 10 PETG black — bottom drawer quarter Q1; 11 PETG black — bottom drawer quarter Q2; 12 PETG black — bottom drawer quarter Q3; 13 PETG black — bottom drawer quarter Q4; 14 PETG black — column drawer v3 (floor down, diagonal, outer brim 5; ~24 h); 15 PETG black — mini-slot body (diagonal, outer brim 5) + sled front rests ×2 + hinge pins; 16 PETG black — tiles A2: band2-LF + band1-LF; 17 PETG black — tiles B2: band2-LR + band1-LR; 18 PETG black — tiles C2: band3-LF + band3-LR; 19 PETG black — tiles D2: band3-RF + band1-R; 20 PETG black — tiles E2: band3-RR + band1-R; 21 PETG black — tile band2-RF + door set fixed rear tile v2; 22 PETG black — tile band2-RR + lighting board enclosure + lid; 23 PETG black — tile band4-LF (legs stand 19); 24 PETG black — tile band4-LR; 25 PETG black — door v3 (face down); 26 PETG black + dark blue — top panel: four tiles standing (thin-part settings) + upright caps ×4 (blue); 27 PETG dark grey + dark blue — bottom drawer facia + iguana logo (standing, diagonal, thin-part settings); 28 PETG dark grey (+ natural for the window) — column facia, sill panel + window, mini-slot facia (standing); 29 PETG dark grey — sled front bar v3 (front face down, diagonal, outer brim 5); 30 PETG dark grey — rear box left half (floor down, outer brim 5); 31 PETG dark grey — rear box right half; 32 PETG dark blue — pull inserts bottom / column / mini v2 + sled-bar liner (supports on, build plate only); 33 PETG any colour (hidden parts) — box braces ×2, strip brackets upper v2 + lower v5, sill blocks left v10 + right v4; 34 TPU blue 95A — frame feet ×4, AWG pads 2 + 2, sled stop caps ×2, slot covers ×6 (no brim, no support; dried, external spool); 35 JIG — any colour, any PETG/PLA — rail spacers 48 / 63.5 / 139.5 / 159 ×2 each + the 3.0 web gauge; 36 JIG — any colour, any PETG/PLA — seating jigs PSU L / R, AWG L / R + AWG pad stand-ins ×4.

Hardware the plates need, from HANDOVER §10: 47 M5 × 10 button head (4 into the uprights' bores, no T-nut), 9 M5 × 10 countersunk, 2 M5 × 12, 54 drop-in T-nuts, M5 × 8 for the 8 cast brackets, 4 M3 × 10, 4 Ø10 × 2 magnets, the 8 mm button and its nut, CA glue.
