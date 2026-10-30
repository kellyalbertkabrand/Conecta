import sherpa_onnx as so, soundfile as sf, numpy as np, subprocess, json, wave
from faster_whisper import WhisperModel
W='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/'; M=W+'modelo/denoise/'
F='/root/.claude/uploads/576081bf-d1ab-5bb8-804a-2a1c062f4721/a6711488-9f07d933-29ef-4700-985b-562011405283.mov'
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',F,'-vn','-ac','1','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
dp=so.OfflineSpeechDenoiser(so.OfflineSpeechDenoiserConfig(model=so.OfflineSpeechDenoiserModelConfig(dpdfnet=so.OfflineSpeechDenoiserDpdfNetModelConfig(model=M+'dpdfnet2_48khz_hr.onnx'),num_threads=4)))
r=dp.run(x,48000); sf.write(W+'voz/d6.wav',np.array(r.samples,np.float32),r.sample_rate)
m=WhisperModel(W+'modelo/small',device='cpu',compute_type='int8')
for nome,f in [('original',W+'reels/a6.wav'),('limpo',W+'voz/d6.wav')]:
  y=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
  segs,_=m.transcribe(y,language='pt',word_timestamps=True,beam_size=5)
  L=[{'start':s.start,'end':s.end,'text':s.text.strip(),'words':[(w.start,w.end,w.word) for w in s.words]} for s in segs]
  print(nome,' '.join(f"{w[2].strip()}@{w[0]:.2f}" for s in L for w in s['words']))
  if nome=='original':
    t=json.load(open(W+'reels/transcricao.json')); t['6']=L; json.dump(t,open(W+'reels/transcricao.json','w'),ensure_ascii=False,indent=1)
