"""Third exit pass: asymmetric support, overlapping torso mechanics."""
from pathlib import Path
builder=Path(__file__).with_name('smooth_skeleton_exit.py').read_text()
scope={'__file__':__file__};exec(builder.rsplit("exec(compile(src,__file__,'exec'))",1)[0],scope);src=scope['src']
src=src.replace("OUT=ROOT/'StandAndStepOff02'","OUT=ROOT/'StandAndStepOff03'")
src=src.replace("hipz=channel(t,[(0,1.015),(.85,1.18),(2.65,1.18),(3.15,1.35),(4.4,1.80),(5.0,1.80),(5.18,1.755),(5.35,1.82)])+lift", "hipz=channel(t,[(0,1.015),(.45,1.06),(.85,1.16),(1.3,1.18),(1.7,1.20),(2.2,1.235),(2.7,1.28),(3.15,1.40),(3.7,1.66),(4.4,1.80),(5.0,1.80),(5.18,1.755),(5.35,1.82)])+lift")
src=src.replace("lean=channel(t,[(0,2),(.65,65),(2.6,65),(2.95,50),(3.5,28),(4.4,2),(5.0,2),(5.25,8),(5.5,5),(7,7)])", "lean=channel(t,[(0,2),(.45,40),(.85,61),(1.3,57),(1.65,59),(2.05,56),(2.5,51),(2.95,40),(3.5,23),(4.4,2),(5.0,2),(5.25,8),(5.5,5),(7,7)])")
start=src.index(" put('pelvis'");end=src.index(" for sign,side",start)
src=src[:start]+''' # Weight first goes to the right supporting hand, then to the left planted foot.
 activity=smooth(t/.35)*(1-smooth((t-3.7)/.7))
 shift=channel(t,[(0,0),(.55,-.040),(1.05,-.055),(1.4,-.02),(1.8,.052),(2.25,.068),(2.7,.035),(3.3,.012),(4.4,0)])
 bank=channel(t,[(0,0),(.6,-8),(1.05,-10),(1.45,-2),(1.85,6),(2.25,8),(2.65,4),(3.4,-1),(4.4,0)])
 twist=channel(t,[(0,0),(.65,-5),(1.1,-8),(1.7,3),(2.15,7),(2.7,1),(3.3,-2),(4.4,0)])
 falling=smooth(air/.35)
 bank+=falling*4*math.sin(air*3)
 twist+=falling*5*math.sin(air*2.5)
 lean+=falling*7
 settle=activity*.65*math.sin(t*math.tau/1.3)
 put('pelvis',Vector((shift,hipy,hipz)),Quaternion((1,0,0),math.radians(lean*.25))@Quaternion((0,1,0),math.radians(bank*.3))@Quaternion((0,0,1),math.radians(twist*.25)))
 for n,offset,factor in [('spine_01',-6,.45),('spine_02',0,.75),('spine_03',5,1),('neck_01',1,.7)]:
  q=Quaternion((1,0,0),math.radians(lean+offset+settle*factor))@Quaternion((0,1,0),math.radians(bank*factor))@Quaternion((0,0,1),math.radians(twist*factor))
  put(n,pos(n),q)
 # Head counterbalances the chest, then settles back to the ocean-facing stare.
 put('head',pos('head'),Quaternion((1,0,0),math.radians(-2+activity*4+settle))@Quaternion((0,1,0),math.radians(bank*.25))@Quaternion((0,0,1),math.radians(twist*.20)))
 for side in ['l','r']:
  sign=1 if side=='l' else -1
  q=Quaternion((1,0,0),math.radians(lean+3+settle*sign))@Quaternion((0,1,0),math.radians(bank*.85))@Quaternion((0,0,1),math.radians(twist*.85))
  put('clavicle_'+side,pos('clavicle_'+side),q)
''' +src[end:]
src=src.replace("release=smooth((t-(2.30 if side=='l' else 2.42))/.48)","release=smooth((t-(1.15 if side=='l' else 1.50))/.48)")
src=src.replace("relaxed=shoulder+Vector((sign*.025,-.015,-.505))", "relaxed=shoulder+Vector((sign*(.025+.018*activity+.095*falling),-.015+.022*activity*math.sin(t*2.1+sign)+.05*falling,-.505+.012*activity*math.sin(t*2.7)+.075*falling))")
src=src.replace("(.045 if side=='r' else .015)*math.sin(min(1,air/.3)*math.pi/2)","(.11 if side=='r' else .035)*math.sin(min(1,air/.4)*math.pi/2)+.025*falling*math.sin(air*5+sign)")
src=src.replace('STAND / PAUSE / STEP OFF:', 'ASYMMETRIC WEIGHT TRANSFER / PAUSE / HOP:')
# Pause and hop channels from pass 02 are unchanged after 4.4 seconds.
exec(compile(src,__file__,'exec'))
