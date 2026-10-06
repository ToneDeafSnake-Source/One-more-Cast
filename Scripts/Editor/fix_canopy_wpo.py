"""Clear inherited constant override through Unreal's native property command."""
import unreal,json,re
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir());OUT=ROOT/'Saved/CodexCanopyInspection'
mat=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion')
editor_data=mat.get_editor_property('editor_only_data')
assert editor_data.get_path_name().startswith('/Game/Core/Environment/CanopyMotion/')
lib=unreal.MaterialEditingLibrary
node=lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
assert node
unreal.SystemLibrary.execute_console_command(None,'set '+editor_data.get_path_name()+' WorldPositionOffset (UseConstant=False)')
assert lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)==node
lib.recompile_material(mat)
t=unreal.AssetExportTask();t.object=mat;t.filename=str(OUT/'material_fixed.copy');t.automated=True;t.prompt=False
assert unreal.Exporter.run_asset_export_task(t)
line=next(x for x in (OUT/'material_fixed.copy').read_text().splitlines() if x.strip().startswith('WorldPositionOffset='))
assert 'UseConstant=True' not in line and 'Expression=' in line,line
assert unreal.EditorAssetLibrary.save_loaded_asset(mat,only_if_is_dirty=False)
r={'status':'saved','wpo_input':line.strip(),'cause':'Inherited UseConstant=True overrode connected expression with zero'}
(OUT/'wpo_fix.json').write_text(json.dumps(r,indent=2));unreal.log('CODEX_WPO_FIX '+json.dumps(r))
