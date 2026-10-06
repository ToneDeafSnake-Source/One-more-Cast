# One More Cast — Codex Instructions

Read `ONE_MORE_CAST_CONTEXT.md` in this repository root before meaningful project work. It is the living technical handoff. Verify the actual implementation whenever the document is uncertain or conflicts with project files.

## Working approach

- This is Seth's Blueprint-only Unreal Engine 5.7 project. Preserve working systems and make focused, reusable changes. Do not add project C++ unless Seth and Codex first discuss the concrete benefit and Seth explicitly approves it. Do not make a broad shop/save rewrite without a task that calls for it.
- Use the current asset paths, field names, enums and data sources. Distinguish an existing asset/function from a verified working graph. Never mark an earlier assistant proposal as implemented without evidence.
- When guiding Seth through manual Blueprint work, explain what and why in plain language. Name the nodes, pin types, variables, inputs and outputs explicitly. Define prerequisites before using them, and work in manageable stages.
- `.uasset` and `.umap` files are binary. Use appropriate Unreal Editor tooling for asset changes; do not modify binary assets with text replacement. If graph inspection/editing is unavailable, explain the limitation and give precise manual steps.
- Unreal Editor control is case by case. Ask Seth before launching or controlling the Editor. Without approval or reliable Editor access, keep Blueprint graph work instructional and verify it through screenshots or Seth's reported results.
- Seth controls project file handling and Git. Do not pull, commit, create branches, merge, push, or otherwise change repository history/state unless Seth and Codex explicitly agree that Codex should handle that operation. Public GitHub `main` is the latest completed checkpoint and normally trails the active local work until Seth publishes at the end of the workday.
- For underspecified design choices, recommend an approach, explain its reasoning and tradeoffs, and wait for Seth's decision before implementing the choice. Keep proposals distinct from accepted design.
- Preserve the species/quality catch pipeline, complete `ST_ItemData` payload, fixed inventory slot indices, existing purchase router, and per-roll bait lifecycle.
- Current names include Catch Journal, Gambeetle, Shimmerworm, `BP_FishingRodMesh`, `LinkedRowID`, and `TotalCollected`. Consult the context document's historical-name table before renaming anything.
- Reuse `SavedCatchJournalRecords`; inspect its existing assignments before adding duplicate save fields. Save-system behavior must be tested, but old development/playtest saves do not require indefinite compatibility. Discuss and document any deliberate reset, migration, or `SaveVersion` change before changing saved structs, IDs or enums.
- Never claim compile, PIE, save/load or packaged-build checks passed unless they were run. Record what was checked and what remains unverified.

## Maintain local project memory

After completing a meaningful architecture, gameplay-system, save-data, UI-system or naming change:

1. Update the affected current-state sections of `ONE_MORE_CAST_CONTEXT.md`.
2. Replace superseded facts rather than appending contradictory versions.
3. Separate current implementation, accepted design, historical approaches and unresolved questions.
4. Update the current task, known-issue status and next steps.
5. Add a concise dated changelog entry identifying the change and validation result.

Keep this file short. Put detailed architecture and history in the context document. Do not copy changing game facts into several competing memory files. If the user asks only for analysis or a proposal, document that status without implying the game was changed.
