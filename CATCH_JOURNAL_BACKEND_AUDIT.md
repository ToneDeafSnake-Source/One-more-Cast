# Catch Journal backend audit — September 29, 2026

## Scope and actual changes

Read-only headless Unreal inspection completed successfully: 31 Blueprint/WidgetBlueprint assets under /Game/Core exported, plus catch arrays from 37 exact BP_FishingSpot-class instances in saved MainDock. No gameplay assets saved, no ID migration, no catalog created, no compile/PIE/save-load test. Added audit_backend.py and report_backend.py; extended summarize_exports.py to accept an export directory. Generated reports and updated project memory only.

Evidence: Saved/CodexCatchJournal/BackendReview contains manifest.json, native .t3d exports, graph summaries, definitions.json and usage_index.md. Native exports contain generated duplicates: repeated matches in _MERGED graphs are not separate gameplay calls. This is a Core/saved-MainDock audit, not a guarantee of every reference in other content, plugins, unsaved Editor state or save files.

## Most important findings

### 1. AddItem has an internal result but no function result

BP_InventoryComponent.AddItem resets the member Boolean AddedItem to false, loops Items, and tests each slot's HasItem. For the first empty slot it writes via Set Array Elem (Size to Fit false), sets AddedItem=true and breaks. If no slot is empty, it writes nothing and finishes with AddedItem=false. There is no exposed success output and no full-inventory reporting in this function.

Evidence: inventory component graph summary, AddItem section lines 12–105. This establishes a silent no-insertion path by graph inspection, not a reproduced gameplay session.

### 2. Catch acquisition ignores that result

BP_Fisherman.EventGraph's AddCaughtFishToInventory calls AddItem and unconditionally continues to UpdateCatchJournal with the original CaughtFish payload. Thus an invocation with full inventory can update the journal despite no item storage. Earlier room checks exist but are not an acceptance contract at this boundary. The normal spot path displays ShowCatchToast before calling acquisition.

Do not describe this as a proven common player-facing reproduction: whether normal gameplay permits capacity to change at the relevant time still needs testing. The unsafe boundary itself is visible in the graph.

### 3. AddItem rebuilds an incomplete payload

The actual array write is fed by Make ST_ItemData, not the complete incoming item. FishID and ItemID inputs are unconnected with default None; Quality is unconnected with default NewEnumerator0 (Legendary in the inspected enum). Quantity is fixed at 1; HasItem is fixed true. Several other fields are forwarded, including name, icon, weights, sell value and catch type flags. BaseName is not forwarded in the inspected Make node.

This supersedes earlier context statements implying AddItem preserves the complete payload. The journal sees the original input, so it can appear correct while the stored inventory item loses identity/quality. This also affects transfers that use AddItem. Verify runtime stored fields, but fix payload preservation before integrating a catalog based on stable IDs.

### 4. Known AddItem callers

Within exported original Core graphs, three call sites were found, all in BP_Fisherman:

- EventGraph / AddCaughtFishToInventory: no acceptance branch after AddItem.
- MoveOneFishToCooler: destination Has room check, AddItem, then source clearing.
- MoveOneFishToInventory: destination Has room check, AddItem, then source clearing.

The latter two should preserve complete item identity/quantity/quality. Do not put journal updates in generic AddItem. Their room checks are directly in the transfer sequence, unlike a potentially earlier fishing eligibility check. Review them when adding the result output; avoid changing fixed-slot indices or capacity logic.

### 5. D20 award path

WBP_FishingRollPopup.ShowRollOutcomeText compares FinalRollWithBonus >= RequiredRoll. Its success path updates success presentation, computes the existing Shimmerworm-related payload modification and calls AddCaughtFishToInventory. Its failure path returns through failure handling without that award call. No direct UpdateCatchJournal call was found in this popup. The award path contains no final AddItem acceptance result or Has room check.

One original ShowRollOutcomeText call site was found in the popup EventGraph, and one original acquisition call inside that function. There is a bIsRolling guard in the roll flow, but that is not proof of exactly-once resolution. ShowRollOutcomeText has side effects despite its display-oriented name and no entry-level resolved guard was observed. Calling it twice on a successful result would award twice. No duplicate gameplay execution has been reproduced. Animation/callback timing, cleanup and re-entry remain runtime verification items; do not add a guard or rename the function without reviewing intended repeat behavior.

## Recommended first implementation stage — approval required

Fix BP_InventoryComponent.AddItem's payload preservation first, as a focused change before catalog migration:

1. Store the complete ItemToAdd payload at the discovered empty index rather than rebuilding a subset.
2. If HasItem must be normalized, use a local full copy plus Set Members in ST_ItemData changing only HasItem; do not overwrite IDs, quantity, quality or BaseName.
3. Preserve current fixed-slot search, write index and no-growth behavior.
4. Verify a deliberately distinctive item survives insertion and both cooler transfers field-for-field, including FishID, ItemID, BaseName, Quality, Quantity and bait-modified SellValue.

This modifies the shared insertion helper, so test all three known callers. No saved schema or stable ID changes are required. It will not repair already stored/defaulted items automatically. Existing saves stay untouched.

Next, separately add proposed bAddedSuccessfully output: false on no insertion, true after the successful write. Reuse the existing AddedItem state or a local result, with explicit return coverage; do not invent a second loosely synchronized flag. Branch at AddCaughtFishToInventory before journal/success notifications. Keep cleanup on both outcomes, do not double-notify, and leave generic transfers/load/sales outside journal acquisition logic. The existing API limitation still prevents claiming autonomous Blueprint pin editing is available; supported editing access or precise manual steps are needed for these changes.

## Definition ownership and usage

Current fishing spots hold ST_FishCatchEntry arrays with FishID, FishDisplayName, FishIcon, flags and mechanics. BuildCaughtFishItem is the current conversion point to ST_ItemData. Inventory/toast/shop paths receive item presentation snapshots. UpdateCatchJournal keys the progress map from the original acquired ST_ItemData.FishID. Save helpers copy that map. The detailed exported usage index lists graph locations for IDs, presentation fields, journal metadata and builders; a text match is not itself an executed consumer.

There is no new authoritative table yet. Proposed DT_CatchDefinitions uses proposed ST_CatchDefinition with DisplayName (Text), Icon (Texture2D reference), CatchType (new small Fish/Treasure enum), JournalCategoryID (Name), JournalSortOrder (Integer). Row name is the stable ID; no second editable ID field. Naming/schema approval remains required before creation.

After approval, BuildCaughtFishItem should resolve catalog presentation for eligible catches while preserving spot-specific odds/quality/weight/value mechanics, quality-prefix formatting, ordinary junk behavior and full ST_ItemData. Existing held items may retain snapshots as requested. Legacy fields remain until consumers are migrated; no immediate deletion. Journal reads catalog + records, never current inventory as its catalog.

## Migration proposal and uncertainty

See CATCH_JOURNAL_MIGRATION_REVIEW.md for all 17 old/new ID proposals, display names, exact icons, current category variants, proposed categories/order and per-ID spot lists.

All inspected RequiredPassTier values are 0, so they cannot prove physical pier grouping. Category proposals use icon-folder hints and must be reviewed. Correction from direct recount of BackendReview/definitions.json: EmeraldRing appears once in all 37 spots; the earlier statement of 36 carried forward the older export incorrectly. Suggested ScaleFish category: Non_Exclusive; treasure remains Treasure even when broadly available. Membership still requires Seth's review.

Icon file existence is checked, not visual correctness. Metadata presence does not establish positive catch probability, reachable spots or actual obtainability. Confirm those before counting unfinished content toward completion.

Prefix renames change save-map keys. Inventory/cooler ST_ItemData.FishID snapshots, journal keys, legacy SavedCaughtFishIDs/related consumers and any hardcoded identity comparisons need review. The exported Core usage index is a starting point, not a complete project-wide reference proof. Do not apply ID mappings until wider references and save policy are settled. For disposable development saves a deliberate reset is simpler than maintaining migration code, but Seth must approve it; no reset is performed or required merely to add a table with unchanged IDs.

## Approval checklist

- [x] Seth approved first focused AddItem full-payload preservation fix. Implementation pending: available tooling cannot safely edit Blueprint pin connections; manual Editor step required. Approval does not include mouse control or the separate success-output change.
- [ ] Approve the separate success-output/acquisition-gating change after reviewing its exact wiring plan.
- [ ] Approve DT_CatchDefinitions / ST_CatchDefinition / catch-type schema.
- [ ] Approve prefix convention and every proposed mapping (or retain current IDs).
- [ ] Approve categories, Non-Exclusive membership and sort order.
- [ ] Decide development-save reset versus migration before any ID change.
- [ ] Confirm Common versus Decent quality ranking; do not change it meanwhile.
- [ ] Confirm full-inventory rejection presentation, preserving fishing cleanup.

## Unverified work

No compilation or runtime/save tests. Full project-wide reference closure, D20 callback exactly-once behavior, visual icon correctness, catch obtainability and unsaved live state remain unverified. No changes to odds, quality configuration, weights, saves, gameplay graphs or UMG have been made.
