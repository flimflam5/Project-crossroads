#!/usr/bin/env python3
"""Convert the owner's MP3 to a bounded, signed 8-bit GBA direct-sound sample."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[2]
src=R/'crossroads/audio/Black_Ledger_Title_Demo_v5.mp3'
dest=R/'sound/direct_sound_samples/crossroads/black_ledger_title.pcm'
with tempfile.TemporaryDirectory() as temp:
 decoded=Path(temp)/'track.pcm'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ac','1','-ar','31536','-f','s8','-acodec','pcm_s8',str(decoded)],check=True)
 pcm=bytearray(decoded.read_bytes());fade=631
 # 20 ms edges avoid a discontinuity on the provisional full-track repeat.
 for i in range(fade):
  for j in (i,len(pcm)-1-i):
   value=pcm[j] if pcm[j]<128 else pcm[j]-256
   pcm[j]=round(value*i/fade)&255
 assert 2_000_000<len(pcm)<3_000_000
 dest.write_bytes(pcm)
 meta={'source':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sample_sha256':hashlib.sha256(pcm).hexdigest(),'sample_rate':31536,'channels':1,'encoding':'signed 8-bit PCM','samples':len(pcm),'duration_seconds':len(pcm)/31536,'loop_start_sample':0,'edge_fade_samples':fade,'loop_status':'Owner accepted the full-track repeat in 0.8.1; retained unchanged.'}
 (R/'crossroads/audio/title-music.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('Title sample:',len(pcm),'bytes;',len(pcm)/31536,'seconds')
