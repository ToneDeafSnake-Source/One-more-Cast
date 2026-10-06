import unreal,json
from pathlib import Path
m=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion');e=m.get_editor_property('editor_only_data');r={}
for name in ['WorldPositionOffset','world_position_offset','WorldPositionOffset_DEPRECATED']:
 try:r[name]=str(e.get_editor_property(name))
 except Exception as ex:r[name]=str(ex)
t=unreal.AssetExportTask();t.object=m;t.filename=str(Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/material.copy');t.automated=True;t.prompt=False
r['export']=unreal.Exporter.run_asset_export_task(t)
(Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/input_probe.json').write_text(json.dumps(r,indent=2));unreal.log('CODEX_INPUT '+json.dumps(r))
