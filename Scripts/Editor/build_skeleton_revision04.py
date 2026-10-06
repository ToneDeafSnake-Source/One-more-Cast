"""Reuse the earlier authoring helpers, preserving all prior deliverables."""
from pathlib import Path
source=Path(__file__).with_name('revise_skeleton_pose.py').read_text(encoding='utf-8')
source=source.replace("OUT=ROOT/'Revision03'","OUT=ROOT/'Revision04'")
# Hook before animation authoring, after the previous geometry pass has assembled.
marker="rig.data.pose_position='POSE';rig.animation_data_clear();rig.animation_data_create()"
assert source.count(marker)==1
geometry=r'''
# Flat ivory, separate dark cavities, unchanged gold bracelet.
def plain(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.9
    return m
ivory=plain('M_FlatIvory',(.82,.81,.77));dark=plain('M_SocketDark',(.045,.043,.039))
body.data.materials.append(ivory);ivory_index=len(body.data.materials)-1
for p in body.data.polygons:
    if 'Gold' not in body.data.materials[p.material_index].name:p.material_index=ivory_index
# Remove old head and only the two backward neck rods (not vertebrae).
bm=bmesh.new();bm.from_mesh(body.data);dl=bm.verts.layers.deform.active
headid=body.vertex_groups['head'].index;neckid=body.vertex_groups['neck_01'].index
remove={v for v in bm.verts if headid in v[dl].keys()}
unseen=set(bm.verts)
neck_removed=0
while unseen:
    v=unseen.pop();island={v};todo=[v]
    while todo:
        for e in todo.pop().link_edges:
            for w in e.verts:
                if w in unseen:unseen.remove(w);island.add(w);todo.append(w)
    if len(island)==14 and all(neckid in v[dl].keys() for v in island):remove.update(island);neck_removed+=1
bmesh.ops.delete(bm,geom=list(remove),context='VERTS');bm.to_mesh(body.data);bm.free()
assert neck_removed==2,neck_removed
parts=[];mat=ivory
sphere('Skull • rounded cranium',(0,.010,1.661),(.103,.100,.126),'head');skull=parts[-1]
for sign in [-1,1]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(sign*.042,-.080,1.655));cut=bpy.context.object;cut.scale=(.032,.056,.030)
    bpy.context.view_layer.objects.active=cut;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bpy.context.view_layer.objects.active=skull;mod=skull.modifiers.new('Smaller eye socket','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    mat=dark;sphere('Dark socket',(sign*.042,-.047,1.655),(.029,.020,.026),'head');mat=ivory
skull.vertex_groups['head'].add(list(range(len(skull.data.vertices))),1,'REPLACE')
sphere('Compact maxilla',(0,-.055,1.595),(.055,.037,.025),'head')
tube('Quiet jaw',[(-.067,.005,1.612),(-.065,-.035,1.559),(-.038,-.073,1.547),(0,-.080,1.545),(.038,-.073,1.547),(.065,-.035,1.559),(.067,.005,1.612)],.012,'head')
mat=dark
me=bpy.data.meshes.new('Nasal opening');me.from_pydata([(-.011,-.087,1.615),(.011,-.087,1.615),(0,-.091,1.637)],[],[(0,1,2)])
o=bpy.data.objects.new('Nasal opening',me);col.objects.link(o);finish(o,'head');mat=ivory
for j in range(9):
    for zz in [1.568,1.557]:
        bpy.ops.mesh.primitive_cube_add(size=1,location=((j-4)*.009,-.086+abs(j-4)*.001,zz));o=bpy.context.object;o.name='Small tooth';o.scale=(.007,.009,.007)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);finish(o,'head')
bpy.ops.object.select_all(action='DESELECT');body.select_set(True)
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join()
# Bind the extra stylized fingers to the available middle-finger chain.
for v in body.data.vertices:
    n=body.vertex_groups[max(v.groups,key=lambda g:g.weight).group].name
    if n.startswith('hand_'):
        side=n[-1];sign=1 if side=='l' else -1
        if sign*(v.co.x-heads['middle_01_'+side].x)>0:
            target='middle_02_'+side if sign*(v.co.x-heads['middle_02_'+side].x)>0 else 'middle_01_'+side
            body.vertex_groups[n].remove([v.index]);body.vertex_groups[target].add([v.index],1,'REPLACE')
# NPC-only proportion adjustment: preserve hierarchy, shorten arm chains by 12%.
oldrest={n:m.copy() for n,m in rest.items()}
armnames={}
for side in ['l','r']:
    names=[]
    def descendants(b):
        names.append(b.name)
        for c in b.children:descendants(c)
    descendants(rig.data.bones['upperarm_'+side]);armnames[side]=names
bpy.context.view_layer.objects.active=rig;body.select_set(False);rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for side,names in armnames.items():
    pivot=heads['upperarm_'+side]
    for n in names:
        b=rig.data.edit_bones[n]
        b.head=WI@(pivot+(W@b.head-pivot)*.88+Vector((0,0,-.025)))
        b.tail=WI@(pivot+(W@b.tail-pivot)*.88+Vector((0,0,-.025)))
bpy.ops.object.mode_set(mode='OBJECT')
rest={b.name:W@b.matrix_local for b in rig.data.bones};heads={n:m.translation.copy() for n,m in rest.items()}
for v in body.data.vertices:
    n=body.vertex_groups[max(v.groups,key=lambda g:g.weight).group].name
    if any(n in ns for ns in armnames.values()):
        side=n[-1];pivot=oldrest['upperarm_'+side].translation
        v.co=pivot+(v.co-pivot)*.88+Vector((0,0,-.025))
    elif n.startswith('clavicle'):
        # Blend the collarbone down into the lowered shoulder socket.
        v.co.z-=.025*min(1,abs(v.co.x)/.17)
# A slightly raised preview deck places the edge directly under the hands.
for o in scene.objects:
    if o.name.startswith('PREVIEW dock plank'):o.location.z+=.025
'''
source=source.replace(marker,geometry+'\n'+marker)
source=source.replace("action=bpy.data.actions.new('A_PierSkeleton_SupportedRecline_8s')","action=bpy.data.actions.new('A_PierSkeleton_EdgeRest_8s')")
start=source.index('    lean=Quaternion(');end=source.index('    for n,m in legs[f].items():',start)
source=source[:start]+'''    sway=1.2*math.sin(t)
    put('pelvis',Vector((0,.045,1.015)),Quaternion())
    # Different bends along the spine form a shallow relaxed curve.
    for n,angle in [('spine_01',-10),('spine_02',2),('spine_03',9),('neck_01',3)]:
        q=Quaternion((1,0,0),math.radians(angle+1.5*math.sin(t)))@Quaternion((0,1,0),math.radians(sway))
        put(n,pos(n),q)
    put('head',pos('head'),Quaternion((1,0,0),math.radians(-2+1.5*math.sin(t-.5)))@Quaternion((0,0,1),math.radians(2*math.sin(t))))
    for side in ['l','r']:put('clavicle_'+side,pos('clavicle_'+side),Quaternion((1,0,0),math.radians(6+1.5*math.sin(t))))
'''+source[end:]
source=source.replace("wrist=Vector((sign*.255,.47,.981))","wrist=Vector((sign*.235,-.008,1.003))")
source=source.replace("e=elbow(a,wrist,l1,l2,(sign,.3,0))","e=elbow(a,wrist,l1,l2,(sign*.12,.9,0))")
source=source.replace("target=basis(Vector((sign*.45,-1,0)),Vector((0,0,1)))","target=basis(Vector((0,-1,0)),Vector((0,0,1)))")
marker2="    contacts[f]={s:list(pos('hand_'+s)) for s in ['l','r']}"
source=source.replace(marker2,'''    for sign,side in [(1,'l'),(-1,'r')]:
        # Toe motion trails calf swing rather than pointing rigidly down.
        n='foot_'+side;m=W@rig.pose.bones[n].matrix
        q=Quaternion((1,0,0),math.radians(4*math.sin(t+(0 if sign==1 else 1.3)-.7)))
        rig.pose.bones[n].matrix=WI@Matrix.Translation(m.translation)@q.to_matrix().to_4x4()@m.to_3x3().to_4x4();bpy.context.view_layer.update()
        for digit in ['index','middle','thumb']:
            for j,angle in [(1,12),(2,48),(3,20)]:
                n=f'{digit}_0{j}_{side}';m=W@rig.pose.bones[n].matrix
                q=Quaternion((1,0,0),math.radians(angle))
                rig.pose.bones[n].matrix=WI@Matrix.Translation(m.translation)@q.to_matrix().to_4x4()@m.to_3x3().to_4x4();bpy.context.view_layer.update()
'''+marker2)
source=source.replace('REVISION 03\\nSupported recline, connected shoulders, smaller teeth, no hat, gold bracelet retained.', 'REVISION 04\\nEdge-supported upright slouch, flatter ivory, smaller sockets and revised skull. Shorter NPC arms; Manny retargeting NOT tested.')
source=source.replace('Original Gentleman rest rig retained.', 'Gentleman-derived hierarchy with NPC-only shorter-arm rest proportions.')
source=source.replace("'teeth_resized':teeth", "'new_small_teeth':18,'rear_neck_rods_removed':neck_removed,'arm_length_factor':.88")
exec(compile(source,str(Path(__file__)), 'exec'))
