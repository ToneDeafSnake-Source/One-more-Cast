# Catch Journal layered art kit

Start with **Previews/assembled_layout.png**, then **ASSEMBLY_GUIDE.md**.

- **Textures/**: 23 transparent PNGs to import into Unreal. Includes the frame, parchment, title plaque, normal/selected category and entry backgrounds, selection pointer, pier/Treasure/All Piers icons, close parts, sort parts, divider, illustration wash, and separate left/right rope overlays.
- **Originals/**: unscaled generation source images, kept for optional Photoshop polishing.
- **Previews/**: assembled layout and labeled contact sheet. Example text and counts are preview annotations; no fish icons are supplied.
- **layout.json**: 1440x860 design-canvas rectangles and draw order.
- **PROMPTS.json**: built-in image-generation prompts, including two corrected standalone symbols.
- **validation.json**: dimensions/alpha inspection record. Unreal import, compile and PIE have not been run.

This recreates the reference style rather than extracting exact source layers. Text, fish artwork, counts and quality words belong in live UMG widgets. No font, fish silhouettes, star art, gameplay Blueprint changes or save changes are included. Photoshop is optional; manual Unreal import and widget wiring are required.

For corner overlap: parchment → buttons/details → wood frame and plaque → rope overlays → inset close button. Decorative images must not intercept clicks.
