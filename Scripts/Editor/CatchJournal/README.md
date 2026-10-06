# Catch Journal inspection tools

These tools inspect the saved project and generate reports; they do not author journal widgets or save game assets. Run only when Seth approves launching a separate headless Unreal process. Unsaved live Editor state is not included.

From the repository root, run each of `inspect_journal.py`, `inspect_details.py`, and `audit_definitions.py` using this pattern (substitute the script filename):

```powershell
& 'D:\UE5\UE_5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' 'G:/Unreal Projects/OneMoreCast/OneMoreCast.uproject' /Engine/Maps/Entry '-ExecutePythonScript=G:/Unreal Projects/OneMoreCast/Scripts/Editor/CatchJournal/inspect_journal.py' -unattended -nop4 -nosplash -NoSound -NullRHI -DDC-ForceMemoryCache -stdout -FullStdOutLogOutput
```

Forward slashes in the Python script argument avoid path escape interpretation. Memory-only derived-data cache avoids shared-cache permission trouble. Reports are written under Saved/CodexCatchJournal; rerunning replaces those generated reports, not Content assets.

Then run the report processors with standalone Python:

```powershell
& 'D:\UE5\UE_5.7\Engine\Binaries\ThirdParty\Python3\Win64\python.exe' Scripts/Editor/CatchJournal/summarize_exports.py
& 'D:\UE5\UE_5.7\Engine\Binaries\ThirdParty\Python3\Win64\python.exe' Scripts/Editor/CatchJournal/report_definitions.py
```

The map audit covers saved MainDock actors whose class is exactly BP_FishingSpot. It is not an exhaustive other-map/subclass/streaming audit. The native text parsers are project-specific inspection helpers, not full Unreal serialization parsers. The CSV is for review, not DataTable import; its SourceSpots column groups all occurrences of an ID rather than tracing individual metadata variants. Use definitions.json for precise source rows.

Do not text-edit/reimport exported Blueprints, patch binary assets, or interpret successful inspection as compilation/runtime validation. See the root CATCH_JOURNAL_CHATGPT_HANDOFF.md for verified findings and the manual continuation plan.
