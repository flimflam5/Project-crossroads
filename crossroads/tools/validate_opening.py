#!/usr/bin/env python3
"""Static checks for Project Crossroads story and staged starter script.

These tests are NOT a substitute for compiling or playing the ROM.
"""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
crossroads = root / "crossroads"
story = json.loads((crossroads / "story" / "opening.json").read_text())
expected = {"ELGYEM", "SEEDOT", "TRUBBISH"}
actual = {choice["species"] for choice in story["starter_choices"]}
assert actual == expected, (actual, expected)

ids = [scene["id"] for scene in story["scenes"]]
assert len(ids) == len(set(ids)), "Duplicate scene ID"
assert ids == [
    "apartment", "office", "heist", "starter",
    "security", "extraction", "safehouse",
]
assert next(s for s in story["scenes"] if s["id"] == "starter")["action"] == "choose_starter"
assert next(s for s in story["scenes"] if s["id"] == "security")["action"] == "trainer_battle"
assert len(set(story["progression_flags"])) == len(story["progression_flags"])

vars_header = (root / "include/constants/vars.h").read_text()
assert re.search(r"^#define\s+VAR_CROSSROADS_STARTER\s+0x40FA\b", vars_header, re.M)
assert "VAR_UNUSED_0x40FA" not in vars_header

script = (crossroads / "scripts/prologue.inc").read_text()
for species, value in (("ELGYEM", 1), ("SEEDOT", 2), ("TRUBBISH", 3)):
    block = script.split(f"Crossroads_EventScript_{species.title()}::", 1)[1]
    block = re.split(r"(?m)^Crossroads_EventScript_[A-Za-z0-9_]+::", block, maxsplit=1)[0]
    assert f"givemon SPECIES_{species}, 5, ITEM_NONE" in block
    assert "goto_if_eq VAR_RESULT, MON_CANT_GIVE, Crossroads_EventScript_NoRoom" in block
    assert f"setvar VAR_CROSSROADS_STARTER, {value}" in block
assert "goto_if_ne VAR_CROSSROADS_STARTER, 0" in script
assert "MULTI_CHOICE_CROSSROADS_STARTERS" not in script
print("Project Crossroads narrative and staged script checks: PASS")

# The staged copy alone does not prove that the ROM uses a safe starter event.
live = (crossroads / 'scripts/starter_rescue.inc').read_text()
live = live.split('Crossroads_EventScript_ChooseStarter::', 1)[1]
assert 'goto_if_ne VAR_CROSSROADS_STARTER, 0, Crossroads_EventScript_AlreadyChosen' in live
assert len(re.findall(r'^    givemon ', live, re.M)) == 3
for species, value in (("ELGYEM", 1), ("SEEDOT", 2), ("TRUBBISH", 3)):
    block = live.split(f'Crossroads_EventScript_{species.title()}::', 1)[1]
    block = re.split(r'(?m)^Crossroads_EventScript_[A-Za-z0-9_]+::', block, maxsplit=1)[0]
    grant = block.index(f'givemon SPECIES_{species}, 5, ITEM_NONE')
    failed = block.index('goto_if_eq VAR_RESULT, MON_CANT_GIVE, Crossroads_EventScript_NoRoom')
    persist = block.index(f'setvar VAR_CROSSROADS_STARTER, {value}')
    assert grant < failed < persist
assert 'crossroads/scripts/starter_rescue.inc' in (root / 'data/event_scripts.s').read_text()
print('Linked starter rescue, duplication guard and success-only persistence: PASS')

# A grant must run on the real Olivine acquisition map, not the legacy bedroom.
links = []
for path in (root / 'data/maps').glob('*/map.json'):
    m = json.loads(path.read_text())
    for event in (m.get('object_events') or []) + (m.get('bg_events') or []) + (m.get('coord_events') or []):
        if event.get('script') == 'Crossroads_EventScript_ChooseStarter':
            links.append((m['id'], m['region_map_section']))
assert links == [('MAP_OLIVINE_CITY_SILPH_OFFICE', 'MAPSEC_OLIVINE_CITY')], links
legacy = json.loads((root / 'data/maps/LittlerootTown_BrendansHouse_2F/map.json').read_text())
assert any(e.get('script') == 'Crossroads_EventScript_VisitRescueCase' for e in legacy['bg_events'])
print('Only live starter grant is in Olivine; legacy room is a travel bridge: PASS')
