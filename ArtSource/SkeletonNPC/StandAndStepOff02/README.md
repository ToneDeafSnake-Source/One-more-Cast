# Exit animation — smoother supported pass

Open `PierSkeleton_StandPauseStepOff.blend`, press Space. Preview: `StandPauseStepOff_Preview.mp4` (24 fps). FBX: `A_PierSkeleton_StandPauseStepOff.fbx`. The earlier StandAndStepOff clip and seated idle are preserved.

Seven seconds, 169 samples at 24 fps. Hand-supported tuck, sequential foot placement onto the deck, weight transfer and rise, short standing pause, small preparatory dip and approximately 7 cm hop forward, then drop into water.

Changes: continuous monotone motion paths instead of stopping at each waypoint; clamped smooth key handles; sagittal knee-bend direction; lift-clear-before-crossing foot paths; soles set to the actual preview deck height; hand release delayed until the first foot is planted; rise finishes only after both feet plant. Preview is now 24 fps rather than the previous 12 fps.

Checks: all 169 frame transforms finite; start matches cleaned idle frame 1; rest rig unchanged; complete weights; generated targets within limb reach. The calf/foot/ball vertices were checked against the preview deck's interior bounds at every frame: zero interior hits (3 mm top-surface tolerance). Standing soles measured approximately Z=0.975022 m versus deck top Z=0.975 m. This vertex/bounds check is not a full triangle collision test, inter-frame sweep, or Unreal runtime test. Major poses visually reviewed; perceived motion quality still needs Seth's review.

As before, displacement is baked into the pelvis, NOT validated Unreal root motion. In-game alignment, capsule/physics, Manny retargeting, splash, timer, disappearance/respawn and runtime transition blending remain pending. No Unreal assets were changed.
