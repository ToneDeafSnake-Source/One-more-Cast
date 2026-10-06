"""Read-only fresh-process inspection before repairing a moved skeletal mesh.

Run only after Seth closes the interactive Editor. Never saves or deletes assets.
"""
import json
import traceback
from pathlib import Path
import unreal

root = Path(unreal.Paths.project_dir())
report_dir = root / 'Saved' / 'AssetRepairBackups' / 'GentlemanMove_2026-10-01'
assert report_dir.is_dir(), 'Verified repair backup must already exist'
paths = [
    '/Game/PolygonPirates/Meshes/CharactersUE4Mannequin/SK_Chr_Gentleman_01',
    '/Game/Core/Environment/PolygonPirates/Meshes/CharactersUE4Mannequin/SK_Chr_Gentleman_01',
]
report = {'mode': 'read_only', 'assets': [], 'errors': []}
try:
    for path in paths:
        mesh = unreal.load_asset(path)
        assert isinstance(mesh, unreal.SkeletalMesh), f'Expected mesh at {path}'
        entry = {'path': mesh.get_path_name(), 'properties': {}}
        for name in ['skeleton', 'physics_asset', 'asset_import_data', 'asset_user_data', 'materials']:
            try:
                value = mesh.get_editor_property(name)
                if isinstance(value, unreal.Object):
                    entry['properties'][name] = value.get_path_name()
                else:
                    entry['properties'][name] = str(value)
            except Exception as error:
                entry['properties'][name] = {'unavailable': str(error)}
        try:
            entry['hard_referencers'] = [str(v) for v in unreal.EditorAssetLibrary.find_package_referencers_for_asset(path, load_assets_to_confirm=True)]
        except Exception as error:
            entry['referencer_error'] = str(error)
        report['assets'].append(entry)
    report['status'] = 'inspected_without_changes'
except Exception:
    report['status'] = 'failed'
    report['errors'].append(traceback.format_exc())
(report_dir / 'fresh_mesh_inspection.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
unreal.log('CODEX_GENTLEMAN_INSPECTION ' + json.dumps(report))
