# SiglentTower-complete.3mf — the plates (2026-11-07)

One Bambu Studio project with every printed part of the tower, one plate per print, in filament order; the jigs last. Made by `src/publish_3mf.py` from the fitted STLs in `parts/` (and `jigs/`, `coupons/spacers/`); re-run it after any part changes. Print profile `SiglentTower fit 0.20` on every plate (ROADMAP §2 has the settings). Coupons are not in it.

**Filament slots** (the project has five; set your own spools against them): 1 black ABS+ (eSUN — the sliding pairs and long thin bars), 2 dark blue PETG (the accents; it also stands in for the clear window on plate 28), 3 black ABS, 4 PETG in the colour the plate name says (black, dark grey, white, yellow — any PETG profile), 5 blue TPU 95A.

**One material per plate** (Gareth, 2026-11-06): no plate mixes filaments, so no purge tower — except the two objects that are two-colour by design, each on its own plate: the bottom facia with its logo inlay (26) and the sill panel with its clear window (27).

**Skirt loops 0 in the profile** (plate 13's column drawer leaves no room for one; the brims do that job).

**Settings that are in the file, per object:** outer brim 5 mm with 0.1 gap on every ABS+ and ABS part that had one; outer brim 15 mm, gap 0 and outer wall 60 mm/s on the thin standing parts (the three facias and the four top tiles); ironing on the top surfaces of the runners; no brim and no support on the TPU; 2 walls and 15 % infill on the jigs.
**Settings that are NOT in the file** (filament- or plate-level — set them when you slice): dry ABS+ and TPU first; ABS and ABS+ with the door closed; the thin-part plates (25, 26, 27, 28) with the skirt off, bed 80 °C, part fan 30 % max; the cradle plate (06) and the runner plates (02, 03, 05) with Quality → Bridge counterbore holes → Sacrificial layer; TPU from the external spool holder with the Generic TPU preset.

| Plate | Object | Turned | Centre x, y | Slot | Per-object settings |
|---|---|---|---|---|---|
| 01 | sled-foot-210.stl | 0° | 131.8, 37.1 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-foot-210.stl | 0° | 131.8, 54.1 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-left-front-v2.stl | 0° | 46.7, 163.0 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-right-front-v2.stl | 0° | 125.2, 162.2 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-left-rear-v1.stl | 0° | 185.4, 160.5 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 01 | sled-beam-right-rear-v1.stl | 0° | 229.1, 160.2 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 02 | drawer-runner-300-v1.stl | 0° | 129.9, 128.2 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1, ironing_type top |
| 03 | drawer-runner-300-v1.stl | 0° | 133.9, 126.6 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1, ironing_type top |
| 04 | column-strip-upper-v1.stl | 45° | 117.4, 117.4 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 04 | column-strip-upper-v1.stl | 45° | 138.6, 138.6 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 05 | column-strip-lower-v1.stl | 45° | 112.8, 112.8 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 05 | mini-slot-runner-v3.stl | 45° | 134.0, 134.0 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1, ironing_type top |
| 05 | column-strip-lower-short-v1.stl | 45° | 155.2, 155.2 | 1 | brim_type outer_only, brim_width 5, brim_object_gap 0.1 |
| 06 | psu-cradle-v3.stl | 0° | 148.0, 117.2 | 3 | brim_type outer_only, brim_width 5 |
| 06 | psu-cradle-v3.stl | 0° | 212.0, 117.2 | 3 | brim_type outer_only, brim_width 5 |
| 06 | psu-cradle-right-v4.stl | 0° | 84.0, 62.8 | 3 | brim_type outer_only, brim_width 5 |
| 06 | psu-cradle-right-front-v5.stl | 0° | 84.0, 195.2 | 3 | brim_type outer_only, brim_width 5 |
| 06 | awg-cradle-left-v2.stl | 0° | 206.8, 187.0 | 3 | brim_type outer_only, brim_width 5 |
| 06 | awg-cradle-left-v2.stl | 0° | 206.8, 225.0 | 3 | brim_type outer_only, brim_width 5 |
| 07 | sled-cross-bar-front-v2.stl | -45° | 116.7, 116.7 | 3 | brim_type outer_only, brim_width 5 |
| 07 | sled-cross-bar-rear-v2.stl | -45° | 136.8, 136.8 | 3 | brim_type outer_only, brim_width 5 |
| 08 | awg-cradle-right-v2.stl | 0° | 63.3, 148.0 | 3 | brim_type outer_only, brim_width 5 |
| 08 | awg-cradle-right-v2.stl | 0° | 63.3, 212.0 | 3 | brim_type outer_only, brim_width 5 |
| 08 | cable-channel-v1.stl | 0° | 218.7, 165.5 | 3 | brim_type no_brim |
| 08 | sled-splice-v2.stl | 0° | 119.2, 182.0 | 3 | brim_type no_brim |
| 08 | sled-splice-v2.stl | 0° | 168.7, 182.0 | 3 | brim_type no_brim |
| 08 | hinge-door-v2.stl | 0° | 135.5, 46.0 | 3 | brim_type no_brim |
| 08 | hinge-door-v2.stl | 0° | 178.5, 46.0 | 3 | brim_type no_brim |
| 08 | hinge-frame-v2.stl | 0° | 60.0, 45.0 | 3 | brim_type no_brim |
| 08 | hinge-frame-v2.stl | 0° | 96.0, 45.0 | 3 | brim_type no_brim |
| 08 | magnet-bracket-front-v2.stl | 0° | 222.0, 56.0 | 3 | brim_type no_brim |
| 08 | magnet-tab-rear-v2.stl | 0° | 78.9, 89.6 | 3 | brim_type no_brim |
| 09 | drawer-Q1-v1.stl | 0° | 84.8, 111.0 | 4 | — |
| 10 | drawer-Q2-v1.stl | 0° | 84.8, 111.0 | 4 | — |
| 11 | drawer-Q3-v1.stl | 0° | 84.8, 111.0 | 4 | — |
| 12 | drawer-Q4-v1.stl | 0° | 84.8, 111.0 | 4 | — |
| 13 | column-drawer-v3.stl | 45° | 126.3, 132.4 | 4 | brim_type outer_only, brim_width 5 |
| 14 | mini-slot-body-v1.stl | 45° | 128.0, 128.0 | 4 | brim_type outer_only, brim_width 5 |
| 14 | sled-front-rest-v2-gap3.0.stl | 0° | 40.0, 42.0 | 4 | — |
| 14 | sled-front-rest-v2-gap3.0.stl | 0° | 72.0, 42.0 | 4 | — |
| 14 | hinge-pins-v1.stl | 0° | 40.0, 78.0 | 4 | — |
| 15 | tile-band2-LF-v2.stl | 0° | 82.3, 109.5 | 4 | — |
| 15 | tile-band1-LF-v2.stl | 0° | 205.1, 79.5 | 4 | — |
| 16 | tile-band2-LR-v2.stl | 0° | 82.3, 109.5 | 4 | — |
| 16 | tile-band1-LR-v2.stl | 0° | 205.1, 79.5 | 4 | — |
| 17 | tile-band3-LF-v2.stl | 0° | 47.6, 109.5 | 4 | — |
| 17 | tile-band3-LR-v2.stl | 0° | 142.8, 79.5 | 4 | — |
| 18 | tile-band3-RF-v2.stl | 0° | 47.8, 109.5 | 4 | — |
| 18 | tile-band1-R-v2.stl | 0° | 133.1, 79.5 | 4 | — |
| 19 | tile-band3-RR-v2.stl | 0° | 47.8, 109.5 | 4 | — |
| 19 | tile-band1-R-v2.stl | 0° | 133.1, 79.5 | 4 | — |
| 20 | tile-band2-RF-v1.stl | 0° | 168.6, 79.5 | 4 | — |
| 20 | rear-tile-v2.stl | 90° | 42.0, 116.4 | 4 | — |
| 21 | tile-band2-RR-v1.stl | 0° | 104.6, 79.5 | 4 | — |
| 21 | board-enclosure-v1.stl | 0° | 221.2, 56.0 | 4 | — |
| 21 | board-lid-v1.stl | 0° | 221.2, 167.8 | 4 | — |
| 22 | tile-band4-LF-v1.stl | 0° | 105.9, 79.5 | 4 | — |
| 23 | tile-band4-LR-v1.stl | 0° | 105.9, 79.5 | 4 | — |
| 24 | door-v3.stl | 0° | 102.5, 117.0 | 4 | — |
| 25 | top-tile-FL-v1.stl | 0° | 130.0, 18.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 25 | top-tile-FR-v1.stl | 0° | 110.0, 55.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 25 | top-tile-RL-v1.stl | 0° | 110.0, 92.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 25 | top-tile-RR-v1.stl | 0° | 110.0, 129.5 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 26 | drawer-facia-v1.stl + drawer-facia-logo-v1.stl | -45° | 128.0, 128.0 | 4 + 2 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 27 | sill-panel-v3.stl + sill-panel-window-v4.stl | -45° | 128.0, 128.0 | 4 + 2 | brim_type outer_only, brim_width 5 |
| 28 | column-facia-v1.stl | -45° | 128.0, 128.0 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 28 | mini-slot-facia-v1.stl | 0° | 70.0, 30.0 | 4 | brim_type outer_only, brim_width 15, brim_object_gap 0, outer_wall_speed 60 |
| 29 | sled-front-bar-v3.stl | -45° | 128.0, 128.0 | 4 | brim_type outer_only, brim_width 5 |
| 30 | rear-box-left-v1.stl | 0° | 98.8, 69.5 | 4 | brim_type outer_only, brim_width 5 |
| 31 | rear-box-right-v1.stl | 0° | 98.8, 69.5 | 4 | brim_type outer_only, brim_width 5 |
| 32 | upright-cap-v1.stl | 0° | 244.0, 12.0 | 2 | — |
| 32 | upright-cap-v1.stl | 0° | 244.0, 36.0 | 2 | — |
| 32 | upright-cap-v1.stl | 0° | 244.0, 60.0 | 2 | — |
| 32 | upright-cap-v1.stl | 0° | 135.7, 70.0 | 2 | — |
| 32 | pull-insert-bottom-v2.stl | 0° | 82.0, 23.5 | 2 | — |
| 32 | pull-insert-column-v2.stl | 0° | 173.5, 29.0 | 2 | — |
| 32 | pull-insert-mini-v2.stl | 0° | 217.5, 29.0 | 2 | — |
| 32 | sled-bar-pull-liner-v1.stl | 0° | 61.9, 54.9 | 2 | — |
| 33 | box-brace-v1.stl | 0° | 72.0, 9.5 | 4 | brim_type no_brim |
| 33 | box-brace-v1.stl | 0° | 176.0, 9.5 | 4 | brim_type no_brim |
| 33 | strip-bracket-upper-v2.stl | 0° | 174.8, 41.0 | 4 | brim_type no_brim |
| 33 | strip-bracket-lower-v5.stl | 0° | 62.0, 53.0 | 4 | brim_type no_brim |
| 33 | sill-block-left-v10.stl | 0° | 129.8, 27.0 | 4 | brim_type no_brim |
| 33 | sill-block-right-v4.stl | 0° | 121.0, 43.0 | 4 | brim_type no_brim |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 35.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 47.1 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 58.5 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 69.9 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 81.3 | 5 | brim_type no_brim, enable_support 0 |
| 34 | slot-cover-240-v1.stl | 0° | 122.0, 92.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 62.7, 14.0 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 90.7, 14.0 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 118.7, 14.0 | 5 | brim_type no_brim, enable_support 0 |
| 34 | frame-foot-v1.stl | 0° | 146.7, 14.0 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-left-v1.stl | 0° | 172.7, 12.0 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-left-v1.stl | 0° | 196.7, 12.0 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-right-v1.stl | 0° | 34.4, 5.8 | 5 | brim_type no_brim, enable_support 0 |
| 34 | awg-pad-right-v1.stl | 0° | 34.4, 17.2 | 5 | brim_type no_brim, enable_support 0 |
| 34 | sled-stop-cap-v1.stl | 0° | 250.0, 5.7 | 5 | brim_type no_brim, enable_support 0 |
| 34 | sled-stop-cap-v1.stl | 0° | 250.0, 17.1 | 5 | brim_type no_brim, enable_support 0 |
| 35 | spacer-159.stl | 0° | 101.5, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-159.stl | 0° | 101.5, 36.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-139.5.stl | 0° | 71.8, 60.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-139.5.stl | 0° | 71.8, 84.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-63.5.stl | 0° | 216.8, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-63.5.stl | 0° | 216.8, 36.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-48.stl | 0° | 169.5, 84.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | spacer-48.stl | 0° | 221.5, 84.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 35 | gauge-3.0.stl | 0° | 175.5, 60.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-psu-L.stl | 0° | 54.2, 125.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-psu-R.stl | 0° | 122.8, 123.5 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-awg-L.stl | 0° | 169.0, 113.5 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | seat-jig-awg-R.stl | 0° | 193.0, 112.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 169.0, 239.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 193.0, 236.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 217.0, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |
| 36 | awg-pad-standin.stl | 0° | 241.0, 12.0 | 4 | wall_loops 2, sparse_infill_density 15%, brim_type no_brim |

Plate names in the project: 01 ABS+ black — sled T-feet ×2, beam halves ×4 (feet standing; outer brim 5); 02 ABS+ black — bottom drawer runner (1 of 2; leg top down, ironing on top); 03 ABS+ black — bottom drawer runner (2 of 2); 04 ABS+ black — column guide strips upper ×2 (rail face down, diagonal); 05 ABS+ black — column guide strips lower right + lower left short, mini-slot runner v3 (diagonal; ironing on the runner's top); 06 ABS black — cradles — PSU left v3 ×2, right rear v4, right front v5, AWG left v2 ×2 (sacrificial layer in the cups); 07 ABS black — sled cross bars front + rear v2 (flat, lips up, diagonal); 08 ABS black — AWG right cradles v2 ×2, cable channel, splices ×2, hinge leaves 2 + 2, magnet bracket, magnet tab; 09 PETG black — bottom drawer quarter Q1; 10 PETG black — bottom drawer quarter Q2; 11 PETG black — bottom drawer quarter Q3; 12 PETG black — bottom drawer quarter Q4; 13 PETG black — column drawer v3 (floor down, diagonal, outer brim 5; ~24 h); 14 PETG black — mini-slot body (diagonal, outer brim 5) + sled front rests ×2 + hinge pins; 15 PETG black — tiles A2 — band2-LF + band1-LF; 16 PETG black — tiles B2 — band2-LR + band1-LR; 17 PETG black — tiles C2 — band3-LF + band3-LR; 18 PETG black — tiles D2 — band3-RF + band1-R; 19 PETG black — tiles E2 — band3-RR + band1-R; 20 PETG black — tile band2-RF + door set fixed rear tile v2; 21 PETG black — tile band2-RR + lighting board enclosure + lid; 22 PETG black — tile band4-LF (legs stand 19); 23 PETG black — tile band4-LR; 24 PETG black — door v3 (face down); 25 PETG black — top panel — four tiles standing (thin-part settings); 26 PETG dark grey + dark blue logo inlay — bottom drawer facia (standing, diagonal, thin-part settings); 27 PETG dark grey + natural window — sill panel (standing, diagonal, brim 5); 28 PETG dark grey — column facia + mini-slot facia (standing, thin-part settings); 29 PETG dark grey — sled front bar v3 (front face down, diagonal, outer brim 5); 30 PETG dark grey — rear box left half (floor down, outer brim 5); 31 PETG dark grey — rear box right half; 32 PETG dark blue — pull inserts bottom, column, mini v2 + sled-bar liner + upright caps ×4 (supports on, build plate only); 33 PETG any colour (hidden parts) — box braces ×2, strip brackets upper v2 + lower v5, sill blocks left v10 + right v4; 34 TPU blue 95A — frame feet ×4, AWG pads 2 + 2, sled stop caps ×2, slot covers ×6 (no brim, no support; dried, external spool); 35 JIG — any colour, any PETG or PLA — rail spacers 48, 63.5, 139.5, 159 ×2 each + the 3.0 web gauge; 36 JIG — any colour, any PETG or PLA — seating jigs PSU L, PSU R, AWG L, AWG R + AWG pad stand-ins ×4.

Hardware the plates need, from HANDOVER §10: 47 M5 × 10 button head (4 into the uprights' bores, no T-nut), 9 M5 × 10 countersunk, 2 M5 × 12, 54 drop-in T-nuts, M5 × 8 for the 8 cast brackets, 4 M3 × 10, 4 Ø10 × 2 magnets, the 8 mm button and its nut, CA glue.
