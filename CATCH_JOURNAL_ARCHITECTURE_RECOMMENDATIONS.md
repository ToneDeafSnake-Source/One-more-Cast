# Catch Journal — Codex opinions and decision handoff to ChatGPT

Date: September 29, 2026. Owner: Seth. Project: One More Cast, Blueprint-only Unreal Engine 5.7.4.

## Purpose and status

Seth requested this handoff before answering the pending implementation questions. Please review these recommendations with him, help settle the choices, and then guide implementation in manageable stages. This is an architecture recommendation, not evidence that the proposed assets or changes exist.

No journal widgets, catalog, gameplay assets, or save changes have been implemented by Codex. The earlier work produced read-only audit tools, reports, and documentation. No journal compile, PIE, or save/load round trip has been verified. The animation pilot is paused and outside this task.

Read ONE_MORE_CAST_CONTEXT.md for current project facts. The earlier CATCH_JOURNAL_CHATGPT_HANDOFF.md remains useful for verified paths and UMG instructions, but **its proposed runtime fishing-spot scan is superseded by the dedicated-catalog recommendation below**. This is a change of recommendation, not an accepted or implemented migration.

Seth wants names and icons to remain easily editable in Unreal. He wants focused, non-destructive changes actually integrated into the existing game, not disconnected asset shells. No C++, broad inventory/shop/save rewrite, mouse control, or Git operations without the relevant explicit agreement. Ask before launching another headless Unreal process; that permission remains pending. Do not infer answers to the pending design questions from his request to begin planning.

## My recommended direction

Use a dedicated static catalog, one primary journal category per catch, the existing saved progress map, and the agreed three-widget UI. Establish the catalog before building the UMG; do not build a temporary runtime actor scanner first.

Responsibilities:

| System | Owns |
|---|---|
| Static catalog | Stable identity, base display name, icon, catch type, journal category and order |
| Fishing-spot definitions | What can be caught there, probabilities and applicable quality configuration |
| CatchJournalRecords | Player discovery, count and best records |
| Journal UI | Read-only presentation and navigation |

The catalog should know the complete intended journal list regardless of loaded maps, streaming or placed actors. Actor scanning remains useful for Editor validation, not runtime completeness. A future non-fishing treasure source can reference the same catalog identity.

## Verified project foundation and limits

Existing assets and members:

- `/Game/Core/PlayerBlueprints/BP_Fisherman`: CatchJournalRecords, UpdateCatchJournal, GetFishQualityRank, AddCaughtFishToInventory and existing menu helpers.
- `/Game/Core/Inventory_Systems/BP_InventoryComponent`: AddItem and Has room.
- `/Game/Core/SaveGame/BP_SaveGame`: SavedCatchJournalRecords.
- `/Game/Core/Data/Structs/CollectionLog/ST_CatchJournalRecord`: Discovered, TotalCollected, BestWeight, BestQuality.
- `/Game/Core/Data/Structs/ST_FishCatchEntry`: FishID, FishDisplayName, FishIcon, catch flags, JournalCategoryID, JournalSortOrder and catch configuration.
- `/Game/Core/Data/DataTables/CollectionLog/DT_JournalCategories`, using ST_JournalCategoryData. Current sort field is spelled **SortOtder**.
- `/Game/Core/Interactables/FishingSpot/BP_FishingSpot`: FishCatchTable arrays.
- `/Game/Core/UI_Components/Inventory/WBP_Inventory`: existing inventory/menu integration point.
- `/Game/Core/UI_Components/Menus/FishingRollPopup/WBP_FishingRollPopup`: D20 resolution to inspect next.

Native exported graph connections verify player CatchJournalRecords -> SavedCatchJournalRecords in FillSaveObjectFromCurrentState and the reverse assignment in ApplyCoreSaveData. They do not prove actual disk persistence.

UpdateCatchJournal uses FishID, checks fish/treasure eligibility and nonempty identity, and has new/existing record logic for counts, best weight and ranked quality. The inspected helper ranks Valuable=5, Legendary=4, Rare=3, Common=2, Decent=1, Sickly=0. Do not compare enum ordinals or change this ranking without confirming intent.

The September 28 saved MainDock audit covered 37 exact BP_FishingSpot-class instances, yielding 17 eligible unique IDs: 16 fish and EmeraldRing. It did not cover unsaved edits, other maps or subclasses. Every ID has blank journal category metadata in at least one occurrence; Catfish has both Pier_01/sort 10 and blank/sort 0 variants. Only Pier_01 exists in the category table.

IDs: Agar, Angloria, CateFish, Catfish, ChloroFish, CowFish, DuctFish, EmeraldRing, Grasper, Izatagar, JuneBeetle, PinkyPoo, ScaleFish, SeaBear, SmoothEmberscale, Triangel, YellowfinTuna.

## Catalog design: proposed, not created

I recommend a new DT_CatchJournalEntries with a small new Blueprint struct, rather than reusing ST_FishCatchEntry. Proposed fields:

- DataTable row name = existing FishID, with identical values. Do not add a second independently editable CatchID field.
- DisplayName: Text, base name rather than quality-prefixed item name.
- Icon: Texture2D reference.
- CatchType: small Fish/Treasure enum, scoped to this feature rather than migrating all item types.
- JournalCategoryID: Name.
- JournalSortOrder: Integer.

Keep existing FishID variable names and saved keys. Changing a display name or icon must not change identity. Stable IDs are not user-facing labels.

Seth should be able to open one catalog row and edit its name/icon directly in Unreal. However, creating the table alone does not make other systems use it. Be explicit about the integration stage:

1. Seed a candidate catalog from existing definitions and review conflicts.
2. Approve membership/order; make the table authoritative for journal display.
3. Preserve existing fishing fields initially; validate overlapping names/icons/types against the catalog.
4. In a focused integration step, have BuildCaughtFishItem resolve shared presentation data by FishID for catalog-eligible catches while preserving the full ST_ItemData payload and existing quality-prefix behavior. Leave ordinary junk and unrelated items on their existing path.
5. Stop treating overlapping spot presentation fields as independently authored truth once that integration is verified. Do not immediately delete struct members.

If Seth expects one edit to affect inventory, toast and journal in this milestone, include step 4 before calling it complete. Do not promise centralized editing while those consumers still read separate copies.

Existing inventory/save items may already contain captured names/icons. Decide whether old held items retain that snapshot or presentation is resolved at display time. Centralizing the builder guarantees consistency for newly built items, not automatically for previously saved item payloads. Avoid rewriting historical item stats or save contents merely to refresh labels.

Do not continuously regenerate the authoritative table from spots; that reverses ownership and could erase journal-only content. Use scanners to report missing IDs, conflicts and unreachable entries instead.

## Metadata migration and categories

I favor one primary category per catch. Category membership describes journal organization, not every place a fish can be caught. Location information can be separate later. One saved record remains keyed by identity regardless of category.

Suggested categories/order: Treasure, Pier 1, Pier 2, Pier 3. Confirm exact labels/IDs and ScaleFish membership with Seth. Do not infer approved membership from texture folder names.

With a dedicated catalog, do not first edit every map-instance journal field merely to normalize data that the new UI will stop reading. Inspect existing consumers, author consistent catalog metadata, and leave legacy fields intact until safe cleanup. If an existing consumer still requires them, synchronize only category/order with a before/after audit. Never change catch odds, nested quality tables, existing IDs or unrelated fishing data during metadata work.

I recommend leaving SortOtder unchanged for this milestone. If Seth prefers correcting it, do that separately in Unreal, preserving values and checking struct-node pins, DataTable rows, scripts/import headers, compilation and reopen behavior. Do not delete/recreate the field casually.

## Acquisition correctness: highest-priority investigation

Verified from the saved exported call site:

- AddCaughtFishToInventory calls inventory AddItem.
- AddItem's normal execution output directly calls UpdateCatchJournal.
- The exported AddItem call node has execution pins, Target and ItemToAdd, **no exposed success/failure result pin**.
- Upstream Has room checks exist, but their coverage is not proven.
- The inspected normal-catch path calls ShowCatchToast before AddCaughtFishToInventory.

Correction to earlier guidance: do not instruct Seth to connect an existing AddItem Success pin; the inspected node does not have one.

Still needed: the complete AddItem implementation and D20 resolution graph. We cannot yet assert how insertion fails, whether every path guarantees space, or whether duplicate completion callbacks exist. The full-inventory count problem is a credible risk, not a reproduced runtime bug.

My proposed remedy if confirmed: add an explicit Boolean acceptance output to AddItem (proposed name bAddedSuccessfully), true only after actual successful storage. Branch on it at the catch acquisition boundary; only success calls UpdateCatchJournal. Preserve existing callers and inspect return paths. No journal logic inside generic AddItem, because moves, restores and other operations must not count as new catches.

Both normal and successful D20 catches should reach one acquisition/reporting point. Failed D20 resolution must not award. Success notifications should follow acquisition, and necessary cleanup should run on failure too. A success Boolean does not prevent duplicate successful calls: inspect one-time resolution separately.

Recommended overflow policy, pending Seth's answer: reject, clearly report inventory full, and do not increment the journal. Do not add automatic cooler transfer, item dropping or an overflow system without agreement.

## UI, counting and save opinions

The approved conceptual structure is sound: WBP_CatchJournal with WidgetSwitcher pages Categories / Entries / Detail, plus reusable WBP_JournalCategoryButton and WBP_JournalEntrySlot. None has been created by Codex.

Use small reusable catalog/count helpers so eventual reward checks do not depend on opening a widget. No Tick scanning. Refresh on open and appropriate state changes. Parent controls navigation; children report selected IDs through dispatchers.

Count definitions in the catalog, not saved-map length. Discovered means record exists AND Discovered=true. Complete means Total>0 AND DiscoveredCount==Total. White while incomplete, green when complete. No hardcoded totals. Unknown saved IDs should not inflate totals or be deleted during UI refresh.

Reuse icons with black tint and full alpha for silhouettes, checking that source textures have useful transparency; opaque backgrounds will become black rectangles. Undiscovered name/tooltip text must not leak the name. Reset text, tint and visibility for every detail selection. Fish and treasure share one detail view; treasure collapses weight/quality. Requested treasure detail: Type Treasure, Total Found, name ??? and count 0 before discovery.

Existing CatchJournalRecords -> SavedCatchJournalRecords is enough. Static catalog data does not belong in that save record. Catalog addition alone need not change SaveVersion if IDs and record semantics stay unchanged; test old development saves rather than assuming compatibility. Do not repurpose or rename stable IDs silently.

Future completion rewards can use this structure, but persistent one-time claiming will likely need an additive saved set/map of claimed reward IDs. Defer it. Adding content may make a formerly complete category incomplete; decide that policy when rewards are implemented, without revoking prior rewards automatically.

Legendary quality does not create a second species entry. A genuinely distinct special catch can have its own stable ID. Make sure catalog entries intended for completion are actually obtainable; do not accidentally count unfinished content.

## Questions awaiting Seth's answers

1. Approve catalog ownership of names/icons/type/category/order, and include item-builder integration in this milestone so new catches use those edits everywhere?
2. Confirm categories/order and one primary category per catch. Where does ScaleFish belong? Review the remaining membership list before authoring.
3. Confirm full-inventory award policy: reject with message and no journal increment, or something else?
4. Confirm fish ranking Legendary > Rare > Common > Decent > Sickly, especially Common above Decent. Valuable remains separate in the existing helper.
5. Navigation preference: inventory launch; Back/Escape details -> entries -> categories -> close; Tab/Close directly to gameplay? Pause policy should match the chosen existing menu behavior, not be guessed.
6. Any relevant changes since the audit, or catches outside MainDock?
7. Permit another read-only headless Unreal export without mouse control, or use screenshots only?

Additional presentation question when wiring centralized editing: should changing a catalog name/icon immediately affect previously held/saved items, or only newly obtained items? Explain the distinction before choosing the smallest implementation.

## Requested screenshots, in priority order

First batch:

1. BP_InventoryComponent -> AddItem: complete graph, every return, empty-slot search, array write, full handling, and Inputs/Outputs Details panel. Multiple readable overlapping screenshots are better than one illegible overview.
2. WBP_FishingRollPopup: final success/failure decision through item award and cleanup. Include calls to AddCaughtFishToInventory, AddItem, UpdateCatchJournal and notifications; inspect any delegated helper next.

Second batch:

3. BP_Fisherman -> AddCaughtFishToInventory, entire execution chain.
4. BP_FishingSpot -> BuildCaughtFishItem, especially name/icon/ID/type and full ST_ItemData assembly.
5. BP_Fisherman -> Open Inventory and the visible inventory UI when implementing menu integration.

Do not ask for unrelated Blueprint screenshots or launch/control the Editor without permission. Existing exports can inform discussion, but recent screenshots may supersede them.

## Safest order from here

1. Settle choices and inspect AddItem/D20 contracts.
2. Agree on catalog ownership, row schema and memberships.
3. Seed and validate the catalog; no balance changes.
4. Implement verified acquisition gating with one journal update point.
5. Integrate shared presentation lookup to the agreed extent, preserving complete item payloads.
6. Build journal UI against catalog + saved progress; integrate existing menu ownership/close behavior.
7. Test normal/D20 success, failure/full capacity, repeats/double callbacks, treasure, moving/selling, old/new saves, keyboard/mouse closure and category completeness.
8. Record actual changed assets and validation results in ONE_MORE_CAST_CONTEXT.md. Defer rewards, broad cleanup and further catch-system restructuring.

Please help Seth make the outstanding decisions before giving a long build tutorial. Guide one manageable stage at a time and distinguish verified current wiring, agreed design, proposed changes and tested results throughout.
