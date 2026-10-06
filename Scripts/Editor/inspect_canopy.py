"""Read-only canopy inspection and FBX export. Never save project assets."""
import unreal, json, traceback
from pathlib import Path
out=Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection'
out.mkdir(parents=True,exist_ok=True)
r={}
try:
 m=unreal.load_asset('/Game/GanzSe_Fishing_Harbor/Static_Meshes/SM_FH_Props_Canopy_Type1_Color1')
 assert m
 r['mesh']=m.get_path_name();r['bounds']=str(m.get_bounds())
 r['materials']=[]
 for slot in m.get_editor_property('static_materials'):
  mat=slot.material_interface
  entry={'slot':str(slot.material_slot_name),'material':mat.get_path_name() if mat else None}
  if isinstance(mat,unreal.MaterialInstanceConstant):
   entry['parent']=mat.get_editor_property('parent').get_path_name()
  r['materials'].append(entry)
 task=unreal.AssetExportTask();task.object=m;task.filename=str(out/'canopy.fbx')
 task.automated=True;task.prompt=False;task.options=unreal.FbxExportOption()
 task.options.set_editor_property('level_of_detail',False)
 r['exported']=unreal.Exporter.run_asset_export_task(task)
except Exception:r['error']=traceback.format_exc()
(out/'unreal_report.json').write_text(json.dumps(r,indent=2))
unreal.log('CODEX_CANOPY '+json.dumps(r))
