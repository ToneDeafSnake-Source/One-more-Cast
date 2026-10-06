"""Export private reference copies only; never save Unreal assets."""
import unreal, json
from pathlib import Path
out=Path(unreal.Paths.project_dir())/'ArtSource/SkeletonNPC/Reference'
out.mkdir(parents=True,exist_ok=True)
mesh=unreal.load_asset('/Game/PolygonPirates/Meshes/CharactersUE4Mannequin/SK_Chr_Gentleman_01')
task=unreal.AssetExportTask()
task.object=mesh; task.filename=str(out/'Gentleman_reference.fbx')
task.automated=True; task.prompt=False
task.options=unreal.FbxExportOption()
task.options.ascii=False
ok=unreal.Exporter.run_asset_export_task(task)
report={'mesh_export':ok,'materials':[],'pier_meshes':[]}
for slot in mesh.get_editor_property('materials'):
    mat=slot.material_interface
    entry={'material':mat.get_path_name(),'textures':[]}
    for param in unreal.MaterialEditingLibrary.get_texture_parameter_names(mat):
        tex=unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(mat,param)
        if not tex:continue
        entry['textures'].append({'parameter':str(param),'asset':tex.get_path_name()})
        t=unreal.AssetExportTask();t.object=tex;t.filename=str(out/(tex.get_name()+'.tga'));t.automated=True;t.prompt=False
        unreal.Exporter.run_asset_export_task(t)
    report['materials'].append(entry)
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
levels.load_level('/Game/MainDock')
seen=set()
for actor in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    for comp in actor.get_components_by_class(unreal.StaticMeshComponent):
        sm=comp.static_mesh
        if sm and any(w in sm.get_name().lower() for w in ('pier','dock','jetty')) and sm.get_path_name() not in seen:
            seen.add(sm.get_path_name());report['pier_meshes'].append(sm.get_path_name())
            if len(seen)<=2:
                t=unreal.AssetExportTask();t.object=sm;t.filename=str(out/(sm.get_name()+'.fbx'));t.automated=True;t.prompt=False;t.options=unreal.FbxExportOption()
                unreal.Exporter.run_asset_export_task(t)
(out/'reference_report.json').write_text(json.dumps(report,indent=2))
unreal.log('CODEX_REFERENCE '+json.dumps(report))
