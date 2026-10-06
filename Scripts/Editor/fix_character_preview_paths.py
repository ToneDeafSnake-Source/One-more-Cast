"""Repair soft preview paths in already-relocated character packages, natively."""
import hashlib
import json
import traceback
from pathlib import Path
import unreal
root = Path(unreal.Paths.project_dir())
out = root / 'Saved/AssetRepairBackups/GentlemanMove_2026-10-01'
repair = json.loads((out / 'character_move_report.json').read_text(encoding='utf-8'))
report = {'changed': [], 'errors': []}
try:
    assert repair['status'] == 'repaired_native_relocation'
    mapping = {}
    objects = []
    packages = []
    before = {}
    for entry in repair['plan']:
        source, dest = entry['source'], entry['destination']
        mapping[unreal.SoftObjectPath(source + '.' + source.rsplit('/', 1)[1])] = unreal.SoftObjectPath(dest + '.' + dest.rsplit('/', 1)[1])
        obj = unreal.load_asset(dest)
        assert obj and obj.get_path_name().split('.')[0] == dest
        objects.append(obj)
        package = obj
        while package.get_outer() is not None:
            package = package.get_outer()
        assert isinstance(package, unreal.Package)
        packages.append(package)
        file = root / 'Content' / (dest[6:] + '.uasset')
        before[dest] = hashlib.sha256(file.read_bytes()).hexdigest()
    unreal.AssetToolsHelpers.get_asset_tools().rename_referencing_soft_object_paths(packages, mapping)
    for obj in objects:
        assert unreal.EditorAssetLibrary.save_loaded_asset(obj, only_if_is_dirty=True)
        dest = obj.get_path_name().split('.')[0]
        file = root / 'Content' / (dest[6:] + '.uasset')
        if hashlib.sha256(file.read_bytes()).hexdigest() != before[dest]:
            report['changed'].append(dest)
    report['status'] = 'soft_preview_paths_updated'
except Exception:
    report['status'] = 'failed'
    report['errors'].append(traceback.format_exc())
(out / 'preview_path_repair.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
unreal.log('CODEX_PREVIEW_PATH_REPAIR ' + json.dumps(report))
