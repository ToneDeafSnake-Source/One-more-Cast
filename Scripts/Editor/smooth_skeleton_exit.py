"""Second exit pass: supported transfers, clearance arcs, stable knees, small hop."""
from pathlib import Path
src=Path(__file__).with_name('animate_skeleton_exit.py').read_text()
src=src.replace("OUT=ROOT/'StandAndStepOff'","OUT=ROOT/'StandAndStepOff02'")
start=src.index('def channel(');end=src.index('def pos(',start)
src=src[:start]+'''def channel(t,keys):
 if t<=keys[0][0]:return keys[0][1]
 if t>=keys[-1][0]:return keys[-1][1]
 slopes=[(b-a)/(tb-ta) for (ta,a),(tb,b) in zip(keys,keys[1:])]
 tangents=[0]+[0 if slopes[i-1]*slopes[i]<=0 else 2*slopes[i-1]*slopes[i]/(slopes[i-1]+slopes[i]) for i in range(1,len(slopes))]+[0]
 for i,((ta,a),(tb,b)) in enumerate(zip(keys,keys[1:])):
  if t<=tb:
   h=tb-ta;u=(t-ta)/h
   return (2*u**3-3*u*u+1)*a+(u**3-2*u*u+u)*h*tangents[i]+(-2*u**3+3*u*u)*b+(u**3-u*u)*h*tangents[i+1]
''' +src[end:]
src=src.replace('F=157','F=169')
src=src.replace('v=Vector(pole);v=(v-u*v.dot(u)).normalized()', "v=Vector((0,d.z,-d.y)) if a.startswith('thigh') else Vector(pole);v=(v-u*v.dot(u)).normalized()")
start=src.index(' fall=max(');end=src.index(" put('pelvis'",start)
src=src[:start]+''' air=max(0,t-5.35)
 lift=1.0*air-3.5*air*air if air>0 else 0
 drop=-lift
 hipy=channel(t,[(0,.045),(.65,.26),(2.7,.26),(3.4,.24),(4.4,.15),(5.05,.15),(5.35,.08)])-air*1.4
 hipz=channel(t,[(0,1.015),(.85,1.18),(2.65,1.18),(3.15,1.35),(4.4,1.80),(5.0,1.80),(5.18,1.755),(5.35,1.82)])+lift
 lean=channel(t,[(0,2),(.65,65),(2.6,65),(2.95,50),(3.5,28),(4.4,2),(5.0,2),(5.25,8),(5.5,5),(7,7)])
''' +src[end:]
start=src.index('  offset=');end=src.index("  shoulder=",start)
src=src[:start]+'''  offset=0 if side=='l' else 1.15
  # Lift outside the deck first, then move back over it, then plant.
  waiting=Vector((sign*.12,-.36,.91))
  ankle=path(t,[(0,start),(.65,waiting)]+([(.30+offset,waiting)] if side=='r' else [])+[(.95+offset,(sign*.145,-.34,1.115)),(1.30+offset,(sign*.13,.10,1.115)),(1.55+offset,(sign*.12,.10,1.053)),(5.35,(sign*.12,.10,1.053))])
  if air>0:ankle=Vector((sign*.12,.10-air*1.4,1.053+lift+(.045 if side=='r' else .015)*math.sin(min(1,air/.3)*math.pi/2)))
  limb('thigh_'+side,'calf_'+side,'foot_'+side,ankle,(sign*.32,-1,.02))
  put('foot_'+side,pos('foot_'+side),Quaternion((1,0,0),math.radians(channel(t,[(0,0),(.95+offset,-4),(1.30+offset,0),(5.35,0),(5.6,8),(6,12),(7,16)]))))
''' +src[end:]
src=src.replace("release=smooth((t-(.65 if side=='l' else .8))/.75)","release=smooth((t-(2.30 if side=='l' else 2.42))/.48)")
src=src.replace("for k in fc.keyframe_points:k.interpolation='LINEAR'","for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'")
src=src.replace('6.5 seconds','7 seconds').replace("'duration_seconds':6.5","'duration_seconds':7")
src=src.replace("for f in [25,49,73,97,121,133]:","for f in [19,31,49,61,73,85,109,125,133,145]:")
src=src.replace('s.frame_step=2;s.render.fps=12;','s.frame_step=1;s.render.fps=24;')
exec(compile(src,__file__,'exec'))
