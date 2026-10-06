# Pier Skeleton — Revision 02

Open `PierSkeleton_SeatedIdle.blend` and press Space to preview the eight-second seated idle. The original `../Prototype` files are untouched.

## This revision

- Narrower skull and rib cage; similar character height rather than matching the Gentleman's clothed bulk.
- Removed the earring. Added a small, low-crowned brown leather hat with one gently cocked side and a single gold wrist bracelet. This is a stylized sailor-inspired design, not an authenticated historical reconstruction.
- Level, steady, empty gaze over the water. No animated head turn, bowed head, or overtly sad pose.
- Uses the actual armature imported from the Gentleman reference export: 42 Blender bones, with original bone names, parents and rest matrices preserved. This is the Polygon Pirates UE4-based rig, not UE5 Manny.
- Adapted rigid bone weights and rebaked the seated performance. The reference has fewer finger chains; ring/pinky geometry follows its hand bones. No additional finger bones were added.

## Files

- `PierSkeleton_SeatedIdle.blend`: editable scene, rig, animation, packed bone palette and materials.
- `SK_PierSkeleton_GentlemanRig.fbx`: rest-pose character, rig and bone/accessory materials.
- `A_PierSkeleton_SeatedIdle.fbx`: character and eight-second baked animation, 24 fps, repeated endpoint at frame 193.
- `Skeleton_Palette.png`: bone texture. Hat and bracelet use simple material colors; metallic/roughness setup may need recreating in Unreal.
- `SeatedIdle_Preview.png`, `Idle_Frame_049.png`, `Idle_Frame_145.png`: rendered previews.
- `validation.json`, `animation_checks.json`: checks from Blender.

Only the character mesh and armature are exported. The dock, water, lights and camera are preview scenery. Enable viewport overlays to see the rig; switch the armature to Rest Position to inspect standing proportions.

## Validation and remaining work

Blender checks cover all 193 animation samples for finite bone transforms, matching loop endpoints, fixed armature transform, sensible world-space bounds and assigned weights. A fresh FBX import into Blender checks the bone names, parents and world-space joint positions against the reference armature.

**Unreal import / shared-skeleton compatibility is not yet tested.** Do not approve a prompt that would regenerate or overwrite the existing Gentleman skeleton. The next step is a separately authorized isolated import test, verifying scale, hierarchy, materials and the animation without changing the existing skeleton asset. Blender round-trip validation alone does not establish Unreal compatibility.

No Unreal Content assets, gameplay Blueprints, skeleton assets or maps were changed. Stand-up, walking, disappearance/respawn and the NPC timer are not implemented. There are no animator-friendly IK controls yet; this is a deform rig with a baked idle.
