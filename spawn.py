import read
import utils
import header
import objects
import level_points
import fmt
import config


def parse_spawn_body(packets, data, classes):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnChunks.HEADER:
            header.read_header(chunk_data)

        elif chunk_id == fmt.SpawnChunks.SPAWN_OBJECTS:
            objects.read_objects(packets, chunk_data, classes)

        elif chunk_id == fmt.SpawnChunks.LEVEL_POINTS:
            level_points.read_level_points(chunk_data)

        elif chunk_id == fmt.SpawnChunks.WAY_POINTS:
            pass

        else:
            print('unknown main chunk: {}'.format(chunk_id))


def parse_spawn(packets, file_path):
    classes = config.scan_configs()

    spawn_data = utils.read_file(file_path)
    parse_spawn_body(packets, spawn_data, classes)


file_path = 'D:\\E\\soc\\gamedata_unpack\\spawns\\all.spawn'
packets = {}
parse_spawn(packets, file_path)
