# Skeleton NPC — Unreal import handoff

## Ready to preview

Content Browser folder: `/Game/Core/NPCs/SkeletonNPC_ImportTest`

- `SK_PierSkeleton_Test`: cleaned character mesh.
- `SK_PierSkeleton_Test_Skeleton`: separate NPC skeleton; do not replace the Gentleman/Manny skeleton with this.
- `M_Ivory_Test`, `M_Sockets_Test`, `M_Gold_Test`: assigned flat bone, cavity and bracelet materials.
- `A_PierSkeleton_SeatedIdle_Test`: approximately 7.6833 seconds.
- `A_PierSkeleton_Exit_Test`: approximately 5.30 seconds, already sped up as approved. Preview at speed 1.0.

Open either animation in Unreal to preview. Nothing was placed in MainDock and no existing player or gameplay assets were changed. If the Content Browser was open during the external import, it may need a refresh/restart to discover the new files; save your own work before restarting.

## What was verified (September 30, 2026)

Native Unreal import and save, followed by a separate read-only process reloading the mesh, skeleton, three material assignments and both animations. Sampled 61 times per clip with the imported mesh: 43 bones including root, finite tracked bone positions, expected matching seated start and downward exit travel. Exit root stays fixed; motion is in the pelvis. Small idle endpoint sampling difference (roughly 0.12 mm at the sampled left foot) after frame snapping. No visual Unreal playback, PIE or packaged build test was performed.

Initial problems repaired: animation endpoints incompatible with 60 fps (enabled nearest-frame snapping), skeleton dependency not saved, material slot assignments not persisted. Source idle FBX duration was 7.68 s, not the previously described 8 s. Exit source 5.303 s rounds to 5.30 s. Source Blender files are unchanged.

Evidence: `Saved/CodexSkeletonImport/continuation_report.json` and `saved_validation.json`. Headless commandlets returned nonzero due to sandboxed cache-access errors; explicit validation reports succeeded using the memory-cache fallback. This is not a claim of a clean project-wide build.

## Still needed for the actual NPC

1. Visually check both clips and materials in Unreal, including shoulders/feet and the fall.
2. Create a separate Blueprint Actor with this skeletal mesh for the scripted pier NPC. A nonblocking decorative actor avoids pretending the pelvis animation moves a Character capsule. This is a recommendation, not implemented behavior.
3. Align to a selected pier. Source preview deck surface is 97.5 cm above the rig origin; source edge maps approximately to Unreal local Y=13 cm, with ocean/exit toward +Y. Use visual placement checks, not these numbers alone, on the actual pier.
4. Loop idle, then transition to exit after the chosen timer. Exit starts at idle phase zero: blend from the current pose or synchronize the transition to avoid a pop.
5. Play exit once at rate 1.0; coordinate splash, hide/despawn and later reappearance explicitly. Do not enable root motion expecting it to move the actor/collision: root remains fixed, pelvis travels approximately 2.27 m forward and 7.06 m downward from its seated start by the final frame.
6. Manny animation reuse requires a separate retarget setup. This test did not establish Manny compatibility or change the player's skeleton.

Approved source mesh/idle: `Revision04_Cleanup`. Approved exit: `StandAndStepOff06_Polish`. Older folders are preserved iterations, not the current export choice.
