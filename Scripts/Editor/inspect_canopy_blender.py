import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path('G:/Unreal Projects/OneMoreCast/Saved/CodexCanopyInspection')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(out/'canopy.fbx'))
report=[]
for obj in list(bpy.context.scene.objects):
 if obj.type!='MESH':continue
 mesh=obj.data
 adjacency={v.index:set() for v in mesh.vertices}
 for e in mesh.edges:
  a,b=e.vertices;adjacency[a].add(b);adjacency[b].add(a)
 unseen=set(adjacency);islands=[]
 while unseen:
  seed=unseen.pop();group={seed};stack=[seed]
  while stack:
   for n in adjacency[stack.pop()]:
    if n in unseen:unseen.remove(n);group.add(n);stack.append(n)
  coords=[obj.matrix_world@mesh.vertices[i].co for i in group]
  polys=[p for p in mesh.polygons if p.vertices[0] in group]
  islands.append({'verts':len(group),'faces':len(polys),'materials':sorted(set(p.material_index for p in polys)),
    'min':[min(v[i] for v in coords) for i in range(3)],'max':[max(v[i] for v in coords) for i in range(3)]})
 report.append({'name':obj.name,'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),
 'materials':[m.name for m in mesh.materials],'colors':[a.name for a in mesh.color_attributes],
 'islands':sorted(islands,key=lambda x:-x['verts'])})
 obj.color=(.72,.76,.82,1)
 obj.show_wire=True;obj.show_all_edges=True
(out/'geometry_report.json').write_text(json.dumps(report,indent=2))
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT'
scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH';scene.display.shading.background_type='WORLD'
scene.world=bpy.data.worlds.new('Inspection');scene.world.color=(.12,.12,.12)
points=[o.matrix_world@Vector(c) for o in scene.objects if o.type=='MESH' for c in o.bound_box]
center=sum(points,Vector())/len(points)
size=max(max(p[i] for p in points)-min(p[i] for p in points) for i in range(3))
bpy.ops.object.camera_add(location=center+Vector((1.3,-1.7,1.1))*size)
cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=size*1.55;scene.camera=cam
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.filepath=str(out/'canopy_inspection.png')
bpy.ops.render.render(write_still=True)
print('CANOPY_GEOMETRY',json.dumps(report))
