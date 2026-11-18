#!/usr/bin/env python3
"""Verify uninstalled gate art and conditions; this is not gameplay testing."""
import io,json,re,struct
from pathlib import Path
from PIL import Image
from stage_hgss_ruins_gate_art import stage as stage_art
from stage_hgss_ruins_gate_events import stage as stage_events
from stage_hgss_ruins_hidden_graph import stage as stage_graph,FIRST,IDS

R=Path(__file__).resolve().parents[2]
def read(p):return (R/p).read_bytes()
def words(b):return struct.unpack('<%dH'%(len(b)//2),b)

def run():
 files={}
 def write(path,value):assert path not in files;files[path]=value
 meta=stage_art(write);assert meta==40 and len(files)==19
 root='data/tilesets/primary/hgssruinschamber'
 for file in ('metatiles.bin','metatile_attributes.bin'):
  old=read(f'{root}/{file}');new=files[f'{root}/{file}'];assert new.startswith(old)
  assert len(new)-len(old)==(16 if file=='metatiles.bin' else 2)
 attrs=words(files[root+'/metatile_attributes.bin']);assert attrs[40]==0x60
 old_meta=words(read(root+'/metatiles.bin'));assert all(v>>12<5 for v in old_meta)
 for i in range(5):assert files[f'{root}/palettes/{i:02}.pal']==read(f'{root}/palettes/{i:02}.pal')
 src='crossroads/donor/hns-ruins-pockets/data/tilesets/secondary/ruins_of_alph_writing_hns'
 assert files[root+'/palettes/05.pal']==read(src+'/palettes/11.pal')
 old_sheet=Image.open(io.BytesIO(read(root+'/tiles.png')));new_sheet=Image.open(io.BytesIO(files[root+'/tiles.png']))
 assert new_sheet.size==(128,48) and new_sheet.crop((0,0,128,40)).tobytes()==old_sheet.tobytes()
 donor=Image.open(io.BytesIO(read(src+'/tiles.png')))
 packed=words(files[root+'/metatiles.bin'])[40*8:41*8];expected=(734,735,750,751)
 for i,source_tile in enumerate(expected):
  entry=packed[i];assert entry>>12==5 and not entry&0xc00
  a=source_tile-640;b=entry&1023
  def tile(im,n):return im.crop(((n%16)*8,(n//16)*8,(n%16+1)*8,(n//16+1)*8)).tobytes()
  assert tile(donor,a)==tile(new_sheet,b)
 assert packed[4:]==(0,0,0,0)
 rooms={};scripts={}
 for name in ('RuinsOfAlph_SouthwestChamber','RuinsOfAlph_NorthwestChamber'):
  m=json.loads(read(f'data/maps/{name}/map.json'));rooms[m['id']]=m;scripts[m['id']]=read(f'data/maps/{name}/scripts.inc').decode()
 *_,proposals,gates=stage_graph(lambda p,b:None,rooms)
 mapped,output=stage_events(proposals,scripts,meta)
 for i,key in enumerate(FIRST):
  assert mapped[key]['warp_events']==proposals[key]['warp_events']
  assert mapped[key]['bg_events'][:-1]==rooms[key]['bg_events']
  assert (mapped[key]['bg_events'][-1]['x'],mapped[key]['bg_events'][-1]['y'])==(5,1)
  assert mapped[key]['bg_events'][-1]['player_facing_dir']=='BG_EVENT_PLAYER_FACING_NORTH'
  s=output[key];assert s.startswith(scripts[key])
  assert ('checkitem ITEM_WATER_STONE, 1' if i==0 else 'checkspecies SPECIES_HO_OH') in s
  assert f'warp {IDS[i]}, 6, 17' in s and 'setmetatile 5, 1, 40, FALSE' in s
  assert not re.search(r'^\s*(?:setflag|clearflag|giveitem|removeitem|givemon)\b',s,re.M)
  assert gates[key]['installed'] is False
 return files,mapped,output

if __name__=='__main__':
 assert run()==run()
 print('Staged gate: existing pixels/metatiles/palettes preserved, donor door exact, nonconsuming condition and safe return proposals PASS; no engine/visual test.')
