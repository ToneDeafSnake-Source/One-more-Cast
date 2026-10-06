# Main-system light review — September 29, 2026

Read-only review of recent native exports for 31 Core Blueprints, saved spot definitions, current file inventory and project context. No gameplay edits, deletions, new Editor launch, compile or runtime testing. MainDock was saved after the export; map findings are snapshot evidence, not verification of current unsaved/live state. AddItem manual fix is approved but completion has not been confirmed.

## Priority findings

1. **AddItem partial payload — confirmed in export and Seth's screenshot.** Make ST_ItemData drops IDs/BaseName/Quality and fixes Quantity at 1. First repair remains preserving the full incoming item, normalizing only HasItem. Then test both cooler transfers.
2. **Journal acceptance — confirmed unsafe graph boundary.** AddItem may write nothing; AddCaughtFishToInventory still updates progress. Add an explicit accepted result and gate acquisition side effects after the payload fix. Runtime reachability with full inventory has not been reproduced.
3. **Normal catch notification precedes insertion — confirmed graph ordering.** Success presentation can precede confirmed storage. Review alongside acceptance gating, preserving cleanup on both outcomes.
4. **D20 award is inside ShowRollOutcomeText — confirmed responsibility mismatch.** Calling the function is not merely refreshing text; a successful result awards an item. Avoid reusing it for display refresh. Re-entry/duplicate resolution is a test candidate, not a reproduced bug.
5. **Journal category metadata incomplete — snapshot finding.** Existing spot-level metadata is not a dependable catalog. Follow the approved dedicated-catalog direction; do not spend time normalizing legacy per-spot fields unless a consumer needs them.
6. **RequiredPassTier is 0 on all 37 exported spots.** This prevents using it to infer physical pier identity. It may be intentional if gates own access. Test access boundaries before changing any value.
7. **Quality labels/rank require design confirmation.** Common ranks above Decent; TrophyOrLegendaryCatch remains a historical-looking condition name. Not proof of wrong behavior. Preserve existing ranking until Seth confirms intent.

## Correction: EmeraldRing

The older export recorded 36 of 37 spots, but the September 29 BackendReview/definitions.json contains exactly one EmeraldRing row on each of its 37 spots. The prior backend report incorrectly carried forward the old count. Do not add another EmeraldRing row based on that report. Row presence does not establish correct odds or reachable catch behavior. The map has been saved again since that export.

## Naming and redundancy candidates

- **SortOtder:** actual category-struct typo. Cosmetic; leave for a separate controlled struct/reference cleanup.
- **SaveEquippedRodIDs:** inconsistent spelling/plural wording; current references exist. Do not rename as part of bug fixing.
- **SavedCoolerUpgradeTier versus SavedCoolerTier:** the former is declared in BP_SaveGame, but no match appears in exported graph summaries; the latter has player save/load references. Candidate stale field, not proven safe to delete: inspect defaults/serialization and all references before removal.
- **SavedCaughtFishIDs:** despite looking superseded by the journal map, player save and load graph references still exist. It is not currently safe to classify as unused.
- **WBP_ShopMenu_Working_Backup:** clear backup candidate. Confirm no live references, then let Seth decide whether external archival is preferable to keeping it in Content.
- **Core/FishingSpot_OLD and old FishingSpot paths:** prior review identifies redirectors. Use Unreal's redirector workflow after reference review; never delete these directly in Explorer.
- **BP_CodexRotationTest:** candidate experimental asset. Need level/reference check before removal.
- **FishermanTest and CodexRetargetTest:** names alone are not evidence of redundancy. Character assets may be in use; retarget assets belong to an intentionally paused pilot. Preserve them.

## Scope limits and safe cleanup order

### Owner clarification after this review

Seth confirms RequiredPassTier=0 is intentional debugging, not a defect. WBP_ShopMenu_Working_Backup and BP_CodexRotationTest should be removed in a later cleanup after reference checks. FishermanTest remains undecided. SavedCoolerUpgradeTier may predate the revised cooler upgrade system; inspect before removing. Investigate old redirectors through Unreal. Existing development save files need not remain compatible, but current save/load functionality must remain correct; no immediate save deletion was requested.

This is not a complete unused-asset analysis. No-reference-in-these-exports is not proof of unused: levels, animation assets, soft references and dynamically loaded content also matter.

Recommended order: finish and test AddItem; fix acceptance/notification handling; approve catalog/category data; validate save/load and D20; only then perform a separately approved cleanup. Before deletions, Seth should establish a recoverable checkpoint, inspect Unreal referencers/dependencies and soft loads, review exact candidates, and use Editor deletion/redirector tools. Avoid cleaning whole purchased packs or folders based on names. Test MainDock and a packaged build after material cleanup.

No assets have been declared safe to delete by this review.
