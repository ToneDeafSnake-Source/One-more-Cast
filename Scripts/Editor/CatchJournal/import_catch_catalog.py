"""Import the reviewed catch CSV after E_CatchType and ST_CatchDefinition exist."""
import csv,json,traceback
from pathlib import Path
import unreal

root=Path(unreal.Paths.project_dir())
source=root/'ArtSource/CatchJournal/DT_CatchDefinitions_source.csv'
dest='/Game/Core/Data/DataTables/CollectionLog/DT_CatchDefinitions'
schema='/Game/Core/Data/Structs/CollectionLog/ST_CatchDefinition'
report=root/'Saved/CodexCatchJournal/catalog_import_report.json'
r={'status':'not_started','source':str(source),'destination':dest}
created=False
try:
 rows=list(csv.DictReader(source.open(encoding='utf-8-sig',newline='')))
 expected={'Name','DisplayName','Icon','CatchType','JournalCategoryID','JournalSortOrder'}
 assert len(rows)==17 and set(rows[0])==expected
 ids=[row['Name'] for row in rows]
 assert len(ids)==len(set(ids))
 for row in rows:
  assert row['CatchType'] in ('Fish','Treasure')
  assert row['Icon'].startswith("Texture2D'/Game/") and row['Icon'].endswith("'")
  asset=row['Icon'].split("'",1)[1][:-1]
  assert unreal.EditorAssetLibrary.does_asset_exist(asset),asset
 struct=unreal.load_asset(schema)
 assert isinstance(struct,unreal.UserDefinedStruct),f'Missing native schema {schema}'
 enum=unreal.load_asset('/Game/Core/Data/Enum/E_CatchType')
 assert isinstance(enum,unreal.UserDefinedEnum),'Missing E_CatchType'
 assert not unreal.EditorAssetLibrary.does_asset_exist(dest),'Catalog already exists; refusing overwrite'
 factory=unreal.DataTableFactory();factory.set_editor_property('struct',struct)
 table=unreal.AssetToolsHelpers.get_asset_tools().create_asset('DT_CatchDefinitions','/Game/Core/Data/DataTables/CollectionLog',unreal.DataTable,factory)
 assert table,'DataTable creation failed'
 created=True
 ok=unreal.DataTableFunctionLibrary.fill_data_table_from_csv_file(table,str(source))
 assert ok,'CSV import failed; inspect Unreal log'
 actual={str(x) for x in unreal.DataTableFunctionLibrary.get_data_table_row_names(table)}
 assert actual==set(ids),{'missing':sorted(set(ids)-actual),'extra':sorted(actual-set(ids))}
 exported=unreal.DataTableFunctionLibrary.export_data_table_to_json_string(table)
 assert exported and len(json.loads(exported))==17
 assert unreal.EditorAssetLibrary.save_loaded_asset(table,only_if_is_dirty=False)
 r.update(status='saved',rows=len(actual),row_names=sorted(actual))
except Exception:
 r.update(status='failed',error=traceback.format_exc())
 if created:
  r['new_table_removed']=unreal.EditorAssetLibrary.delete_asset(dest)
report.write_text(json.dumps(r,indent=2))
unreal.log('CODEX_CATCH_CATALOG_IMPORT '+json.dumps(r))
