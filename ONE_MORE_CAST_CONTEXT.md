# One More Cast — Current Project Context and Codex Handoff

> **Project memory rule:** Read this document before meaningful project changes. After completing an architecture, gameplay, save-data, UI, or naming change, update the affected current-state sections and add a short dated changelog entry. Replace superseded details; retain history only in the explicitly historical section. Verified implementation takes precedence over this document. Record uncertainty instead of guessing.

Last reviewed: **2026-10-01**. Owner/developer: **Seth** (`ToneDeafSnake-Source`).

## 1. Review baseline and evidence

| Item | Reviewed baseline |
|---|---|
| Repository | https://github.com/ToneDeafSnake-Source/One-more-Cast |
| Actual local checkout | `G:\Unreal Projects\OneMoreCast` |
| Project file | `OneMoreCast.uproject` |
| Branch / commit | `main`, `5eb4b78a027408abec87326c4ad7c89ea9f4a946` — “Update 9 - 20 - 26” |
| Published checkpoint | Public GitHub `main` was verified in a live browser at `5eb4b78`, matching the local checkout. GitHub normally trails active local work until Seth publishes after the workday |
| Working tree | No gameplay assets were changed by the onboarding/review work. `AGENTS.md` and this context file are local untracked project-memory files |
| Engine | `.uproject` associates with UE **5.7**; Seth reported **5.7.4** in the conversation |
| Conversation | All **371 available turns** of **One More Cast 2**, June 22–September 27, 2026 |

The public repository at `https://github.com/ToneDeafSnake-Source/One-more-Cast` was verified in a live browser on September 27, 2026. Its `main` head matched the local checkout at `5eb4b78`. During active work, use the local files as the newest truth; use GitHub as the authoritative completed/published checkpoint when local evidence is missing or ambiguous. Do not pull or publish on Seth's behalf without explicit agreement.

Evidence labels used below:

- **[Repository]**: directly observed filenames, configuration, commit changes, or serialized asset names/fields/references.
- **[Confirmed]**: Seth explicitly described the working implementation or confirmed a fix in the conversation, supported by current asset symbols where available.
- **[Design]**: accepted desired behavior; not proof of implementation.
- **[Verify]**: current wiring, defaults, or runtime behavior still needs an Unreal Editor check.
- **[Historical]**: older approach or proposal that must not be treated as current.

Unreal `.uasset` and `.umap` files are binary. This review inspected their readable metadata, not a fully reconstructed executable graph. Asset/function presence does not prove correct execution order, connections, save compatibility, or gameplay behavior. No Unreal compile, PIE session, or packaged-game test was performed. Conversation screenshots and the initial uploaded handoff file were not exposed by conversation retrieval; their contents were not visually reviewed. [Epic’s asset/source-control documentation](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine) explains the binary format limitation.

## 2. Game direction and collaboration rules

**One More Cast** is Seth’s solo, Blueprint-only fishing game: a cozy, humorous dock/pier setting with a “one more trip” feeling. The existing loop is **fish → sell for Scales → buy upgrades → access better fishing**. The next purpose layer is the Catch Journal, small quests, and balancing before another friends playtest. The present release goal is to make a meaningful game to share with friends; a public demo or commercial release has not been committed to. Five to ten hours of progression is an aspiration, not a measured current playtime. **[Confirmed / Design]**

Seth is learning Unreal and wants an expert teacher’s explanation: specific node names, pin types, inputs/outputs, and the reason for each change. Work in manageable stages. Define required functions, variables, structs, and enums before instructions depend on them. Build a sound final architecture in small slices; avoid disposable implementations and unnecessary rewrites. Preserve the working shop and catch pipeline. Reuse data and keep UMG small and reusable.

Gameplay implementation should remain in Blueprints. C++ may be discussed only when it has a concrete advantage, and it requires Seth's explicit approval because he must be able to read, maintain and extend the project himself. Text/configuration/documentation changes can be handled directly when authorized. Unreal Editor control requires case-by-case permission; otherwise provide precise Blueprint instructions and verify through screenshots or Seth's results. Seth controls Git and project file handling. Codex must not pull, commit, branch, merge or push unless both collaborators explicitly agree that Codex should perform that operation. **[Confirmed]**

For an underspecified design choice, Codex should present a recommendation, explain why it works and describe the tradeoffs; Seth makes the decision before implementation. The intended identity is **chill, casual and rewarding**, with rare items and oddities creating progress and discovery, plus enough friction to remain interesting. Most mechanics and stories should feel grounded and sincere, while a limited number can turn unexpectedly ridiculous for a chuckle. Tutorials should prefer natural, human dialogue and nonintrusive gameplay over flow-stopping instruction popups. **[Confirmed / Design]**

Longer-term plans include an arrival NPC who introduces the dock through natural dialogue and nonintrusive actions, an introductory quest awarding five Scales for the first pass, first-time shop guidance, fish delivery quests, a five-minute fishing contest, rare treasure turn-ins, legendary trophies, a personal shack with displays, sleeping through the night, night content, and a live main-menu background with a short first-new-save cinematic. Future quest work should favor reusable Blueprint foundations for straightforward fetch/delivery objectives and extensible patterns for more complex tasks. Humor can come from occasional grounded setups with absurd reveals; any individual example remains illustrative until explicitly accepted as content. These are **[Design]**, not established completed systems. Night-fish art and imported characters do not prove night progression, quests, or a character integration is complete.

### Deferred topic: reusable dialogue for quests and activities

**[Seth's request, September 29; future discussion, not implemented]** Build a very simple, reusable Blueprint dialogue system shared by different NPC interactions, including an arrival introduction that offers a short fetch quest and small reward, and an NPC offering participation in a fishing contest. Keep dialogue content easy to author/edit and avoid separate dialogue implementations for each NPC. This does not replace the current inventory/Catch Journal task.

**[Proposed direction, not yet approved architecture]** One shared dialogue UI and data-driven lines/choices, with conditions selecting appropriate responses and explicit actions requesting quest acceptance/turn-in or contest entry. Keep quest progress, inventory checks/item removal, contest rules/timers and reward validation outside the dialogue widget. Recheck requirements when executing an action and prevent duplicate rewards. Start with one short fetch-quest conversation, then reuse the same foundation for a contest NPC; avoid building a large general-purpose narrative editor. Decide branching needs, interaction/input behavior, save flags and content format when this topic is resumed.

### Deferred narrative direction: Marc and nighttime melancholy

**[Accepted creative direction, not implemented]** Seth wants lighthearted, slightly goofy daytime life with a veneer of “everyone is fine” while people avoid their issues. Night becomes quiet, lonely and melancholy, with occasional eerie/Halloween undertones rather than relentless despair or forced story objectives. The world/story should develop incidentally through ordinary play. Skeleton NPC concept name: **Marc**; he sits looking over the ocean, appreciating ocean sounds, passing boats and small things. Do not infer dialogue/gameplay implementation from existing mesh/animations.

**First-meeting dialogue draft to preserve:** Player: “Hey...” Marc: “Hey.. Why are you looking at me like that?” Player: “I don't want to be rude... but...” Marc: “Didn't expect to see a skeleton here did you?” Player: “Well.. No.” Marc: “The names Marc. I'd drop a cliche and say 'well it used to be'.. But it's still Marc.” Player: “Ah.. I get you. Because of the whole-” Marc: “Because of the whole being dead and a skeleton thing, yeah.” Player: “May I ask why you're just sitting here?” Marc: “Just watching the water and the ocean sounds are peaceful. Sometimes you catch a glimpse of a boat going by. Just the small things, ya know?” Player: “Your out here kinda late aren't you?” Marc: “I mean, you are too” Player: “You got me there.” [Silence.] Player: “So, being a skeleton does that mean you don't have to sleep?” Marc: “Nah. I have to sleep. Right now I'm just too exhausted to sleep” Player: **“That doesn't make sense”** Marc: **“I know it doesn't.”** [Silence.] Marc: “Listen. I'll see you around. Here, take this. Maybe you'll find a use for it” [Gives bait, stands, jumps into water and disappears; possible later encounters/new dialogue/small quest, depth undecided.]

**Interaction prompt [accepted design]:** Before the first introduction, show “Talk to skeleton”. After the player learns his name during that encounter, subsequent interaction prompts show “Talk to Marc”. Name-known state and persistence are not implemented; decide storage during dialogue work.

**Explicit authorial intent:** Preserve the exhaustion exchange. Marc should feel misunderstood: the player realizes they also misunderstood him in that moment, like everyone else. Do not replace the player's response with immediate empathy or resolve/explain the feeling too quickly. Quiet pause and subsequent bait gift support this reading. Assistant suggestions about a “going home” exit, boat quest or extra lines remain unaccepted possibilities. Future work only; Catch Journal stays current priority.

## 3. Project layout and startup

**[Repository]** No project C++ `Source` directory or declared game modules were found. Gameplay is Blueprint-oriented. Do not introduce a C++ migration as part of routine feature work.

| Configuration | Current value |
|---|---|
| Editor startup / default game map | `/Game/MainDock.MainDock` |
| Default GameMode | `/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C` |
| GameInstance | `/Game/Core/SaveGame/BP_FishingGameInstance.BP_FishingGameInstance_C` |
| Enabled plugins | ModelingToolsEditorMode (editor only), GameplayStateTree, ElectronicNodes |
| Packaging baseline | Development; Pak / IoStore / compression enabled; MainDock included |

The current target is an offline Windows PC game, initially mouse-and-keyboard. Controller support is a possible later addition. The general performance target is 60 FPS at 1920×1080, with player-selectable display/performance settings when that work is prioritized. The low-poly art and low-detail textures are expected to make this achievable, but performance must still be measured rather than assumed. A friends-only leaderboard is a speculative future idea; do not introduce online architecture for it now. **[Confirmed / Design]**

The September 20 commit added `Content/FishermanTest` character assets and modified `MainDock`. Whether the test character replaces the active player mesh is **[Verify]**.

### Active asset map

Paths are relative to the repository root. Open these active assets rather than similarly named redirectors or backups.

| Asset / location | Responsibility |
|---|---|
| `Content/Core/PlayerBlueprints/BP_Fisherman.uasset` | Player state, inventory entry point, currency, purchase routing, equipment, bait, interaction focus, save orchestration, journal updates, fishing state and action audio |
| `Content/Core/Interactables/FishingSpot/BP_FishingSpot.uasset` | Spot catch definitions, species/quality selection, building an item, normal/D20 decision, popup creation, fishing stand point and pass checks |
| `Content/Core/Inventory_Systems/BP_InventoryComponent.uasset` | Fixed slot array, add/remove/move/swap, capacity and save helpers |
| `Content/Core/PlayerAttachments/BP_FishingRodMesh.uasset` | Shared held-rod actor, mesh selection and pose corrections |
| `Content/Core/SaveGame/BP_SaveGame.uasset` | Saved durable player/progression data |
| `Content/Core/SaveGame/BP_FishingGameInstance.uasset` | Pending slot/user and load-after-level-open handoff |
| `Content/Core/UI_Components/BPI_Interact.uasset` | `OnInteract` and `SetInteractionFocused` interface contract |
| `Content/Core/NPCs/NPC_Blueprints/MainShopNPC/BP_ShopNPC.uasset` | Shop interaction and opening the existing menu |
| `Content/Core/Interactables/Pier_Access/BP_PierAccessGate.uasset` | Pier access gate behavior |
| `Content/Core/Interactables/Gamemessages/BP_GameMessages.uasset` and `BP_SignMessages.uasset` in that folder | Interactable messages/signs |
| `Content/Core/UI_Components/Inventory/WBP_Inventory.uasset` and `WBP_InventorySlot.uasset` | Inventory/cooler display, slot interactions and bait display |
| `Content/Core/UI_Components/Menus/TackleShop/WBP_ShopMenu.uasset` | Combined buy/sell shop; generated buy rows, sell grids, confirmation and refresh |
| `Content/Core/UI_Components/Menus/TackleShop/WBP_ShopBuySlot.uasset` | One reusable shop listing / purchase button |
| `Content/Core/UI_Components/Menus/TackleShop/WBP_MerchantSellSlot.uasset` | One sellable inventory entry |
| `Content/Core/UI_Components/Menus/FishingRollPopup/WBP_FishingRollPopup.uasset` | D20 presentation, bait confirmation, roll resolution and outcome handoff |
| `Content/Core/UI_Components/Menus/FishingRollPopup/WBP_BaitSlot.uasset` | Reused bait icon/count/tooltip/click dispatcher |
| `Content/Core/UI_Components/Menus/PauseMenu/WBP_PauseMenu.uasset` | Save, load, resume and unstuck controls |
| `Content/Core/UI_Components/OnScreenMessages/WBP_CatchToast.uasset` | Existing catch toast; journal-specific presentation is still to verify/build |
| `Content/Core/UI_Components/OnScreenMessages/Signs/WBP_SignFishIcons.uasset` | Sign icon widget; current name is plural |
| `Content/Core/SFX_Music/BP_AudioManager.uasset` | Ocean audio component |
| `Content/Core/Environment/PolygonPirates/EpicContent/Mannequin/Animations/ThirdPerson_AnimBP.uasset` | Character animation Blueprint, including the discussed footstep notify flow; pack relocated by Seth in Content Browser October 1 |
| `Content/Core/Floating_Objects/BP_FloatingTrash.uasset` | Floating trash prop asset; motion needs runtime verification |

Player component names include `BP_InventoryComponent` and `BP_CoolerInventoryComponent`; the latter is a player component instance name, not a separately found Blueprint asset. Both use the reusable inventory component architecture. **[Repository / Confirmed]**

**October 1 character-folder repair [native verified]:** Seth moved PolygonPirates into `Core/Environment` through Content Browser; 11 original-path full mesh remnants had broken dependencies, and the live original Gentleman mesh failed saving with invalid internal references. After Editor closure and verified backups, native headless Python removed only unreferenced, backed-up destination conflicts and relocated 37 working meshes/physics assets/attachments to `Content/PolygonPirates/Meshes/CharactersUE4Mannequin/`. Shared skeleton/materials and character Blueprints remain under `Core/Environment/PolygonPirates`; references were updated natively in BP_Fisherman, 12 character Blueprints and three isolated retarget-pilot assets. Also repaired 11 physics preview soft paths. Fresh process verified all 37 reload/save operations, source redirectors or absence of references to removed paths, skeleton/physics/material/import ownership, and BP_Fisherman's original-path Gentleman mesh. 81 non-character pack assets remained byte-identical; props were not relocated, and MainDock matched its pre-repair backup. Backup/reports: `Saved/AssetRepairBackups/GentlemanMove_2026-10-01`; scripts: `Scripts/Editor/*character_move*.py`, `fix_character_preview_paths.py`, `inspect_gentleman_move.py`. Interactive Save All/PIE remain untested; needed source-folder redirectors are retained. Next: Seth reopens the Editor, tries Save All and checks the player before resuming Catch Journal UMG.

## 4. Fishing and item flow

### Current responsibility split

**[Confirmed, repository symbols present]**:

```text
BP_FishingSpot: Choosing Fish To Catch
  → RollFishSpecies
  → RollFishQuality
  → BuildCaughtFishItem
  → complete ST_ItemData, stored locally as CaughtFish
  → normal catch: BP_Fisherman.AddCaughtFishToInventory
  → gated catch: Make ST_FishingRollContext → WBP_FishingRollPopup
      → roll success: final item → BP_Fisherman.AddCaughtFishToInventory
      → roll failure: fish escapes; no inventory item
```

`ST_ItemData` is the shared item payload for inventory, toast, tooltip, and selling. Keep one authoritative item result. `CaughtFish` remains useful inside the fishing spot; the popup reads `RollContext.CaughtItemData`. The context wraps the same item, not a second independent fish state.

Species selection uses explicit rare-catch attempts plus a weighted fallback pool. `ExplicitCatchRateDenominator` expresses a 1-in-N attempt: a larger denominator makes that attempt rarer. `CommonRollWeighting` affects fallback **species** selection, not quality. Sequential explicit attempts can affect effective overall probabilities; check the graph/order before quoting final balance odds. **[Confirmed / Verify]**

Quality is selected from each catch entry’s nested `QualityTable`. Its entry supplies weight range, value multiplier and `RequiredCatchDC`. The builder computes sell value from **base value × quality multiplier** (rounded); weight is for flavor/records and does **not** multiply sell value. Seth explicitly corrected earlier advice on this. The historical stray multiplication by zero was fixed. **[Confirmed]**

**Important current discrepancy:** `E_FishQuality` contains **Legendary, Rare, Common, Decent, Sickly, Valuable**, not the older chat’s Common/Uncommon/Rare/Trophy/Legendary list. The actual stored D20-related item fields are `IsLegendaryFish` and `IsRareFish`. Verify the builder’s flags, gate condition, quality labels and `GetFishQualityRank` together. Do not reintroduce Trophy or assume enum numerical order is best-to-worst. `TrophyOrLegendaryCatch` still exists as a condition label and needs reconciliation. **[Repository / Verify]**

Junk and treasure currently share the catch pipeline through `bIsFishCatch`, `bIsJunkCatch`, and `bIsTreasureCatch`, becoming the matching item booleans. There is no current `E_ItemType` asset. For non-fish entries, do not leave `QualityTable` empty unless the actual graph supports that: older guidance used a neutral single quality entry. Treasure journal support should ignore weight/quality in presentation without breaking the existing catch builder. **[Confirmed / Verify]**

## 5. Structs, enums and data tables

These are **current serialized field names**, not suggested replacements. Field types and defaults should be confirmed in the Editor before changing schema.

### Structs

| Struct | Current fields / contract |
|---|---|
| `ST_ItemData` | `HasItem`, `ItemName`, `BaseName`, `Quantity`, `CatchDC`, `SellValue`, `ItemIcon`, `MinWeight`, `MaxWeight`, `FishWeight`, `ItemID`, `FishID`, `Quality`, `IsLegendaryFish`, `IsRareFish`, `bIsFish`, `bIsJunk`, `bIsTreasure` |
| `ST_FishCatchEntry` | `FishID`, `FishDisplayName`, `FishIcon`, `BaseSellValue`, `ExplicitCatchRateDenominator`, `CommonRollWeighting`, `QualityTable`, `bUseExplicitCatchRate`, `bIsFishCatch`, `bIsJunkCatch`, `bIsTreasureCatch`, `JournalCategoryID`, `JournalSortOrder` |
| `ST_FishQualityEntry` | `Quality`, `RateDenominator`, `ValueMultiplier`, `MinWeight`, `MaxWeight`, `RequiredCatchDC` |
| `ST_FishingRollContext` | **Only** `CaughtItemData`, `FishingSpotRef`, `bIsNight` are current struct fields; `SpotTags` is not present |
| `ST_FishingRodData` | `RodName`, `RodIcon`, `Description`, `CostScales`, `CatchBonus`, `SpecialTags`, `ConditionalCatchBonus`, `BonusCatchCondition`, `ConditionalRollModifiers`, `RodActorClass`, `RodMesh`; rod identity currently comes from the table row name, not a stored `RodID` member |
| `ST_CatchBonusModifier` | `ModifierID`, `DisplayName`, `Condition`, `RequiredTag`, `BonusAmount` |
| `ST_BaitData` | `BaitID`, `BaitName`, `BaitIcon`, `Description`, `ToolTipText`, `CostScales`, `MaxOwned`, `EffectGroup`, `EffectType`, `BonusAmount`, `SortOrder` |
| `ST_ShopEntry` | `EntryID`, `EntryType`, `LinkedRowID`, `UpgradeChainID`, `DisplayName`, `Description`, `Icon`, `CostScales`, `SortOrder`, `bHideWhenOwned`, `Status` |
| `ST_CatchJournalRecord` | `Discovered`, `TotalCollected`, `BestWeight`, `BestQuality` |
| `ST_JournalCategoryData` | `CategoryID`, `DisplayName`, `Description`, `Icon`, **`SortOtder`** — this spelling is the current field |

`ST_ItemData.FishID` is the stable catch/species journal key. `ItemName` may contain a quality prefix; do not key records by display name, per-catch identity, or quality. `CatchID` was proposed, not implemented. `ItemID` and `FishID` both exist; inspect their separate roles before altering either.

Journal structures live under `Content/Core/Data/Structs/CollectionLog/`; the other structs are under `Content/Core/Data/Structs/`. `BestWeight` has serialized real/double metadata; do not silently change precision based on older examples.

### Enums

All six are under `Content/Core/Data/Enum/`.

| Enum | Current display labels |
|---|---|
| `E_FishQuality` | Legendary, Rare, Common, Decent, Sickly, Valuable; the listed serialization order is **not a ranking contract** |
| `E_BaitEffectGroup` | CatchBonus, Misc |
| `E_BaitEffectType` | CatchRollBonus, SellValuePercentBonus, WeightBonus, RollMarginScalesChange |
| `E_CatchBonusCondition` | Always, AtNight, DuringDay, JunkCatch, TrophyOrLegendaryCatch, SpotHasTag |
| `E_InventoryContainerType` | MainInventory, Cooler |
| `E_ShopEntryType` | Rod, Bait, CoolerUpgrade, FishingPass |

`WeightBonus`, time conditions, clothing/buff variables and tag conditions are extension hooks; their presence does not prove authored content or complete active behavior.

### Tables and authored definition sources

| Source | Current evidence |
|---|---|
| `Content/Core/Data/DataTables/DT_FishingRods.uasset` | BasicRod / SturdyRod identities; equip by row ID |
| `Content/Core/Data/DataTables/DT_Baits.uasset` | TastyBait, Shimmerworm, Gambeetle |
| `Content/Core/Data/DataTables/DT_ShopEntries.uasset` | Pass and cooler Tier1/Tier2/Tier3 listings; rod/bait listings; drives display and charged purchase cost |
| `Content/Core/Data/DataTables/CollectionLog/DT_JournalCategories.uasset` | `Pier_01` is observed; verify/add Treasure and other intended categories |
| `BP_FishingSpot.FishCatchTable` | Current species definitions are arrays of `ST_FishCatchEntry` on fishing spots, with nested quality arrays |

No `DT_FishData`, `DT_CoolerUpgrades`, `DT_FishingPasses`, `ST_PlayerSaveData`, or `E_ItemType` asset was found. Those names appeared in proposals; they are not current dependencies. Full row values, map-instance catch arrays, prices, catch counts, and category totals were not exported/validated in this review. Export the actual data before balancing. Unreal provides Editor Scripting CSV/JSON table export functions. [Epic’s DataTable API](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDataTableFunctionLibrary).

## 6. Inventory, cooler and selling

**[Confirmed, component/helper symbols present]** The inventory is a permanent slot array of `ST_ItemData`. Empty slots use `HasItem=false`. Selling clears a slot; it must not remove its array index and shift the remaining items.

- `Initialize_Inventory` establishes slots. The older project bible described main inventory capacity 20; inspect current component defaults before using that number as a balancing assumption.
- **[September 30 screenshot + Seth's test report]** Seth implemented `AddItem` full-payload preservation: ItemToAdd is copied into ItemToStore, Set members in ST_ItemData changes only HasItem=true, and Set Array Elem stores that copy. Screenshot confirms existing empty-slot search, fixed index, Size to Fit unchecked and AddedItem=true/break after insertion. Seth reports testing works; no independent compile/runtime or field-by-field transfer verification by Codex. The earlier partial Make-struct defect is repaired. Separate acceptance issue remains: AddedItem is internal, no success output is shown, and the last inspected catch boundary calls UpdateCatchJournal unconditionally. See the September 29 historical audit in `CATCH_JOURNAL_BACKEND_AUDIT.md`.
- `Has room` checks empty slots, not `Items.Length < MaxSlots` on the already allocated array.
- `RemoveItemAtIndex`, `ClearItemAtIndex`, and `SetItemAtIndex` are current symbols; emptying a slot uses a default item at the existing index.
- `MoveOrSwapItem` supports slot moves/swaps. Same slot and empty source are no-ops. The player’s `GetInventoryComponentByContainer` chooses main/cooler for cross-container operations.
- `ExpandInventorySlots`, `GetItemsForSave`, and `LoadItemsForSave` are existing helpers.
- `WBP_Inventory.RefreshInventory` and `RefreshCoolerGrid` rebuild the relevant display. Slots preserve the real array index and container type.
- `SellItemAtIndex` awards the item’s `SellValue`, clears that exact slot and refreshes. `SellAll_InventoryFish`, `SellAllCoolerFish`, and both total-value queries exist.

Cooler tiers and capacity variables include `HasCooler`, `CoolerTier`, `CurrentCoolerUpgradeTier`, `CoolerMaxSlots`, `CoolerMaxTier`, and tier-specific capacities. The three-tier design uses 10 → 15 → 20 slots in the documented working approach; verify authored values before changing it. The old four-stage 25-slot guide is historical. Avoid duplicating or conflating the multiple existing tier variables during save/load.

`AutoFishingEnabled` and `AutoFillCoolerUnlocked` are current variables, but unlock rules, actual item routing and save coverage need an Editor check. Do not claim automatic cooler routing is guaranteed from these names alone.

Important regression rule: moving fish between inventories, selling, refreshing UI, or restoring saved inventory is **not a new catch**. None should increment the Catch Journal.

## 7. Shop and progression

**[Confirmed / Repository]** The existing buy/sell shop is already data-driven. Keep the sell side while extending buy behavior.

```text
DT_ShopEntries
  → WBP_ShopMenu.BuildBuyShop
  → ShouldShowShopEntry
  → AddBuySlotFromEntry
  → WBP_ShopBuySlot holds ST_ShopEntry + FishermanRef
  → BP_Fisherman.TryPurchaseShopEntry
  → TryPurchaseRod / TryPurchaseBait / BuyOrUpgradeCooler / BuyOrUpgradeFishingPass
  → successful purchase dispatcher → rebuild/refresh menu
```

The current layout uses a scrolling **vertical list** (`VerticalBox_BuySlotContainer`), superseding the older WrapBox/card-grid steps. `OnPurchaseSucceeded` was the established dispatcher contract; check its exact current binding in the Editor if altering refresh behavior. `RefreshShopMenu` is present. Do not introduce a separate `WBP_ShopBuyPanel` simply because an older assistant proposed one.

Ownership/progression queries belong to the player, not hardcoded widget state. Current helper spelling is **`GetNextFishPassUpgradeID`**, plus `GetNextCoolerUpgradeID`, `GetCurrentFishingPassTier`, and `GetCurrentCoolerUpgradeTier`. Older instructions used `GetNextFishingPassUpgradeID`.

Only the next valid pass/cooler tier should appear; after a purchase, that listing advances. At the final tier, preserve the owned/maxed representation where configured (`bHideWhenOwned=false`); `bIsMaxed` is passed to the reusable slot for its display. Player state determines maxed/owned status, not a universal static table flag.

**Purchase price fix confirmed August 5:** the amount deducted comes from `ST_ShopEntry.CostScales`, matching the displayed price. Old `BasicPassPrice`, `Tier2PassPrice`, `BasicCoolerPrice`, etc. still exist in player metadata. Their presence does not prove they still control purchases; audit references before removing them.

Identity conventions:

- `EntryID`: shop listing identity.
- `LinkedRowID`: purchased product / upgrade identifier. **This remains the current name.** `ProductID` was only suggested.
- `UpgradeChainID`: links progression listings such as Cooler/FishingPass.
- BasicRod is the fallback/default equipment identity; SturdyRod is the discussed +1 upgrade. Use the actual row values for costs/bonuses.

Gate, pass and purchase progression is established. `OpenedGateIDs` and saved open/unlocked IDs exist. Check loaded gates against saved progression, and test that a loaded max-tier cooler does not show Tier1 for sale.

## 8. Rods and roll bonuses

**[Confirmed / Repository]** Durable rod state is `OwnedRodIDs` plus `EquippedRodID`; `EquippedRodData` is `ST_FishingRodData`, loaded from `DT_FishingRods`.

`InitializeRodSystemAfterLoad` ensures BasicRod ownership/fallback, validates the equipped ID, and calls `EquipRodByID`. Equip updates row data and `RodCatchBonus`, then calls `RecalculateFishingStats`. Recalculation recomputes persistent/base bonuses; it must not repeatedly add a rod bonus onto the previous total.

`GetCurrentCatchBonus(RollContext)` calculates the **usable bonus for this roll** from the persistent base, conditional equipment effects, `ActiveOneCatchRollModifiers` and applicable bait. `EvaluateCatchBonusModifier` implements condition checks. The popup’s `RefreshCurrentCatchBonus` should display the same result the roll consumes, including immediately after bait confirmation. Verify current formula and unused legacy `BaitCatchBonus` paths before editing.

The held actor is now **`BP_FishingRodMesh`**, with `EquippedFishingRod` on the player. Its current functions include `SetRodMesh`, `ApplyRodDefaultPose`, `ApplyRodCorrectionPose`, and `ApplyRodCatchCorrectionPose`. The confirmed visual approach spawns/obtains the shared actor, applies `EquippedRodData.RodMesh`, attaches to the hand socket (`SOC_FishingRod` appears in metadata), and applies the appropriate pose. Do not revert to one Blueprint class per rod just to change a mesh.

Animation uses separate cast, waiting and catch montages. The waiting montage loops a section internally until the next action overrides it; do not repeatedly replay it through a Delay. The loop seam/pop, mesh alignment, IK, bobber/hook and fishing-line polish are separate visual work, not a reason to rebuild the catch architecture.

**2026-09-28 animation pilot [Headless inspection / preview pending]:** Saved `BP_Fisherman` defaults use `SK_Chr_Gentleman_01` with `ThirdPerson_AnimBP` on the Polygon Pirates UE4 skeleton. The inspected `AM_CatchFish` and `Core/Animations/AS_CatchandecRast` use the FishingAnimPack UE5 skeleton. This does not establish the live pawn's mesh overrides or runtime montage routing. Existing hand/elbow targets and fishing Two Bone IK remain unchanged. Seth authorized headless scripting, but no mouse/Computer Use.

Created three isolated assets in `/Game/Core/Animations/CodexRetargetTest`: `IK_Gentleman_Codex`, `RTG_FishingPack_To_Gentleman_Codex`, and `AS_CatchandecRast_Gentleman_Codex`. The retargeter reuses the pack's source IK rig with Quinn as source preview, exact chain mapping, aligned target pose, and disabled Run IK Rig operation; motion is baked into the target sequence. The test sequence retains 18.3 seconds and targets the Gentleman skeleton. At source time 1.0 s, headless hand-bone spacing measured Quinn 31.36 cm, original sequence evaluated on Gentleman 64.47 cm, and retargeted Gentleman 39.57 cm. These measurements demonstrate improvement, not visual grip correctness. No montage replacement, Tick removal, gameplay integration, visual preview or PIE validation performed. Next: Seth previews this isolated sequence; then inspect actual runtime animation routing and disable only redundant fishing IK for accepted retargeted clips. Cast/wait still need separate treatment.

Night bonuses and `SpotHasTag` are future-ready contracts. Seth deferred tag implementation, and the current roll context has no `SpotTags` member. Verify whether the condition reads tags from `FishingSpotRef`; do not claim a completed tag/night system or invent extra current context fields.

## 9. Bait system

**[Confirmed / Repository]** Bait is bought in the shop and consumed for a chosen D20 catch. It is not persistent equipped gear or an ordinary fish-inventory item.

| State / helper | Contract |
|---|---|
| `OwnedBaitCounts` | Name → integer count map |
| `CarriedBaitSlots` | Name array with **three permanent positions**, empty positions `None` |
| `ActiveRollBaitIDs` | Temporary activated bait for this roll |
| `InitializeCarriedBaitSlots` | Establish three slots; the historical length-zero purchase bug was fixed |
| `EnsureBaitInCarriedSlots` / `ClearBaitFromCarriedSlots` | Allocate a free slot or clear its value without shifting positions |
| `TryAddBait`, `GetBaitCount`, `GetBaitData`, `TryConsumeBait` | Existing ownership/data helpers |
| `CanActivateBaitForCurrentRoll` / `TryActivateBaitForCurrentRoll` | Validate ownership and effect-group conflict; consume once on confirmation |
| `GetActiveBaitEffectAmount(RequestedEffectType)` | Aggregate matching effects across active bait |
| `ClearActiveRollBaits` / `ClearOneCatchRollModifiers` | Clear temporary roll state |

Inventory bait slots show icon/count and tooltip only. Popup bait slots can be clicked; `WBP_BaitSlot.bIsClickable` distinguishes contexts. `OnBaitSlotClicked` passes the ID to the popup. Its existing `Border_ConfirmBait` / `Button_ConfirmUseBait` handles confirmation. Cancellation spends nothing. Confirmation consumes one, updates count/slots, activates the effect, and refreshes the displayed roll bonus.

One effect per group per roll: CatchBonus + Misc can coexist; CatchBonus + CatchBonus and Misc + Misc cannot. Consequently **Shimmerworm + Gambeetle is blocked**, while TastyBait can combine with either. Current ownership limit is three of each authored bait; do not confuse quantity three with three distinct carried bait types.

| Bait row | Accepted behavior |
|---|---|
| `TastyBait` | `CatchRollBonus`, +1 to this roll |
| `Shimmerworm` | `SellValuePercentBonus`, +25% to the successful catch’s final sell value |
| `Gambeetle` | `RollMarginScalesChange`, amount 1: gain/lose Scales according to final roll margin |

Shimmerworm applies on the successful popup outcome after base/quality value creation and before inventory insertion: `Round(SellValue × (1 + amount / 100.0))`. Preserve all other fields of the item. Do not put popup-selected bait into the unconditional fishing-spot builder or multiply by weight.

Gambeetle applies once after computing the final roll and before success/failure branching:

```text
delta = (FinalRollWithBonus - RequiredDC) × effectAmount
Scales = Max(Scales + delta, 0)
```

It affects currency on **both success and failure**, not catch bonus or fish sell price. Show its UI when the effect is active, including an equal-DC zero result; hide when unused. `HorizontalBox_GambeetlePopup` and `Text_GambeetleScales` exist. The historical text bug used Set Tool Tip Text instead of Set Text and was corrected.

The generic effect getter must initialize its running total to zero, examine the full loop, and return from Completed. Earlier early-return/nonmatching-bait behavior was fixed. Clear active effects before a fresh roll and after all success/failure/cancel/load paths, after their effects have been applied. Already-consumed bait is not automatically refunded on an abandoned roll; confirm refund design before adding one.

## 10. Interaction, menus and audio

### Interaction and menu state

**[Seth confirmed, September 29]** The interaction-trace Cube is attached to the camera and rotates with it. It intentionally provides a camera-directed trace independently of character-mesh facing, fixing an earlier character-facing targeting issue. Do not describe this setup as character-facing or recommend changing its orientation without evidence of a new problem. The menu/focus/input-gating findings are separate from trace direction.

**[September 29 targeted exported-graph diagnosis; no runtime test or fix]** Inventory opening assigns InventoryWidget and CurrentOpenMenuWidget and uses GameAndUI input. The fishing spot's D20 opening path removes InventoryWidget and clears that reference, but does not clear/replace CurrentOpenMenuWidget; popup opening/closing separately controls bFishingRollPopupOpen and input/cursor. E's inspected path checks FocusedInteractable validity then sends OnInteract, without a menu gate. UpdateInteractionFocus traces from Cube forward 200 units, checks interface and changes focus only when the target changes; it has no entry menu gate. Proposed repair: consistent menu ownership plus a shared permission check for new world interactions, prompt visibility and E dispatch; clear focus/hide fishing prompt on menu open and recompute on close. Seth wants existing fishing to continue during inventory use but no new cast while inventory remains open. Preserve ongoing catch resolution; do not cancel/pause fishing merely to suppress interaction. Trace-based targeting itself is not established defective. These assets' on-disk timestamps precede the inspected export; unsaved edits remain outside evidence.

**[Confirmed / Repository]** `BP_Fisherman.UpdateInteractionFocus` performs the established short forward trace (roughly 200 units in the discussed setup), stores `FocusedInteractable`, and calls `BPI_Interact.SetInteractionFocused` when focus changes. E interacts with that stored target. Clear the old prompt/target with `ClearInteractionFocus` when focus is lost or gameplay state makes interaction invalid. Prompts and the E target must refer to the same actor.

`NearbyFishingSpots`, `RegisterFishingSpot`, and `UnregisterFishingSpot` also exist for proximity handling. Keep overlapping-spot registration separate from trace focus; one spot’s EndOverlap must not erase every still-nearby spot. Debug traces should be disabled in the playtest build.

`CloseMenuAndReturnToGame` exists in inventory/shop. Pause has `ResumeGameFromPauseMenu`. Menu closure must restore game input, unpause where appropriate, clear UI-open state, hide the cursor and restore player focus. `TeleportPlayerToStart` is the current unstuck helper. Reset transient fishing/positioning state before teleporting. Preserve hover tooltips while ensuring display-only inventory bait cannot steal activation/focus.

### Audio

**[Repository]** `BP_AudioManager.OceanAudio` currently references **`SQue_Ambient_Ocean_02`** under `Content/Core/SFX_Music/CUE/AmbientCues/`. Do not replace this name with the earlier hypothetical `SCue_OceanLoop`.

**[Confirmed]** The ocean bed is intended as a continuous global, nonspatial ambience loop. Localized splashes/creaks use placed ambient sources, attenuation and randomized delays. Continuous-wave looping and sporadic cue looping are different configurations; avoid individually looping every intermittent sound.

Current sound classes are **`SC_Master`, `SC_SFX`, `SC_UI`, `SC_Music`, and `Ambience`**. Ambience/SFX/UI reference the master in metadata. `SC_Music` exists but its parenting/routing needs verification; do not assume all category routes are finished. Audio settings sliders, SoundMix volume controls and saved preferences were proposed; no corresponding settings/SoundMix implementation was found.

Footsteps were confirmed working: `Footstep_L` / `Footstep_R` animation notifies → player `PlayFootstep` with `foot_l` / `foot_r` socket position → randomized wood cue at that location. `SCue_Footstep_Wood` exists.

Fishing action notifies discussed: `Cast_Start`, `BaitSplash`, `Start_Reeling`, `Line_Tension`, `Finish_Catch`. Player `PlayFishingActionAudio` stores `CurrentFishingActionAudio`, fades a valid previous component and spawns the next attached sound. Both valid and invalid previous-component paths must spawn the requested sound. Closely spaced clips cutting each other off remains a regression check.

The popup separately holds `D20RollingAudio`; stop/fade it at roll completion. UI cues include the actual assets **`SCue_InventoryOpen`** and **`SCue_InventoryClosing`**, plus purchase, click and failure cues. Inventory close being silent and empty AmbientSound sources were reported; see the issue ledger rather than assuming completion.

## 11. Catch Journal — current status and accepted design

### What is already present

The official player-facing name is **Catch Journal**, covering fish and treasure. **[Repository]** The September 6 commit added the generic record/category assets and changed player, save, catch, inventory and related UI assets:

- `ST_CatchJournalRecord` with `Discovered`, `TotalCollected`, `BestWeight`, `BestQuality`.
- `BP_Fisherman.CatchJournalRecords`, `UpdateCatchJournal`, and `GetFishQualityRank`.
- `BP_SaveGame.SavedCatchJournalRecords`, also referenced in `BP_Fisherman`.
- `ST_FishCatchEntry.JournalCategoryID` and `JournalSortOrder`.
- `ST_JournalCategoryData` and `DT_JournalCategories`, with `Pier_01` observed.

**[Confirmed]** The earlier fish backend tracked first discovery, total catches, best weight and quality. The repeated-first-discovery bug was fixed with an explicit false return on the existing-record path. **[Repository, 2026-09-28 native graph audit]** UpdateCatchJournal has fish/treasure eligibility, stable FishID lookup, new/existing record paths and rank-based best-quality comparison. GetFishQualityRank maps Valuable=5, Legendary=4, Rare=3, Common=2, Decent=1, Sickly=0. **[Seth's September 30 report]** Seth implemented the new AddItem Boolean result and gated UpdateCatchJournal with a Branch; he reports testing works. Current live graph and specific full-inventory/D20 test cases were not independently inspected by Codex. Earlier export shows the normal spot calls ShowCatchToast before AddCaughtFishToInventory; notification timing remains to repair.

**2026-09-28 saved-map audit:** 37 exact BP_FishingSpot instances in MainDock contain 17 unique eligible IDs (16 fish, EmeraldRing treasure). All 17 have blank category metadata in at least one occurrence; Catfish also has a Pier_01/sort 10 occurrence versus blank/sort 0 elsewhere. DT_JournalCategories contains only Pier_01. Unsaved Editor changes, subclasses and other maps were not covered. Category membership and the authoritative catalog approach remain undecided; do not infer membership from icon folder names.

**Current UI status:** no journal widgets or gameplay assets were changed by this audit. Available headless Python APIs lack the required Widget Tree authoring/general graph wiring; disconnected widget shells were deliberately not created. See `CATCH_JOURNAL_CHATGPT_HANDOFF.md` for staged manual implementation, verified paths and remaining decisions. Read-only inspection scripts are in `Scripts/Editor/CatchJournal`; reports are in `Saved/CodexCatchJournal`.

No `WBP_CatchJournal`, category/entry journal widgets, or separate journal toast widget were found. The 17-row `DT_CatchDefinitions` now supplies the editable catch name/icon catalog; the journal **backend foundation and catalog are present, while UI and persistence validation remain unfinished**.

### Record contract

**[Design / Confirmed fish behavior]**:

1. Use one record per stable `FishID`, regardless of catch quality. Missing key means undiscovered.
2. Journal eligible fish and treasure; exclude ordinary junk. Reject an empty/None ID.
3. On first accepted catch, set Discovered true and initialize count and applicable records.
4. On subsequent accepted catches, increment `TotalCollected`; fish retain maximum weight and highest quality according to **`GetFishQualityRank`**, not enum ordinal.
5. `record.Discovered=true` remains true permanently. The event/function output `WasNewDiscovery` is true only on that first catch, false on repeats.
6. Update exactly once after the actual inventory acceptance succeeds. Failed D20 rolls, rejected full-inventory results, display refresh, sales, inventory transfers and load must not count.
7. Selling a catch does not erase its journal history. Treasure uses `TotalCollected` as “Total Found”; it does not need weight/quality shown.

### UI Seth requested

**[Design — not yet a verified screen]** Open from an inventory button. Use a bounded window like the inventory/shop, with the environment visible around its edges.

| Screen | Required behavior |
|---|---|
| Category list | Treasure first, then titled pier categories. Show discovered/total counts to the right; white while incomplete, green when fully discovered |
| Category entries | Icons for discovered catches, silhouettes for undiscovered entries; clicking opens the shared detail view |
| Undiscovered fish detail | Silhouette; name `???`; Type Fish; Best Weight N/A; Best Quality N/A; Total Caught 0 |
| Discovered fish detail | Actual icon/base species name; Type Fish; best weight with lbs; best quality; total caught |
| Undiscovered treasure detail | Silhouette; name `???`; Type Treasure; Total Found 0 |
| Discovered treasure detail | Actual icon/name; Type Treasure; Total Found; omit weight and quality |

**Accepted layout, October 1:** one **`WBP_CatchJournal`** with three simultaneously visible columns: clickable categories on the left, the selected category's catch grid in the middle, and one shared selected-catch details panel on the right. This replaces the earlier three-state WidgetSwitcher proposal. Use reusable category/entry children; close/input behavior should reuse the existing menu pattern. Widget names remain proposed, not current verified assets. Seth approved the supplied wood/rope/parchment reference and requested rope OVER the top corner fittings and word labels for Best Quality instead of stars. All Piers is a virtual aggregate fish filter, alongside actual catalog categories; details use current labels and lbs rather than the reference's example Uncommon/kg/stars. Layered art and assembly guidance are under `ArtSource/UI/CatchJournalLayeredKit`; no widget import or graph authoring is implied by the art kit.

Static definitions must be separate from player records. An undiscovered entry needs catalog icon, type, category and sort order. **[Native catalog saved September 30; builder lookup reported working by Seth]** Seth created E_CatchType and ST_CatchDefinition. Codex imported `/Game/Core/Data/DataTables/CollectionLog/DT_CatchDefinitions` with 17 rows keyed by unchanged FishIDs, and added Treasure/Pier_02/Pier_03/Non_Exclusive to DT_JournalCategories, preserving its existing Pier_01 row. Fresh-process reload verified all 17 row types, category IDs, sort orders and icon paths, five category IDs and their order. Source snapshot: `ArtSource/CatchJournal/DT_CatchDefinitions_source.csv`; validation: `Saved/CodexCatchJournal/catalog_validation.json`. Seth manually integrated a `ResolveCatchPresentation` lookup into `BuildCaughtFishItem` and reports it works; Codex has not independently inspected the finished graph or run the catch cases. The journal UI does not read the catalog yet. Existing held/saved item snapshots retain prior presentation; catalog name/icon changes are intended to affect new catches. Fish_/Treasure_ ID renaming remains a separate migration decision. Do not reimport the source CSV after user edits unless intentionally replacing the native rows. A zero-entry category must not falsely display as complete.

**[September 29 inspection clarification]** The previously exported AddItem call node exposes no success/failure result pin. Its implementation and D20 award paths still need inspection before designing acceptance gating; do not assume an existing Success pin. No new Editor process or asset edits were made during the architecture review.

Requested toast text: **“Catch journal updated: [Fish Name]”**, with no extra record statistics. The trigger policy (first discovery only, also record improvements, or every accepted catch) was not finalized. Choose/document that small policy before wiring it; keep it separate from the normal catch toast.

Future reward hooks should detect a category’s incomplete → complete transition once, and keep completion separate from reward claiming. No reward system or saved claimed-reward schema is currently established. Build a small extension point when needed; do not grant repeated rewards on UI refresh or silently add a full rewards system to this milestone.

## 12. Save and load flow

### Existing flow — preserve it

Seth described this working flow September 4; matching helper names are present:

```text
Save button
  → BP_Fisherman.SavePlayerGame
  → Create Save Game Object (BP_SaveGame)
  → FillSaveObjectFromCurrentState
  → Save Game to Slot

Load button
  → RequestLoadPlayerGame
  → set pending slot/user and load-after-level-open flag
  → Open Level / reset to start
  → new world sees flag and clears it
  → default setup (rod, bait, movement)
  → LoadPlayerGameFromSlot
  → Does Save Game Exist
  → Load Game From Slot
  → Cast BP_SaveGame
  → ApplyLoadedSaveData
      → ResetTemporaryStateForLoad
      → validate LoadedSave
      → ApplyCoreSaveData
      → RefreshInventory
```

`BP_FishingGameInstance` stores `bLoadSaveAfterLevelOpen`, `PendingSaveSlotName`, and `PendingSaveUserIndex`. `MainSave` is an observed slot default. Treat the above as the described flow, not a verified execution graph. Especially check post-load rod/bait initialization: applying defaults before loading is fine for baseline setup, but reconstruct equipment/stats **after** saved IDs are restored. Do not let a later initialization reset loaded bait slots, inventory, journal or capacity.

### Current saved fields

All of the following names are present in `BP_SaveGame`:

| Group | Fields |
|---|---|
| Version/currency/world | `SaveVersion`, `SavedScales`, `SavedMapName` |
| Pass/access | `SavedFishingPass`, `SavedUnlockedPierIDs`, `SavedOpenGateIDs` |
| Item arrays | `SavedInventoryItems`, `SavedCoolerItems` |
| Cooler state | `SavedIsCoolerUnlocked`, `SavedCoolerTier`, `SavedCoolerUpgradeTier`, `SavedCoolerMaxSlots` |
| Bait | `SavedOwnedBaitCounts`, `SavedCarriedBaitSlots` |
| Rods | `SavedOwnedRodIDs`, **`SaveEquippedRodIDs`** (current spelling; verify its actual type despite the plural name) |
| Journal / older discovery | `SavedCatchJournalRecords`, `SavedCaughtFishIDs` |

`SavedCatchJournalRecords` is the durable journal map counterpart. **[Repository, 2026-09-28 native graph audit]** Both assignments and their execution links are present: player CatchJournalRecords → saved map in `FillSaveObjectFromCurrentState`, saved map → player CatchJournalRecords in `ApplyCoreSaveData`. Actual disk save/restart/load remains untested. Reuse this map; do not add duplicate journal save fields. `SavedCaughtFishIDs` may be legacy/other progression; inspect references before replacing/removing it. Also inspect the two cooler-tier save fields for duplicated or stale state.

Do not save actor/widget references, active fishing state, current candidate roll, `ActiveRollBaitIDs`, one-catch modifiers, interaction focus or playing audio components. Rebuild transient equipment/UI from durable IDs/data. `ResetTemporaryStateForLoad` must clear fishing, movement-to-spot, open popup/menu state and temporary effects so loading cannot leave the player stuck.

Save correctness matters, but old development and friends-playtest saves are disposable after they have served their test purpose. Preserve compatibility by default while a feature is in progress, but a deliberate reset or migration is acceptable after discussion when it produces a cleaner system. Document any `SaveVersion` change or intentional incompatibility before changing saved structs, IDs or enums. When compatibility is retained, missing journal data in an older save should produce an empty journal without discarding the rest of the save; validate IDs and preserve valid inventory contents when restoring capacities. Renaming user-defined structs/fields is not automatically proven safe for old saves.

**[Historical proposal]** A nested `ST_PlayerSaveData` could organize the many assignments. It is not present and was deferred. Complete journal persistence using the existing helpers first; do not make a save-system rewrite a prerequisite.

## 13. Completed work versus unfinished work

“Completed” here means confirmed during development and supported by the current files; it is not a fresh regression-test result.

| Work | Status |
|---|---|
| Species + quality item building, shared inventory/shop/toast payload | Established; current quality label/gate mapping needs reconciliation |
| D20 popup/context handoff and normal versus gated catch paths | Established; preserve the split |
| Fixed-slot inventory, selling, cooler expansion and cross-container helpers | Established; test restored tier/capacity consistency |
| Generated shop buy listings, upgrade-chain filtering and success refresh | Confirmed working |
| Displayed versus charged purchase cost | Confirmed fixed August 5 |
| Rod ownership, equip/stats and shared-actor mesh approach | Confirmed; alignment/animation polish separate |
| Three bait slots, purchase/consume/confirmation/group stacking | Confirmed; focus/tooltip regression remains |
| TastyBait, Shimmerworm percentage effect, Gambeetle margin currency | Confirmed; regression test both roll outcomes |
| Focus-based interaction prompts and E target | Confirmed working August 3 |
| Save/reopen/load/core-apply architecture | Described as working; new journal round trip unverified |
| Fish journal tracking and repeated-discovery fix | Confirmed; generic assets/save field now present |
| Catch Journal complete screen and static catalog | Catalog saved/verified; Seth reports new-catch lookup working; journal screen unfinished |
| Footsteps and ocean looping | Confirmed working; cue routing/timing still check |
| Small quests, fishing contest, journal rewards, shack, night progression, main menu/cinematic | Planned, not verified implemented |

## 14. Known issues, risks and technical debt

Keep reported symptoms distinct from newly verified bugs. Do not silently mark these fixed after an unrelated “everything works” message.

### Seth's September 29 cleanup and testing clarifications

- `WBP_ShopMenu_Working_Backup` and `BP_CodexRotationTest` are intended for eventual deletion. No deletion performed; inspect references and handle cleanup as a separate scoped step.
- Old fishing-spot redirector paths require investigation, not blind filesystem deletion. Redirectors can preserve references to assets moved/renamed in Unreal.
- `SavedCoolerUpgradeTier` may be a leftover from the older cooler upgrade system, which Seth changed to align with the fishing-pass upgrade approach. Hypothesis only; verify consumers before removal.
- `FishermanTest` is a possible deletion candidate, pending Seth's inspection and reference checks. Not approved for deletion yet.
- `RequiredPassTier = 0` on spots is intentional debug configuration so Seth can test without repeatedly buying passes. Do not treat it as a bug or change it automatically. Restore intended access requirements before a release/playtest that tests progression.
- Existing manually created development save files are disposable. Seth does not require compatibility with those old files and does not need migration machinery solely to preserve them. The save/load system itself must still function correctly and be tested. Record any deliberate reset, ID/schema or SaveVersion change; this clarification is not an instruction to delete saves immediately.

| Priority | Issue / evidence | Next check |
|---|---|---|
| High | Journal save assignments verified September 28; round trip remains untested | Save/restart/load fish and treasure records; check accepted-insertion timing |
| High | Current six quality labels differ from older five-tier instructions; `TrophyOrLegendaryCatch` name remains | Inspect gate flags, rank helper and all enum switches; preserve current values |
| High | Runtime journal filtering, dynamic categories and category counts work by Seth report | Test new/repeat discoveries, completion and save/load; finish entry states/details |
| Medium | Multiple cooler tier variables/save fields; Tier2 loading previously restored items but shop showed Tier1 | Save/reload each tier; compare capacities, ownership, next upgrade and maxed UI |
| Medium | Default/equipment setup was described before save application | Ensure saved IDs/counts are restored before final equipment/stat/slot reconstruction |
| Medium | Display-only bait stole focus/clicks in inventory; tooltips are required | Test keyboard/mouse navigation and hover while `bIsClickable=false`; do not disable all hit testing and lose tooltip behavior |
| Medium | Inventory closing cue reported silent; no explicit later fix located | Test actual `SCue_InventoryClosing` playback, UI class, close event order and paused behavior |
| Medium | Closely spaced fishing audio clips could overwrite each other; older valid-component branch missed spawning | Verify both spawn paths and notify timing; change concurrency only for intentional overlap |
| Medium | Pause/unstuck could leave/re-show cursor on subsequent clicks | Test shared resume cleanup and teleport while paused/fishing/UI open |
| Low | Empty AmbientSound sources produced editor warnings | Inspect placed sound actors and remove/configure only confirmed empty sources |
| Low | Dirty-water overlay disappearing by angle / wave surface poking through was reported; water assets changed September 6 | Reproduce before diagnosing current material/plane settings |
| Low | `SortOtder` typo; `SaveEquippedRodIDs` wording; old FishJournal comments and old-price variables | Treat as naming/reference cleanup with save/schema considerations, not silent renames |
| Low | Backup shop widget and redirectors remain tracked | Audit references; use Editor fix-up workflow when appropriate; do not manually delete redirectors blindly |
| Low | `.gitattributes` contains only `* text=auto`; no explicit LFS rules for large Unreal assets | Review repository storage strategy separately; no history rewrite or LFS migration was performed |

Past resolved bugs to remember as regression cases: stale struct/Get pins caused UI handoff errors; zero sell values came from a stray ×0; empty bait array blocked purchases; a generic bait loop returned too early; existing species falsely returned new discovery; Gambeetle UI changed tooltip text instead of displayed text. Reconnect/refresh stale Blueprint struct nodes after schema edits before blaming saved data.

## 15. Current task and next recommended steps

**Canopy gust/flap revision, September 30:** Implemented on the existing generated variant after Seth confirmed Editor closed. Front/back flaps have separate G/B weights with loose side corners freed; broad fold-centered sway replaces traveling edge waves, plus subtle trailing flex. Added Gust_Speed=1, Speed_Variation=0.45, Strength_Variation=0.4, Gust_Offset=0, Flap_Swing_degrees=7. Integrated multi-frequency gust timing avoids phase jumps; variation is smooth deterministic motion, not true randomness. Preserved Seth's MI overrides (Overall_Strength=2, Movement_Speed≈1.217, Cloth_Ripple_cm=0.2336, Edge_Flutter_cm=5, Wave_Size_cm=500, Phase_Offset≈6.283). Earlier WPO UseConstant repair remains applied; collision stays CTF_USE_COMPLEX_AS_SIMPLE. Fresh reload and offscreen three-time front renders passed without shader errors; round-trip positions/masks passed with fixed geometry weights exactly zero. No PIE walk-through or packaged test. Seth visually approved the motion, then requested shared front-to-back wind direction. Follow-up changes only two shader lines: rear uses the front's swing sign/phase and both share the trailing-flex direction, so front goes back/down while rear goes back/up on the forward stroke. Mesh and MI files verified byte-identical; settings/collision preserved. Next: Seth checks the directional adjustment in-game.

**Canopy assets:** `/Game/Core/Environment/CanopyMotion` contains `SM_Canopy_GentleMotion`, `M_Canopy_GentleMotion`, `MI_Canopy_GentleMotion`. Current source: `ArtSource/CanopyMotion/GustRevision`; tuning guide: `ArtSource/CanopyMotion/README.md`. Geometry remains 1,263 vertices/2,482 triangles; cloth 622 vertices, supports 641. R=main cloth/G=front flap/B=back flap; rigid supports zero. Bounds extension 30 cm. Original mesh, shared palette and maps untouched. No wind actor, rig, gameplay Tick or C++. Prior asset backups: `Saved/CodexCanopyInspection/GustRevision/Before`; verification: `GustRevision/` and `RenderGusts/` under the same inspection folder. Launch-only writable DDC settings do not alter project configuration.

**Current skeleton NPC status, September 30:** Isolated native import completed in `/Game/Core/NPCs/SkeletonNPC_ImportTest`: `SK_PierSkeleton_Test`, its separate `SK_PierSkeleton_Test_Skeleton`, three flat materials, `A_PierSkeleton_SeatedIdle_Test`, and `A_PierSkeleton_Exit_Test`. Fresh-process reload verified all dependencies/material assignments and 61 finite pose samples per animation on the imported mesh (43 bones including root). Idle imports as 7.6833 seconds; exit as 5.3000 seconds. FBX source idle was 7.68 seconds despite earlier eight-second descriptions. Import uses 60 fps with endpoint snapping; no additional playback speed multiplier. Initial import's unsaved skeleton, unassigned material slots and frame-boundary failures were repaired only in this folder. Evidence: `Saved/CodexSkeletonImport/saved_validation.json`. Commandlet returns nonzero because sandboxed DDC is unavailable; explicit validation completed successfully using memory-cache fallback. No visual Unreal playback, PIE, packaged build or Manny retarget test. Existing gameplay/map/player assets untouched.

**Latest approved source:** `ArtSource/SkeletonNPC/StandAndStepOff06_Polish` adds right shin/ankle follow-through during frames 17–36, a subtle 2.3 cm pre-hop squat, breath gesture, and 1.32x original speed (approximately 5.303 seconds). Cleaned mesh/idle: `ArtSource/SkeletonNPC/Revision04_Cleanup`. Previous versions retained. Blender's 169 finite poses and fixed squat foot targets checked; no new full collision sweep. Root remains stationary in Unreal while pelvis carries travel/fall: this is not capsule-moving root motion. Next: visual preview and pier alignment, then separately agree/build the NPC's idle timer, exit playback, splash/despawn/respawn behavior. Manny animation reuse still needs retargeting; do not assign the player's existing skeleton directly. See `ArtSource/SkeletonNPC/UNREAL_IMPORT_HANDOFF.md`.

**Character design retained:** Gentleman's approximate scale, more upright edge-supported hands/slight slouch, NPC-only 88%-length arm rest chains/lowered shoulders, smaller natural skull/sockets, no cheek or rear-neck projections, flat near-white bone and gold bracelet; no hat. Believable stylized anatomy takes priority over realism. Gentleman-derived hierarchy is not a drop-in Manny skeleton. Gameplay task below remains paused.

**Current task:** Native catch catalog and five category rows saved and verified September 30. Seth manually wired `BuildCaughtFishItem` to a stable-ID name/icon lookup with spot fallback and reports it works; Codex has not independently inspected the final graph or run normal/D20, inventory/toast, or save/load tests. October 1: Seth approved the three-column reference layout and requested a layered UMG art ZIP. Seth has manually assembled the three-column shell/title and accepted the replacement frame after setting its Texture Group to UI. Designer screenshots now confirm the close button and five category instances (All Piers, Treasure, Pier 1–3). Seth reports label alignment repaired and per-instance icon tint working; count translation Y=-5 retained. Seth accepted 180x190 catch tiles in a three-column scrolling grid: ScrollBox_Catches X365/Y250, 570x490, Z10; Grid_Catches padding4/6/4/6. Icons use Scale To Fit with native texture proportions; names use font20, AutoWrap off, WrapTextAt168 in a fixed168x70 area, directly parenting text without a name ScaleBox; icon area height104. Runtime catalog tiles now build and category filtering is user-confirmed. Seth confirmed explicit wrapping fixes flicker/overflow, and adjusted ScrollBox height490 to prevent lower tile cutoff. Headings, splash and detail-stat shell are now visually confirmed. October 2: Seth confirms CategoryID/OnCategoryClicked setup completed; screenshot verifies five OnInitialized bindings targeting category children and HandleCategoryClicked delegate. Seth reports journal category buttons return expected IDs in-game on October2, confirming dispatch/bind/handler path and a working test launch. Close/cursor/input restoration not yet reported tested. Screenshots verify existing OpenInventory creates widget, assigns CurrentOpenMenuWidget, adds to viewport, shows cursor, sets GameAndUI/focus. CloseMenuAndReturnToGame removes current widget via CloseCurrentOpenMenu, restores GameOnly/cursor. Current test launch/category filtering/runtime grid work by user report. Left buttons have been moved into ScrollBox_Categories → VerticalBox_Categories and still filter correctly. October 5: dynamic categories now build from DT_JournalCategories through BuildCategoryList, SortCategoryList and AddCategoryButton, with virtual AllPiers and per-created-widget dispatcher binding. Table icons and Non-Exclusive label are fixed. IsCatchDiscovered reads the existing record map (Found AND Discovered, false for invalid FishermanRef). GetCategoryCounts iterates catalog rows, counts category members and unique discovered IDs; AddCategoryButton formats its outputs into CategoryCountText. Seth reports displayed numbers are correct. Independent compile/runtime/save tests and repeat-catch count regression remain unverified. Future board multi-menu launch deferred. Seth also confirms WBP_JournalEntry discovery presentation works: exposed IsDiscovered is passed from IsCatchDiscovered during grid creation; PreConstruct selects CatchName or ??? and tints the species texture white or opaque black to preserve its alpha silhouette. Next: entry click dispatch and real shared detail data; completion colors and inventory launch remain pending. Current FishIDs/saved keys are unchanged; Fish_/Treasure_ renaming and save reset/migration deferred. The animation pilot remains paused and existing IK active.

**UI visual direction accepted September 30:** Seth approved cohesive Catch Journal, shop, inventory and catch-toast concepts using simplified low-poly dockwood, warm parchment, restrained rope/metal and marine-teal selected states. A contact sheet and 12 separate transparent concept PNGs are packaged with a usage guide at `ArtSource/UI/CozyHarborUIConceptKit.zip`. This is art source only; no textures were imported into Unreal, UMG widgets changed, or gameplay/UI behavior validated. The generated mockups contain illustrative names/counts and must not be treated as authoritative gameplay schema.

**Next gameplay milestone:** make the loop more meaningful by completing the Catch Journal as the first clear goal/collection layer, then use that foundation to support short quests and further progression.

1. **Inspect and verify the existing journal backend/save wiring.** Open `UpdateCatchJournal`, `GetFishQualityRank`, `AddCaughtFishToInventory`, `FillSaveObjectFromCurrentState`, and `ApplyCoreSaveData`. Resolve the current quality labels and success timing. Reuse the existing saved map. Verify both fish and treasure, an empty ID, repeats and failed/full-inventory outcomes.
2. **Establish the static catalog and category contract.** Use stable IDs and the current category/sort fields; include undiscovered entries, Treasure and actual pier membership. Do not duplicate species definitions without a single authoritative edit location.
3. **Build the minimal journal UI** described in section 11, including one reusable detail screen, inventory launch, back/close, silhouettes and completion counts. Make adding an entry/category data-driven.
4. **Wire the short journal toast and reward extension point.** Finalize toast trigger policy. Keep reward claiming outside this feature until requested.
5. **Run a focused regression pass**, then document verified results and actual changed assets. Do not call the journal complete merely because its map exists.
6. **After journal completion:** design one small arrival/intro or fish-delivery quest and the minimum reusable Blueprint quest contract it genuinely needs, followed by a balance-data export and playtest pass. Fishing contest, shack/night content and cinematic can follow; do not open all of those systems at once.

### Acceptance checks for that milestone

- First fish: one record, correct count, weight/quality and new-discovery result.
- Same fish with another quality: same key; count increases; best records never regress; no repeated first discovery.
- Treasure: correct ID/count; no fish-only detail fields. Junk: excluded.
- Normal and successful D20 catches: update once after accepted insertion. Failure/full inventory: no journal increment.
- Sell/move/refresh/load: no extra count; selling preserves discovery.
- Save, close/reopen the level/game, load: journal, Scales, inventory/cooler, capacities, rod and bait restore together.
- If pre-journal save compatibility is retained: the rest of the save remains usable and the journal begins empty. If not, intentionally bump/reset and document the decision.
- New game: no previous save’s journal leakage.
- Category totals include undiscovered definitions, deduplicate correctly and turn green only at full discovery.
- Undiscovered details conceal names/records; discovered fish/treasure show the specified fields.
- Close/back/input/cursor behavior works by keyboard and mouse, including from inventory.
- Journal edits do not regress shop costs, bait confirmation/group conflicts or Gambeetle success/failure effects.

## 16. Historical / obsolete approaches

| Historical name or approach | Current truth / disposition |
|---|---|
| Fish Collection Log / Fish Journal; `ST_FishCollectionRecord`, `FishCollectionRecords`, `UpdateFishCollection`, `TotalCaught` backend member | Catch Journal; `ST_CatchJournalRecord`, `CatchJournalRecords`, `UpdateCatchJournal`, `TotalCollected`. UI still labels fish count Total Caught |
| Bonus Beetle | **Gambeetle**; roll-margin Scales gain/loss, not a +roll popup |
| ShinyBait / flat +5 value | **Shimmerworm**, percentage bonus in the successful popup outcome |
| Old weight-based sell-value roll | Species base value × quality multiplier; weight does not affect price |
| Common/Uncommon/Rare/Trophy/Legendary as assumed current enum | Current labels are Legendary/Rare/Common/Decent/Sickly/Valuable; inspect live gate/ranking |
| Per-rod duplicated actor classes (`BP_BasicFishingRod` / proposed `BP_SturdyRod`) | Active shared held actor is `BP_FishingRodMesh`; old names remain in metadata/history |
| Handwritten upgrade buttons, WrapBox grid, proposed standalone shop buy panel | Existing generated vertical buy list in the combined `WBP_ShopMenu` |
| `ProductID` as if a completed rename | Current shop field remains `LinkedRowID` |
| `CatchID`, `E_ItemType`, `DT_FishData`, `ST_PlayerSaveData` | Proposals, not current assets; introduce only deliberately if needed |
| `SpotTags` assumed present in the roll context | Actual context has three fields; tags were deferred |
| Always-visible overlap prompts while E used another target | Focus-driven prompt and interaction target; proximity array remains separate |
| `PlayCastAudio` / `CurrentCastAudio` | Current helpers are `PlayFishingActionAudio` / `CurrentFishingActionAudio` |
| `SC_Ambience`, `SCue_OceanLoop`, `SCue_InventoryClose` example names | Actual assets: `Ambience`, manager reference `SQue_Ambient_Ocean_02`, `SCue_InventoryClosing` |
| `GetNextFishingPassUpgradeID`, `WBP_SignFishIcon`, `InitializeInventory`, `TeleportToPlayerStart` examples | Current observed names: `GetNextFishPassUpgradeID`, `WBP_SignFishIcons`, `Initialize_Inventory`, `TeleportPlayerToStart` |
| Old four-tier cooler guide / maximum 25 slots | Current discussed and observed shop progression has three tiers; verify actual capacities |

Current redirectors include `Content/Core/FishingSpot/BP_FishingSpot.uasset`, `Content/Core/FishingSpot_OLD/BP_FishingSpot_C.uasset`, the old Core/Interactables game-message path and ThirdPerson shop-NPC paths. The active paths are listed in section 3. `WBP_ShopMenu_Working_Backup` is a retained historical backup; do not use it as the active architecture reference.

## 17. Sources and validation record

Primary project evidence reviewed:

- Local `OneMoreCast.uproject`, relevant `Config` startup/packaging settings, README, `.gitignore`, `.gitattributes`, current asset inventory and readable serialized fields/references.
- Live public GitHub repository verification on September 27, 2026: public `main` and the local checkout both pointed to `5eb4b78`. GitHub is the completed published checkpoint; active local work normally leads it until Seth publishes.
- Git commit `5a62259` (September 6): generic journal/category assets, player/save/fishing/UI and water updates. Commit `5eb4b78` (September 20): FishermanTest character assets and MainDock update.
- Full available text of **One More Cast 2**. Key explicit decisions: June 22 species/quality baseline and D20 ownership; June 30 roll context; July shop/rod/bait/audio work; August 3 interaction focus; August 5 pricing fix and game direction; August 29 journal categories; September 4 record fix, save flow and Catch Journal design; September 27 persistent-memory request.
- Existing root project bible, quick-context/prototype notes, cooler/shop/inventory guides and patch notes were read as historical supporting material. Their “current” titles do not override newer files or confirmations. The initial conversation’s attached file was unavailable; root documents supplied additional local context without assuming they were that exact attachment.

Original onboarding validation: local path/remote identity, public repository and matching published commit, local gameplay-content baseline, commit history, active/redirector distinctions, schemas/symbols, absence checks for proposed journal UI/catalog/save structs. **September 28 journal follow-up:** successful native graph exports and focused pin-connection audit of journal/save/menu wiring; category-table export; saved MainDock exact BP_FishingSpot-class catch-array export and deduplicated metadata report. This supersedes the original metadata-only limitation for those specifically inspected graphs, not the entire project. **Not performed for the journal:** asset compile, PIE, runtime/save round trip, audio playback or packaged build. No remote fetch/pull or journal asset changes.

When maintaining this document, replace each Verify item with a dated result only after checking the implementation. Keep a small changelog; Git retains detailed history. An uploaded ChatGPT copy is a snapshot: refresh it after local changes. Root `AGENTS.md` points Codex to this file; see `ONE_MORE_CAST_SETUP.md` for the setup workflow.

## 18. Changelog

- **2026-10-01:** Seth dropped all four corner ropes; title lashings stay. Generated a matching optional frame replacement (native1704x923, exact-slot1366x740 export) under `L:/Game Projects/One More Cast/Images/UI/UI Images/CatchJournal/FrameReplacement`, with prompt/source/settings. Verified PNG dimensions and transparent center; old frame retained. Seth subsequently imported it, corrected Texture Group to UI, and accepted its Designer appearance in a screenshot; runtime sharpness remains untested. Generated images should use Seth's Images directory, reusing suitable folders/subfolders. Next: replace Img_Frame brush at unchanged35/100,1366x740,Z20 and inspect before close button.

- **2026-10-01:** Screenshots confirm three parchment columns plus title/lashings in WBP_CatchJournal. Captured Seth's manual rope/text overrides: left rope 442/35, right 928.592224/35.684727 (both 62x155, Z40); title 537.508118/58.056973, 365x60, Z31, hvd_edding_Font size 50 and dark brown. Updated placement overrides; next corner ropes. Title now centered, so do not assume space for the earlier proposed fish emblem. Screenshot validation only; no independent compile/PIE.

- **2026-10-01:** Catch Journal Designer screenshots verify root Canvas → centered 1440x860 Size Box → inner Canvas, plus backing parchment/frame. Seth adjusted Img_Frame to X=35, Y=100, size 1366x740, alignment 0/0, Auto Size off, ZOrder=20; this supersedes original kit frame placement. Recorded `ArtSource/UI/CatchJournalLayeredKit/UMG_PLACEMENT_OVERRIDES.json` with proposed adjusted panel rectangles. Next: three parchment columns, then title/rope layers. Visual confirmation only; compile/PIE not independently run.

- **2026-10-01:** Repaired PolygonPirates character move after Seth closed Editor: 37 working character assets restored to the original character folder, 11 unreferenced stale mesh conflicts removed using native APIs, references and 11 physics preview paths updated. Backups hash-verified; final headless process exited 0 and verified all 37 reload/save operations, player mesh and reference integrity. Props/81 non-character pack assets unchanged; interactive Save All and PIE pending. No Git operations or UI control used for repair.

- **2026-10-01:** Seth accepted simultaneous category/grid/details columns for the Catch Journal reference, rope above corner fittings, and word quality labels. Created `ArtSource/UI/CatchJournalLayeredKit` with 23 transparent import PNGs, generation originals/prompts, assembled/contact-sheet previews, exact starting layout and manual UMG assembly guide. Inspected preview layering and repaired two malformed generated symbols; checked alpha/dimensions. No Unreal import, widgets, compile, PIE or save/load validation; next is manual widget construction and data wiring.

- **2026-09-30:** Created a labeled UI concept sheet and 12 individually named transparent PNG elements for the accepted visual direction, plus usage guide and ZIP under `ArtSource/UI`. Checked PNG dimensions/alpha and ZIP entry count. No Unreal import or widget changes.

- **2026-09-30:** Seth manually integrated the catch presentation lookup into `BuildCaughtFishItem` and reports it works. Final graph, full normal/D20 catch cases, and save/load were not independently checked. Next: journal UI/category counts.

- **2026-09-30:** Imported and saved 17-row DT_CatchDefinitions from Seth's new enum/struct; added four category rows while preserving Pier_01. Fresh Unreal process verified all IDs, types, categories, sort orders and icon paths. At import time, no Blueprint lookup, journal UI, catch runtime or save/load test had been run.

- **2026-09-30:** Accepted catalog approach with stable current FishIDs, proposed categories, and new-catches-only name/icon updates. Prepared 17-row source CSV and guarded one-time DataTable importer; validated unique IDs and icon file presence. No native catalog or gameplay wiring created. Manual enum/struct creation required by available Unreal Python authoring API.

- **2026-09-30:** Seth reports manual AddItem success output and BP_Fisherman journal Branch working. Codex did not inspect the updated graph or run tests. Next manual stage: move ShowCatchToast to the successful award path; prior export shows it precedes inventory acceptance in BP_FishingSpot.

- **2026-09-30:** Screenshot confirms Seth's manual AddItem full-payload copy/HasItem-only repair, retaining fixed-slot insertion. Seth reports successful testing; Codex did not run compile/PIE or independently inspect stored fields. Marked payload issue repaired; explicit success output and acquisition gating remain pending.

- **2026-09-30:** Aligned canopy front/rear swing and trailing flex to shared wind direction after Seth approved the rest of the motion. Saved generated parent material only; mesh and MI hashes unchanged. Headless save and fresh offscreen rear renders passed with no shader errors (`DirectionalWindBack`); in-game directional check pending.

- **2026-09-30:** Updated isolated canopy variant with separate front/back flap masks, broad coherent swing and smooth integrated gust speed/strength controls. Preserved user MI overrides and original assets/maps; backed up prior variant assets. Fresh-load, offscreen render and geometry/mask round-trip checks passed; PIE/collision walk-through remains untested.

- **2026-09-30:** Fixed canopy's actual no-motion cause: inherited WPO UseConstant=True ignored connected animation graph. Cleared flag via Unreal native property command and saved; fresh offscreen renders confirm distinct cloth poses at default amplitude. Verified complex-as-simple collision saved. No map/original changes or PIE walk-through; prior compile-only result was insufficient.

- **2026-09-30:** Responded to canopy's blocked opening/no-motion report. Verified original mesh uses complex-as-simple collision; attempted variant correction blocked by live Editor file lock, not saved. Original asset/map unchanged. Collision fix and motion diagnosis pending; asked for component WPO setting.

- **2026-09-30:** Created isolated canopy WPO mesh/material/instance with pinned support mask and six movement controls. Native material compile and fresh-load/round-trip checks passed; no original/shared assets or map changes. In-level visual/collision validation remains pending; tuning guide saved in `ArtSource/CanopyMotion/README.md`.

- **2026-09-30:** Inspected canopy via read-only Unreal FBX export and Blender geometry analysis/render. Found separately connected cloth geometry but shared palette material; recommended masked WPO on an isolated variant. No asset edits or motion validation.

- **2026-09-30:** Completed isolated skeleton NPC mesh/material/idle/exit import and repaired initial dependency/material/timing failures. Fresh Unreal process reloaded seven assets and sampled 61 finite poses per clip. Exit 5.30 s, idle 7.6833 s; stationary root/pelvis-baked travel verified. No gameplay wiring, Manny retargeting or visual/PIE test; existing player/map unchanged.

- **2026-09-29:** Saved exit pass 06 with right-foot/shin follow-through and extra pre-hop squat. Kept speed/breath and earlier files. Validated finite poses and planted squat foot targets; Unreal unchanged and untested.

- **2026-09-29:** Saved exit pass 05 with another 10% speed increase and a pre-hop inhale-like chest/shoulder gesture. Checked finite poses and unchanged lower-body matrices within tolerance; duration approximately 5.303 seconds. Prior versions and Unreal assets untouched.

- **2026-09-29:** Saved separate 1.2x-speed exit clip in StandAndStepOff04_Faster after Seth approved pass-03 motion. Verified identical pose curves/handles, effective 28.8 fps and 5.8333-second duration. Original clip/idle and Unreal assets unchanged; engine timing untested.

- **2026-09-29:** Created exit pass 03 with lateral weight shifts, overlapping upper-body movement and airborne follow-through. Verified 169 finite frames, idle-start match, unchanged rest rig, complete weights and sampled preview-deck lower-leg clearance. No Unreal changes; naturalness awaits Seth's review.

- **2026-09-29:** Revised exit animation in separate StandAndStepOff02 folder for smoother support transfer, knee paths, pier clearance, foot contact and tiny hop. Checked 169 frames, matching idle start, unchanged rig, reachable limb targets and zero sampled lower-leg deck-interior vertex hits. Original files retained; Unreal unmodified/untested.

- **2026-09-29:** Authored separate StandAndStepOff Blender/FBX clip and preview video. Preserved cleaned model and idle; checked 157 finite frames, exact seated-start match within tolerance, unchanged rest rig and final preview-water submersion. No unreachable generated limb targets. Unreal import/root motion/runtime integration not tested; pelvis-baked travel documented.

- **2026-09-29:** Saved separate Revision04_Cleanup Blender/FBX files after trimming 12 vertices from the overlapping pelvic-arch tips and capping the ends. No rig or animation changes; previous revision recoverable. Unreal unchanged.

- **2026-09-29:** Skeleton Revision04 adds edge-supported upright slouch, NPC-only shortened arms/lowered shoulders, rebuilt smaller-socket skull, flat ivory, removed cheek/neck projections, upper-body shifts and ankle follow-through. Prior versions and Unreal Content untouched. Blender loop/weight/FBX round-trip checks passed; Manny retargeting and Unreal import remain unverified.

- **2026-09-29:** Skeleton Revision03 removes the hat, retains bracelet, reduces teeth, rebuilds shoulder/collarbone and rib-cage geometry, and rebakes a supported recline with offset small leg swings. Reference rest rig preserved; stable hand-joint targets verified. Prior versions preserved; no Unreal Content changes or runtime tests.

- **2026-09-29:** Created Skeleton NPC Revision02 separately from the preserved prototype: slimmer skull/ribs, leather hat, gold bracelet, no earring, level fixed gaze. Adapted mesh and seated animation to the Gentleman's exported rest rig without changing its bones. Blender checked 193 finite samples, zero loop seam/root-object drift, complete weights and matching FBX round-trip hierarchy/joint positions. Unreal import and NPC gameplay remain untested/unimplemented; no Content assets changed.

- **2026-09-29:** Created separate original skeleton-NPC Blender prototype under `ArtSource/SkeletonNPC/Prototype`, with 42-bone rig, packed palette texture and eight-second seated idle; exported rest/animation FBXs but did not import or modify Unreal assets. Gentleman FBX/palette and two dock references exported read-only after retrying offscreen rendering (NullRHI attempt asserted). Inspected Gentleman appearance/1.83 m bounds and prototype renders. Fresh Blender validation: zero unweighted vertices, finite matrices across 193 samples, exact loop endpoints and zero root drift. Stand-up/walk/timer behavior and Unreal import remain unimplemented/unverified. See prototype README.
- **2026-09-29:** Saved Seth's deferred reusable-dialogue request for arrival/fetch quests and fishing-contest interactions, with a proposed separation between dialogue presentation and gameplay validation. Documentation only; no implementation or architecture approval implied.

- **2026-09-29:** Light main-system review recorded in `PROJECT_LIGHT_REVIEW.md`; no gameplay edits/deletions or runtime tests. Corrected stale EmeraldRing count: September 29 export has one row in all 37 spots, unlike the older export. Flagged partial AddItem payload, acceptance/notification ordering and review-only cleanup candidates; no asset declared safe to delete. Manual AddItem repair completion remains unconfirmed.

- **2026-09-29:** Seth approved the focused AddItem full-payload fix. Tool discovery found no Unreal graph-editing connector and the inspected Python API lacks pin-wiring operations. Fix remains unimplemented pending a manual Editor step; mouse control and separate acceptance-output changes are not authorized by this approval.

- **2026-09-29:** Authorized read-only headless export succeeded for 31 Core Blueprints and 37 spots. Verified AddItem's silent no-insertion path, internal AddedItem flag, missing output, and partial payload reconstruction; documented D20 success award path. Added backend audit and 17-entry migration proposal. No assets saved, compiled or runtime-tested; proposed fixes await approval.

- **2026-09-29:** Added `CATCH_JOURNAL_ARCHITECTURE_RECOMMENDATIONS.md` at Seth's request. Recommended a dedicated editable catalog over runtime actor scanning, documented pending decisions/screenshots and clarified the missing AddItem result pin. Documentation only; no journal gameplay changes or runtime validation.

- **2026-09-28:** Audited journal graph/save links and 37 saved fishing spots; found incomplete category metadata across all 17 eligible IDs and one Catfish metadata conflict. Added read-only audit scripts and `CATCH_JOURNAL_CHATGPT_HANDOFF.md`. No journal assets changed; UMG/graph authoring is blocked by available Python APIs. Runtime/save tests remain outstanding. Animation pilot paused after Seth's positive visual feedback.

- **2026-09-28:** Created an isolated three-asset catch retarget pilot through Unreal Python without mouse control. Verified target skeleton, preserved duration and improved sampled hand spacing; a fresh process reloaded all three assets and checked finite root/pelvis/hand/foot positions at 550 samples. Visual grip quality and gameplay integration remain unverified; existing animation/IK gameplay setup unchanged.

- **2026-09-27:** Recorded collaboration authority, Blueprint-only boundary, Git/Editor-control policy, disposable development-save policy, PC/offline/1080p60 target, game tone, current Catch Journal UI milestone and future reusable quest direction. Verified the public GitHub checkpoint still matches local commit `5eb4b78`. Documentation only; no Unreal assets changed and no runtime validation performed.
- **2026-09-27:** Created repository-grounded handoff from local commit `5eb4b78` and all available One More Cast 2 turns. Recorded existing generic journal/save foundation, absent journal UI/catalog, current enum/field/asset names, and verification limits. No gameplay assets modified.

- **2026-10-01:** Seth accepted the manually assembled close button in Designer: Button_Close at X1324.262085/Y115.346481, 64x64, alignment0/0, SizeToContent off, Z50; child img_CloseX. Recorded placement overrides. Click/input behavior untested; next manual stage is reusable category button.

- **2026-10-01:** Seth accepted WBP_JournalCategoryButtons normal appearance with cyan fish: Brush Tint sRGB00CDFFFF (linear0/0.61272/1/1), ColorAndOpacity white, icon64x64, Overlay padding5/0/0/0, Left/Center alignment. Screenshot confirms appearance; selected state and click behavior remain unimplemented/unverified. Preview Desired fixes full-screen root sizing. Other user-adjusted padding not shown; preserve it. Next: place one category widget in journal to verify fit.

- **2026-10-01:** Seth accepted the five-button category column after manual alignment repairs. Category widget exposes label/icon/count and per-instance Linear Color tint; fish cyan, other artwork original colors. Count RenderTransform Y=-5. Screenshot verifies visual layout only; filtering/selected-state/input/save tests pending. Next: reusable catch entry tile.

- **2026-10-01:** Seth accepted three-column grid Designer preview, adjusted catch-name font to25 and ScrollBox height to488 to align with lower parchment edge. Recorded placement overrides; three preview tiles are not catalog population. Icons fit proportions after ScaleBox correction. Runtime scrolling, longest-name wrapping at25, filtering and selection untested. Next: middle heading/shared details shell.

- **2026-10-01:** Designer screenshot confirms middle heading and right detail name/subtitle plus proportion-preserving large Catfish icon. These remain preview values; no catalog selection wiring verified. Next: description and TotalCollected/BestWeight/word-quality detail presentation, then data wiring. No runtime tests.

- **2026-10-01:** Latest Designer screenshot confirms different exposed preview entry icons/names, detail_wash backdrop and stat rows clearing frame. Entry CatchIcon/CatchName PreConstruct reported implemented; icons preserve proportions. Detail stats remain illustrative (71,4.2 lbs,Legendary), not verified records. Manual stat Y targets600/645/690; dividers590/635/680; description height52. Runtime/data wiring not tested. Next: category Name ID and click dispatcher, then parent filtering. AllPiers will be a virtual UI ID, not a catalog row; Non_Exclusive presentation still pending.

### Deferred Tackle Shop presentation review — after Catch Journal

Seth requested screenshot-only assessment on October 1; no shop work authorized now. Subsequent runtime/hierarchy/graph screenshots show buy/sell views, cooler locked/unlocked/max-tier presentation, and existing RefreshShopMenu/RefreshSellGrid/RefreshCoolerSellGrid/BuildBuyShop/AddBuySlotFromEntry/ShouldShowShopEntry/BuildBaitSlots functions. HandleShopPurchaseSucceeded calls RefreshShopMenu; sell confirmation dispatches to player SellAllInventoryFish/SellAllCoolerFish, then refreshes. Seth reports functionality largely works, but hierarchy feels patched together and purchase button text sometimes fails to update. These screenshots do not show purchase router or refresh function internals, so cause is unverified. Future agreed scope is visual redesign plus focused bug fixes after journal; recommend modular presentation cleanup while preserving backend, not full-system rewrite. Possible message race to inspect: generic shop messages use a resettable timer, while maxed messages use Delay then hide the same ShopInformationBox. WBP_ShopMenu Designer shows cooler/shop panels, buy/sell controls, locked/error overlays and SellAll confirmation simultaneously, with inconsistent spacing/colors/type. Screenshot does not establish runtime visibility or graph quality. Recommendation (proposal, not approved implementation): preserve working purchase router, inventory/save/currency and sell validation; reorganize or rebuild the visual shell with reusable panels and a shared confirmation presentation, inspect existing graph dependencies before reparenting/replacing widgets. Do not infer that backend must be rewritten from Designer clutter. Revisit after Catch Journal.

- **2026-10-01:** Saved end-of-night journal handoff: visual shell complete in screenshots; category click dispatcher stage proposed, not confirmed. Recorded deferred screenshot-only shop review and presentation-focused recommendation. No Unreal assets changed or runtime tests run.

- **2026-10-01:** Saved Seth's deferred daytime/nighttime melancholy direction and Marc first-meeting dialogue draft, explicitly preserving the misunderstood exhaustion exchange. Narrative concept only; no dialogue/gameplay assets changed or tests run.

- **2026-10-02:** Seth tested journal category buttons and reports correct printed IDs. Runtime category dispatch confirmed by user; catalog population/filtering remains pending, close/input restoration not yet confirmed. Next instructional stage: ShouldIncludeCatch filter using ST_CatchDefinition.CatchType and JournalCategoryID.

- **2026-10-04:** Screenshots verify ShouldIncludeCatch branch (AllPiers→Fish, otherwise JournalCategoryID match) and BuildVisibleCatchList (clear Name array, iterate DT_CatchDefinitions row names, read/filter/add matching IDs, Completed→Return). No runtime filter result yet. Next manual step: call list builder after SelectedCategoryID assignment and print matching IDs; then grid creation. Category dispatch runtime was user-confirmed October2.

- **2026-10-04:** Seth tested BuildVisibleCatchList through category handler and confirms IDs narrow correctly for each category. Filter runtime confirmed by user. Next: populate Grid_Catches with WBP_JournalEntry from matching row IDs, retain stable CatchID on each tile. Discovery masking/details/ordering remain pending; preview full-art/name tiles are development-only.

- **2026-10-04:** Seth confirms name flicker/overflow fixed: tile180x190, button padding6, icon height104, name area168x70, font25, AutoWrap false/WrapTextAt168. ScrollBox_Catches height490 supersedes488. Runtime tiles build after removing erroneous handler loop that overwrote SelectedCategoryID with catch IDs. Stable ordering, discovery masking and selection/details still pending.

- **2026-10-05:** Seth confirms removing leftover ScaleBox_CatchName stops first-frame resizing; font20 fits direct SizeBox text and is accepted baseline. Left scroll/vertical containers retain functional category buttons. Next: BuildCategoryList from ST_JournalCategoryData rows, then sorting/dynamic creation. No independent runtime tests.

- **2026-10-05:** Dynamic category buttons build and left scrolling work by user test. Table icons assigned and Non_Exclusive label corrected; category-title shrink-only ScaleBox accepted. Category builder/sort/add/bind graphs visually checked, sort runtime order still not explicitly reported. Next: discovery lookup via FishermanRef.CatchJournalRecords, then real category counts and unknown tile presentation. Do not duplicate save fields.

- **2026-10-05:** Screenshots verified IsCatchDiscovered and GetCategoryCounts graph wiring; Seth reports category numbers correct after connecting formatted counts during button creation. Existing CatchJournalRecords reused; no save fields changed. Next: undiscovered entry presentation and selection/details. No independent compile, PIE or save/load checks.

- **2026-10-05:** Seth reports discovered-name/artwork and undiscovered ???/black-alpha-silhouette tile states working after manual wiring. No independent Editor checks. Next: entry-click dispatcher and shared detail selection.
