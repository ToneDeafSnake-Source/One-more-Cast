# Pier Skeleton — Revision 03

Open `PierSkeleton_SeatedIdle.blend` and press Space for the eight-second looping idle.

This version removes the hat, retains the gold bracelet, reduces all 13 teeth, rebuilds the collarbones/shoulder sockets and rib cage, and leans the torso back with hands supporting it on the dock. The empty gaze stays nearly level. Legs have a small five-degree dangling swing with offset timing, plus a subtle torso shift. The user's photo was used for pose inspiration only; geometry remains the original stylized character.

The Gentleman reference armature's bone hierarchy and rest matrices are unchanged. Stylized connecting geometry fills the shoulder gaps without altering the reference skeleton. Earlier Prototype and Revision02 files are preserved. No Unreal assets were changed.

Files: editable `.blend`, rest mesh `SK_PierSkeleton_GentlemanRig.fbx`, animated `A_PierSkeleton_SeatedIdle.fbx`, packed/separate `Skeleton_Palette.png`, previews and check reports. The FBX contains only the character, not the preview pier/water. Gold material appearance may need configuring in Unreal.

Validation: Blender loop, finite transforms, weights, fixed armature, FBX rest hierarchy/joint round trip, and stable hand-joint positions. Hand joints stay within a micrometer of their targets during the loop; this does not establish collision-tested palm contact with a real Unreal pier.

Unreal import/shared-skeleton compatibility remains unverified. Do not regenerate the existing Gentleman skeleton during import. No stand-up/walk animations, timer, disappearance/respawn logic or IK authoring controls are implemented.
