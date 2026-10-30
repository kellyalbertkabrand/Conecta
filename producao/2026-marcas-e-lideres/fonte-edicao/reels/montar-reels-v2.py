import subprocess,os,sys,json
U='/root/.claude/uploads/576081bf-d1ab-5bb8-804a-2a1c062f4721/'
R='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/reels/'
OV=R+'ov/'; OV2=R+'ov2/'; S=R+'seg2/'; os.makedirs(S,exist_ok=True)
V1L=U+'e0429e01-354416555fb842f981d0d47f4d9692b5.mov'   # video ACIGRA longo (premiados no palco)
V2=U+'b25ac763-c037c9a0-bb70-4833-804c-aed856033ce8.mov'
V3=U+'91c3fac4-687db9f1-3805-46eb-9a44-dc4e3f310648.mov'
V4=U+'251289ad-4d2e6db1-988a-41b9-bbca-462045f52142.mov'
VP=U+'5820196b-ad63d4a8-d0d8-4e3b-8c5b-03d389dd5569.mov'  # categoria Pampas Garden
E_=[U+f+'.mov' for f in ['8cb26dfe-2fc9adb6-f8ed-46f3-8a76-c1e5cbd909cb','bc2ac019-8c15b77c-1590-4b35-9490-cf3a1c953b54','a91f6ffc-aebb29a2-36ed-4a00-a8d0-5e1c5efde648','6a9a6738-1cbf8fa9-f93d-4e1d-9a0c-8cb7aea76272','e6cd750c-01d51540-c36d-4c96-89f1-eee1689b15e8']]
LOOK="eq=contrast=1.06:saturation=1.08:brightness=0.01"; SH="unsharp=5:5:0.6"
ENC=['-c:v','libx264','-preset','medium','-crf','18','-r','30','-pix_fmt','yuv420p']
EXTRA={4:',eq=gamma=1.45:brightness=0.03:saturation=1.05',3:',eq=gamma=1.15'}
SOMENTE=os.environ.get('SOMENTE')
def run(c):
  if SOMENTE and os.path.exists(c[-1]) and not any(os.path.basename(c[-1]).startswith(x) for x in SOMENTE.split(',')): return
  r=subprocess.run(c,capture_output=True,text=True)
  if r.returncode: print(' '.join(c)[:400]); print(r.stderr[-2500:]); sys.exit(1)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def shot(out,s,d):
  """renderiza um plano 1080x1920 com duracao d"""
  t=s[0]
  if t=='self':
    _,src,ss,i=s; inp=['-i',src]
    fc=f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,{SH},{LOOK}{EXTRA.get(i,'')},fps=30,setsar=1[o]"
  elif t=='f':   # video horizontal emoldurado sobre fundo desfocado
    _,src,ss,x=s; k=x/0.55; inp=['-i',src]
    fc=(f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,split[a][b];"
        f"[a]crop=ih*0.5625:ih:(iw-ih*0.5625)*0.5:0,scale=1080:1920,boxblur=30:3,eq=brightness=-0.12:saturation=0.9[bg];"
        f"[b]crop=ih*0.8:ih:(iw-ih*0.8)*{k:.4f}:0,scale=1080:1350:flags=lanczos,{SH},{LOOK}[fg];[bg][fg]overlay=0:285,fps=30,setsar=1[o]")
  elif t=='v9':
    _,src,ss=s; inp=['-i',src]
    fc=f"[0:v]trim=start={ss}:duration={d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,{SH},{LOOK},fps=30,setsar=1[o]"
  elif t=='pz':
    _,img,x=s; inp=['-framerate','30','-loop','1','-t',str(d),'-i',U+img]
    fc=(f"[0:v]scale=-2:1920,crop=1080:1920:(iw-1080)*{x}:0,scale=2160:3840,"
        f"zoompan=z='1+0.07*on/({d}*30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,{LOOK},setsar=1[o]")
  else:
    _,img,a,b=s; inp=['-framerate','30','-loop','1','-t',str(d),'-i',U+img]
    fc=f"[0:v]scale=-2:3840,crop=2160:3840:(iw-2160)*({a}+({b}-{a})*t/{d}):0,scale=1080:1920:flags=lanczos,fps=30,{LOOK},setsar=1[o]"
  run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc+f";[o]trim=duration={d}[o2]",'-map','[o2]','-an',*ENC,out])
def montar(nome,planos):
  fs=[]
  for j,(d,s) in enumerate(planos):
    f=f'{S}{nome}_{j:02d}.mp4'; shot(f,s,d); fs.append(f)
  open(S+nome+'.txt','w').write(''.join(f"file '{f}'\n" for f in fs))
  run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+nome+'.txt','-c','copy',S+nome+'_base.mp4'])
  return S+nome+'_base.mp4'
spec=json.load(open(R+'spec2.json'))
cortes={1:(2.85,30.95),2:(0.0,17.85),3:(0.3,34.0),4:(0.6,14.1),5:(0.0,11.95)}
# planos por entrevista: (inicio relativo, fim relativo, plano). 'self' = a pessoa falando
def S_(i,t): return ('self',E_[i-1],cortes[i][0]+t,i)
roteiro={
 1:[(0,6.85,'self'),(6.85,11.55,('pp','2ffd8058-image.jpg',0.15,0.85)),(11.55,13.75,('f',V1L,39.7,0.40)),(13.75,28.1,'self')],
 2:[(0,5.6,'self'),(5.6,9.0,('pp','8fe42a3a-image.jpg',0.30,0.55)),(9.0,12.8,'self'),(12.8,15.6,('pp','3e720eac-image.jpg',0.30,0.60)),(15.6,17.85,'self')],
 3:[(0,7.8,'self'),(7.8,12.8,('f',VP,12.8,0.05)),(12.8,18.5,'self'),(18.5,22.5,('pp','c2cba76d-image.jpg',0.25,0.45)),(22.5,27.4,'self'),(27.4,31.0,('pz','00731385-image.jpg',0.5)),(31.0,33.7,'self')],
 4:[(0,4.9,'self'),(4.9,8.1,('f',V3,22.0,0.0)),(8.1,11.4,('pz','ee9475eb-image.jpg',0.5)),(11.4,13.5,'self')],
 5:[(0,3.0,'self'),(3.0,6.2,('f',V4,8.8,0.12)),(6.2,9.0,('pz','60e18573-image.jpg',0.15)),(9.0,11.95,'self')],
}
AUD="highpass=f=90,lowpass=f=11000,afftdn=nr=14:nf=-32:tn=1,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.5:g=3,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-15:TP=-1.5:LRA=8"
outs=[R+'seg/B00.mp4']   # abertura ja aprovada (sem audio)
for i in range(1,6):
  a,b=cortes[i]; d=b-a; L=spec['leg'][str(i)]
  planos=[(t1-t0,(S_(i,t0) if p=='self' else p)) for t0,t1,p in roteiro[i]]
  base=montar(f'e{i}',planos)
  t_nome=roteiro[i][0][1]  # crachá so no primeiro plano da pessoa
  inp=['-i',base,'-i',E_[i-1],'-loop','1','-i',OV+'logo.png','-loop','1','-i',OV+f'n{i}.png']
  fc=(f"[0:v][2:v]overlay=0:0:shortest=1[c];[3:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1,fade=out:st={min(7.5,t_nome-0.6):.2f}:d=0.5:alpha=1[nm];"
      f"[c][nm]overlay=0:0:shortest=1:enable='lt(t,{min(8.0,t_nome-0.1):.2f})'[v0]")
  last='v0'
  for j,(s0,s1,_) in enumerate(L):
    inp+=['-loop','1','-i',OV2+f'c{i}_{j:02d}.png']; n=j+4
    t0=max(0,s0-a-0.05); t1=(L[j+1][0]-a-0.05) if j+1<len(L) else min(d,s1-a+0.5)
    fc+=f";[{last}][{n}:v]overlay=0:0:shortest=1:enable='between(t,{t0:.2f},{t1:.2f})'[v{j+1}]"; last=f'v{j+1}'
  fc+=f";[{last}]trim=duration={d}[o];[1:a]atrim=start={a}:duration={d},asetpts=PTS-STARTPTS,{AUD},afade=t=in:d=0.15,afade=t=out:st={d-0.3}:d=0.3,aresample=48000,aformat=channel_layouts=stereo[au]"
  out=f'{S}B{i:02d}.mp4'; outs.append(out)
  run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-map','[au]',*ENC,'-c:a','aac','-b:a','192k',out])
  print('entrevista',i,round(d,2),flush=True)
# ---------- MONTAGEM FINAL DO EVENTO (apos a Adriana) ----------
fim=[(3.0,('v9',V2,13.6)),(2.8,('f',V1L,0.5,0.35)),(3.2,('pp','2ffd8058-image.jpg',0.85,0.25)),(2.2,('f',V1L,39.7,0.40)),(3.6,('pz','ee9475eb-image.jpg',0.5))]
base=montar('fim',fim); D=dur(base)
fc=(f"[0:v][1:v]overlay=0:0:shortest=1[c];[2:v]format=rgba,fade=in:st={D-6.2}:d=0.6:alpha=1[t];[c][t]overlay=0:0:shortest=1:enable='gte(t,{D-6.2})'[o]")
run(['ffmpeg','-v','error','-y','-i',base,'-loop','1','-i',OV+'logo.png','-loop','1','-i',OV2+'pf.png','-f','lavfi','-t',str(D),'-i','anullsrc=r=48000:cl=stereo',
     '-filter_complex',fc,'-map','[o]','-map','3:a',*ENC,'-c:a','aac','-b:a','192k','-t',str(D),S+'B90.mp4'])
outs+= [S+'B90.mp4', R+'seg/B99.mp4']
open(S+'final.txt','w').write(''.join(f"file '{f}'\n" for f in outs))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+'final.txt','-c:v','libx264','-preset','slow','-crf','22','-maxrate','6M','-bufsize','12M','-r','30','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',R+'reels_v2.mp4'])
print('final',dur(R+'reels_v2.mp4'))
