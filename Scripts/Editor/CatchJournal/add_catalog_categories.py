"""Add four agreed journal category IDs, preserving the existing Pier_01 row."""
import unreal,json,traceback,shutil
from pathlib import Path
root=Path(unreal.Paths.project_dir())
out=root/'Saved/CodexCatchJournal/CategoryRevision';out.mkdir(parents=True,exist_ok=True)
path='/Game/Core/Data/DataTables/CollectionLog/DT_JournalCategories'
r={}
try:
 src=root/'Content/Core/Data/DataTables/CollectionLog/DT_JournalCategories.uasset'
 backup=out/src.name
 if not backup.exists():shutil.copy2(src,backup)
 table=unreal.load_asset(path)
 rows=json.loads(unreal.DataTableFunctionLibrary.export_data_table_to_json_string(table))
 assert len(rows)==1 and rows[0]['Name']=='Pier_01','Unexpected existing categories; inspect before modifying'
 original=rows[0].copy()
 assert 'SortOtder' in original,'Unexpected category schema'
 proposed=[('Treasure','Treasure',0),('Pier_02','Pier 2',20),('Pier_03','Pier 3',30),('Non_Exclusive','All Piers',40)]
 for ident,label,order in proposed:
  rows.append({'Name':ident,'CategoryID':ident,'DisplayName':label,'Description':'','Icon':'None','SortOtder':order})
 assert unreal.DataTableFunctionLibrary.fill_data_table_from_json_string(table,json.dumps(rows))
 result=json.loads(unreal.DataTableFunctionLibrary.export_data_table_to_json_string(table))
 by_name={row['Name']:row for row in result}
 assert len(result)==5 and set(by_name)=={row['Name'] for row in rows}
 assert by_name['Pier_01']==original,'Existing Pier_01 row changed'
 for ident,label,order in proposed:
  assert by_name[ident]['CategoryID']==ident and by_name[ident]['SortOtder']==order
 assert unreal.EditorAssetLibrary.save_loaded_asset(table,only_if_is_dirty=False)
 r={'status':'saved','rows':sorted(by_name),'original_pier_01_preserved':True}
except Exception:r={'status':'failed','error':traceback.format_exc()}
(out/'result.json').write_text(json.dumps(r,indent=2));unreal.log('CODEX_CATEGORY_ADD '+json.dumps(r))
