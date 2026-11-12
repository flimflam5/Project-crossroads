JohtoRoute42_MapScripts::
    map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Qa10_JohtoRoute42_ArrivalFacing_Table
    map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, Qa10_JohtoRoute42_ArrivalFacing
    .byte 0

@ BEGIN QA10 COORDINATE-SCOPED ARRIVAL FACING
Qa10_JohtoRoute42_ArrivalFacing_Table:
    map_script_2 VAR_TEMP_0, VAR_TEMP_0, Qa10_JohtoRoute42_ArrivalFacing
    .2byte 0

Qa10_JohtoRoute42_ArrivalFacing::
    getplayerxy VAR_0x8004, VAR_0x8005
    goto_if_eq VAR_0x8004, 3, Qa10_JohtoRoute42_ArrivalFacing_X3
    end

Qa10_JohtoRoute42_ArrivalFacing_X3:
    goto_if_eq VAR_0x8005, 13, Qa10_JohtoRoute42_ArrivalFacing_DIR_EAST
    goto_if_eq VAR_0x8005, 14, Qa10_JohtoRoute42_ArrivalFacing_DIR_EAST
    goto_if_eq VAR_0x8005, 15, Qa10_JohtoRoute42_ArrivalFacing_DIR_EAST
    end

Qa10_JohtoRoute42_ArrivalFacing_DIR_EAST:
    turnobject LOCALID_PLAYER, DIR_EAST
    end
@ END QA10 COORDINATE-SCOPED ARRIVAL FACING
