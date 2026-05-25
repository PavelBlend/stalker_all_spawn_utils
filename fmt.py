class SpawnChunks:
    HEADER          = 0
    SPAWN_OBJECTS   = 1
    LEVEL_POINTS    = 2
    WAY_POINTS      = 3


class SpawnObjectsChunks:
    COUNT   = 0
    OBJECTS = 1
    EDGES   = 2


class SpawnObjectChunks:
    OBJECT_ID   = 0
    OBJECT_BODY = 1


class SpawnWayPointsChunks:
    COUNT   = 0
    OBJECTS = 1


class SpawnWayPointChunks:
    NAME    = 0
    DATA    = 1


class SpawnWayPointDataChunks:
    COUNT   = 0
    POINTS  = 1
    LINKS   = 2


class SpawnPointChunks:
    ID      = 0
    DATA    = 1


class NetPackedChunks:
    SPAWN   = 0
    UPDATE  = 1


class SpawnStates:
    UPDATE  = 0
    SPAWN   = 1


SPAWN_STATE = {
    SpawnStates.UPDATE      :   'Update',
    SpawnStates.SPAWN       :   'Spawn'
}


class GameID:
    ANY             = 0
    SINGLE          = 1
    DEATHMATCH      = 2
    CS              = 5
    TEAMDEATHMATCH  = 6
    ARTEFACTHUNT    = 7


GAME_ID = {
    GameID.ANY             :   'Any',
    GameID.SINGLE          :   'Single',
    GameID.DEATHMATCH      :   'Death Match',
    GameID.CS              :   'CS',
    GameID.TEAMDEATHMATCH  :   'Team Death Match',
    GameID.ARTEFACTHUNT    :   'Artefact Hunt'
}


class ShapeType:
    SPHERE      = 0
    BOX         = 1


SHAPE_SPHERE    = 'Sphere'
SHAPE_BOX       = 'Box'

SHAPE_TYPE = {
    ShapeType.SPHERE    :   SHAPE_SPHERE,
    ShapeType.BOX       :   SHAPE_BOX
}


class PhysicObjectType:
    BOX             = 0
    FIXED_CHAIN     = 1
    FREE_CHAIN      = 2
    SKELETON        = 3


PHYSIC_BOX              = 'Box'
PHYSIC_FIXED_CHAIN      = 'Fixed Chain'
PHYSIC_FREE_CHAIN       = 'Free Chain'
PHYSIC_SKELETON         = 'Skeleton'

PHYSIC_OBJECT_TYPE = {
    PhysicObjectType.BOX            :   PHYSIC_BOX,
    PhysicObjectType.FIXED_CHAIN    :   PHYSIC_FIXED_CHAIN,
    PhysicObjectType.FREE_CHAIN     :   PHYSIC_FREE_CHAIN,
    PhysicObjectType.SKELETON       :   PHYSIC_SKELETON
}


class RestrictorType:
    DEFAULT_NONE    = 0
    DEFAULT_OUT     = 1
    DEFAULT_IN      = 2
    NONE            = 3
    IN              = 4
    OUT             = 5


RESTRICTOR_TYPE_DEFAULT_NONE    = 'Default None'
RESTRICTOR_TYPE_DEFAULT_OUT     = 'Default Out'
RESTRICTOR_TYPE_DEFAULT_IN      = 'Default In'
RESTRICTOR_TYPE_NONE            = 'None'
RESTRICTOR_TYPE_IN              = 'In'
RESTRICTOR_TYPE_OUT             = 'Out'

RESTRICTOR_TYPE = {
    RestrictorType.DEFAULT_NONE     :   RESTRICTOR_TYPE_DEFAULT_NONE,
    RestrictorType.DEFAULT_OUT      :   RESTRICTOR_TYPE_DEFAULT_OUT,
    RestrictorType.DEFAULT_IN       :   RESTRICTOR_TYPE_DEFAULT_IN,
    RestrictorType.NONE             :   RESTRICTOR_TYPE_NONE,
    RestrictorType.IN               :   RESTRICTOR_TYPE_IN,
    RestrictorType.OUT              :   RESTRICTOR_TYPE_OUT
}


class SpawnFlags:
    OBJECT_LOCAL        = 1 << 0    # after spawn it becomes local (authorative)
    OBJECT_HAS_UPDATE   = 1 << 2    # after spawn info it has update inside message
    OBJECT_AS_PLAYER    = 1 << 3    # after spawn it must become viewable
    OBJECT_PHANTOM      = 1 << 4    # after spawn it must become viewable
    VERSION             = 1 << 5    # control version
    UPDATE              = 1 << 6    # + update packet
    TIME                = 1 << 7    # + spawn time


class VisualFlags:
    OBSTACLE    = 1 << 0


class ALifeObjectFlags:
    USE_SWITCHES            = 1 << 0
    SWITCH_ONLINE           = 1 << 1
    SWITCH_OFFLINE          = 1 << 2
    INTERACTIVE             = 1 << 3
    VISIBLE_FOR_AI          = 1 << 4
    USEFUL_FOR_AI           = 1 << 5
    OFFLINE_NO_MOVE         = 1 << 6
    USED_AI_LOCATIONS       = 1 << 7
    GROUP_BEHAVIOUR         = 1 << 8
    CAN_SAVE                = 1 << 9
    VISIBLE_FOR_MAP         = 1 << 10
    USE_SMART_TERRAINS      = 1 << 11
    CHECK_FOR_SEPARATOR     = 1 << 12


class PHSkeletonFlags:
    ACTIVE          = 1 << 0
    SPAWN_COPY      = 1 << 1
    SAVED_DATA      = 1 << 2
    NOT_SAVE        = 1 << 3


class ALifeObjectHangingLampFlags:
    PHYSIC              = 1 << 0
    CAST_SHADOW         = 1 << 1
    R1                  = 1 << 2
    R2                  = 1 << 3
    TYPE_SPOT           = 1 << 4
    POINT_AMBIENT       = 1 << 5


class TraderFlags:
    INFINITE_AMMO   = 1 << 0
    DUMMY           = 0xffffffff


class WeaponAddonFlags:
    SCOPE               = 1 << 0
    GRENADE_LAUNCHER    = 1 << 1
    SILENCER            = 1 << 2


XR_AI_VERSION = 8
