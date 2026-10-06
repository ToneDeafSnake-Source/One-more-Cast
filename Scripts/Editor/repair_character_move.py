"""Guarded native Unreal character relocation. Default: plan only.

Repair requires the verified backup plus a marker file named authorize_repair.txt.
Only assets inside CharactersUE4Mannequin are candidates; props stay in place.
Existing destination assets are removed ONLY if unreferenced and backed up.
"""
import hashlib
import json
import traceback
from pathlib import Path
import unreal

ROOT = Path(unreal.Paths.project_dir())
OUT = ROOT / 'Saved/AssetRepairBackups/GentlemanMove_2026-10-01'
SRC = '/Game/Core/Environment/PolygonPirates/Meshes/CharactersUE4Mannequin'
DST = '/Game/PolygonPirates/Meshes/CharactersUE4Mannequin'
EAL = unreal.EditorAssetLibrary
report = {'status': 'planning', 'plan': [], 'removed_unused_conflicts': [], 'moved': [], 'errors': []}

def path_file(asset):
    assert asset.startswith('/Game/')
    return ROOT / 'Content' / (asset[6:] + '.uasset')

def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()

def capture(obj):
    result = {'class': obj.get_class().get_name()}
    if isinstance(obj, unreal.SkeletalMesh):
        result['skeleton'] = str(obj.get_editor_property('skeleton').get_path_name())
        physics = obj.get_editor_property('physics_asset')
        result['physics'] = physics.get_path_name() if physics else None
        result['materials'] = [m.material_interface.get_path_name() if m.material_interface else None for m in obj.get_editor_property('materials')]
        assert result['materials'] and all(result['materials']), 'Working mesh has missing materials'
    return result

try:
    assert OUT.is_dir()
    reg = unreal.AssetRegistryHelpers.get_asset_registry()
    reg.search_all_assets(synchronous_search=True)
    source_data = reg.get_assets_by_path(SRC, recursive=True)
    assert source_data, 'No source character assets'
    for data in source_data:
        source = str(data.package_name)
        assert source.startswith(SRC + '/')
        if 'ObjectRedirector' in str(data.asset_class_path):
            continue
        dest = DST + source[len(SRC):]
        source_file = path_file(source)
        source_backup = OUT / 'Environment_PolygonPirates' / source[len('/Game/Core/Environment/PolygonPirates/'):]
        source_backup = source_backup.with_suffix('.uasset')
        assert source_backup.is_file() and sha(source_file) == sha(source_backup), f'Source changed since backup: {source}'
        obj = unreal.load_asset(source)
        assert obj and obj.get_path_name().split('.')[0] == source
        source_refs = [str(r) for r in EAL.find_package_referencers_for_asset(source, load_assets_to_confirm=False)]
        entry = {'source': source, 'destination': dest, 'snapshot': capture(obj), 'conflict': False, 'source_referencers': source_refs}
        if EAL.does_asset_exist(dest):
            conflict_file = path_file(dest)
            conflict_backup = (OUT / 'Original_PolygonPirates' / dest[len('/Game/PolygonPirates/'):]).with_suffix('.uasset')
            assert conflict_backup.is_file() and sha(conflict_file) == sha(conflict_backup), f'Destination changed since backup: {dest}'
            refs = [str(r) for r in EAL.find_package_referencers_for_asset(dest, load_assets_to_confirm=True)]
            entry.update(conflict=True, destination_referencers=refs)
            assert not refs, f'Destination still referenced; refusing deletion: {dest}: {refs}'
            old = unreal.load_asset(dest)
            assert old and old.get_class() == obj.get_class(), 'Conflicting asset class differs'
        report['plan'].append(entry)
    assert len(report['plan']) <= 100, 'Unexpected relocation scope'
    report['status'] = 'plan_ready'
    (OUT / 'character_move_plan.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    if (OUT / 'authorize_repair.txt').is_file():
        # Native rename may update referencing packages. Preserve each disk file first.
        for entry in report['plan']:
            for ref in entry['source_referencers']:
                if not ref.startswith('/Game/'):
                    continue
                disk = path_file(ref)
                if not disk.is_file():
                    disk = disk.with_suffix('.umap')
                assert disk.is_file(), f'Referencer file missing: {ref}'
                backup = OUT / 'ReferencingPackages' / disk.relative_to(ROOT / 'Content')
                backup.parent.mkdir(parents=True, exist_ok=True)
                if not backup.exists():
                    backup.write_bytes(disk.read_bytes())
                assert sha(disk) == sha(backup), f'Referencer backup mismatch: {ref}'
        report['status'] = 'repairing'
        # All collision/reference/backup guards passed before the first mutation.
        for entry in report['plan']:
            if entry['conflict']:
                assert EAL.delete_asset(entry['destination']), 'Native removal failed'
                report['removed_unused_conflicts'].append(entry['destination'])
            assert EAL.rename_asset(entry['source'], entry['destination']), f'Native relocation failed: {entry}'
            moved = unreal.load_asset(entry['destination'])
            assert moved and moved.get_path_name().split('.')[0] == entry['destination']
            assert EAL.save_loaded_asset(moved, only_if_is_dirty=False), 'Moved asset failed to save'
            report['moved'].append(entry['destination'])
        # Rename creates source-location redirectors; preserve them for saved callers.
        # Save only the target character folder and source redirectors.
        assert EAL.save_directory(DST, only_if_is_dirty=True, recursive=True)
        assert EAL.save_directory(SRC, only_if_is_dirty=True, recursive=True)
        report['status'] = 'repaired_native_relocation'
except Exception:
    report['status'] = 'failed'
    report['errors'].append(traceback.format_exc())
(OUT / 'character_move_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
unreal.log('CODEX_CHARACTER_REPAIR ' + json.dumps(report))
