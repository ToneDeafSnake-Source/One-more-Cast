import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
revision=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'Revision02'
root=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC')/revision
bpy.ops.wm.open_mainfile(filepath=str(root/'PierSkeleton_SeatedIdle.blend'))
rig=bpy.data.objects['Gentleman_Reference_Rig'];body=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];scene=bpy.context.scene
scene.frame_set(1);first={b.name:b.matrix.copy() for b in rig.pose.bones};world=rig.matrix_world.copy()
scene.frame_set(193)
seam=max(abs(first[b.name][i][j]-b.matrix[i][j]) for b in rig.pose.bones for i in range(4) for j in range(4))
finite=True;drift=0;minz=100;maxz=-100
for f in range(1,194):
    scene.frame_set(f)
    finite &= all(math.isfinite(x) for b in rig.pose.bones for row in b.matrix for x in row)
    drift=max(drift,max(abs(rig.matrix_world[i][j]-world[i][j]) for i in range(4) for j in range(4)))
    ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    zs=[(body.matrix_world@Vector(v)).z for v in ev.bound_box];minz=min(minz,min(zs));maxz=max(maxz,max(zs))
report={'all_193_frames_finite':finite,'loop_endpoint_error_armature_units':seam,'armature_object_drift':drift,'animated_world_z_bounds_m':[minz,maxz],'unweighted_vertices':sum(not v.groups for v in body.data.vertices),'unreal_import_tested':False}
assert finite and seam<.001 and drift<.00001
assert .1<minz<1 and 1.5<maxz<2.5,report
assert report['unweighted_vertices']==0
scene.cycles.samples=12;scene.render.resolution_x=700;scene.render.resolution_y=700
for f in [49,145]:
    scene.frame_set(f);scene.render.filepath=str(root/f'Idle_Frame_{f:03}.png');bpy.ops.render.render(write_still=True)
# Reload the exported rest FBX and compare reference bone hierarchy / positions.
expected={b.name:(b.parent.name if b.parent else None,list(world@b.head_local)) for b in rig.data.bones}
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.fbx(filepath=str(root/'SK_PierSkeleton_GentlemanRig.fbx'),use_anim=False)
rr=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
actual={b.name:(b.parent.name if b.parent else None,list(rr.matrix_world@b.head_local)) for b in rr.data.bones}
report['fbx_roundtrip_same_bones_and_parents']=expected.keys()==actual.keys() and all(expected[n][0]==actual[n][0] for n in expected)
report['fbx_roundtrip_max_joint_error_m']=max(abs(expected[n][1][i]-actual[n][1][i]) for n in expected for i in range(3))
(root/'animation_checks.json').write_text(json.dumps(report,indent=2));print('REVISION_VALIDATION',json.dumps(report))
