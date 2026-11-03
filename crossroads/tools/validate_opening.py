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
expected = {"PORYGON", "HOUNDOUR", "TRUBBISH"}
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
for species, value in (("PORYGON", 1), ("HOUNDOUR", 2), ("TRUBBISH", 3)):
    block = script.split(f"Crossroads_EventScript_{species.title()}::", 1)[1]
    block = block.split("Crossroads_EventScript_", 1)[0]
    assert f"givepokemon SPECIES_{species}, 5, ITEM_NONE" in block
    assert f"setvar VAR_CROSSROADS_STARTER, {value}" in block
assert "goto_if_ne VAR_CROSSROADS_STARTER, 0" in script
assert "MULTI_CHOICE_CROSSROADS_STARTERS" not in script
print("Project Crossroads narrative and staged script checks: PASS")
