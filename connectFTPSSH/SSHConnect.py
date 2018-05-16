#!/usr/bin/python

import time
import datetime
# import shutil
import os, sys, getopt
import paramiko
# import filecmp

HOSTNAME = '10.102.131.52'
USERNAME = 'root'
PASSWORD = 'rootubinas2016'
PATH_LOCAL = '/home/pc17/Desktop/SSHconnect/'
PATH_REMOTE = '/root/rick/'
EXTENSION = '.miniseed'
RANGE = -2
BYTES = 5000
DATE = ''


def help(text):
    print (text)
    print ('      Test.py -H [hostname]')
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

    try:
        opts, args = getopt.getopt(argv, 'hH:U:P:L:R:b:r:e:D:', ['hostname=',
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

    print ('------------------ START ------------------')
    print ('connectando... ' + str(USERNAME) + '@' + str(HOSTNAME))
    print ('    pathLocal: ' + str(PATH_LOCAL))
    print ('    pathRemote: ' + str(PATH_REMOTE))
    print ('    extensionFile: ' + str(EXTENSION))
    print ('    DATE: ' + str(datetime.datetime.today()))
    print ('-------------------------------------------')
    # print ('Hostname: ', HOSTNAME)
    # print ('Username: ', USERNAME)
    # print ('Password: ', PASSWORD)
    # print ('Path Local: ', PATH_LOCAL)
    # print ('Path Remote: ', PATH_REMOTE)


# CONEXION SSH
def connectionSSH(H, U, P):
    paramiko.Transport.default_max_packet_size = 2
    paramiko.Transport.default_window_size = 2
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=H,  username=U, password=P)
    sftp = ssh.open_sftp()
    return sftp, ssh


# COPARAR FILE
def compareFiles(sftp, localFile, remoteFile):
    ttime = time.time()
    statLocal = os.stat(localFile)
    file_mod_time = statLocal.st_mtime
    last_time_local = (ttime - file_mod_time) / 60
    size_file_local = statLocal.st_size
    # print("LOCAL: ", last_time_local)

    statRemote = sftp.stat(remoteFile)
    file_mod_time = statRemote.st_mtime
    last_time_remote = (ttime - file_mod_time) / 60
    size_file_remote = statRemote.st_size
    # print("REMOTE: ", last_time_remote)

    return size_file_local != size_file_remote or int(last_time_local) > int(last_time_remote)


def sftpGet(sftp, remotepath, localpath, callback=None):
    fr = sftp.file(remotepath, 'rb')
    file_size = sftp.stat(remotepath).st_size
    fr.prefetch()
    try:
        fl = open(localpath, 'wb')
        try:
            size = 0
            # ttime = time.time()
            while True:
                tStart = time.time()
                data = fr.read(int(BYTES))
                tEnd = time.time()
                ttotal = float(tEnd - tStart)

                if len(data) == 0:
                    break
                fl.write(data)
                size += len(data)

                if ttotal < 1:
                    time.sleep(float(1.0 - ttotal))

                if callback is not None:
                    callback(size, file_size)

                #if ttotal < 1:
                #time.sleep(float(1.0 - ttotal))

        finally:
            fl.close()
    finally:
        fr.close()


# ProgressBar
def progress_bar(transferred, toBeTransferred, timeTransferred =0, suffix=''):
    suffix = "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
    bar_len = 60
    filled_len = int(round(bar_len * transferred / float(toBeTransferred)))
    percents = round(100.0 * transferred / float(toBeTransferred), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


# Generar fecha Path
def generateDatePath(index, PRemote, PLocal):
    today = datetime.date.today() - datetime.timedelta(days=int(index))
    if int(today.day) < 10:
        dia = '0' + str(today.day)
    else:
        dia = str(today.day)

    if int(today.month) < 10:
        mes = '0' + str(today.month)
    else:
        mes = str(today.month)
    year = today.year
    miniPath = str(year) + '/' + str(mes) + '/' + str(dia) + '/'
    return PRemote + miniPath, PLocal + miniPath


# VALIDATE DATE
def validateDate(date):
    isValidDate = True
    try:
        year, month, day = date.split('/')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    return isValidDate


# COPIAR FILE
def copyFile(sftp, file, source, dest):
    try:
        sftp.stat(source)
        print (file + ' >>> ' + dest)
        # sftp.get(source, dest, callback=progress_bar)
        sftpGet(sftp, source, dest, callback=progress_bar)
    except:
        print('#Error: No existe el archivo ', source)


# LIST FILES
def listFiles(SFTP, PRemote, PLocal):
    # Genera ruta Local
    if not os.path.exists(PLocal):
        os.makedirs(PLocal)
    # Valida Ruta Remota
    try:
        SFTP.stat(PRemote)
        # Lista evalua files
        sources = SFTP.listdir(PRemote)
        print('#Acces: ruta ' + str(PRemote) + ' :')
        for file in sources:
            if file.endswith(EXTENSION):
                # print (PRemote + file)
                if os.path.exists(PLocal + file):
                    if compareFiles(SFTP, PLocal + file, PRemote + file):
                        # print('son distintos')
                        copyFile(SFTP, file, PRemote + file, PLocal + file)
                        print
                    else:
                        print('#Alert: El archivo' + str(PRemote) + str(file) + ' ya existe en local')
                else:
                    # print('son nuevos')
                    copyFile(SFTP, file, PRemote + file, PLocal + file)
                    print
                    # print ('-----------------------')
        print
    except:
        print('#Error: No existe la ruta ' + str(PRemote))
        # sys.exit(2)


#
def write_log(path, timeDuration, total_files = 0, total_copy = 0):
    now = datetime.datetime.now()
    # id = int(now.timestamp()*1000000)
    date = now.strftime('%d-%m-%Y %H:%M:%S')
    file = sys.argv[0].split('/')[-1]

    c = timeDuration
    duration = "%s days, %.2dh: %.2dm: %.2ds" % (c.days,c.seconds//3600,(c.seconds//60)%60, c.seconds%60)

    f = open(path + "log-server.txt", "a+")
    f.write('date:{} file:{}  duration:{}  totalFiles:{}  totalCopy:{}\n'.format(date, file, duration, total_files, total_copy))
    f.close()
    print('Create log in log-server.txt:', id)


if __name__ == "__main__":
    main(sys.argv[1:])
    SFTP, SSH = connectionSSH(HOSTNAME, USERNAME, PASSWORD)
    nowInit = datetime.datetime.now()
    if DATE != '' and validateDate(DATE):
        PRemote, PLocal = PATH_REMOTE + DATE + '/', PATH_LOCAL + DATE + '/'
        listFiles(SFTP, PRemote, PLocal)
    else:

        if RANGE == 0:
            PRemote, PLocal = generateDatePath(0, PATH_REMOTE, PATH_LOCAL)
            listFiles(SFTP, PRemote, PLocal)
        else:
            for i in range(RANGE):
                # GENERAR RUTA
                PRemote, PLocal = generateDatePath(i+1, PATH_REMOTE, PATH_LOCAL)
                listFiles(SFTP, PRemote, PLocal)

    SFTP.close()
    SSH.close()
    nowEnd = datetime.datetime.now()
    duration = nowEnd - nowInit
    write_log(PATH_LOCAL, duration)
    print ('         El proceso ha finalizado          ')
    print ('------------------- END -------------------')
    print
