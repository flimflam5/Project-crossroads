@ Reference gatehouses; no story/save flags.
Hgss_WestCityGateEnter::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 0
    waitstate
    releaseall
    end

Hgss_WestRouteGateEnter::
    lockall
    warp MAP_ECRUTEAK_CITY_WEST_GATE, 1
    waitstate
    releaseall
    end

Hgss_WestGateGuide::
    msgbox Hgss_WestGateText, MSGBOX_NPC
    end
Hgss_WestGateText:
    .string "West: ROUTE 38.\nEast: ECRUTEAK CITY.$"

Hgss_EastCityGateEnter::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 0
    waitstate
    releaseall
    end

Hgss_EastRouteGateEnter::
    lockall
    warp MAP_ECRUTEAK_CITY_EAST_GATE, 1
    waitstate
    releaseall
    end

Hgss_EastGateGuide::
    msgbox Hgss_EastGateText, MSGBOX_NPC
    end
Hgss_EastGateText:
    .string "West: ECRUTEAK CITY.\nEast: ROUTE 42.$"
