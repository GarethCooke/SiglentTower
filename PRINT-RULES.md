# Print rules and design-for-print review (v1, 2026-09-17)

House rules for every printed part in this project, then a review of every production part designed so far against them. The same rules are saved as a Claude skill (`print-oriented-design`) so they apply to every project, not just this one. Coupons (P1–P9, spacers) are exempt from the review; they follow the rules by construction.

## 1. Rules

1. **Every part has a designated bed face before it is modelled**, not after. The bed face is the largest flat face, and it must be at least 30 % of the footprint. The STL is exported in that orientation with z = 0 on the bed. `src/printcheck.py` verifies this on every export and lists every downward face above the bed.
2. **Precision surfaces are vertical walls.** Anything that slides, locates or mates — dovetail flanks, runner grooves, T-foot flanks, bores, clip barbs, cup walls — is printed as a vertical wall so its dimension comes from XY (±0.05 on the X1C), never as a top surface (layer-quantised) or a ceiling (sags). Layer lines run along the sliding direction.
3. **One part, one direction of features.** A part may have features rising from its bed face, never features hanging below it. If a design needs both (a web under a beam, a peg under a bracket), the interface is a joint and the part splits there.
4. **Overhangs are designed out, not supported.** Slots and grooves in vertical walls get 45° roofs. Horizontal round holes are teardrops. Mushroom heads and lips have a 45° underside. Bridges are kept under 12 mm. Counterbores that must face the bed use the slicer's sacrificial layer (Bambu: Quality → Bridge counterbore holes → Sacrificial layer), not support.
5. **Supports are a house rule, not a design tool.** They stay enabled with "On build plate only" so they can never grow inside a part. If the slicer preview shows support on any fit surface, the part is wrong.
6. **Clearances live in one place** (`src/fit.py`), set by coupons, read by every part script. No X-Y compensation in the slicer.
7. **Bed-edge features get a 0.4 mm chamfer** on their bottom edge so elephant foot cannot close a clearance on the first layer.
8. **Split rather than tilt** when a part exceeds the bed. A diagonal placement is fine for a bar; a fit part with sliding surfaces is split with a joint that itself obeys rules 2–4.

## 2. Review of production parts

| Part | Bed face | Precision surfaces | Finding | Ruling |
|---|---|---|---|---|
| Bottom drawer quarters ×4 (D2) | floor, walls up | floor tabs (in-plane), wall dovetail rib/slot (vertical) | conforms. **Runner grooves** on the outer side walls are still to be modelled: a horizontal groove in a vertical wall has a ceiling | groove roof at 45° (house-shaped section), or run the groove as a rib on the drawer and the groove in the runner (rib is an upward feature — preferred) |
| Column drawer (D5) and mini slot (D7) | floor, walls up, diagonal on the bed | wall faces, neck step | conforms | same runner rule as above |
| Three fronts + sled bar (D3) | **bottom long edge**, standing, diagonal | J-pull pocket | standing on the bottom edge the pocket roof is a 12 mm bridge and the 30° floor faces up; standing on the top edge the floor becomes a 30° ceiling and fails | bottom edge down, always; P6 prints that way. Logo inlay is a vertical-wall feature — fine with AMS |
| Drawer runners, column guide strips | flat, diagonal | sliding face | if the drawer carries a groove, the runner is a plain bar — conforms; if the drawer carries a rib, the runner carries the groove with a 45° roof | decided with the drawer above |
| Housing-top tiles ×6, top tiles ×4, H-spline | flat | none | conforms | — |
| Side tiles (16), door, fixed rear tile (D4) | tile face down (textured outside) | slot clips on the inside face | clips rise from the tile — conforms; **clip barbs** are undercuts | barb underside at 45°; the P4 coupon carries that geometry |
| Door hinge knuckles | — | 3 mm pin bore, horizontal | a round barrel on a face-down tile has its underside as an overhang | knuckles are **separate parts printed standing** (bore vertical, teardrop unnecessary), located on the door by a 2-pin socket and glued; door tile stays flat |
| Magnet bosses, frame-side L-bracket, rear-tile tab | flat / boss face up | 10.4 × 2.2 pockets | pockets open upward — conforms | — |
| PSU cradle ×4, AWG cradle ×4 | **saddle/arm top face down** (re-exported 2026-09-17) | foot cup, saddle channel | cup-up rested on the gusset tip — could not print; top-down leaves the cup and two counterbores as 4 mm ceilings over the plate | Bambu "Bridge counterbore holes: Sacrificial layer" — no support at all; punch out the discs. AWG cradles inherit the orientation |
| Sled T-feet ×2 + web | **standing** on the flange and web bottom edges, layers along the slide | neck flanks (5.8 in the 6.2 mouth), flange faces, web thickness, rib flank | HANDOVER has the web "down from the beam", which would hang a feature below a flat beam — violates rule 3. With the web on the foot, the neck/flange grow toward −x and the rib toward +x, so neither web face can be the bed either | **the web belongs to the foot** (`src/parts/sled_foot.py`): one inverted-T part, 210 long, printed standing — flange and web are vertical walls, the rib flank is 45°, the only downward face is the neck's 2.5 mm bridge between flange and web. Rib on the web's top edge (z 337–341) widens 2.5 → 5.0 toward +x at 45°; the beam threads onto it from the front and cannot lift (the flank pushes the web toward the upright, 0.5 away). P1 coupon carries this exact section |
| Sled beams ×2 (split, D6) | **top face down** (cups and pads to the plate, sacrificial layer as the cradles) | rib rebate on the outer bottom edge, cup walls, pads | flat-with-cups-up leaves the rebate as a 5 mm one-sided ceiling over the bed (not a bridge — open at the outer face) | top face down the rebate opens upward with a 45° undercut; cups/pads print as ceilings with the sacrificial layer; split joint at y 165 per P7 |
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
- §6: drawer runner interface is rib-on-drawer / groove-in-runner (45° roof) unless P3 says otherwise.
- §8 print notes: cradles print top face down with a sacrificial layer over the cup; fronts stand on their bottom edge; "no supports" now means "none inside a part".
- §7: strip-bracket pegs get a 45° cone under the head.

These land in HANDOVER v19 at close-out; until then this file is the reference.
