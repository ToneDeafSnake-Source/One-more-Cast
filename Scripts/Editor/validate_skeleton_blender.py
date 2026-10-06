import bpy,json,math
from pathlib import Path
root=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC/Prototype')
bpy.ops.wm.open_mainfile(filepath=str(root/'PierSkeleton_SeatedIdle.blend'))
rig=bpy.data.objects['PierSkeleton_Rig'];mesh=bpy.data.objects['SK_PierSkeleton_Prototype'];scene=bpy.context.scene
scene.frame_set(1)
start={b.name:b.matrix.copy() for b in rig.pose.bones}
scene.frame_set(193)
seam=max(abs(start[b.name][i][j]-b.matrix[i][j]) for b in rig.pose.bones for i in range(4) for j in range(4))
finite=True;roots=[]
for f in range(1,194):
    scene.frame_set(f);roots.append(list(rig.pose.bones['root'].head))
    finite &= all(math.isfinite(x) for b in rig.pose.bones for row in b.matrix for x in row)
report={'loop_endpoint_max_matrix_error':seam,'all_193_frames_finite':finite,'root_max_motion':max(abs(a-b) for r in roots for a,b in zip(r,roots[0])),
        'unweighted_vertices':sum(not v.groups for v in mesh.data.vertices),'packed_images':[(im.name,im.packed_file is not None) for im in bpy.data.images if im.name.startswith('Skeleton')],
        'unreal_import_tested':False}
(root/'animation_checks.json').write_text(json.dumps(report,indent=2))
scene.cycles.samples=12;scene.render.resolution_x=600;scene.render.resolution_y=600
for f in [49,97,145]:
    scene.frame_set(f);scene.render.filepath=str(root/f'Idle_Frame_{f:03}.png');bpy.ops.render.render(write_still=True)
print('CODEX_VALIDATION',json.dumps(report))
