#!/usr/bin/env python3
"""Shared actual-controller harness for the focused QA10 city detail runners.

The four existing menu/Save/Continue functions are loaded without executing the
legacy25-case test script. This reuses its real UI/inventory integrity checks,
not game initialization or coordinate fixtures. Only the shared harness's
explicit encounter-suppression RAM write is used; no XY/warp/flag setup.
"""
from pathlib import Path
from types import SimpleNamespace
import ast,hashlib,json,runpy,subprocess,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def load(save,library,output,rom_sha256):
    save=Path(save);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256((ROOT/'pokeemerald.gba').read_bytes()).hexdigest()==rom_sha256
    battery_hash=hashlib.sha256(save.read_bytes()).hexdigest()
    sys.argv=['johto_network_smoke.py','--save',str(save),'--library',str(library),'--output',str(output),'--targets','']
    d=runpy.run_path(str(ROOT/'crossroads/tools/johto_network_smoke.py'))
    ns={name:d[name] for name in ['go','walk','read','write','frames','key','current','pos','close','lib','syms','sb']}
    ns.update(R=ROOT,out=output,a=SimpleNamespace(save=save),d=d,records=[],hashlib=hashlib,json=json)
    source=(ROOT/'crossroads/tools/olivine_save_smoke.py').read_text()
    wanted={'memory','inventory_state','menu','save_continue','clear_point'}
    nodes=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    assert len(nodes)==len(wanted)
    for node in nodes:exec(compile(ast.Module(body=[node],type_ignores=[]),'olivine_save_smoke.py','exec'),ns)
    g=ns['walk'].__globals__;g['dry_only']=True;g['route_cache'].clear()
    if ns['read']('sJohtoTestAccess',1):
        ns['go']('OlivineCity_HarborOffice');ns['walk']((1,6));flags=ns['memory'](ns['sb']()+0x1270,300)
        ns['frames'](1,64);ns['frames'](20);ns['key'](1);ns['frames'](180)
        for _ in range(8):
            if not ns['read']('sLockFieldControls',1):break
            ns['key'](1);ns['frames'](180)
        assert ns['memory'](ns['sb']()+0x1270,300)==flags
    assert ns['read']('sJohtoTestAccess',1)==0
    views=[];clips=[]
    def facing():
        event=ns['read'](ns['syms']['gPlayerAvatar']+5,1)
        return ns['read'](ns['syms']['gObjectEvents']+event*36+24,1)&15
    def shot(label):
        ns['frames'](30);path=output/(label+'.png');assert ns['lib'].emu_image(str(path).encode())
        image=Image.open(path).convert('RGB');assert image.size==(240,160)
        assert not any(c==(255,0,255) for c in image.getdata()),(label,'Debug magenta')
        views.append(dict(label=label,map=ns['current'](),position=ns['pos'](),facing=facing(),native_size=[240,160],debug_magenta=0))
        return image
    def capture(label,action):
        native=g['frames'];local=ns['frames'];folder=output/(label+'-frames');folder.mkdir(exist_ok=True);count=0
        def recording(n=60,k=0):
            nonlocal count
            while n:
                step=min(4,n);native(step,k);n-=step
                assert ns['lib'].emu_image(str(folder/f'{count:04d}.png').encode());count+=1
        g['frames']=recording;ns['frames']=recording
        try:
            result=action();recording(24);return result
        finally:
            g['frames']=native;ns['frames']=local
            if count:
                subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(output/(label+'.mp4'))],check=True)
                clips.append(dict(label=label,native_size=[240,160],frame_count=count))
    def finish(extra=None,error=None):
        assert hashlib.sha256(save.read_bytes()).hexdigest()==battery_hash
        assert hashlib.sha256((ROOT/'pokeemerald.gba').read_bytes()).hexdigest()==rom_sha256
        report=dict(rom_sha256=rom_sha256,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_battery_sha256=battery_hash,source_battery_unchanged=True,setup='Copied normal battery; cold Continue, normal controller paths and real desk OFF. Save/Continue uses actual UI and private output batteries; exact party/boxes/decoded inventory/flags/starter checked. No player/map/warp/flag coordinate fixtures; only shared encounter suppression in test RAM.',views=views,recordings=clips,normal_save_continue=ns['records'],final_map=ns['current'](),final_position=ns['pos'](),final_survey_access=ns['read']('sJohtoTestAccess',1),owner_delta_visual_acceptance='PENDING',error=error)
        if extra:report.update(extra)
        (output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    ns.update(g=g,shot=shot,capture=capture,finish=finish,facing=facing)
    return ns
