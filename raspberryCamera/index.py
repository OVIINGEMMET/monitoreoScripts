#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getImage import Camera
import mapConfig
import thread
import time
import datetime
import sys, getopt
import os

SWITCH = True
# print("argv was", sys.argv)
# print("sys.executable was", sys.executable)
# print("restart now")


def help(text):
    print (text)
    print ('      index.py -h <help>')
    print ('               -c <filename config.ini in principal PATH>')
    print


# ----- VARIABLES GLOBALES ------
def main(argv):
    global SWITCH
    global DATA
    global PATH
    global PATH_LOGO
    global FONT
    global CAMERAS
    global storageCamera
    global SECONDS
    global OBJCAMERA
    # global MAX_ERROR

    global configFile

    configFile = ''

    try:
        opts, args = getopt.getopt(argv, 'hc:', ['config='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help('Help:')
            sys.exit()
        elif opt in ('-c', '--config'):
            configFile = arg

    SWITCH = True
    DATA = mapConfig.init(configFile)
    SECONDS = DATA['SECONDS']
    # MAX_ERROR = DATA['MAX_ERROR']
    PATH = DATA['ROOTPATH']
    FONT = DATA['FONT']
    CAMERAS = DATA['CAMERA']
    PATH_LOGO = DATA['PATH_LOGO']
    OBJCAMERA = []

# -------------------------------


def taskCamera():
    # RECORREMOS TODAS LAS CAMARAS REGISTRADAS
    for idx, cam in enumerate(CAMERAS):
        if cam['enable']:
            # INICIAMOS EL OBJETO
            a = Camera()
            # SETEAMOS PARAMETROS
            cam['id'] = idx
            cam['GLOBALPATH'] = PATH
            cam['SWITCH'] = True
            cam['EXEC'] = [sys.executable, ['python'] + sys.argv]
            if cam['type'] == 'camera':
                cam['FONT'] = FONT
                cam['PATH_LOGO'] = PATH_LOGO
                a.setParameters(cam)
            elif cam['type'] == 'sync':
                a.setSynchronizer(cam)
            elif cam['type'] == 'syncServerToLocal':
                a.setSynchronizerServerToLocal(cam)
            elif cam['type'] == 'updateImageWeb':
                a.setSyncronizerWEB(cam)
            elif cam['type'] == 'updateImageServer':
                a.setSyncronizerLocalToServer(cam)
            elif cam['type'] == 'generateScale':
                a.setGenerateScale(cam)
            # a.printParams(cam)
            # -------------------
            # DECLARAMOS LOS THREADS
            OBJCAMERA.append(a)
            thread.start_new_thread(threadTask, (a,))
            # RETARDAMOS CADA THREAD 1 SEGUNDO PARA EVITAR SOLAPAMIENTO DE HILOS
            time.sleep(1)


def threadTask(cam):
    # global SWITCH
    total_errors = 0
    while cam.SWITCH:
        # cam.countErrors = cam.countErrors + total_errors
        # MEDIMOS EL TIMEPO DE DESCARGA EN SEGUDOS
        timeInit = datetime.datetime.now()

        if cam.type == 'camera':
            cam.getImageThread()
        elif cam.type == 'sync':
            cam.synchronizeLocal()
        elif cam.type == 'syncServerToLocal':
            cam.synchronizeServerToLocal()
        elif cam.type == 'updateImageWeb':
            cam.syncUpdateImageWeb()
        elif cam.type == 'updateImageServer':
            cam.syncUpdateImageLocalToServer()
        elif cam.type == 'generateScale':
            cam.generetaScale()
        # cam.sendFTP()
        timeEnd = datetime.datetime.now()
        duration = timeEnd - timeInit
        totalSeconds = duration.total_seconds()
        # ----------------------------------------

        # OBTENEMOS EL TIEMPO DE LA CAMARA
        secondsLocal = float(cam.timer)
        if totalSeconds < secondsLocal:
            lapso = secondsLocal - totalSeconds
        else:
            lapso = 0

        cam.printColor('waiting ' + str(lapso) + ' seconds...')

        if SECONDS is not None:

            # SI EL TIEMPO DE DESCARGA ES MENOR AL TIEMPO CONFIGURDO EN LA CAMARA
            # SE INICIA UN RETRASO CON EL TIEMPO FALTANTE
            # PARA QUE LA PETICION DE CADA IMAGEN SE REALICE EN EL TIEMPO SOLICITADO
            time.sleep(lapso)
        else:
            cam.SWITCH = False


if __name__ == "__main__":
    main(sys.argv[1:])
    # SE INICIA LA TAREA
    taskCamera()

    # SE REQUIERE PARA QUE LOS THREADS FUNCIONEN
    while 1:
        cen = False
        # error_total = 0
        for idx, cam in enumerate(OBJCAMERA):
            cen = cen or cam.SWITCH
            # error_total = error_total + cam.totalCountErrors

        if cen is True:
            # if error_total >= int(MAX_ERROR):
            #     time.sleep(1)
            #     print('Reboot Now... [ERRORS ' + str(error_total) + '/' + str(MAX_ERROR) + ']')
            #     # time.sleep(5)
            #     os.execv(sys.executable, ['python'] + sys.argv)
            # else:
            #     pass
            pass
        else:
            sys.exit(1)
