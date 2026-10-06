# Catch catalog authoring source — September 30, 2026

`DT_CatchDefinitions_source.csv` seeded the native 17-row DataTable on September 30. Runtime gameplay is not yet wired to read it. Asset filenames/IDs retain their current spellings; edit user-facing `DisplayName` independently. `CateFish` and `Catfish` are distinct existing IDs. `EmeraldRing` uses the icon currently assigned in the inspected spots, `ROD`; verify that artwork before shipping.

Native assets under `/Game/Core/Data`:

- `E_CatchType`: Fish, Treasure.
- `ST_CatchDefinition`: `DisplayName` (Text), `Icon` (Texture2D object reference), `CatchType` (E_CatchType), `JournalCategoryID` (Name), `JournalSortOrder` (Integer).
- `DT_CatchDefinitions`: DataTable using `ST_CatchDefinition`, seeded from this CSV. Fresh-process reload verified 17 rows, type, category, sort order, and icon paths.

The CSV `Name` column is the DataTable row name and equals the current `ST_ItemData.FishID`. A display-name or icon edit will affect newly built catches after `BuildCaughtFishItem` is integrated. Existing held/saved item snapshots retain their prior presentation. Catalog categories describe one journal home per entry; catch spots can still offer entries from several categories. `Pier_01/02/03` assignments follow the icon folders and groups of saved fishing spots, not their debug `RequiredPassTier=0` values. `DT_JournalCategories` now has `Treasure`, `Pier_01`, `Pier_02`, `Pier_03`, and `Non_Exclusive` (displayed as All Piers), ordered 0/10/20/30/40. The preexisting Pier 1 row was preserved field-for-field.

The catalog must never be regenerated automatically from spots after user edits. The CSV is an authoring snapshot and should not be reimported after editing the native DataTable unless intentionally replacing its current rows. Spot odds, quality tables, weights, values, save records, and current IDs remain separate. `Scripts/Editor/CatchJournal/import_catch_catalog.py` was a one-time importer and refuses to overwrite an existing catalog. `Saved/CodexCatchJournal/catalog_validation.json` and `CategoryRevision/result.json` contain validation reports; a prechange category-table backup is in `CategoryRevision`. The next step is Blueprint wiring in `BuildCaughtFishItem`; compile, catch, inventory, and save/load behavior with catalog edits remain unverified.
