import fmt


int32       = 'int32'
uint8       = 'uint8'
uint16      = 'uint16'
uint32      = 'uint32'
uint64      = 'uint64'
float32     = 'float32'
bool8       = 'bool8'
bool32      = 'bool32'
vec3        = 'vec3'
vec4        = 'vec4'
matrix3x4   = 'matrix3x4'
flags8      = 'flags8'
flags16     = 'flags16'
flags32     = 'flags32'
enum8       = 'enum8'
enum16      = 'enum16'
enum32      = 'enum32'
string      = 'string'
ctime       = 'ctime'
get_bytes   = 'get_bytes'
comment     = 'comment'

def_fun = lambda x: bool(x)

###############################################################################


class NetPacket:

    def __init__(self, reader, props_desc, clas_name, debug=False):

        self.reader         = reader
        self.props_desc     = props_desc
        self.debug = debug

        # first comment
        reader.props.append([clas_name, None, comment])

        # read net packet properties
        self.read()

        # new line
        reader.props.append(['', None, comment])

    def read_prop(self, prop, index=None):

        name    = prop[0]
        typ     = prop[1]

        if len(prop) == 4:
            cond_name = prop[2]
            cond_fun  = prop[3]

            if index is not None:
                cond_name = cond_name.format(index)

            cond_value = self.get_readed_prop(cond_name)
            cond = cond_fun(cond_value)

            if cond:
                self.get(name, typ)

        elif typ in (flags8, flags16, flags32):
            flag_props = prop[2]
            flags_value = self.get(name, typ, append=False)

            for flag_name, flag_mask in flag_props:
                flag_value = bool(flags_value & flag_mask)
                self.append(flag_name, flag_value, typ)

        elif typ in (enum8, enum16, enum32):
            enum_names = prop[2]
            val = self.get(name, typ, append=False)
            enum_name = enum_names.get(val, None)
            if enum_name is None:
                enum_name = 'Unknown_{}'.format(val)
            self.append(name, enum_name, typ)

        elif typ == get_bytes:
            size_prop = prop[2]
            size = self.get_readed_prop(size_prop)
            offs = self.reader.offset
            data = self.reader.data[offs : offs + size]
            self.reader.skip(size)
            self.append(name, data, typ)

        elif name == 'cycle':
            iter_count_prop = self.get_readed_prop(typ)
            cycle_props = prop[2]
            for i in range(iter_count_prop):
                for cycle_prop in cycle_props:
                    prop_name = cycle_prop[0].format(i)
                    prop = list(cycle_prop)
                    prop[0] = prop_name
                    self.read_prop(prop, index=i)

        else:
            val = self.get(name, typ)

    def read(self):
        for prop in self.props_desc:
            self.read_prop(prop)

    def get_readed_prop(self, prop_name):

        result = None

        for name, value, fmt in self.reader.props:
            if name == prop_name:
                result = value

        if result is None:
            print(f'cannot find property: {prop_name}')

        return result

    def get(self, name, fmt, *args, append=True):
        read_fun = getattr(self.reader, fmt, None)
        value = read_fun(*args)
        if append:
            self.reader.props.append([name, value, fmt])
        return value

    def append(self, name, value, fmt):
        self.reader.props.append([name, value, fmt])
