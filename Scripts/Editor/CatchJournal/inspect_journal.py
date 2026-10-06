"""Read-only Catch Journal inspection. Run through Unreal Editor Python."""
import unreal
import json
from pathlib import Path

OUT=Path(unreal.Paths.project_saved_dir())/'CodexCatchJournal'
OUT.mkdir(parents=True,exist_ok=True)
report={}
paths={
 'player':'/Game/Core/PlayerBlueprints/BP_Fisherman',
 'save':'/Game/Core/SaveGame/BP_SaveGame',
 'inventory':'/Game/Core/UI_Components/Inventory/WBP_Inventory',
 'shop':'/Game/Core/UI_Components/Menus/TackleShop/WBP_ShopMenu',
 'toast':'/Game/Core/UI_Components/OnScreenMessages/WBP_CatchToast',
 'spot':'/Game/Core/Interactables/FishingSpot/BP_FishingSpot',
 'categories':'/Game/Core/Data/DataTables/CollectionLog/DT_JournalCategories',
}
for label,path in paths.items():
    obj=unreal.load_asset(path)
    info={'path':path,'class':obj.get_class().get_name() if obj else None}
    if not obj:
        report[label]=info
        continue
    for prop in ('widget_tree','new_variables','function_graphs','ubergraph_pages','status'):
        try:
            v=obj.get_editor_property(prop)
            info[prop]=str(v)
        except Exception as exc:
            info[prop]=str(exc)
    if isinstance(obj,unreal.Blueprint):
        cls=unreal.EditorAssetLibrary.load_blueprint_class(path)
        cdo=unreal.get_default_object(cls)
        info['members']=[x for x in dir(cdo) if any(k in x.lower() for k in ('journal','collection','fish','catch','save','close','inventory'))]
        for name in info['members']:
            try:
                value=cdo.get_editor_property(name)
                info[name]=str(value)
            except Exception:
                pass
    if isinstance(obj,unreal.DataTable):
        info['rows']=unreal.DataTableFunctionLibrary.export_data_table_to_json_string(obj)
    report[label]=info
for clsname in ('WidgetBlueprint','WidgetTree','BlueprintEditorLibrary','WidgetBlueprintEditorSubsystem','WidgetBlueprintLibrary','EditorAssetLibrary'):
    cls=getattr(unreal,clsname,None)
    report['api_'+clsname]=[n for n in dir(cls) if not n.startswith('_')] if cls else None
(OUT/'inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
unreal.log('CODEX_JOURNAL: inspection written '+str(OUT/'inspection.json'))
