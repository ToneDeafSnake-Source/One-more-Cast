import bpy,json
from mathutils import Vector
from pathlib import Path
p=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC/Revision04')
bpy.ops.wm.open_mainfile(filepath=str(p/'PierSkeleton_SeatedIdle.blend'))
o=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];bpy.context.scene.frame_set(1)
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
links={v.index:set() for v in o.data.vertices}
for e in o.data.edges:
 a,b=e.vertices;links[a].add(b);links[b].add(a)
unseen=set(links);out=[]
while unseen:
 first=unseen.pop();island={first};todo=[first]
 while todo:
  for k in links[todo.pop()]:
   if k in unseen:unseen.remove(k);island.add(k);todo.append(k)
 coords=[o.matrix_world@me.vertices[i].co for i in island];c=sum(coords,Vector())/len(coords)
 if any(o.vertex_groups[g.group].name=='pelvis' for i in island for g in o.data.vertices[i].groups):
  out.append({'indices':sorted(island),'center':list(c),'count':len(island),'groups':list({o.vertex_groups[g.group].name for i in island for g in o.data.vertices[i].groups})})
print('CANDIDATES',json.dumps(out));ev.to_mesh_clear()
