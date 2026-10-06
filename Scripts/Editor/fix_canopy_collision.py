"""Restore the original canopy's collision policy on only the generated variant."""
import unreal,json
from pathlib import Path
original=unreal.load_asset('/Game/GanzSe_Fishing_Harbor/Static_Meshes/SM_FH_Props_Canopy_Type1_Color1')
mesh=unreal.load_asset('/Game/Core/Environment/CanopyMotion/SM_Canopy_GentleMotion')
src=original.get_editor_property('body_setup');dst=mesh.get_editor_property('body_setup')
before=str(dst.get_editor_property('collision_trace_flag'))
dst.set_editor_property('collision_trace_flag',src.get_editor_property('collision_trace_flag'))
assert dst.get_editor_property('collision_trace_flag')==unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE
assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
r={'before':before,'after':str(dst.get_editor_property('collision_trace_flag')),'saved':True}
(Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/collision_fix.json').write_text(json.dumps(r,indent=2))
unreal.log('CODEX_COLLISION_FIX '+json.dumps(r))
