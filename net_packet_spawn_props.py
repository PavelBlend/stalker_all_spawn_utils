from net_packet import *


BASE = (
    ('net_packet_size',     uint16),
    ('state',               enum16,     fmt.SPAWN_STATE)
)

SPAWN_FLAGS = (
    ('object_local',        fmt.SpawnFlags.OBJECT_LOCAL),
    ('object_has_update',   fmt.SpawnFlags.OBJECT_HAS_UPDATE),
    ('object_as_player',    fmt.SpawnFlags.OBJECT_AS_PLAYER),
    ('object_phantom',      fmt.SpawnFlags.OBJECT_PHANTOM),
    ('check_version',       fmt.SpawnFlags.VERSION),
    ('update_packet',       fmt.SpawnFlags.UPDATE),
    ('spawn_time',          fmt.SpawnFlags.TIME)
)

ABSTRACT = (
    ('section_name',        string),
    ('name',                string),
    ('game_type',           enum8,          fmt.GAME_ID),
    ('respawn_point',       uint8),     ####### разобрать - use supplied coords
    ('position',            vec3),
    ('direction',           vec3),
    ('respawn_time',        uint16),
    ('object_id',           uint16),
    ('id_parent',           uint16),
    ('id_phantom',          uint16),
    ('spawn_flags',         flags16,        SPAWN_FLAGS),
    ('version',             uint16,         'check_version',    def_fun),
    ('script_version',      uint16),
    ('client_data_size',    uint16),
    ('client_data',         get_bytes,      'client_data_size'),
    ('spawn_id',            uint16),
    ('size',                uint16)
)

VISUAL_FLAGS = (
    ('visual_obstacle', fmt.VisualFlags.OBSTACLE),
)

VISUAL = (
    ('visual_name',     string),
    ('visual_flags',    flags8,     VISUAL_FLAGS)
)

OBJECT_FLAGS = (
    ('use_switches',            fmt.ALifeObjectFlags.USE_SWITCHES),
    ('switch_online',           fmt.ALifeObjectFlags.SWITCH_ONLINE),
    ('switch_offline',          fmt.ALifeObjectFlags.SWITCH_OFFLINE),
    ('interactive',             fmt.ALifeObjectFlags.INTERACTIVE),
    ('visible_for_ai',          fmt.ALifeObjectFlags.VISIBLE_FOR_AI),
    ('useful_for_ai',           fmt.ALifeObjectFlags.USEFUL_FOR_AI),
    ('offline_no_move',         fmt.ALifeObjectFlags.OFFLINE_NO_MOVE),
    ('used_ai_locations',       fmt.ALifeObjectFlags.USED_AI_LOCATIONS),
    ('group_behaviour',         fmt.ALifeObjectFlags.GROUP_BEHAVIOUR),
    ('object_can_save',         fmt.ALifeObjectFlags.CAN_SAVE),
    ('visible_for_map',         fmt.ALifeObjectFlags.VISIBLE_FOR_MAP),
    ('use_smart_terrains',      fmt.ALifeObjectFlags.USE_SMART_TERRAINS),
    ('check_for_separator',     fmt.ALifeObjectFlags.CHECK_FOR_SEPARATOR)
)

OBJECT = (
    ('graph_id',                uint16),
    ('distance',                float32),
    ('direct_control',          bool32),
    ('node_id',                 uint32),
    ('alife_object_flags',      flags32,    OBJECT_FLAGS),
    ('ini_string',              string),
    ('story_id',                uint32),
    ('spawn_story_id',          uint32)
)

OBJECT_BREAKABLE = (
    ('breakable_health',    float32),
)

CFORM = (
    ('shapes_count',    uint8),
    ('cycle',       'shapes_count', (
        ('shape_type_{}',   enum8,      fmt.SHAPE_TYPE),
        ('position_{}',     vec3,       'shape_type_{}',    lambda x: x == fmt.SHAPE_SPHERE),
        ('radius_{}',       float32,    'shape_type_{}',    lambda x: x == fmt.SHAPE_SPHERE),
        ('matrix_{}',       matrix3x4,  'shape_type_{}',    lambda x: x != fmt.SHAPE_SPHERE)
        )
    )
)

PH_SKELETON_FLAGS = (
    ('skeleton_active',         fmt.PHSkeletonFlags.ACTIVE),
    ('skeleton_spawn_copy',     fmt.PHSkeletonFlags.SPAWN_COPY),
    ('skeleton_saved_data',     fmt.PHSkeletonFlags.SAVED_DATA),
    ('skeleton_not_save',       fmt.PHSkeletonFlags.NOT_SAVE)
)

PH_SKELETON = (
    ('skeleton_startup_animation',  string),
    ('skeleton_flags',              flags8,     PH_SKELETON_FLAGS),
    ('skeleton_source_id',          uint16),
    ('skeleton_bones_mask',         uint64,     'skeleton_saved_data',      def_fun),
    ('skeleton_root_bone',          uint16,     'skeleton_saved_data',      def_fun),
    ('skeleton_linear_vel',         vec3,       'skeleton_saved_data',      def_fun),
    ('skeleton_position',           vec3,       'skeleton_saved_data',      def_fun),
    ('skeleton_quaternion',         vec4,       'skeleton_saved_data',      def_fun),
    ('skeleton_enabled',            uint8,      'skeleton_saved_data',      def_fun),
    ('skeleton_vec_min',            vec3,       'skeleton_saved_data',      def_fun),
    ('skeleton_vec_max',            vec3,       'skeleton_saved_data',      def_fun)
)

CREATURE_ABSTRACT = (
    ('team',                        uint8),
    ('squad',                       uint8),
    ('group',                       uint8),
    ('creature_health',             float32),
    ('dynamic_out_restrictions',    uint32),
    ('dynamic_in_restrictions',     uint32),
    ('killer_id',                   uint16),
    ('game_death_time',             uint64)
)

TRADER_FLAGS = (
    ('infinite_ammo',   fmt.TraderFlags.INFINITE_AMMO),
    ('dummy',           fmt.TraderFlags.DUMMY)
)

TRADER_ABSTRACT = (
    ('money',               uint32),
    ('specific_character',  string),
    ('trader_flags',        flags32,    TRADER_FLAGS),
    ('character_profile',   string),
    ('community_index',     int32),
    ('rank',                int32),
    ('reputation',          int32),
    ('character_name',      string)
)

CREATURE_ACTOR = (
    ('holder_id', uint16),
)

OBJECT_PHYSIC = (
    ('physic_type',         uint32),    ###################### разобрать
    ('physic_mass',         float32),
    ('physic_fixed_bones',  string)
)

HANGING_LAMP_FLAGS = (
    ('physic',          fmt.ALifeObjectHangingLampFlags.PHYSIC),
    ('cast_shadow',     fmt.ALifeObjectHangingLampFlags.CAST_SHADOW),
    ('r1',              fmt.ALifeObjectHangingLampFlags.R1),
    ('r2',              fmt.ALifeObjectHangingLampFlags.R2),
    ('type_spot',       fmt.ALifeObjectHangingLampFlags.TYPE_SPOT),
    ('point_ambient',   fmt.ALifeObjectHangingLampFlags.POINT_AMBIENT)
)

HANGING_LAMP = (
    ('color',                       uint32),    ###### разобрать на RGB
    ('brightness',                  float32),
    ('color_animator',              string),
    ('range',                       float32),
    ('handing_lamp_flags',          flags16,     HANGING_LAMP_FLAGS),
    ('startup_animation',           string),
    ('handing_lamp_fixed_bones',    string),
    ('handing_lamp_health',         float32),
    ('virtual_size',                float32),
    ('ambient_radius',              float32),
    ('ambient_power',               float32),
    ('ambient_texture',             string),
    ('light_texture',               string),
    ('light_main_bone',             string),
    ('spot_cone_angle',             float32),
    ('glow_texture',                string),
    ('glow_radius',                 float32),
    ('light_ambient_bone',          string)
)

SPACE_RESTRICTOR = (
    ('space_restrictor_type',  uint8),    ####### разобрать
)

LEVEL_CHANGER = (
    ('next_graph_id',           uint16),
    ('next_node_id',            uint32),
    ('next_position',           vec3),
    ('angles',                  vec3),
    ('level_to_change',         string),
    ('level_point_to_change',   string),
    ('silent_mode',             uint8)    ####### разобрать
)

MONSTER_ABSTRACT = (
    ('out_space_restrictors',   string),
    ('in_space_restrictors',    string),
    ('smart_terrain_id',        uint16),
    ('task_reached',            uint8)
)

MONSTER_BASE = (
    ('spec_object_id',  uint16),
    ('unknown',         uint16)    ####### разобрать
)

HUMAN_STALKER = (
    ('job_online',              uint8),
    ('job_online_condlist',     string,     'job_online',     lambda x: x > 2),
    ('was_in_smart_terrain',    uint8),
    ('death_droped',            uint8)
)

HUMAN_BRAIN = (
    ('equipment_preference_count', uint32),
    ('cycle',       'equipment_preference_count', (('equipment_preference_{}', uint8), )),
    ('weapon_preferences_count', uint32),
    ('cycle',       'weapon_preferences_count',   (('weapon_preferences_{}',   uint8), ))
)

HELICOPTER = (
    ('startup_animation',   string),
    ('engine_sound',        string)
)

MOTION = (
    ('motion_name', string),
)

INVENTORY_ITEM = (
    ('condition', float32),
)

CUSTOM_ZONE = (
    ('max_power',           float32),
    ('owner_id',            uint32),
    ('enabled_time',        uint32),
    ('disabled_time',       uint32),
    ('start_time_shift',    uint32)
)

ANOMALOUS_ZONE = (
    ('offline_interactive_radius',  float32),
    ('artefact_spawn_count',        uint16),
    ('artefact_position_offset',    uint32)
)

ITEM_WEAPON = (
    ('current',         uint16),
    ('elapsed',         uint16),
    ('wpn_state',       uint8),    ####### разобрать
    ('addon_flags',     uint8),    ####### разобрать
    ('ammo_type',       uint8)     ####### разобрать
)

SMART_ZONE = (
    ('table_size',      uint8),
    ('cycle',           'table_size',   (('spawned_obj_{}',  uint16), ))
)

ZONE_VISUAL = (
    ('startup_animation',   string),
    ('attack_animation',    string),
    ('zone_visual_flags',   uint8)    ####### разобрать
)

ITEM_AMMO = (
    ('elapsed', uint16),
)

CAR = (
    ('car_health', float32),
)

SMART_TERRAIN = (
    ('duration_end',    ctime),
    ('idle_end',        ctime)
)

ZONE_ANOM = (
    ('anom_flags',          uint8),    ####### разобрать
    ('last_spawn_time',     ctime,  'anom_flags',   def_fun)
)
