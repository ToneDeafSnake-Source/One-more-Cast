"""Preserve the prior source and author independent front/back flap masks."""
import bpy,json
from pathlib import Path
ROOT=Path('G:/Unreal Projects/OneMoreCast');OUT=ROOT/'ArtSource/CanopyMotion/GustRevision';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'ArtSource/CanopyMotion/Canopy_GentleMotion.blend'))
obj=bpy.data.objects['SM_Canopy_GentleMotion'];mesh=obj.data
adj={v.index:set() for v in mesh.vertices}
for e in mesh.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
unseen=set(adj);groups=[]
while unseen:
 seed=unseen.pop();g={seed};todo=[seed]
 while todo:
  for n in adj[todo.pop()]:
   if n in unseen:unseen.remove(n);g.add(n);todo.append(n)
 groups.append(g)
cloth=max(groups,key=len)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
weights={};front=[];back=[]
for v in mesh.vertices:
 p=obj.matrix_world@v.co
 if v.index not in cloth:weights[v.index]=(0,0,0,1);continue
 f=1-smooth(-1.58,-1.44,p.y)
 b=smooth(1.44,1.57,p.y)
 side=1-smooth(1.05,1.28,abs(p.x))
 pin=smooth(.05,.35,min(abs(p.y+1.41),abs(p.y-1.41)))
 weights[v.index]=(side*pin*(1-f)*(1-b),f,b,1)
 if f>0:front.append((p.x,p.y,p.z,f))
 if b>0:back.append((p.x,p.y,p.z,b))
attr=mesh.color_attributes.active_color
for l in mesh.loops:attr.data[l.index].color=weights[l.vertex_index]
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
# Complex-as-simple collision is set in Unreal; do not export the old solid UCX hull.
bpy.ops.export_scene.fbx(filepath=str(OUT/'SM_Canopy_GentleMotion.fbx'),use_selection=True,object_types={'MESH'},bake_anim=False,axis_forward='-Y',axis_up='Z',colors_type='LINEAR')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Canopy_Gusts.blend'))
r={'front_vertices':len(front),'back_vertices':len(back),'cloth_vertices':len(cloth),'support_max_weight':max(max(weights[i][:3]) for i in weights if i not in cloth),'front':front,'back':back}
assert r['support_max_weight']==0 and front and back
(OUT/'weights.json').write_text(json.dumps(r,indent=2));print('GUST_MASKS',len(front),len(back))
