"""Read-only native text exports and property inspection; no asset saves."""
import unreal,json
from pathlib import Path
out=Path(unreal.Paths.project_saved_dir())/'CodexCatchJournal'
out.mkdir(parents=True,exist_ok=True)
r={}
paths={
'player':'/Game/Core/PlayerBlueprints/BP_Fisherman',
'save':'/Game/Core/SaveGame/BP_SaveGame',
'spot':'/Game/Core/Interactables/FishingSpot/BP_FishingSpot',
'inventory':'/Game/Core/UI_Components/Inventory/WBP_Inventory',
'shop':'/Game/Core/UI_Components/Menus/TackleShop/WBP_ShopMenu',
'toast':'/Game/Core/UI_Components/OnScreenMessages/WBP_CatchToast'}
for label,path in paths.items():
    obj=unreal.load_asset(path)
    cdo=unreal.get_default_object(unreal.EditorAssetLibrary.load_blueprint_class(path))
    r[label]={}
    for prop in ('CatchJournalRecords','SavedCatchJournalRecords','FishCollectionRecords','FishCatchTable','FishTable','WidgetTree','FishermanRef'):
        try:r[label][prop]=str(cdo.get_editor_property(prop))
        except Exception as e:r[label][prop]=str(e)
    try:
        task=unreal.AssetExportTask()
        task.object=obj
        task.filename=str(out/(label+'.t3d'))
        task.automated=True
        task.prompt=False
        task.exporter=unreal.ObjectExporterT3D()
        r[label]['export']=unreal.Exporter.run_asset_export_task(task)
    except Exception as e:r[label]['export']=str(e)
r['available']=[n for n in dir(unreal) if any(k in n for k in ('Widget','Graph','Export','UserDefinedStruct'))]
(out/'details.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
unreal.log('CODEX_JOURNAL: details complete')
