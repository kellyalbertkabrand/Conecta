import subprocess, os, sys
U='/root/.claude/uploads/576081bf-d1ab-5bb8-804a-2a1c062f4721/'
W='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/video/'
OV=W+'ov/'; S=W+'seg/'; os.makedirs(S,exist_ok=True)
V1=U+'a07918b5-354416555fb842f981d0d47f4d9692b5.mov'; V2=U+'b25ac763-c037c9a0-bb70-4833-804c-aed856033ce8.mov'
V3=U+'91c3fac4-687db9f1-3805-46eb-9a44-dc4e3f310648.mov'; V4=U+'251289ad-4d2e6db1-988a-41b9-bbca-462045f52142.mov'
P=lambda n: U+n
LOOK="eq=contrast=1.06:saturation=1.08:brightness=0.01"
SHARP="unsharp=5:5:0.6"
# (tipo, fonte, inicio, dur, param, texto)
segs=[
 ('v',V1,0.0,4.0,('x',0.275),'t1'),
 ('v',V1,10.9,2.6,('x',0.48),None),
 ('v',V1,5.0,2.6,('x',0.10),None),
 ('v',V1,13.35,2.2,('x',0.30),None),
 ('v',V2,13.6,3.2,('y',0.40),None),
 ('pz',P('752c85a0-image.jpg'),0,3.6,0.60,'t2'),
 ('v',V4,17.3,3.4,('x',0.30),None),
 ('pp',P('aae13598-image.jpg'),0,3.4,(0.20,0.45),None),
 ('v',V3,37.5,3.4,('x',0.20),'t3'),
 ('pp',P('8fe42a3a-image.jpg'),0,3.4,(0.25,0.45),None),
 ('v',V4,25.0,3.2,('x',0.20),None),
 ('pz',P('60e18573-image.jpg'),0,3.4,0.35,None),
 ('v',V3,50.0,3.2,('x',0.35),None),
 ('pz',P('20390039-image.jpg'),0,3.4,0.55,None),
 ('pp',P('3e720eac-image.jpg'),0,5.0,(0.0,1.0),'t4'),
]
def run(c):
  r=subprocess.run(c,capture_output=True,text=True)
  if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
files=[]
for i,(t,src,ss,d,par,txt) in enumerate(segs):
  out=f'{S}s{i:02d}.mp4'; files.append(out)
  inp=[]; 
  if t=='v':
    inp=['-i',src]
    if par[0]=='x': base=f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,crop=ih*0.8:ih:(iw-ih*0.8)*{par[1]/0.55:.4f}:0"
    else: base=f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,crop=iw:iw*1.25:0:(ih-iw*1.25)*{par[1]/0.30:.4f}"
    base+=f",scale=1080:1350:flags=lanczos,{SHARP},{LOOK},fps=30,setsar=1"
  elif t=='pz':  # zoom in suave
    inp=['-framerate','30','-loop','1','-t',str(d),'-i',src]
    base=(f"[0:v]scale=1080:-2,crop=1080:1350:0:(ih-1350)*{par},scale=2160:2700,"
          f"zoompan=z='1+0.07*on/({d}*30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1350:fps=30,{LOOK},setsar=1")
  else:  # pan horizontal
    inp=['-framerate','30','-loop','1','-t',str(d),'-i',src]
    a,b=par
    base=(f"[0:v]scale=-2:2700,crop=2160:2700:(iw-2160)*({a}+({b}-{a})*t/{d}):0,scale=1080:1350:flags=lanczos,fps=30,{LOOK},setsar=1")
  fc=base+"[b]"; n=1; inp+=['-loop','1','-t',str(d),'-i',OV+'logo.png']
  fc+=f";[{n}:v]format=rgba[lg];[b][lg]overlay=0:0:shortest=1[c]"; last='c'
  if txt:
    n+=1; inp+=['-loop','1','-t',str(d),'-i',OV+txt+'.png']
    fc+=f";[{n}:v]format=rgba,fade=in:st=0.25:d=0.6:alpha=1[tx];[c][tx]overlay=0:0:shortest=1[c2]"; last='c2'
  fc+=f";[{last}]trim=duration={d},format=yuv420p[o]"
  run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-an','-c:v','libx264','-preset','medium','-crf','17','-r','30',out])
  print('ok',i,d)
# end card
d=5.5; run(['ffmpeg','-v','error','-y','-loop','1','-t',str(d),'-i',OV+'end.png','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','17','-r','30',S+'end.mp4'])
open(S+'list.txt','w').write(''.join(f"file '{f}'\n" for f in files))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+'list.txt','-c','copy',S+'main.mp4'])
