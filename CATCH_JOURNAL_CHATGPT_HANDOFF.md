# Catch Journal — implementation handoff for Seth and ChatGPT

Date: 2026-09-28. Project: One More Cast, Blueprint-only UE 5.7.4.

## Read this first: where Codex stopped

This is an audited implementation plan, **not a completed journal UI**. Codex inspected the saved project using Unreal's headless Python runtime and native object exports, including graph pin connections. No journal `.uasset` or `.umap` was created or modified. No gameplay C++, plugins, Git operations, mouse control, or save-schema changes were made. The animation pilot is paused and unchanged.

Created: inspection/report scripts in `Scripts/Editor/CatchJournal`, reports in `Saved/CodexCatchJournal`, this handoff, and updated project memory. No journal compile, PIE, actual save/load, or packaged-build check has passed because none was run.

The available Python interface can inspect assets, export graph information, and create some Blueprint shells/variables. It does not expose the Widget Tree authoring and general node/pin wiring needed to build this connected UMG feature. `WidgetTree` and `WidgetBlueprintEditorSubsystem` were absent; `widget_tree` was unavailable and CDO WidgetTree access protected. Codex deliberately did not leave empty widgets for Seth to finish or patch binary assets. Native `.t3d` exports below are inspection evidence, not a supported whole-Blueprint edit/reimport workflow.

**Instructions to ChatGPT:** read `ONE_MORE_CAST_CONTEXT.md` as well. Help Seth build the remaining feature in small stages, explicitly naming nodes, pin types, inputs, outputs, and prerequisites. Ask for screenshots when wiring is uncertain. Do not say the proposed variables/functions below already exist. Start with the category/catalog decision, then get one category and one entry working before expanding. Expect several working sessions, not a few clicks. Ask before Editor control. Do not rewrite shop, inventory, saves, fishing, or animation systems.

## Verified existing foundation

| Asset | Existing contract |
|---|---|
| `/Game/Core/PlayerBlueprints/BP_Fisherman` | `CatchJournalRecords`, `UpdateCatchJournal`, `GetFishQualityRank`, menu helpers |
| `/Game/Core/SaveGame/BP_SaveGame` | `SavedCatchJournalRecords` |
| `/Game/Core/Data/Structs/CollectionLog/ST_CatchJournalRecord` | `Discovered` Boolean, `TotalCollected` Integer, `BestWeight` double, `BestQuality` E_FishQuality |
| `/Game/Core/Data/Structs/ST_FishCatchEntry` | FishID, FishDisplayName, FishIcon, fish/junk/treasure flags, JournalCategoryID, JournalSortOrder, and existing catch data |
| `/Game/Core/Interactables/FishingSpot/BP_FishingSpot` | `FishCatchTable` array of ST_FishCatchEntry, populated on placed actors |
| `/Game/Core/Data/DataTables/CollectionLog/DT_JournalCategories` | Uses ST_JournalCategoryData; one row presently: Pier_01 |
| `/Game/Core/UI_Components/Inventory/WBP_Inventory` | Existing FishermanRef and shared close behavior |

The category struct lives beside ST_CatchJournalRecord. Its fields are CategoryID, DisplayName, Description, Icon, **SortOtder**. Preserve that actual spelling; do not silently rename it.

Native graph connections show:

- `FillSaveObjectFromCurrentState`: player CatchJournalRecords feeds SavedCatchJournalRecords on the save object, with execution connected.
- `ApplyCoreSaveData`: saved SavedCatchJournalRecords feeds player CatchJournalRecords, with execution connected.
- `UpdateCatchJournal` accepts ST_ItemData, uses FishID as the map key, checks fish/treasure eligibility and nonempty ID, and has new/existing record paths. Existing record logic increments count, compares weight and uses GetFishQualityRank for quality.
- Quality ranks in the existing helper: Valuable=5, Legendary=4, Rare=3, Common=2, Decent=1, Sickly=0. Enum serialization order is different. Reuse the helper; display enum labels, not integer ordinals.
- `AddCaughtFishToInventory` calls inventory AddItem, then directly calls UpdateCatchJournal from AddItem's normal execution output. **Acceptance gating remains a risk to inspect:** this alone does not prove the item was accepted. Inspect AddItem's result and upstream capacity checks before changing anything; test full inventory. Do not double-update the journal in the UI.

Save assignments are verified graph wiring, **not a successful persistence test**. Reuse the saved map. No new save fields are needed for this UI.

## Data audit and the decision needed first

The saved `/Game/MainDock` contains 37 exact BP_FishingSpot-class instances. Their definitions yield 17 unique journal-eligible IDs: 16 fish and EmeraldRing (treasure). This audit excludes junk and did not inspect other maps, subclasses, or unsaved live Editor edits.

IDs: Agar, Angloria, CateFish, Catfish, ChloroFish, CowFish, DuctFish, EmeraldRing, Grasper, Izatagar, JuneBeetle, PinkyPoo, ScaleFish, SeaBear, SmoothEmberscale, Triangel, YellowfinTuna.

Every ID has at least one definition with a blank JournalCategoryID. Catfish has conflicting metadata: Pier_01/sort 10 in some definitions, blank/sort 0 in others. The only current category row is Pier_01, display name `Pier 1`, description `The first fishing area`, no icon, SortOtder=10. Counts cannot be trusted until these omissions/conflicts are resolved.

Review `Saved/CodexCatchJournal/catalog_review.csv` and `catalog_audit.json`. SourceSpots in the CSV is the set for the whole ID, not precise provenance for each differing variant; `definitions.json` preserves exact per-spot rows. This CSV is a review report, **not an import-ready DataTable**.

**Recommendation, not yet accepted:** for this single-map milestone, keep the existing spot arrays authoritative and build a transient, deduplicated display cache once when opening the journal. Do not maintain a second hand-edited fish catalog. This minimizes changes but relies on all relevant spots being loaded; streaming/multiple maps would need a complete shared catalog or generated catalog later. Do not scan every Tick.

Ask Seth to approve:

1. Categories and membership, particularly ScaleFish (present across all piers) and treasure. Icon folder names are clues, not an approved category rule.
2. Whether each species has exactly one journal category. That matches the existing single JournalCategoryID field. If multiple category membership is desired, discuss a separate membership design before implementing.
3. The transient-cache approach above versus a deliberately shared authoritative catalog. Do not migrate fishing definitions automatically.

Then edit only the journal metadata on applicable existing catch definitions and add approved rows to DT_JournalCategories. Keep catch odds, nested QualityTable, IDs, icons, and full item payload intact. Make repeated definitions consistent. Never use actor enumeration order as a conflict-resolution rule.

## Proposed UI assets — none created yet

Suggested folder: `/Game/Core/UI_Components/Menus/CatchJournal`.

- WBP_CatchJournal: one parent, three views.
- WBP_JournalCategoryButton: reusable category entry.
- WBP_JournalEntrySlot: reusable catch entry.

Suggested parent hierarchy (names proposed):

```text
Root / centered panel
  Background
  VerticalBox
    Header: title, overall count, Close button
    WidgetSwitcher_Journal
      [0] Categories: ScrollBox -> VerticalBox_Categories
      [1] Entries: category heading -> ScrollBox -> UniformGridPanel_Entries
      [2] Detail: image, name, type, fish-only quality/weight group, count
    Back button
```

Existing style references, inspected as metadata rather than rendered UI:
`/Game/Core/Images/TackleShopMenu/TackleShopBackground`,
`/Game/Core/Images/UI_Icons/CatchToastCard`, and
`/Engine/EngineFonts/hvd_edding_Font` (inventory text uses size 20, outline 1).
Reuse appropriate art/style rather than duplicating entire shop graphs.

## Stage 1 — prerequisites and display cache

Proposed parent variables:

| Variable | Type / purpose |
|---|---|
| FishermanRef | BP_Fisherman object reference; supply during initialization |
| DefinitionsByID | Map: Name -> ST_FishCatchEntry; transient display cache |
| SortedCategories | Array ST_JournalCategoryData |
| SelectedCategoryID | Name |
| SelectedFishID | Name |
| CurrentPage | Integer, 0/1/2 |
| Columns | Integer, initially 5; must be greater than zero |

Proposed `InitializeJournal` function input: InFisherman (BP_Fisherman object reference). Validate it, assign FishermanRef, build the definition cache, refresh category list, select switcher index 0. Call explicitly after Create Widget, not through a Tick binding. Design-time PreConstruct must not query gameplay state.

Proposed `BuildDefinitionCache`:

1. Clear DefinitionsByID. Use `Get All Actors Of Class` BP_FishingSpot once, `For Each Loop`, read each FishCatchTable, then a nested For Each Loop.
2. Break ST_FishCatchEntry. Include `(bIsFishCatch OR bIsTreasureCatch) AND NOT bIsJunkCatch`. Reject empty FishID.
3. Validate JournalCategoryID against authored category IDs. Log/report blanks and conflicts rather than silently assigning a category or accepting whichever actor arrives first.
4. `Find` in DefinitionsByID using FishID (Name). If absent, `Add` the full entry. If present, compare journal-relevant fields. Catch odds can differ between spots; that is not itself a journal conflict. Name/icon/type/category/sort must be consistent for the chosen single-category design.
5. Continue from each loop's Completed pin; do not Return inside the first loop iteration.

Use `Get Data Table Row Names` for DT_JournalCategories, then `Get Data Table Row` with ST_JournalCategoryData output. Validate row CategoryID uniqueness and agreement with entry membership. Sort categories by SortOtder, entries by JournalSortOrder, with an explicit stable secondary key for ties. Blueprint does not automatically provide a generic struct sort: teach a small insertion-sort helper (find first larger sort value, Array Insert, otherwise Add) or author unique sort numbers. Do not promise a nonexistent generic Sort Struct Array node.

## Stage 2 — category child and counts

WBP_JournalCategoryButton contains Button, optional Image, display-name TextBlock and progress TextBlock.
Proposed dispatcher `OnCategorySelected(CategoryID: Name)`; store the ID on the child.
Proposed `SetupCategory(Data: ST_JournalCategoryData, DiscoveredCount: Integer, TotalCount: Integer)` sets its text/icon and ID. Button OnClicked calls the dispatcher.

Parent `RefreshCategories` clears old children before rebuilding. For each sorted category, iterate unique DefinitionsByID values matching its ID. Increment total for each unique eligible definition, regardless of discovery. `Find` FishermanRef.CatchJournalRecords with FishID; discovered is **Found AND record.Discovered**. Increment discovered only when true.

Create each child with the owning player, bind its dispatcher to the parent's `ShowCategory(CategoryID: Name)`, call SetupCategory, and Add Child to VerticalBox. Count color is white unless `TotalCount > 0 AND DiscoveredCount == TotalCount`, then green. No rewards or save writes on refresh. Overall progress counts all unique eligible definitions, not saved map length or summed duplicate memberships.

## Stage 3 — entry grid

Parent `ShowCategory` stores SelectedCategoryID, clears old grid children, filters cache values by category, sorts them and creates WBP_JournalEntrySlot instances. Add Child to Uniform Grid: Row = integer Index / Columns; Column = Index % Columns. Switch to page 1.

Child has Button and Image, optionally name text. Proposed `SetupEntry(Definition: ST_FishCatchEntry, bDiscovered: Boolean)` stores FishID, uses `Set Brush From Texture` with FishIcon, then `Set Color and Opacity` white `(1,1,1,1)` if discovered, black `(0,0,0,1)` otherwise. Preserve the texture alpha; do not set alpha to zero. No new silhouette assets.

Undiscovered name/tooltip/accessibility text must be `???`, not a leaked display name. Dispatcher `OnEntrySelected(FishID: Name)` calls parent ShowEntry. Bind once per newly created child. Undiscovered entries remain clickable if the detail view is meant to show their silhouette.

## Stage 4 — one reusable detail view

Proposed `ShowEntry(FishID: Name)` uses DefinitionsByID.Find; handle missing definition safely. Separately Find CatchJournalRecords; never assume the record exists. Store SelectedFishID and switch to page 2.

- Undiscovered: name `???`, black silhouette, hide record values. Do not display default enum quality as if it were earned.
- Discovered fish: full-color icon, FishDisplayName (not quality-prefixed ItemName), highest quality from BestQuality, best weight using the game's existing unit convention, `Total Caught` from TotalCollected.
- Discovered treasure: name, type `Treasure`, `Total Collected`; **Collapsed** quality/weight group. No fabricated treasure weight/quality.
- Explicitly reset visibility, tint and text every time so switching fish -> treasure -> undiscovered cannot leave stale content.

UI reads records only. Do not call UpdateCatchJournal to populate screens. Back moves detail -> selected category grid -> categories. Close exits; decide with Seth whether Tab closes from every page and Escape acts Back before Close. Keep keyboard events Handled only when used.

## Stage 5 — integrate inventory and existing menu ownership

Existing WBP_Inventory has FishermanRef. Its Tab handler and close button use BP_Fisherman's `CloseMenuAndReturnToGame`. Player also has `CurrentOpenMenuWidget`, `CloseCurrentOpenMenu`, InventoryWidget, ShopMenuWidget and PauseMenuWidget.

Inspect the current inventory opening graph for focus, pause, cursor and movement policy before duplicating that policy. Proposed player entry point `OpenCatchJournal` is **new**, not an existing function:

1. Validate that opening a menu is allowed using the same restrictions as inventory.
2. Close/remove the current inventory through the shared menu replacement path (`CloseCurrentOpenMenu`), not the return-to-game helper halfway through opening a new menu.
3. `Create Widget` WBP_CatchJournal with the actual owning PlayerController; pass player reference via InitializeJournal.
4. Assign the new instance to CurrentOpenMenuWidget; Add to Viewport; match existing input mode/pause/cursor policy and explicitly focus the journal. Set the widget Is Focusable when needed for OnKeyDown.
5. Add one Catch Journal button to WBP_Inventory that calls OpenCatchJournal on FishermanRef.
6. Journal Close calls existing CloseMenuAndReturnToGame. Do not invent a second independent close/input system. A dedicated cached JournalWidget reference is unnecessary unless the existing architecture needs it; avoid leaving stale references if one is introduced.

Verify repeated inventory -> journal -> close cycles, mouse clicks, keyboard navigation and normal movement afterwards. Do not modify project input mappings for this feature.

## Stage 6 — backend risk checks and acceptance testing

Before calling the feature complete, inspect AddItem and the callers of AddCaughtFishToInventory. If AddItem can fail, ensure journal updates occur exactly once only after successful insertion, using the actual result contract. Do not guess a success-pin name or alter the failure policy without showing Seth the existing graph.

Test with controlled development data, without overwriting a wanted save:

- Fresh journal includes undiscovered definitions, correct category totals, zero-entry category not green.
- First fish: new discovery, one record/count, correct weight/quality.
- Repeated fish at different qualities: same FishID, count increments, best values never regress.
- Treasure: tracked count and treasure-only detail; junk and empty IDs excluded.
- Failed D20/full inventory: no count increase; successful normal/D20 catches update once.
- Selling/moving/opening/closing UI: no count change, discovery retained.
- Save -> restart/reopen -> load: records and the rest of inventory, Scales, rod, bait and cooler restore. No extra save field or SaveVersion change is planned.
- Add an approved definition/category: UI updates without a new widget class or hardcoded total.
- Missing icon, missing record, duplicate ID, category conflict: safe display plus visible diagnostic, no crash or silent inflated total.
- Compile changed assets; verify shop, bait and fishing still work. Record results, not assumptions.

Optional journal toast is deferred: existing WBP_CatchToast is not evidence of a finished journal notification. Agree on first-discovery versus record-update policy before adding `Catch journal updated: [Fish Name]`. Rewards, claimed flags and automatic completion grants remain out of scope.

## Evidence and resuming

`Saved/CodexCatchJournal/inspection.json`, `details.json`, `definitions.json`, `catalog_audit.json`, `catalog_review.csv`, and `*_graph_summary.txt` contain this audit. Large native `.t3d` exports remain there for local inspection. Saved output may not travel with the repository; this handoff contains the essential findings.

Next concrete action: **ask Seth to settle category membership and approve the definition-source approach, then walk through Stage 1 in the Editor.** Keep proposed state separate from actual implementation. After each working stage, update ONE_MORE_CAST_CONTEXT.md with changed assets and checks performed.
