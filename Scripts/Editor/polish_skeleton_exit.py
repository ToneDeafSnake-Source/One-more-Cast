import bpy,math,json
from pathlib import Path
from mathutils import Matrix,Vector,Quaternion
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC');OUT=ROOT/'StandAndStepOff06_Polish';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'StandAndStepOff05_Breath/PierSkeleton_StandHop_Breath.blend'))
s=bpy.context.scene;r=bpy.data.objects['Gentleman_Reference_Rig'];body=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];W=r.matrix_world.copy();WI=W.inverted()
rest={b.name:W@b.matrix_local for b in r.data.bones};H={n:m.translation.copy() for n,m in rest.items()};poses={}
for f in range(1,170):
 s.frame_set(f);poses[f]={b.name:(W@b.matrix).copy() for b in r.pose.bones}
act=r.animation_data.action.copy();act.name='A_PierSkeleton_FootFollowThrough_HopDip';r.animation_data.action=act
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def put(n,m):r.pose.bones[n].matrix=WI@m;bpy.context.view_layer.update()
def solve(side,target):
 a='thigh_'+side;b='calf_'+side;c='foot_'+side;p=(W@r.pose.bones[a].matrix).translation
 d=target-p;L1=(H[b]-H[a]).length;L2=(H[c]-H[b]).length;dist=min(d.length,L1+L2-.0001);u=d.normalized();along=(L1*L1-L2*L2+dist*dist)/(2*dist)
 v=Vector((0,d.z,-d.y));v=(v-u*v.dot(u)).normalized();k=p+along*u+v*math.sqrt(max(0,L1*L1-along*along))
 for n,child,point in [(a,b,k),(b,c,target)]:
  q=(H[child]-H[n]).rotation_difference(point-(W@r.pose.bones[n].matrix).translation)
  m=Matrix.Translation((W@r.pose.bones[n].matrix).translation)@q.to_matrix().to_4x4()@rest[n].to_3x3().to_4x4();put(n,m)
for f in range(1,170):
 envelope=smooth((f-11)/7)*(1-smooth((f-35)/7))
 dip=smooth((f-120)/5)*(1-smooth((f-125)/4))
 if envelope==0 and dip==0:continue
 s.frame_set(f)
 for b in r.pose.bones:put(b.name,poses[f][b.name])
 if envelope:
  # Continuous low-amplitude dangle, smoothly entering/leaving the flagged interval.
  ankle=poses[f]['foot_r'].translation.copy();ankle.y-=.013*envelope*math.sin((f-11)*math.pi/26);ankle.z+=.008*envelope*math.sin((f-11)*math.pi/18)
  solve('r',ankle)
  q=Quaternion((1,0,0),math.radians(3.5*envelope*math.sin((f-11)*math.pi/23)))
  put('foot_r',Matrix.Translation((W@r.pose.bones['foot_r'].matrix).translation)@q.to_matrix().to_4x4()@poses[f]['foot_r'].to_3x3().to_4x4())
 if dip:
  m=poses[f]['pelvis'].copy();m.translation.z-=.023*dip;put('pelvis',m)
  # Keep both feet fixed while the pelvis descends, making the knee bend carry weight.
  for side in ['l','r']:
   solve(side,poses[f]['foot_'+side].translation)
   put('foot_'+side,poses[f]['foot_'+side])
 for pb in r.pose.bones:
  for prop in ['location','rotation_quaternion','scale']:pb.keyframe_insert(prop,frame=f)
for fc in act.fcurves:
 for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);r.select_set(True);bpy.context.view_layer.objects.active=r;r.name='root'
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_PolishedExit.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
r.name='Gentleman_Reference_Rig';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_PolishedExit.blend'))
finite=True;plant=0
for f in range(1,170):
 s.frame_set(f);finite &= all(math.isfinite(x) for b in r.pose.bones for row in b.matrix for x in row)
 if 121<=f<=128:
  for side in ['l','r']:plant=max(plant,((W@r.pose.bones['foot_'+side].matrix).translation-poses[f]['foot_'+side].translation).length)
assert finite and plant<.0001
(OUT/'checks.json').write_text(json.dumps({'finite_all_169_frames':finite,'squat_foot_target_max_change_m':plant,'added_squat_depth_m':.023,'duration_seconds':168/(s.render.fps/s.render.fps_base),'unreal_tested':False},indent=2))
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.render.resolution_x=720;s.render.resolution_y=720
s.frame_step=1;s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.filepath=str(OUT/'PolishedExit_Preview.mp4');bpy.ops.render.render(animation=True)
print('POLISH',finite,plant)
