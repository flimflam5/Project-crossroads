#ifndef GUARD_tilesets_H
#define GUARD_tilesets_H

extern const u32 gTilesetTiles_General[];
extern const u16 gTilesetPalettes_General[][16];

extern const struct Tileset *const gTilesetPointer_SecretBase;
extern const struct Tileset *const gTilesetPointer_SecretBaseRedCave;

extern const struct Tileset gTileset_Building;
extern const struct Tileset gTileset_BuildingFrlg;
extern const struct Tileset gTileset_BrendansMaysHouse;
extern const struct Tileset gTileset_GenericBuilding1;
extern const struct Tileset gTileset_General;
extern const struct Tileset gTileset_Petalburg;
extern const struct Tileset gTileset_Rustboro;
extern const struct Tileset gTileset_Fallarbor;
extern const struct Tileset gTileset_Mauville;
extern const struct Tileset gTileset_Slateport;
extern const struct Tileset gTileset_Dewford;
extern const struct Tileset gTileset_Lilycove;
extern const struct Tileset gTileset_Mossdeep;
extern const struct Tileset gTileset_Sootopolis;
extern const struct Tileset gTileset_EverGrande;
extern const struct Tileset gTileset_Pacifidlog;
extern const struct Tileset gTileset_PetalburgGym;
extern const struct Tileset gTileset_PokemonCenter;
extern const struct Tileset gTileset_InsideShip;
extern const struct Tileset gTileset_Fallarbor;
extern const struct Tileset gTileset_Shop;
extern const struct Tileset gTileset_Dewford;
extern const struct Tileset gTileset_BattleFrontier;
extern const struct Tileset gTileset_BattleFrontierOutsideWest;
extern const struct Tileset gTileset_BattleFrontierOutsideEast;
extern const struct Tileset gTileset_BattleArena;
extern const struct Tileset gTileset_BattleDome;
extern const struct Tileset gTileset_BattlePalace;
extern const struct Tileset gTileset_Slateport;
extern const struct Tileset gTileset_Mauville;
extern const struct Tileset gTileset_BattleFrontierOutsideWest;
extern const struct Tileset gTileset_BattleTent;
extern const struct Tileset gTileset_TrainerHill;
extern const struct Tileset gTileset_General_Frlg;
extern const struct Tileset gTileset_PalletTown;
extern const struct Tileset gTileset_ViridianCity;
extern const struct Tileset gTileset_PewterCity;
extern const struct Tileset gTileset_SaffronCity;
extern const struct Tileset gTileset_CeruleanCity;
extern const struct Tileset gTileset_LavenderTown;
extern const struct Tileset gTileset_VermilionCity;
extern const struct Tileset gTileset_CeladonCity;
extern const struct Tileset gTileset_FuchsiaCity;
extern const struct Tileset gTileset_CinnabarIsland;
extern const struct Tileset gTileset_SeviiIslands123;
extern const struct Tileset gTileset_SeviiIslands45;
extern const struct Tileset gTileset_SeviiIslands67;
extern const struct Tileset gTileset_DepartmentStore;
extern const struct Tileset gTileset_PokemonCenterFrlg;
extern const struct Tileset gTileset_SilphCo;
extern const struct Tileset gTileset_SSAnne;
extern const struct Tileset gTileset_SeaCottage;
extern const struct Tileset gTileset_TrainerTower;

extern const struct Tileset gTileset_WesternCity;
extern const struct Tileset gTileset_WesternInteriors;

// BEGIN OWNER EIGHT GYMS INTEGRATION
#if !IS_FRLG
extern const struct Tileset gTileset_BlGymEcruteakPrimary;
extern const struct Tileset gTileset_BlGymEcruteakSecondary;
extern const struct Tileset gTileset_BlGymOlivinePrimary;
extern const struct Tileset gTileset_BlGymOlivineSecondary;
extern const struct Tileset gTileset_BlGymVioletPrimary;
extern const struct Tileset gTileset_BlGymVioletSecondary;
extern const struct Tileset gTileset_BlGymAzaleaPrimary;
extern const struct Tileset gTileset_BlGymAzaleaSecondary;
extern const struct Tileset gTileset_BlGymGoldenrodPrimary;
extern const struct Tileset gTileset_BlGymGoldenrodSecondary;
extern const struct Tileset gTileset_BlGymCianwoodPrimary;
extern const struct Tileset gTileset_BlGymCianwoodSecondary;
extern const struct Tileset gTileset_BlGymMahoganyPrimary;
extern const struct Tileset gTileset_BlGymMahoganySecondary;
extern const struct Tileset gTileset_BlGymBlackthornPrimary;
extern const struct Tileset gTileset_BlGymBlackthornSecondary;
#endif
// END OWNER EIGHT GYMS INTEGRATION
// BEGIN HGSS VIOLET ORIGINAL ART
#if !IS_FRLG
extern const struct Tileset gTileset_HgssVioletPrimary;
extern const struct Tileset gTileset_HgssVioletSecondary;
extern const struct Tileset gTileset_HgssVioletRoutePrimary;
#endif
// END HGSS VIOLET ORIGINAL ART
// BEGIN ECRUTEAK NEUTRAL BUFFER
#if !IS_FRLG
extern const struct Tileset gTileset_HgssEcruteakBuffer;
#endif
// END ECRUTEAK NEUTRAL BUFFER
// BEGIN ECRUTEAK GATE BUFFER
#if !IS_FRLG
extern const struct Tileset gTileset_HgssEcruteakGateBuffer;
#endif
// END ECRUTEAK GATE BUFFER



// BEGIN OLIVINE LANDMARK INTERIORS
#if !IS_FRLG
extern const struct Tileset gTileset_HgssOlivineLandmarks;
extern const struct Tileset gTileset_HgssOlivineLandmarkIndoor;
extern const struct Tileset gTileset_HgssOlivineLandmarkOutdoor;
#endif
// END OLIVINE LANDMARK INTERIORS

// BEGIN HGSS OLIVINE EXTERIORS
#if !IS_FRLG
extern const struct Tileset gTileset_HgssOlivinePrimary;
extern const struct Tileset gTileset_HgssOlivineSecondary;
#endif
// END HGSS OLIVINE EXTERIORS
// BEGIN HGSS OLIVINE ROOMS
#if !IS_FRLG
extern const struct Tileset gTileset_HgssOlivineHome;
extern const struct Tileset gTileset_HgssOlivineGym;
#endif
// END HGSS OLIVINE ROOMS
#endif //GUARD_tilesets_H
