#!/usr/bin/env python3
"""Reproduce stripped geometry facts from public pret reference files.

Input archive is reference terrain data, never a commercial ROM. The archive and
source event scripts are not copied into game data or committed. Supply the
GitHub file-download JSON and header/matrix/event selection explicitly.
"""
import argparse,base64,hashlib,json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--downloads',type=Path,required=True);p.add_argument('--selection',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
b=a.archive.read_bytes();sha=blob(b);assert sha=='33105ab54c804a33503fb52db0ffa93a4d38191a'
assert b[:4]==b'NARC';count=struct.unpack_from('<H',b,24)[0];off=16;gmif=None
while off<len(b):
 magic,length=struct.unpack_from('<4sI',b,off)
 if magic==b'GMIF':gmif=off+8;break
 off+=length
assert gmif is not None
entries={Path(x['path']).name:x for x in json.loads(a.downloads.read_text())}
def data(e):
 v=base64.b64decode(e['content']) if e['encoding']=='base64' else e['content'].encode();assert blob(v)==e['sha'];return v
out={}
for s in json.loads(a.selection.read_text()):
 matrix=entries[s['matrix']+'.bin'];event=entries[s['event']+'.json'];m=data(matrix);w,h=m[:2];n=w*h;offset=5+m[4]+n*2*m[2]+n*m[3];models=struct.unpack_from('<'+str(n)+'H',m,offset);chunks=[]
 for model in models:
  assert model<count;start,end=struct.unpack_from('<II',b,28+model*8);v=b[gmif+start:gmif+end];permissions,propbytes,_,_=struct.unpack_from('<4I',v);magic,extra=struct.unpack_from('<2H',v,16);assert magic==0x1234 and permissions==2048
  offset=20+extra;perms=list(struct.unpack_from('<1024H',v,offset));offset+=permissions;props=[]
  assert propbytes%48==0
  for pos in range(offset,offset+propbytes,48):
   values=struct.unpack_from('<12i',v,pos);props.append(dict(model=values[0],tile_x=values[1]/65536+16,tile_z=values[3]/65536+16,rotation=list(values[4:7])))
  chunks.append(dict(model=model,permissions=perms,props=props))
 e=json.loads(data(event));out[s['header']]=dict(matrix_dimensions=[w,h],chunks=chunks,warps=[{k:x[k] for k in ['x','z','header','anchor','y']} for x in e['warps']],objects=[{k:x[k] for k in ['x','z','y','spriteId']} for x in e.get('objects',[])],source=dict(matrix=matrix['display_url'],matrix_blob_sha=matrix['sha'],events=event['display_url'],events_blob_sha=event['sha'],terrain_blob_sha=sha))
dest=R/'crossroads/hgss/canonical_events/ecruteak-interior-geometry.json'
if a.check:assert out==json.loads(dest.read_text()),'Reference extraction differs'
else:dest.write_text(json.dumps(out,indent=2)+'\n')
print('Reproducible source SHA, matrix, extended-header terrain permissions and stripped prop/warp facts: PASS',len(out),'headers')
