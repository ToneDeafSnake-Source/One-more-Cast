"""Fast motion-review video, separate from the saved production scene."""
import bpy
from pathlib import Path
root=Path('G:/Unreal Projects/OneMoreCast/ArtSource/SkeletonNPC/Revision04')
bpy.ops.wm.open_mainfile(filepath=str(root/'PierSkeleton_SeatedIdle.blend'))
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=640
s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True
s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.background_type='WORLD';s.world.color=(.12,.18,.20)
s.frame_start=1;s.frame_end=192;s.frame_step=2;s.render.fps=12
s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='HIGH'
s.render.filepath=str(root/'Idle_Motion_Preview.mp4');bpy.ops.render.render(animation=True)
