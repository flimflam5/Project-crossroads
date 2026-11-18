#ifndef CROSSROADS_RUINS_HIDDEN_TRIGGER_PROTOTYPE_H
#define CROSSROADS_RUINS_HIDDEN_TRIGGER_PROTOTYPE_H

/* Unlinked prototype. Coordinates are local to the existing 10x11 donor crop.
 * The caller must read the actual active map, player position/facing and bag
 * item at the field-item-use boundary. It must not consume the Water Stone. */
static int AlphIsWaterStoneTrigger(unsigned item, unsigned waterStone,
                                   unsigned map, unsigned southwestChamber,
                                   int x, int y, unsigned facing, unsigned north)
{
    return item == waterStone && map == southwestChamber
        && x == 5 && y == 2 && facing == north;
}

/* HGSS accepts a fainted Ho-Oh, but excludes eggs and checks the party only.
 * Call for every occupied party slot, never the PC or a Pokédex flag. */
static int AlphIsQualifyingHoOh(unsigned species, unsigned hoOh, int isEgg)
{
    return !isEgg && species == hoOh;
}

#endif
