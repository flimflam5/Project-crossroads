@ Reference gatehouses; no story/save flags.
Hgss_WestCityGateEnter0::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 2
    waitstate
    releaseall
    end

Hgss_WestCityGateEnter1::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 0
    waitstate
    releaseall
    end

Hgss_WestCityGateEnter2::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 3
    waitstate
    releaseall
    end

Hgss_WestRouteGateEnter0::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 4
    waitstate
    releaseall
    end

Hgss_WestRouteGateEnter1::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 1
    waitstate
    releaseall
    end

Hgss_WestRouteGateEnter2::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 5
    waitstate
    releaseall
    end

Hgss_WestGateGuide::
    msgbox Hgss_WestGateText, MSGBOX_NPC
    end
Hgss_WestGateText:
    .string "West: ROUTE 38.\nEast: ECRUTEAK CITY.$"

Hgss_EastCityGateEnter0::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 2
    waitstate
    releaseall
    end

Hgss_EastCityGateEnter1::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 0
    waitstate
    releaseall
    end

Hgss_EastCityGateEnter2::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 3
    waitstate
    releaseall
    end

Hgss_EastRouteGateEnter0::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 4
    waitstate
    releaseall
    end

Hgss_EastRouteGateEnter1::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 1
    waitstate
    releaseall
    end

Hgss_EastRouteGateEnter2::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 5
    waitstate
    releaseall
    end

Hgss_EastGateGuide::
    msgbox Hgss_EastGateText, MSGBOX_NPC
    end
Hgss_EastGateText:
    .string "West: ECRUTEAK CITY.\nEast: ROUTE 42.$"
