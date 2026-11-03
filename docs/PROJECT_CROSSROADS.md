# Project Crossroads — Story and Development Bible

Status: preproduction. Engine: rh-hideout/pokeemerald-expansion (GBA). This repository is a fork of the engine.

## Premise
Joseph "Joe" Mercer, 35, is a burned-out Silph Co. logistics middle manager in Saffron City. During a Meridian Syndicate raid to steal an experimental Atlas Drive, Joe is mistaken for an operative. Security sees him carrying the stolen case; Meridian mistakes him for its extraction contact. He becomes a fugitive and gradually embraces the criminal life. The player's choices shape his conscience, loyalty, and notoriety.

## Confirmed game pillars
- Multiple regions, planned in phases: Kanto prologue, Johto, Sinnoh, Unova.
- Curated regional Pokédexes, rather than unrestricted encounters everywhere.
- Selectable Casual, Standard, and Expert difficulties.
- Mega Evolution and a tournament-style endgame, subject to engine integration and testing.
- Joe starts with one of three Pokémon chosen by the player: Porygon, Houndour, or Trubbish.
- Adult corporate satire and a morally complicated crime story.

## Opening mission: Wrong Place, Wrong Time
1. Joe's apartment: alarm, supervisor message, and a rushed commute.
2. Silph Co.: mundane logistics tasks and a meeting.
3. Meridian raid: lockdown and chaos; operative Mara Voss hands Joe the Atlas Drive case.
4. Starter choice: player rescues Porygon, Houndour, or Trubbish; persist the choice.
5. First battle: escape a Silph security officer.
6. Loading dock: Meridian mistakenly extracts Joe.
7. Safehouse: commander Cassian Vale assumes Joe is a professional operative. Joe learns he's wanted.

## Implementation checklist
- [ ] Compile unmodified engine in a cloud Linux development environment.
- [ ] Confirm emulator boots the unmodified build.
- [ ] Define dedicated story flags/variables without colliding with engine constants.
- [ ] Implement a prototype starter-choice event and test each branch.
- [ ] Implement first security battle and healing/recovery logic.
- [ ] Add apartment, office, maintenance corridor, loading dock, safehouse maps.
- [ ] Script and test opening sequence, save/load, and all three starter choices.
- [ ] Implement difficulty selection and persist settings.
- [ ] Expand regional content only after a stable playable vertical slice.

## Technical guardrails
- Do not commit commercial ROM binaries, copyrighted base ROMs, or secrets.
- Source commits alone are not evidence of a playable game. Record compilation and emulator results separately.
- The fork currently contains upstream engine source; this document is design groundwork, not an implemented event script.
