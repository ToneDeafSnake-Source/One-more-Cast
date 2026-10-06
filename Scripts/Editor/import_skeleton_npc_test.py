"""Isolated native FBX import. Never load/save existing gameplay assets."""
import unreal,json,traceback,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir());OUT=ROOT/'Saved/CodexSkeletonImport';OUT.mkdir(parents=True,exist_ok=True)
DEST='/Game/Core/NPCs/SkeletonNPC_ImportTest'
report={'destination':DEST,'assets':[],'errors':[]}
try:
 if unreal.EditorAssetLibrary.does_directory_exist(DEST):raise RuntimeError('Destination already exists; refusing to overwrite.')
 unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
 def task(filename,name,mesh,skeleton=None):
  ui=unreal.FbxImportUI();ui.set_editor_property('automated_import_should_detect_type',False)
  ui.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_SKELETAL_MESH if mesh else unreal.FBXImportType.FBXIT_ANIMATION)
  ui.set_editor_property('import_mesh',mesh);ui.set_editor_property('import_as_skeletal',True)
  ui.set_editor_property('import_animations',not mesh);ui.set_editor_property('import_materials',False);ui.set_editor_property('import_textures',False)
  ui.set_editor_property('create_physics_asset',False)
  if skeleton:ui.set_editor_property('skeleton',skeleton)
  if not mesh:
   ui.anim_sequence_import_data.set_editor_property('use_default_sample_rate',False)
   ui.anim_sequence_import_data.set_editor_property('custom_sample_rate',60)
  t=unreal.AssetImportTask();t.filename=str(filename);t.destination_path=DEST;t.destination_name=name;t.automated=True;t.replace_existing=False;t.save=True;t.options=ui;t.factory=unreal.FbxFactory()
  unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);paths=list(t.imported_object_paths)
  report['assets']+=paths;unreal.log('CODEX_IMPORT '+str(paths));return [unreal.load_asset(p) for p in paths]
 meshresults=task(ROOT/'ArtSource/SkeletonNPC/Revision04_Cleanup/SK_PierSkeleton_GentlemanRig.fbx','SK_PierSkeleton_Test',True)
 mesh=next(a for a in meshresults if isinstance(a,unreal.SkeletalMesh));skel=mesh.get_editor_property('skeleton')
 assert skel.get_path_name().startswith(DEST+'/')
 report['mesh']=mesh.get_path_name();report['skeleton']=skel.get_path_name()
 report['bounds']=str(mesh.get_bounds());report['material_slots']=[str(x.material_slot_name) for x in mesh.get_editor_property('materials')]
 for file,name in [('Revision04_Cleanup/A_PierSkeleton_SeatedIdle.fbx','A_PierSkeleton_SeatedIdle_Test'),('StandAndStepOff06_Polish/A_PierSkeleton_PolishedExit.fbx','A_PierSkeleton_Exit_Test')]:
  assets=task(ROOT/'ArtSource/SkeletonNPC'/file,name,False,skel)
  for a in assets:
   if isinstance(a,unreal.AnimSequence):
    report.setdefault('animations',[]).append({'path':a.get_path_name(),'length':a.get_editor_property('sequence_length'),'skeleton':a.get_editor_property('skeleton').get_path_name()})
 # Flat materials authored only in the isolated test folder.
 mats={}
 for name,color,metal in [('M_Ivory_Test',(.82,.81,.77),0),('M_Sockets_Test',(.045,.043,.039),0),('M_Gold_Test',(.60,.35,.075),.72)]:
  m=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,DEST,unreal.Material,unreal.MaterialFactoryNew())
  c=unreal.MaterialEditingLibrary.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);c.set_editor_property('constant',unreal.LinearColor(*color,1))
  unreal.MaterialEditingLibrary.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
  for prop,val in [(unreal.MaterialProperty.MP_ROUGHNESS,.35 if metal else .9),(unreal.MaterialProperty.MP_METALLIC,metal)]:
   node=unreal.MaterialEditingLibrary.create_material_expression(m,unreal.MaterialExpressionConstant);node.set_editor_property('r',val);unreal.MaterialEditingLibrary.connect_material_property(node,'',prop)
  unreal.MaterialEditingLibrary.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m);mats[name]=m
 slots=mesh.get_editor_property('materials')
 for slot in slots:
  n=str(slot.material_slot_name).lower();slot.material_interface=mats['M_Gold_Test' if 'gold' in n else 'M_Sockets_Test' if 'dark' in n or 'socket' in n else 'M_Ivory_Test']
 mesh.set_editor_property('materials',slots);unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 report['animation_api']=[x for x in dir(unreal.AnimPoseExtensions) if 'bone' in x or 'pose' in x] if hasattr(unreal,'AnimPoseExtensions') else []
 report['status']='imported'
 try:
  options=unreal.AnimPoseEvaluationOptions()
  evaluated=[]
  for item in report['animations']:
   a=unreal.load_asset(item['path']);length=item['length'];samples=[];finite=True;bone_names=[]
   for i in range(61):
    pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(a,length*i/60,options)
    if i==0:bone_names=[str(n) for n in unreal.AnimPoseExtensions.get_bone_names(pose)]
    points={}
    for bone in ['root','pelvis','head','hand_l','hand_r','foot_l','foot_r']:
     tr=unreal.AnimPoseExtensions.get_bone_pose(pose,bone,unreal.AnimPoseSpaces.WORLD)
     xyz=[tr.translation.x,tr.translation.y,tr.translation.z];finite &= all(math.isfinite(v) for v in xyz);points[bone]=xyz
    samples.append(points)
   evaluated.append({'path':item['path'],'finite':finite,'bones':bone_names,'first':samples[0],'middle':samples[30],'last':samples[-1],'root_max_displacement_cm':max(math.dist(x['root'],samples[0]['root']) for x in samples),'pelvis_max_displacement_cm':max(math.dist(x['pelvis'],samples[0]['pelvis']) for x in samples)})
  report['pose_evaluation']=evaluated
 except Exception:report['pose_evaluation_error']=traceback.format_exc()
except Exception:
 report['errors'].append(traceback.format_exc());report['status']='failed';unreal.log_error(report['errors'][-1])
(OUT/'import_report.json').write_text(json.dumps(report,indent=2));unreal.log('CODEX_SKELETON_IMPORT '+json.dumps(report))
