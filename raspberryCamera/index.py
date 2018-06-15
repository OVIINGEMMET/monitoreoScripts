#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getImage import Camera
import mapConfig
import thread
import time
import datetime

SWITCH = True


# ----- VARIABLES GLOBALES ------
def main():
    global SWITCH
    global DATA
    global PATH
    global PATH_LOGO
    global FONT
    global CAMERAS
    global storageCamera
    global SECONDS
    global OBJCAMERA

    SWITCH = True
    DATA = mapConfig.init()
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
            else:
                a.setSynchronizer(cam)
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
        else:
            cam.synchronizeLocal()
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

        cam.printColor('waiting '+ str(lapso) + ' seconds...')

        if SECONDS is not None:
            # SI EL TIEMPO DE DESCARGA ES MENOR AL TIEMPO CONFIGURDO EN LA CAMARA
            # SE INICIA UN RETRASO CON EL TIEMPO FALTANTE
            # PARA QUE LA PETICION DE CADA IMAGEN SE REALICE EN EL TIEMPO SOLICITADO
            time.sleep(lapso)
        else:
            cam.SWITCH = False


if __name__ == "__main__":
    main()
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
            exit()
