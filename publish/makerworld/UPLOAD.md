# MakerWorld upload — what goes where

Everything the listing needs is in this folder and in `publish/SiglentTower-complete.3mf`. `MAKERWORLD.md` holds the text.

## Before uploading

1. Slice every plate of `publish/SiglentTower-complete.3mf` in Bambu Studio (Slice all plates) with your real filaments against the five slots — MakerWorld only accepts a print profile whose plates are sliced. Slot 1 black ABS+, 2 dark blue PETG, 3 black ABS, 4 the PETG the plate name says, 5 TPU 95A.
2. Upload from Bambu Studio (File → Upload to MakerWorld) so the project and the sliced profile go together, or from the website with the .3mf as the model file.

## The form

| Box | Use |
|---|---|
| Title | `MAKERWORLD.md` → Title |
| Summary | → Summary |
| Description | → Description, the whole section |
| Model files | `publish/SiglentTower-complete.3mf` (every mesh is in it; add the `parts/` STLs as well if you want them downloadable one by one — `publish/makerworld/make-stl-zip.cmd` builds the zip) |
| Print profile | the sliced project from step 1, profile name `SiglentTower fit 0.20` |
| Cover image | `photos/tower-front.jpg` |
| Gallery, in this order | `photos/tower-lit.jpg`, `photos/sled-out.jpg`, `photos/box-out.jpg`, `photos/drawers.jpg`, `photos/board.jpg`, `diagrams/layout-as-built.png`, `diagrams/drawer-quarters-plan.png`, `diagrams/door-plan.png`, `diagrams/skin-sheet.png`, `diagrams/wiring-4-connections.png`, `diagrams/plates-sheet.png` |
| Licence | CC BY 4.0 (matches `LICENSE-DESIGN.md`) |
| Category / tags | → Category, Tags |
| "Instruments / hardware required" | → Hardware |
| Print settings notes | → Print notes |

## Captions for the gallery

- tower-front — The finished tower: scope on its sled at the top, AWG and PSU below, three drawers, the logo on the bottom drawer.
- tower-lit — The backlight on: light through the hex tiles and at the sill button.
- sled-out — The scope pulled forward 92 mm on its sled.
- box-out — The storage box out sideways through the door, with the sled forward.
- drawers — Bottom drawer, column drawer and mini slot open.
- board — The lighting board: XIAO ESP32-S3 Plus, level shifter, locking plugs.
- layout-as-built — Front and side elevations, plan, levels and cut list, as built.
- drawer-quarters-plan — The 315 × 300 bottom drawer as four dovetailed quarters.
- door-plan — The fold-down door: hinge, magnets, fixed rear tile.
- skin-sheet — Where every side tile goes and where each clip finger lands.
- wiring-4-connections — Every lighting connection and the pin map.
- plates-sheet — The 36 plates from above.
