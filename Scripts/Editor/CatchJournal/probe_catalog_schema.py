"""Inspect authoring APIs without changing project assets."""
import unreal,json
from pathlib import Path
r={}
r['candidate_names']=[n for n in dir(unreal) if any(k in n.lower() for k in ('structureeditor','structeditor','enumerator','enumeditor','blueprinteditor','datatablefunction','kismeteditor','editortable'))]
for n in ['StructureFactory','EnumFactory','UserDefinedStruct','UserDefinedEnum','DataTableFactory','DataTableFunctionLibrary','BlueprintEditorLibrary']:
 cls=getattr(unreal,n,None)
 if cls:
  r[n]={'doc':str(cls.__doc__)[:1000],'members':[x for x in dir(cls) if not x.startswith('_')][:100]}
out=Path(unreal.Paths.project_dir())/'Saved/CodexCatchJournal/catalog_schema_probe.json'
out.write_text(json.dumps(r,indent=2));unreal.log('CODEX_SCHEMA_PROBE '+str(out))
