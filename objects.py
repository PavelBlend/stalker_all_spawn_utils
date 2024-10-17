import read
import fmt
import net_packet
import clas


def read_net_packet(data, classes):
    reader = read.Reader(data)

    reader.offset = 4
    section_name = reader.string()
    reader.offset = 0

    clas_name = classes.get(section_name, None)
    packet = clas.net_packet_by_class.get(clas_name, None)

    try:
        print('\n'*10)
        print(packet)
        packet(reader)
        print('\n'*10)

        if len(reader.data) != reader.offset:
            print(reader.offset, len(reader.data))
            raise Exception('offset')

    except:
        print(packet)
        print(clas_name)
        print(section_name)
        '''with open(section_name, 'wb') as file:
            file.write(data)'''
        raise Exception('stop')


def read_object_body(data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.NetPackedChunks.SPAWN:
            read_net_packet(chunk_data, classes)

        elif chunk_id == fmt.NetPackedChunks.UPDATE:
            # read_net_packet(chunk_data, classes)
            pass

        else:
            raise BaseException('read_object_body chunk')


def read_object_id(data):
    reader = read.Reader(data)
    object_id = reader.uint16()


def read_spawn_object(data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnObjectChunks.OBJECT_ID:
            read_object_id(chunk_data)

        elif chunk_id == fmt.SpawnObjectChunks.OBJECT_BODY:
            read_object_body(chunk_data, classes)

        else:
            raise BaseException('read_spawn_object chunk')


def read_spawn_objects(data, classes):
    chunks = read.Chunks(data)

    for object_id, object_data in chunks:
        read_spawn_object(object_data, classes)


def read_objects_count(data):
    reader = read.Reader(data)
    objects_count = reader.uint32()


def read_objects(data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnObjectsChunks.COUNT:
            read_objects_count(chunk_data)

        elif chunk_id == fmt.SpawnObjectsChunks.OBJECTS:
            read_spawn_objects(chunk_data, classes)

        elif chunk_id == fmt.SpawnObjectsChunks.UNKNOWN:
            pass

        else:
            raise BaseException('read_objects chunk')
