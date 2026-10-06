"""Separate hand-assisted rise / pause / step-off clip for the cleaned NPC."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC');OUT=ROOT/'StandAndStepOff';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Revision04_Cleanup/PierSkeleton_SeatedIdle.blend'))
s=bpy.context.scene;r=bpy.data.objects['Gentleman_Reference_Rig'];body=bpy.data.objects['SK_PierSkeleton_GentlemanRig']
s.frame_set(1);W=r.matrix_world.copy();WI=W.inverted();rest={b.name:W@b.matrix_local for b in r.data.bones};H={n:m.translation.copy() for n,m in rest.items()}
initial={b.name:(W@b.matrix).copy() for b in r.pose.bones};idle=r.animation_data.action;idle.use_fake_user=True
r.animation_data_clear();r.animation_data_create();act=bpy.data.actions.new('A_PierSkeleton_StandPauseStepOff');r.animation_data.action=act
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def channel(t,keys):
 for (ta,a),(tb,b) in zip(keys,keys[1:]):
  if t<=tb:return a+(b-a)*smooth((t-ta)/(tb-ta))
 return keys[-1][1]
def pos(n):return (W@r.pose.bones[n].matrix).translation
def put(n,p,q):
 r.pose.bones[n].matrix=WI@Matrix.Translation(p)@q.to_matrix().to_4x4()@rest[n].to_3x3().to_4x4();bpy.context.view_layer.update()
def aim(n,child,target):put(n,pos(n),(H[child]-H[n]).rotation_difference(Vector(target)-pos(n)))
maxreach=0;reach_by_limb={}
def limb(a,b,c,target,pole):
 global maxreach
 p=pos(a);target=Vector(target);l1=(H[b]-H[a]).length;l2=(H[c]-H[b]).length
 d=target-p;dist=d.length;maxreach=max(maxreach,max(0,dist-l1-l2));reach_by_limb[a]=max(reach_by_limb.get(a,0),max(0,dist-l1-l2));dist=min(dist,l1+l2-.0002);u=d.normalized()
 target=p+u*dist;along=(l1*l1-l2*l2+dist*dist)/(2*dist);v=Vector(pole);v=(v-u*v.dot(u)).normalized()
 joint=p+along*u+v*math.sqrt(max(0,l1*l1-along*along));aim(a,b,joint);aim(b,c,target)
def path(t,points):return Vector([channel(t,[(tt,p[i]) for tt,p in points]) for i in range(3)])
F=157;s.render.fps=24;s.frame_start=1;s.frame_end=F
samples={};finite=True
for f in range(1,F+1):
 t=(f-1)/24;s.frame_set(f);r.matrix_world=W
 for pb in r.pose.bones:pb.rotation_mode='QUATERNION';pb.matrix_basis=Matrix.Identity(4)
 bpy.context.view_layer.update()
 fall=max(0,t-5.12);drop=min(4.2,4.0*fall*fall)
 hipy=channel(t,[(0,.045),(.45,.07),(1.5,.22),(2.5,.22),(3.6,.18),(4.3,.18),(5.12,-.15),(6.5,-.60)])
 hipz=channel(t,[(0,1.015),(.4,1.03),(1.4,1.17),(2.35,1.31),(3.6,1.83),(6.5,1.83)])-drop
 lean=channel(t,[(0,2),(.6,38),(1.4,48),(2.4,43),(3.6,2),(4.3,2),(5.2,7),(6.5,9)])
 put('pelvis',Vector((0,hipy,hipz)),Quaternion((1,0,0),math.radians(lean*.25)))
 for n,offset in [('spine_01',-6),('spine_02',0),('spine_03',5),('neck_01',1)]:put(n,pos(n),Quaternion((1,0,0),math.radians(lean+offset)))
 put('head',pos('head'),Quaternion((1,0,0),math.radians(-2)))
 for side in ['l','r']:put('clavicle_'+side,pos('clavicle_'+side),Quaternion((1,0,0),math.radians(lean+3)))
 for sign,side in [(1,'l'),(-1,'r')]:
  start=initial['foot_'+side].translation
  offset=0 if side=='l' else .80
  ankle=path(t,[(0,start),(.5+offset,start),(1.0+offset,(sign*.12,-.22,1.15)),(1.55+offset,(sign*.12,.13,1.075)),(4.3,(sign*.12,.13,1.075))])
  if t>4.3:
   if side=='r':ankle=path(t,[(4.3,(sign*.12,.13,1.075)),(4.7,(sign*.12,-.13,1.18)),(5.12,(sign*.12,-.40,1.075)),(6.5,(sign*.12,-.70,1.02))])
   else:ankle=path(t,[(4.3,(sign*.12,.13,1.075)),(5.12,(sign*.12,.13,1.075)),(5.6,(sign*.12,-.23,1.14)),(6.5,(sign*.12,-.48,1.02))])
  ankle.z-=drop
  limb('thigh_'+side,'calf_'+side,'foot_'+side,ankle,(0,-1,.12))
  put('foot_'+side,pos('foot_'+side),Quaternion((1,0,0),math.radians(channel(t,[(0,0),(1.1+offset,-10),(1.55+offset,0),(5.12,0),(6.5,15)]))))
  shoulder=pos('upperarm_'+side);plant=initial['hand_'+side].translation
  release=smooth((t-(.65 if side=='l' else .8))/.75)
  relaxed=shoulder+Vector((sign*.025,-.015,-.505))
  wrist=plant.lerp(relaxed,release)
  limb('upperarm_'+side,'lowerarm_'+side,'hand_'+side,wrist,(sign*.15,.5,0))
  q0=initial['hand_'+side].to_quaternion()@rest['hand_'+side].to_quaternion().inverted()
  q1=(H['middle_01_'+side]-H['hand_'+side]).rotation_difference(Vector((0,-.05,-1)))
  put('hand_'+side,pos('hand_'+side),q0.slerp(q1,release))
  for digit in ['index','middle','thumb']:
   for j in [1,2,3]:
    n=f'{digit}_0{j}_{side}'
    r.pose.bones[n].rotation_quaternion=Quaternion((0,0,1),math.radians(8*release))
 # Exact first pose, with a short transition away from the idle hand/leg details.
 blend=smooth(t/.35)
 if blend<1:
  for pb in r.pose.bones:
   target=W@pb.matrix;old=initial[pb.name]
   p=old.translation.lerp(target.translation,blend);q=old.to_quaternion().slerp(target.to_quaternion(),blend)
   scale=old.to_scale().lerp(target.to_scale(),blend)
   pb.matrix=WI@Matrix.LocRotScale(p,q,scale);bpy.context.view_layer.update()
 for p in ['location','rotation_euler','scale']:r.keyframe_insert(p,frame=f)
 for pb in r.pose.bones:
  for p in ['location','rotation_quaternion','scale']:pb.keyframe_insert(p,frame=f)
 finite &= all(math.isfinite(x) for pb in r.pose.bones for row in pb.matrix for x in row)
 if f in [1,25,49,73,97,121,145,157]:samples[f]={n:list(pos(n)) for n in ['pelvis','head','foot_l','foot_r']}
for fc in act.fcurves:
 for k in fc.keyframe_points:k.interpolation='LINEAR'
act.use_fake_user=True
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);r.select_set(True);bpy.context.view_layer.objects.active=r;r.name='root'
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_StandPauseStepOff.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
r.name='Gentleman_Reference_Rig';s.frame_set(1)
cam=s.camera;cam.data.ortho_scale=3.65;cam.location=(3.1,-4.8,3.0);cam.rotation_euler=(Vector((0,-.1,1.38))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.data.texts['START HERE'].write('\nSTAND / PAUSE / STEP OFF: 6.5 seconds, nonlooping. Starts at idle frame 1. Vertical/horizontal travel baked in pelvis; NOT tested Unreal root motion. Preview water has no splash/collision.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_StandPauseStepOff.blend'))
(OUT/'checks.json').write_text(json.dumps({'all_frames_finite':finite,'duration_seconds':6.5,'maximum_unreachable_target_m':maxreach,'reach_by_limb':reach_by_limb,'samples':samples,'unreal_tested':False},indent=2))
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
s.render.resolution_x=720;s.render.resolution_y=720
for f in [25,49,73,97,121,133]:
 s.frame_set(f);s.render.image_settings.file_format='PNG';s.render.filepath=str(OUT/f'Pose_{f:03}.png');bpy.ops.render.render(write_still=True)
s.frame_step=2;s.render.fps=12;s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.filepath=str(OUT/'StandPauseStepOff_Preview.mp4');bpy.ops.render.render(animation=True)
print('EXIT_ANIMATION',finite,maxreach)
