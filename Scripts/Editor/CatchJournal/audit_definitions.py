"""Inspect saved MainDock catch definitions without saving the map or assets."""
import unreal,json
from pathlib import Path
out=Path(unreal.Paths.project_saved_dir())/'CodexCatchJournal'
out.mkdir(parents=True,exist_ok=True)
result={'spots':[],'schemas':{}}
for name,path in {
 'item':'/Game/Core/Data/Structs/ST_ItemData',
 'entry':'/Game/Core/Data/Structs/ST_FishCatchEntry',
 'record':'/Game/Core/Data/Structs/CollectionLog/ST_CatchJournalRecord',
 'quality':'/Game/Core/Data/Enum/E_FishQuality',
 'category':'/Game/Core/Data/Structs/CollectionLog/ST_JournalCategoryData'}.items():
    obj=unreal.load_asset(path)
    task=unreal.AssetExportTask()
    task.object=obj
    task.filename=str(out/(name+'.t3d'))
    task.automated=True
    task.prompt=False
    task.exporter=unreal.ObjectExporterT3D()
    result['schemas'][name]=unreal.Exporter.run_asset_export_task(task)
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.load_level('/Game/MainDock')
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
spotcls=unreal.EditorAssetLibrary.load_blueprint_class('/Game/Core/Interactables/FishingSpot/BP_FishingSpot')
for actor in actors:
    if actor.get_class()==spotcls:
        rows=actor.get_editor_property('FishCatchTable')
        result['spots'].append({'actor':actor.get_path_name(),'label':actor.get_actor_label(),'entries':[row.export_text() for row in rows]})
(out/'definitions.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
unreal.log('CODEX_JOURNAL: saved map inspected; spots='+str(len(result['spots'])))
