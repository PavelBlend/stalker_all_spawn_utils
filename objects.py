import fmt
import clas
import read
import debug
import net_packet


def read_net_packet(data, classes, file_offset):
    # create reader
    reader = read.Reader(data, file_offs=file_offset)

    # get section name and object name
    reader.offset = 4
    section_name = reader.string()
    obj_name = reader.string()
    reader.offset = 0
    reader.file_offs = file_offset

    # get packet
    clas_name = classes.get(section_name, None)
    props = clas.net_packet_by_class.get(clas_name, None)

    # read packet
    net_packet.NetPacket(reader, props, clas_name)

    debug.print_objects_info(reader)

    return section_name, obj_name, reader


def read_object_body(data, classes, file_offset):
    sect = None
    obj = None
    packet = None

    chunks = read.Chunks(data, file_offs=file_offset)

    for chunk_id, chunk_data in chunks:
        chunk_offset, data_offset = chunks.get_offs()

        if chunk_id == fmt.NetPackedChunks.SPAWN:
            sect, obj, packet = read_net_packet(chunk_data, classes, data_offset)

        elif chunk_id == fmt.NetPackedChunks.UPDATE:
            # read_net_packet(chunk_data, classes)
            pass

        else:
            raise BaseException('read_object_body chunk')

    return sect, obj, packet


def read_object_id(data):
    reader = read.Reader(data)
    object_id = reader.uint16()
    return object_id


def read_spawn_object(packets, data, classes, file_offset):
    chunks = read.Chunks(data, file_offs=file_offset)

    for chunk_id, chunk_data in chunks:
        chunk_offset, data_offset = chunks.get_offs()

        if chunk_id == fmt.SpawnObjectChunks.OBJECT_ID:
            obj_id = read_object_id(chunk_data)

        elif chunk_id == fmt.SpawnObjectChunks.OBJECT_BODY:
            sect, obj, packet = read_object_body(chunk_data, classes, data_offset)

        else:
            raise BaseException('read_spawn_object chunk')

    packets.append((obj_id, sect, obj, packet))


def read_spawn_objects(packets, data, classes, file_offset):
    chunks = read.Chunks(data, file_offs=file_offset)

    for object_id, object_data in chunks:
        chunk_offset, data_offset = chunks.get_offs()
        read_spawn_object(packets, object_data, classes, data_offset)


def read_spawn_edges(packets, data):
    reader = read.Reader(data)

    while reader.offset < len(data):

        object_1_id         = reader.uint32()
        edges_count         = reader.uint32()

        for i in range(edges_count):
            object_2_id = reader.uint32()
            edge_weight = reader.float32()


def read_objects_count(data):
    reader = read.Reader(data)
    objects_count = reader.uint32()


def read_objects(packets, data, classes, file_offset):
    chunks = read.Chunks(data, file_offs=file_offset)

    for chunk_id, chunk_data in chunks:

        chunk_offset, data_offset = chunks.get_offs()

        if chunk_id == fmt.SpawnObjectsChunks.COUNT:
            read_objects_count(chunk_data)

        elif chunk_id == fmt.SpawnObjectsChunks.OBJECTS:
            read_spawn_objects(packets, chunk_data, classes, data_offset)

        elif chunk_id == fmt.SpawnObjectsChunks.EDGES:
            read_spawn_edges(packets, chunk_data)

        else:
            raise BaseException('read_objects chunk')
