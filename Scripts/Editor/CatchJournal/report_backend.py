"""Generate review-only Markdown from exported evidence; never imports assets."""
import json, re
from pathlib import Path
root = Path(__file__).resolve().parents[3]
out = root / 'Saved/CodexCatchJournal/BackendReview'
data = json.loads((out / 'definitions.json').read_text())
def field(raw, name):
    match = re.search(r'\b'+name+r'_\d+_[A-F0-9]+=("(?:\\.|[^"\\])*"|[^,)]+)', raw)
    return match[1].strip('"') if match else ''
groups = {}
for spot in data['spots']:
    for raw in spot['entries']:
        fish, treasure = field(raw,'bIsFishCatch')=='True', field(raw,'bIsTreasureCatch')=='True'
        if not (fish or treasure) or field(raw,'bIsJunkCatch')=='True': continue
        ident = field(raw,'FishID')
        name = re.search(r'FishDisplayName_\d+_[A-F0-9]+=NSLOCTEXT\(".*?", ".*?", "(.*?)"\)',raw)
        values = (name[1] if name else field(raw,'FishDisplayName'), field(raw,'FishIcon'), 'Fish' if fish else 'Treasure',field(raw,'JournalCategoryID'),field(raw,'JournalSortOrder'))
        g = groups.setdefault(ident, {'variants':set(), 'spots':set(), 'tiers':set()})
        g['variants'].add(values); g['spots'].add(spot['label']); g['tiers'].add(spot['properties']['RequiredPassTier'])
lines = ['# Catch identity migration review — September 29, 2026','',
         'Proposals only; no ID/category changes applied. Tier membership below uses saved RequiredPassTier, not verified physical pier boundaries. Sort values are proposed alphabetical spacing within each category, not catch rarity. Confirm all membership, icons and obtainability before import.','',
         '| Current ID | Proposed ID | Display name | Type | Categories seen | Proposed category | Sort | Pass tiers | Spots | Issues |',
         '|---|---|---|---|---|---|---:|---|---|---|']
details=[]; counters={}
for ident,g in sorted(groups.items()):
    name,icon,kind,_,_=sorted(g['variants'])[0]
    tiers=sorted(g['tiers'])
    folder=re.search(r'/Pier_(\d)/',icon)
    proposed='Treasure' if kind=='Treasure' else ('Non_Exclusive' if '/All_Piers/' in icon else ('Pier_0'+folder[1] if folder else 'REVIEW'))
    counters[proposed]=counters.get(proposed,0)+10
    cats=', '.join(sorted({v[3] or '(blank)' for v in g['variants']}))
    issues=['category missing' if any(not v[3] for v in g['variants']) else '', 'category is a folder-based suggestion; approve physical membership']
    if len(g['variants'])>1: issues.append('metadata variants')
    assetpath=icon.split("'")[1] if "'" in icon else ''
    disk=root/'Content'/(assetpath.removeprefix('/Game/').split('.')[0]+'.uasset')
    issues.append('icon file exists' if disk.is_file() else 'VERIFY ICON')
    lines.append(f"| {ident} | {kind}_{ident} | {name} | {kind} | {cats} | {proposed} | {counters[proposed]} | {', '.join(tiers)} | {len(g['spots'])} | {'; '.join(filter(None,issues))} |")
    details += ['',f'## {ident}',f'- Icon: `{assetpath}`',f"- Spots: {', '.join(sorted(g['spots']))}",f'- Exact static variants: `{sorted(g["variants"])}`']
(root/'CATCH_JOURNAL_MIGRATION_REVIEW.md').write_text('\n'.join(lines+details)+'\n',encoding='utf-8')
terms=('FishID','FishDisplayName','FishIcon','JournalCategoryID','JournalSortOrder','ST_FishCatchEntry','BuildCaughtFishItem','ItemName','BaseName','ItemIcon','CatchJournalRecords','UpdateCatchJournal','AddItem','ShowRollOutcomeText')
index=['# Exported Core Blueprint usage index','', 'Text matches identify inspection locations, not proof that every matched node executes. Generated/merged graphs excluded. Scope: 31 Core Blueprints, not all project/plugin assets.','']
for path in sorted(out.glob('*_graph_summary.txt')):
    graph=''; found={}
    for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if line.startswith('Begin Object Name=') and 'ExportPath=' in line:
            graph=re.search(r'Name="([^"]+)"',line)[1]
        if '_MERGED' in graph or graph.startswith('ExecuteUbergraph'):continue
        for term in terms:
            if term in line:found.setdefault((graph,term),[]).append(number)
    if found:
        index += [f'## {path.stem}', '']
        for (graph,term),numbers in sorted(found.items()):
            index.append(f'- {graph} / {term}: summary lines '+', '.join(map(str,numbers)))
(out/'usage_index.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
print('Review and usage index generated:',len(groups),'IDs; tier sets', {i:sorted(g['tiers']) for i,g in groups.items()})
