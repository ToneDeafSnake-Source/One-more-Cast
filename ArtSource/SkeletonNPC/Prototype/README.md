# Pier Skeleton — seated-idle prototype

Open **PierSkeleton_SeatedIdle.blend** in Blender 4.3.2 or later. Hover over the 3D viewport and press Space to play the eight-second seated idle. Frame range 1–192 at 24 fps; frame 193 is the matching loop endpoint. If material preview takes time to initialize, use Material Preview or Rendered shading after loading.

## Included

- Original faceted skeleton mesh: 5,245 vertices / 5,184 polygons (not triangle count).
- 42-bone humanoid deformation rig including fingers and feet. This is a pose-bone rig, not an animator-friendly IK control rig, and not the exact UE4 mannequin hierarchy.
- Rigid vertex weights appropriate for separate hard bone pieces. No talking/jaw animation.
- Warm bone palette texture, packed into the blend and also provided as Skeleton_Palette.png. Minor color variation, not a detailed painted PBR texture set.
- A_PierSkeleton_SeatedIdle_8s action: small posture/head movement and gentle dangling-leg movement. No root drift.
- SK_PierSkeleton_Prototype.fbx: standing rest-pose rig and mesh, no animation.
- A_PierSkeleton_SeatedIdle.fbx: same character plus baked seated action, including repeated endpoint for eight-second duration.
- SeatedIdle_Preview.png and three additional pose previews.

The CHARACTER collection contains only the character mesh and rig. PREVIEW ONLY contains original stand-in dock boards, water plane, camera and lights; it is excluded from FBX exports. The preview pier is not a mesh copied from the game. It supplies a seating surface at approximately 0.95 m; position the actor accordingly when testing another pier. Character rest height is approximately 1.8 m, comparable to the exported Gentleman's approximately 1.83 m overall bounds. Match final placement against the actual chosen pier.

## Editing

Select PierSkeleton_Rig, enter Pose Mode and select a named bone. Existing idle channels are baked per frame; duplicate the action before authoring other clips. Switch Armature Data > Skeleton > Rest Position to view the standing rest pose, then switch back to Pose Position for animation. Enable viewport overlays to see/select bones; overlays are hidden in the saved presentation view. Mesh vertices are assigned to the bone pieces they belong to.

Change the packed palette image or material to recolor the character. The modest brass hoop and chipped tooth provide nautical character without clothing. All generated character geometry and texture are original; exported commercial-pack reference copies are kept separately in ../Reference and are not embedded in this blend/FBX.

## Validation performed

Fresh Blender process reopened the .blend. All 193 sampled frames have finite bone matrices, root motion is zero, endpoint matrices match exactly, and no mesh vertices are unweighted. Packed texture verified. Rendered frames 1, 49, 97 and 145 were inspected. See animation_checks.json and validation.json.

## Not finished or verified

No Unreal import, skeleton compatibility/retargeting, physics asset, collision, LODs, packaged-game validation, walk or stand-up clips, or gameplay timing/spawn/despawn behavior. FBX import orientation/material assignment still needs an Unreal test. Do not assign the Gentleman's existing Unreal Skeleton directly to this new rig; import with a new Skeleton when testing, then set up deliberate retargeting if desired.

This is the first art-direction prototype for Seth's approval. Next: review silhouette/style, then test import in an isolated folder before authoring a stand-up transition and walking animation. The gameplay loop (sit -> timer -> stand -> walk into water -> disappear/reappear) is a separate implementation stage.
