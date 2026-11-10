#ifndef GUARD_JOHTO_EXPLORATION_H
#define GUARD_JOHTO_EXPLORATION_H
// Appended only; WarpData mapGroup/mapNum are signed bytes.
#define JOHTO_EXTRA_MAP_GROUP 76
bool32 Johto_IsExplorationGroup(u8 group);
bool32 Johto_CanTestSurf(void);
void Johto_ToggleTestAccess(void);
void Johto_EnableTestAccess(void);
#endif
