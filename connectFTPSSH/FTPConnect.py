# Libreria para conexiones FTP
import ftplib
# Libreria para generar progressBar
import tqdm
# Librerias de Python
import time
import datetime
import os, sys, getopt


# HOSTNAME: IP del servidor
# PATH_LOCAL: Path donde se guardaran los archivos descargados
# PATH_REMOTE: Path del servidor done estan los archivos
# EXTENSION: Extension del Archivo a descargar
# GPS: Nombre del GPS por ejemplo 'MAD2', 'MAD3', 'MGAL' o 'MAD1'
# ALL: Switch - False descarga de las fechas que corresponden al valor de RANGE / True descarga de todas las fechas
# LOOPH: Switch - False descarga el GPS ingresado / True descarga datos de la lista HOSTS

HOSTNAME = '10.101.0.12'
USERNAME = 'ovi'
PASSWORD = 'sistemaovi'
PATH_LOCAL = '/home/pc17/Desktop/realtime/'
PATH_REMOTE = '/home/ovi/'
EXTENSION = '.T02'
GPS = ''
ALL = False
LOOPH = False
RANGE = -2
BYTES = 10000
DATE = ''

# Lista de host o servers registrados
HOSTS = ['192.168.0.122', '192.168.0.123', '192.168.0.124', '192.168.0.121', '10.101.0.12']
# Directorio de gps registrados, cada item de esta lista se asocia a un respectivo Host segun su posicion
GPSLIST = ['MAD2', 'MAD3', 'MGAL', 'MAD1', 'test']

DATEYEARINIT = ''
DATENOW = ''


def help(text):
    print (text)
    print ('      Test.py -h <help>')
    print ('              -X <COPY Internal Hostnames by range -r>')
    print ('              -A <copiar todo by date -D>')
    print ('              -H [hostname]')
    print ('              -U [username]')
    print ('              -P [password]')
    print ('              -L [path local]')
    print ('              -R [path remote]')
    print ('              -b [bytes=5000]')
    print ('              -r [range <=-1]')
    print ('              -e [extension=.txt]')
    print ('              -D [date=aaaa/mm/dd]')
    print


# MAIN
def main(argv):
    global HOSTNAME
    global USERNAME
    global PASSWORD
    global PATH_LOCAL
    global PATH_REMOTE
    global BYTES
    global RANGE
    global EXTENSION
    global DATE
    global GPS
    global DATEYEARINIT
    global DATENOW
    global ALL
    global LOOPH

    try:
        opts, args = getopt.getopt(argv, 'hH:U:P:L:R:b:r:e:D:A:X', ['hostname=',
                                                               'username=',
                                                               'password=',
                                                               'pathLocal=',
                                                               'pathRemote=',
                                                               'bytes=',
                                                               'range=',
                                                               'extension=',
                                                               'date='
                                                               ])
    except getopt.GetoptError:
        help('Error de argumentos')
        sys.exit(2)

    # print(opts)

    for opt, arg in opts:
        if opt == '-h':
            help('Help:')
            sys.exit()
        elif opt == '-A':
            ALL = True
        elif opt == '-X':
            LOOPH = True
        elif opt in ('-H', '--hostname'):
            HOSTNAME = arg
        elif opt in ('-U', '--username'):
            USERNAME = arg
        elif opt in ('-P', '--password'):
            PASSWORD = arg
        elif opt in ('-L', '--pathLocal'):
            PATH_LOCAL = arg
        elif opt in ('-R', '--pathRemote'):
            PATH_REMOTE = arg
        elif opt in ('-b', '--bytes'):
            BYTES = int(arg)
        elif opt in ('-r', '--range'):
            RANGE = int(arg)
        elif opt in ('-e', '--extension'):
            EXTENSION = arg
        elif opt in ('-D', '--date'):
            DATE = arg

    if PASSWORD == '':
        print ('Debe asignar un password [-P]')
        sys.exit(1)

    if DATE != '' and not validateDate(DATE):
        print ('Debe asignar una fecha con formato aaaa/mm/dd [-D]')
        sys.exit(1)

    if RANGE > 0:
        print ('Debe asignar un rango negativo <= -1 [-r]')
        sys.exit(1)
    else:
        RANGE = RANGE * -1

    if LOOPH is False:
        index = -1
        for (i, hostname) in enumerate(HOSTS):
            if HOSTNAME == hostname:
                index = i

        if index > -1:
            GPS = GPSLIST[index]
        else:
            GPS = ''
            print ('Debe registrar una IP o HOSTANAME valida')
            sys.exit(1)

    DATENOW = datetime.date.today()
    DATEYEARINIT = datetime.date(DATENOW.year, 1, 1)

    d = DATENOW - DATEYEARINIT
    print(d.days)
    print ('------------------ START ------------------')
    print ('FTP connectando... ' + str(USERNAME) + '@' + str(HOSTNAME))
    print ('    pathLocal: ' + str(PATH_LOCAL))
    print ('    pathRemote: ' + str(PATH_REMOTE))
    print ('    extensionFile: ' + str(EXTENSION))
    print ('    DATE: ' + str(datetime.datetime.today()))
    print ('    COPIAR TODO: ' + str(ALL))
    print ('-------------------------------------------')


# VALIDATE DATE
def validateDate(date):
    isValidDate = True
    try:
        year, month, day = date.split('/')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    return isValidDate


# CONEXION SSH
def connectionFTP(H, U, P):
    ftp = ftplib.FTP(H)
    ftp.login(U, P)
    return ftp


# ----------------------------------------------
# Generar fecha Path
def generateDatePath(index, PRemote, PLocal):
    today = datetime.date.today() - datetime.timedelta(days=int(index))
    dia = today.day
    if int(today.month) < 10:
        mes = '0' + str(today.month)
    else:
        mes = str(today.month)
    year = today.year
    miniPath = str(year) + '/' + str(mes) + '/' + str(dia) + '/'
    return PRemote + miniPath, PLocal + miniPath


# Generar fecha Short Path
def generateShortDatePath(index, PRemote, PLocal, gps):
    today = DATENOW - datetime.timedelta(days=int(index))
    dia = today.day
    if int(today.month) < 10:
        mes = '0' + str(today.month)
    else:
        mes = str(today.month)
    year = today.year
    miniPath = str(year) + str(mes) + '/'
    miniPath2 = gps + '/' + str(year) + '/'

    # DAYS
    dif = today - DATEYEARINIT
    return PRemote + miniPath, PLocal + miniPath2, (dif.days + 1)


# LIST FILES
def listFiles(FTP, PRemote, PLocal, Fdays):
    # Genera ruta Local
    if not os.path.exists(PLocal):
        os.makedirs(PLocal)

    try:
        FTP.cwd('/')
        FTP.cwd(PRemote)
        sources = []

        if Fdays != -1:
            # print('POR DIAS')
            if Fdays < 100:
                strFdays = '0' + str(Fdays)
            else:
                strFdays = str(Fdays)

            FTP.retrlines('LIST *' + strFdays + 'a*' + EXTENSION + '*', sources.append)
            print('#Acces: ruta ' + str(PRemote) + ' :')
            for line in sources:
                file = line.split(' ')[-1]
                if os.path.exists(PLocal + file):
                    if compareFiles(FTP, PLocal + file, PRemote + file, file):
                        downLoad(FTP, file, PRemote + file, PLocal + file)
                        print
                    else:
                        print('     #Alert: El archivo' + str(PRemote) + str(file) + ' ya existe en local')
                else:
                    downLoad(FTP, file, PRemote + file, PLocal + file)
                    print
        else:
            # print('POR MES')
            FTP.retrlines('LIST *' + EXTENSION, sources.append)
            print('#Acces: ruta ' + str(PRemote) + ' :')

            for line in sources:
                file = line.split(' ')[-1]
                if os.path.exists(PLocal + file):
                    if compareFiles(FTP, PLocal + file, PRemote + file, file):
                        downLoad(FTP, file, PRemote + file, PLocal + file)
                        print
                    else:
                        print('     #Alert: El archivo' + str(PRemote) + str(file) + ' ya existe en local')
                else:
                    downLoad(FTP, file, PRemote + file, PLocal + file)
                    print
        print
    except:
        print('#Error: No existe la ruta ' + str(PRemote))


# COPIAR FILE
def copyFile(ftp, file, source, dest):
    ftp.retrbinary("RETR " + file, open(os.path.join(dest), "wb").write)
    try:
        print (file + ' >>> ' + dest)
        ftp.retrbinary("RETR " + file, open(os.path.join(dest), "wb").write)
    except:
        print('     #Error: Ocurrio un problema al copiar el archivo [' + source + ']')


def downLoad(ftp, file, remotePath, localPath):
    bufsize = BYTES
    fp = open(localPath, 'wb')
    total = ftp.size(file)
    pbar = tqdm.tqdm(total=total)

    def bar(data):
        fp.write(data)
        pbar.update(len(data))
        time.sleep(1)

    print time.ctime(), 'Begin to download: %s' % remotePath
    ftp.retrbinary('RETR ' + file, bar, bufsize)
    pbar.close()
    fp.close()
    print time.ctime(), 'Download is finished.'


# COPARAR FILE
def compareFiles(ftp, localFile, remoteFile, file):
    statLocal = os.stat(localFile)
    size_file_local = statLocal.st_size
    size_file_remote = ftp.size(file)
    return size_file_local != size_file_remote


def principalFTP(host, user, password, gps=''):

    if gps == '':
        LOCALGPS = GPS
    else:
        LOCALGPS = gps

    FTP = connectionFTP(host, user, password)
    if DATE != '' and validateDate(DATE):
        fecha = DATE.split('/')
        PRemote, PLocal = PATH_REMOTE + fecha[0] + fecha[1] + '/', PATH_LOCAL + LOCALGPS + '/' + fecha[0] + '/'
        print PRemote, PLocal
        if ALL is False:
            iDate = datetime.date(int(fecha[0]), int(fecha[1]), int(fecha[2]))
            diff = iDate - DATEYEARINIT
            fdays = diff.days + 1
        else:
            fdays = -1
        print "DIAS: " + str(fdays)
        listFiles(FTP, PRemote, PLocal, fdays)
    else:
        if RANGE == 0:
            PRemote, PLocal, fdays = generateShortDatePath(0, PATH_REMOTE, PATH_LOCAL, LOCALGPS)
            listFiles(FTP, PRemote, PLocal, fdays)
        else:
            for i in range(RANGE):
                # GENERAR RUTA
                PRemote, PLocal, fdays = generateShortDatePath(i, PATH_REMOTE, PATH_LOCAL, LOCALGPS)
                print "DIAS --- " + str(fdays)
                listFiles(FTP, PRemote, PLocal, fdays)
    FTP.quit()


#
def write_log(path, timeDuration, total_files = 0, total_copy = 0):
    now = datetime.datetime.now()
    # id = int(now.timestamp()*1000000)
    date = now.strftime('%d-%m-%Y %H:%M:%S')
    file = sys.argv[0].split('/')[-1]

    c = timeDuration
    duration = "%s days, %.2dh: %.2dm: %.2ds" % (c.days,c.seconds//3600,(c.seconds//60)%60, c.seconds%60)

    f = open(path + "log-server-gps.txt", "a+")
    f.write('date:{} file:{}  duration:{}  totalFiles:{}  totalCopy:{}\n'.format(date, file, duration, total_files, total_copy))
    f.close()
    # print('Create log in log-server.txt:', id)


if __name__ == "__main__":
    main(sys.argv[1:])
    nowInit = datetime.datetime.now()
    if LOOPH is False:
        principalFTP(HOSTNAME, USERNAME, PASSWORD)
    else:
        for h in range(len(HOSTS)):
            principalFTP(HOSTS[h], USERNAME, PASSWORD, GPSLIST[h])

    nowEnd = datetime.datetime.now()
    duration = nowEnd - nowInit
    write_log(PATH_LOCAL, duration)
    print
    print ('         El proceso ha finalizado          ')
    print ('------------------- END -------------------')
    print
