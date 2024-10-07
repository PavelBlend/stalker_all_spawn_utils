import fmt


def _read_cform(self):
    print('_read_cform')

    shapes_count = self.reader.uint8()
    print('shapes_count = {}'.format(shapes_count))

    for shape_index in range(shapes_count):
        shape_type = self.reader.uint8()
        print('shape_type = {}'.format(shape_type))

        if shape_type == 0:    # sphere
            position = self.reader.vec3()
            radius = self.reader.float32()

        else:    # box
            matrix = self.reader.matrix3x4()
            print('matrix = {}'.format(list(map(lambda x: '{:.2f}'.format(x), matrix))))

    print(len(self.reader.data), self.reader.offset)


class CSE_Abstract:
    def __init__(self, reader):
        self.reader = reader
        self._read()

    def _read(self):
        print('Base')

        net_packet_size = self.reader.uint16()
        print('net_packet_size = {}'.format(net_packet_size))

        state = self.reader.uint16()
        print('state = {}'.format(state))

        if state == fmt.SpawnStates.UPDATE:
            self._read_update()

        elif state == fmt.SpawnStates.SPAWN:
            self._read_state()

        else:
            print('Unknown NET Packet state')

    def _read_update(self):
        self.section_name = 'UPDATE'

    def _read_state(self):
        print('CSE_Abstract')

        self.section_name = self.reader.string()
        print('section_name = {}'.format(self.section_name))

        self.name = self.reader.string()
        print('name = {}'.format(self.name))

        game_type = self.reader.uint8()    # GameID in fmt
        print('game_type = {}'.format(game_type))

        rp = self.reader.uint8()    # use supplied coords
        print('rp = {}'.format(rp))

        position = self.reader.vec3()
        print('position = {:.3f}, {:.3f}, {:.3f}'.format(*position))

        direction = self.reader.vec3()
        print('direction = {:.3f}, {:.3f}, {:.3f}'.format(*direction))

        respawn_time = self.reader.uint16()
        print('respawn_time = {}'.format(respawn_time))

        object_id = self.reader.uint16()
        print('object_id = {}'.format(object_id))

        id_parent = self.reader.uint16()
        print('id_parent = {}'.format(id_parent))

        id_phantom = self.reader.uint16()
        print('id_phantom = {}'.format(id_phantom)) 

        flags = self.reader.uint16()
        print('flags = {}'.format(flags))

        obj_local = flags & fmt.SpawnFlags.OBJECT_LOCAL
        obj_upd = flags & fmt.SpawnFlags.OBJECT_HAS_UPDATE
        obj_as_player = flags & fmt.SpawnFlags.OBJECT_AS_PLAYER
        obj_phantom = flags & fmt.SpawnFlags.OBJECT_PHANTOM
        check_ver = flags & fmt.SpawnFlags.VERSION
        update_packet = flags & fmt.SpawnFlags.UPDATE
        spawn_time = flags & fmt.SpawnFlags.TIME

        if check_ver:
            version = self.reader.uint16()
            print('version = {}'.format(version))

        script_version = self.reader.uint16()
        print('script_version = {}'.format(script_version))

        client_data_size = self.reader.uint16()
        print('client_data_size = {}'.format(client_data_size))

        client_data = self.reader.get_bytes(client_data_size)
        print('client_data = {}'.format(client_data))

        spawn_id = self.reader.uint16()
        print('spawn_id = {}'.format(spawn_id))

        size = self.reader.uint16()
        print('size = {}'.format(size))

        print(len(self.reader.data), self.reader.offset)


def read_alife_object(self):
    print('CSE_ALifeObject')

    graph_id = self.reader.uint16()
    print('graph_id = {}'.format(graph_id))

    distance = self.reader.float32()
    print('distance = {:.3f}'.format(distance))

    direct_control = self.reader.uint32()
    print('direct_control = {}'.format(direct_control))

    node_id = self.reader.uint32()
    print('node_id = {}'.format(node_id))

    flags = self.reader.uint32()
    print('flags = {}'.format(flags))

    ini_string = self.reader.string()
    print('ini_string = "{}"'.format(ini_string))

    story_id = self.reader.uint32()
    print('story_id = {}'.format(story_id))

    spawn_story_id = self.reader.uint32()
    print('spawn_story_id = {}'.format(spawn_story_id))

    print(len(self.reader.data), self.reader.offset)


class CSE_ALifeObject(CSE_Abstract):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_Abstract._read_state(self)
        read_alife_object(self)


class CSE_ALifeDynamicObject(CSE_ALifeObject):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeObject._read_state(self)

        print('CSE_ALifeDynamicObject')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeSpaceRestrictor(CSE_ALifeDynamicObject):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObject._read_state(self)

        _read_cform(self)

        print('CSE_ALifeSpaceRestrictor')

        space_restrictor_type = self.reader.uint8()
        print('space_restrictor_type = {}'.format(space_restrictor_type))

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


class CSE_Visual:
    def read_visual(self):
        print('CSE_Visual')

        visual_name = self.reader.string()
        print('visual_name = "{}"'.format(visual_name))

        flags = self.reader.uint8()
        print('flags = {}'.format(flags))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeDynamicObjectVisual(CSE_ALifeDynamicObject, CSE_Visual):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObject._read_state(self)
        CSE_Visual.read_visual(self)

        print('CSE_ALifeDynamicObjectVisual')

        print(len(self.reader.data), self.reader.offset)


class CSE_PHSkeleton:

    def _read_update(self):
        pass

    def _read_state(self):
        print('CSE_PHSkeleton')

        startup_animation = self.reader.string()
        print('startup_animation = "{}"'.format(startup_animation))

        flags = self.reader.uint8()
        print('flags = {}'.format(flags))

        source_id = self.reader.uint16()
        print('source_id = {}'.format(source_id))

        if flags & fmt.SkeletonFlags.SavedData:

            # bones data
            bones_mask = self.reader.uint64()
            print('bones_mask = {}'.format(bones_mask))

            root_bone = self.reader.uint16()
            print('root_bone = {}'.format(root_bone))

            linear_vel = self.reader.vec3()
            print('linear_vel = {}'.format(linear_vel))

            position = self.reader.vec3()
            print('position = {}'.format(position))

            quaternion = self.reader.vec4()
            print('quaternion = {}'.format(quaternion))

            enabled = self.reader.uint8()
            print('enabled = {}'.format(enabled))

            vec_min = self.reader.vec3()
            print('vec_min = {}'.format(vec_min))

            vec_max = self.reader.vec3()
            print('vec_max = {}'.format(vec_max))

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


class CSE_ALifeCreatureAbstract(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)

        print('CSE_ALifeCreatureAbstract')

        team = self.reader.uint8()
        print('team = {}'.format(team))

        squad = self.reader.uint8()
        print('squad = {}'.format(squad))

        group = self.reader.uint8()
        print('group = {}'.format(group))

        health = self.reader.float32()
        print('health = {:.3f}'.format(health))

        dynamic_out_restrictions = self.reader.uint32()
        print('dynamic_out_restrictions = {}'.format(dynamic_out_restrictions))

        dynamic_in_restrictions = self.reader.uint32()
        print('dynamic_in_restrictions = {}'.format(dynamic_in_restrictions))

        killer_id = self.reader.uint16()
        print('killer_id = {}'.format(killer_id))

        game_death_time = self.reader.uint64()
        print('game_death_time = {}'.format(game_death_time))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeTraderAbstract:
    def _read_update(self):
        pass

    def _read_state(self):
        print('CSE_ALifeTraderAbstract')

        money = self.reader.uint32()
        print('money = {}'.format(money))

        specific_character = self.reader.string()
        print('specific_character = "{}"'.format(specific_character))

        trader_flags = self.reader.uint32()
        print('trader_flags = {}'.format(trader_flags))

        character_profile = self.reader.string()
        print('character_profile = "{}"'.format(character_profile))

        community_index = self.reader.int32()
        print('community_index = {}'.format(community_index))

        rank = self.reader.int32()
        print('rank = {}'.format(rank))

        reputation = self.reader.int32()
        print('reputation = {}'.format(reputation))

        character_name = self.reader.string()
        print('character_name = "{}"'.format(character_name))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeCreatureActor(CSE_ALifeCreatureAbstract, CSE_ALifeTraderAbstract, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeCreatureAbstract._read_state(self)
        CSE_ALifeTraderAbstract._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeCreatureActor')

        holder_id = self.reader.uint16()
        print('holder_id = {}'.format(holder_id))

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


class CSE_ALifeMonsterAbstract(CSE_ALifeCreatureAbstract, CSE_ALifeSchedulable):
    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeCreatureAbstract._read_state(self)

        print('CSE_ALifeMonsterAbstract')

        out_space_restrictors = self.reader.string()
        print('out_space_restrictors = "{}"'.format(out_space_restrictors))

        in_space_restrictors = self.reader.string()
        print('in_space_restrictors = "{}"'.format(in_space_restrictors))

        smart_terrain_id = self.reader.uint16()
        print('smart_terrain_id = {}'.format(smart_terrain_id))

        task_reached = self.reader.uint16()
        print('task_reached = {}'.format(task_reached))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeHumanAbstract(CSE_ALifeTraderAbstract, CSE_ALifeMonsterAbstract):
    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeTraderAbstract._read_state(self)
        read_alife_object(self)

        print('CSE_ALifeHumanAbstract')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeHumanStalker(CSE_ALifeHumanAbstract, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_Abstract._read_state(self)
        CSE_ALifeHumanAbstract._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeHumanStalker')

        print(len(self.reader.data), self.reader.offset)


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


class CSE_ALifeMonsterBase(CSE_ALifeMonsterAbstract, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeMonsterAbstract._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeMonsterBase')

        spec_object_id = self.reader.uint16()
        print('spec_object_id = {}'.format(spec_object_id))

        unknown = self.reader.uint16()
        print('unknown = {}'.format(unknown))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeMountedWeapon(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)

        print('CSE_ALifeMountedWeapon')

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeObjectBreakable(CSE_ALifeDynamicObjectVisual):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)

        print('CSE_ALifeObjectBreakable')

        health = self.reader.float32()
        print('health = {:.3f}'.format(health))

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


class CSE_ALifeObjectHangingLamp(CSE_ALifeDynamicObjectVisual, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeObjectHangingLamp')

        color = self.reader.uint32()
        print('color = {}'.format(color))

        brightness = self.reader.float32()
        print('brightness = {:.3f}'.format(brightness))

        color_animator = self.reader.string()
        print('color_animator = "{}"'.format(color_animator))

        range_ = self.reader.float32()
        print('range = {:.3f}'.format(range_))

        flags = self.reader.uint16()
        print('flags = {}'.format(flags))

        startup_animation = self.reader.string()
        print('startup_animation = "{}"'.format(startup_animation))

        fixed_bones = self.reader.string()
        print('fixed_bones = "{}"'.format(fixed_bones))

        health = self.reader.float32()
        print('health = {:.3f}'.format(health))

        virtual_size = self.reader.float32()
        print('virtual_size = {:.3f}'.format(virtual_size))

        ambient_radius = self.reader.float32()
        print('ambient_radius = {:.3f}'.format(ambient_radius))

        ambient_power = self.reader.float32()
        print('ambient_power = {:.3f}'.format(ambient_power))

        ambient_texture = self.reader.string()
        print('ambient_texture = "{}"'.format(ambient_texture))

        light_texture = self.reader.string()
        print('light_texture = "{}"'.format(light_texture))

        light_main_bone = self.reader.string()
        print('light_main_bone = "{}"'.format(light_main_bone))

        spot_cone_angle = self.reader.float32()
        print('spot_cone_angle = {:.3f}'.format(spot_cone_angle))

        glow_texture = self.reader.string()
        print('glow_texture = "{}"'.format(glow_texture))

        glow_radius = self.reader.float32()
        print('glow_radius = {:.3f}'.format(glow_radius))

        light_ambient_bone = self.reader.string()
        print('light_ambient_bone = "{}"'.format(light_ambient_bone))

        print(len(self.reader.data), self.reader.offset)


class CSE_ALifeObjectPhysic(CSE_ALifeDynamicObjectVisual, CSE_PHSkeleton):

    def _read_update(self):
        pass

    def _read_state(self):
        CSE_ALifeDynamicObjectVisual._read_state(self)
        CSE_PHSkeleton._read_state(self)

        print('CSE_ALifeObjectPhysic')

        type_ = self.reader.uint32()
        print('type = {}'.format(type_))

        mass = self.reader.float32()
        print('mass = {}'.format(mass))

        fixed_bones = self.reader.string()
        print('fixed_bones = "{}"'.format(fixed_bones))

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
