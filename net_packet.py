import fmt


int32       = 'int32'
uint8       = 'uint8'
uint16      = 'uint16'
uint32      = 'uint32'
uint64      = 'uint64'
float32     = 'float32'
vec3        = 'vec3'
vec4        = 'vec4'
matrix3x4   = 'matrix3x4'
flags8      = 'flags8'
flags16     = 'flags16'
flags32     = 'flags32'
string      = 'string'
ctime       = 'ctime'
get_bytes   = 'get_bytes'
comment     = 'comment'

def_fun = lambda x: bool(x)

###############################################################################


class NetPacket:

    def __init__(self, reader, props_desc):

        self.reader         = reader
        self.props_desc     = props_desc

        # first comment
        reader.props.append([self.__class__.__name__, None, comment])

        # read net packet properties
        self.read()

        # new line
        reader.props.append(['', None, comment])

    def read_prop(self, prop):

        name    = prop[0]
        typ     = prop[1]

        if len(prop) == 4:
            cond_name = prop[2]
            cond_fun  = prop[3]

            cond_value = self.get_readed_prop(cond_name)
            cond = cond_fun(cond_value)

            if cond:
                self.get(name, typ)

        elif typ in (flags8, flags16, flags32):
            flag_props = prop[2]
            flags_value = self.get(name, typ, append=False)

            for flag_name, flag_mask in flag_props:
                flag_value = bool(flags_value & flag_mask)
                self.append(flag_name, flag_value, typ)

        elif typ == get_bytes:
            size_prop = prop[2]
            size = self.get_readed_prop(size_prop)
            offs = self.reader.offset
            data = self.reader.data[offs : offs + size]
            self.reader.skip(size)
            self.append(name, data, typ)

        elif name == 'cycle':
            iter_count_prop = self.get_readed_prop(typ)
            cycle_props = prop[2]
            for i in range(iter_count_prop):
                for cycle_prop in cycle_props:
                    prop_name = cycle_prop[0].format(i)
                    prop = list(cycle_prop)
                    prop[0] = prop_name
                    self.read_prop(prop)

        else:
            self.get(name, typ)

    def read(self):
        for prop in self.props_desc:
            self.read_prop(prop)

    def get_readed_prop(self, prop_name):

        result = None

        for name, value, fmt in self.reader.props:
            if name == prop_name:
                result = value

        if result is None:
            print(f'cannot find property: {prop_name}')

        return result

    def get(self, name, fmt, *args, append=True):
        read_fun = getattr(self.reader, fmt, None)
        value = read_fun(*args)
        if append:
            self.reader.props.append([name, value, fmt])
        return value

    def append(self, name, value, fmt):
        self.reader.props.append([name, value, fmt])


###############################################################################


BASE = (
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

CSE_ABSTRACT = (
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
    ('version',             uint16,         'check_version',    def_fun),
    ('script_version',      uint16),
    ('client_data_size',    uint16),
    ('client_data',         get_bytes,      'client_data_size'),
    ('spawn_id',            uint16),
    ('size',                uint16)
)

VISUAL_FLAGS = (
    ('obstacle', fmt.VisualFlags.OBSTACLE),
)

CSE_VISUAL = (
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

CSE_ALIFE_OBJECT = (
    ('graph_id',        uint16),
    ('distance',        float32),
    ('direct_control',  uint32),
    ('node_id',         uint32),
    ('flags',           flags32,    ALIFE_OBJECT_FLAGS),
    ('ini_string',      string),
    ('story_id',        uint32),
    ('spawn_story_id',  uint32)
)

CSE_ALIFE_OBJECT_BREAKABLE = (
    ('health', float32),
)

CFORM = (
    ('shapes_count',    uint8),
    ('cycle',       'shapes_count', (
            ('shape_type',   uint8),
            ('position_{}',     vec3,       'shape_type',   lambda x: x == 0),
            ('radius_{}',       float32,    'shape_type',   lambda x: x == 0),
            ('matrix_{}',       matrix3x4,  'shape_type',   lambda x: x != 0)
        )
    )
)

PH_SKELETON_FLAGS = (
    ('active',       fmt.PHSkeletonFlags.ACTIVE),
    ('spawn_copy',   fmt.PHSkeletonFlags.SPAWN_COPY),
    ('saved_data',   fmt.PHSkeletonFlags.SAVED_DATA),
    ('not_save',     fmt.PHSkeletonFlags.NOT_SAVE)
)

CSE_PH_SKELETON = (
    ('startup_animation',   string),
    ('flags',               flags8,     PH_SKELETON_FLAGS),
    ('source_id',           uint16),
    ('bones_mask',          uint64,     'saved_data',    def_fun),
    ('root_bone',           uint16,     'saved_data',    def_fun),
    ('linear_vel',          vec3,       'saved_data',    def_fun),
    ('position',            vec3,       'saved_data',    def_fun),
    ('quaternion',          vec4,       'saved_data',    def_fun),
    ('enabled',             uint8,      'saved_data',    def_fun),
    ('vec_min',             vec3,       'saved_data',    def_fun),
    ('vec_max',             vec3,       'saved_data',    def_fun)
)

CSE_ALIFE_CREATURE_ABSTRACT = (
    ('team',                        uint8),
    ('squad',                       uint8),
    ('group',                       uint8),
    ('health',                      float32),
    ('dynamic_out_restrictions',    uint32),
    ('dynamic_in_restrictions',     uint32),
    ('killer_id',                   uint16),
    ('game_death_time',             uint64)
)

CSE_ALIFE_TRADER_ABSTRACT = (
    ('money',               uint32),
    ('specific_character',  string),
    ('trader_flags',        uint32),
    ('character_profile',   string),
    ('community_index',     int32),
    ('rank',                int32),
    ('reputation',          int32),
    ('character_name',      string)
)

CSE_ALIFE_CREATURE_ACTOR = (
    ('holder_id', uint16),
)

CSE_ALIFE_OBJECT_PHYSIC = (
    ('type_',           uint32),
    ('mass',            float32),
    ('fixed_bones',     string)
)

ALIFE_OBJECT_HANGING_LAMP_FLAGS = (
    ('physic',          fmt.ALifeObjectHangingLampFlags.PHYSIC),
    ('cast_shadow',     fmt.ALifeObjectHangingLampFlags.CAST_SHADOW),
    ('r1',              fmt.ALifeObjectHangingLampFlags.R1),
    ('r2',              fmt.ALifeObjectHangingLampFlags.R2),
    ('type_spot',       fmt.ALifeObjectHangingLampFlags.TYPE_SPOT),
    ('point_ambient',   fmt.ALifeObjectHangingLampFlags.POINT_AMBIENT)
)

CSE_ALIFE_OBJECT_HANGING_LAMP = (
    ('color',               uint32),
    ('brightness',          float32),
    ('color_animator',      string),
    ('range_',              float32),
    ('flags',               uint16,     ALIFE_OBJECT_HANGING_LAMP_FLAGS),
    ('startup_animation',   string),
    ('fixed_bones',         string),
    ('health',              float32),
    ('virtual_size',        float32),
    ('ambient_radius',      float32),
    ('ambient_power',       float32),
    ('ambient_texture',     string),
    ('light_texture',       string),
    ('light_main_bone',     string),
    ('spot_cone_angle',     float32),
    ('glow_texture',        string),
    ('glow_radius',         float32),
    ('light_ambient_bone',  string)
)

CSE_ALIFE_SPACE_RESTRICTOR = (
    ('space_restrictor_type',  uint8),
)

CSE_ALIFE_LEVEL_CHANGER = (
    ('next_graph_id',  uint16),
    ('next_node_id',  uint32),
    ('next_position',  vec3),
    ('angles',  vec3),
    ('level_to_change',  string),
    ('level_point_to_change',  string),
    ('silent_mode',  uint8)
)

CSE_ALIFE_MONSTER_ABSTRACT = (
    ('out_space_restrictors',   string),
    ('in_space_restrictors',    string),
    ('smart_terrain_id',        uint16),
    ('task_reached',            uint8)
)

CSE_ALIFE_MONSTER_BASE = (
    ('spec_object_id',  uint16),
    ('unknown',         uint16)
)

CSE_ALIFE_HUMAN_STALKER = (
    ('job_online',              uint8),
    ('job_online_condlist',     string,     'job_online',     lambda x: x > 2),
    ('was_in_smart_terrain',    uint8),
    ('death_droped',            uint8)
)

CALIFE_HUMAN_BRAIN = (
    ('equipment_preference_count', uint32),
    ('cycle',       'equipment_preference_count', (('equipment_preference_{}', uint8), )),
    ('weapon_preferences_count', uint32),
    ('cycle',       'weapon_preferences_count',   (('weapon_preferences_{}',   uint8), ))
)

CSE_ALIFE_HELICOPTER = (
    ('startup_animation',   string),
    ('engine_sound',        string)
)

CSE_MOTION = (
    ('motion_name', string),
)

CSE_ALIFE_INVENTORY_ITEM = (
    ('condition', float32),
)

CSE_ALIFE_CUSTOM_ZONE = (
    ('max_power',           float32),
    ('owner_id',            uint32),
    ('enabled_time',        uint32),
    ('disabled_time',       uint32),
    ('start_time_shift',    uint32)
)

CSE_ALIFE_ANOMALOUS_ZONE = (
    ('offline_interactive_radius',  float32),
    ('artefact_spawn_count',        uint16),
    ('artefact_position_offset',    uint32)
)

CSE_ALIFE_ITEM_WEAPON = (
    ('current',         uint16),
    ('elapsed',         uint16),
    ('wpn_state',       uint8),
    ('addon_flags',     uint8),
    ('ammo_type',       uint8)
)

CSE_ALIFE_SMART_ZONE = (
    ('table_size',      uint8),
    ('cycle',           'table_size',   (('spawned_obj_{}',  uint16), ))
)

CSE_ALIFE_ZONE_VISUAL = (
    ('startup_animation',   string),
    ('attack_animation',    string),
    ('flag',                uint8)
)

CSE_ALIFE_ITEM_AMMO = (
    ('elapsed', uint16),
)

CSE_ALIFE_CAR = (
    ('health', float32),
)

SE_SMART_TERRAIN = (
    ('duration_end',    ctime),
    ('idle_end',        ctime)
)

SE_ZONE_ANOM = (
    ('flag', uint8),
    ('last_spawn_time', ctime, 'flag', def_fun)
)

###############################################################################

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
