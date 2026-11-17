#!/usr/bin/env python3
"""Execute the real Continue C against exhaustive Route 33 fixtures on a host.

The engine interfaces are minimal mocks; this checks location policy and save
preservation, not real object spawn, movement, rendering or emulator behavior.
"""
from pathlib import Path
import subprocess, tempfile
R = Path(__file__).resolve().parents[2]
STUB = r'''
#ifndef TEST_GLOBAL_H
#define TEST_GLOBAL_H
#include <stdint.h>
#include <string.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int16_t s16; typedef int32_t s32; typedef int bool32; typedef int bool8;
#define TRUE 1
#define FALSE 0
#define MAPGRID_COLLISION_MASK 0x0c00
#define MAPGRID_METATILE_ID_MASK 0x03ff
#define MAP_OFFSET 7
#define OBJECT_EVENTS_COUNT 16
#define WARP_ID_NONE -1
#define PLAYER_AVATAR_STATE_NORMAL 0
#define OBJ_EVENT_GFX_JOE_SURFING 0x3f06
#define OBJ_EVENT_GFX_BRENDAN_SURFING 0x11
#define OBJ_EVENT_GFX_MAY_SURFING 0x12
#define MAP_JOHTO_ROUTE33 ((75 << 8) | 83)
#define MAP_AZALEA_TOWN ((75 << 8) | 64)
#define MAP_ECRUTEAK_CITY ((75 << 8) | 10)
#define MAP_VIOLET_CITY ((75 << 8) | 43)
#define MAP_OLIVINE_CITY ((75 << 8) | 0)
#define MAP_GROUP(x) ((x) >> 8)
#define MAP_NUM(x) ((x) & 255)
#define HEAL_LOCATION_OLIVINE_CITY 1
#define HEAL_LOCATION_ECRUTEAK_CITY 2
#define HEAL_LOCATION_VIOLET_CITY 3
#define AZALEA_KILN_ORIGIN_X 19
#define AZALEA_KILN_ORIGIN_Y 30
#define AZALEA_KILN_WIDTH 4
#define AZALEA_KILN_HEIGHT 4
#define METATILE_ATTRIBUTE_BEHAVIOR 0
struct Coord { s16 x,y; };
struct WarpData { s16 mapGroup,mapNum,warpId,x,y; };
struct ObjectEvent { u16 graphicsId; u8 spriteId,isPlayer; struct Coord initialCoords,currentCoords,previousCoords; };
struct MapLayout { s32 width,height; const u16 *map; bool8 isFrlg; };
struct WarpEvent { s16 x,y; };
struct ObjectEventTemplate { s16 x,y; };
struct MapEvents { u32 warpCount,objectEventCount; const struct WarpEvent *warps; const struct ObjectEventTemplate *objectEvents; };
struct MapHeader { const struct MapLayout *mapLayout; const struct MapEvents *events; u16 mapLayoutId; };
struct SaveBlock1 { struct WarpData location,lastHealLocation; struct Coord pos; u16 mapLayoutId; u16 mapView[256]; struct ObjectEvent objectEvents[OBJECT_EVENTS_COUNT]; u32 partyMarker,bagMarker,flagsMarker; };
struct SaveBlock2 { u8 playerGender; };
extern struct SaveBlock1 *gSaveBlock1Ptr; extern struct SaveBlock2 *gSaveBlock2Ptr;
extern struct MapHeader gMapHeader; extern struct ObjectEvent gObjectEvents[OBJECT_EVENTS_COUNT];
bool32 Johto_IsExplorationGroup(int); void SetLastHealLocationWarp(int); void SetCurrentMapLayout(int);
u16 GetPlayerAvatarGraphicsIdByStateIdAndGender(int,int);
u32 GetAttributeByMetatileIdAndMapLayout(u16,u8,bool32); bool8 MetatileBehavior_IsSurfableWaterOrUnderwater(u8);
#define CpuFill16(v,p,n) memset((p),(v),(n))
#endif
'''
TEST = r'''
#include "global.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "actual_continue.c"
static struct SaveBlock1 save1; static struct SaveBlock2 save2;
struct SaveBlock1 *gSaveBlock1Ptr=&save1; struct SaveBlock2 *gSaveBlock2Ptr=&save2;
struct MapHeader gMapHeader; struct ObjectEvent gObjectEvents[OBJECT_EVENTS_COUNT];
static u16 blocks[1024], old[768], attributes[1024];
static struct MapLayout layout={32,32,blocks,0};
static struct WarpEvent warps[]={{19,13}};
static struct ObjectEventTemplate objects[]={{21,25},{10,19},{23,26},{24,26}};
static struct MapEvents events={1,4,warps,objects};
bool32 Johto_IsExplorationGroup(int x){return x==75;}
void SetLastHealLocationWarp(int x){(void)x;} void SetCurrentMapLayout(int x){save1.mapLayoutId=x;}
u16 GetPlayerAvatarGraphicsIdByStateIdAndGender(int x,int y){(void)x;(void)y;return 73;}
u32 GetAttributeByMetatileIdAndMapLayout(u16 id,u8 type,bool32 frlg){assert(!type && !frlg);return attributes[id]&255;}
bool8 MetatileBehavior_IsSurfableWaterOrUnderwater(u8 b){return b==0x10 || b==0x11 || b==0x12 || b==0x13 || b==0x14 || b==0x15;}
static void load(const char *path,u16 *dst,size_t count){FILE *f=fopen(path,"rb");assert(f);assert(fread(dst,2,count,f)==count);assert(fgetc(f)==EOF);fclose(f);}
static int object(int x,int y){unsigned i;for(i=0;i<events.objectEventCount;i++)if(objects[i].x==x && objects[i].y==y)return 1;return 0;}
static int valid(int x,int y){return x>=0 && x<32 && y>=0 && y<32 && !(blocks[y*32+x]&0xc00) && blocks[y*32+x]>>12==3 && !(x==19&&y==13) && !object(x,y);}
static void reset(int x,int y,int surf){memset(&save1,0,sizeof(save1));memset(gObjectEvents,0,sizeof(gObjectEvents));save1.location.mapGroup=75;save1.location.mapNum=83;save1.lastHealLocation.mapGroup=2;save1.pos=(struct Coord){x,y};save1.mapLayoutId=44;gMapHeader=(struct MapHeader){&layout,&events,44};save1.partyMarker=0x10293847;save1.bagMarker=0xabcddcba;save1.flagsMarker=0x13579bdf;save1.objectEvents[0].isPlayer=1;save1.objectEvents[0].spriteId=127;save1.objectEvents[0].graphicsId=surf?((OBJ_EVENT_GFX_JOE_SURFING>>8)|(OBJ_EVENT_GFX_JOE_SURFING<<8)):0;gObjectEvents[0].isPlayer=1;gObjectEvents[0].initialCoords=gObjectEvents[0].currentCoords=gObjectEvents[0].previousCoords=(struct Coord){x+7,y+7};save1.objectEvents[0].initialCoords=save1.objectEvents[0].currentCoords=save1.objectEvents[0].previousCoords=(struct Coord){x+7,y+7};}
static void invariant(void){assert(save1.partyMarker==0x10293847 && save1.bagMarker==0xabcddcba && save1.flagsMarker==0x13579bdf);}
static void player_coords_match(void){struct ObjectEvent a=gObjectEvents[0], b=save1.objectEvents[0];struct Coord p={save1.pos.x+7,save1.pos.y+7};assert(a.initialCoords.x==p.x&&a.initialCoords.y==p.y&&a.currentCoords.x==p.x&&a.currentCoords.y==p.y&&a.previousCoords.x==p.x&&a.previousCoords.y==p.y);assert(b.initialCoords.x==p.x&&b.initialCoords.y==p.y&&b.currentCoords.x==p.x&&b.currentCoords.y==p.y&&b.previousCoords.x==p.x&&b.previousCoords.y==p.y);}
int main(int argc,char **argv){int x,y,count=0,stayed=0,moved=0,non3=0,warp=0;u16 original; assert(argc==5);load(argv[1],blocks,1024);load(argv[2],old,768);load(argv[3],attributes,512);load(argv[4],attributes+512,512);
 for(y=0;y<24;y++)for(x=0;x<32;x++){
  u16 prior=old[y*32+x], next=blocks[y*32+x];int keep,dist,best=9999,xx,yy;
  if((prior&0xc00)||((prior>>12)!=0&&(prior>>12)!=3))continue;
  count++;
  keep=!(next&0xc00) && !object(x,y) && next>>12==3 && !(x==19&&y==13);
  if(!(next&0xc00) && next>>12!=3)non3++;
  if(x==19&&y==13)warp++;
  reset(x,y,0);assert(Crossroads_PrepareContinue());invariant();player_coords_match();
  if(keep){assert(save1.pos.x==x&&save1.pos.y==y);stayed++;}
  else{assert(valid(save1.pos.x,save1.pos.y));dist=abs(save1.pos.x-x)+abs(save1.pos.y-y);for(yy=0;yy<32;yy++)for(xx=0;xx<32;xx++)if(valid(xx,yy)&&abs(xx-x)+abs(yy-y)<best)best=abs(xx-x)+abs(yy-y);assert(dist==best);moved++;}
 }
 assert(count==530 && non3==10 && warp==1 && moved==344 && stayed==186);
 /* The active threshold is repaired even if a prior walking save landed here. */
 reset(19,13,0);assert(Crossroads_PrepareContinue());assert(valid(save1.pos.x,save1.pos.y));assert(save1.pos.x!=19||save1.pos.y!=13);invariant();
 /* Synthetic ocean fixture checks behavior lookup and preserves a real Surf state. */
 original=blocks[31*32+31];blocks[31*32+31]=0x1000|536;assert((attributes[536]&255)==0x15);
 reset(31,31,1);assert(Crossroads_PrepareContinue());assert(save1.pos.x==31&&save1.pos.y==31);invariant();
 reset(31,31,0);assert(Crossroads_PrepareContinue());assert(valid(save1.pos.x,save1.pos.y));invariant();
 /* A Surf sprite on non-surfable elevation-1 data must not be stranded. */
 blocks[31*32+31]=0x1000|1;assert((attributes[1]&255)!=0x15);
 reset(31,31,1);assert(Crossroads_PrepareContinue());assert(valid(save1.pos.x,save1.pos.y));invariant();player_coords_match();assert(gObjectEvents[0].graphicsId==73 && save1.objectEvents[0].graphicsId==(73<<8) && save1.objectEvents[0].spriteId==127);blocks[31*32+31]=original;
 /* No Route 33 migration guard applies to the old 24-row layout or another map. */
 layout.height=24;reset(25,18,0);assert(Crossroads_PrepareContinue());assert(save1.pos.x==25&&save1.pos.y==18);layout.height=32;
 reset(25,18,0);save1.location.mapNum=84;assert(Crossroads_PrepareContinue());assert(save1.pos.x==25&&save1.pos.y==18);
 puts("PASS actual Continue C: 530 old positions (186 kept, 344 relocated), 10 cliff/sea cells, cave warp, synthetic Surf/walking water, non-surfable water, and other-map/old-layout controls. Host mocks only; emulator and visual tests pending.");return 0;}
'''
with tempfile.TemporaryDirectory(prefix='route33-continue-host-') as td:
    d = Path(td); (d/'global.h').write_text(STUB)
    for p in ['johto_exploration.h','crossroads_continue.h','event_object_movement.h','field_player_avatar.h','fieldmap.h','metatile_behavior.h','overworld.h','constants/maps.h','constants/event_objects.h','constants/heal_locations.h','constants/azalea_kiln_door.h']:
        f=d/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('#include "global.h"\n')
    (d/'actual_continue.c').write_bytes((R/'src/crossroads_continue.c').read_bytes()); (d/'test.c').write_text(TEST)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-I',str(d),str(d/'test.c'),'-o',str(d/'test')],check=True)
    subprocess.run([str(d/'test'),str(R/'data/layouts/JohtoRoute33/map.bin'),str(R/'crossroads/donor/hns-route33/data/layouts/Route33_hns/black-ledger-baseline.bin'),str(R/'data/tilesets/primary/bl_gym_azalea/metatile_attributes.bin'),str(R/'data/tilesets/secondary/hns_route33/metatile_attributes.bin')],check=True)
