"""Original low-poly skeleton prototype. Run using Blender --background --python.
Reference imports are not included in deliverable character geometry.
"""
import bpy, math, json, random
from mathutils import Vector, Matrix, Quaternion
from pathlib import Path
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC')
OUT=ROOT/'Prototype';OUT.mkdir(parents=True,exist_ok=True)
random.seed(17)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
character=bpy.data.collections.new('CHARACTER • export this');scene.collection.children.link(character)
stage=bpy.data.collections.new('PREVIEW ONLY • pier and lighting');scene.collection.children.link(stage)
def move(o,col):
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o)
palette=[(.64,.55,.37,1),(.80,.72,.52,1),(.91,.85,.66,1),(.19,.22,.20,1),(.035,.043,.041,1),(.45,.24,.095,1),(.13,.27,.25,1),(.33,.37,.32,1)]
img=bpy.data.images.new('Skeleton_Palette_Weathered',width=256,height=32)
pixels=[]
for y in range(32):
    for x in range(256):
        c=palette[x//32];noise=random.uniform(-.018,.018)
        pixels.extend([max(0,min(1,v+noise)) for v in c[:3]]+[1])
img.pixels=pixels;img.filepath_raw=str(OUT/'Skeleton_Palette.png');img.file_format='PNG';img.save();img.pack()
mat=bpy.data.materials.new('M_WeatheredBone_Palette');mat.use_nodes=True
nodes=mat.node_tree.nodes;bsdf=nodes.get('Principled BSDF');bsdf.inputs['Roughness'].default_value=.88
tex=nodes.new('ShaderNodeTexImage');tex.image=img;tex.interpolation='Closest'
mat.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
parts=[]
def finish(o,name,bone='pelvis',color=1):
    o.name=name;move(o,character)
    bpy.context.view_layer.objects.active=o
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.clear();o.data.materials.append(mat)
    uv=o.data.uv_layers.active or o.data.uv_layers.new(name='PaletteUV')
    for face in o.data.polygons:
        tile=color
        if color==1:tile=random.choices([0,1,2],[.1,.75,.15])[0]
        for idx in face.loop_indices:uv.data[idx].uv=((tile+.35+random.random()*.3)/8,.35+random.random()*.3)
        face.use_smooth=False
    if bone:
        vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
    parts.append(o);return o
def ell(name,loc,scale,bone='pelvis',color=1,segments=10,rings=6):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc)
    o=bpy.context.object;o.scale=scale;return finish(o,name,bone,color)
def rod(name,a,b,r,bone,color=1,r2=None):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=7,radius1=r,radius2=r2 if r2 is not None else r*.85,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=d.to_track_quat('Z','Y')
    return finish(o,name,bone,color)
def tube(name,points,r,bone,color=1,sides=6):
    points=[Vector(p) for p in points];verts=[];faces=[]
    for i,p in enumerate(points):
        tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
        u=tangent.cross(Vector((0,0,1)))
        if u.length<.01:u=tangent.cross(Vector((0,1,0)))
        u.normalize();v=tangent.cross(u).normalized()
        for j in range(sides):verts.append(p+r*(math.cos(j*math.tau/sides)*u+math.sin(j*math.tau/sides)*v))
    for i in range(len(points)-1):
        for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);character.objects.link(o);return finish(o,name,bone,color)
def box(name,loc,scale,bone,color=1):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale;return finish(o,name,bone,color)

# Proportions in meters; front is -Y. Broad stylized skull, compact torso, long limbs.
bones={}
def bone(name,a,b,parent=None):bones[name]=(Vector(a),Vector(b),parent)
bone('root',(0,0,0),(0,0,.15))
bone('pelvis',(0,0,.94),(0,0,1.04),'root')
bone('spine_01',(0,0,1.04),(0,0,1.20),'pelvis')
bone('spine_02',(0,0,1.20),(0,0,1.39),'spine_01')
bone('neck_01',(0,0,1.39),(0,0,1.50),'spine_02')
bone('head',(0,0,1.50),(0,0,1.78),'neck_01')
for sign,side in [(1,'l'),(-1,'r')]:
    x=lambda v:sign*v
    bone('clavicle_'+side,(0,0,1.39),(x(.21),0,1.39),'spine_02')
    bone('upperarm_'+side,(x(.21),0,1.39),(x(.48),0,1.34),'clavicle_'+side)
    bone('lowerarm_'+side,(x(.48),0,1.34),(x(.73),0,1.30),'upperarm_'+side)
    bone('hand_'+side,(x(.73),0,1.30),(x(.82),0,1.29),'lowerarm_'+side)
    bone('thigh_'+side,(x(.105),0,.94),(x(.12),0,.53),'pelvis')
    bone('calf_'+side,(x(.12),0,.53),(x(.12),0,.12),'thigh_'+side)
    bone('foot_'+side,(x(.12),0,.12),(x(.12),-.15,.07),'calf_'+side)
    bone('ball_'+side,(x(.12),-.15,.07),(x(.12),-.23,.06),'foot_'+side)
    for j,label in enumerate(['index','middle','ring','pinky']):
        y=(j-1.5)*.027
        bone(label+'_01_'+side,(x(.81),y,1.29),(x(.867),y,1.284),'hand_'+side)
        bone(label+'_02_'+side,(x(.867),y,1.284),(x(.916 if j<2 else .903),y,1.275),label+'_01_'+side)
    bone('thumb_01_'+side,(x(.755),-.03,1.30),(x(.795),-.074,1.286),'hand_'+side)
    bone('thumb_02_'+side,(x(.795),-.074,1.286),(x(.834),-.086,1.278),'thumb_01_'+side)

# Skull is modeled with actual socket cavities, not painted circles.
skull=ell('Skull • faceted cranium',(0,.004,1.655),(.133,.108,.155),'head',1,16,10)
for sign in [-1,1]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(sign*.055,-.092,1.661))
    cut=bpy.context.object;cut.scale=(.049,.068,.047)
    bpy.context.view_layer.objects.active=cut;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bpy.context.view_layer.objects.active=skull
    mod=skull.modifiers.new('Carved orbit','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    ell('Socket interior',(sign*.055,-.048,1.661),(.044,.024,.040),'head',4)
    rod('Brow ridge',(sign*.017,-.09,1.705),(sign*.105,-.074,1.70),.015,'head')
    ell('Cheekbone',(sign*.091,-.074,1.607),(.04,.032,.023),'head')
skull.vertex_groups['head'].add(list(range(len(skull.data.vertices))),1,'REPLACE')
ell('Upper muzzle',(0,-.065,1.587),(.069,.049,.031),'head')
# Triangular nasal aperture.
me=bpy.data.meshes.new('Nose');me.from_pydata([(-.019,-.114,1.627),(.019,-.114,1.627),(0,-.118,1.658)],[],[(0,1,2)])
o=bpy.data.objects.new('Nasal aperture',me);character.objects.link(o);finish(o,o.name,'head',4)
tube('Mandible',[(-.091,-.006,1.60),(-.089,-.05,1.55),(-.05,-.093,1.535),(0,-.104,1.53),(.05,-.093,1.535),(.089,-.05,1.55),(.091,-.006,1.60)],.018,'head')
for j in range(7):
    x=(j-3)*.017
    box('Upper tooth', (x,-.109+abs(x)*.23,1.568),(.013,.017,.022),'head',2)
    if j!=1:box('Lower tooth',(x,-.11+abs(x)*.22,1.547),(.012,.016,.013),'head',2)
# restrained nautical charm: oxidized hoop on one side; no clothing.
bpy.ops.mesh.primitive_torus_add(major_segments=12,minor_segments=5,location=(.14,0,1.59),major_radius=.031,minor_radius=.006,rotation=(math.pi/2,0,0))
finish(bpy.context.object,'Old brass hoop','head',5)
for z in [1.02,1.07,1.12,1.17,1.22,1.27,1.32,1.37,1.43,1.47]:
    owner='pelvis' if z<1.04 else ('spine_01' if z<1.20 else ('spine_02' if z<1.39 else 'neck_01'))
    ell('Vertebra',(0,.032,z),(.034,.03,.022),owner,0)
    rod('Spinous process',(0,.04,z),(0,.078,z-.008),.012,owner)
for i in range(6):
    z=1.37-i*.043;width=[.115,.146,.165,.168,.153,.125][i]
    for sign in [-1,1]:
        pts=[]
        for k in range(13):
            t=k/12*math.pi
            pts.append((sign*(.025+width*math.sin(t)),.035-.125*(1-math.cos(t))/2,z-.018*math.sin(t)-.018*k/12))
        tube('Rib %d'%i,pts,.0105,'spine_02' if i<4 else 'spine_01')
rod('Sternum',(0,-.099,1.36),(0,-.103,1.17),.021,'spine_02')
for sign,side in [(1,'l'),(-1,'r')]:
    tube('Clavicle',[(0,-.055,1.396),(sign*.11,-.039,1.41),(sign*.21,0,1.39)],.017,'clavicle_'+side)
    ell('Scapula',(sign*.12,.056,1.32),(.069,.018,.083),'spine_02',0)
    ell('Iliac wing',(sign*.088,.007,.98),(.080,.035,.079),'pelvis',1,8,4)
    tube('Pelvic arch',[(sign*.145,0,.97),(sign*.12,-.03,.89),(sign*.055,-.043,.86),(0,-.032,.89)],.023,'pelvis')
    for label in ['upperarm','thigh']:
        a,b,_=bones[label+'_'+side];d=b-a
        rod(label,a+d*.10,b-d*.10,.024 if label=='thigh' else .017,label+'_'+side,r2=.018 if label=='thigh' else .013)
        for p in [a+d*.10,b-d*.07]:ell('Joint end',p,(.03,.026,.03),label+'_'+side)
    for label in ['lowerarm','calf']:
        a,b,_=bones[label+'_'+side];d=b-a
        for off in [-.011,.011]:
            shift=Vector((0,off,0)) if label=='lowerarm' else Vector((sign*off,0,0))
            rod(label+' paired',a+d*.06+shift,b-d*.04+shift,.012 if off<0 else .008,label+'_'+side)
    ell('Patella',(sign*.12,-.026,.53),(.026,.018,.031),'calf_'+side)
    a,b,_=bones['hand_'+side]
    for j in range(4):rod('Metacarpal',a+Vector((0,(j-1.5)*.014,0)),(sign*.81,(j-1.5)*.027,1.29),.006,'hand_'+side)
    for name,(a,b,parent) in bones.items():
        if name.endswith('_'+side) and any(name.startswith(x) for x in ['index','middle','ring','pinky','thumb']):
            rod(name,a,b,.0065,name);ell('Knuckle',a,(.008,.008,.008),name)
    ell('Ankle',(sign*.12,0,.12),(.023,.023,.028),'foot_'+side)
    ell('Heel',(sign*.12,.016,.083),(.035,.039,.029),'foot_'+side)
    for j in range(5):
        xx=sign*.12+(j-2)*.017
        rod('Metatarsal',(xx,0,.083),(xx,-.15,.066),.009,'foot_'+side)
        rod('Toe',(xx,-.15,.066),(xx,-.218+(abs(j-1))*.013,.056),.007,'ball_'+side)

# Join all rigid-weighted pieces into one deforming mesh, then create the rig.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join()
body=bpy.context.object;body.name='SK_PierSkeleton_Prototype'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
rigdata=bpy.data.armatures.new('PierSkeleton_Rig');rig=bpy.data.objects.new('PierSkeleton_Rig',rigdata);character.objects.link(rig)
bpy.context.view_layer.objects.active=rig;body.select_set(False);rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for name,(a,b,parent) in bones.items():
    eb=rigdata.edit_bones.new(name);eb.head=a;eb.tail=b
    if parent:eb.parent=rigdata.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True
modifier=body.modifiers.new('Rigid bone deformation','ARMATURE');modifier.object=rig;body.parent=rig
rig['Notes']='Original stylized prototype. Rigid weights are intentional for bone pieces. Front -Y. Root stays fixed in idle.'

def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*color,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.85;return m
wood=material('Preview • worn dock',(.20,.105,.048));water=material('Preview • sea',(.065,.20,.23))
def propcube(name,loc,scale,m):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m);move(o,stage)
    bevel=o.modifiers.new('Soft worn edges','BEVEL');bevel.width=.007;bevel.segments=1;return o
for j in range(8):propcube('PREVIEW dock plank',((j-3.5)*.19,.42,.895),(.18,1.1,.11),wood)
for x in [-.63,.63]:propcube('PREVIEW piling',(x,.05,.38),(.13,.13,1.15),wood)
propcube('PREVIEW water',(0,0,.10),(200,200,.025),water)

# Rest-pose FBX, isolated character objects only.
def select_character():
    bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
select_character()
bpy.ops.export_scene.fbx(filepath=str(OUT/'SK_PierSkeleton_Prototype.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True)

def set_segment(name,head,tail,extra=None):
    pb=rig.pose.bones[name];a,b,_=bones[name]
    q=(b-a).rotation_difference(Vector(tail)-Vector(head))
    rot=q.to_matrix().to_4x4()@rigdata.bones[name].matrix_local.to_3x3().to_4x4()
    pb.matrix=Matrix.Translation(Vector(head))@rot
    if extra:pb.rotation_quaternion=pb.rotation_quaternion@extra
    bpy.context.view_layer.update()
def solve_elbow(a,c,L1,L2,pole):
    delta=c-a;dist=min(delta.length,L1+L2-.001);u=delta.normalized()
    along=(L1*L1-L2*L2+dist*dist)/(2*dist)
    v=Vector(pole);v=(v-u*v.dot(u)).normalized()
    return a+u*along+v*math.sqrt(max(0,L1*L1-along*along))
scene.render.fps=24;scene.frame_start=1;scene.frame_end=192
rig.animation_data_create();action=bpy.data.actions.new('A_PierSkeleton_SeatedIdle_8s');rig.animation_data.action=action
for frame in range(1,194):
    scene.frame_set(frame);t=(frame-1)/192*math.tau
    for pb in rig.pose.bones:pb.rotation_mode='QUATERNION';pb.matrix_basis=Matrix.Identity(4)
    hip=Vector((0,.045,1.015))
    # Mild posture shift, not breathing; seated pelvis is fixed on the plank.
    lean=Quaternion((1,0,0),math.radians(7+1.1*math.sin(t)))@Quaternion((0,1,0),math.radians(.65*math.sin(t)))
    def upper(p):return hip+lean@(Vector(p)-bones['pelvis'][0])
    set_segment('pelvis',hip,hip+Vector((0,0,.10)))
    for name in ['spine_01','spine_02','neck_01','head']:
        a,b,_=bones[name];set_segment(name,upper(a),upper(b))
    rig.pose.bones['head'].rotation_quaternion @= Quaternion((0,1,0),math.radians(3*math.sin(t)))
    bpy.context.view_layer.update()
    for sign,side in [(1,'l'),(-1,'r')]:
        ha=hip+Vector((sign*.105,0,0));knee=ha+Vector((sign*.028,-.408,-.026))
        ankle=knee+Vector((0,.028+ .012*math.sin(t+(0 if sign==1 else math.pi)), -.409))
        set_segment('thigh_'+side,ha,knee);set_segment('calf_'+side,knee,ankle)
        toe=ankle+Vector((0,-.15,-.05));set_segment('foot_'+side,ankle,toe);set_segment('ball_'+side,toe,toe+Vector((0,-.08,-.01)))
        a,b,_=bones['clavicle_'+side];shoulder=upper(b);set_segment('clavicle_'+side,upper(a),shoulder)
        wrist=hip+Vector((sign*.17,-.27,.042))
        L1=(bones['upperarm_'+side][1]-bones['upperarm_'+side][0]).length
        L2=(bones['lowerarm_'+side][1]-bones['lowerarm_'+side][0]).length
        elbow=solve_elbow(shoulder,wrist,L1,L2,(sign,0,-.1))
        set_segment('upperarm_'+side,shoulder,elbow);set_segment('lowerarm_'+side,elbow,wrist)
        set_segment('hand_'+side,wrist,wrist+Vector((0,-.09,-.012)))
    for pb in rig.pose.bones:
        pb.keyframe_insert('location',frame=frame);pb.keyframe_insert('rotation_quaternion',frame=frame);pb.keyframe_insert('scale',frame=frame)
for fc in action.fcurves:
    for key in fc.keyframe_points:key.interpolation='LINEAR'
    fc.modifiers.new('CYCLES')
action.use_fake_user=True
select_character()
scene.frame_end=193  # Include repeated endpoint for an exact 8-second FBX clip.
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_SeatedIdle.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
scene.frame_end=192

scene.frame_set(1)
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.world.color=(.18,.18,.18)
bpy.ops.object.camera_add(location=(2.6,-4.2,2.45));cam=bpy.context.object;move(cam,stage);aim(cam,(0,-.07,1.15));cam.data.type='ORTHO';cam.data.ortho_scale=2.25;scene.camera=cam
for loc,power,size in [((2,-4,5),650,4),((-3,-1,3),400,3),((0,3,4),800,3)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;move(o,stage);o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,1))
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'SeatedIdle_Preview.png')
select_character()
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.shading.type='MATERIAL'
            area.spaces.active.overlay.show_overlays=False
readme=bpy.data.texts.new('START HERE')
readme.write('PIER SKELETON — original prototype\nPress Space to preview 8-second seated idle.\nCharacter collection contains only rig + mesh. Dock/water are preview only.\nArmature rest pose is standing A/T pose. Pose Position / Rest Position switches in Armature data.\nTexture is packed and supplied separately. Rigid bone weights are intentional.\nUnreal import/retarget/stand-up/walk/gameplay timer are NOT implemented or validated.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_SeatedIdle.blend'))
bpy.ops.render.render(write_still=True)
report={'vertices':len(body.data.vertices),'polygons':len(body.data.polygons),'bones':len(rigdata.bones),'frames':192,'fps':24,'duration_seconds':8,'unweighted_vertices':sum(not v.groups for v in body.data.vertices),'unreal_validated':False}
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
print('CODEX_SKELETON',json.dumps(report))
