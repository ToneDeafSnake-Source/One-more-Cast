import bpy, json, math
from pathlib import Path
from mathutils import Vector
root=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.fbx(filepath=str(root/'Reference/Gentleman_reference.fbx'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
report={'meshes':[],'bones':[]}
for o in meshes:
    report['meshes'].append({'name':o.name,'dimensions':list(o.dimensions),'bounds':[list(o.matrix_world@Vector(c)) for c in o.bound_box]})
for o in bpy.context.scene.objects:
    if o.type=='ARMATURE':
        for b in o.data.bones:report['bones'].append({'name':b.name,'head':list(o.matrix_world@b.head_local),'tail':list(o.matrix_world@b.tail_local)})
for img in bpy.data.images:
    for path in (root/'Reference').glob('*.tga'):
        img.filepath=str(path);img.reload();break
for mat in bpy.data.materials:
    if not mat.use_nodes:continue
    tex=next(iter((root/'Reference').glob('*.tga')),None)
    bsdf=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if tex and bsdf:
        n=mat.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(tex),check_existing=True)
        mat.node_tree.links.new(n.outputs['Color'],bsdf.inputs['Base Color'])
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
scene.world.color=(.2,.2,.2)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(3,-5,2.4));cam=bpy.context.object;aim(cam,(0,0,.95));cam.data.type='ORTHO';cam.data.ortho_scale=2.5;scene.camera=cam
for loc,power,size in [((3,-4,5),600,4),((-3,-2,3),350,3),((0,3,4),500,3)]:
    bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,(0,0,1))
scene.render.resolution_x=800;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.filepath=str(root/'Reference/gentleman_preview.png')
(root/'Reference/blender_reference_metrics.json').write_text(json.dumps(report,indent=2))
bpy.ops.render.render(write_still=True)
