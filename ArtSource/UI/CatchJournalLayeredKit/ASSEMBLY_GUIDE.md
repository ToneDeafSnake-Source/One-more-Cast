# Catch Journal layered UMG kit

Prepared October 1, 2026. Art-source deliverable, not imported textures or completed widgets. Generated with the built-in image tool using Seth's supplied screen as the visual reference. This is a recreation in that style, not an exact extraction of the original pixels. Fish/species icons and a font are not supplied.

## Start here

1. Look at `Previews/assembled_layout.png` and `Previews/contact_sheet.png` before importing anything. The assembled preview checks layout and layering; sample text is illustrative.
2. Import ONLY `Textures/` into `/Game/Core/UI_Components/Menus/CatchJournal/Art`. Do not import the reference, previews or generation originals.
3. Open each texture. Use Compression Settings **UserInterface2D (RGBA)**, Texture Group **UI**, sRGB enabled and, where available, Mip Gen Settings **NoMipmaps**. Keep alpha. Use linear/default filtering, not pixel-art nearest filtering.
4. Create `WBP_CatchJournal`, `WBP_JournalCategoryButton` and `WBP_JournalEntryButton` as Widget Blueprints. These are proposed names, not claims of existing assets.
5. Build the static layout first. Check it in Designer at a 1920x1080 screen size, then wire the data. No Editor launch/control, import, Blueprint compile or PIE was performed to produce this ZIP.

## Size and root structure

The layout uses a **1440x860 design canvas** centered in the screen. All coordinates in `layout.json` refer to that canvas, not screen coordinates.

```text
Canvas_Root [screen size]
  SizeBox_Journal [Width Override 1440; Height Override 860]
    Canvas_Journal [local 1440x860 layout]
      Img_BackParchment
      Img_LeftParchment
      Img_MiddleParchment
      Img_RightParchment
      Scroll_Categories [contains VerticalBox_Categories]
      Panel_Entries [heading, optional sort control, ScrollBox containing WrapBox_Entries]
      Panel_Details [name/type, catch image, optional description, stats]
      Img_Frame
      Img_TitlePlaque
      Img_TitleFish
      Txt_Title [Catch Journal]
      Img_RopeCorner_TL / TR / BL / BR
      Img_RopeTitle_L / R
      Btn_Close [with Img_CloseGlyph]
```

On the Size Box's root Canvas slot use center anchors, position (0,0), alignment (0.5,0.5), and Auto Size/Size to Content. For narrower screens, place a Scale Box outside the Size Box using Scale To Fit; verify your project's DPI scaling instead of applying a second arbitrary scale. Do not force this design to fill the screen. The game world remains visible around it.

Keep the window's decorative parent clipping at Inherit; Clip to Bounds on the title's parent would cut off its raised top. Clip the entries Scroll Box and category Scroll Box to their own bounds instead.

## Draw order: fixing the rope corners

The frame contains wood and iron fittings, **no baked rope**. The rope images contain rope, **no baked wood**. That is what makes the overlap controllable.

Use increasing Canvas slot ZOrder:

| ZOrder | What appears here |
|---|---|
| 0 | Broad backing parchment |
| 1 | Three individual parchment panels |
| 10 | Category buttons, entry buttons, selected-catch details |
| 20 | Hollow wooden frame and its corner fittings |
| 30 | Title plaque |
| 31 | Live title text and generic fish title emblem |
| 40 | Four corner ropes and two title lashings |
| 50 | Close button and its separate X glyph |

The ropes therefore render OVER the wood/metal blocks at both top corners. Supplied left/right rope PNGs are already mirrored: use their filenames directly without a negative UMG scale. The close button is inset on the top rail, away from the corner rope.

Set decorative Images to **Not Hit-Testable (Self & All Children)**. Set containers that hold buttons to **Not Hit-Testable (Self Only)** if needed; do not disable their children. Buttons remain Visible and clickable. A frame with a transparent center can still block clicks when its Image is hit-testable.

`layout.json` lists exact starting rectangles and ZOrder. Use fixed Image draw mode for the frame, plaque, ropes and icons. Resize the whole window together rather than stretching each decorative part independently.

## Left: reusable category buttons

Create one `WBP_JournalCategoryButton`:

```text
SizeBox [220x92]
  Button_Category
    HorizontalBox
      ScaleBox > Image_CategoryIcon [52x52 allocation]
      VerticalBox
        Text_CategoryName
        Text_DiscoveredTotal
```

Use `category_normal.png` for the Button's Normal/Hovered/Pressed style brushes to start. Draw As **Box**, margins initially (0.08,0.15,0.08,0.15). Adjust once at the intended on-screen size. For Hovered lighten its tint slightly; for Pressed darken it slightly. White is the default brush tint. Keep Normal Padding and Pressed Padding equal so text does not jump.

Selected is persistent data, separate from hover. Store `bSelected` (Boolean) and use `category_selected.png` for all three style brushes when true. Change text tint to ivory for the teal state. Incomplete counts are white per the accepted requirement; completed counts turn green only if Total > 0 and Discovered == Total. For white text on pale normal backgrounds, use a dark outline/shadow or a dark small count chip for legibility; test that appearance before finalizing.

For the reference's projecting teal tip, add `category_pointer.png` as a separate non-hit-testable Image overlapping the selected button's right edge. Show it only on the selected row. Keep its Canvas parent unclipped. The title emblem can reuse `icon_all_piers.png` with a dark brown UMG tint; its default ivory version is for teal buttons.

Inputs: `CategoryID` (Name), `CategoryName` (Text), `CategoryIcon` (Texture2D object reference), `DiscoveredCount` (Integer), `TotalCount` (Integer). Add an Event Dispatcher `OnCategorySelected` with `CategoryID` (Name). Button OnClicked calls that dispatcher. The parent handles selection and grid refresh.

The five supplied navigation icons are a generic All Piers fish emblem, three pier designs, and Treasure. Reuse a pier icon for future categories if appropriate; category icons are independent of species icons.

Generate category rows from `DT_JournalCategories`; use its current **SortOtder** field, not a silently corrected field name. Treasure stays first. Include the existing `Non_Exclusive` category in a scrollable list when it has content. An All Piers button is a virtual filter across fish definitions, not a new saved category: deduplicate by table row ID and exclude Treasure. Do not write artificial All Piers membership to the catalog.

## Middle: selected category contents

`Panel_Entries` has a live heading such as `Pier 1 (3 / 6)` and a Scroll Box with a Wrap Box. Start at four columns, each entry **136x142**, with an 8-unit gap. The Scroll Box handles additional rows. A Wrap Box does not enforce four columns by itself; constrain available width to 568 units and verify padding at that width.

Create `WBP_JournalEntryButton`:

```text
SizeBox [136x142]
  Button_Entry
    VerticalBox
      ScaleBox > Image_Catch [96-unit high image area]
      Text_CatchName
```

Use `entry_normal.png` and `entry_selected.png` for the persistent unselected/selected brush states. Start Draw As Box with margins (0.10,0.10,0.10,0.10). Keep the input hit rectangle rectangular and reasonably generous. Add `CatchID` (Name) and dispatcher `OnCatchSelected(CatchID: Name)`.

Read rows from `DT_CatchDefinitions`, filter on the selected category, then order by the existing definition sort field. Use the actual `ST_CatchDefinition` field names/types in the Editor. The DataTable row name is the current stable FishID. For All Piers, filter to fish and deduplicate row IDs. Include undiscovered definitions, not just records from the player's map.

Find each row ID in `BP_Fisherman.CatchJournalRecords`. A missing record means undiscovered. Show the existing catch icon if discovered; otherwise use its alpha silhouette and `???`. Do not use a dark tint alone if the source image retains visible interior details: a small UI-domain material should output one solid silhouette color and use the texture's alpha for opacity. If the icons have opaque backgrounds, those species icons need alpha cleanup first. No placeholder silhouettes are included because silhouettes must match your actual fish icons.

Selecting a category rebuilds the middle list, sets persistent category selection, and clears or selects the first entry deliberately. Do not leave the previous category's details visible as if they belong to the new one. Selecting an entry updates the right panel and its persistent grid selection. None of these display operations changes journal records.

The sort field background and dropdown arrow are included because they appear in the reference. Sorting behavior is a later wiring step: omit the control until implemented rather than showing a nonfunctional dropdown. Default to authored catalog order. Name sorting for undiscovered entries must not expose hidden names.

Use the Scroll Box's built-in scrollbar when needed; no scrollbar is visible in the reference. Native hover/pressed states can use brush tint changes on the included base textures. No separate font, baked text, species silhouette or star textures are part of this kit.

## Right: one shared details view

Use the existing icon in a Scale Box with Scale To Fit. Put `detail_wash.png` behind it. Keep the name, type and all values as **UMG Text Blocks**.

Fish rows:
- Type: Fish
- Total Caught: record `TotalCollected`
- Best Weight: record `BestWeight`, followed by **lbs**
- Best Quality: the displayed enum word, such as **Legendary**, **Common**, **Rare**, **Decent**, **Sickly** or **Valuable**

Treasure rows:
- Type: Treasure
- Total Found: record `TotalCollected`
- Collapse both fish-only rows (weight and quality), rather than hiding their text while leaving blank gaps.

For undiscovered fish show `???`, silhouette, Type Fish, Total Caught 0, Best Weight N/A, Best Quality N/A. For undiscovered treasure show `???`, silhouette, Type Treasure and Total Found 0. Get quality display text from the actual `E_FishQuality` value; do not show enum numeric order or introduce Uncommon. No stars are supplied or used.

Descriptions in the reference are example art. A description is not proven to exist in the current catalog schema; keep that area collapsed unless you decide to author descriptions. Do not add a saved field for a visual detail. The remaining space can give the icon more room.

Use `divider.png` between visible stats rows. It is decorative and non-hit-testable. Use right-aligned values, a legible dark brown body font and deep teal values. The handwritten font in the concept is not included; pick a licensed font you already own or use a readable engine font while wiring the UI.

## Image use and nine-slice

| Image | Draw As / suggested starting margin |
|---|---|
| Frame, title plaque, ropes, icons, wash | Image; no margin; preserve intended aspect |
| Parchment panels | Box; 0.08 on all sides |
| Category normal / selected | Box; L/R 0.08, T/B 0.15 |
| Entry normal / selected | Box; 0.10 on all sides |
| Sort background | Box; L/R 0.05, T/B 0.18 |
| Close background | Image at 64x64 |
| Divider | Image; wide narrow slot |

These margins are starting values, not verified Unreal settings. AI-generated ornament is not guaranteed to produce perfect procedural nine-slice edges. Keep to the supplied preview sizes initially. If a corner stretches, adjust its margin at the final widget size. If you want an exact hand-polished shape, Photoshop is useful for edge cleanup and nine-slice guides; it is not a prerequisite to try the supplied kit.

## What still needs manual work

Import textures, create widgets, assign brushes/fonts, wire button dispatchers, catalog filtering, player reference, record lookup and existing menu/input behavior. No new save fields are needed. No reward or toast behavior is introduced by this art kit. Preserve the current inventory/catch/save systems.

Verify mouse click-through after ropes are placed; category contents and counts; unknown silhouettes; fish/treasure detail differences; word quality labels; scrolling; close/input restoration; 1080p and a smaller screen; and journal save/load. Never call these checks passed from the art preview alone.

Epic reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-styling-in-unreal-engine — brush states and Box margins. This guide applies those concepts to the supplied artwork.
