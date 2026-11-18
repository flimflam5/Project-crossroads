#!/usr/bin/env python3
"""Extract terrain and exit facts from pinned public pret HGSS source data.

The 19 MiB public terrain archive is supplied separately and is not committed.
This writes numeric permissions and exit coordinates, not DS graphics.
"""
import argparse, hashlib, json, re, struct, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REV='6bf138d6035aa6b43d6f8f4132a12df70f86dcec'
ARCHIVE_SHA='33105ab54c804a33503fb52db0ffa93a4d38191a'
FILES={
 'matrix_sw':'files/fielddata/mapmatrix/map_matrix/map_matrix_0039_D24R0207.bin',
 'matrix_nw':'files/fielddata/mapmatrix/map_matrix/map_matrix_0041_D24R0209.bin',
 'matrix_second':'files/fielddata/mapmatrix/map_matrix/map_matrix_0182_D24R0212.bin',
 'event_sw_hidden':'files/fielddata/eventdata/zone_event/288_D24R0207.json',
 'event_nw_hidden':'files/fielddata/eventdata/zone_event/290_D24R0209.json',
 'event_nw_second':'files/fielddata/eventdata/zone_event/297_D24R0214.json',
 'event_sw_second':'files/fielddata/eventdata/zone_event/298_D24R0215.json',
 'script_sw_hidden':'files/fielddata/script/scr_seq/scr_seq_0044_D24R0207.s',
 'script_nw_hidden':'files/fielddata/script/scr_seq/scr_seq_0046_D24R0209.s',
 'script_nw_second':'files/fielddata/script/scr_seq/scr_seq_0051_D24R0214.s',
 'script_sw_second':'files/fielddata/script/scr_seq/scr_seq_0052_D24R0215.s'}
SHAS=dict(zip(FILES,[
 'bb2bc527d2e24f224991ac6d259545be6be24047','faead62cd9300bd8c3ec56e0fe355cee16b97cb0',
 'c860a62e92b459ed78baf582b8716a0235bb53ca','77f81e2df4be25e6d1fd6879f32bca1dc20c6524',
 'c9ce52c4c84202c1b24a964ba5e0585c55fc2f7f','e7eae101845f0002326b7b8c73f7062a80fec17f',
 '73f291110d4cc3e893be87369c5d2ea8fd445d4c','834364e4ea310e90f68f1189f139ffb1dbbf2ff5',
 'ce21f30b470c264cdeed9e422b28c1fef71e535e','0dcfbf4bc8f50b5be6c8753d80569204644f3594',
 '5abc9b9653664cd483a76646f44ec24e3c874748']))
FILES.update({
 'matrix_hall':'files/fielddata/mapmatrix/map_matrix/map_matrix_0037_D24R0205.bin',
 'event_hall':'files/fielddata/eventdata/zone_event/286_D24R0205.json',
 'event_hall_entry':'files/fielddata/eventdata/zone_event/294_D24R0211.json',
 'script_sw_first':'files/fielddata/script/scr_seq/scr_seq_0043_D24R0206.s',
 'script_nw_first':'files/fielddata/script/scr_seq/scr_seq_0045_D24R0208.s'})
SHAS.update({'matrix_hall':'864f1321126e3de049b769b9239114bc217920d0',
 'event_hall':'0533fde38c55857f57d59556204b1ef02731f2a1',
 'event_hall_entry':'ed0130f303b44882295ac8de1b2e9b310e72eb83',
 'script_sw_first':'c93945c7a60722a967db9608c59ca416414eb119',
 'script_nw_first':'6b70939c38e9ec1c8bf8ba78e82d493ed36885f3'})
def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def build(archive,reference_dir=None):
 data=archive.read_bytes();assert blob(data)==ARCHIVE_SHA
 offset=16;assert data[:4]==b'NARC'
 while offset<len(data):
  magic,length=struct.unpack_from('<4sI',data,offset)
  if magic==b'GMIF':base=offset+8;break
  offset+=length
 else:raise AssertionError('Missing terrain archive GMIF')
 sources={}
 for name,path in FILES.items():
  if reference_dir:
   raw=(reference_dir/Path(path).name).read_bytes()
  else:
   raw=urllib.request.urlopen(f'https://raw.githubusercontent.com/pret/pokeheartgold/{REV}/{path}',timeout=30).read()
  assert blob(raw)==SHAS[name],name
  sources[name]=raw
 def terrain(name):
  matrix=sources[name];assert matrix[:4]==bytes([1,1,0,0]);model=struct.unpack_from('<H',matrix,5+matrix[4])[0]
  start,end=struct.unpack_from('<II',data,28+model*8);record=data[base+start:base+end]
  perm_bytes,prop_bytes,_,_=struct.unpack_from('<4I',record);magic,extra=struct.unpack_from('<2H',record,16)
  assert perm_bytes==2048 and prop_bytes==0 and magic==0x1234
  return dict(model=model,permissions=list(struct.unpack_from('<1024H',record,20+extra)))
 def hall():
  matrix=sources['matrix_hall'];assert matrix[:4]==bytes([1,2,0,0])
  models=struct.unpack_from('<2H',matrix,5+matrix[4]);assert models==(470,471)
  chunks=[]
  for model in models:
   start,end=struct.unpack_from('<II',data,28+model*8);record=data[base+start:base+end]
   perm_bytes,prop_bytes,_,_=struct.unpack_from('<4I',record);magic,extra=struct.unpack_from('<2H',record,16)
   assert perm_bytes==2048 and prop_bytes%48==0 and magic==0x1234
   chunks.append(list(struct.unpack_from('<1024H',record,20+extra)))
  e=json.loads(sources['event_hall']);entry=json.loads(sources['event_hall_entry'])
  assert [(w['x'],w['z'],w['anchor']) for w in e['warps']]==[(18,24,1),(18,23,1)]
  assert [(w['x'],w['z'],w['anchor']) for w in entry['warps'][:2]]==[(6,13,8),(6,7,0)]
  return dict(matrix_dimensions=[1,2],models=list(models),permissions=chunks,
      exits=[[w['x'],w['z'],w['anchor']] for w in e['warps']],
      entrance_exits=[[w['x'],w['z'],w['header'],w['anchor']] for w in entry['warps'][:2]],
      background_positions=[[o['x'],o['z']] for o in e['bgs']],
      object_positions=[[o['x'],o['z']] for o in e['objects']])
 def event(name):return json.loads(sources[name])
 sw_hidden=event('event_sw_hidden');nw_hidden=event('event_nw_hidden')
 nw_second=event('event_nw_second');sw_second=event('event_sw_second')
 for e in (nw_second,sw_second):
  assert len(e['warps'])==1 and (e['warps'][0]['x'],e['warps'][0]['z'],e['warps'][0]['anchor'])==(6,17,1)
  assert len(e['coords'])==1 and (e['coords'][0]['x'],e['coords'][0]['z'])==(6,3)
 for e,point in ((sw_hidden,(20,13)),(nw_hidden,(20,21))):
  assert not e.get('warps') and len(e['coords'])==1 and (e['coords'][0]['x'],e['coords'][0]['z'])==point
 for script,dest in [('script_sw_second','MAP_RUINS_OF_ALPH_SOUTHWEST_HIDDEN_ROOM, 0, 11, 7'),
                     ('script_nw_second','MAP_RUINS_OF_ALPH_NORTHWEST_HIDDEN_ROOM, 0, 11, 14'),
                     ('script_sw_hidden','MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 0, 5, 42'),
                     ('script_nw_hidden','MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 0, 5, 24'),
                     ('script_sw_first','MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 0, 5, 42'),
                     ('script_nw_first','MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 0, 5, 24')]:
  assert re.search(r'\bWarp\s+'+re.escape(dest)+r'\b',sources[script].decode()),script
 return dict(revision=REV,terrain_blob_sha=ARCHIVE_SHA,sources={k:dict(path=FILES[k],blob_sha=SHAS[k]) for k in FILES},
  second=dict(**terrain('matrix_second'),exit=[6,17],fall=[6,3],northwest_object_positions=[[o['x'],o['z']] for o in nw_second['objects']],
              southwest_object_positions=[[o['x'],o['z']] for o in sw_second['objects']]),
  hall=hall(),
  northwest_hidden=dict(**terrain('matrix_nw'),landing=[11,14],exit=[20,21],hall_landing=[5,24]),
  southwest_hidden=dict(**terrain('matrix_sw'),landing=[11,7],exit=[20,13],hall_landing=[5,42]))

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--reference-dir',type=Path);p.add_argument('--output',type=Path,default=ROOT/'crossroads/hgss/canonical_events/ruins-hidden-geometry.json');p.add_argument('--check',action='store_true');a=p.parse_args()
 result=build(a.archive,a.reference_dir)
 if a.check:assert json.loads(a.output.read_text())==result
 else:a.output.write_text(json.dumps(result,indent=2)+'\n')
 print('Pinned hidden-room permissions, entrances and scripted falls: source facts verified; no game maps activated.')
if __name__=='__main__':main()
