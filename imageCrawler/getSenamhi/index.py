from getSenamhi import GetSenamhi
# import ftplib
import datetime
import mapConfig
import threading
import time
import sys
import os


def main(argv):
    global VOLCANO
    global PATH_LOCAL
    global PROXYURL
    global PORT_P
    global USER_P
    global PASS_P
    global ISPROXY
    global SECONDS_FRECUENCY_LOOP

    global PATH_SERVER_DEST
    global HOST_S
    global PORT_S
    global USER_S
    global PASS_S

    DATA = mapConfig.init()
    PATH_LOCAL = DATA['PATH_LOCAL']
    PROXYURL = DATA['PROXYURL']
    PORT_P = DATA['PORT_P']
    USER_P = DATA['USER_P']
    PASS_P = DATA['PASS_P']
    ISPROXY = DATA['ISPROXY']
    SECONDS_FRECUENCY_LOOP = DATA['SECONDS_FRECUENCY_LOOP']
    VOLCANO = DATA['VOLCANO']

    PATH_SERVER_DEST = DATA['PATH_SERVER_DEST']
    HOST_S = DATA['HOST_S']
    PORT_S = DATA['PORT_S']
    USER_S = DATA['USER_S']
    PASS_S = DATA['PASS_S']


# def generateDateRange():
#     DATE = datetime.datetime.now()
#     H = DATE.hour
#     H2 = H - 2
#     if H <= 9:
#         H = '0' + str(H)
#     if H2 <= 9:
#         H2 = '0' + str(H2)
#
#     M = DATE.minute
#     if M <= 9:
#         M = '0' + str(M)
#
#     timeTo = str(H) + ':' + str(M) + ':00'
#     timeFrom = str(H2) + ':' + str(M) + ':00'
#     return timeFrom, timeTo
#
#
def getImage(params):
    gif = GetSenamhi()
    gif.setParams(params)
    gif.getImages()
    del gif


def worker():
    print(str(time.ctime()))
    print('-------------------------------------')
    task()
    threading.Timer(float(SECONDS_FRECUENCY_LOOP), worker).start()


def task():
    # timeFrom, timeTo = generateDateRange()
    for idx, vol in enumerate(VOLCANO):
        if vol['enable']:
            vol['id'] = idx
            vol['pathLocal'] = PATH_LOCAL
            vol['PROXYURL'] = PROXYURL
            vol['PORT_P'] = PORT_P
            vol['USER_P'] = USER_P
            vol['PASS_P'] = PASS_P
            vol['ISPROXY'] = ISPROXY

            vol['PATH_SERVER_DEST'] = PATH_SERVER_DEST
            vol['HOST_S'] = HOST_S
            vol['PORT_S'] = PORT_S
            vol['USER_S'] = USER_S
            vol['PASS_S'] = PASS_S
            # vol['PATH_DEST_GIF_SERVER'] = PATH_DEST_GIF_SERVER

            print('VOLCANO: [' + vol['name'] + ']')
            getImage(vol)
            print('-------------------------------------')
        else:
            print('VOLCANO: [' + vol['name'] + '] DISABLE!!')
    print


if __name__ == "__main__":
    main(sys.argv[1:])
    if SECONDS_FRECUENCY_LOOP is not None:
        worker()
    else:
        task()

