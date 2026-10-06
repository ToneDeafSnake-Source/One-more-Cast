# Gentle canopy movement

## Place it

In Unreal's Content Browser, open `Content/Core/Environment/CanopyMotion`.
Drag **SM_Canopy_GentleMotion** into the level. Its movement material is already assigned; no Blueprint, wind actor, skeletal rig or animation clip is required.

Alternatively, select an existing canopy actor and change its Static Mesh to **SM_Canopy_GentleMotion**, retaining the actor's transform. Check its Materials overrides: an old palette-material override can hide the motion. Assign **MI_Canopy_GentleMotion** to Element 0 if necessary. No placed actors were automatically replaced.

View movement in Play/Simulate, or enable viewport Realtime (Ctrl+R). The effect is subtle at normal scale.

The initial no-motion defect is repaired: the duplicated palette material had an inherited **UseConstant=True** flag on World Position Offset, which ignored the connected animation graph. That flag is now cleared and saved. Seth's actor WPO setting was already correct. For new actors, the regular **Evaluate World Position Offset** setting should remain enabled.

## Adjust movement

Open **MI_Canopy_GentleMotion** (the material instance, not the parent material). Expand **Canopy Movement**, tick the checkbox beside a parameter to override it, change its value, and save.

| Parameter | Default | Effect |
|---|---:|---|
| Overall_Strength | 1.0 | Multiplies all motion. 0 stops it; 0.5 halves it. |
| Movement_Speed | 1.0 | Timing multiplier. Try 0.6 for slower drift or 1.3 for slightly livelier movement. 0 freezes the current time-independent wave shape; use Overall_Strength=0 to restore the unmoved shape. |
| Cloth_Ripple_cm | 1.2 | Main cloth's maximum combined vertical ripple before masking and overall strength. |
| Edge_Flutter_cm | 2.0 | Small coherent trailing flex on the flaps; no longer a traveling edge wave. Broad swing is controlled separately below. |
| Wave_Size_cm | 220 | Larger produces broader waves; smaller produces tighter ripples. Start between 150 and 350. |
| Phase_Offset | 0.0 | Changes wave timing independently of other material instances. Try 2 or 4 on another instance. |

Suggested calmer settings: Overall_Strength=0.65, Movement_Speed=0.7. Keep amplitudes modest: this is a visual material effect, not collision-aware cloth simulation. Motion values describe the unscaled mesh; actor transforms can affect world-space displacement.

### Gust revision

The existing instance's overrides were preserved: Overall_Strength=2, Movement_Speed≈1.217, Cloth_Ripple_cm=0.2336, Edge_Flutter_cm=5, Wave_Size_cm=500, Phase_Offset≈6.283. The table above lists parent defaults, not those overrides. Try Overall_Strength=1 if the new broad flap swing feels too lively.

New controls are under **Canopy Gusts**:

| Parameter | Default | Effect |
|---|---:|---|
| Flap_Swing_degrees | 7 | Broad front/back flap swing around their anchored folds, multiplied by overall strength and gust strength. |
| Gust_Speed | 1 | How quickly the breeze changes. Lower gives longer gradual gusts. 0 holds the gust level constant. |
| Speed_Variation | 0.45 | Amount of speeding up/slowing down. 0 gives steady timing; 0.9 is the maximum effective variation. |
| Strength_Variation | 0.4 | Amount of swelling/fading motion strength. 0 gives constant strength; effective maximum 0.9. |
| Gust_Offset | 0 | Shifts the gust pattern for duplicated material instances. |

These are smooth, deterministic overlapping cycles that feel irregular, not newly sampled random values. Movement_Speed affects all timing; 0 freezes motion. The timing integrates speed changes so gusts do not cause phase jumps. Both flaps share the same swing sign, timing and trailing-flex direction: on the front-to-back stroke, the front moves back/down and the rear back/up, rather than both spreading outward. Folds remain anchored and the rigid frame remains still. This is an inexpensive approximation, not physical cloth or collision-aware wind. Swing is safety-clamped to 25 degrees after strength multiplication; extreme settings still need visual checks.

Changing this instance affects every canopy using it. For independent control, duplicate **MI_Canopy_GentleMotion**, rename the copy, assign it to one canopy's Element 0, and edit the copy.

## Scope and limitations

The original harbor mesh, shared palette material and map were not edited. This variant preserves the original visible geometry/UVs and palette material logic, adds vertex weights, and uses material World Position Offset. Red weights animate the main cloth; green weights identify the front flap and blue the back flap; zero weights keep poles, ropes and support bands fixed. Loose flap corners no longer inherit the roof's side-edge pinning.

The Unreal mesh uses **Use Complex Collision As Simple**, matching the original harbor mesh (saved and reloaded). Collision does not deform with the cloth; verify blocking in the intended placement. Bounds now have a 30 cm extension. Large amplitudes, major rescaling, collision interaction and distant rendering need separate checks.

Current authoring source: `GustRevision/Canopy_Gusts.blend` and `GustRevision/SM_Canopy_GentleMotion.fbx`. Earlier source files are preserved. Runtime assets retain their names: `SM_Canopy_GentleMotion`, `M_Canopy_GentleMotion`, `MI_Canopy_GentleMotion`. Pre-revision asset copies are in `Saved/CodexCanopyInspection/GustRevision/Before`. No project C++ or gameplay Tick logic.

## Validation — September 30, 2026

Gust revision: fresh native reload confirmed existing overrides, five new controls, material assignment, and complex-as-simple collision. Offscreen Unreal renders at three controlled times show deformation without shader errors; the temporary test-time input was not saved. Round-trip checks preserve 1,263 vertices/2,482 triangles, position error <0.000001 m, mask error <0.004 and exactly zero weights on fixed geometry. Reports: `Saved/CodexCanopyInspection/GustRevision`; front renders: `RenderGusts`. No PIE, in-level walk-through, or packaged-build test.

Follow-up after Seth's report: confirmed the WPO constant-override defect through native text export and forced-displacement/mask renders. Cleared the override without changing the wave graph or default strengths. Fresh offscreen Unreal scene rendered phase 0/2/4 at strength 1 with visibly different fabric silhouettes. These frozen-phase renders verify deformation; they are not an in-game PIE or walk-through test. Collision mode also reloaded correctly. Final images/report: `Saved/CodexCanopyInspection/RenderFixed`.

Fresh Unreal process reloaded assets, verified assignment/parent/parameters and compiled the material with rendering enabled: 153 vertex and 201 pixel shader instructions, no material compilation errors found. Existing base-color graph does not directly consume the new vertex weights. Unreal-exported variant reimported into Blender retains 1,263 vertices/2,482 triangles; max vertex displacement from source below 0.000001 m, fixed weights zero, mask differences within 8-bit quantization. The commandlet's nonzero exit is from sandbox DDC access, not a material compile failure. No in-level visual playback or collision test was performed. Reports are in `Saved/CodexCanopyInspection`.
