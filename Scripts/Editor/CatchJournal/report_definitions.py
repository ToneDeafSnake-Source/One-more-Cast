"""Build a reviewable, deduplicated static-definition audit from native exports.
Reports only: does not choose categories or modify Unreal content.
"""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'Saved/CodexCatchJournal'
data=json.loads((OUT/'definitions.json').read_text(encoding='utf-8'))
def field(text,name,default=''):
    m=re.search(r'\b'+re.escape(name)+r'_\d+_[A-F0-9]+=("(?:\\.|[^"\\])*"|[^,)]+)',text)
    return m[1].strip('"') if m else default
groups={}
for spot in data['spots']:
    for raw in spot['entries']:
        ident=field(raw,'FishID')
        fish=field(raw,'bIsFishCatch')=='True'
        treasure=field(raw,'bIsTreasureCatch')=='True'
        junk=field(raw,'bIsJunkCatch')=='True'
        if not (fish or treasure) or junk:continue
        display=re.search(r'FishDisplayName_\d+_[A-F0-9]+=NSLOCTEXT\("(?:\\.|[^"\\])*", "(?:\\.|[^"\\])*", "((?:\\.|[^"\\])*)"\)',raw)
        entry={'ID':ident,'DisplayName':display[1] if display else field(raw,'FishDisplayName'),'Type':'Fish' if fish else 'Treasure','Category':field(raw,'JournalCategoryID'),'Sort':field(raw,'JournalSortOrder','0'),'Icon':field(raw,'FishIcon')}
        key=ident.casefold()
        group=groups.setdefault(key,{'ID':ident,'variants':[],'spots':[]})
        if entry not in group['variants']:group['variants'].append(entry)
        if spot['label'] not in group['spots']:group['spots'].append(spot['label'])
with (OUT/'catalog_review.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['ID','DisplayName','Type','Category','Sort','Icon','SourceSpots','VariantCount'])
    w.writeheader()
    for key,g in sorted(groups.items()):
        for v in g['variants']:w.writerow(dict(v,SourceSpots='; '.join(g['spots']),VariantCount=len(g['variants'])))
summary={'saved_spot_count':len(data['spots']),'unique_eligible_ids':len(groups),'fish_ids':sum(any(v['Type']=='Fish' for v in g['variants']) for g in groups.values()),'treasure_ids':sum(any(v['Type']=='Treasure' for v in g['variants']) for g in groups.values()),'ids_with_missing_category':[g['ID'] for g in groups.values() if any(v['Category'] in ('','None') for v in g['variants'])],'ids_with_conflicting_definitions':[g['ID'] for g in groups.values() if len(g['variants'])>1],'groups':groups}
(OUT/'catalog_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='groups'},indent=2))
