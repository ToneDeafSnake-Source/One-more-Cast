"""Run transient diagnostic renders using the existing renderer test setup."""
from pathlib import Path
import unreal
script=Path(unreal.Paths.project_dir())/'Scripts/Editor/render_canopy_test.py'
source=script.read_text()
source=source.replace("/RenderTest'","/RenderDiagnostics'")
source=source.replace("r={};state=", "r={};state=")
source=source.replace("   if f==300:",'''   if f==280:
    lib=unreal.MaterialEditingLibrary
    mat=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion')
    wpo=lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    custom=lib.get_inputs_for_material_expression(mat,wpo)[0]
    state['mat']=mat;state['custom']=custom;state['original_code']=custom.get_editor_property('code')
    custom.set_editor_property('code','return float3(0,0,Phase*30.0);')
    lib.recompile_material(mat)
    mid.set_scalar_parameter_value('Phase_Offset',0)
   if f==320:capture.capture_scene()
   if f==350:unreal.RenderingLibrary.export_render_target(world,rt,str(OUT),'force_0.png')
   if f==360:mid.set_scalar_parameter_value('Phase_Offset',2)
   if f==400:capture.capture_scene()
   if f==430:unreal.RenderingLibrary.export_render_target(world,rt,str(OUT),'force_2.png')
   if f==440:
    lib=unreal.MaterialEditingLibrary;mat=state['mat']
    vc=lib.create_material_expression(mat,unreal.MaterialExpressionVertexColor)
    lib.connect_material_property(vc,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    state['custom'].set_editor_property('code','return float3(0,0,0);')
    lib.recompile_material(mat)
   if f==480:capture.capture_scene()
   if f==510:unreal.RenderingLibrary.export_render_target(world,rt,str(OUT),'mask.png')
   if f==540:''')
source=source.replace("    unreal.unregister_slate_post_tick_callback(handle);unreal.SystemLibrary.quit_editor()", "    state['ready']=True",1)
source=source.replace("  except Exception:\n   r['error']", """   if f>540:
    job=OUT/'job.py'
    if job.exists() and job.stat().st_mtime!=state.get('last_job'):
     state['last_job']=job.stat().st_mtime
     exec(compile(job.read_text(),str(job),'exec'),globals())
  except Exception:
   r['error']""")
exec(compile(source,str(script),'exec'))
