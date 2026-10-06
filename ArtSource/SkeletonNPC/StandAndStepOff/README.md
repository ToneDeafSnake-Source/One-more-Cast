# Stand, pause, step off

Open `PierSkeleton_StandPauseStepOff.blend`, press Space. `StandPauseStepOff_Preview.mp4` is the studio-shaded motion preview. The separate baked FBX is `A_PierSkeleton_StandPauseStepOff.fbx`.

6.5-second nonlooping clip, 24 fps, frames 1–157:
- Hand-assisted lift and bringing the dangling feet onto the deck.
- Rise out of the crouch to standing by 3.6 seconds.
- Brief 0.7-second forward stare.
- Casual forward step, support release at about 5.12 seconds, downward drop below the preview water.

Starts exactly at frame 1 of the cleaned seated idle. The earlier idle and model files are preserved; the idle action is also retained in this Blender file. For runtime transitions from arbitrary idle phases, use a blend or a designated exit phase; matching frame 1 does not guarantee a seamless transition from every idle time.

The model and NPC-specific rest skeleton are unchanged. Blender checks: finite transforms for 157 frames, matching seated starting pose, unchanged rest hierarchy, complete weights, and character fully below preview water at the end. Generated hand/foot targets stay within limb reach; no geometry stretching was introduced to reach them. Key poses were visually reviewed. These are not full collision or runtime foot-contact tests.

Important integration boundary: this is a preview/baked animation, not an implemented Unreal NPC. Translation is baked in the pelvis; it is **not validated Unreal root motion**. Do not also move the actor along the same path without handling that translation. The authored pier edge is at Y=-0.13 m, deck top Z=0.975 m, ocean faces -Y in Blender. Actual in-game pier alignment, root-motion conversion or actor-motion coordination, capsule collision, splash, water entry, disappearance, timer and respawn all remain to implement. UE5 Manny retargeting and Unreal import remain untested.

No existing Unreal Content assets, map or gameplay systems were changed.
