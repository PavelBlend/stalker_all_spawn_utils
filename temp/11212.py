with open('1.cpp', 'r') as file:
    lines = file.readlines()

classes = set()

for i in lines:

    if i[0] == '#':
        line = '    {}'.format(i)

    elif i == '\n':
        line = i

    else:
        clas, sect, _ = i.split("'")
        line = "    '{}': net_packet.{},\n".format(sect, clas)

        print(line, end='')
        classes.add(
            'class {}(CSE_Abstract):\n\n    def _read_update(self):\n        pass\n\n' \
            '    def _read_state(self):\n        pass\n\n'.format(clas)
        )

for c in sorted(classes):
    print(c)

input('ok')
