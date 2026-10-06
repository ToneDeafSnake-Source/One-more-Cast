"""Validate exported Unreal variant against authored masks and original positions."""
import bpy,json
from pathlib import Path
from mathutils.kdtree import KDTree
ROOT=Path('G:/Unreal Projects/OneMoreCast');out=ROOT/'Saved/CodexCanopyInspection'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'ArtSource/CanopyMotion/Canopy_GentleMotion.blend'))
source=bpy.data.objects['SM_Canopy_GentleMotion'];a=source.data.color_attributes.active_color
weights={l.vertex_index:tuple(a.data[l.index].color) for l in source.data.loops}
pts=[source.matrix_world@v.co for v in source.data.vertices]
kd=KDTree(len(pts))
for i,p in enumerate(pts):kd.insert(p,i)
kd.balance()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(out/'imported_motion.fbx'))
mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH' and not o.name.startswith('UCX_'))
color=mesh.data.color_attributes.active_color
assert color,'Movement vertex colors missing after Unreal import'
position_error=0.;weight_error=0.;rigid_error=0.
for l in mesh.data.loops:
 p=mesh.matrix_world@mesh.data.vertices[l.vertex_index].co
 _,idx,d=kd.find(p);position_error=max(position_error,d)
 # UE exports raw 8-bit vertex weights as FBX colors; Blender interprets
 # those as sRGB on import. Read color_srgb to compare the stored weights.
 c=color.data[l.index].color_srgb;expected=weights[idx]
 weight_error=max(weight_error,abs(c[0]-expected[0]),abs(c[1]-expected[1]))
 if expected[0]==expected[1]==0:rigid_error=max(rigid_error,c[0],c[1])
r={'max_position_error_m':position_error,'max_mask_error':weight_error,'fixed_vertex_mask_max':rigid_error,
   'imported_vertices':len(mesh.data.vertices),'imported_triangles':len(mesh.data.polygons)}
assert position_error<.0001,r
# FBX color gamma conversion may differ; fixed zeros must always survive exactly.
assert rigid_error<.001,r
assert weight_error<.02,r
r['status']='passed'
(out/'roundtrip_report.json').write_text(json.dumps(r,indent=2));print('CANOPY_ROUNDTRIP',r)
