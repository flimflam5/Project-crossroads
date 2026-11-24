#!/usr/bin/env python3
"""Compile the actual Alph and item-use C function bodies against host mocks.

This checks dispatch and party predicates, not compiled ROM behavior, bag UI,
field rendering, real save files or emulator play.
"""
import re
import subprocess
import tempfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]


def function(source, name):
    match = re.search(r'(?m)^(?:static\s+)?(?:void|bool32|u16)\s+'
                      + re.escape(name) + r'\([^;]*?\)\s*\{', source)
    assert match, name
    start, pos = match.start(), match.end()
    depth = 1
    while depth:
        char = source[pos]
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
        pos += 1
    return source[start:pos]


alph = (R / 'src/crossroads_alph.c').read_text()
item = (R / 'src/item_use.c').read_text()
source = '\n'.join(function(alph, n) for n in (
    'Crossroads_AlphShouldUseWaterStone', 'Crossroads_AlphHasNonEggHoOh'))
source += '\n' + '\n'.join(function(item, n) for n in (
    'ItemUseOnFieldCB_AlphWaterStone', 'ItemUseOutOfBattle_EvolutionStone'))
assert 'RemoveBagItem' not in source and 'FlagSet' not in source
assert (R / 'data/specials.inc').read_text().count('def_special Crossroads_AlphHasNonEggHoOh') == 1

prelude = r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32;
typedef int16_t s16; typedef int bool32;
#define IS_FRLG 0
#define TRUE 1
#define FALSE 0
#define MAP_OFFSET 7
#define ITEM_WATER_STONE 42
#define MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER 0x4c03
#define MAP_GROUP(v) ((v)>>8)
#define MAP_NUM(v) ((v)&255)
#define DIR_NORTH 2
#define B_TRAINER_PLAYER 0
#define MON_DATA_IS_EGG 1
#define MON_DATA_SPECIES 2
#define SPECIES_HO_OH 250
#define PYRAMID_LOCATION_NONE 0
#define ITEMMENULOCATION_FIELD 0
#define tUsingRegisteredKeyItem data[3]
struct Loc { u8 mapGroup, mapNum; };
struct Save { struct Loc location; } save;
struct Save *gSaveBlock1Ptr=&save;
struct Pokemon { u16 species; u8 egg, fainted; };
struct Pokemon gParties[1][6];
static int partyCount;
static u8 CalculatePlayerPartyCount(void) { return partyCount; }
static u32 GetMonData(struct Pokemon *m,int field) { return field==MON_DATA_IS_EGG ? m->egg : m->species; }
static u16 gSpecialVar_ItemId;
static s16 xPos,yPos; static int facing;
static void PlayerGetDestCoords(s16 *x,s16 *y) { *x=xPos; *y=yPos; }
static int GetPlayerFacingDirection(void) { return facing; }
struct Task { int data[16]; } gTasks[4];
static struct BagMenu { void (*newScreenCallback)(void); } bag;
static struct BagMenu *gBagMenu=&bag;
static struct { int location; } gBagPosition;
static void (*gFieldCallback)(void), (*gItemUseCB)(void), (*sItemUseOnFieldCB)(u8);
static int pyramid, closed, fallback, destroyed, bagCount;
static const u8 RuinsOfAlph_SouthwestChamber_WaterStoneUsed[]={0};
static const u8 *script;
static int CurrentBattlePyramidLocation(void) {return pyramid;}
static void ScriptContext_SetupScript(const u8 *s) {script=s;}
static void DestroyTask(u8 id) {(void)id; destroyed++;}
static void FieldCB_UseItemOnField(void) {}
static void CB2_ReturnToField(void) {}
static void ItemUseCB_EvolutionStone(void) {}
static void Task_FadeAndCloseBagMenu(u8 id) {(void)id; closed++;}
static void SetUpItemUseCallback(u8 id) {(void)id; fallback++;}
'''

harness = r'''
static void reset(void) {
    memset(&save,0,sizeof(save)); memset(gTasks,0,sizeof(gTasks)); memset(&bag,0,sizeof(bag));
    gSpecialVar_ItemId=ITEM_WATER_STONE;
    save.location.mapGroup=MAP_GROUP(MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER);
    save.location.mapNum=MAP_NUM(MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER);
    xPos=5+MAP_OFFSET; yPos=2+MAP_OFFSET; facing=DIR_NORTH;
    gBagPosition.location=ITEMMENULOCATION_FIELD; pyramid=0;
    gFieldCallback=NULL; gItemUseCB=NULL; sItemUseOnFieldCB=NULL;
    script=NULL; closed=fallback=destroyed=0; bagCount=4;
}
static void assertFallback(void) {
    ItemUseOutOfBattle_EvolutionStone(0);
    assert(fallback==1 && closed==0 && sItemUseOnFieldCB==NULL);
    assert(gItemUseCB==ItemUseCB_EvolutionStone && gFieldCallback==NULL && bagCount==4);
}
int main(void) {
    reset(); assert(Crossroads_AlphShouldUseWaterStone());
    ItemUseOutOfBattle_EvolutionStone(0);
    assert(closed==1 && fallback==0 && bagCount==4);
    assert(gFieldCallback==FieldCB_UseItemOnField && bag.newScreenCallback==CB2_ReturnToField);
    assert(sItemUseOnFieldCB!=NULL && script==NULL);
    sItemUseOnFieldCB(0);
    assert(script==RuinsOfAlph_SouthwestChamber_WaterStoneUsed && destroyed==1 && bagCount==4);
    reset(); gSpecialVar_ItemId++; assertFallback();
    reset(); save.location.mapGroup++; assertFallback();
    reset(); save.location.mapNum++; assertFallback();
    reset(); xPos--; assertFallback();
    reset(); xPos++; assertFallback();
    reset(); yPos--; assertFallback();
    reset(); yPos++; assertFallback();
    reset(); facing++; assertFallback();
    reset(); gBagPosition.location=1; assertFallback();
    reset(); pyramid=1; assertFallback();
    reset(); gTasks[0].tUsingRegisteredKeyItem=1; assertFallback();
    memset(gParties,0,sizeof(gParties)); partyCount=0; assert(!Crossroads_AlphHasNonEggHoOh());
    partyCount=2; gParties[0][0]=(struct Pokemon){250,1,0}; gParties[0][1]=(struct Pokemon){251,0,0};
    assert(!Crossroads_AlphHasNonEggHoOh());
    gParties[0][1]=(struct Pokemon){250,0,1}; assert(Crossroads_AlphHasNonEggHoOh());
    partyCount=1; assert(!Crossroads_AlphHasNonEggHoOh());
    puts("PASS actual C: field-item dispatch and 11 fallback contexts, no mock bag-count change; non-egg player-party check including fainted Ho-Oh. Host mocks only.");
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='alph-trigger-') as tmp:
    c = Path(tmp) / 'test.c'
    exe = Path(tmp) / 'test'
    c.write_text(prelude + '\n' + source + '\n' + harness)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(c), '-o', str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
