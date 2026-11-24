#include <assert.h>
#include "trigger.h"

int main(void)
{
    const unsigned stone = 42, other = 43, southwest = 71, elsewhere = 72;
    const unsigned north = 1, south = 2, hoOh = 250, otherSpecies = 251;
    assert(AlphIsWaterStoneTrigger(stone, stone, southwest, southwest, 5, 2, north, north));
    assert(!AlphIsWaterStoneTrigger(other, stone, southwest, southwest, 5, 2, north, north));
    assert(!AlphIsWaterStoneTrigger(stone, stone, elsewhere, southwest, 5, 2, north, north));
    assert(!AlphIsWaterStoneTrigger(stone, stone, southwest, southwest, 4, 2, north, north));
    assert(!AlphIsWaterStoneTrigger(stone, stone, southwest, southwest, 6, 2, north, north));
    assert(!AlphIsWaterStoneTrigger(stone, stone, southwest, southwest, 5, 1, north, north));
    assert(!AlphIsWaterStoneTrigger(stone, stone, southwest, southwest, 5, 3, north, north));
    assert(!AlphIsWaterStoneTrigger(stone, stone, southwest, southwest, 5, 2, south, north));
    assert(AlphIsQualifyingHoOh(hoOh, hoOh, 0));
    assert(!AlphIsQualifyingHoOh(hoOh, hoOh, 1));
    assert(!AlphIsQualifyingHoOh(otherSpecies, hoOh, 0));
    return 0;
}
