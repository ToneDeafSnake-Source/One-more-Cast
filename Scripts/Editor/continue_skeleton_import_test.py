"""Recover only the isolated test import; validate native sampled poses."""
import unreal, json, traceback, math
from pathlib import Path
ROOT = Path(unreal.Paths.project_dir())
DEST = '/Game/Core/NPCs/SkeletonNPC_ImportTest'
report = {'errors': [], 'animations': []}
try:
    unreal.SystemLibrary.execute_console_command(None, 'Interchange.FeatureFlags.Import.FBX 0')
    mesh = unreal.load_asset(DEST + '/SK_PierSkeleton_Test')
    assert mesh
    slots = mesh.get_editor_property('materials')
    skeleton = mesh.get_editor_property('skeleton')
    if not skeleton:
        ui = unreal.FbxImportUI()
        ui.automated_import_should_detect_type = False
        ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
        ui.import_as_skeletal = True
        ui.import_mesh = True
        ui.import_animations = False
        ui.import_materials = False
        ui.import_textures = False
        ui.create_physics_asset = False
        t = unreal.AssetImportTask()
        t.filename = str(ROOT / 'ArtSource/SkeletonNPC/Revision04_Cleanup/SK_PierSkeleton_GentlemanRig.fbx')
        t.destination_path = DEST
        t.destination_name = 'SK_PierSkeleton_Test'
        t.options = ui
        t.factory = unreal.FbxFactory()
        t.automated = True
        t.replace_existing = True
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
        mesh = unreal.load_asset(DEST + '/SK_PierSkeleton_Test')
        mesh.set_editor_property('materials', slots)
        skeleton = mesh.get_editor_property('skeleton')
    assert skeleton and skeleton.get_path_name().startswith(DEST + '/')
    slots = list(mesh.get_editor_property('materials'))
    for slot in slots:
        name = str(slot.get_editor_property('material_slot_name')).lower()
        material_name = 'M_Gold_Test' if 'gold' in name else 'M_Sockets_Test' if 'dark' in name or 'socket' in name else 'M_Ivory_Test'
        material = unreal.load_asset(DEST + '/' + material_name)
        assert material
        slot.set_editor_property('material_interface', material)
    mesh.set_editor_property('materials', slots)
    assert unreal.EditorAssetLibrary.save_loaded_asset(skeleton, only_if_is_dirty=False)
    assert unreal.EditorAssetLibrary.save_loaded_asset(mesh, only_if_is_dirty=False)
    report['skeleton'] = skeleton.get_path_name()
    for source, name in [
        ('Revision04_Cleanup/A_PierSkeleton_SeatedIdle.fbx', 'A_PierSkeleton_SeatedIdle_Test'),
        ('StandAndStepOff06_Polish/A_PierSkeleton_PolishedExit.fbx', 'A_PierSkeleton_Exit_Test')]:
        a = unreal.load_asset(DEST + '/' + name) if unreal.EditorAssetLibrary.does_asset_exist(DEST + '/' + name) else None
        if not a:
            ui = unreal.FbxImportUI()
            ui.automated_import_should_detect_type = False
            ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
            ui.import_mesh = False
            ui.import_as_skeletal = True
            ui.import_animations = True
            ui.skeleton = skeleton
            ui.anim_sequence_import_data.set_editor_property('use_default_sample_rate', False)
            ui.anim_sequence_import_data.set_editor_property('custom_sample_rate', 60)
            ui.anim_sequence_import_data.set_editor_property('snap_to_closest_frame_boundary', True)
            t = unreal.AssetImportTask()
            t.filename = str(ROOT / 'ArtSource/SkeletonNPC' / source)
            t.destination_path = DEST
            t.destination_name = name
            t.options = ui
            t.factory = unreal.FbxFactory()
            t.automated = True
            t.save = True
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
            a = unreal.load_asset(DEST + '/' + name)
        assert isinstance(a, unreal.AnimSequence), name + ' failed import'
        assert a.get_editor_property('skeleton') == skeleton
        unreal.EditorAssetLibrary.save_loaded_asset(a, only_if_is_dirty=False)
        length = a.get_editor_property('sequence_length')
        options = unreal.AnimPoseEvaluationOptions()
        samples = []
        for i in range(61):
            pose = unreal.AnimPoseExtensions.get_anim_pose_at_time(a, length*i/60, options)
            bones = [str(n) for n in unreal.AnimPoseExtensions.get_bone_names(pose)]
            points = {}
            for bone in ['root', 'pelvis', 'head', 'hand_l', 'hand_r', 'foot_l', 'foot_r']:
                assert bone in bones, bone
                tr = unreal.AnimPoseExtensions.get_bone_pose(pose, bone, unreal.AnimPoseSpaces.WORLD)
                xyz = [tr.translation.x, tr.translation.y, tr.translation.z]
                assert all(math.isfinite(v) for v in xyz)
                points[bone] = xyz
            samples.append(points)
        report['animations'].append({'path': a.get_path_name(), 'length': length,
            'bone_count': len(bones), 'finite_samples': len(samples),
            'first': samples[0], 'last': samples[-1],
            'root_displacement_cm': max(math.dist(s['root'],samples[0]['root']) for s in samples),
            'pelvis_displacement_cm': max(math.dist(s['pelvis'],samples[0]['pelvis']) for s in samples)})
    report['status'] = 'imported_and_pose_sampled'
except Exception:
    report['status'] = 'failed'
    report['errors'].append(traceback.format_exc())
(ROOT / 'Saved/CodexSkeletonImport/continuation_report.json').write_text(json.dumps(report, indent=2))
unreal.log('CODEX_CONTINUATION ' + json.dumps(report))
