#!/usr/bin/env python3
"""Walk every corrected court cell and verify real composed Joe visibility."""
import argparse,ast,json
from pathlib import Path
from qa10_city_runtime import load
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',required=True);p.add_argument('--rom-sha256',required=True);args=p.parse_args()
h=load(args.save,args.library,args.output,args.rom_sha256)
# Independent hardware sprite/framebuffer check already used for the gate repro.
source=Path(__file__).with_name('gate_layer_smoke.py').read_text();node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='joe_pixels');exec(compile(ast.Module(body=[node],type_ignores=[]),'gate_layer_smoke.py','exec'),h)
rows=[]
def message(label):
    address=h['syms'][label];data=bytearray()
    for i in range(512):
        value=h['read'](address+i,1);data.append(value)
        if value==255:return bytes(data)
    raise AssertionError(('Unterminated native message',label))
def main():
    d=h['d'];h['go']('EcruteakCity');contract=json.loads((h['R']/'crossroads/hgss/qa10/ecruteak-court-art-contract.json').read_text());assert len(contract['cells'])==39
    def circuit():
        for row in sorted(contract['cells'],key=lambda q:(q['y'],q['x'] if q['y']%2==0 else -q['x'])):
            point=(row['x'],row['y']);h['walk'](point);frame=h['shot']('court-'+str(point[0])+'-'+str(point[1]));visible=h['joe_pixels'](frame)
            assert h['current']()=='EcruteakCity' and h['pos']()==point and not h['read']('gPlayerAvatar',1)&8
            assert visible['opaque_expected']>0 and visible['opaque_hidden']==0,(point,'Court ground hides Joe',visible)
            rows.append(dict(point=point,visibility=visible,result='PASS'))
    h['capture']('court-normal-controller-circuit',circuit)
    for label,point,button in [('north',(36,44),128),('south',(36,46),64),('west',(35,45),16),('east',(37,45),32)]:
        h['walk'](point);h['frames'](1,button);h['frames'](20);h['key'](1);h['frames'](120)
        assert h['read']('sLockFieldControls',1),'Directory A interaction did not open text'
        assert message('gStringVar4')==message('Ecruteak_Directory_Text'),'Wrong displayed directory message'
        h['shot']('court-directory-'+label+'-message');h['close']();assert h['current']()=='EcruteakCity' and h['pos']()==point and not h['read']('sLockFieldControls',1)
    h['walk']((35,44));h['save_continue']('court-normal-save');h['walk']((34,44));h['shot']('court-after-normal-continue-walkaway')
    assert h['read']('sJohtoTestAccess',1)==0
    h['finish'](dict(corrected_cells=rows,directory_sides=['north','south','west','east'],actual_post_continue_walk_away=h['pos']()));print('Ecruteak court PASS:',len(rows),'actual cells/full Joe visibility,4 directory sides,normal Save/cold Continue',flush=True)
try:main()
except Exception as error:
    h['lib'].emu_image(str(Path(args.output)/'failure.png').encode());h['finish'](dict(corrected_cells=rows),str(error));raise
