"""Transient empty-world rendering test; no map or material-instance saves."""
import unreal,json,traceback
from pathlib import Path
OUT=Path(unreal.Paths.project_dir())/'Saved/CodexCanopyInspection/DirectionalWindBack';OUT.mkdir(exist_ok=True)
r={};state={'frame':0};handle=None
try:
 unreal.EditorPythonScripting.set_keep_python_script_alive(True)
 actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
 world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
 mesh=unreal.load_asset('/Game/Core/Environment/CanopyMotion/SM_Canopy_GentleMotion')
 inst=unreal.load_asset('/Game/Core/Environment/CanopyMotion/MI_Canopy_GentleMotion')
 r['saved_parameters']={str(n):unreal.MaterialEditingLibrary.get_material_instance_scalar_parameter_value(inst,n) for n in unreal.MaterialEditingLibrary.get_scalar_parameter_names(inst)}
 actor=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,0))
 comp=actor.static_mesh_component;comp.set_static_mesh(mesh);comp.set_evaluate_world_position_offset(True)
 mat=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion')
 custom=unreal.find_object(None,mat.get_path_name()+':MaterialExpressionCustom_0')
 lib=unreal.MaterialEditingLibrary
 test_time=lib.create_material_expression(mat,unreal.MaterialExpressionScalarParameter,-1200,400)
 test_time.set_editor_property('parameter_name','Transient_Test_Time')
 assert lib.connect_material_expressions(test_time,'',custom,'T')
 lib.recompile_material(mat)
 mid=comp.create_dynamic_material_instance(0,inst)
 light=actors.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,500),unreal.Rotator(-45,-45,0))
 light.light_component.set_intensity(5)
 sky=actors.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,500))
 sky.light_component.set_intensity(1)
 position=unreal.Vector(530,-600,410);target=unreal.Vector(0,0,220)
 camera=actors.spawn_actor_from_class(unreal.SceneCapture2D,position,unreal.MathLibrary.find_look_at_rotation(position,target))
 capture=camera.get_component_by_class(unreal.SceneCaptureComponent2D)
 rt=unreal.RenderingLibrary.create_render_target2d(world,1024,1024,unreal.TextureRenderTargetFormat.RTF_RGBA8)
 capture.set_editor_property('texture_target',rt)
 capture.set_editor_property('capture_source',unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
 capture.set_editor_property('capture_every_frame',False)
 capture.set_editor_property('capture_on_movement',False)
 capture.set_editor_property('fov_angle',45)
 r['collision_mode']=str(mesh.get_editor_property('body_setup').get_editor_property('collision_trace_flag'))
 def tick(delta):
  global handle
  try:
   state['frame']+=1;f=state['frame']
   if f in [30,120,210]:
    mid.set_scalar_parameter_value('Phase_Offset',0)
    mid.set_scalar_parameter_value('Transient_Test_Time',{30:0.,120:2.,210:5.}[f])
   if f in [60,150,240]:capture.capture_scene()
   if f in [90,180,270]:
    unreal.RenderingLibrary.export_render_target(world,rt,str(OUT),'phase_'+str(f)+'.png')
   if f==300:
    r['status']='captured';(OUT/'report.json').write_text(json.dumps(r,indent=2))
    unreal.unregister_slate_post_tick_callback(handle);unreal.SystemLibrary.quit_editor()
  except Exception:
   r['error']=traceback.format_exc();(OUT/'report.json').write_text(json.dumps(r,indent=2))
   unreal.unregister_slate_post_tick_callback(handle);unreal.SystemLibrary.quit_editor()
 handle=unreal.register_slate_post_tick_callback(tick)
except Exception:
 r['error']=traceback.format_exc();(OUT/'report.json').write_text(json.dumps(r,indent=2));unreal.log_error(r['error'])
 unreal.SystemLibrary.quit_editor()
