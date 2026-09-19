# Print rules and design-for-print review (v1, 2026-09-17)

House rules for every printed part in this project, then a review of every production part designed so far against them. The same rules are saved as a Claude skill (`print-oriented-design`) so they apply to every project, not just this one. Coupons (P1–P9, spacers) are exempt from the review; they follow the rules by construction.

## 1. Rules

1. **Every part has a designated bed face before it is modelled**, not after. The bed face is the largest flat face, and it must be at least 30 % of the footprint. The STL is exported in that orientation with z = 0 on the bed. `src/printcheck.py` verifies this on every export and lists every downward face above the bed.
2. **Precision surfaces are vertical walls.** Anything that slides, locates or mates — dovetail flanks, runner grooves, T-foot flanks, bores, clip barbs, cup walls — is printed as a vertical wall so its dimension comes from XY (±0.05 on the X1C), never as a top surface (layer-quantised) or a ceiling (sags). Layer lines run along the sliding direction. One allowance (P3, 2026-09-19): a horizontal *bearing* face whose height only sets play — the runner rib's bottom, the drawer's groove flank — may be a top surface (flat, smooth, ±0.1), never a ceiling; the locating faces beside it (rib tip, groove back) stay vertical walls.
3. **One part, one direction of features.** A part may have features rising from its bed face, never features hanging below it. If a design needs both (a web under a beam, a peg under a bracket), the interface is a joint and the part splits there.
4. **Overhangs are designed out, not supported.** Slots and grooves in vertical walls get 45° roofs. Horizontal round holes are teardrops. Mushroom heads and lips have a 45° underside. Bridges are kept under 12 mm. Counterbores that must face the bed use the slicer's sacrificial layer (Bambu: Quality → Bridge counterbore holes → Sacrificial layer), not support.
5. **Supports are a house rule, not a design tool.** They stay enabled with "On build plate only" so they can never grow inside a part. If the slicer preview shows support on any fit surface, the part is wrong.
6. **Clearances live in one place** (`src/fit.py`), set by coupons, read by every part script. No X-Y compensation in the slicer.
7. **Bed-edge features get a 0.4 mm chamfer** on their bottom edge so elephant foot cannot close a clearance on the first layer.
8. **Split rather than tilt** when a part exceeds the bed. A diagonal placement is fine for a bar; a fit part with sliding surfaces is split with a joint that itself obeys rules 2–4.

## 2. Review of production parts

| Part | Bed face | Precision surfaces | Finding | Ruling |
|---|---|---|---|---|
| Bottom drawer quarters ×4 (D2) | floor, walls up | floor tabs (in-plane), wall dovetail rib/slot (vertical), groove back (vertical) | conforms. **Runner groove** (modelled 2026-09-19, `drawer_runner.groove_cut()`): a house-shaped side pocket in a 10 × 20 boss along each outer wall — flank at the floor top (z 3, bearing), back at 7.3, 45° roof up to the wall face at 17.3. It crosses the left/right wall dovetails (x 3.4–9.4), so those move up to z 20–60 | groove in the drawer, rib on the runner (the 3 mm gap decided it — see the runner row) |
| Column drawer (D5) and mini slot (D7) | floor, walls up, diagonal on the bed | wall faces, neck step | conforms | same runner rule as above |
| Three fronts + sled bar (D3) | **bottom long edge**, standing, diagonal | none on the front itself | a pull slot cut into a standing front leaves its top edge as a 100–120 mm bridge; a 30° pocket floor is a 30° overhang | **D9**: the front carries a notch in its top edge (no bridge); the pull is a separate insert printed face-down (slot, hook strip, pocket with a leaning floor and a 7 mm bridged back wall) and glued in, accent colour. Brim allowed on fronts (no fit flanks). Logo inlay is a vertical-wall feature — fine with AMS |
| Drawer runners ×2 (`src/parts/drawer_runner.py`) | **leg-top down** (an L: leg over the base rail's top face bolted into the top slot, 2.7 plate down the inner face, 7 mm rib z 6–20 whose top slopes 45° back to the plate) | rib tip (locates sideways — vertical wall), rib bottom (bearing — top surface, rule 2 allowance) | the drawer wall is 3 mm off the rail face, so nothing bolted through that gap can hide an M5 head without breaking into the bearing face; the fixing moved to the rail top. Counterbores open onto the bed → sacrificial layer, as the cradles | conforms; P3 coupon is 80 mm of it. Column guide strips ×4 and the mini-slot runner get their own sections (2 mm gap on the inner sub-frame side) once P3 sets `RUNNER_CLR` |
| Housing-top tiles ×6, top tiles ×4, H-spline | flat | none | conforms | — |
| Side tiles (16), door, fixed rear tile (D4) | tile face down (textured outside) | slot clips on the inside face | clips rise from the tile — conforms; **clip barbs** are undercuts | barb underside at 45°; the P4 coupon carries that geometry |
| Door hinge knuckles | — | 3 mm pin bore, horizontal | a round barrel on a face-down tile has its underside as an overhang | knuckles are **separate parts printed standing** (bore vertical, teardrop unnecessary), located on the door by a 2-pin socket and glued; door tile stays flat |
| Magnet bosses, frame-side L-bracket, rear-tile tab | flat / boss face up | 10.4 × 2.2 pockets | pockets open upward — conforms | — |
| PSU cradle ×4, AWG cradle ×4 | **saddle/arm top face down** (re-exported 2026-09-17) | foot cup, saddle channel | cup-up rested on the gusset tip — could not print; top-down leaves the cup and two counterbores as 4 mm ceilings over the plate | Bambu "Bridge counterbore holes: Sacrificial layer" — no support at all; punch out the discs. AWG cradles inherit the orientation |
| Sled T-feet ×2 + web | **standing** on the flange and web bottom edges, layers along the slide | neck flanks (5.8 in the 6.2 mouth), flange faces, web thickness, rib flank | HANDOVER has the web "down from the beam", which would hang a feature below a flat beam — violates rule 3. With the web on the foot, the neck/flange grow toward −x and the rib toward +x, so neither web face can be the bed either | **the web belongs to the foot** (`src/parts/sled_foot.py`): one inverted-T part, 210 long, printed standing — flange and web are vertical walls, the rib flank is 45°, the only downward face is the neck's 4.2 mm bridge between flange and web. Web at x 22.2–24.7 (2.2 off the rail face) so the beam keeps a 1.5 mm wall outside it. Rib on the web's top edge (z 337–341) widens 2.5 → 5.0 inboard at 45°; the beam threads onto it from the front. P1 v2 coupon carries this exact section |
| Sled beams ×2 (split, D6) | **flat, top face up** — cups and stand pockets open upward | closed dovetail groove in the underside (1.5 outer wall, 45° inboard flank, 5.4 mm bridged ceiling), cup walls, pocket walls | v1 had the groove open at the beam's outer face, which left a one-sided 5 mm ceiling; moving the web inboard 1.7 closes it | conforms: every pocket opens up, the groove ceiling is a bridge under 12; split joint at y 165 per P7. Front stands sit in 2.5 mm pockets (14 − 11.5), not on lipped pads |
| Front bar, rear cross bars with guide lips | flat (bar on edge, diagonal) | guide lips, J-pull opening | lips rise from the bar — conforms | — |
| Rear box halves | floor down, open side up | dovetails (vertical), guide-lip engagement | conforms | — |
| Cable channel (separate, D6) | floor down | wedge tabs "45° solid support" | designed to the rule already | — |
| TPU feet, AWG pads, stop caps | flat, spigot up | spigot | conforms | TPU profile at P8 |
| Blue caps | open side down? | — | a cap with a 5 mm spigot into the bore prints spigot-up, closed face down | closed face on the bed |
| Probe hanger | flat | keyholes | through-holes — conforms | — |
| Strip brackets (keyhole pegs) | bracket face down | peg heads (mushroom) | a mushroom head is a 100 % overhang | peg = post + 45° cone under the head (self-supporting), or head printed as a separate disc on an M3 |
| Rear-right cable clips | flat | — | not yet designed | design to rule 4 |

## 3. Changes this review makes to HANDOVER

- §4: the 2.5 web is part of the T-foot, not the beam; beam-to-foot joint is a sliding dovetail along y on the beam underside.
- §5: hinge knuckles are separate standing parts; clip barbs 45°.
- §6: drawer runner is an L bolted into the base rail's top slot with a 7 mm rib; the drawer's outer walls carry a house-shaped groove in a 10 × 20 boss (P3); side-wall dovetails z 20–60.
- §8 print notes: cradles print top face down with a sacrificial layer over the cup; fronts stand on their bottom edge; "no supports" now means "none inside a part".
- §7: strip-bracket pegs get a 45° cone under the head.

These land in HANDOVER v19 at close-out; until then this file is the reference.
