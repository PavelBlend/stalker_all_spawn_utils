from net_packet_spawn import *


cse_alife_dynamic_object_visual = (
    *BASE,
    *CSE_ABSTRACT,
    *CSE_ALIFE_OBJECT,
    *CSE_VISUAL
)

cse_alife_object_breakable = (
    *cse_alife_dynamic_object_visual,
    *CSE_ALIFE_OBJECT_BREAKABLE
)

cse_alife_object_climable = (
    *BASE,
    *CSE_ABSTRACT,
    *CSE_ALIFE_OBJECT,
    *CFORM
)

cse_alife_creature_abstract = (
    *cse_alife_dynamic_object_visual,
    *CSE_ALIFE_CREATURE_ABSTRACT
)

cse_alife_creature_actor = (
    *cse_alife_creature_abstract,
    *CSE_ALIFE_TRADER_ABSTRACT,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_CREATURE_ACTOR
)

cse_alife_object_physic = (
    *cse_alife_dynamic_object_visual,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_OBJECT_PHYSIC
)

cse_alife_object_hanging_lamp = (
    *cse_alife_dynamic_object_visual,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_OBJECT_HANGING_LAMP
)

cse_alife_trader = (
    *cse_alife_dynamic_object_visual,
    *CSE_ALIFE_TRADER_ABSTRACT
)

cse_alife_space_restrictor = (
    *BASE,
    *CSE_ABSTRACT,
    *CSE_ALIFE_OBJECT,
    *CFORM,
    *CSE_ALIFE_SPACE_RESTRICTOR
)

cse_alife_level_changer = (
    *cse_alife_space_restrictor,
    *CSE_ALIFE_LEVEL_CHANGER
)

cse_alife_smart_zone = (
    *cse_alife_space_restrictor,
    *CSE_ALIFE_SMART_ZONE
)

se_smart_terrain = (
    *cse_alife_smart_zone,
    *SE_SMART_TERRAIN
)

cse_alife_monster_base = (
    *cse_alife_creature_abstract,
    *CSE_ALIFE_MONSTER_ABSTRACT,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_MONSTER_BASE
)

cse_alife_human_stalker = (
    *BASE,
    *CSE_ABSTRACT,
    *CSE_ALIFE_TRADER_ABSTRACT,
    *CSE_ALIFE_OBJECT,
    *CSE_VISUAL,
    *CSE_ALIFE_CREATURE_ABSTRACT,
    *CSE_ALIFE_MONSTER_ABSTRACT,
    *CALIFE_HUMAN_BRAIN,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_HUMAN_STALKER
)

cse_alife_helicopter = (
    *cse_alife_dynamic_object_visual,
    *CSE_MOTION,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_HELICOPTER
)

cse_alife_car = (
    *cse_alife_dynamic_object_visual,
    *CSE_PH_SKELETON,
    *CSE_ALIFE_CAR
)

cse_alife_item = (
    *cse_alife_dynamic_object_visual,
    *CSE_ALIFE_INVENTORY_ITEM
)

cse_alife_item_weapon = (
    *cse_alife_item,
    *CSE_ALIFE_ITEM_WEAPON
)

cse_alife_item_ammo = (
    *cse_alife_item,
    *CSE_ALIFE_ITEM_AMMO
)

cse_alife_anomalous_zone = (
    *cse_alife_space_restrictor,
    *CSE_ALIFE_CUSTOM_ZONE,
    *CSE_ALIFE_ANOMALOUS_ZONE
)

se_zone_anom = (
    *cse_alife_anomalous_zone,
    *SE_ZONE_ANOM
)

cse_alife_zone_visual = (
    *cse_alife_space_restrictor,
    *CSE_ALIFE_CUSTOM_ZONE,
    *CSE_ALIFE_ANOMALOUS_ZONE,
    *CSE_VISUAL,
    *CSE_ALIFE_ZONE_VISUAL
)

cse_alife_torrid_zone = (
    *cse_alife_space_restrictor,
    *CSE_ALIFE_CUSTOM_ZONE,
    *CSE_MOTION
)
