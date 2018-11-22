import cv2
import numpy as np
import os
import datetime

from os.path import isfile, join
VALID_EXTENSIONS = ('png', 'jpg')
# RESTRICT = [['00:00:01', '05:00:00'], ['19:00:00', '23:59:59']]
RESTRICT = []


def restrictHour(restrict, filename):
    year = filename[-18:-16]
    month = filename[-15:-13]
    day = filename[-13:-11]
    aux = 6
    try:
        hour = int(filename[-10-aux:-8-aux])
        minute = int(filename[-8-aux:-6-aux])
        second = int(filename[-6-aux:-4-aux])
    except:
        return False

    # obtenemos la hora de la imagen por el nombre del archivo
    fileTime = datetime.time(hour, minute, second)

    if restrict is None:
        return False, []

    # VARIABLE DE ESCAPE DEL BUCLE
    centinel = False
    hourRestrict = []
    # localtime = datetime.datetime.now().time()

    # BUCLE PARA LEER EL ARRAY DE RESTRICCIONES
    for r in restrict:
        # DESDE
        h = r[0].split(':')
        rtimeFrom = datetime.time(int(h[0]), int(h[1]), int(h[2]))
        # HASTA
        h = r[1].split(':')
        rtimeTo = datetime.time(int(h[0]), int(h[1]), int(h[2]))

        # EVALUAMOS SI LA HORA LOCAL ESTA DENTRO DEL RANGO DE RESTRICCION
        if rtimeFrom < fileTime < rtimeTo:
            hourRestrict = r
            centinel = True
            break

    return centinel, hourRestrict


def convert_frames_to_video(pathIn, pathOut, fps):
    frame_array = []
    # files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    files = sorted(os.listdir(pathIn))
    # for sorting the file names properly
    # files.sort(key=lambda x: int(x[5:-4]))

    for i in range(len(files)):
        print 'item ' + str(i)
        try:
            filename = pathIn + files[i]
            # reading each files
            # cen, _ = restrictHour(RESTRICT, files[i])
            # print 'CEN: ' + cen
            if filename.lower().endswith(VALID_EXTENSIONS):
                try:
                    img = cv2.imread(filename)
                    height, width, layers = img.shape
                    size = (width, height)
                    print(filename)
                    # inserting the frames into an image array
                    frame_array.append(img)
                except:
                    print 'ERROR: ' + filename
            # else:
            #     print 'NO FORMATO: ' + filename
        except:
            print '??? ' + files[i]

    # print frame_array
    print 'VideoWriter START'
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    print 'VideoWriter STARTING'

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    print 'VideoWriter END'


def main():
    # pathIn = '/home/pc17/Desktop/getImage/sabancaya/2018/05/30/'
    # pathIn = '/home/pc17/monitoreo/Visual/Procesados/sabancaya2/2018/08/08/'
    pathIn = '/home/pc17/Desktop/GIF/'
    pathOut = 'gifSabancayaIR.avi'
    fps = 1.0
    convert_frames_to_video(pathIn, pathOut, fps)


if __name__ == "__main__":
    main()