import read


def read_level_points(data):
    # read artefact spawn positions

    reader = read.Reader(data)
    point_count = reader.uint32()

    for point_index in range(point_count):
        pos_x, pos_y, pos_z     = reader.vec3()
        level_vertex_id         = reader.uint32()
        distance                = reader.float32()
