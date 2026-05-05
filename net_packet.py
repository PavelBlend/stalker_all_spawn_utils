import fmt


int32 = 'int32'
uint8 = 'uint8'
uint16 = 'uint16'
uint32 = 'uint32'
uint64 = 'uint64'
float32 = 'float32'
vec3 = 'vec3'
vec4 = 'vec4'
matrix3x4 = 'matrix3x4'
flags8 = 'flags8'
flags16 = 'flags16'
flags32 = 'flags32'
string = 'string'
ctime = 'ctime'
get_bytes = 'get_bytes'
comment = 'comment'


###############################################################################


class NetPacket:
    def __init__(self, reader):
        self.reader = reader
        reader.props.append([self.__class__.__name__, None, comment])
        self.read()
        reader.props.append(['', None, comment])

    def read(self):
        for prop in self.props:
            name    = prop[0]
            typ     = prop[1]

            if len(prop) == 4:
                cond_name = prop[2]
                cond_fun = prop[3]

            elif typ == flags16:
                flag_props = prop[2]

            elif typ == get_bytes:
                size = prop[2]

            self.get(name, typ)

    def get(self, name, fmt, *args, append=True):
        read_fun = getattr(self.reader, fmt, None)
        value = read_fun(*args)
        if append:
            self.reader.props.append([name, value, fmt])
        return value

    def append(self, name, value, fmt):
        self.reader.props.append([name, value, fmt])


###############################################################################


BASE_PROPS = (
    ('net_packet_size',     uint16),
    ('state',               uint16)
)

SPAWN_FLAGS = (
    ('object_local',        fmt.SpawnFlags.OBJECT_LOCAL),
    ('object_upd',          fmt.SpawnFlags.OBJECT_HAS_UPDATE),
    ('object_as_player',    fmt.SpawnFlags.OBJECT_AS_PLAYER),
    ('object_phantom',      fmt.SpawnFlags.OBJECT_PHANTOM),
    ('check_version',       fmt.SpawnFlags.VERSION),
    ('update_packet',       fmt.SpawnFlags.UPDATE),
    ('spawn_time',          fmt.SpawnFlags.TIME)
)

CSE_ABSTRACT_PROPS = (
    ('section_name',        string),
    ('name',                string),

    ('game_type',           uint8),    # GameID in fmt
    ('rp',                  uint8),    # use supplied coords
    ('position',            vec3),
    ('direction',           vec3),
    ('respawn_time',        uint16),
    ('object_id',           uint16),
    ('id_parent',           uint16),
    ('id_phantom',          uint16),
    ('flags',               flags16,        SPAWN_FLAGS),
    ('version',             uint16,         'check_version',    lambda x: bool(x)),
    ('script_version',      uint16),
    ('client_data_size',    uint16),
    ('client_data',         get_bytes,      'client_data_size'),
    ('spawn_id',            uint16),
    ('size',                uint16)
)

VISUAL_FLAGS = (
    ('obstacle', fmt.VisualFlags.OBSTACLE),
)

CSE_VISUAL_PROPS = (
    ('visual_name', string),
    ('flags',       flags8,     VISUAL_FLAGS)
)

ALIFE_OBJECT_FLAGS = (
    ('use_switches',            fmt.ALifeObjectFlags.USE_SWITCHES),
    ('switch_online',           fmt.ALifeObjectFlags.SWITCH_ONLINE),
    ('switch_offline',          fmt.ALifeObjectFlags.SWITCH_OFFLINE),
    ('interactive',             fmt.ALifeObjectFlags.INTERACTIVE),
    ('visible_for_ai',          fmt.ALifeObjectFlags.VISIBLE_FOR_AI),
    ('useful_for_ai',           fmt.ALifeObjectFlags.USEFUL_FOR_AI),
    ('offline_no_move',         fmt.ALifeObjectFlags.OFFLINE_NO_MOVE),
    ('used_ai_locations',       fmt.ALifeObjectFlags.USED_AI_LOCATIONS),
    ('group_behaviour',         fmt.ALifeObjectFlags.GROUP_BEHAVIOUR),
    ('can_save',                fmt.ALifeObjectFlags.CAN_SAVE),
    ('visible_for_map',         fmt.ALifeObjectFlags.VISIBLE_FOR_MAP),
    ('use_smart_terrains',      fmt.ALifeObjectFlags.USE_SMART_TERRAINS),
    ('check_for_separator',     fmt.ALifeObjectFlags.CHECK_FOR_SEPARATOR)
)

CSE_ALIFE_OBJECT_PROPS = (
    ('graph_id',        uint16),
    ('distance',        float32),
    ('direct_control',  uint32),
    ('node_id',         uint32),
    ('flags',           flags32,    ALIFE_OBJECT_FLAGS),
    ('ini_string',      string),
    ('story_id',        uint32),
    ('spawn_story_id',  uint32)
)


class Base(NetPacket):

    def read(self):
        self.get('net_packet_size', uint16)
        self.get('state', uint16)


class CSE_ALifeObjectBreakable(NetPacket):

    def read(self):
        self.get('health', float32)


class CForm(NetPacket):

    def read(self):
        shapes_count = self.get('shapes_count', uint8)

        for shape_index in range(shapes_count):
            shape_type = self.get('shape_type_{}'.format(shape_index), uint8)

            if shape_type == 0:    # sphere
                self.get('position_{}'.format(shape_index),    vec3)
                self.get('radius_{}'.format(shape_index),      float32)

            else:    # box
                self.get('matrix_{}'.format(shape_index), matrix3x4)


class CSE_PHSkeleton(NetPacket):

    def read(self):
        self.get            ('startup_animation',   string)
        flags = self.get    ('flags',               uint8, append=False)
        self.get            ('source_id',           uint16)

        active      = bool(flags & fmt.PHSkeletonFlags.ACTIVE)
        spawn_copy  = bool(flags & fmt.PHSkeletonFlags.SPAWN_COPY)
        saved_data  = bool(flags & fmt.PHSkeletonFlags.SAVED_DATA)
        not_save    = bool(flags & fmt.PHSkeletonFlags.NOT_SAVE)

        self.append('active',       active,         'flags')
        self.append('spawn_copy',   spawn_copy,     'flags')
        self.append('saved_data',   saved_data,     'flags')
        self.append('not_save',     not_save,       'flags')

        if saved_data:

            # bones data
            self.get('bones_mask',  uint64)
            self.get('root_bone',   uint16)
            self.get('linear_vel',  vec3)
            self.get('position',    vec3)
            self.get('quaternion',  vec4)
            self.get('enabled',     uint8)
            self.get('vec_min',     vec3)
            self.get('vec_max',     vec3)


class CSE_ALifeCreatureAbstract(NetPacket):

    def read(self):
        self.get('team',                        uint8)
        self.get('squad',                       uint8)
        self.get('group',                       uint8)
        self.get('health',                      float32)
        self.get('dynamic_out_restrictions',    uint32)
        self.get('dynamic_in_restrictions',     uint32)
        self.get('killer_id',                   uint16)
        self.get('game_death_time',             uint64)


class CSE_ALifeTraderAbstract(NetPacket):

    def read(self):
        self.get('money',               uint32)
        self.get('specific_character',  string)
        self.get('trader_flags',        uint32)
        self.get('character_profile',   string)
        self.get('community_index',     int32)
        self.get('rank',                int32)
        self.get('reputation',          int32)
        self.get('character_name',      string)


class CSE_ALifeCreatureActor(NetPacket):

    def read(self):
        self.get('holder_id', uint16)


class CSE_ALifeObjectPhysic(NetPacket):

    def read(self):
        self.get('type_',           uint32)
        self.get('mass',            float32)
        self.get('fixed_bones',     string)


class CSE_ALifeObjectHangingLamp(NetPacket):

    def read(self):
        self.get('color',               uint32)
        self.get('brightness',          float32)
        self.get('color_animator',      string)
        self.get('range_',              float32)

        flags = self.get('flags',               uint16, append=False)

        physic          = bool(flags & fmt.ALifeObjectHangingLampFlags.PHYSIC)
        cast_shadow     = bool(flags & fmt.ALifeObjectHangingLampFlags.CAST_SHADOW)
        r1              = bool(flags & fmt.ALifeObjectHangingLampFlags.R1)
        r2              = bool(flags & fmt.ALifeObjectHangingLampFlags.R2)
        type_spot       = bool(flags & fmt.ALifeObjectHangingLampFlags.TYPE_SPOT)
        point_ambient   = bool(flags & fmt.ALifeObjectHangingLampFlags.POINT_AMBIENT)

        self.append('physic',           physic,         'flags')
        self.append('cast_shadow',      cast_shadow,    'flags')
        self.append('r1',               r1,             'flags')
        self.append('r2',               r2,             'flags')
        self.append('type_spot',        type_spot,      'flags')
        self.append('point_ambient',    point_ambient,  'flags')

        self.get('startup_animation',   string)
        self.get('fixed_bones',         string)
        self.get('health',              float32)
        self.get('virtual_size',        float32)
        self.get('ambient_radius',      float32)
        self.get('ambient_power',       float32)
        self.get('ambient_texture',     string)
        self.get('light_texture',       string)
        self.get('light_main_bone',     string)
        self.get('spot_cone_angle',     float32)
        self.get('glow_texture',        string)
        self.get('glow_radius',         float32)
        self.get('light_ambient_bone',  string)


class CSE_ALifeSpaceRestrictor(NetPacket):

    def read(self):
        self.get('space_restrictor_type',  uint8)


class CSE_ALifeLevelChanger(NetPacket):

    def read(self):
        self.get('next_graph_id',  uint16)
        self.get('next_node_id',  uint32)
        self.get('next_position',  vec3)
        self.get('angles',  vec3)
        self.get('level_to_change',  string)
        self.get('level_point_to_change',  string)
        self.get('silent_mode',  uint8)


class CSE_ALifeMonsterAbstract(NetPacket):

    def read(self):
        self.get('out_space_restrictors',   string)
        self.get('in_space_restrictors',    string)
        self.get('smart_terrain_id',        uint16)
        self.get('task_reached',            uint8)


class CSE_ALifeMonsterBase(NetPacket):

    def read(self):
        self.get('spec_object_id',  uint16)
        self.get('unknown',         uint16)


class CSE_AlifeHumanStalker(NetPacket):
    def read(self):
        job_online = self.get('job_online', uint8)
        if job_online > 2:
            self.get('job_online_condlist', string)
        self.get('was_in_smart_terrain',    uint8)
        self.get('death_droped',            uint8)


class CALifeHumanBrain(NetPacket):

    def read(self):
        equipment_preference_count = self.get('item_count', uint32)
        for i in range(equipment_preference_count):
            self.get('equipment_preference_{}'.format(i), uint8)

        weapon_preferences_count = self.get('item_count', uint32)
        for i in range(weapon_preferences_count):
            self.get('weapon_preferences_{}'.format(i), uint8)


class CSE_ALifeHelicopter(NetPacket):

    def read(self):
        self.get('startup_animation',   string)
        self.get('engine_sound',        string)


class CSE_Motion(NetPacket):

    def read(self):
        self.get('motion_name', string)


class CSE_ALifeInventoryItem(NetPacket):

    def read(self):
        self.get('condition', float32)


class CSE_ALifeCustomZone(NetPacket):

    def read(self):
        self.get('max_power',           float32)
        self.get('owner_id',            uint32)
        self.get('enabled_time',        uint32)
        self.get('disabled_time',       uint32)
        self.get('start_time_shift',    uint32)


class CSE_ALifeAnomalousZone(NetPacket):

    def read(self):
        self.get('offline_interactive_radius',  float32)
        self.get('artefact_spawn_count',        uint16)
        self.get('artefact_position_offset',    uint32)


class CSE_ALifeItemWeapon(NetPacket):

    def read(self):
        self.get('current',         uint16)
        self.get('elapsed',         uint16)
        self.get('wpn_state',       uint8)
        self.get('addon_flags',     uint8)
        self.get('ammo_type',       uint8)


class CSE_AlifeSmartZone(NetPacket):

    def read(self):
        table_size = self.get('table_size', uint8)
        for i in range(table_size):
            self.get('spawned_obj_{}'.format(i), uint16)


class CSE_ALifeZoneVisual(NetPacket):

    def read(self):
        self.get('startup_animation',   string)
        self.get('attack_animation',    string)
        self.get('flag',                uint8)


class CSE_ALifeItemAmmo(NetPacket):

    def read(self):
        self.get('elapsed', uint16)


class CSE_ALifeCar(NetPacket):

    def read(self):
        self.get('health', float32)


class SE_SmartTerrain(NetPacket):

    def read(self):
        self.get('duration_end',    ctime)
        self.get('idle_end',        ctime)


class SE_ZoneAnom(NetPacket):

    def read(self):
        flag = self.get('flag', uint8)
        if flag:
            self.get('last_spawn_time', ctime)


###############################################################################


def cse_alife_dynamic_object_visual(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)


def cse_alife_object_breakable(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_ALifeObjectBreakable(reader)


def cse_alife_object_climable(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CForm(reader)


def cse_alife_creature_abstract(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_ALifeCreatureAbstract(reader)


def cse_alife_creature_actor(reader):
    cse_alife_creature_abstract(reader)
    CSE_ALifeTraderAbstract(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeCreatureActor(reader)


def cse_alife_object_physic(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeObjectPhysic(reader)


def cse_alife_object_hanging_lamp(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeObjectHangingLamp(reader)


def cse_alife_trader(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_ALifeTraderAbstract(reader)


def cse_alife_space_restrictor(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CForm(reader)
    CSE_ALifeSpaceRestrictor(reader)


def cse_alife_level_changer(reader):
    cse_alife_space_restrictor(reader)
    CSE_ALifeLevelChanger(reader)


def cse_alife_smart_zone(reader):
    cse_alife_space_restrictor(reader)
    CSE_AlifeSmartZone(reader)


def se_smart_terrain(reader):
    cse_alife_smart_zone(reader)
    SE_SmartTerrain(reader)


def cse_alife_monster_base(reader):
    cse_alife_creature_abstract(reader)
    CSE_ALifeMonsterAbstract(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeMonsterBase(reader)


def cse_alife_human_stalker(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeTraderAbstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_ALifeCreatureAbstract(reader)
    CSE_ALifeMonsterAbstract(reader)
    CALifeHumanBrain(reader)
    CSE_PHSkeleton(reader)
    CSE_AlifeHumanStalker(reader)


def cse_alife_helicopter(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_Motion(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeHelicopter(reader)


def cse_alife_car(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeCar(reader)


def cse_alife_item(reader):
    cse_alife_dynamic_object_visual(reader)
    CSE_ALifeInventoryItem(reader)


def cse_alife_item_weapon(reader):
    cse_alife_item(reader)
    CSE_ALifeItemWeapon(reader)


def cse_alife_item_ammo(reader):
    cse_alife_item(reader)
    CSE_ALifeItemAmmo(reader)


def cse_alife_anomalous_zone(reader):
    cse_alife_space_restrictor(reader)
    CSE_ALifeCustomZone(reader)
    CSE_ALifeAnomalousZone(reader)


def se_zone_anom(reader):
    cse_alife_anomalous_zone(reader)
    SE_ZoneAnom(reader)


def cse_alife_zone_visual(reader):
    cse_alife_space_restrictor(reader)
    CSE_ALifeCustomZone(reader)
    CSE_ALifeAnomalousZone(reader)
    CSE_Visual(reader)
    CSE_ALifeZoneVisual(reader)


def cse_alife_torrid_zone(reader):
    cse_alife_space_restrictor(reader)
    CSE_ALifeCustomZone(reader)
    CSE_Motion(reader)
