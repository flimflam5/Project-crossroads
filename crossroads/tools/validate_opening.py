#!/usr/bin/env python3
"""Validate Project Crossroads narrative data; does not build a GBA ROM."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
story = json.loads((root / "story" / "opening.json").read_text())
expected = {"PORYGON", "HOUNDOUR", "TRUBBISH"}
actual = {choice["species"] for choice in story["starter_choices"]}
assert actual == expected, (actual, expected)
ids = [scene["id"] for scene in story["scenes"]]
assert len(ids) == len(set(ids)), "Duplicate scene ID"
assert ids == ["apartment", "office", "heist", "starter", "security", "extraction", "safehouse"]
assert next(s for s in story["scenes"] if s["id"] == "starter")["action"] == "choose_starter"
assert next(s for s in story["scenes"] if s["id"] == "security")["action"] == "trainer_battle"
assert len(set(story["progression_flags"])) == len(story["progression_flags"])
print("Project Crossroads opening narrative validation: PASS")
