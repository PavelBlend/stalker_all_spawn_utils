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


XR_AI_VERSION = 8
