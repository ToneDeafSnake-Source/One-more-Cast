import unreal,json,traceback
from pathlib import Path
D='/Game/Core/Environment/CanopyMotion/';r={'errors':[]}
try:
 lib=unreal.MaterialEditingLibrary
 mesh=unreal.load_asset(D+'SM_Canopy_GentleMotion');mat=unreal.load_asset(D+'M_Canopy_GentleMotion');inst=unreal.load_asset(D+'MI_Canopy_GentleMotion')
 assert mesh and mat and inst
 assert mesh.get_material(0)==inst and inst.get_editor_property('parent')==mat
 assert lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
 r['parameters']={str(n):lib.get_material_instance_scalar_parameter_value(inst,n) for n in lib.get_scalar_parameter_names(inst)}
 assert r['parameters']['Overall_Strength']==1 and r['parameters']['Movement_Speed']==1
 orig=unreal.load_asset('/Game/GanzSe_Fishing_Harbor/Materials/Material_Instances/MI_Base_Palette')
 pending=[lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_BASE_COLOR)];seen=set();types=[]
 while pending:
  expression=pending.pop()
  if not expression or expression.get_path_name() in seen:continue
  seen.add(expression.get_path_name());types.append(expression.get_class().get_name())
  pending.extend(lib.get_inputs_for_material_expression(mat,expression))
 assert 'MaterialExpressionVertexColor' not in types,'Movement colors affect base color'
 r['base_color_expression_types']=types
 r['textures']={str(n):str(lib.get_material_instance_texture_parameter_value(inst,n)) for n in lib.get_texture_parameter_names(inst)}
 for n in lib.get_texture_parameter_names(orig):assert lib.get_material_instance_texture_parameter_value(inst,n)==lib.get_material_instance_texture_parameter_value(orig,n)
 lib.recompile_material(mat);lib.update_material_instance(inst)
 r['statistics']=str(lib.get_statistics(mat))
 t=unreal.AssetExportTask();t.object=mesh;t.filename=str(Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/imported_motion.fbx');t.automated=True;t.prompt=False;t.options=unreal.FbxExportOption()
 t.options.set_editor_property('level_of_detail',False)
 assert unreal.Exporter.run_asset_export_task(t)
 r['status']='reloaded_connected_and_recompiled'
except Exception:r['errors'].append(traceback.format_exc());r['status']='failed'
(Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/validation_report.json').write_text(json.dumps(r,indent=2))
unreal.log('CODEX_CANOPY_VERIFY '+json.dumps(r))
