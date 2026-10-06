import bpy,json,math,sys
from pathlib import Path
variant=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'StandAndStepOff02'
root=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC')/variant
bpy.ops.wm.open_mainfile(filepath=str(root/'PierSkeleton_StandPauseStepOff.blend'))
s=bpy.context.scene;o=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];r=bpy.data.objects['Gentleman_Reference_Rig']
ids={side:[v.index for v in o.data.vertices if any(o.vertex_groups[g.group].name in ['calf_'+side,'foot_'+side,'ball_'+side] for g in v.groups)] for side in ['l','r']}
feet={side:[v.index for v in o.data.vertices if any(o.vertex_groups[g.group].name in ['foot_'+side,'ball_'+side] for g in v.groups)] for side in ['l','r']}
hits=[];soles=[];finite=True;prev={};maxstep={side:0 for side in ids}
for f in range(1,170):
 s.frame_set(f);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
 finite &= all(math.isfinite(x) for b in r.pose.bones for row in b.matrix for x in row)
 for side,indices in ids.items():
  for i in indices:
   p=o.matrix_world@mesh.vertices[i].co
   if abs(p.x)<.76 and -.128<p.y<.97 and .867<p.z<.972:hits.append((f,side,round(p.y,4),round(p.z,4)))
  if 70<=f<=123:soles.append(min((o.matrix_world@mesh.vertices[i].co).z for i in feet[side]))
  p=r.matrix_world@r.pose.bones['calf_'+side].head
  if side in prev and f<=129:maxstep[side]=max(maxstep[side],(p-prev[side]).length)
  prev[side]=p.copy()
 ev.to_mesh_clear()
report={'finite':finite,'lower_leg_deck_interior_vertex_hits':len(hits),'first_hits':hits[:15],'worst_frame_hits':max(((f,sum(h[0]==f for h in hits)) for f in range(1,170)),key=lambda x:x[1]),'standing_sole_z_range':[min(soles),max(soles)],'deck_top_z':.975,'max_knee_frame_step_m':maxstep,'unreal_tested':False}
(root/'contact_checks.json').write_text(json.dumps(report,indent=2));print(report)
