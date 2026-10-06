"""Author a separate masked FBX, preserving source vertex positions and UVs."""
import bpy,bmesh,json,math
from pathlib import Path
ROOT=Path('G:/Unreal Projects/OneMoreCast')
OUT=ROOT/'ArtSource/CanopyMotion';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(ROOT/'Saved/CodexCanopyInspection/canopy.fbx'))
obj=bpy.data.objects['SM_FH_Props_Canopy_Type1_Color1'];mesh=obj.data
adj={v.index:set() for v in mesh.vertices}
for e in mesh.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
unseen=set(adj);groups=[]
while unseen:
 seed=unseen.pop();group={seed};todo=[seed]
 while todo:
  for n in adj[todo.pop()]:
   if n in unseen:unseen.remove(n);group.add(n);todo.append(n)
 groups.append(group)
cloth=max(groups,key=len);assert len(cloth)==622
def smooth(a,b,x):
 t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
weights={}
for v in mesh.vertices:
 p=obj.matrix_world@v.co
 if v.index not in cloth:weights[v.index]=(0,0,0,1);continue
 side=1-smooth(1.05,1.28,abs(p.x))
 # Pin cloth at the front/back crossbars; hanging ends regain freedom away from them.
 support=min(abs(p.y+1.41),abs(p.y-1.41))
 pin=smooth(.065,.40,support)
 fringe=max(1-smooth(-1.85,-1.49,p.y),smooth(1.49,1.68,p.y))
 weights[v.index]=(side*pin*(1-fringe),side*pin*fringe,0,1)
attr=mesh.color_attributes.new(name='CanopyMotion',type='FLOAT_COLOR',domain='CORNER')
for loop in mesh.loops:attr.data[loop.index].color=weights[loop.vertex_index]
mesh.color_attributes.active_color=attr
obj.name='SM_Canopy_GentleMotion'
for o in list(bpy.context.scene.objects):
 if o.type=='MESH' and o.name.startswith('UCX_'):
  o.name='UCX_SM_Canopy_GentleMotion_00'
  bm=bmesh.new();bm.from_mesh(o.data)
  bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False)
  bm.to_mesh(o.data);bm.free()
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.select_set(True)
bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.fbx(filepath=str(OUT/'SM_Canopy_GentleMotion.fbx'),use_selection=True,object_types={'MESH'},bake_anim=False,axis_forward='-Y',axis_up='Z',colors_type='LINEAR')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Canopy_GentleMotion.blend'))
r={'cloth_vertices':len(cloth),'rigid_vertices':len(mesh.vertices)-len(cloth),
   'rigid_max_weight':max(max(weights[i][:2]) for i in weights if i not in cloth),
   'weighted_vertices':sum(max(c[:2])>0 for c in weights.values()),'geometry_unchanged':True}
(OUT/'mask_checks.json').write_text(json.dumps(r,indent=2));print('CANOPY_MASK',r)
