"""Read-only native exports of Core Blueprints and current saved spot definitions."""
import json
from pathlib import Path
import unreal

out = Path(unreal.Paths.project_saved_dir()) / 'CodexCatchJournal' / 'BackendReview'
out.mkdir(parents=True, exist_ok=True)
results = []
for path in unreal.EditorAssetLibrary.list_assets('/Game/Core', recursive=True, include_folder=False):
    data = unreal.EditorAssetLibrary.find_asset_data(path)
    if str(data.asset_class_path.asset_name) not in ('Blueprint', 'WidgetBlueprint'):
        continue
    obj = unreal.load_asset(path)
    filename = path.split('.')[0].replace('/Game/', '').replace('/', '__') + '.t3d'
    task = unreal.AssetExportTask()
    task.object = obj
    task.filename = str(out / filename)
    task.automated = True
    task.prompt = False
    task.exporter = unreal.ObjectExporterT3D()
    ok = unreal.Exporter.run_asset_export_task(task)
    results.append({'asset': path, 'file': filename, 'exported': ok})
(out / 'manifest.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
unreal.log('CODEX_BACKEND: exported ' + str(len(results)) + ' Core Blueprints')
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.load_level('/Game/MainDock')
spot_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/Core/Interactables/FishingSpot/BP_FishingSpot')
spots = []
for actor in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if actor.get_class() != spot_class:
        continue
    properties = {}
    for name in ('RequiredPassTier',):
        try:
            properties[name] = str(actor.get_editor_property(name))
        except Exception as error:
            properties[name] = str(error)
    spots.append({'actor': actor.get_path_name(), 'label': actor.get_actor_label(),
                  'properties': properties,
                  'entries': [row.export_text() for row in actor.get_editor_property('FishCatchTable')]})
(out / 'definitions.json').write_text(json.dumps({'spots': spots}, indent=2), encoding='utf-8')
unreal.log('CODEX_BACKEND: inspected ' + str(len(spots)) + ' saved spots; no assets saved')
