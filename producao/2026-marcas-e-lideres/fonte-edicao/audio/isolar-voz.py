import sherpa_onnx as so, soundfile as sf, numpy as np, json, subprocess, sys, os
W='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/'; M=W+'modelo/denoise/'; O=W+'voz/'
U='/root/.claude/uploads/576081bf-d1ab-5bb8-804a-2a1c062f4721/'
E_=[U+f+'.mov' for f in ['8cb26dfe-2fc9adb6-f8ed-46f3-8a76-c1e5cbd909cb','bc2ac019-8c15b77c-1590-4b35-9490-cf3a1c953b54','a91f6ffc-aebb29a2-36ed-4a00-a8d0-5e1c5efde648','6a9a6738-1cbf8fa9-f93d-4e1d-9a0c-8cb7aea76272','e6cd750c-01d51540-c36d-4c96-89f1-eee1689b15e8']]
tr=json.load(open(W+'reels/transcricao.json'))
def den(model):
  c=so.OfflineSpeechDenoiserConfig(model=model); return so.OfflineSpeechDenoiser(c)
def load(path,sr):
  raw=subprocess.run(['ffmpeg','-v','error','-i',path,'-vn','-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout
  return np.frombuffer(raw,np.float32).copy()
dp=den(so.OfflineSpeechDenoiserModelConfig(dpdfnet=so.OfflineSpeechDenoiserDpdfNetModelConfig(model=M+'dpdfnet2_48khz_hr.onnx'),num_threads=4))
for i in range(1,6):
  x48=load(E_[i-1],48000)
  a=dp.run(x48,48000); y=np.array(a.samples,np.float32); print(i,'dpdf sr',a.sample_rate,flush=True)
  sf.write(O+f'd{i}.wav',y,a.sample_rate)
  # amostra de voz p/ VoxLock: trecho continuo de fala da propria pessoa (do audio ja limpo)
  segs=[s for s in tr[str(i)] if s['end']-s['start']>=3.0 and (i!=1 or 2.9<=s['start']<30)]
  s0=max(segs,key=lambda s:s['end']-s['start']); a0,b0=s0['start'],min(s0['end'],s0['start']+8)
  sm=subprocess.run(['ffmpeg','-v','error','-y','-i',O+f'd{i}.wav','-ss',str(a0),'-to',str(b0),'-ac','1','-ar','16000',O+f'amostra{i}.wav'])
  vx=den(so.OfflineSpeechDenoiserModelConfig(voxlock=so.OfflineSpeechDenoiserVoxLockModelConfig(enroll_model=M+'vx/sherpa-onnx-voxlock/enroll.onnx',chunk_model=M+'vx/sherpa-onnx-voxlock/chunk.onnx',voice_sample=O+f'amostra{i}.wav'),num_threads=4))
  x16=load(O+f'd{i}.wav',16000)
  b=vx.run(x16,16000); z=np.array(b.samples,np.float32); print(i,'voxlock sr',b.sample_rate,'amostra',round(a0,1),round(b0,1),flush=True)
  sf.write(O+f'v{i}.wav',z,b.sample_rate)
