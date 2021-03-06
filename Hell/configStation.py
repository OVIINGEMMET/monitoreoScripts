#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

FILEPATHNAME = os.path.dirname(sys.argv[0])
FILEFULLPATH = os.path.abspath(FILEPATHNAME)


def init(configFile=''):
    DATA = {'STATION': []}
    isCamera = False
    itemCamera = {}

    if configFile == '':
        configFile = 'configFile.ini'

    print('Loading... ' + configFile)

    try:
        f = open(FILEFULLPATH + '/' + configFile, 'r')
    except:
        print('El archivo de configuracion [' + configFile + '] no existe!!')
        sys.exit(1)

    content = f.read().splitlines()
    for idx, line in enumerate(content):
        # print idx, line
        line = line

        if line == '<<STATION':
            itemCamera = {}
            isCamera = True
        elif line == '>>' and isCamera is True:
            isCamera = False
            DATA['STATION'].append(itemCamera)
        elif isCamera is True:
            dato = line.split(':=')
            key = dato[0].strip()
            value = dato[1].strip()

            if value == 'None':
                auxDato = None
            elif value == 'True':
                auxDato = True
            elif value == 'False':
                auxDato = False
            elif key.startswith('restrict'):
                restrict = value.split('|')
                result = []
                for rest in restrict:
                    result.append(rest.split('-'))
                auxDato = result
            else:
                auxDato = value.strip()

            itemCamera[key] = auxDato

        # elif idx >= 0:  # and idx <=3
        #     dato = line.split(':=')
        #     DATA[dato[0]] = specialValue(dato[1].strip())

        else:
            pass

    return DATA


def specialValue(value):
    if value == 'None':
        auxDato = None
    elif value == 'True':
        auxDato = True
    elif value == 'False':
        auxDato = False
    else:
        auxDato = value.strip()

    return auxDato
