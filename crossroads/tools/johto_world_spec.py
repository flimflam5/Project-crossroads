"""Authored Johto geography and scope; never an encounter/story roster."""
GYM_CITIES={'VioletCity','AzaleaTown','GoldenrodCity','CianwoodCity','MahoganyTown','BlackthornCity'}
CITIES={
 'GoldenrodCity':('GOLDENROD CITY','central',(9,14),'commercial'),
 'VioletCity':('VIOLET CITY','central',(18,10),'academy'),
 'AzaleaTown':('AZALEA TOWN','south',(13,19),'woodland'),
 'CherrygroveCity':('CHERRYGROVE CITY','south',(20,16),'coastal'),
 'NewBarkTown':('NEW BARK TOWN','south',(25,16),'village'),
 'MahoganyTown':('MAHOGANY TOWN','east',(21,6),'mountain'),
 'BlackthornCity':('BLACKTHORN CITY','east',(27,6),'ridge'),
 'CianwoodCity':('CIANWOOD CITY','west',(2,17),'island'),
}
# Map name, cluster, relative atlas position, terrain, dimensions.
ROUTES={
 37:('central',(12,9),'orchard',(28,40)),36:('central',(15,10),'junction',(56,28)),
 35:('central',(9,12),'garden',(28,36)),34:('south',(9,17),'coast',(28,44)),
 33:('south',(16,19),'rain',(32,24)),32:('south',(18,15),'riverside',(28,64)),
 31:('south',(20,10),'woodland',(40,28)),30:('south',(21,13),'orchard',(28,44)),
 29:('south',(23,16),'meadow',(52,28)),46:('east',(26,14),'foothills',(28,40)),
 45:('east',(27,11),'ridge',(28,64)),42:('east',(17,6),'lakes',(64,28)),
 43:('east',(21,3),'lakepath',(28,40)),44:('east',(24,6),'ponds',(48,28)),
 40:('west',(3,13),'sea',(32,48)),41:('west',(2,16),'islands',(48,48)),
 47:('west',(0,19),'cliff',(48,32)),48:('west',(0,16),'valley',(28,40)),
}
# name,label,cluster,terrain,dimensions,atlas position,parent section label
LANDMARKS=[
 ('NationalPark','NATIONAL PARK','central','park',(40,40),(9,11)),
 ('RuinsOfAlph','RUINS OF ALPH','central','ruins',(40,36),(16,13)),
 ('IlexForest','ILEX FOREST','south','forest',(40,48),(10,19)),
 ('LakeOfRage','LAKE OF RAGE','east','lake',(48,44),(21,1)),
 ('SafariZoneGate','SAFARI GATE','west','gate',(32,32),(0,14)),
 ('SafariWetlands','SAFARI WETLANDS','west','wetlands',(40,40),(0,13)),
]
# Outdoor border edges: A direction B. Coordinate chosen at center of overlap.
EDGES=[
 ('EcruteakCity','down','JohtoRoute37'),('JohtoRoute37','down','JohtoRoute36'),
 ('JohtoRoute36','right','VioletCity'),('JohtoRoute36','left','NationalPark'),
 ('NationalPark','down','JohtoRoute35'),('JohtoRoute35','down','GoldenrodCity'),
 ('JohtoRoute36','down','RuinsOfAlph'),
 ('GoldenrodCity','down','JohtoRoute34'),('JohtoRoute34','down','IlexForest'),
 ('IlexForest','right','AzaleaTown'),('AzaleaTown','right','JohtoRoute33'),
 ('JohtoRoute32','up','VioletCity'),('JohtoRoute32','left','RuinsOfAlph'),
 ('VioletCity','right','JohtoRoute31'),('JohtoRoute31','down','JohtoRoute30'),
 ('JohtoRoute30','down','CherrygroveCity'),('CherrygroveCity','right','JohtoRoute29'),
 ('JohtoRoute29','right','NewBarkTown'),
 ('EcruteakCity','right','JohtoRoute42'),('JohtoRoute42','right','MahoganyTown'),
 ('MahoganyTown','up','JohtoRoute43'),('JohtoRoute43','up','LakeOfRage'),
 ('MahoganyTown','right','JohtoRoute44'),('BlackthornCity','down','JohtoRoute45'),
 ('JohtoRoute45','down','JohtoRoute46'),('JohtoRoute46','down','JohtoRoute29'),
 ('OlivineCity','left','JohtoRoute40'),('JohtoRoute40','down','JohtoRoute41'),
 ('JohtoRoute41','left','CianwoodCity'),('JohtoRoute47','up','JohtoRoute48'),
 ('JohtoRoute48','up','SafariZoneGate'),('SafariZoneGate','up','SafariWetlands'),
]
# Dungeons: ordered floors, external mouths. Mouth=(parent,x,y,initial floor).
DUNGEONS=[
 ('SproutTower','SPROUT TOWER','central',3,'tower',[( 'VioletCity',10,7,0)]),
 ('AlphChambers','ALPH CHAMBERS','central',3,'ruins',[('RuinsOfAlph',10,8,0),('RuinsOfAlph',28,8,2)]),
 ('UnionCave','UNION CAVE','south',3,'cave',[('JohtoRoute32',18,55,0),('JohtoRoute33',24,7,0)]),
 ('SlowpokeWell','SLOWPOKE WELL','south',2,'well',[('AzaleaTown',38,26,0)]),
 ('DarkCave','DARK CAVE','east',3,'cave',[('JohtoRoute31',30,6,0),('JohtoRoute46',7,8,1),('JohtoRoute45',19,12,2)]),
 ('MtMortar','MT. MORTAR','east',4,'cave',[('JohtoRoute42',10,6,0),('JohtoRoute42',31,6,1),('JohtoRoute42',51,6,3)]),
 ('IcePath','ICE PATH','east',4,'ice',[('JohtoRoute44',38,6,0),('BlackthornCity',8,9,3)]),
 ('DragonsDen','DRAGON\'S DEN','east',2,'shrine',[('BlackthornCity',32,7,0)]),
 ('WhirlIslands','WHIRL ISLANDS','west',4,'islandcave',[('JohtoRoute41',12,10,0),('JohtoRoute41',33,10,1),('JohtoRoute41',12,31,2),('JohtoRoute41',33,31,3)]),
 ('CliffEdgeGate','CLIFF EDGE GATE','west',1,'gate',[('CianwoodCity',12,36,0),('JohtoRoute47',38,10,0)]),
 ('CliffCave','CLIFF CAVE','west',2,'cave',[('JohtoRoute47',28,8,0),('JohtoRoute47',18,24,1)]),
 ('TohjoFalls','TOHJO FALLS','south',2,'falls',[('NewBarkTown',44,18,0)]),
]
# New sectional IDs must fit <=252; preserve pre-existing NONE=213.
SECTIONS=['NewBarkTown','CherrygroveCity','VioletCity','AzaleaTown','GoldenrodCity','CianwoodCity','MahoganyTown','BlackthornCity']+[f'JohtoRoute{i}' for i in range(29,49) if i not in (38,39)]+['SproutTower','RuinsOfAlph','UnionCave','IlexForest','NationalPark','DarkCave','MtMortar','LakeOfRage','IcePath','DragonsDen','WhirlIslands','SlowpokeWell','TohjoFalls']
CLUSTERS=['central','south','east','west']
