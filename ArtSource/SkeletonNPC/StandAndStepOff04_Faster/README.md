# Exit animation — 20% faster

`PierSkeleton_StandPauseHop_Faster.blend`, `A_PierSkeleton_StandPauseHop_Faster.fbx`, and `Faster_Preview.mp4` contain the approved pass-03 motion at 1.2x speed. Duration: approximately 5.8333 seconds instead of 7 seconds. All poses and interpolation handles are identical; only playback timing changed. Scene effective frame rate is 28.8 fps (30 / 1.0416667), preserving every original sample.

Original pass 03 and the separate seated idle are unchanged. Use the original idle file for its 24 fps timing, not the idle action retained inside this faster scene. Timing verification is in `timing_checks.json`.

FBX import timing, UE5 Manny retargeting and Unreal root motion remain untested. Travel is still pelvis-baked. Do not apply an additional 1.2x playback multiplier to this already sped-up export unless intentionally making it faster again. No Unreal assets changed.
