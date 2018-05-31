#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getImage import Camera
import mapConfig
import thread
import time
import datetime


# ----- VARIABLES GLOBALES ------
def main():
    global SWITCH 
    global DATA
    global PATH
    global FONT
    global CAMERAS
    global storageCamera
    global SECONDS

    SWITCH = True
    DATA = mapConfig.init()
    SECONDS = DATA['SECONDS']
    PATH = DATA['ROOTPATH']
    FONT = DATA['FONT']
    CAMERAS = DATA['CAMERA']
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
            cam['FONT'] = FONT
            a.setParameters(cam)
            # -------------------
            # DECLARAMOS LOS THREADS
            thread.start_new_thread(threadTask, (a,))
            # RETARDAMOS CADA THREAD 1 SEGUNDO PARA EVITAR SOLAPAMIENTO DE HILOS
            time.sleep(1)


def threadTask(cam):
    while SWITCH:
        # MEDIMOS EL TIMEPO DE DESCARGA EN SEGUDOS
        timeInit = datetime.datetime.now()
        cam.getImageThread()
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

        # SI EL TIEMPO DE DESCARGA ES MENOR AL TIEMPO CONFIGURDO EN LA CAMARA
        # SE INICIA UN RETRASO CON EL TIEMPO FALTANTE
        # PARA QUE LA PETICION DE CADA IMAGEN SE REALICE EN EL TIEMPO SOLICITADO
        time.sleep(lapso)


if __name__ == "__main__":
    main()
    # SE INICIA LA TAREA
    taskCamera()

    # SE REQUIERE PARA QUE LOS THREADS FUNCIONEN
    while 1:
        pass