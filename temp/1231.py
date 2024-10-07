with open('2.cpp', 'r') as file:
    lines = file.readlines()

classes_ids = {}

for line in lines:
    if 'CLSID_' in line and 'define' in line:
        line = line[0 : -1]
        line = line.replace('\t', ' ')
        parts = line.split(' ')
        classes = []
        for part in parts:
            if part == '#define':
                continue
            if not part:
                continue
            classes.append(part)
        classes_ids[classes[0]] = classes[1]

all_code = ''.join(lines)
for src, replace in classes_ids.items():
    all_code = all_code.replace(src, replace)

all_code = all_code.replace('\t', ' ')
all_code = all_code.replace('TEXT2CLSID(', '')

for line in all_code.splitlines():
    if 'ADD' in line:
        parts = line.split('(')[1]
        parts = parts.split(',')
        net_packet = parts[1].replace(' ', '')
        cls = parts[2].replace(' ', '').replace(')', '').replace('"', '')
        print('    {1: <24}:    net_packet.{0},'.format(net_packet, '\''+cls+'\''))

input('ok')
