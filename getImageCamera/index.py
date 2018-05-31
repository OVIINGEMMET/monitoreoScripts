#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getImage import Camera
import mapConfig
import threading
import time
import sys
import datetime
import os
# CAMERAS = None


def main(argv):
    global DATA
    global PATH
    global FONT
    global CAMERAS
    global storageCamera
    global SECONDS

    DATA = mapConfig.init()
    SECONDS = DATA['SECONDS']
    PATH = DATA['ROOTPATH']
    FONT = DATA['FONT']
    CAMERAS = DATA['CAMERA']
    storageCamera = Camera()


def worker():
    print(str(time.ctime()))
    # MEDIMOS EL TIMEPO DE DESCARGA EN SEGUDOS
    timeInit = datetime.datetime.now()
    taskCamera()
    timeEnd = datetime.datetime.now()
    duration = timeEnd - timeInit
    totalSeconds = duration.total_seconds()

    if totalSeconds < SECONDS:
        lapso = SECONDS - totalSeconds
    else:
        lapso = 0

    threading.Timer(lapso, worker).start()


def taskCamera():
    for idx, cam in enumerate(CAMERAS):
        if not storageCamera.isWorking:
            cam['id'] = idx
            cam['GLOBALPATH'] = PATH
            cam['FONT'] = FONT
            storageCamera.setParameters(cam)
            storageCamera.getImage()
        else:
            print ('IS working ' + storageCamera.cameraName)

    print


if __name__ == "__main__":
    main(sys.argv[1:])
    worker()

