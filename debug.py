import net_packet


def print_objects_info(reader):
    print(';' + '-'*78)

    for name, value, typ in reader.props:

        if typ in (net_packet.enum8, net_packet.enum16, net_packet.enum32):
            print('{0: <30} = "{1}"'.format(name, value))

        elif typ == net_packet.comment:
            if name:
                print('; {0}'.format(name))
            else:
                print()

        elif name == 'ini_string':
            value = value.replace('\r\n', '\\n ')
            print('{0: <30} = "{1}"'.format(name, value))

        elif typ == net_packet.respawn_point:
            if type(value) == str:
                print('{0: <30} = "{1}"'.format(name, value))
            else:
                print('{0: <30} = {1}'.format(name, value))

        elif typ == net_packet.string:
            print('{0: <30} = "{1}"'.format(name, value))

        elif typ == net_packet.vec3:
            print('{0: <30} = {1:.4f}, {2:.4f}, {3:.4f}'.format(name, *value))

        elif typ == net_packet.matrix3x4:
            print('{0: <30} = {1:.1f}, {2:.1f}, {3:.1f}, {4:.1f}, {5:.1f}, {6:.1f}, {7:.1f}, {8:.1f}, {9:.1f}, {10:.1f}, {11:.1f}, {12:.1f}'.format(name, *value))

        else:
            print('{0: <30} = {1}'.format(name, value))

    print('\n'*3)
