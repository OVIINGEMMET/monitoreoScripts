from createGifAll import CreateGif
# import ftplib
import datetime
import mapConfig
import threading
import time
import sys, getopt
import os


def help(text):
    print (text)
    print ('      index.py -h <help>')
    print ('               -c <filename config.ini in principal PATH>')
    print


def main(argv):
    global DATA
    global PATH_ORIGIN_GIF_LOCAL
    global PATH_DEST_GIF_SERVER
    global SECONDS_FRECUENCY_CREATE
    global CAMERAS

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

    DATA = mapConfig.init(configFile)
    PATH_ORIGIN_GIF_LOCAL = DATA['PATH_ORIGIN_GIF_LOCAL']
    PATH_DEST_GIF_SERVER = DATA['PATH_DEST_GIF_SERVER']
    SECONDS_FRECUENCY_CREATE = DATA['SECONDS_FRECUENCY_CREATE']
    CAMERAS = DATA['CAMERA']


def generateDateRange():
    DATE = datetime.datetime.now()
    H = DATE.hour
    H2 = H - 2
    if H <= 9:
        H = '0' + str(H)
    if H2 <= 9:
        H2 = '0' + str(H2)

    M = DATE.minute
    if M <= 9:
        M = '0' + str(M)

    timeTo = str(H) + ':' + str(M) + ':00'
    timeFrom = str(H2) + ':' + str(M) + ':00'
    return timeFrom, timeTo


def createGif(params):
    gif = CreateGif()
    gif.setParams(params)
    gif.createGif()
    del gif


def worker():
    print(str(time.ctime()))
    print('-------------------------------------')
    taskCreateGif()
    threading.Timer(SECONDS_FRECUENCY_CREATE, worker).start()


def taskCreateGif():
    timeFrom, timeTo = generateDateRange()
    for idx, cam in enumerate(CAMERAS):
        if cam['enable']:
            cam['id'] = idx
            cam['path'] = PATH_ORIGIN_GIF_LOCAL
            if cam['automatic']:
                cam['time'] = [timeFrom, timeTo]
            else:
                auxTime = cam['rangeTime'].split('-')
                cam['time'] = [auxTime[0], auxTime[1]]

            cam['PATH_DEST_GIF_SERVER'] = PATH_DEST_GIF_SERVER

            print('CAMERA: [' + cam['cameraName'] + ']')
            createGif(cam)
            print('-------------------------------------')
        # else:
        #    print('CAMERA: [' + cam['cameraName'] + '] DISABLE!!')
    print


if __name__ == "__main__":
    main(sys.argv[1:])

    if SECONDS_FRECUENCY_CREATE is not None:
        worker()
    else:
        taskCreateGif()

