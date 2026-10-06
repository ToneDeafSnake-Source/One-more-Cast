"""Read-only probe of UE 5.7 Python asset-authoring surfaces."""
import unreal,json
from pathlib import Path
names=[n for n in dir(unreal) if any(k in n.lower() for k in ('enumfactory','structfactory','structurefactory','datatablefactory','userdefinedstruct','userdefinedenum','datasmith'))]
factories={}
for n in names:
 try:
  cls=getattr(unreal,n)
  if isinstance(cls,type):factories[n]=[x for x in dir(cls) if any(k in x.lower() for k in ('create','add','property','enum','structure','struct','row'))][:30]
 except Exception as exc:factories[n]=str(exc)
r={'names':names,'factories':factories}
out=Path(unreal.Paths.project_dir())/'Saved/CodexCatchJournal/catalog_authoring_probe.json'
out.write_text(json.dumps(r,indent=2))
unreal.log('CODEX_CATALOG_PROBE '+json.dumps(r))
