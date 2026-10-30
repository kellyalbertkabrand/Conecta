import subprocess,os,sys,json
U='/root/.claude/uploads/576081bf-d1ab-5bb8-804a-2a1c062f4721/'
R='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/reels/'
OV=R+'ov/'; S=R+'seg/'; os.makedirs(S,exist_ok=True)
V1=U+'a07918b5-354416555fb842f981d0d47f4d9692b5.mov'; V2=U+'b25ac763-c037c9a0-bb70-4833-804c-aed856033ce8.mov'
V3=U+'91c3fac4-687db9f1-3805-46eb-9a44-dc4e3f310648.mov'; V4=U+'251289ad-4d2e6db1-988a-41b9-bbca-462045f52142.mov'
E_=[U+f+'.mov' for f in ['8cb26dfe-2fc9adb6-f8ed-46f3-8a76-c1e5cbd909cb','bc2ac019-8c15b77c-1590-4b35-9490-cf3a1c953b54','a91f6ffc-aebb29a2-36ed-4a00-a8d0-5e1c5efde648','6a9a6738-1cbf8fa9-f93d-4e1d-9a0c-8cb7aea76272','e6cd750c-01d51540-c36d-4c96-89f1-eee1689b15e8']]
LOOK="eq=contrast=1.06:saturation=1.08:brightness=0.01"; SH="unsharp=5:5:0.6"
ENC=['-c:v','libx264','-preset','medium','-crf','18','-r','30','-pix_fmt','yuv420p']
SOMENTE=os.environ.get('SOMENTE')
def run(c):
  out=c[-1]
  if SOMENTE and os.path.exists(out) and not any(os.path.basename(out).startswith(x) for x in SOMENTE.split(',')): return
  r=subprocess.run(c,capture_output=True,text=True)
  if r.returncode: print(' '.join(c)[:500]); print(r.stderr[-2500:]); sys.exit(1)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
# ---------- ABERTURA ----------
ab=[('f',V1,0.0,3.5,0.275),('f',V1,10.9,2.1,0.48),('pz','752c85a0-image.jpg',3.5,0.5),('f',V1,13.35,1.9,0.30),
    ('v9',V2,13.6,4.0),('f',V4,17.3,3.0,0.30),('pp','8fe42a3a-image.jpg',3.5,(0.30,0.55)),('f',V3,37.5,3.0,0.20),
    ('pz','60e18573-image.jpg',3.5,0.15),('pz','20390039-image.jpg',3.0,0.5),('pp','3e720eac-image.jpg',4.6,(0.10,0.90))]
files=[]
for i,s in enumerate(ab):
  out=f'{S}a{i:02d}.mp4'; files.append(out); t=s[0]
  if t=='f':
    _,src,ss,d,x=s; k=x/0.55
    fc=(f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,split[a][b];"
        f"[a]crop=ih*0.5625:ih:(iw-ih*0.5625)*0.5:0,scale=1080:1920,boxblur=30:3,eq=brightness=-0.12:saturation=0.9[bg];"
        f"[b]crop=ih*0.8:ih:(iw-ih*0.8)*{k:.4f}:0,scale=1080:1350:flags=lanczos,{SH},{LOOK}[fg];"
        f"[bg][fg]overlay=0:285,fps=30,setsar=1[o]")
    inp=['-i',src]
  elif t=='v9':
    _,src,ss,d=s; inp=['-i',src]
    fc=f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,{SH},{LOOK},fps=30,setsar=1[o]"
  elif t=='pz':
    _,img,d,x=s; inp=['-framerate','30','-loop','1','-t',str(d),'-i',U+img]
    fc=(f"[0:v]scale=-2:1920,crop=1080:1920:(iw-1080)*{x}:0,scale=2160:3840,"
        f"zoompan=z='1+0.07*on/({d}*30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,{LOOK},setsar=1[o]")
  else:
    _,img,d,(a,b)=s; inp=['-framerate','30','-loop','1','-t',str(d),'-i',U+img]
    fc=f"[0:v]scale=-2:3840,crop=2160:3840:(iw-2160)*({a}+({b}-{a})*t/{d}):0,scale=1080:1920:flags=lanczos,fps=30,{LOOK},setsar=1[o]"
  run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-an',*ENC,out])
open(S+'ab.txt','w').write(''.join(f"file '{f}'\n" for f in files))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+'ab.txt','-c','copy',S+'ab_base.mp4'])
D=dur(S+'ab_base.mp4'); print('abertura',D)
# frases ao longo da abertura (inicio, fim)
P=[('p1',0.3,6.0),('p2',6.0,12.0),('p3',12.0,18.0),('p4',18.0,24.5),('p5',24.5,30.5),('p6',30.5,D)]
inp=['-i',S+'ab_base.mp4','-loop','1','-i',OV+'logo.png']; fc="[0:v][1:v]overlay=0:0:shortest=1[v0]"; last='v0'
for j,(k,a,b) in enumerate(P):
  inp+=['-loop','1','-i',OV+k+'.png']; n=j+2
  fc+=f";[{n}:v]format=rgba,fade=in:st={a}:d=0.5:alpha=1,fade=out:st={b-0.4}:d=0.4:alpha=1[t{j}];[{last}][t{j}]overlay=0:0:shortest=1:enable='between(t,{a},{b})'[v{j+1}]"; last=f'v{j+1}'
fc+=f";[{last}]fade=in:st=0:d=0.4,trim=duration={D}[o]"
run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]',*ENC,'-an',S+'abertura_v.mp4'])
# trilha silenciosa
run(['ffmpeg','-v','error','-y','-i',S+'abertura_v.mp4','-f','lavfi','-t',str(D),'-i','anullsrc=r=48000:cl=stereo','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',S+'B00.mp4'])
# ---------- ENTREVISTAS ----------
spec=json.load(open(R+'spec.json'))
cortes={1:(2.85,30.95),2:(0.0,17.85),3:(0.3,34.0),4:(0.6,14.1),5:(0.0,11.95)}
AUD="highpass=f=90,lowpass=f=11000,afftdn=nr=14:nf=-32:tn=1,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.5:g=3,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-15:TP=-1.5:LRA=8"
outs=[S+'B00.mp4']
EXTRA={4:',eq=gamma=1.45:brightness=0.03:saturation=1.05',3:',eq=gamma=1.15'}
for i in range(1,6):
  a,b=cortes[i]; d=b-a; src=E_[i-1]; L=spec['leg'][str(i)]
  inp=['-i',src,'-loop','1','-i',OV+'logo.png','-loop','1','-i',OV+f'n{i}.png']
  fc=(f"[0:v]trim=start={a}:duration={d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,{SH},{LOOK}{EXTRA.get(i,'')},fps=30,setsar=1[b];"
      f"[b][1:v]overlay=0:0:shortest=1[c];[2:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1,fade=out:st=7.5:d=0.6:alpha=1[nm];[c][nm]overlay=0:0:shortest=1:enable='lt(t,8.2)'[v0]")
  last='v0'
  for j,(s0,s1,_) in enumerate(L):
    inp+=['-loop','1','-i',OV+f'c{i}_{j:02d}.png']; n=j+3
    t0=max(0,s0-a-0.05); t1=(L[j+1][0]-a-0.05) if j+1<len(L) else min(d,s1-a+0.5)
    fc+=f";[{last}][{n}:v]overlay=0:0:shortest=1:enable='between(t,{t0:.2f},{t1:.2f})'[v{j+1}]"; last=f'v{j+1}'
  fc+=f";[{last}]trim=duration={d}[o];[0:a]atrim=start={a}:duration={d},asetpts=PTS-STARTPTS,{AUD},afade=t=in:d=0.15,afade=t=out:st={d-0.3}:d=0.3,aresample=48000,aformat=channel_layouts=stereo[au]"
  out=f'{S}B{i:02d}.mp4'; outs.append(out)
  run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-map','[au]',*ENC,'-c:a','aac','-b:a','192k',out])
  print('entrevista',i,d)
# ---------- CARD FINAL ----------
run(['ffmpeg','-v','error','-y','-framerate','30','-loop','1','-t','4.5','-i',OV+'end.png','-f','lavfi','-t','4.5','-i','anullsrc=r=48000:cl=stereo','-vf','fade=in:st=0:d=0.5,format=yuv420p','-map','0:v','-map','1:a',*ENC,'-c:a','aac','-b:a','192k','-shortest',S+'B99.mp4'])
outs.append(S+'B99.mp4')
open(S+'final.txt','w').write(''.join(f"file '{f}'\n" for f in outs))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+'final.txt','-c:v','libx264','-preset','slow','-crf','19','-r','30','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',R+'reels.mp4'])
print('final',dur(R+'reels.mp4'))
