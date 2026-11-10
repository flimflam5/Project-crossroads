#!/usr/bin/env python3
"""Extract factual Johto outdoor geometry from public pret reference data.

No ROM or source story scripts are imported. Source downloads/archive remain out
of the repository; only permissions, props, coordinates and verified provenance
are written. This is reference evidence, not a claim of implemented map content.
"""
import argparse,json,base64,struct,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--downloads',type=Path,required=True);p.add_argument('--selection',type=Path,required=True);p.add_argument('--map-constants',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
archive=a.archive.read_bytes();terrain_sha=blob(archive);assert terrain_sha=='33105ab54c804a33503fb52db0ffa93a4d38191a';assert archive[:4]==b'NARC';count=struct.unpack_from('<H',archive,24)[0];off=16;gmif=None
while off<len(archive):
 tag,length=struct.unpack_from('<4sI',archive,off)
 if tag==b'GMIF':gmif=off+8;break
 off+=length
assert gmif is not None
sources={x['path']:x for x in json.loads(a.downloads.read_text())};selection=json.loads(a.selection.read_text());ids={name:int(id) for name,id in re.findall(r'^#define (MAP_\w+)\s+(\d+)\b',a.map_constants.read_text(),re.M)}
def data(entry):
 b=base64.b64decode(entry['content']) if entry['encoding']=='base64' else entry['content'].encode();assert blob(b)==entry['sha'];return b
matrix_source=sources[selection[0]['matrix_path']];m=data(matrix_source);w,h,has_headers,has_heights,text=m[:5];assert has_headers and has_heights;off=5+text;headers=struct.unpack_from('<'+str(w*h)+'H',m,off);off+=w*h*2;heights=m[off:off+w*h];off+=w*h;models=struct.unpack_from('<'+str(w*h)+'H',m,off);assert off+w*h*2==len(m);cache={}
def chunk(id):
 if id in cache:return cache[id]
 assert 0<=id<count;start,end=struct.unpack_from('<2I',archive,28+id*8);v=archive[gmif+start:gmif+end];psize,prop_size,_,_=struct.unpack_from('<4I',v);magic,extra=struct.unpack_from('<2H',v,16);assert magic==0x1234 and psize==2048 and prop_size%48==0;offset=20+extra;permissions=list(struct.unpack_from('<1024H',v,offset));offset+=psize;props=[]
 for j in range(offset,offset+prop_size,48):
  z=struct.unpack_from('<12i',v,j);props.append(dict(model=z[0],tile_x=z[1]/65536+16,tile_z=z[3]/65536+16,rotation=list(z[4:7])))
 cache[id]=dict(permissions=permissions,props=props);return cache[id]
areas={}
for sel in selection:
 header=sel['header'];cells=[(i%w,i//w,models[i],heights[i]) for i,H in enumerate(headers) if H==ids[header]];assert cells,(header,'No world cells');x0=min(x for x,y,id,z in cells);y0=min(y for x,y,id,z in cells);cw=max(x for x,y,id,z in cells)-x0+1;ch=max(y for x,y,id,z in cells)-y0+1;event=sources[sel['event_path']];e=json.loads(data(event));parts=[]
 for x,y,id,height in cells:parts.append(dict(x=x-x0,y=y-y0,model=id,matrix_height=height,**chunk(id)))
 warps=[dict(x=z['x']-x0*32,y=z['z']-y0*32,destination=z['header'],anchor=z['anchor']) for z in e.get('warps',[])];objects=[dict(x=z['x']-x0*32,y=z['z']-y0*32,sprite=z['spriteId']) for z in e.get('objects',[])];bgs=[dict(x=z['x']-x0*32,y=z['z']-y0*32,type=z['type']) for z in e.get('bgs',[])]
 areas[header]=dict(header_id=ids[header],origin=[x0*32,y0*32],dimensions=[cw*32,ch*32],cells=parts,warps=warps,objects=objects,backgrounds=bgs,source=dict(matrix=matrix_source['display_url'],matrix_blob_sha=matrix_source['sha'],events=event['display_url'],events_blob_sha=event['sha'],terrain_blob_sha=terrain_sha),status='reference facts only; reconstruction and visual/runtime acceptance tracked separately')
out=dict(authority='HGSS public world matrix/event/terrain reference facts',source_tree_sha='6bf138d6035aa6b43d6f8f4132a12df70f86dcec',areas=areas)
dest=R/'crossroads/hgss/canonical_events/johto-outdoor-geometry.json'
if a.check:assert json.loads(dest.read_text())==out
else:dest.write_text(json.dumps(out,indent=2)+'\n')
print('Verified canonical outdoor ground/props/endpoints:',len(areas),'areas; no game completion asserted.')
