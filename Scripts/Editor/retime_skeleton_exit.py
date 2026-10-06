"""Uniform 1.2x playback, without changing any poses or overwriting earlier files."""
import bpy,json,math
from pathlib import Path
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC');OUT=ROOT/'StandAndStepOff04_Faster';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'StandAndStepOff03/PierSkeleton_StandPauseStepOff.blend'))
s=bpy.context.scene;r=bpy.data.objects['Gentleman_Reference_Rig'];body=bpy.data.objects['SK_PierSkeleton_GentlemanRig']
old=r.animation_data.action;action=old.copy();action.name='A_PierSkeleton_StandPauseHop_120Percent';r.animation_data.action=action
# 168 intervals remain intact: 28.8 fps / 24 fps = 1.2, duration 168/28.8.
# This preserves every original sample and interpolation handle, including the idle action.
s.render.fps=30;s.render.fps_base=30/28.8;s.frame_start=1;s.frame_end=169
s.frame_set(1)
bpy.data.texts['START HERE'].write('\nTIMING PASS: 1.2x speed; 5.833333 seconds. Poses unchanged. Scene FPS 30 / base 1.0416667 = 28.8 fps. Idle action retained but earlier idle file remains the timing authority.\n')
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);r.select_set(True);bpy.context.view_layer.objects.active=r;r.name='root'
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_StandPauseHop_Faster.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
r.name='Gentleman_Reference_Rig'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_StandPauseHop_Faster.blend'))
same=len(old.fcurves)==len(action.fcurves) and all(a.data_path==b.data_path and a.array_index==b.array_index and len(a.keyframe_points)==len(b.keyframe_points) and all(tuple(ka.co)==tuple(kb.co) and tuple(ka.handle_left)==tuple(kb.handle_left) and tuple(ka.handle_right)==tuple(kb.handle_right) for ka,kb in zip(a.keyframe_points,b.keyframe_points)) for a,b in zip(old.fcurves,action.fcurves))
assert same
report={'speed_multiplier':1.2,'duration_seconds':168/(s.render.fps/s.render.fps_base),'pose_curves_and_handles_identical':same,'effective_fps':s.render.fps/s.render.fps_base,'unreal_tested':False}
(OUT/'timing_checks.json').write_text(json.dumps(report,indent=2))
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
s.render.resolution_x=720;s.render.resolution_y=720;s.frame_step=1
s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.filepath=str(OUT/'Faster_Preview.mp4');bpy.ops.render.render(animation=True)
print('RETIME',report)
