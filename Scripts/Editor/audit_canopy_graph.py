import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir());lib=unreal.MaterialEditingLibrary
mat=unreal.load_asset('/Game/Core/Environment/CanopyMotion/M_Canopy_GentleMotion')
seen=set();rows=[]
def visit(node):
 if not node or node.get_path_name() in seen:return
 seen.add(node.get_path_name());inputs=lib.get_inputs_for_material_expression(mat,node)
 r={'node':node.get_name(),'class':node.get_class().get_name(),'pins':list(lib.get_material_expression_input_names(node)),'inputs':[n.get_name() if n else None for n in inputs]}
 for p in ['inputs','code','default_value','parameter_name','transform_type','transform_source_type']:
  try:r[p]=str(node.get_editor_property(p))
  except Exception:pass
 rows.append(r)
 for n in inputs:visit(n)
visit(lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET))
(root/'Saved/CodexCanopyInspection/graph.json').write_text(json.dumps(rows,indent=2))
exec((root/'Scripts/Editor/fix_canopy_collision.py').read_text())
unreal.log('CODEX_GRAPH '+json.dumps(rows))
