EcruteakCity_BarrierCorridor_MapScripts::
    map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing_Table
    map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing
    .byte 0

@ BEGIN QA10 COORDINATE-SCOPED ARRIVAL FACING
Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing_Table:
    map_script_2 VAR_TEMP_0, VAR_TEMP_0, Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing
    .2byte 0

Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing::
    getplayerxy VAR_0x8004, VAR_0x8005
    goto_if_eq VAR_0x8004, 6, Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing_X6
    end

Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing_X6:
    goto_if_eq VAR_0x8005, 3, Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing_DIR_SOUTH
    end

Qa10_EcruteakCity_BarrierCorridor_ArrivalFacing_DIR_SOUTH:
    turnobject LOCALID_PLAYER, DIR_SOUTH
    end
@ END QA10 COORDINATE-SCOPED ARRIVAL FACING
