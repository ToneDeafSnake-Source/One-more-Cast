"""Read-only fresh-process validation of saved isolated skeleton assets."""
import unreal, json, traceback, math
from pathlib import Path
D='/Game/Core/NPCs/SkeletonNPC_ImportTest/'
r={'errors':[],'animations':[]}
try:
    mesh=unreal.load_asset(D+'SK_PierSkeleton_Test')
    skeleton=unreal.load_asset(D+'SK_PierSkeleton_Test_Skeleton')
    assert mesh and skeleton and mesh.get_editor_property('skeleton')==skeleton
    r['materials']=[s.material_interface.get_path_name() for s in mesh.get_editor_property('materials')]
    assert len(r['materials'])==3 and all(p.startswith(D) for p in r['materials'])
    for name in ['A_PierSkeleton_SeatedIdle_Test','A_PierSkeleton_Exit_Test']:
        a=unreal.load_asset(D+name)
        assert a and a.get_editor_property('skeleton')==skeleton
        length=a.get_editor_property('sequence_length')
        opts=unreal.AnimPoseEvaluationOptions()
        opts.optional_skeletal_mesh=mesh
        points=[]
        for i in range(61):
            pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(a,length*i/60,opts)
            names=[str(n) for n in unreal.AnimPoseExtensions.get_bone_names(pose)]
            assert len(names)==43
            sample={}
            for bone in ['root','pelvis','head','foot_l','foot_r']:
                t=unreal.AnimPoseExtensions.get_bone_pose(pose,bone,unreal.AnimPoseSpaces.WORLD)
                xyz=[t.translation.x,t.translation.y,t.translation.z]
                assert all(math.isfinite(v) for v in xyz)
                sample[bone]=xyz
            points.append(sample)
        r['animations'].append({'name':name,'length':length,'samples':61,'first':points[0],'last':points[-1]})
    r['status']='saved_assets_reloaded_and_sampled'
except Exception:
    r['status']='failed';r['errors'].append(traceback.format_exc())
(Path(unreal.Paths.project_dir())/'Saved/CodexSkeletonImport/saved_validation.json').write_text(json.dumps(r,indent=2))
unreal.log('CODEX_SAVED_VALIDATION '+json.dumps(r))
