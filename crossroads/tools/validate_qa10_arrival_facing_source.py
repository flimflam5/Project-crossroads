#!/usr/bin/env python3
"""Independent scope/control-flow checks for the native25-cell facing repair.

No generator is imported. Final checks require all45 explicit physical-facing
expectations and preservation of B4 map/graphics/ID data outside6 script hooks.
"""
import argparse
import hashlib
import json
import re
import shutil
import struct
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[2]
BASE = 'df8c4598d88c7770626be4621a5f39cf60dadb95'
# Independently reviewed physical landings. These literals are not imported
# from the authoring helper or learned from controller outcomes.
EXPECTED = {
    'EcruteakCity': {(7,37):'DIR_EAST',(7,38):'DIR_EAST',(7,39):'DIR_EAST',
        (59,46):'DIR_WEST',(59,47):'DIR_WEST',(59,48):'DIR_WEST'},
    'JohtoRoute38': {(62,12):'DIR_WEST',(62,13):'DIR_WEST',(62,14):'DIR_WEST'},
    'JohtoRoute42': {(3,13):'DIR_EAST',(3,14):'DIR_EAST',(3,15):'DIR_EAST'},
    'EcruteakCity_WestGate': {(1,6):'DIR_EAST',(1,7):'DIR_EAST',(1,8):'DIR_EAST',
        (10,6):'DIR_WEST',(10,7):'DIR_WEST',(10,8):'DIR_WEST'},
    'EcruteakCity_EastGate': {(1,6):'DIR_EAST',(1,7):'DIR_EAST',(1,8):'DIR_EAST',
        (10,6):'DIR_WEST',(10,7):'DIR_WEST',(10,8):'DIR_WEST'},
    'EcruteakCity_BarrierCorridor': {(6,3):'DIR_SOUTH'},
}
BEGIN = '@ BEGIN QA10 COORDINATE-SCOPED ARRIVAL FACING'
END = '@ END QA10 COORDINATE-SCOPED ARRIVAL FACING'


def validate_callbacks(scripts_root=R):
    layouts={v['id']:v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
    simulations=0
    for name, coordinates in EXPECTED.items():
        path=f'data/maps/{name}/scripts.inc'
        original=subprocess.check_output(['git','show',BASE+':'+path],cwd=R,text=True)
        actual=(scripts_root/path).read_text()
        prefix='Qa10_'+name+'_ArrivalFacing'
        hook='    map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, '+prefix+'_Table\n'
        return_hook='    map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, '+prefix+'\n'
        assert actual.count(hook)==actual.count(return_hook)==actual.count(BEGIN)==actual.count(END)==1,name
        before,rest=actual.split(BEGIN);block,after=rest.split(END)
        restored=(before.replace(hook,'',1).replace(return_hook,'',1)+after).rstrip()+'\n'
        assert restored==original,('Existing native map scripts changed beyond the scoped hook',name)
        lines=[s.strip()for s in block.splitlines()if s.strip()]
        assert lines[:3]==[prefix+'_Table:',
            'map_script_2 VAR_TEMP_0, VAR_TEMP_0, '+prefix,'.2byte 0'],name
        commands=[];labels={}
        for line in lines[3:]:
            if line.endswith(':'):
                label=line.rstrip(':');assert label not in labels
                labels[label]=len(commands)
            else:
                assert re.fullmatch(r'getplayerxy VAR_0x8004, VAR_0x8005|goto_if_eq VAR_0x800[45], \d+, \w+|turnobject LOCALID_PLAYER, DIR_(?:NORTH|SOUTH|WEST|EAST)|end',line),(name,'Forbidden effects/command',line)
                commands.append(line)
        assert sum(s.startswith('getplayerxy')for s in commands)==1,name
        mapj=json.loads((R/f'data/maps/{name}/map.json').read_text());layout=layouts[mapj['layout']]
        assert all(0<=x<layout['width']and 0<=y<layout['height']for x,y in coordinates)
        for y in range(layout['height']):
            for x in range(layout['width']):
                pc=labels[prefix];regs={};turns=[]
                for _ in range(40):
                    cmd=commands[pc];pc+=1
                    if cmd=='end':break
                    if cmd.startswith('getplayerxy'):
                        regs.update(VAR_0x8004=x,VAR_0x8005=y)
                    elif cmd.startswith('goto_if_eq'):
                        var,value,label=cmd.removeprefix('goto_if_eq ').split(', ')
                        if regs[var]==int(value):pc=labels[label]
                    else:turns.append(cmd.removeprefix('turnobject LOCALID_PLAYER, '))
                else:raise AssertionError((name,'Unbounded callback',x,y))
                assert turns==([coordinates[x,y]]if(x,y)in coordinates else[]),(name,x,y,turns)
                simulations+=1
    return simulations


def validate_built():
    nm=shutil.which('arm-none-eabi-nm') or '/workspace/toolchain/root/usr/bin/arm-none-eabi-nm'
    symbols={p[2]:int(p[0],16) for line in subprocess.check_output(
        [nm,'-an',str(R/'pokeemerald.elf')],text=True).splitlines()
        if len(p:=line.split())==3}
    rom=(R/'pokeemerald.gba').read_bytes()
    def read(address,fmt):
        offset=address-0x08000000;size=struct.calcsize(fmt)
        assert 0<=offset<=len(rom)-size,('Compiled pointer leaves ROM',hex(address))
        return struct.unpack_from(fmt,rom,offset)
    groups=json.loads((R/'data/maps/map_groups.json').read_text())
    opcodes={n:int(v,16)for n,v in re.findall(r'(SCR_OP_\w+)\s*=\s*(0x[0-9A-Fa-f]+)',(R/'include/constants/script_commands.h').read_text())}
    directions={'DIR_SOUTH':1,'DIR_NORTH':2,'DIR_WEST':3,'DIR_EAST':4}
    report=[]
    assert 'gMapGroups' in symbols
    for name,coordinates in EXPECTED.items():
        prefix='Qa10_'+name+'_ArrivalFacing'
        required=[name,name+'_MapScripts',prefix,prefix+'_Table']
        required += [prefix+'_X'+str(x)for x in sorted({x for x,y in coordinates})]
        required += [prefix+'_'+d for d in sorted(set(coordinates.values()))]
        assert all(s in symbols for s in required),('Arrival callback absent from actual ELF',name,[s for s in required if s not in symbols])
        # Resolve the real compiled group->map header. A spare unreferenced table
        # or label in the ROM is insufficient proof of installed map callbacks.
        candidates=[(i,groups[g].index(name))for i,g in enumerate(groups['group_order'])if name in groups[g]]
        assert len(candidates)==1,(name,candidates)
        group,index=candidates[0]
        group_ptr,=read(symbols['gMapGroups']+group*4,'<I')
        header_ptr,=read(group_ptr+index*4,'<I')
        assert header_ptr==symbols[name],('Built map group points at another header',name)
        script_ptr,=read(header_ptr+8,'<I')
        assert script_ptr==symbols[name+'_MapScripts'],('Built map header lacks its script table',name)
        found=[];returns=[];tags=[];cursor=script_ptr
        for _ in range(20):
            tag,=read(cursor,'<B');cursor+=1
            if not tag:break
            pointer,=read(cursor,'<I');cursor+=4
            assert tag in range(1,8) and tag not in tags,(name,'Invalid/duplicate native map-script tag',tag)
            tags.append(tag)
            if tag==4:found.append(pointer)
            if tag==7:returns.append(pointer)
        else:raise AssertionError((name,'Unterminated actual map-script table'))
        assert found==[symbols[prefix+'_Table']],('Actual OnWarp pointer is missing/stale',name,found)
        assert returns==[symbols[prefix]],('Actual post-spawn OnReturn pointer is missing/stale',name,returns)
        var1,var2,target,terminator=read(found[0],'<HHIH')
        assert (var1,var2,target,terminator)==(0x4000,0x4000,symbols[prefix],0),('Actual OnWarp condition/target/terminator differs',name)
        assert read(target,'<BHH')==(opcodes['SCR_OP_GETPLAYERXY'],0x8004,0x8005),('Actual callback does not read only the reviewed coordinate scratch',name)
        for direction in set(coordinates.values()):
            assert read(symbols[prefix+'_'+direction],'<BHBB')==(opcodes['SCR_OP_TURNOBJECT'],255,directions[direction],opcodes['SCR_OP_END']),('Actual native turn body differs',name,direction)
        report.append(dict(map=name,group=group,map_number=index,map_header=hex(header_ptr),
            map_scripts=hex(script_ptr),on_warp_table=hex(found[0]),callback=hex(target),
            return_to_field_callback=hex(returns[0]),exact_self_comparison_and_terminator=True,compiled_player_turns=True))
    return dict(rom_sha256=hashlib.sha256(rom).hexdigest(),
        elf_sha256=hashlib.sha256((R/'pokeemerald.elf').read_bytes()).hexdigest(),maps=report,
        actual_group_headers_script_tables_and_turn_bodies_verified=6)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--built',action='store_true',help='Verify actual ROM group/header/OnWarp+OnReturn pointers, table and native turn bytes using ELF symbols')
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    assert subprocess.check_output(['git','rev-parse',BASE+'^{commit}'],cwd=R,text=True).strip()==BASE, 'Fetch the immutable full B4 commit before preservation checks'
    simulations=validate_callbacks()
    # No map/warp metadata, blockdata, metatile attrs/pixels or critical IDs may
    # change merely to repair facing. The already-pinned B4 assets are the base.
    paths=['data','src','include','graphics','sound','Makefile']
    changed=set(subprocess.check_output(['git','diff','--name-only',BASE,'--']+paths,cwd=R,text=True).splitlines())
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--']+paths,cwd=R,text=True).splitlines()
    assert not untracked,('Untracked game inputs escape the preservation baseline',untracked)
    allowed={f'data/maps/{n}/scripts.inc'for n in EXPECTED}
    assert changed==allowed,('Changes escaped the6 native scripts',sorted(changed-allowed),sorted(allowed-changed))
    manifest=json.loads((R/'crossroads/hgss/doorways-qa10.json').read_text())
    intended=json.loads((R/'crossroads/hgss/qa10/doorway-intended-facing-b4.json').read_text())
    groups={g['label']:g for g in manifest['groups']}
    assert len(groups)==len(intended['groups'])==45
    for expected in intended['groups']:
        actual=groups[expected['label']]
        for side in ['outside','inside']:
            s=expected['sides'][side]
            assert actual[side]['map']==s['map']and actual[side]['segments']==s['segments']
            assert actual[side].get('expected_facing')==s['intended_arrival_facing'],(expected['label'],side,'Missing/wrong independent facing expectation')
    assert sum(len(v['segments'])for g in groups.values()for k,v in g.items()if k in['outside','inside'])==173
    report=dict(source_preservation_baseline=BASE,source_coordinate_cases=simulations,
        exact_native_scripts=6,exact_landings=25,independent_facing_groups=45,
        all_other_game_inputs_unchanged=True)
    if a.built:report['built']=validate_built()
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(json.dumps(report,indent=2)+'\n')
    print('Independent native arrival-facing source checks:6 maps,25 exactcells,',simulations,'coordinate cases; allothergameinputs unchanged;45groups/173segments requireintendedfacing;', 'actual6ROM callbacks verified;'if a.built else'compiled callbacks not checked;', 'PASS')


if __name__=='__main__':main()
