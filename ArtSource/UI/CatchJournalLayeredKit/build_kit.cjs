// Mechanical alpha trimming, sizing, mirroring and QA assembly only.
// Artwork is generated separately using the built-in image tool.
const fs = require('fs');
const path = require('path');
const sharp = require('C:/Users/concr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = __dirname;
const manifest = JSON.parse(fs.readFileSync(path.join(root,'generation_manifest.json'),'utf8'));
const sizes = {
 frame_wood:[1400,740], rope_corner:[256,256],rope_header:[128,384],panel_parchment:[512,640],title_plaque:[1024,224],
 category_normal:[512,224],category_selected:[512,224],category_pointer:[64,128],entry_normal:[256,256],entry_selected:[256,256],
 icon_all_piers:[128,128],icon_pier_01:[128,128],icon_pier_02:[128,128],icon_pier_03:[128,128],icon_treasure:[128,128],
 close_background:[128,128],icon_close:[128,128],sort_background:[512,128],icon_dropdown:[64,64],detail_wash:[512,512],divider:[512,32]
};
const layout=[];
function item(name,x,y,w,h,z,asset,extra={}){layout.push({name,x,y,width:w,height:h,zOrder:z,asset,...extra});}
item('Backing',85,178,1270,585,0,'panel_parchment');
item('CategoriesPanel',88,180,250,580,1,'panel_parchment');
item('EntriesPanel',340,180,620,580,1,'panel_parchment');
item('DetailsPanel',962,180,390,580,1,'panel_parchment');
const cats=[['All Piers','icon_all_piers','5 / 16'],['Treasure','icon_treasure','0 / 1'],['Pier 1','icon_pier_01','3 / 6'],['Pier 2','icon_pier_02','2 / 7'],['Pier 3','icon_pier_03','0 / 3']];
for(let i=0;i<cats.length;i++){
 const y=205+i*102;item('Category_'+i,103,y,220,92,10,i===2?'category_selected':'category_normal');
 item('CategoryIcon_'+i,117,y+17,52,52,11,cats[i][1]);
}
item('CategoryPointer',315,424,20,40,12,'category_pointer');
item('SortBackground',768,202,164,38,10,'sort_background');item('SortArrow',906,213,18,18,11,'icon_dropdown');
for(let r=0;r<3;r++)for(let c=0;c<4;c++)item('Entry_'+r+'_'+c,367+c*144,258+r*154,136,142,10,r===0&&c===0?'entry_selected':'entry_normal');
item('DetailWash',1010,275,300,290,10,'detail_wash');
for(let i=0;i<3;i++)item('Divider_'+i,994,607+i*46,320,4,10,'divider');
item('Frame',20,100,1400,740,20,'frame_wood');
item('TitlePlaque',445,35,550,120,30,'title_plaque');item('TitleEmblem',492,68,60,50,31,'icon_all_piers');
item('CornerTL',10,94,120,140,40,'rope_corner_left');item('CornerTR',1310,94,120,140,40,'rope_corner_right');
item('CornerBL',10,718,120,140,40,'rope_corner_right');item('CornerBR',1310,718,120,140,40,'rope_corner_left');
item('TitleRopeL',430,27,64,155,40,'rope_header_left');item('TitleRopeR',945,27,64,155,40,'rope_header_right');
item('CloseButton',1335,114,64,64,50,'close_background');item('CloseGlyph',1350,129,34,34,51,'icon_close');
function escapeXml(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function label(x,y,t,size=23,color='#362313',anchor='start'){return `<text x="${x}" y="${y}" fill="${color}" font-size="${size}" font-family="Segoe UI,Arial,sans-serif" text-anchor="${anchor}">${escapeXml(t)}</text>`;}
async function main(){
 for(const d of ['Textures','Originals','Previews'])fs.mkdirSync(path.join(root,d),{recursive:true});
 const validation=[];
 for(const src of manifest.assets){
  fs.copyFileSync(src.path,path.join(root,'Originals',src.name+'.png'));
  const {data,info}=await sharp(src.path).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let minX=info.width,minY=info.height,maxX=-1,maxY=-1,zero=0,visible=0;
  for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){
   const a=data[(y*info.width+x)*4+3];if(a===0)zero++;if(a>8){visible++;minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y);}
  }
  if(!zero||!visible)throw Error('Invalid transparency: '+src.name);
  const [w,h]=sizes[src.name];
  const preserve = src.name.startsWith('icon_') || src.name.startsWith('rope_') || src.name === 'detail_wash';
  await sharp(src.path).extract({left:minX,top:minY,width:maxX-minX+1,height:maxY-minY+1}).resize(w,h,{fit:preserve?'contain':'fill',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(path.join(root,'Textures',src.name+'.png'));
  validation.push({name:src.name,width:w,height:h,sourceWidth:info.width,sourceHeight:info.height,sourceTransparentPixels:zero,alphaBoundingBox:{minX,minY,maxX,maxY}});
 }
 for(const [src,dst,flip] of [['rope_corner','rope_corner_left',false],['rope_corner','rope_corner_right',true],['rope_header','rope_header_left',false],['rope_header','rope_header_right',true]]){
  let p=sharp(path.join(root,'Textures',src+'.png'));if(flip)p=p.flop();await p.png().toFile(path.join(root,'Textures',dst+'.png'));
 }
 // Generic master ropes remain in Originals. Deliver only named placement variants.
 fs.unlinkSync(path.join(root,'Textures','rope_corner.png'));fs.unlinkSync(path.join(root,'Textures','rope_header.png'));
 fs.writeFileSync(path.join(root,'layout.json'),JSON.stringify({canvas:{width:1440,height:860},note:'Starting rectangles; category counts are illustrative, not catalog membership. Text is separate UMG.',elements:layout},null,2));
 const comps=[];
 for(const el of [...layout].sort((a,b)=>a.zOrder-b.zOrder)){
  let img=sharp(path.join(root,'Textures',el.asset+'.png')).resize(el.width,el.height);
  if(el.name==='TitleEmblem')img=img.linear([0.20,0.14,0.08,1],[0,0,0,0]);
  comps.push({input:await img.png().toBuffer(),left:el.x,top:el.y});
 }
 let txt=label(572,112,'Catch Journal',38);
 for(let i=0;i<cats.length;i++){const y=205+i*102;const col=i===2?'#fff4d7':'#362313';txt+=label(179,y+38,cats[i][0],24,col)+label(179,y+68,cats[i][2],19,col);}
 txt+=label(368,235,'Pier 1 (3 / 6)',25)+label(783,228,'Sort: Name',17)+label(1150,231,'Selected catch',27,'#362313','middle')+label(1150,261,'Type: Fish',19,'#126577','middle');
 txt+=label(1150,406,'YOUR CATCH ICON',20,'#126577','middle')+label(1150,433,'goes here',17,'#126577','middle');
 txt+=label(995,639,'Total Caught',21)+label(1311,639,'3',22,'#126577','end');
 txt+=label(995,685,'Best Weight',21)+label(1311,685,'2.4 lbs',22,'#126577','end');
 txt+=label(995,731,'Best Quality',21)+label(1311,731,'Legendary',22,'#126577','end');
 for(let r=0;r<3;r++)for(let c=0;c<4;c++){const x=435+c*144,y=258+r*154;txt+=label(x,y+73,r===0&&c===0?'Your icon':'???',19,'#71604a','middle')+label(x,y+125,r===0&&c===0?'Catch name':'???',17,'#362313','middle');}
 comps.push({input:Buffer.from(`<svg width="1440" height="860" xmlns="http://www.w3.org/2000/svg">${txt}</svg>`),left:0,top:0});
 const preview=await sharp({create:{width:1440,height:860,channels:4,background:'#738e96'}}).composite(comps).png().toBuffer();
 fs.writeFileSync(path.join(root,'Previews','assembled_layout.png'),preview);
 const files=fs.readdirSync(path.join(root,'Textures')).filter(x=>x.endsWith('.png'));
 const sw=1200,cellW=240,cellH=205,sh=Math.ceil(files.length/5)*cellH;const tiles=[];let captions='';
 for(let i=0;i<files.length;i++){const x=(i%5)*cellW,y=Math.floor(i/5)*cellH;tiles.push({input:await sharp(path.join(root,'Textures',files[i])).resize(218,155,{fit:'contain',background:'#70858c'}).png().toBuffer(),left:x+11,top:y+8});captions+=label(x+120,y+186,files[i].replace('.png',''),14,'#fff9ec','middle');}
 tiles.push({input:Buffer.from(`<svg width="${sw}" height="${sh}" xmlns="http://www.w3.org/2000/svg">${captions}</svg>`),left:0,top:0});
 await sharp({create:{width:sw,height:sh,channels:4,background:'#70858c'}}).composite(tiles).png().toFile(path.join(root,'Previews','contact_sheet.png'));
 for(const f of files){const meta=await sharp(path.join(root,'Textures',f)).metadata();if(!meta.hasAlpha)throw Error('Missing alpha '+f);}
 fs.writeFileSync(path.join(root,'validation.json'),JSON.stringify({textureCount:files.length,allTexturesHaveAlpha:true,unrealImported:false,compileOrPIETested:false,assets:validation},null,2));
 console.log(JSON.stringify({textureCount:files.length,preview:path.join(root,'Previews','assembled_layout.png')}));
}
main().catch(e=>{console.error(e);process.exit(1);});
