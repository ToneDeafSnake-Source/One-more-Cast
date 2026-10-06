import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
root=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC')
variant=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'StandAndStepOff'
bpy.ops.wm.open_mainfile(filepath=str(root/'Revision04_Cleanup/PierSkeleton_SeatedIdle.blend'));bpy.context.scene.frame_set(1)
r=bpy.data.objects['Gentleman_Reference_Rig'];start={b.name:(r.matrix_world@b.matrix).copy() for b in r.pose.bones}
rest={b.name:(b.parent.name if b.parent else None,[list(row) for row in b.matrix_local]) for b in r.data.bones}
bpy.ops.wm.open_mainfile(filepath=str(root/variant/'PierSkeleton_StandPauseStepOff.blend'))
s=bpy.context.scene;r=bpy.data.objects['Gentleman_Reference_Rig'];s.frame_set(1)
error=max(abs(start[b.name][i][j]-(r.matrix_world@b.matrix)[i][j]) for b in r.pose.bones for i in range(4) for j in range(4))
finite=True
for f in range(1,s.frame_end+1):
 s.frame_set(f);finite &= all(math.isfinite(v) for b in r.pose.bones for row in b.matrix for v in row)
o=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());top=max((o.matrix_world@Vector(p)).z for p in ev.bound_box)
unchanged=rest=={b.name:(b.parent.name if b.parent else None,[list(row) for row in b.matrix_local]) for b in r.data.bones}
report={'fresh_load_finite_all_frames':finite,'frames':s.frame_end,'idle_start_world_matrix_max_error':error,'rest_rig_unchanged':unchanged,'final_mesh_top_z_m':top,'preview_water_z_m':.1125,'unweighted_vertices':sum(not v.groups for v in o.data.vertices),'unreal_tested':False}
assert finite and error<.0001 and unchanged and top<.1125
(root/variant/'validation.json').write_text(json.dumps(report,indent=2));print(report)
