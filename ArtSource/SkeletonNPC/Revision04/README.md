# Pier Skeleton — Revision 04

Open `PierSkeleton_SeatedIdle.blend` and press Space for the eight-second idle. `Idle_Motion_Preview.mp4` is a simplified studio-shaded motion preview; `SeatedIdle_Preview.png` shows the scene lighting. Prior revisions are unchanged.

## Changes

- More upright edge-supported pose, shallow curve through separate spine joints, lower shoulders, less outward elbow bend.
- Arms shortened to 88% of prior rest lengths on this NPC only. Hands placed beside the hips with curled fingers at the mock pier edge.
- Rebuilt rounder cranium, smaller carved eye sockets, compact jaw/teeth, no protruding cheek pieces.
- Both rear-facing neck cylinders removed; vertebrae retained.
- Uniform near-white ivory material, dark sockets and gold bracelet. No randomized face-color texture on the bones; geometric lighting variation remains.
- Upper-body shift and restrained head movement, staggered leg motion and delayed ankle motion.

## Rig and engine boundary

The hierarchy derives from the Gentleman's exported skeleton, but **rest proportions are now different**. The legacy FBX name `SK_PierSkeleton_GentlemanRig.fbx` does not imply direct shared-skeleton compatibility. Import as an isolated NPC skeleton; do not regenerate or overwrite the existing Gentleman skeleton. UE5 Manny animation reuse is intended through retargeting, not direct skeleton assignment. Neither Unreal import nor Manny retargeting has been tested.

The existing Gentleman, maps, Blueprints and Content assets were not modified. No stand-up/walk/gameplay timer work was done. Preview pier geometry is not exported. The pose is authored for this mock pier height/edge and will need placement alignment in the game.

## Checks

Blender validation covers all 193 samples, matching loop endpoints, finite transforms, fixed armature transform, complete vertex weights, and rest-FBX reimport bone hierarchy/joint consistency against this revision (not the original Gentleman). Hand-joint targets vary less than one micrometer. This is not a collision or exact finger-contact test; inspect the pose on the actual pier before integration.

The Blender file contains the current flat materials. The old packed palette remains available but is not used by the current ivory material. Unreal material setup may need recreating after import.
