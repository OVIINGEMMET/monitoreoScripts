#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getImage import Camera
import mapConfig
import thread
import time
import datetime
import sys, getopt

SWITCH = True


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

    global configFile

    configFile = ''

    try:
        opts, args = getopt.getopt(argv, 'c:', ['config='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-c', '--config'):
            configFile = arg

    SWITCH = True
    DATA = mapConfig.init(configFile)
    SECONDS = DATA['SECONDS']
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

            if cam['type'] == 'camera':
                cam['FONT'] = FONT
                cam['PATH_LOGO'] = PATH_LOGO
                a.setParameters(cam)
            elif cam['type'] == 'sync':
                a.setSynchronizer(cam)
            elif cam['type'] == 'syncWeb':
                a.setSyncronizerWEB(cam)
            elif cam['type'] == 'syncLocal':
                a.setSyncronizerLocal(cam)
            # a.printParams(cam)
            # -------------------
            # DECLARAMOS LOS THREADS
            OBJCAMERA.append(a)
            thread.start_new_thread(threadTask, (a,))
            # RETARDAMOS CADA THREAD 1 SEGUNDO PARA EVITAR SOLAPAMIENTO DE HILOS
            time.sleep(1)


def threadTask(cam):
    # global SWITCH
    while cam.SWITCH:
        # MEDIMOS EL TIMEPO DE DESCARGA EN SEGUDOS
        timeInit = datetime.datetime.now()

        if cam.type == 'camera':
            cam.getImageThread()
        elif cam.type == 'sync':
            cam.synchronizeLocal()
        elif cam.type == 'syncWeb':
            cam.syncUpdateImageWeb()
        elif cam.type == 'syncLocal':
            cam.syncUpdateImageLocal()
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
        # pass
        cen = False
        for idx, cam in enumerate(OBJCAMERA):
            # print cam.cameraName
            cen = cen or cam.SWITCH

        if cen is True:
            pass
        else:
            sys.exit(1)
