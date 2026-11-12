JohtoRoute38_MapScripts::
    map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Qa10_JohtoRoute38_ArrivalFacing_Table
    map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, Qa10_JohtoRoute38_ArrivalFacing
    .byte 0

@ BEGIN QA10 COORDINATE-SCOPED ARRIVAL FACING
Qa10_JohtoRoute38_ArrivalFacing_Table:
    map_script_2 VAR_TEMP_0, VAR_TEMP_0, Qa10_JohtoRoute38_ArrivalFacing
    .2byte 0

Qa10_JohtoRoute38_ArrivalFacing::
    getplayerxy VAR_0x8004, VAR_0x8005
    goto_if_eq VAR_0x8004, 62, Qa10_JohtoRoute38_ArrivalFacing_X62
    end

Qa10_JohtoRoute38_ArrivalFacing_X62:
    goto_if_eq VAR_0x8005, 12, Qa10_JohtoRoute38_ArrivalFacing_DIR_WEST
    goto_if_eq VAR_0x8005, 13, Qa10_JohtoRoute38_ArrivalFacing_DIR_WEST
    goto_if_eq VAR_0x8005, 14, Qa10_JohtoRoute38_ArrivalFacing_DIR_WEST
    end

Qa10_JohtoRoute38_ArrivalFacing_DIR_WEST:
    turnobject LOCALID_PLAYER, DIR_WEST
    end
@ END QA10 COORDINATE-SCOPED ARRIVAL FACING
