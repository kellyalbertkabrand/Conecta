import subprocess,os,sys,json
R='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/reels/'
VOZ='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/voz/'
OV3=R+'ov3/'; OV2=R+'ov2/'; S1=R+'seg/'; S2=R+'seg2/'; S=R+'seg3/'; os.makedirs(S,exist_ok=True)
ENC=['-c:v','libx264','-preset','medium','-crf','18','-r','30','-pix_fmt','yuv420p']
def run(c):
  r=subprocess.run(c,capture_output=True,text=True)
  if r.returncode: print(' '.join(c)[:400]); print(r.stderr[-2500:]); sys.exit(1)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
spec=json.load(open(R+'spec3.json'))
# ---------- ABERTURA (mesmas imagens, novos letterings, sem textinho em cima) ----------
D=dur(S1+'ab_base.mp4')
P=[('p0',0.3,5.0),('p1',5.0,10.0),('p2',10.0,15.0),('p3',15.0,20.0),('p4',20.0,25.0),('p5',25.0,30.5),('p6',30.5,D)]
inp=['-i',S1+'ab_base.mp4','-loop','1','-i',OV3+'logo.png']; fc="[0:v][1:v]overlay=0:0:shortest=1[v0]"; last='v0'
for j,(k,a,b) in enumerate(P):
  inp+=['-loop','1','-i',OV3+k+'.png']; n=j+2
  fc+=f";[{n}:v]format=rgba,fade=in:st={a}:d=0.5:alpha=1,fade=out:st={b-0.4}:d=0.4:alpha=1[t{j}];[{last}][t{j}]overlay=0:0:shortest=1:enable='between(t,{a},{b})'[v{j+1}]"; last=f'v{j+1}'
fc+=f";[{last}]fade=in:st=0:d=0.4,trim=duration={D}[o]"
run(['ffmpeg','-v','error','-y',*inp,'-f','lavfi','-t',str(D),'-i','anullsrc=r=48000:cl=stereo','-filter_complex',fc,'-map','[o]','-map',f'{len(P)+2}:a',*ENC,'-c:a','aac','-b:a','192k','-t',str(D),S+'B00.mp4'])
print('abertura',D,flush=True)
# ---------- ENTREVISTAS: imagem da v2 + audio so com a voz (DPDFNet) ----------
cortes={1:(2.85,30.95),2:(0.0,17.85),3:(0.3,34.0),4:(0.6,14.1),5:(0.0,11.95)}
t_nome={1:6.85,2:5.6,3:7.8,4:4.9,5:3.0}
VOZCH=("highpass=f=80,agate=mode=downward:threshold=0.012:ratio=3:range=0.05:attack=8:release=220:knee=4,"
       "equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.5:g=2.5,"
       "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-15:TP=-1.5:LRA=8")
outs=[S+'B00.mp4']
for i in range(1,6):
  a,b=cortes[i]; d=b-a; L=spec['leg'][str(i)]; tn=t_nome[i]
  inp=['-i',S2+f'e{i}_base.mp4','-i',VOZ+f'd{i}.wav','-loop','1','-i',OV3+'logo.png','-loop','1','-i',OV3+f'n{i}.png']
  fc=(f"[0:v][2:v]overlay=0:0:shortest=1[c];[3:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1,fade=out:st={min(7.5,tn-0.6):.2f}:d=0.5:alpha=1[nm];"
      f"[c][nm]overlay=0:0:shortest=1:enable='lt(t,{min(8.0,tn-0.1):.2f})'[v0]")
  last='v0'
  for j,(s0,s1,_) in enumerate(L):
    inp+=['-loop','1','-i',OV2+f'c{i}_{j:02d}.png']; n=j+4
    t0=max(0,s0-a-0.05); t1=(L[j+1][0]-a-0.05) if j+1<len(L) else min(d,s1-a+0.5)
    fc+=f";[{last}][{n}:v]overlay=0:0:shortest=1:enable='between(t,{t0:.2f},{t1:.2f})'[v{j+1}]"; last=f'v{j+1}'
  fc+=f";[{last}]trim=duration={d}[o];[1:a]atrim=start={a}:duration={d},asetpts=PTS-STARTPTS,{VOZCH},afade=t=in:d=0.12,afade=t=out:st={d-0.3}:d=0.3,aresample=48000,aformat=channel_layouts=stereo[au]"
  out=f'{S}B{i:02d}.mp4'; outs.append(out)
  run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-map','[au]',*ENC,'-c:a','aac','-b:a','192k','-t',str(d),out])
  print('entrevista',i,round(d,2),flush=True)
# ---------- FINAL DO EVENTO + CARD ----------
base=S2+'fim_base.mp4'; D=dur(base)
fc=(f"[0:v][1:v]overlay=0:0:shortest=1[c];[2:v]format=rgba,fade=in:st={D-6.2}:d=0.6:alpha=1[t];[c][t]overlay=0:0:shortest=1:enable='gte(t,{D-6.2})'[o]")
run(['ffmpeg','-v','error','-y','-i',base,'-loop','1','-i',OV3+'logo.png','-loop','1','-i',OV3+'pf.png','-f','lavfi','-t',str(D),'-i','anullsrc=r=48000:cl=stereo',
     '-filter_complex',fc,'-map','[o]','-map','3:a',*ENC,'-c:a','aac','-b:a','192k','-t',str(D),S+'B90.mp4'])
run(['ffmpeg','-v','error','-y','-framerate','30','-loop','1','-t','4.5','-i',OV3+'end.png','-f','lavfi','-t','4.5','-i','anullsrc=r=48000:cl=stereo','-vf','fade=in:st=0:d=0.5,format=yuv420p','-map','0:v','-map','1:a',*ENC,'-c:a','aac','-b:a','192k','-shortest',S+'B99.mp4'])
outs+=[S+'B90.mp4',S+'B99.mp4']
open(S+'final.txt','w').write(''.join(f"file '{f}'\n" for f in outs))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+'final.txt','-c:v','libx264','-preset','slow','-crf','22','-maxrate','6M','-bufsize','12M','-r','30','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',R+'reels_v3.mp4'])
print('final',dur(R+'reels_v3.mp4'))
