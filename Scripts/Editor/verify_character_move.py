"""Fresh-process native reload/save verification after character relocation."""
import hashlib
import json
import traceback
from pathlib import Path
import unreal

root = Path(unreal.Paths.project_dir())
out = root / 'Saved/AssetRepairBackups/GentlemanMove_2026-10-01'
repair = json.loads((out / 'character_move_report.json').read_text(encoding='utf-8'))
report = {'status': 'checking', 'checked': [], 'errors': []}
src_prefix = '/Game/Core/Environment/PolygonPirates/Meshes/CharactersUE4Mannequin'
dst_prefix = '/Game/PolygonPirates/Meshes/CharactersUE4Mannequin'
def remap(path):
    return dst_prefix + path[len(src_prefix):] if path and path.startswith(src_prefix + '/') else path
try:
    assert repair['status'] == 'repaired_native_relocation', 'Repair incomplete'
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.search_all_assets(synchronous_search=True)
    registry.scan_paths_synchronous(['/Game'], force_rescan=True)
    reference_options = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True)
    for entry in repair['plan']:
        obj = unreal.load_asset(entry['destination'])
        assert obj and obj.get_path_name().split('.')[0] == entry['destination']
        assert obj.get_class().get_name() == entry['snapshot']['class']
        legacy_file = root / 'Content' / (entry['source'][6:] + '.uasset')
        if legacy_file.exists():
            legacy = unreal.load_asset(entry['source'])
            assert legacy == obj, f'Source redirector does not resolve to destination: {entry}'
        else:
            refs = registry.get_referencers(entry['source'], reference_options)
            assert not refs, f'Removed source path still referenced: {entry["source"]}: {[str(r) for r in refs]}'
        if isinstance(obj, unreal.SkeletalMesh):
            assert obj.get_editor_property('skeleton').get_path_name() == entry['snapshot']['skeleton']
            phys = obj.get_editor_property('physics_asset')
            assert (phys.get_path_name() if phys else None) == remap(entry['snapshot']['physics'])
            assert [m.material_interface.get_path_name() if m.material_interface else None for m in obj.get_editor_property('materials')] == entry['snapshot']['materials']
            assert obj.get_editor_property('asset_import_data').get_path_name().startswith(obj.get_path_name() + ':'), 'Import data owned by wrong mesh'
        # Exercise the operation that failed, in a fresh process.
        assert unreal.EditorAssetLibrary.save_loaded_asset(obj, only_if_is_dirty=False), f'Save still fails: {entry["destination"]}'
        report['checked'].append({'asset': entry['destination'], 'fresh_load': True, 'saved': True, 'old_path': 'redirector' if legacy_file.exists() else 'removed_after_reference_update'})
    bp = unreal.load_asset('/Game/Core/PlayerBlueprints/BP_Fisherman')
    assert bp
    cdo = unreal.get_default_object(bp.generated_class())
    comp = cdo.get_editor_property('mesh')
    mesh = comp.get_editor_property('skeletal_mesh_asset')
    report['player_mesh'] = mesh.get_path_name()
    assert report['player_mesh'] == dst_prefix + '/SK_Chr_Gentleman_01.SK_Chr_Gentleman_01'
    unchanged = 0
    updated_referencers = []
    allowed_updates = {r for e in repair['plan'] for r in e['source_referencers']}
    backup = out / 'Environment_PolygonPirates'
    for file in backup.rglob('*.uasset'):
        rel = file.relative_to(backup)
        if str(rel).replace('\\', '/').startswith('Meshes/CharactersUE4Mannequin/'):
            continue
        current = root / 'Content/Core/Environment/PolygonPirates' / rel
        assert current.is_file(), f'Non-character asset missing: {rel}'
        if hashlib.sha256(current.read_bytes()).digest() == hashlib.sha256(file.read_bytes()).digest():
            unchanged += 1
        else:
            package = '/Game/Core/Environment/PolygonPirates/' + str(rel.with_suffix('')).replace('\\', '/')
            assert package in allowed_updates, f'Unexpected non-character asset change: {rel}'
            updated_referencers.append(package)
    report['unchanged_non_character_environment_assets'] = unchanged
    report['updated_referencing_packages'] = updated_referencers
    report['status'] = 'fresh_reload_save_and_references_verified'
except Exception:
    report['status'] = 'failed'
    report['errors'].append(traceback.format_exc())
(out / 'character_move_validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
unreal.log('CODEX_CHARACTER_VALIDATION ' + json.dumps(report))
