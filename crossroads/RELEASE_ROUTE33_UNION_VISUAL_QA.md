# Pokémon: Black Ledger — Route 33 / Union Cave visual QA

This is a focused QA checkpoint. It fixes the sampled Route 33 transition where Joe disappeared behind the Azalea road and fills photographed black gaps in Union Cave's rock shelves. The cave's exterior black space remains. Four cave arrows observed in the owner screenshots are the engine's directional cues at functioning exit thresholds. The Olivine port screenshot shows the established north-facing terminal entrance; its roof-heavy perspective remains available for visual review.

Game source: `04f88ee948c26c8da06d239b8203453147c171d1`  
ROM SHA-256: `07f2a10ca19e3eb585c1114ce656caa2475f4de487a4d416dc5bef461a2627a5`  
Matching ELF SHA-256: `ce32b5ba4d016bbb62054c4f97ac40630d461f58a693b4ae96f168eb7c6de92f`

The owner has not accepted the visuals. This is not a completed Johto release. The enlarged Ruins hall and four hidden rooms remain outside this build; the wider Johto reconstruction and unsampled visual/collision cases remain unfinished.

## Delta QA

Back up your battery save, import the `.gba` from this ZIP, and use normal Continue instead of an old save state. Walk both ways around the Azalea–Route 33 crossing and the rock, including along the road's ends. Check Joe remains visible and can move normally. Explore Union Cave's shelf edges and ladder pockets, check that floors and walls look coherent, and enter and leave its exits in both directions. Walk into water where Surf is available, save normally, close and Continue. Inspect the Olivine port entrance if its roof perspective was a concern. Report any visual, movement or save problems with their location.

## What was tested

Scripted emulator controller tests on the exact candidate included 15 reciprocal cave/Ruins warp pairs, 12 sampled cave collision approaches, both implemented puzzles' cancel and solve, Surf Save/cold Continue and dry Route 33–32 travel. Twelve copied older QA10 save fixtures from one profile passed the sampled compatibility checks. The Route 33 visibility sample changed from 0/187 unobscured player pixels before the fix to 187/187 after it at the reproduced location. Three cave viewpoints were checked after the shelf repair; four exit arrows were verified as cues at real exit thresholds. These checks sample the game, not every boundary or save.

Title, the three starter selections and duplication checks, Fly, field actions and a practice-battle loss/healing check passed scripted regression. Tests used disclosed Survey access and temporary QA gear; the starter test skipped the opening using a RAM fixture. Separately, the Olivine terminal's two north doorway leaves were tested on the earlier `a320` baseline, not this candidate: ten approaches passed and two lateral starts were unavailable on dry land. No private batteries, emulator snapshots, ROMs or memory dumps are in the evidence ZIP.
