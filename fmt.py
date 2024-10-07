class SpawnChunks:
    HEADER          = 0
    SPAWN_OBJECTS   = 1
    LEVEL_POINTS    = 2
    WAY_POINTS      = 3


class SpawnObjectsChunks:
    COUNT   = 0
    OBJECTS = 1
    UNKNOWN = 2


class SpawnObjectChunks:
    OBJECT_ID   = 0
    OBJECT_BODY = 1


class NetPackedChunks:
    SPAWN   = 0
    UPDATE  = 1


class SpawnStates:
    UPDATE  = 0
    SPAWN   = 1


class GameID:
    ANY = 0
    SINGLE = 1
    DEATHMATCH = 2
    CS = 5
    TEAMDEATHMATCH = 6
    ARTEFACTHUNT = 7


class SpawnFlags:
    OBJECT_LOCAL        = 1 << 0    # after spawn it becomes local (authorative)
    OBJECT_HAS_UPDATE   = 1 << 2    # after spawn info it has update inside message
    OBJECT_AS_PLAYER    = 1 << 3    # after spawn it must become viewable
    OBJECT_PHANTOM      = 1 << 4    # after spawn it must become viewable
    VERSION             = 1 << 5    # control version
    UPDATE              = 1 << 6    # + update packet
    TIME                = 1 << 7    # + spawn time


class SkeletonFlags:
    Active      = 1 << 0
    SpawnCopy   = 1 << 1
    SavedData   = 1 << 2
    NotSave     = 1 << 3


XR_AI_VERSION = 8
