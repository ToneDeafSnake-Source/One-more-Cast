const fs=require('fs');const path=require('path');
const sharp=require('C:/Users/concr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
async function main(){
 const source='C:/Users/concr/.codex/generated_images/01a0f89c-7bb8-7751-a71c-cb76e4afb3e6/exec-723cfb11-8d9e-42a9-a5a8-b97620e5f34b.png';
 const dest='L:/Game Projects/One More Cast/Images/UI/UI Images/CatchJournal/FrameReplacement';
 fs.mkdirSync(dest,{recursive:true});
 const file=path.join(dest,'frame_wood_v2_1366x740.png');
 if(fs.existsSync(file))throw Error('Replacement already exists; refusing overwrite');
 fs.copyFileSync(source,path.join(dest,'frame_wood_v2_generated_1704x923.png'));
 await sharp(source).resize(1366,740,{fit:'fill',kernel:'lanczos3'}).png().toFile(file);
 const {data,info}=await sharp(file).ensureAlpha().raw().toBuffer({resolveWithObject:true});
 let transparent=0;for(let i=3;i<data.length;i+=4)if(data[i]===0)transparent++;
 if(info.width!==1366||info.height!==740||!transparent)throw Error('Dimension/alpha check failed');
 const center=(370*1366+683)*4+3;if(data[center]!==0)throw Error('Center is not transparent');
 fs.copyFileSync(path.join(__dirname,'FRAME_V2_PROMPT.txt'),path.join(dest,'GENERATION_PROMPT.txt'));
 fs.writeFileSync(path.join(dest,'README.txt'), 'Frame v2 — October 1, 2026\n\nImport frame_wood_v2_1366x740.png as a NEW texture. Keep the old texture.\nGenerated using the built-in image tool from the old frame reference, at native 1704x923, then downsampled to the exact 1366x740 UMG slot. This is not a 2x-native-resolution render.\n\nUnreal: Uncompressed (RGBA8), Texture Group UI, sRGB on, Compress Without Alpha off, NoMipmaps if available. Confirm imported/displayed size is 1366x740 and that no Maximum Texture Size or LOD bias is reducing it.\n\nImg_Frame: replace only Appearance > Brush > Image. Draw As Image. Keep Canvas X=35, Y=100, Size=1366x740, alignment=0/0, ZOrder=20, Size to Content off. Keep decorative hit testing disabled.\n\nNo Photoshop needed to try this replacement. No corner ropes; title lashings remain. Transparent center and outer pixels verified. Native source provided for optional cleanup.\n');
 const result={file,width:info.width,height:info.height,transparentPixels:transparent,transparentCenter:true,nativeGeneratedSize:[1704,923],unrealImported:false};
 fs.writeFileSync(path.join(dest,'validation.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
}main().catch(e=>{console.error(e);process.exit(1);});
