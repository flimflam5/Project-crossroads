#!/usr/bin/env python3
"""Run actual continue C source on host using fixture engine types; not an emulator.

Compiles the unchanged C function bodies, embeds generated real masks and loads
actual candidate map.bin files. Engine functions and save structs are minimal
mocks; no ROM, user's save, hardware graphics or game ABI are exercised.
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
source = (R / 'src/crossroads_continue.c').read_text()
source = re.sub(r'^#include .*\n', '', source, flags=re.M)

def embedded(match):
    data = (R / match.group(1)).read_bytes()
    return '{' + ','.join(map(str, data)) + '}'
source = re.sub(r'INCBIN_U8\("([^"\n]+)"\)', embedded, source)
layouts = json.loads((R / 'data/layouts/layouts.json').read_text())['layouts']
layout_ids = {v['id']: i + 1 for i, v in enumerate(layouts)}
groups = json.loads((R / 'data/maps/map_groups.json').read_text())
map_ids = {}
for group_id, group_name in enumerate(groups['group_order']):
    for map_id, name in enumerate(groups[group_name]):
        data = json.loads((R / 'data/maps' / name / 'map.json').read_text())
        map_ids[data['id']] = (group_id << 8) | map_id
required_maps = ['MAP_UNION_CAVE_1_F','MAP_UNION_CAVE_2_F','MAP_UNION_CAVE_3_F',
                 'MAP_AZALEA_TOWN','MAP_ECRUTEAK_CITY','MAP_VIOLET_CITY','MAP_OLIVINE_CITY']
required_layouts = ['LAYOUT_UNION_CAVE_1_F','LAYOUT_UNION_CAVE_2_F','LAYOUT_UNION_CAVE_3_F',
                    'LAYOUT_HGSS_UNION_CAVE_1_F','LAYOUT_HGSS_UNION_CAVE_2_F','LAYOUT_HGSS_UNION_CAVE_3_F']
defines = ''.join(f'#define {n} {map_ids[n]}\n' for n in required_maps)
defines += ''.join(f'#define {n} {layout_ids[n]}\n' for n in required_layouts)
prelude = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32;
typedef int16_t s16; typedef int32_t bool32;
#define TRUE 1
#define FALSE 0
#define MAP_GROUP(id) ((id) >> 8)
#define MAP_NUM(id) ((id) & 255)
#define MAPGRID_COLLISION_MASK 0x0c00
#define MAP_OFFSET 7
#define WARP_ID_NONE -1
#define OBJECT_EVENTS_COUNT 16
#define OBJ_EVENT_GFX_JOE_SURFING 0x3f09
#define OBJ_EVENT_GFX_BRENDAN_SURFING 22
#define OBJ_EVENT_GFX_MAY_SURFING 23
#define PLAYER_AVATAR_STATE_NORMAL 0
#define HEAL_LOCATION_OLIVINE_CITY 1
#define HEAL_LOCATION_ECRUTEAK_CITY 2
#define HEAL_LOCATION_VIOLET_CITY 3
#define AZALEA_KILN_ORIGIN_X 19
#define AZALEA_KILN_ORIGIN_Y 30
#define AZALEA_KILN_WIDTH 4
#define AZALEA_KILN_HEIGHT 4
struct Coords { s16 x, y; };
struct ObjectEvent { unsigned isPlayer; u16 graphicsId; u8 spriteId; struct Coords initialCoords, currentCoords, previousCoords; };
struct WarpData { s16 mapGroup, mapNum, warpId, x, y; };
struct MapLayout { int width, height; const u16 *map; };
struct Event { s16 x, y; };
struct Events { u32 warpCount, objectEventCount; struct Event *warps, *objectEvents; };
struct MapHeader { const struct MapLayout *mapLayout; u16 mapLayoutId; struct Events *events; } gMapHeader;
static struct MapHeader b1header;
static struct MapLayout b1layout;
static struct Events b1events;
static u16 b1cells[32 * 64];
static const struct MapHeader *Overworld_GetMapHeaderByGroupAndId(int group, int num) {
    assert(group == MAP_GROUP(MAP_UNION_CAVE_2_F) && num == MAP_NUM(MAP_UNION_CAVE_2_F));
    return &b1header;
}
struct Save1 { struct WarpData location, lastHealLocation; u16 mapLayoutId; u8 mapView[128]; struct Coords pos; struct ObjectEvent objectEvents[OBJECT_EVENTS_COUNT]; u8 preserved[128]; } s1;
struct Save2 { u8 playerGender; } s2;
struct Save1 *gSaveBlock1Ptr = &s1; struct Save2 *gSaveBlock2Ptr = &s2;
struct ObjectEvent gObjectEvents[OBJECT_EVENTS_COUNT];
static int setLayoutCalls, healCalls;
static int Johto_IsExplorationGroup(int group) { return group == MAP_GROUP(MAP_UNION_CAVE_1_F); }
static void SetLastHealLocationWarp(int value) { (void)value; healCalls++; }
static void SetCurrentMapLayout(u16 id) { gSaveBlock1Ptr->mapLayoutId = id; setLayoutCalls++; }
static void CpuFill16(int value, void *dst, size_t size) { memset(dst, value, size); }
static u16 GetPlayerAvatarGraphicsIdByStateIdAndGender(int state, int gender) { (void)state; (void)gender; return 42; }
'''
harness = r'''
static u16 cells[32 * 96];
static struct MapLayout layout;
static struct Events events;
static struct Event eventObjects[2], eventWarps[2];
static void init(int map, int oldLayout, int newLayout, int height) {
    char path[128]; FILE *f;
    memset(&s1,0,sizeof(s1)); memset(&s2,0,sizeof(s2)); memset(gObjectEvents,0,sizeof(gObjectEvents));
    memset(&events,0,sizeof(events)); memset(eventObjects,0,sizeof(eventObjects)); memset(eventWarps,0,sizeof(eventWarps));
    memset(s1.preserved,0xa5,sizeof(s1.preserved)); memset(s1.mapView,0x5a,sizeof(s1.mapView));
    s1.location.mapGroup = MAP_GROUP(map); s1.location.mapNum = MAP_NUM(map); s1.mapLayoutId = oldLayout;
    s1.lastHealLocation.mapGroup = 4; s1.lastHealLocation.warpId = WARP_ID_NONE;
    events.warps=eventWarps; events.objectEvents=eventObjects;
    snprintf(path,sizeof(path),"data/layouts/HgssUnionCave_%dF/map.bin", map-MAP_UNION_CAVE_1_F+1);
    f=fopen(path,"rb"); assert(f); assert(fread(cells,2,32*height,f)==(size_t)(32*height)); fclose(f);
    f=fopen("data/layouts/HgssUnionCave_2F/map.bin","rb"); assert(f); assert(fread(b1cells,2,32*64,f)==32*64); fclose(f);
    memset(&b1events,0,sizeof(b1events)); b1layout.width=32; b1layout.height=64; b1layout.map=b1cells;
    b1header.mapLayout=&b1layout; b1header.mapLayoutId=LAYOUT_HGSS_UNION_CAVE_2_F; b1header.events=&b1events;
    layout.width=32; layout.height=height; layout.map=cells;
    gMapHeader.mapLayout=&layout; gMapHeader.mapLayoutId=newLayout; gMapHeader.events=&events;
    setLayoutCalls=healCalls=0;
    s1.objectEvents[0].isPlayer=1; s1.objectEvents[0].spriteId=127;
    s1.objectEvents[0].graphicsId=0x2a00; gObjectEvents[0].isPlayer=1; gObjectEvents[0].graphicsId=42;
}
static void at(int i) {
    s1.pos.x=i%32; s1.pos.y=i/32;
    s1.objectEvents[0].currentCoords.x=gObjectEvents[0].currentCoords.x=s1.pos.x+MAP_OFFSET;
    s1.objectEvents[0].currentCoords.y=gObjectEvents[0].currentCoords.y=s1.pos.y+MAP_OFFSET;
}
static void setSurf(void) { u16 v=OBJ_EVENT_GFX_JOE_SURFING; s1.objectEvents[0].graphicsId=(v>>8)|(v<<8); gObjectEvents[0].graphicsId=v; }
static int find(const u8 *m,int n,int yes,int no,int oldBounds) {
    for(int i=0;i<n;i++) if((m[i]&yes)==yes && !(m[i]&no) && (!oldBounds || (i%32<28 && i/32<22))) return i;
    return -1;
}
static void unchangedData(void) { for(size_t i=0;i<sizeof(s1.preserved);i++)assert(s1.preserved[i]==0xa5); assert(!healCalls); }
static int posIndex(void) { return s1.pos.y*32+s1.pos.x; }
static void run(int map,int legacy,int modern,int height,const u8 *mask) {
    int total=32*height, pub=find(mask,total,4,0,0), isolated=find(mask,total,1,4,1), water=find(mask,total,2,0,0), invalid=find(mask,total,0,7,1);
    assert(pub>=0 && isolated>=0 && water>=0 && invalid>=0);
    init(map,legacy,modern,height); at(isolated); assert(Crossroads_PrepareContinue());
    if(map==MAP_UNION_CAVE_3_F) {
        assert(s1.location.mapNum==MAP_NUM(MAP_UNION_CAVE_2_F));
        assert(gMapHeader.mapLayoutId==LAYOUT_HGSS_UNION_CAVE_2_F && s1.mapLayoutId==LAYOUT_HGSS_UNION_CAVE_2_F);
        assert(sUnionCaveB1FContinueMask[posIndex()]&4);
        assert(s1.location.warpId==WARP_ID_NONE && s1.location.x==WARP_ID_NONE && s1.location.y==WARP_ID_NONE);
    } else { assert(posIndex()!=isolated); assert(mask[posIndex()]&4); }
    assert(setLayoutCalls==1); unchangedData();
    // Public coordinates outside the old 28x22 layout are synthetic; they
    // test the C discriminator, not a physically possible old save.
    init(map,legacy,modern,height); at(pub); assert(Crossroads_PrepareContinue());
    if(map==MAP_UNION_CAVE_3_F) { assert(s1.location.mapNum==MAP_NUM(MAP_UNION_CAVE_2_F)); assert(sUnionCaveB1FContinueMask[posIndex()]&4); }
    else assert(posIndex()==pub);
    assert(setLayoutCalls==1); unchangedData();
    if(map==MAP_UNION_CAVE_3_F) {
        // The old B2F had no water, but a synthetic legacy Surf state must not
        // remain surfing after relocation to the public B1F dry component.
        init(map,legacy,modern,height); at(isolated); setSurf(); assert(Crossroads_PrepareContinue());
        assert(s1.location.mapNum==MAP_NUM(MAP_UNION_CAVE_2_F));
        assert(sUnionCaveB1FContinueMask[posIndex()]&4 && !SavedPlayerWasSurfing());
        assert(gObjectEvents[0].graphicsId==42); unchangedData();
    }
    init(map,modern,modern,height); at(isolated); assert(Crossroads_PrepareContinue()); assert(posIndex()==isolated); assert(!setLayoutCalls); unchangedData();
    init(map,modern,modern,height); at(water); setSurf(); assert(Crossroads_PrepareContinue()); assert(posIndex()==water); assert(SavedPlayerWasSurfing()); unchangedData();
    init(map,modern,modern,height); at(water); assert(Crossroads_PrepareContinue()); assert(mask[posIndex()]&4); assert(!SavedPlayerWasSurfing()); unchangedData();
    init(map,modern,modern,height); at(invalid); assert(Crossroads_PrepareContinue()); assert(mask[posIndex()]&4); unchangedData();
    init(map,modern,modern,height); at(pub); events.objectEventCount=1; eventObjects[0].x=pub%32; eventObjects[0].y=pub/32; assert(Crossroads_PrepareContinue()); assert(posIndex()!=pub && (mask[posIndex()]&4)); unchangedData();
    init(map,modern,modern,height); at(invalid); setSurf(); assert(Crossroads_PrepareContinue()); assert(mask[posIndex()]&4); assert(!SavedPlayerWasSurfing()); assert(gObjectEvents[0].graphicsId==42); unchangedData();
    // Wrong previous layout must not be mistaken for this map's legacy ID.
    init(map,legacy+100,modern,height); at(isolated); assert(Crossroads_PrepareContinue()); assert(posIndex()==isolated); assert(setLayoutCalls==1); unchangedData();
    // A different map in the same group must not activate cave migration.
    init(map,legacy,modern,height); at(isolated); s1.location.mapNum=MAP_NUM(MAP_AZALEA_TOWN); assert(Crossroads_PrepareContinue()); assert(posIndex()==isolated); unchangedData();
    // Unexpected current map dimensions must not index the fixed-size mask.
    init(map,modern,modern,height); layout.width=28; layout.height=22; at(0); cells[0]=0x3001; assert(Crossroads_PrepareContinue()); assert(posIndex()==0); unchangedData();
    printf("map %d: 11 actual-C fixture cases PASS\n",map);
}
int main(void) {
    run(MAP_UNION_CAVE_1_F,LAYOUT_UNION_CAVE_1_F,LAYOUT_HGSS_UNION_CAVE_1_F,96,sUnionCave1FContinueMask);
    run(MAP_UNION_CAVE_2_F,LAYOUT_UNION_CAVE_2_F,LAYOUT_HGSS_UNION_CAVE_2_F,64,sUnionCaveB1FContinueMask);
    run(MAP_UNION_CAVE_3_F,LAYOUT_UNION_CAVE_3_F,LAYOUT_HGSS_UNION_CAVE_3_F,96,sUnionCaveB2FContinueMask);
    init(MAP_UNION_CAVE_1_F,LAYOUT_HGSS_UNION_CAVE_1_F,LAYOUT_HGSS_UNION_CAVE_1_F,96); s1.location.mapGroup=0; at(0); assert(!Crossroads_PrepareContinue()); assert(!setLayoutCalls); unchangedData();
    puts("PASS: wrong-group control; actual C logic, mock engine and generated map/masks only; not emulator verification."); return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='union-continue-test-') as tmp:
    cfile = Path(tmp) / 'fixture.c'
    exe = Path(tmp) / 'fixture'
    cfile.write_text(defines + prelude + source + harness)
    subprocess.run(['cc','-std=c11','-Wall','-Werror','-O2',str(cfile),'-o',str(exe)], check=True)
    subprocess.run([str(exe)], cwd=R, check=True)
