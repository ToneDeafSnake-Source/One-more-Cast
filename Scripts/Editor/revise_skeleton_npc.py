"""Non-destructive second art pass using the exported Gentleman's actual armature."""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector, Matrix

ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC')
OUT=ROOT/'Revision02'; OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Prototype/PierSkeleton_SeatedIdle.blend'))
scene=bpy.context.scene
old=bpy.data.objects['PierSkeleton_Rig']; body=bpy.data.objects['SK_PierSkeleton_Prototype']
character=body.users_collection[0]
oldrest={b.name:b.matrix_local.copy() for b in old.data.bones}
oldheads={b.name:b.head_local.copy() for b in old.data.bones}
oldtails={b.name:b.tail_local.copy() for b in old.data.bones}
poses={}
for f in range(1,194):
    scene.frame_set(f); poses[f]={b.name:b.matrix.copy() for b in old.pose.bones}
old.data.pose_position='REST'
# The original hoop alone uses palette swatch 5; remove its complete mesh islands.
bm=bmesh.new();bm.from_mesh(body.data);uv=bm.loops.layers.uv.active
hoop={v for face in bm.faces if all(int(loop[uv].uv.x*8)==5 for loop in face.loops) for v in face.verts}
assert len(hoop)>0
bmesh.ops.delete(bm,geom=list(hoop),context='VERTS');bm.to_mesh(body.data);bm.free()
for v in body.data.vertices:
    name=body.vertex_groups[max(v.groups,key=lambda g:g.weight).group].name
    if name=='head':
        v.co.x*=.80;v.co.y=.004+(v.co.y-.004)*.86
    elif name in ('spine_01','spine_02'):
        v.co.x*=.77;v.co.y*=.84

# Copy the reference armature, never edit the source FBX or Unreal skeleton.
before=set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=str(ROOT/'Reference/Gentleman_reference.fbx'),use_anim=False)
imported=set(bpy.data.objects)-before
rig=next(o for o in imported if o.type=='ARMATURE')
for o in imported:
    if o!=rig:bpy.data.objects.remove(o,do_unlink=True)
for c in list(rig.users_collection):c.objects.unlink(rig)
character.objects.link(rig)
rig.animation_data_clear(); rig.show_in_front=True
W=rig.matrix_world.copy(); WI=W.inverted()
rest={b.name:W@b.matrix_local for b in rig.data.bones}
heads={n:m.translation.copy() for n,m in rest.items()}
reference_signature={b.name:{'parent':b.parent.name if b.parent else None,'matrix':[list(r) for r in b.matrix_local]} for b in rig.data.bones}
ends={}
for n in heads:
    child={'pelvis':'spine_01','spine_01':'spine_02','spine_02':'spine_03','spine_03':'neck_01','neck_01':'head'}.get(n)
    for side in ('l','r'):
        chain=['clavicle','upperarm','lowerarm','hand','middle_01','middle_02','middle_03']
        for a,b in zip(chain,chain[1:]):
            if n==a+'_'+side:child=b+'_'+side
        chain=['thigh','calf','foot','ball']
        for a,b in zip(chain,chain[1:]):
            if n==a+'_'+side:child=b+'_'+side
        for digit in ('index','thumb'):
            for i in (1,2):
                if n==f'{digit}_0{i}_{side}':child=f'{digit}_0{i+1}_{side}'
    ends[n]=heads[child] if child in heads else heads[n]+Vector((0,0,.10))
    if n.startswith('ball_'):ends[n]=heads[n]+Vector((0,-.08,-.01))

align={}
for n in oldrest:
    if n not in rest:continue
    # Axial anatomy should stay upright, independent of FBX bone display axes.
    q=(oldtails[n]-oldheads[n]).rotation_difference(ends[n]-heads[n])
    if n in ('pelvis','spine_01','spine_02','neck_01','head'):q=Vector((0,0,1)).rotation_difference(Vector((0,0,1)))
    align[n]=q

assignments=[]
for v in body.data.vertices:
    n=body.vertex_groups[max(v.groups,key=lambda g:g.weight).group].name
    target=n if n in rest else ('hand_'+n[-1] if n.startswith(('ring','pinky')) else 'pelvis')
    anchor=n if n in rest else target
    p=v.co-oldheads[anchor]
    if anchor.startswith(('upperarm','lowerarm','thigh','calf','hand','index','middle','thumb','foot','ball')):
        axis=(oldtails[anchor]-oldheads[anchor]).normalized()
        ratio=(ends[anchor]-heads[anchor]).length/(oldtails[anchor]-oldheads[anchor]).length
        p+=axis*p.dot(axis)*(ratio-1)
    v.co=heads[anchor]+align[anchor]@p
    if n=='head':v.co.z-=heads['head'].z-oldheads['head'].z
    assignments.append(target)
body.vertex_groups.clear()
for n in sorted(set(assignments)):
    group=body.vertex_groups.new(name=n);group.add([i for i,x in enumerate(assignments) if x==n],1,'REPLACE')
body.parent=rig;body.matrix_world=Matrix.Identity(4)
body.modifiers[0].object=rig
body.name='SK_PierSkeleton_GentlemanRig'
bpy.data.objects.remove(old,do_unlink=True)
rig.matrix_world=W
bpy.context.view_layer.update()
body.matrix_world=Matrix.Identity(4)
bpy.context.view_layer.update()

# Restrained, low-crowned leather hat with gently cocked side brim.
def material(name,color,metal=0,rough=.8):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    s=m.node_tree.nodes.get('Principled BSDF');s.inputs['Base Color'].default_value=(*color,1)
    s.inputs['Metallic'].default_value=metal;s.inputs['Roughness'].default_value=rough
    return m
leather=material('M_WornBrownLeather',(.105,.052,.024))
edge=material('M_LeatherBrimEdge',(.17,.085,.035))
band=material('M_DarkLeatherHatband',(.035,.024,.015))
gold=material('M_OldGoldBracelet',(.60,.35,.075),.72,.32)
parts=[]
def accessory(name,verts,faces,mat,bone):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);character.objects.link(o);mesh.materials.append(mat)
    vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(verts))),1,'REPLACE');parts.append(o)
    return o
headshift=heads['head']-oldheads['head'];headshift.z=0;z=1.747
N=24;verts=[]
for rx,ry,dz in [(.106,.091,0),(.180,.149,-.012),(.180,.149,-.020),(.106,.091,-.008)]:
    for i in range(N):
        t=i*math.tau/N
        lift=.066*max(0,math.cos(t))**4 if rx>.15 else 0
        verts.append((rx*math.cos(t)+headshift.x,ry*math.sin(t)+.004+headshift.y,z+dz+lift))
faces=[]
for k in range(4):
    for i in range(N):faces.append((k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i))
accessory('Leather hat • modest cocked brim',verts,faces,edge,'head')
verts=[]
for rx,ry,dz in [(.106,.091,0),(.105,.090,.027),(.089,.077,.063),(.052,.045,.088)]:
    for i in range(N):
        t=i*math.tau/N;verts.append((rx*math.cos(t)+headshift.x,ry*math.sin(t)+.004+headshift.y,z+dz))
faces=[(k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i) for k in range(3) for i in range(N)]
faces.append(tuple(range(3*N,4*N)))
accessory('Leather hat • low crown',verts,faces,leather,'head')
verts=[]
for h in [.008,.028]:
    for i in range(N):
        t=i*math.tau/N;verts.append((.107*math.cos(t)+headshift.x,.092*math.sin(t)+.004+headshift.y,z+h))
accessory('Plain dark hat band',verts,[(i,(i+1)%N,N+(i+1)%N,N+i) for i in range(N)],band,'head')
# Bracelet lies around the forearm just above the wrist, and follows that bone.
a=heads['lowerarm_r'];b=heads['hand_r'];axis=(b-a).normalized();center=b-axis*.025
u=axis.cross(Vector((0,0,1))).normalized();v=axis.cross(u).normalized();verts=[]
for i in range(20):
    t=i*math.tau/20;radial=math.cos(t)*u+math.sin(t)*v
    for j in range(6):
        s=j*math.tau/6;verts.append(center+radial*(.022+.004*math.cos(s))+axis*.007*math.sin(s))
faces=[(i*6+j,((i+1)%20)*6+j,((i+1)%20)*6+(j+1)%6,i*6+(j+1)%6) for i in range(20) for j in range(6)]
accessory('Single gold wrist bracelet',verts,faces,gold,'lowerarm_r')
# The reference's extra upper-spine joint needs matching cervical anatomy.
bone_mat=body.data.materials[0]
for zz in (1.36,1.40,1.44):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,location=(0,.047,zz))
    o=bpy.context.object;o.name='Upper vertebra';o.scale=(.028,.026,.021)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for c in list(o.users_collection):c.objects.unlink(o)
    character.objects.link(o);o.data.materials.append(bone_mat)
    for loop in o.data.uv_layers.active.data:loop.uv=(1.5/8,.5)
    group=o.vertex_groups.new(name='spine_03');group.add(list(range(len(o.data.vertices))),1,'REPLACE');parts.append(o)
bpy.ops.object.select_all(action='DESELECT');body.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join()

# Bake the seated performance to the reference hierarchy without editing its rest pose.
rig.animation_data_create();action=bpy.data.actions.new('A_PierSkeleton_SeatedIdle_Gentleman_8s');rig.animation_data.action=action
def orient(n,direction):
    pb=rig.pose.bones[n];pos=(W@pb.matrix).translation
    q=(ends[n]-heads[n]).rotation_difference(Vector(direction))
    pb.matrix=WI@Matrix.Translation(pos)@q.to_matrix().to_4x4()@rest[n].to_3x3().to_4x4()
    bpy.context.view_layer.update()
def elbow(a,c,l1,l2,pole):
    d=c-a;dist=min(d.length,l1+l2-.0001);u=d.normalized();along=(l1*l1-l2*l2+dist*dist)/(2*dist)
    v=Vector(pole);v=(v-u*v.dot(u)).normalized();return a+u*along+v*math.sqrt(max(0,l1*l1-along*along))
for frame in range(1,194):
    scene.frame_set(frame)
    rig.matrix_world=W
    rig.keyframe_insert('scale',frame=frame)
    rig.keyframe_insert('location',frame=frame)
    rig.keyframe_insert('rotation_euler',frame=frame)
    for pb in rig.pose.bones:pb.rotation_mode='QUATERNION';pb.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    for pb in rig.pose.bones:
        n=pb.name
        if n not in align:continue
        pos=(W@pb.matrix).translation
        if n=='pelvis':pos=poses[frame]['pelvis'].translation.copy()
        delta=poses[frame][n].to_quaternion()@oldrest[n].to_quaternion().inverted()@align[n].inverted()
        # An emotionally neutral, level stare, not a nod or a searching head turn.
        if n=='head':delta=Matrix.Identity(3).to_quaternion()
        pb.matrix=WI@Matrix.Translation(pos)@delta.to_matrix().to_4x4()@rest[n].to_3x3().to_4x4()
        bpy.context.view_layer.update()
    hip=(W@rig.pose.bones['pelvis'].matrix).translation
    for sign,side in [(1,'l'),(-1,'r')]:
        shoulder=(W@rig.pose.bones['upperarm_'+side].matrix).translation
        wrist=hip+Vector((sign*.17,-.27,.042))
        L1=(heads['lowerarm_'+side]-heads['upperarm_'+side]).length
        L2=(heads['hand_'+side]-heads['lowerarm_'+side]).length
        e=elbow(shoulder,wrist,L1,L2,(sign,0,-.1))
        orient('upperarm_'+side,e-shoulder);orient('lowerarm_'+side,wrist-e)
        orient('hand_'+side,Vector((0,-.09,-.012)))
    for pb in rig.pose.bones:
        pb.keyframe_insert('location',frame=frame);pb.keyframe_insert('rotation_quaternion',frame=frame);pb.keyframe_insert('scale',frame=frame)
for fc in action.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
    fc.modifiers.new('CYCLES')
action.use_fake_user=True
rig['Notes']='Actual exported Gentleman armature; rest hierarchy preserved. Unreal compatibility pending import verification.'
# Palette remains packed and is provided alongside the FBXs.
for im in bpy.data.images:
    if im.name.startswith('Skeleton_Palette'):
        im.filepath_raw=str(OUT/'Skeleton_Palette.png');im.save();im.pack()
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
rig.data.pose_position='REST'
bpy.ops.export_scene.fbx(filepath=str(OUT/'SK_PierSkeleton_GentlemanRig.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z')
rig.data.pose_position='POSE';scene.frame_end=193
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_SeatedIdle.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
scene.frame_end=192;scene.frame_set(1)
rig.matrix_world=W
bpy.context.view_layer.update()
rig.name='Gentleman_Reference_Rig'
readme=bpy.data.texts.get('START HERE');readme.clear();readme.write('REVISION 02\nSlimmer head and ribs; leather hat; one gold bracelet; no earring.\nGentleman reference armature retained without rest-bone edits.\nPress Space for seated idle. Preview dock/water are not exported.\nUnreal import compatibility remains unverified. Original Prototype folder is intact.\n')
scene.render.filepath=str(OUT/'SeatedIdle_Preview.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_SeatedIdle.blend'))
bpy.ops.render.render(write_still=True)
signature={b.name:{'parent':b.parent.name if b.parent else None,'matrix':[list(r) for r in b.matrix_local]} for b in rig.data.bones}
report={'bones':len(rig.data.bones),'reference_rest_hierarchy_unchanged':signature==reference_signature,'vertices':len(body.data.vertices),'polygons':len(body.data.polygons),'unweighted_vertices':sum(not v.groups for v in body.data.vertices),'rig_object_transform':[list(r) for r in W],'unreal_import_verified':False}
(OUT/'validation.json').write_text(json.dumps(report,indent=2));print('REVISION_REPORT',json.dumps(report))
