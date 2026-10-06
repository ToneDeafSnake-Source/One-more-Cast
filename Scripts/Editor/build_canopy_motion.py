"""Create only isolated canopy assets. No level edits or shared material changes."""
import unreal,json,traceback
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir());D='/Game/Core/Environment/CanopyMotion'
r={'destination':D,'errors':[]}
try:
 assert not unreal.EditorAssetLibrary.does_asset_exist(D+'/SM_Canopy_GentleMotion'),'Refusing to overwrite finished mesh'
 lib=unreal.MaterialEditingLibrary
 original=unreal.load_asset('/Game/GanzSe_Fishing_Harbor/Materials/Material_Instances/MI_Base_Palette')
 parent=original.get_editor_property('parent')
 assert isinstance(parent,unreal.Material)
 assert not lib.get_material_property_input_node(parent,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET),'Existing WPO requires review'
 mat=unreal.load_asset(D+'/M_Canopy_GentleMotion') if unreal.EditorAssetLibrary.does_asset_exist(D+'/M_Canopy_GentleMotion') else unreal.EditorAssetLibrary.duplicate_asset(parent.get_path_name(),D+'/M_Canopy_GentleMotion')
 inst=unreal.load_asset(D+'/MI_Canopy_GentleMotion') if unreal.EditorAssetLibrary.does_asset_exist(D+'/MI_Canopy_GentleMotion') else unreal.EditorAssetLibrary.duplicate_asset(original.get_path_name(),D+'/MI_Canopy_GentleMotion')
 assert not lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET),'Material already built'
 lib.set_material_instance_parent(inst,mat)
 def node(cls,x,y):return lib.create_material_expression(mat,cls,x,y)
 def connect(a,out,b,pin):assert lib.connect_material_expressions(a,out,b,pin),(out,pin)
 wp=node(unreal.MaterialExpressionWorldPosition,-1300,650)
 wp.set_editor_property('world_position_shader_offset',unreal.WorldPositionIncludedOffsets.WPT_EXCLUDE_ALL_SHADER_OFFSETS)
 lp=node(unreal.MaterialExpressionTransformPosition,-1080,650)
 lp.set_editor_property('transform_source_type',unreal.MaterialPositionTransformSource.TRANSFORMPOSSOURCE_WORLD)
 lp.set_editor_property('transform_type',unreal.MaterialPositionTransformSource.TRANSFORMPOSSOURCE_LOCAL)
 connect(wp,'',lp,'')
 clock=node(unreal.MaterialExpressionTime,-1100,850)
 color=node(unreal.MaterialExpressionVertexColor,-1100,1000)
 custom=node(unreal.MaterialExpressionCustom,-400,650)
 custom.set_editor_property('description','Pinned canopy: red=main cloth, green=loose edges; rigid frame=zero')
 custom.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
 names=['P','T','Mask','Strength','Speed','RippleCm','EdgeCm','WaveSizeCm','Phase']
 inputs=[]
 for name in names:
  i=unreal.CustomInput();i.set_editor_property('input_name',name);inputs.append(i)
 custom.set_editor_property('inputs',inputs)
 custom.set_editor_property('code','''
float t=T*max(Speed,0.0)+Phase;
float k=6.2831853/max(WaveSizeCm,20.0);
float wave=0.68*sin(P.x*k+P.y*k*0.53+t*1.1)+0.32*sin(P.y*k*0.81-P.x*k*0.39-t*0.73);
float edge=0.7*sin(P.x*k*1.35+t*1.65)+0.3*sin(P.y*k-t*1.13);
float z=max(Strength,0.0)*(Mask.r*RippleCm*wave+Mask.g*EdgeCm*edge);
float x=max(Strength,0.0)*Mask.g*EdgeCm*0.18*sin(P.x*k+t*1.2);
return float3(x,0,z);
''')
 connect(lp,'',custom,'P');connect(clock,'',custom,'T');connect(color,'',custom,'Mask')
 params=[('Strength',1.0,'Overall_Strength',0,2),('Speed',1.0,'Movement_Speed',0,3),
 ('RippleCm',1.2,'Cloth_Ripple_cm',0,4),('EdgeCm',2.0,'Edge_Flutter_cm',0,5),
 ('WaveSizeCm',220.,'Wave_Size_cm',60,500),('Phase',0.,'Phase_Offset',0,6.283)]
 for idx,(pin,value,name,lo,hi) in enumerate(params):
  p=node(unreal.MaterialExpressionScalarParameter,-850,1200+idx*180)
  p.set_editor_property('parameter_name',name);p.set_editor_property('default_value',value)
  p.set_editor_property('group','Canopy Movement');p.set_editor_property('slider_min',lo);p.set_editor_property('slider_max',hi)
  connect(p,'',custom,pin)
 tr=node(unreal.MaterialExpressionTransform,-100,650)
 tr.set_editor_property('transform_source_type',unreal.MaterialVectorCoordTransformSource.TRANSFORMSOURCE_LOCAL)
 tr.set_editor_property('transform_type',unreal.MaterialVectorCoordTransform.TRANSFORM_WORLD)
 connect(custom,'',tr,'')
 assert lib.connect_material_property(tr,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
 # Duplicated palette has UseConstant=True on WPO; connection alone does not clear it.
 ed=mat.get_editor_property('editor_only_data')
 unreal.SystemLibrary.execute_console_command(None,'set '+ed.get_path_name()+' WorldPositionOffset (UseConstant=False)')
 lib.recompile_material(mat);lib.update_material_instance(inst)
 unreal.EditorAssetLibrary.save_loaded_asset(mat);unreal.EditorAssetLibrary.save_loaded_asset(inst)
 unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
 ui=unreal.FbxImportUI();ui.set_editor_property('automated_import_should_detect_type',False)
 ui.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_STATIC_MESH)
 ui.set_editor_property('import_materials',False);ui.set_editor_property('import_textures',False)
 ui.static_mesh_import_data.set_editor_property('combine_meshes',True)
 ui.static_mesh_import_data.set_editor_property('auto_generate_collision',False)
 ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
 t=unreal.AssetImportTask();t.filename=str(ROOT/'ArtSource/CanopyMotion/SM_Canopy_GentleMotion.fbx')
 t.destination_path=D;t.destination_name='SM_Canopy_GentleMotion';t.options=ui;t.factory=unreal.FbxFactory();t.automated=True;t.save=True
 unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
 mesh=unreal.load_asset(D+'/SM_Canopy_GentleMotion');assert isinstance(mesh,unreal.StaticMesh)
 mesh.set_material(0,inst)
 original_mesh=unreal.load_asset('/Game/GanzSe_Fishing_Harbor/Static_Meshes/SM_FH_Props_Canopy_Type1_Color1')
 mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',original_mesh.get_editor_property('body_setup').get_editor_property('collision_trace_flag'))
 mesh.set_editor_property('positive_bounds_extension',unreal.Vector(10,10,10))
 mesh.set_editor_property('negative_bounds_extension',unreal.Vector(10,10,10))
 unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 r['assets']=[mesh.get_path_name(),mat.get_path_name(),inst.get_path_name()]
 r['parameters']={x[2]:x[1] for x in params};r['status']='created'
except Exception:r['errors'].append(traceback.format_exc());r['status']='failed'
(ROOT/'Saved/CodexCanopyInspection/build_report.json').write_text(json.dumps(r,indent=2))
unreal.log('CODEX_CANOPY_BUILD '+json.dumps(r))
