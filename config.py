#!/usr/bin/python
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()

    filename = 'C:/WorkSpace/Renault/R_AE/OSM_Data_Generation/Xml_Convertor/database.ini'
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

    