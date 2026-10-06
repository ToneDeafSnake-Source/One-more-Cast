"""Fresh-load check of native catch catalog against reviewed source."""
import unreal,csv,json,traceback
from pathlib import Path
root=Path(unreal.Paths.project_dir())
report=root/'Saved/CodexCatchJournal/catalog_validation.json'
r={}
try:
 table=unreal.load_asset('/Game/Core/Data/DataTables/CollectionLog/DT_CatchDefinitions')
 assert isinstance(table,unreal.DataTable)
 data=json.loads(unreal.DataTableFunctionLibrary.export_data_table_to_json_string(table))
 source=list(csv.DictReader((root/'ArtSource/CatchJournal/DT_CatchDefinitions_source.csv').open(encoding='utf-8-sig',newline='')))
 assert len(data)==len(source)==17
 by_name={row['Name']:row for row in data}
 assert set(by_name)=={row['Name'] for row in source}
 categories=unreal.load_asset('/Game/Core/Data/DataTables/CollectionLog/DT_JournalCategories')
 assert isinstance(categories,unreal.DataTable)
 category_rows=json.loads(unreal.DataTableFunctionLibrary.export_data_table_to_json_string(categories))
 category_ids={row['CategoryID'] for row in category_rows}
 assert len(category_rows)==5 and category_ids=={'Pier_01','Pier_02','Pier_03','Non_Exclusive','Treasure'}
 for row in source:
  native=by_name[row['Name']]
  assert native['CatchType']==row['CatchType'],row['Name']
  assert native['JournalCategoryID']==row['JournalCategoryID'] in category_ids,row['Name']
  assert native['JournalSortOrder']==int(row['JournalSortOrder']),row['Name']
  assert native['Icon'].endswith(row['Icon'][10:]),row['Name']
 r['sample_rows']={name:by_name[name] for name in ('Catfish','EmeraldRing','ScaleFish')}
 r['columns']=sorted(data[0]);r['row_count']=len(data)
 r['category_rows']={row['CategoryID']:row['SortOtder'] for row in category_rows}
 r['status']='loaded'
except Exception:r.update(status='failed',error=traceback.format_exc())
report.write_text(json.dumps(r,indent=2));unreal.log('CODEX_CATALOG_VERIFY '+json.dumps(r))
