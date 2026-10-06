"""Change only the generated material's rear swing/flex direction."""
import unreal, json, shutil, hashlib
from pathlib import Path
root=Path(unreal.Paths.project_dir())
out=root/'Saved/CodexCanopyInspection/DirectionalWind';out.mkdir(parents=True,exist_ok=True)
folder=root/'Content/Core/Environment/CanopyMotion'
untouched=[folder/'SM_Canopy_GentleMotion.uasset',folder/'MI_Canopy_GentleMotion.uasset']
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in untouched}
src=folder/'M_Canopy_GentleMotion.uasset'
if not (out/src.name).exists():shutil.copy2(src,out/src.name)
mat=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion')
custom=unreal.find_object(None,mat.get_path_name()+':MaterialExpressionCustom_0')
code=custom.get_editor_property('code')
pairs=[('float ab= angle*(0.72*sin(t*0.85+0.35)+0.28*sin(t*1.31+0.7))*back;',
        'float ab=-angle*(0.72*sin(t*0.85)+0.28*sin(t*1.31+0.4))*back;'),
       ('result.y+=strength*EdgeCm*0.25*(front*front*sin(t*1.25-0.5)-back*back*sin(t*1.25-0.15));',
        'result.y+=strength*EdgeCm*0.25*(front*front+back*back)*sin(t*1.25-0.5);')]
for old,new in pairs:
 assert code.count(old)==1,'Unexpected material code; refusing unverified change'
 code=code.replace(old,new)
custom.set_editor_property('code',code)
unreal.MaterialEditingLibrary.recompile_material(mat)
assert unreal.EditorAssetLibrary.save_loaded_asset(mat,only_if_is_dirty=False)
assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in untouched}
(out/'result.json').write_text(json.dumps({'status':'saved','mesh_and_instance_unchanged':True,'changed_lines':2},indent=2))
unreal.log('CODEX_DIRECTION saved; mesh and material instance unchanged')
