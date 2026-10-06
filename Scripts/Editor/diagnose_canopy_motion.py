import unreal,json,traceback
from pathlib import Path
r={}
try:
 subsystem=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
 for key,path in [('original','/Game/GanzSe_Fishing_Harbor/Static_Meshes/SM_FH_Props_Canopy_Type1_Color1'),('variant','/Game/Core/Environment/CanopyMotion/SM_Canopy_GentleMotion')]:
  mesh=unreal.load_asset(path);body=mesh.get_editor_property('body_setup')
  r[key]={'complexity':str(body.get_editor_property('collision_trace_flag')),
  'body':str(body),'agg_geom':str(body.get_editor_property('agg_geom')),'nanite':str(mesh.get_editor_property('nanite_settings'))}
 mat=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion')
 r['material']={}
 for p in ['use_material_attributes','max_world_position_offset_displacement','world_position_offset_disable_distance']:
  try:r['material'][p]=str(mat.get_editor_property(p))
  except Exception:pass
except Exception:r['error']=traceback.format_exc()
(Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/diagnosis.json').write_text(json.dumps(r,indent=2));unreal.log('CODEX_DIAGNOSIS '+json.dumps(r))
