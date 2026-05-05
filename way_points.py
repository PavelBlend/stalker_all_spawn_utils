import fmt
import read


def read_way_points_count(data):
    reader = read.Reader(data)
    way_points_count = reader.uint32()


def read_way_point_name(data):
    reader = read.Reader(data)
    way_point_name = reader.string()


def read_point_count(data):
    reader = read.Reader(data)
    point_count = reader.uint32()
    return point_count


def read_point_id(data):
    reader = read.Reader(data)
    point_id = reader.uint32()


def read_point_data(data):
    reader = read.Reader(data)

    name                = reader.string()
    position            = reader.vec3()
    flags               = reader.uint32()
    level_vertex_id     = reader.uint32()
    game_vertex_id      = reader.uint16()


def read_point(data):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnPointChunks.ID:
            read_point_id(chunk_data)

        elif chunk_id == fmt.SpawnPointChunks.DATA:
            read_point_data(chunk_data)

        else:
            print('unknown waypoint chunk: {}'.format(chunk_id))


def read_points(data):
    chunks = read.Chunks(data)

    for point_id, point_data in chunks:
        read_point(point_data)


def read_links(data):

    if not data:
        return

    reader = read.Reader(data)

    while reader.offset < len(data):

        point_id        = reader.uint32()
        edge_count      = reader.uint32()

        for edge_id in range(edge_count):
            edge_1          = reader.uint16()
            edge_2          = reader.uint16()
            probability     = reader.float32()


def read_way_point_data(data):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnWayPointDataChunks.COUNT:
            read_point_count(chunk_data)

        elif chunk_id == fmt.SpawnWayPointDataChunks.POINTS:
            read_points(chunk_data)

        elif chunk_id == fmt.SpawnWayPointDataChunks.LINKS:
            read_links(chunk_data)

        else:
            print('unknown waypoint chunk: {}'.format(chunk_id))


def read_way_points_object(data):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnWayPointChunks.NAME:
            read_way_point_name(chunk_data)

        elif chunk_id == fmt.SpawnWayPointChunks.DATA:
            read_way_point_data(chunk_data)

        else:
            print('unknown waypoint chunk: {}'.format(chunk_id))


def read_way_points_objects(data):
    chunks = read.Chunks(data)

    for way_id, way_data in chunks:
        read_way_points_object(way_data)


def read_way_points(data):
    chunks = read.Chunks(data)

    for chunk_id, chunk_data in chunks:

        if chunk_id == fmt.SpawnWayPointsChunks.COUNT:
            read_way_points_count(chunk_data)

        elif chunk_id == fmt.SpawnWayPointsChunks.OBJECTS:
            read_way_points_objects(chunk_data)

        else:
            print('unknown waypoint chunk: {}'.format(chunk_id))
