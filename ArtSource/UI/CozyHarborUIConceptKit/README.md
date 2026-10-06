# Cozy Harbor UI concept kit

This ZIP contains one visual contact sheet and 12 individually generated, transparent PNG components for the Catch Journal, inventory, shop, and catch toast visual direction. These are **art-source concepts**, not imported Unreal assets or a finished UMG layout. No existing game widgets were changed.

| File | Intended use |
| --- | --- |
| `contact_sheet.png` | Labeled overview only; not an importable sprite atlas. |
| `frame_dock_wood.png` | Hollow outer frame for a large menu. |
| `panel_parchment.png` | Content-panel background. |
| `plaque_title.png` | Header behind a dynamic menu title. |
| `button_primary_teal.png` | Prominent action button background. |
| `button_secondary_parchment.png` | Quieter action button background. |
| `tab_selected_teal.png` | Active tab background. |
| `tab_unselected_parchment.png` | Inactive tab background. |
| `slot_empty.png` | Empty item/journal slot background. |
| `slot_selected.png` | Selected item/journal slot background. |
| `toast_background.png` | Catch-notification card background. |
| `corner_wood_rope.png` | Optional decorative upper-left corner accent. |
| `divider_wood_rope.png` | Optional horizontal section divider. |

All labels, icons, counts, and fish artwork should be separate UMG elements so dynamic text can wrap and gameplay data can change without editing these images. The contact sheet includes minor style differences from the individual generations; use the individual PNGs as the actual source artwork. Before production use, inspect appearance at the intended screen size and configure each image's UMG Draw As / 9-slice margins where appropriate. In particular, do not simply stretch the buttons, slots, or ornate frame across arbitrary aspect ratios. The frame is hollow and should layer over the parchment panel.

Created 2026-09-30 with built-in image generation. Prompt family: simplified low-poly dockwood, warm matte parchment, restrained cream rope and dark metal, marine-teal selection accents, front-facing blank UI components with true transparent exteriors. No Unreal import, Blueprint compile, or in-game validation was performed.
