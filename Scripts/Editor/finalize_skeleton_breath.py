"""Add a pre-hop breath gesture and another 10% playback speed."""
import bpy,math,json
from pathlib import Path
from mathutils import Matrix,Quaternion
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC');OUT=ROOT/'StandAndStepOff05_Breath';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'StandAndStepOff04_Faster/PierSkeleton_StandPauseHop_Faster.blend'))
s=bpy.context.scene;r=bpy.data.objects['Gentleman_Reference_Rig'];body=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];old=r.animation_data.action
poses={}
for f in range(1,170):
 s.frame_set(f);poses[f]={b.name:b.matrix.copy() for b in r.pose.bones}
action=old.copy();action.name='A_PierSkeleton_StandHop_Breath_132Percent';r.animation_data.action=action
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
for f in range(1,170):
 # Original-time coordinates keep the gesture aligned with the existing pause.
 t=(f-1)/24
 breath=smooth((t-4.25)/.48)*(1-smooth((t-4.78)/.45))
 if not breath:continue
 s.frame_set(f)
 for pb in r.pose.bones:pb.matrix=poses[f][pb.name];bpy.context.view_layer.update()
 # Small chest opening, head counterbalance, and shoulder lift; feet/pelvis unchanged.
 for n,angle in [('spine_02',-1.4),('spine_03',-1.0),('neck_01',.8),('head',.6)]:
  pb=r.pose.bones[n];m=pb.matrix.copy();pivot=m.translation.copy()
  worldrot=Quaternion((1,0,0),math.radians(angle*breath)).to_matrix().to_4x4()
  pb.matrix=Matrix.Translation(pivot)@worldrot@Matrix.Translation(-pivot)@m;bpy.context.view_layer.update()
 for side in ['l','r']:
  pb=r.pose.bones['clavicle_'+side];m=pb.matrix.copy();m.translation.z+=.45*breath # armature units are centimeters
  pb.matrix=m;bpy.context.view_layer.update()
 for pb in r.pose.bones:
  for prop in ['location','rotation_quaternion','scale']:pb.keyframe_insert(prop,frame=f)
for fc in action.fcurves:
 for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
s.render.fps=32;s.render.fps_base=32/31.68;s.frame_start=1;s.frame_end=169;s.frame_set(1)
bpy.data.texts['START HERE'].write('\nPASS 05: another 10% faster (1.32x original), 5.303 seconds. Subtle chest/shoulder inhale during standing pause.\n')
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);r.select_set(True);bpy.context.view_layer.objects.active=r;r.name='root'
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_StandHop_Breath.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
r.name='Gentleman_Reference_Rig';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_StandHop_Breath.blend'))
finite=True;legerror=0;chestchange=0
for f in range(1,170):
 s.frame_set(f)
 for pb in r.pose.bones:
  finite &= all(math.isfinite(v) for row in pb.matrix for v in row)
  error=max(abs(pb.matrix[i][j]-poses[f][pb.name][i][j]) for i in range(4) for j in range(4))
  if pb.name.startswith(('pelvis','thigh','calf','foot','ball')):legerror=max(legerror,error)
  if pb.name=='spine_03':chestchange=max(chestchange,error)
assert finite and legerror<.001 and chestchange>.001
(OUT/'checks.json').write_text(json.dumps({'finite':finite,'lower_body_matrix_max_change':legerror,'chest_matrix_max_change':chestchange,'speed_vs_original':1.32,'speed_vs_previous':1.1,'duration_seconds':168/(s.render.fps/s.render.fps_base),'unreal_tested':False},indent=2))
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.render.resolution_x=720;s.render.resolution_y=720
s.frame_step=1;s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.filepath=str(OUT/'Breath_Faster_Preview.mp4');bpy.ops.render.render(animation=True)
print('BREATH_CHECKS',finite,legerror,chestchange)
