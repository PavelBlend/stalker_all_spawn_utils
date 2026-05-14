from net_packet_spawn import *


cse_alife_dynamic_object_visual = (
    *BASE,
    *ABSTRACT,
    *OBJECT,
    *VISUAL
)

cse_alife_object_breakable = (
    *cse_alife_dynamic_object_visual,
    *OBJECT_BREAKABLE
)

cse_alife_object_climable = (
    *BASE,
    *ABSTRACT,
    *OBJECT,
    *CFORM
)

cse_alife_creature_abstract = (
    *cse_alife_dynamic_object_visual,
    *CREATURE_ABSTRACT
)

cse_alife_creature_actor = (
    *cse_alife_creature_abstract,
    *TRADER_ABSTRACT,
    *PH_SKELETON,
    *CREATURE_ACTOR
)

cse_alife_object_physic = (
    *cse_alife_dynamic_object_visual,
    *PH_SKELETON,
    *OBJECT_PHYSIC
)

cse_alife_object_hanging_lamp = (
    *cse_alife_dynamic_object_visual,
    *PH_SKELETON,
    *HANGING_LAMP
)

cse_alife_trader = (
    *cse_alife_dynamic_object_visual,
    *TRADER_ABSTRACT
)

cse_alife_space_restrictor = (
    *BASE,
    *ABSTRACT,
    *OBJECT,
    *CFORM,
    *SPACE_RESTRICTOR
)

cse_alife_level_changer = (
    *cse_alife_space_restrictor,
    *LEVEL_CHANGER
)

cse_alife_smart_zone = (
    *cse_alife_space_restrictor,
    *SMART_ZONE
)

se_smart_terrain = (
    *cse_alife_smart_zone,
    *SMART_TERRAIN
)

cse_alife_monster_base = (
    *cse_alife_creature_abstract,
    *MONSTER_ABSTRACT,
    *PH_SKELETON,
    *MONSTER_BASE
)

cse_alife_human_stalker = (
    *BASE,
    *ABSTRACT,
    *TRADER_ABSTRACT,
    *OBJECT,
    *VISUAL,
    *CREATURE_ABSTRACT,
    *MONSTER_ABSTRACT,
    *HUMAN_BRAIN,
    *PH_SKELETON,
    *HUMAN_STALKER
)

cse_alife_helicopter = (
    *cse_alife_dynamic_object_visual,
    *MOTION,
    *PH_SKELETON,
    *HELICOPTER
)

cse_alife_car = (
    *cse_alife_dynamic_object_visual,
    *PH_SKELETON,
    *CAR
)

cse_alife_item = (
    *cse_alife_dynamic_object_visual,
    *INVENTORY_ITEM
)

cse_alife_item_weapon = (
    *cse_alife_item,
    *ITEM_WEAPON
)

cse_alife_item_ammo = (
    *cse_alife_item,
    *ITEM_AMMO
)

cse_alife_anomalous_zone = (
    *cse_alife_space_restrictor,
    *CUSTOM_ZONE,
    *ANOMALOUS_ZONE
)

se_zone_anom = (
    *cse_alife_anomalous_zone,
    *ZONE_ANOM
)

cse_alife_zone_visual = (
    *cse_alife_space_restrictor,
    *CUSTOM_ZONE,
    *ANOMALOUS_ZONE,
    *VISUAL,
    *ZONE_VISUAL
)

cse_alife_torrid_zone = (
    *cse_alife_space_restrictor,
    *CUSTOM_ZONE,
    *MOTION
)
