EcruteakCity_MapScripts::
    map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Qa10_EcruteakCity_ArrivalFacing_Table
    map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, Qa10_EcruteakCity_ArrivalFacing
    .byte 0

@ BEGIN QA10 COORDINATE-SCOPED ARRIVAL FACING
Qa10_EcruteakCity_ArrivalFacing_Table:
    map_script_2 VAR_TEMP_0, VAR_TEMP_0, Qa10_EcruteakCity_ArrivalFacing
    .2byte 0

Qa10_EcruteakCity_ArrivalFacing::
    getplayerxy VAR_0x8004, VAR_0x8005
    goto_if_eq VAR_0x8004, 7, Qa10_EcruteakCity_ArrivalFacing_X7
    goto_if_eq VAR_0x8004, 59, Qa10_EcruteakCity_ArrivalFacing_X59
    end

Qa10_EcruteakCity_ArrivalFacing_X7:
    goto_if_eq VAR_0x8005, 37, Qa10_EcruteakCity_ArrivalFacing_DIR_EAST
    goto_if_eq VAR_0x8005, 38, Qa10_EcruteakCity_ArrivalFacing_DIR_EAST
    goto_if_eq VAR_0x8005, 39, Qa10_EcruteakCity_ArrivalFacing_DIR_EAST
    end

Qa10_EcruteakCity_ArrivalFacing_X59:
    goto_if_eq VAR_0x8005, 46, Qa10_EcruteakCity_ArrivalFacing_DIR_WEST
    goto_if_eq VAR_0x8005, 47, Qa10_EcruteakCity_ArrivalFacing_DIR_WEST
    goto_if_eq VAR_0x8005, 48, Qa10_EcruteakCity_ArrivalFacing_DIR_WEST
    end

Qa10_EcruteakCity_ArrivalFacing_DIR_EAST:
    turnobject LOCALID_PLAYER, DIR_EAST
    end

Qa10_EcruteakCity_ArrivalFacing_DIR_WEST:
    turnobject LOCALID_PLAYER, DIR_WEST
    end
@ END QA10 COORDINATE-SCOPED ARRIVAL FACING
