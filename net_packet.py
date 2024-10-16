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
string = 'string'
get_bytes = 'get_bytes'


class NetPacket:
    def __init__(self, reader):
        self.reader = reader
        self.props = []
        self.read()
        self.debug()

    def read(self):
        raise NotImplementedError

    def get(self, name, fmt, *args):
        read_fun = getattr(self.reader, fmt, None)
        value = read_fun(*args)
        self.props.append([name, value])
        return value

    def debug(self):
        print('-'*79)
        print(self.__class__.__name__)
        print()
        for name, value in self.props:
            print('{0} = {1}'.format(name, value))
        print()
        print(len(self.reader.data), self.reader.offset)
        print('-'*79)
        print('\n'*3)


class Base(NetPacket):

    def read(self):
        self.get('net_packet_size', uint16)
        self.get('state', uint16)


class CSE_Abstract(NetPacket):

    def read(self):

        self.section_name   = self.get('section_name', string)
        self.name           = self.get('name',         string)

        self.get            ('game_type',           uint8)    # GameID in fmt
        self.get            ('rp',                  uint8)    # use supplied coords
        self.get            ('position',            vec3)
        self.get            ('direction',           vec3)
        self.get            ('respawn_time',        uint16)
        self.get            ('object_id',           uint16)
        self.get            ('id_parent',           uint16)
        self.get            ('id_phantom',          uint16)
        flags = self.get    ('flags',               uint16)

        obj_local       = flags & fmt.SpawnFlags.OBJECT_LOCAL
        obj_upd         = flags & fmt.SpawnFlags.OBJECT_HAS_UPDATE
        obj_as_player   = flags & fmt.SpawnFlags.OBJECT_AS_PLAYER
        obj_phantom     = flags & fmt.SpawnFlags.OBJECT_PHANTOM
        check_ver       = flags & fmt.SpawnFlags.VERSION
        update_packet   = flags & fmt.SpawnFlags.UPDATE
        spawn_time      = flags & fmt.SpawnFlags.TIME

        if check_ver:
            self.get('version', uint16)

        self.get        ('script_version',      uint16)
        sz = self.get   ('client_data_size',    uint16)
        self.get        ('client_data',         get_bytes, sz)
        self.get        ('spawn_id',            uint16)
        self.get        ('size',                uint16)


class CSE_Visual(NetPacket):

    def read(self):
        self.get('visual_name', string)
        self.get('flags',       uint8)


class CSE_ALifeObject(NetPacket):

    def read(self):
        self.get('graph_id',        uint16)
        self.get('distance',        float32)
        self.get('direct_control',  uint32)
        self.get('node_id',         uint32)
        self.get('flags',           uint32)
        self.get('ini_string',      string)
        self.get('story_id',        uint32)
        self.get('spawn_story_id',  uint32)


class CSE_ALifeObjectBreakable(NetPacket):

    def read(self):
        self.get('health', float32)


class CForm(NetPacket):

    def read(self):
        shapes_count = self.get('shapes_count', uint8)

        for shape_index in range(shapes_count):
            shape_type = self.get('shape_type', uint8)

            if shape_type == 0:    # sphere
                self.get('position',    vec3)
                self.get('radius',      float32)

            else:    # box
                self.get('matrix', matrix3x4)


class CSE_PHSkeleton(NetPacket):

    def read(self):
        self.get            ('startup_animation',   string)
        flags = self.get    ('flags',               uint8)
        self.get            ('source_id',           uint16)

        if flags & fmt.SkeletonFlags.SavedData:

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
        self.get('flags',               uint16)
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



class CSE_ALifeMonsterAbstract(NetPacket):

    def read(self):
        self.get('out_space_restrictors',   string)
        self.get('in_space_restrictors',    string)
        self.get('smart_terrain_id',        uint16)
        self.get('task_reached',            uint16)


class CSE_ALifeMonsterBase(NetPacket):

    def read(self):
        self.get('spec_object_id',  uint16)
        self.get('unknown',         uint16)


class CALifeHumanBrain(NetPacket):

    def read(self):
        item_count = self.get('item_count', uint8)
        for i in range(item_count):
            self.get('preferences_{}'.format(i), uint8)


def _read_cform(self):
    CForm(self.reader)


def cse_alife_object_breakable(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_ALifeObjectBreakable(reader)


def cse_alife_object_climable(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CForm(reader)


def cse_alife_creature_actor(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_ALifeCreatureAbstract(reader)
    CSE_ALifeTraderAbstract(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeCreatureActor(reader)


def cse_alife_object_physic(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeObjectPhysic(reader)


def cse_alife_object_hanging_lamp(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_PHSkeleton(reader)
    CSE_ALifeObjectHangingLamp(reader)


def cse_alife_trader(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_ALifeTraderAbstract(reader)


def cse_alife_space_restrictor(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CForm(reader)
    CSE_ALifeSpaceRestrictor(reader)


def cse_alife_monster_base(reader):
    Base(reader)
    CSE_Abstract(reader)
    CSE_ALifeObject(reader)
    CSE_Visual(reader)
    CSE_ALifeCreatureAbstract(reader)
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
    reader.offset += 16
    CSE_PHSkeleton(reader)
    CALifeHumanBrain(reader)


class CSE_ALifeDynamicObject(CSE_ALifeObject):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeObject._read_state(self)

        print('CSE_ALifeDynamicObject')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeCustomZone(CSE_ALifeSpaceRestrictor):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeSpaceRestrictor._read_state(self)

        print('CSE_ALifeCustomZone')

        max_power = self.reader.float32()
        print('max_power = {:.3f}'.format(max_power))

        owner_id = self.reader.uint32()
        print('owner_id = {}'.format(owner_id))

        enabled_time = self.reader.uint32()
        print('enabled_time = {}'.format(enabled_time))

        disabled_time = self.reader.uint32()
        print('disabled_time = {}'.format(disabled_time))

        start_time_shift = self.reader.uint32()
        print('start_time_shift = {}'.format(start_time_shift))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeAnomalousZone(CSE_ALifeCustomZone):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeCustomZone._read_state(self)

        print('CSE_ALifeAnomalousZone')

        offline_interactive_radius = self.reader.float32()
        print('offline_interactive_radius = {:.3f}'.format(offline_interactive_radius))

        artefact_spawn_count = self.reader.uint16()
        print('artefact_spawn_count = {}'.format(artefact_spawn_count))

        artefact_position_offset = self.reader.uint32()
        print('artefact_position_offset = {}'.format(artefact_position_offset))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeDynamicObjectVisual(CSE_ALifeDynamicObject, CSE_Visual):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObject._read_state(self)
        CSE_Visual.read_visual(self)

        print('CSE_ALifeDynamicObjectVisual')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeCar(CSE_ALifeDynamicObjectVisual, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeCar')

        health = self.reader.float32()
        print('health = {:.3f}'.format(health))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeCreatureCrow(CSE_ALifeCreatureAbstract):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeCreatureAbstract._read_state(self)

        print('CSE_ALifeCreatureCrow')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeCreaturePhantom(CSE_ALifeCreatureAbstract):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeCreatureAbstract._read_state(self)

        print('CSE_ALifeCreaturePhantom')

        print(len(self.reader.data), self.reader.offset)


class CSE_Motion:

    def _read_update(self):
        pass

    def _read_state(self):
        pass

    def read_motion(self):
        print('CSE_Motion')

        motion_name = self.reader.string()
        print('motion_name = "{}"'.format(motion_name))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeHelicopter(CSE_ALifeDynamicObjectVisual, CSE_Motion, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_Motion.read_motion(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeHelicopter')

        startup_animation = self.reader.string()
        print('startup_animation = "{}"'.format(startup_animation))

        engine_sound = self.reader.string()
        print('engine_sound = "{}"'.format(engine_sound))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeSchedulable:
    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifeInventoryItem():

    def _read_update(self):
        pass

    def _read_state(self):
        print('CSE_ALifeInventoryItem')

        condition = self.reader.float32()
        print('condition = {}'.format(condition))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItem(CSE_ALifeDynamicObjectVisual, CSE_ALifeInventoryItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_ALifeInventoryItem._read_state(self)

        print('CSE_ALifeItem')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemAmmo(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemAmmo')

        elapsed = self.reader.uint16()
        print('elapsed = {}'.format(elapsed))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemArtefact(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemArtefact')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemBolt(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemBolt')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemCustomOutfit(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemCustomOutfit')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemDetector(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemDetector')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemDocument(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemDetector')

        doc = self.reader.string()
        print('doc = "{}"'.format(doc))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemExplosive(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemExplosive')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemGrenade(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemGrenade')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemPDA(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemGrenade')

        original_owner = self.reader.uint16()
        print('original_owner = {}'.format(original_owner))

        specific_character = self.reader.string()
        print('specific_character = "{}"'.format(specific_character))

        info_portion = self.reader.string()
        print('info_portion = "{}"'.format(info_portion))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemTorch(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemTorch')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemWeapon(CSE_ALifeItem):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItem._read_state(self)

        print('CSE_ALifeItemWeapon')

        current = self.reader.uint16()
        print('current = {}'.format(current))

        elapsed = self.reader.uint16()
        print('elapsed = {}'.format(elapsed))

        wpn_state = self.reader.uint8()
        print('wpn_state = {}'.format(wpn_state))

        addon_flags = self.reader.uint8()
        print('addon_flags = {}'.format(addon_flags))

        ammo_type = self.reader.uint8()
        print('ammo_type = {}'.format(ammo_type))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemWeaponMagazined(CSE_ALifeItemWeapon):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItemWeapon._read_state(self)

        print('CSE_ALifeItemWeaponMagazined')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemWeaponMagazinedWGL(CSE_ALifeItemWeaponMagazined):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItemWeaponMagazined._read_state(self)

        print('CSE_ALifeItemWeaponMagazinedWGL')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeItemWeaponShotGun(CSE_ALifeItemWeaponMagazined):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeItemWeaponMagazined._read_state(self)

        print('CSE_ALifeItemWeaponShotGun')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeLevelChanger(CSE_ALifeSpaceRestrictor):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeSpaceRestrictor._read_state(self)

        print('CSE_ALifeLevelChanger')

        next_graph_id = self.reader.uint16()
        print('next_graph_id = {}'.format(next_graph_id))

        next_node_id = self.reader.uint32()
        print('next_node_id = {}'.format(next_node_id))

        next_position = self.reader.vec3()
        print('next_position = {:.3f}, {:.3f}, {:.3f}'.format(*next_position))

        angles = self.reader.vec3()
        print('angles = {:.3f}, {:.3f}, {:.3f}'.format(*angles))

        level_to_change = self.reader.string()
        print('level_to_change = "{}"'.format(level_to_change))

        level_point_to_change = self.reader.string()
        print('level_point_to_change = "{}"'.format(level_point_to_change))

        silent_mode = self.reader.uint8()
        print('silent_mode = {}'.format(silent_mode))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeMountedWeapon(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)

        print('CSE_ALifeMountedWeapon')

        print(len(self.reader.data), self.reader.offset)


class CSE_Shape:

    def _read_update(self):
        pass

    def _read_state(self):
        _read_cform(self)

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeObjectClimable(CSE_Shape, CSE_ALifeDynamicObject):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObject._read_state(self)
        CSE_Shape._read_state(self)

        print('CSE_ALifeObjectClimable')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeObjectProjector(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifePHSkeletonObject(CSE_ALifeDynamicObjectVisual, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifePHSkeletonObject')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifePsyDogPhantom(CSE_ALifeMonsterBase):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifeSmartZone(CSE_ALifeSpaceRestrictor, CSE_ALifeSchedulable):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifeStationaryMgun(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifeTeamBaseZone(CSE_ALifeSpaceRestrictor):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifeTorridZone(CSE_ALifeCustomZone):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_ALifeTrader(CSE_ALifeDynamicObjectVisual, CSE_ALifeTraderAbstract):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_ALifeTraderAbstract._read_state(self)

        print('CSE_ALifeTrader')


class CSE_ALifeZoneVisual(CSE_ALifeAnomalousZone, CSE_Visual):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_InventoryBox(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        pass


class CSE_Spectator(CSE_Abstract):

    def _read_update(self):
        pass

    def _read_state(self):
        return


class CSE_Temporary(CSE_Abstract):

    def _read_update(self):
        pass

    def _read_state(self):
        node_id = self.reader.uint32()


class CSE_AbstractVisual(CSE_Abstract, CSE_Visual):

    def _read_update(self):
        pass

    def _read_state(self):
        print('CSE_AbstractVisual')

        visual_name = self.reader.string()
        flags = self.reader.uint8()
        startup_animation = self.reader.string()

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeGraphPoint(CSE_Abstract):

    def _read_update(self):
        pass

    def _read_state(self):
        print('CSE_ALifeGraphPoint')

        connection_point_name = self.reader.string()
        connection_level_name = self.reader.string()

        location_1 = self.reader.uint8()
        location_2 = self.reader.uint8()
        location_3 = self.reader.uint8()
        location_4 = self.reader.uint8()

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeGroupAbstract(CSE_Abstract):

    def _read_update(self):
        pass

    def _read_state(self):
        print('CSE_ALifeGroupAbstract')

        create_spawn_positions = self.reader.uint32()
        count = self.reader.uint16()
        # E:\disk_x\trunk\xray\xr_3da\xrGame\xrServer_Objects_ALife.cpp line: 513
        # save data

        print(len(self.reader.data), self.reader.offset)
