"""Revision 03: supported recline, connected shoulders and understated teeth."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
ROOT=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC');OUT=ROOT/'Revision03';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Revision02/PierSkeleton_SeatedIdle.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['Gentleman_Reference_Rig'];body=bpy.data.objects['SK_PierSkeleton_GentlemanRig'];col=body.users_collection[0]
W=rig.matrix_world.copy();WI=W.inverted();rest={b.name:W@b.matrix_local for b in rig.data.bones};heads={n:m.translation.copy() for n,m in rest.items()}
signature={b.name:(b.parent.name if b.parent else None,[list(r) for r in b.matrix_local]) for b in rig.data.bones}
legs={}
for f in range(1,194):
    scene.frame_set(f);legs[f]={b.name:(W@b.matrix).copy() for b in rig.pose.bones if b.name.startswith(('thigh','calf','foot','ball'))}
rig.data.pose_position='REST'
bm=bmesh.new();bm.from_mesh(body.data);layer=bm.verts.layers.deform.active
clav={g.index for g in body.vertex_groups if g.name.startswith('clavicle')}
clav.update(g.index for g in body.vertex_groups if g.name in ('spine_01','spine_02'))
remove=set()
for face in bm.faces:
    if 'Leather' in body.data.materials[face.material_index].name:remove.update(face.verts)
for v in bm.verts:
    if any(i in clav for i in v[layer].keys()):remove.add(v)
bmesh.ops.delete(bm,geom=list(remove),context='VERTS');bm.to_mesh(body.data);bm.free()
# Individual connected mesh islands let us resize teeth without touching the skull.
links={v.index:set() for v in body.data.vertices}
for e in body.data.edges:
    a,b=e.vertices;links[a].add(b);links[b].add(a)
unseen=set(links);teeth=0
while unseen:
    first=unseen.pop();island={first};todo=[first]
    while todo:
        for k in links[todo.pop()]:
            if k in unseen:unseen.remove(k);island.add(k);todo.append(k)
    vs=[body.data.vertices[i] for i in island];center=sum((v.co for v in vs),Vector())/len(vs)
    if len(vs)==8 and 1.535<center.z<1.585 and center.y<-.06:
        for v in vs:
            d=v.co-center;d.x*=.67;d.y*=.65;d.z*=.45
            v.co=Vector((center.x*.80,center.y+.008,1.558+(center.z-1.558)*.46))+d
        teeth+=1
assert teeth==13,teeth
mat=body.data.materials[0];parts=[]
def finish(o,n):
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o);o.data.materials.clear();o.data.materials.append(mat)
    uv=o.data.uv_layers.active or o.data.uv_layers.new()
    for loop in uv.data:loop.uv=(1.5/8,.5)
    g=o.vertex_groups.new(name=n);g.add(list(range(len(o.data.vertices))),1,'REPLACE');parts.append(o)
def sphere(name,p,scale,bone):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10,ring_count=6,location=p);o=bpy.context.object;o.name=name;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);finish(o,bone)
def rod(name,a,b,r,bone):
    a,b=Vector(a),Vector(b);bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=r,radius2=r*.9,depth=(b-a).length,location=(a+b)/2)
    o=bpy.context.object;o.name=name;o.rotation_mode='QUATERNION';o.rotation_quaternion=(b-a).to_track_quat('Z','Y');finish(o,bone)
def tube(name,points,r,bone):
    points=[Vector(p) for p in points];verts=[];faces=[];N=6
    for i,p in enumerate(points):
        tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized()
        for j in range(N):verts.append(p+r*(math.cos(j*math.tau/N)*u+math.sin(j*math.tau/N)*v))
    for i in range(len(points)-1):
        for j in range(N):faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o);finish(o,bone)
# A coherent stylized cage deforms as one rigid unit; no split-row seams.
for i,width in enumerate([.105,.13,.145,.146,.131,.103]):
    z=1.35-i*.037
    for sign in [-1,1]:
        pts=[]
        for k in range(17):
            t=k*math.pi/16;pts.append((sign*width*math.sin(t),.064-.145*(1-math.cos(t))/2,z-.020*k/16))
        tube('Unified rib cage',pts,.010,'spine_02')
rod('Sternum',(0,-.081,1.335),(0,-.081,1.145),.015,'spine_02')
for z in [1.02,1.065,1.11,1.155,1.20,1.245,1.29,1.335]:
    sphere('Connected spine',(0,.055,z),(.027,.024,.023),'spine_02' if z>1.15 else 'spine_01')
for sign,side in [(1,'l'),(-1,'r')]:
    joint=heads['upperarm_'+side]
    points=[Vector((sign*.012,-.068,1.342)),Vector((sign*.09,-.034,1.377)),joint+Vector((-sign*.025,-.012,.006)),joint]
    for a,b in zip(points,points[1:]):rod('Connected collarbone',a,b,.015,'clavicle_'+side)
    sphere('Shoulder socket',joint,(.038,.034,.032),'clavicle_'+side)
    a=heads['upperarm_'+side];b=heads['lowerarm_'+side]
    rod('Humeral neck',a,a+(b-a)*.15,.020,'upperarm_'+side)
    sphere('Humeral head',a,(.029,.029,.030),'upperarm_'+side)
    rod('Scapular shoulder bridge',joint+Vector((-sign*.065,.017,-.075)),joint,.019,'clavicle_'+side)
bpy.ops.object.select_all(action='DESELECT');body.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join()
rig.data.pose_position='POSE';rig.animation_data_clear();rig.animation_data_create()
action=bpy.data.actions.new('A_PierSkeleton_SupportedRecline_8s');rig.animation_data.action=action
def put(n,pos,q):
    rig.pose.bones[n].matrix=WI@Matrix.Translation(pos)@q.to_matrix().to_4x4()@rest[n].to_3x3().to_4x4();bpy.context.view_layer.update()
def pos(n):return (W@rig.pose.bones[n].matrix).translation
def orient(n,d,child):put(n,pos(n),(heads[child]-heads[n]).rotation_difference(d))
def elbow(a,c,l1,l2,pole):
    d=c-a;dist=d.length;assert dist<l1+l2,(dist,l1+l2)
    u=d.normalized();along=(l1*l1-l2*l2+dist*dist)/(2*dist);v=Vector(pole);v=(v-u*v.dot(u)).normalized()
    return a+u*along+v*math.sqrt(max(0,l1*l1-along*along))
def basis(direction,up):
    x=direction.normalized();z=(up-x*up.dot(x)).normalized();y=z.cross(x);return Matrix((x,y,z)).transposed()
contacts={}
for f in range(1,194):
    scene.frame_set(f);rig.matrix_world=W
    for pb in rig.pose.bones:pb.rotation_mode='QUATERNION';pb.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update();t=(f-1)*math.tau/192
    lean=Quaternion((1,0,0),math.radians(-19+.3*math.sin(t)))
    put('pelvis',Vector((0,.045,1.015)),Quaternion())
    for n in ['spine_01','spine_02','spine_03','neck_01']:
        put(n,pos(n),lean)
    put('head',pos('head'),Quaternion((1,0,0),math.radians(-4)))
    for side in ['l','r']:put('clavicle_'+side,pos('clavicle_'+side),lean)
    for n,m in legs[f].items():rig.pose.bones[n].matrix=WI@m;bpy.context.view_layer.update()
    for sign,side in [(1,'l'),(-1,'r')]:
        phase=t+(0 if sign==1 else 1.3)
        swing=Quaternion((1,0,0),math.radians(5*math.sin(phase)))
        n='calf_'+side;m=W@rig.pose.bones[n].matrix
        rig.pose.bones[n].matrix=WI@Matrix.Translation(m.translation)@swing.to_matrix().to_4x4()@m.to_3x3().to_4x4()
        bpy.context.view_layer.update()
    for sign,side in [(1,'l'),(-1,'r')]:
        a=pos('upperarm_'+side);wrist=Vector((sign*.255,.47,.981))
        l1=(heads['lowerarm_'+side]-heads['upperarm_'+side]).length;l2=(heads['hand_'+side]-heads['lowerarm_'+side]).length
        e=elbow(a,wrist,l1,l2,(sign,.3,0))
        orient('upperarm_'+side,e-a,'lowerarm_'+side);orient('lowerarm_'+side,wrist-e,'hand_'+side)
        # Spread hands slightly outward, palm plane parallel to the dock.
        source=basis(heads['middle_01_'+side]-heads['hand_'+side],Vector((0,0,1)))
        target=basis(Vector((sign*.45,-1,0)),Vector((0,0,1)))
        put('hand_'+side,pos('hand_'+side),(target@source.transposed()).to_quaternion())
    contacts[f]={s:list(pos('hand_'+s)) for s in ['l','r']}
    for path in ['location','rotation_euler','scale']:rig.keyframe_insert(path,frame=f)
    for pb in rig.pose.bones:
        for path in ['location','rotation_quaternion','scale']:pb.keyframe_insert(path,frame=f)
for fc in action.fcurves:
    for key in fc.keyframe_points:key.interpolation='LINEAR'
    fc.modifiers.new('CYCLES')
action.use_fake_user=True
for im in bpy.data.images:
    if im.name.startswith('Skeleton_Palette'):im.filepath_raw=str(OUT/'Skeleton_Palette.png');im.save();im.pack()
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
# Keep the FBX armature-node naming consistent with the reference export.
rig.name='root';rig.data.pose_position='REST'
bpy.ops.export_scene.fbx(filepath=str(OUT/'SK_PierSkeleton_GentlemanRig.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z')
rig.data.pose_position='POSE';scene.frame_end=193
bpy.ops.export_scene.fbx(filepath=str(OUT/'A_PierSkeleton_SeatedIdle.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z')
rig.name='Gentleman_Reference_Rig';scene.frame_end=192;scene.frame_set(1)
readme=bpy.data.texts['START HERE'];readme.clear();readme.write('REVISION 03\nSupported recline, connected shoulders, smaller teeth, no hat, gold bracelet retained.\nSpace previews the eight-second idle. Original Gentleman rest rig retained.\nUnreal import remains unverified; scenery is preview-only.\n')
scene.render.filepath=str(OUT/'SeatedIdle_Preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PierSkeleton_SeatedIdle.blend'));bpy.ops.render.render(write_still=True)
now={b.name:(b.parent.name if b.parent else None,[list(r) for r in b.matrix_local]) for b in rig.data.bones}
report={'reference_rest_unchanged':signature==now,'teeth_resized':teeth,'hand_joint_max_drift_m':max(abs(contacts[f][s][i]-contacts[1][s][i]) for f in contacts for s in ['l','r'] for i in range(3)),'unreal_import_tested':False}
(OUT/'pose_checks.json').write_text(json.dumps(report,indent=2));print('POSE_CHECKS',report)
