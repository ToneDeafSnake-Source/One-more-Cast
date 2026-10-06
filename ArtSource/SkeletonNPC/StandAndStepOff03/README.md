# Exit pass 03 — weight transfer and falling follow-through

Open `PierSkeleton_StandPauseStepOff.blend` and press Space. Preview: `StandPauseStepOff_Preview.mp4`. Export: `A_PierSkeleton_StandPauseStepOff.fbx`.

The rise now shifts toward the supporting right hand to make room for the left leg, then shifts toward the planted left foot while the other leg comes up. Pelvis translation/bank, chest turn, shoulder tilt and head counterbalance overlap instead of holding one torso pose throughout the leg lifts. Small settling motions continue through the rise. The pause timing and hop trajectory from pass 02 are retained; airborne follow-through adds torso tip/rotation, arms floating out, uneven knee lift and ankle movement.

Seven seconds, 169 baked samples at 24 fps, smooth clamped interpolation. Starts at the cleaned idle's frame 1. Previous passes, model and idle preserved.

Checks: fresh-load finite transforms, matching starting pose, unchanged rest rig, full weights and final submersion. Frame-sampled calf/foot vertices do not enter the preview deck interior (same bounds/tolerances as pass 02). Standing soles remain at deck height. The arm solver clamps an at-most 0.6 mm overreach target rather than stretching bones. Visual key poses reviewed; perceived naturalness remains for Seth to assess in motion. These checks are not triangle collision sweeps or Unreal runtime tests.

Pelvis-baked travel remains NOT validated Unreal root motion. Runtime alignment, collision, splash, timer/despawn, transition blending and Manny retargeting are pending. No Unreal Content assets changed.
