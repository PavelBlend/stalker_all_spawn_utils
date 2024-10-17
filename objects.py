import read
import fmt
import net_packet
import clas


packets = {}


def read_net_packet(packets, data, classes):
    # create reader
    reader = read.Reader(data)

    # get section name
    reader.offset = 4
    section_name = reader.string()
    reader.offset = 0

    # get packet
    clas_name = classes.get(section_name, None)
    packet = clas.net_packet_by_class.get(clas_name, None)

    # read packet
    p = packet(reader)

    obj_name = None
    for name, value in reader.props:
        if name == 'name':
            obj_name = value

    packets[(section_name, obj_name)] = reader


def read_object_body(packets, data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.NetPackedChunks.SPAWN:
            read_net_packet(packets, chunk_data, classes)

        elif chunk_id == fmt.NetPackedChunks.UPDATE:
            # read_net_packet(chunk_data, classes)
            pass

        else:
            raise BaseException('read_object_body chunk')


def read_object_id(data):
    reader = read.Reader(data)
    object_id = reader.uint16()


def read_spawn_object(packets, data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnObjectChunks.OBJECT_ID:
            read_object_id(chunk_data)

        elif chunk_id == fmt.SpawnObjectChunks.OBJECT_BODY:
            read_object_body(packets, chunk_data, classes)

        else:
            raise BaseException('read_spawn_object chunk')


def read_spawn_objects(packets, data, classes):
    chunks = read.Chunks(data)

    for object_id, object_data in chunks:
        read_spawn_object(packets, object_data, classes)


def read_objects_count(data):
    reader = read.Reader(data)
    objects_count = reader.uint32()


def read_objects(packets, data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnObjectsChunks.COUNT:
            read_objects_count(chunk_data)

        elif chunk_id == fmt.SpawnObjectsChunks.OBJECTS:
            read_spawn_objects(packets, chunk_data, classes)

        elif chunk_id == fmt.SpawnObjectsChunks.UNKNOWN:
            pass

        else:
            raise BaseException('read_objects chunk')
