import bpy,bmesh,json
from pathlib import Path
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC');OUT=ROOT/'Revision04_Cleanup';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Revision04/PierSkeleton_SeatedIdle.blend'))
body=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];rig=bpy.data.objects['Gentleman_Reference_Rig'];scene=bpy.context.scene
bm=bmesh.new();bm.from_mesh(body.data);dl=bm.verts.layers.deform.active;pid=body.vertex_groups['pelvis'].index
unseen=set(bm.verts);arches=[]
while unseen:
 v=unseen.pop();island={v};todo=[v]
 while todo:
  for e in todo.pop().link_edges:
   for w in e.verts:
    if w in unseen:unseen.remove(w);island.add(w);todo.append(w)
 if len(island)==24 and all(pid in v[dl].keys() for v in island):arches.append(island)
assert len(arches)==2
removed=0
for island in arches:
 tips={v for v in island if abs(v.co.x)<.025};assert len(tips)==6
 remaining=island-tips;bmesh.ops.delete(bm,geom=list(tips),context='VERTS');removed+=len(tips)
 edges={e for v in remaining for e in v.link_edges if e.is_boundary}
 bmesh.ops.holes_fill(bm,edges=list(edges),sides=0)
bm.to_mesh(body.data);bm.free()
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
rig.name='root';rig.data.pose_position='REST'
bpy.ops.export_scene.fbx(filepath=str(OUT/'SK_PierSkeleton_GentlemanRig.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z')
rig.data.pose_position='POSE';scene.frame_end=193
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_SeatedIdle.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
rig.name='Gentleman_Reference_Rig';scene.frame_end=192;scene.frame_set(1)
scene.render.filepath=str(OUT/'SeatedIdle_Preview.png')
bpy.data.texts['START HERE'].write('\nCleanup: trimmed and capped overlapping pelvic-arch tips; rest of pelvis and animation retained.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_SeatedIdle.blend'));bpy.ops.render.render(write_still=True)
print('CLEANUP',json.dumps({'removed_tip_vertices':removed,'unweighted_vertices':sum(not v.groups for v in body.data.vertices),'rig_bones':len(rig.data.bones)}))
