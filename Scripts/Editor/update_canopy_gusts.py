"""Focused native asset revision; run with the editor closed. Backups precede writes."""
import unreal, json, traceback, shutil
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()); D='/Game/Core/Environment/CanopyMotion/'
OUT=ROOT/'Saved/CodexCanopyInspection/GustRevision'; OUT.mkdir(parents=True,exist_ok=True)
r={}
try:
 backup=OUT/'Before'; backup.mkdir(exist_ok=True)
 for name in ['SM_Canopy_GentleMotion','M_Canopy_GentleMotion','MI_Canopy_GentleMotion']:
  src=ROOT/'Content/Core/Environment/CanopyMotion'/f'{name}.uasset'
  if not (backup/src.name).exists(): shutil.copy2(src,backup/src.name)
 lib=unreal.MaterialEditingLibrary
 mat=unreal.load_asset(D+'M_Canopy_GentleMotion'); inst=unreal.load_asset(D+'MI_Canopy_GentleMotion')
 custom=unreal.find_object(None,mat.get_path_name()+':MaterialExpressionCustom_0')
 assert custom,'Missing known custom node'
 params=[('GustRate','Gust_Speed',1.,0.,3.),('SpeedVar','Speed_Variation',.45,0.,.9),
 ('StrengthVar','Strength_Variation',.4,0.,.9),('GustPhase','Gust_Offset',0.,0.,6.28),
 ('FlapAngle','Flap_Swing_degrees',7.,0.,15.)]
 inputs=list(custom.get_editor_property('inputs')); names=[str(i.get_editor_property('input_name')) for i in inputs]
 for pin,name,value,lo,hi in params:
  if pin not in names:
   i=unreal.CustomInput(); i.set_editor_property('input_name',pin); inputs.append(i)
 custom.set_editor_property('inputs',inputs)
 for idx,(pin,name,value,lo,hi) in enumerate(params):
  p=lib.create_material_expression(mat,unreal.MaterialExpressionScalarParameter,-850,2400+idx*180)
  p.set_editor_property('parameter_name',name);p.set_editor_property('default_value',value)
  p.set_editor_property('group','Canopy Gusts');p.set_editor_property('slider_min',lo);p.set_editor_property('slider_max',hi)
  assert lib.connect_material_expressions(p,'',custom,pin)
 custom.set_editor_property('description','R main cloth; G front flap; B back flap. Integrated gust phase, broad fold swing.')
 custom.set_editor_property('code','''
float baseT=T*max(Speed,0.0);
float rate=max(GustRate,0.0)*0.32;
float a=GustPhase, b=GustPhase*1.37+1.3;
float g=0.65*sin(rate*baseT+a)+0.35*sin(rate*0.713*baseT+b);
float integral;
if(rate>0.0001)
 integral=0.65*(cos(a)-cos(rate*baseT+a))/rate+0.35*(cos(b)-cos(rate*0.713*baseT+b))/(rate*0.713);
else integral=baseT*(0.65*sin(a)+0.35*sin(b));
float t=baseT+clamp(SpeedVar,0.0,0.9)*integral+Phase;
float strength=max(Strength,0.0)*(1.0+clamp(StrengthVar,0.0,0.9)*g);
float k=6.2831853/max(WaveSizeCm,20.0);
float wave=0.68*sin(P.x*k+P.y*k*0.53+t*1.1)+0.32*sin(P.y*k*0.81-P.x*k*0.39-t*0.73);
float3 result=float3(0,0,Mask.r*RippleCm*wave*strength);
// Each flap shares a temporal signal across its width, rotating around its fold.
float front=Mask.g, back=Mask.b;
float angle=clamp(FlapAngle*strength,-25.0,25.0)*0.017453293;
float af=-angle*(0.72*sin(t*0.85)+0.28*sin(t*1.31+0.4))*front;
float ab=-angle*(0.72*sin(t*0.85)+0.28*sin(t*1.31+0.4))*back;
float2 df=P.yz-float2(141,215);
float2 db=P.yz-float2(-141,318);
float2 rf=float2(cos(af)*df.x-sin(af)*df.y,sin(af)*df.x+cos(af)*df.y)-df;
float2 rb=float2(cos(ab)*db.x-sin(ab)*db.y,sin(ab)*db.x+cos(ab)*db.y)-db;
result.yz+=rf+rb;
// Small trailing flex, coherent across width; no traveling edge wave.
result.y+=strength*EdgeCm*0.25*(front*front+back*back)*sin(t*1.25-0.5);
return result;
''')
 ed=mat.get_editor_property('editor_only_data')
 unreal.SystemLibrary.execute_console_command(None,'set '+ed.get_path_name()+' WorldPositionOffset (UseConstant=False)')
 lib.recompile_material(mat);lib.update_material_instance(inst)
 unreal.EditorAssetLibrary.save_loaded_asset(mat,only_if_is_dirty=False)
 unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
 ui=unreal.FbxImportUI();ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 ui.import_materials=False;ui.import_textures=False
 ui.static_mesh_import_data.combine_meshes=True;ui.static_mesh_import_data.auto_generate_collision=False
 ui.static_mesh_import_data.vertex_color_import_option=unreal.VertexColorImportOption.REPLACE
 t=unreal.AssetImportTask();t.filename=str(ROOT/'ArtSource/CanopyMotion/GustRevision/SM_Canopy_GentleMotion.fbx')
 t.destination_path=D.rstrip('/');t.destination_name='SM_Canopy_GentleMotion';t.options=ui;t.factory=unreal.FbxFactory()
 t.automated=True;t.replace_existing=True;t.replace_existing_settings=True;t.save=False
 unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
 assert t.imported_object_paths,'Import failed'
 mesh=unreal.load_asset(D+'SM_Canopy_GentleMotion');mesh.set_material(0,inst)
 mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 mesh.set_editor_property('positive_bounds_extension',unreal.Vector(30,30,30));mesh.set_editor_property('negative_bounds_extension',unreal.Vector(30,30,30))
 unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 r['parameters']={str(n):lib.get_material_instance_scalar_parameter_value(inst,n) for n in lib.get_scalar_parameter_names(inst)}
 r['collision']=str(mesh.get_editor_property('body_setup').get_editor_property('collision_trace_flag'))
 e=unreal.AssetExportTask();e.object=mat;e.filename=str(OUT/'material.copy');e.automated=True;e.prompt=False
 assert unreal.Exporter.run_asset_export_task(e)
 assert 'WorldPositionOffset=(UseConstant=True' not in (OUT/'material.copy').read_text()
 r['status']='saved'
except Exception:r['error']=traceback.format_exc();r['status']='failed'
(OUT/'update.json').write_text(json.dumps(r,indent=2));unreal.log('CODEX_GUST '+json.dumps(r))
