"""Summarize Unreal-native text exports for review; standard Python, no asset edits."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'Saved/CodexCatchJournal'
for asset in ([p.stem for p in OUT.glob('*.t3d')] if len(sys.argv)>1 else ('player','inventory','shop','spot','toast')):
    lines=(OUT/(asset+'.t3d')).read_text(encoding='utf-8-sig').splitlines()
    result=[]
    for line in lines:
        if re.match(r'   Begin Object Name=',line):
            result.append('\n'+line.strip())
        elif re.match(r'      Begin Object Name=',line):
            result.append(line.strip().split(' ExportPath=')[0])
        elif any(x in line for x in ('FunctionReference=','VariableReference=','CustomFunctionName=','NodeComment=','Brush=','Font=','WidthOverride=','HeightOverride=')):
            result.append(line.strip())
        elif 'CustomProperties Pin (' in line:
            name=re.search(r'PinName="([^"]+)"',line)
            links=re.search(r'LinkedTo=\((.*?)\)',line)
            default=re.search(r'DefaultValue="([^"]*)"',line)
            ident=re.search(r'PinId=(\w+)',line)
            if links or default:
                result.append('  '+(ident[1] if ident else '')+' '+(name[1] if name else '')+' '+('OUT ' if 'EGPD_Output' in line else '')+('-> '+links[1] if links else '')+(' default='+default[1] if default else ''))
    (OUT/(asset+'_graph_summary.txt')).write_text('\n'.join(result),encoding='utf-8')
print('Graph summaries written to',OUT)
