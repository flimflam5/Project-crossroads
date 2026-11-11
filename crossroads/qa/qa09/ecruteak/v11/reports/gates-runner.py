import hashlib,io,json,runpy,subprocess,sys
from pathlib import Path
from PIL import Image,ImageChops
sys.path.insert(0,str(Path('crossroads/tools').resolve()))
sha='df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4'
assert hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()==sha
out=Path('build/qa09-ecruteak-gates-v11');out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save','build/area-delivery-sram/EcruteakCity_BellTower-save.state.sav','--library','/tmp/johto-bridge.so','--output',str(out),'--targets','']
q=runpy.run_path('crossroads/tools/johto_network_smoke.py');go,walk,read,frames,key,current,pos,close,lib=[q[k]for k in ['go','walk','read','frames','key','current','pos','close','lib']]
# Real terminal service interaction supplements the furniture collision trial.
go('EcruteakCity_PokemonCenter_B1F');walk((15,6));frames(1,64);frames(20);key(1);frames(120);assert read('sLockFieldControls',1)
lib.emu_image(str(out/'basement-communication-terminal-message.png').encode());close();assert current()=='EcruteakCity_PokemonCenter_B1F'and pos()==(15,6)and not read('sLockFieldControls',1)
print('Actual B1F terminal A dialogue and returned controls PASS',flush=True)
from validate_theater_stage import renderer,data
render,attr=renderer('hgss_gate_interior')
# Match the REAL third background layer from field_camera.c DrawMetatile:
# NORMAL inserts primary tile0x14/palette3 behind transparent bottom/top art.
# The earlier two-layer black-canvas approximation was invalid for plants.
sheet=Image.open(io.BytesIO(data('data/tilesets/primary/building/tiles.png')));glyph=sheet.crop((32,8,40,16));palette=[tuple(int(v)//8 for v in line.split())for line in data('data/tilesets/primary/building/palettes/03.pal').decode().splitlines()[3:]]
garbage=Image.new('RGBA',(8,8));garbage.putdata([tuple((c<<3)|(c>>2)for c in palette[i])+(255,)for i in glyph.tobytes()]);base=Image.new('RGBA',(16,16))
for x,y in [(0,0),(8,0),(0,8),(8,8)]:base.alpha_composite(garbage,(x,y))
def expected(n):
 bg=base.copy()if attr(n)>>12==0 else Image.new('RGBA',(16,16),(0,0,0,255));bg.alpha_composite(render(n));return bg.convert('RGB')
def signed(v):return v-65536 if v&0x8000 else v
results=[]
def report():
 (out/'results.json').write_text(json.dumps(dict(rom_sha256=sha,source_revision='489c404346f572aefb6856b3dd48a9b364a08ceb',method='Actual normal controller input on copied battery; no map/warp/player-coordinate writes. Two real camera positions cover complete upper/lower plants. Expected pixels include engine NORMAL-layer BG3 tile0x3014, not a black-canvas approximation.',results=results),indent=2)+'\n')
for direction in ['West','East']:
 name='EcruteakCity_'+direction+'Gate';go(name);records=[]
 for point,bases,style in [((6,6),[(2,3),(10,3)],[(5,2,'window'),(4,4,'upper-counter')]),((6,7),[(2,11),(10,11)],[(4,7,'floor'),(4,9,'lower-counter')])]:
  walk(point);frames(30);p=out/(direction.lower()+'-gate-'+str(point[1])+'.png');lib.emu_image(str(p).encode());frame=Image.open(p).convert('RGB');assert frame.size==(240,160);assert not any(c==(255,0,255)for c in frame.getdata()),'Debug magenta in compiledgate';raw=q['raw'][name];panx=signed(read('sHorizontalCameraPan',2));pany=signed(read('sVerticalCameraPan',2))+8
  cells=[(x,y+dy,'plant')for x,y in bases for dy in(-1,0)]+style
  for x,y,kind in cells:
   xx=(x+7-pos()[0])*16-panx;yy=(y+7-pos()[1])*16-pany;assert 0<=xx<=224 and 0<=yy<=144,(name,kind,x,y,xx,yy,'Clipped test region')
   predicted=expected(raw[y*12+x]&1023);actual=frame.crop((xx,yy,xx+16,yy+16));assert ImageChops.difference(actual,predicted).getbbox()is None,(name,kind,x,y,'Compiled native tile mismatch')
   records.append(dict(kind=kind,source_cell=[x,y],camera_player=list(pos()),screen_top_left=[xx,yy],pixels_matched=256))
 results.append(dict(case=name+' actual complete four-plants/window/counters/floor pixels',result='PASS',native_pixels_matched=sum(r['pixels_matched']for r in records),records=records));report()
 walk((3,7));frames(20);folder=out/(direction.lower()+'-gate-walking');folder.mkdir(exist_ok=True)
 for i in range(120):
  frames(1,16 if pos()!=(8,7)else 0)
  if i%4==0:lib.emu_image(str(folder/f'{i//4:04d}.png').encode())
 assert current()==name and pos()==(8,7),(name,current(),pos())
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(direction.lower()+'-gate-walking.mp4'))],check=True)
 results.append(dict(case=name+' normal left-to-right floor movement',start=[3,7],end=[8,7],result='PASS'));report();print(name,'all3072 compiled pixels and normal walking PASS',flush=True)
assert hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()==sha
print('Both gate supplemental suites PASS on exact final V11 ROM',flush=True)
