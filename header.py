import read
import fmt


def read_header(data):
    reader = read.Reader(data)

    xr_ai_version = reader.uint32()

    if xr_ai_version != fmt.XR_AI_VERSION:
        raise BaseException('unsupported xr_ai_version: {}'.format(xr_ai_version))

    reader.skip(16)    # guid
    reader.skip(16)    # graph_guid

    spawn_count = reader.uint32()
    level_count = reader.uint32()
