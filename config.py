import os
import ltx


configs_path = 'D:\\E\\soc\\gamedata_unpack\\config\\'
EXT_LTX = os.extsep + 'ltx'


def scan_params(sect, classes, sections):
    if sect.parent:
        parent = sections.get(sect.parent, None)
        while parent:
            sect.params.update(parent.params)
            parent = sections.get(parent.parent, None)

    cls = sect.params.get('class', None)
    if cls:
        classes[sect.name] = cls


def scan_config(sections, classes):
    for sect_name, sect in sections.items():
        scan_params(sect, classes, sections)


def scan_configs():
    sections = {}

    for root, dirs, files in os.walk(configs_path):
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext == EXT_LTX:

                ltx_path = os.path.join(root, file)
                ltx_parser = ltx.LtxParser()
                ltx_parser.from_file(ltx_path)

                for sect_name, sect in ltx_parser.sections.items():
                    avaible_sect = sections.get(sect_name, None)
                    if avaible_sect:
                        avaible_sect.params.update(sect.params)
                    else:
                        sections[sect_name] = sect

    classes = {}
    scan_config(sections, classes)

    return classes
