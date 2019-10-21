import datetime
import getopt
import sys
import time

import _thread
import configStation
import copyGCF

SWITCH = True
# print("argv was", sys.argv)
# print("sys.executable was", sys.executable)
# print("restart now")


def help(text):
    print(text)
    print('      index.py -h <help>')
    print('               -c <filename config.ini in principal PATH>')
    print


def main(argv):
    global SWITCH
    global DATA
    global STATIONS
    global storeStation
    global SECONDS
    global OBJSTATION

    global configFile

    SECONDS = 'None'
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

    DATA = configStation.init(configFile)
    # SECONDS = DATA['SECONDS']
    STATIONS = DATA['STATION']
    OBJSTATION = []
    # print('DATA')
    # print(DATA)


def taskStation():
    for idx, stn in enumerate(STATIONS):
        if stn['enable']:
            # iniciamos el OBJETO
            a = copyGCF.Station()
            #             SETEAMOS LOS PARAMETRSO
            stn['id'] = idx
            stn['SWITCH'] = True
            stn['EXEC'] = [sys.executable, ['phyton'] + sys.argv]
            if stn['type'] == 'copyGCF':
                a.setParametersToCopyGCF(stn)
            # elif stn['type'] == 'convertGCFtoSAC':
            #     a.setParametersToConvertGCFtoSAC(stn)

            a.printParams(stn)

            #             DECLAMARMOS LOS THREADS
            OBJSTATION.append(a)
            _thread.start_new_thread(threadTask, (a,))

            # RETARDAMOS CADA THREAD 1 SEGUNDO PARA EVITAR SOLAPAMIENTO DE HILOS
            time.sleep(1)


def threadTask(stn):
    # global SWITCH
    total_errors = 0
    while stn.SWITCH:
        timeInit = datetime.datetime.now()
        if stn.type == 'copyGCF':
            stn.copyGCF()
        # elif stn.type == 'convertGCFtoSAC':
        #     stn.copyGCF.convertGCFtoSAC()

        timeEnd = datetime.datetime.now()
        duration = timeEnd - timeInit
        totalSeconds = duration.total_seconds()
        # ----------------------------------------

        # OBTENEMOS EL TIEMPO DE LA STATION
        secondsLocal = float(stn.timer)
        if totalSeconds < secondsLocal:
            lapso = secondsLocal - totalSeconds
        else:
            lapso = 0

        stn.printColor('waiting ' + str(lapso) + ' seconds...', 'Lapso')

        if SECONDS is not None:
            # SI EL TIEMPO DE DESCARGA ES MENOR AL TIEMPO CONFIGURDO EN LA CAMARA
            # SE INICIA UN RETRASO CON EL TIEMPO FALTANTE
            # PARA QUE LA PETICION DE CADA IMAGEN SE REALICE EN EL TIEMPO SOLICITADO
            print("TIME SLEEP???")
            time.sleep(lapso)
        else:
            print("SWTICH???")
            stn.SWITCH = False


#
if __name__ == '__main__':
    main(sys.argv[1:])

    # SE INICIA LA TAREA

    taskStation()

    # SE REQUIERE PARA QUE LOS THREADS FUNCIONEN
    while 1:
        cen = False
        # error_total = 0
        for idx, stn in enumerate(OBJSTATION):
            cen = cen or stn.SWITCH
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
            print("llega aqui???")
            sys.exit(1)
