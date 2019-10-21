from datetime import datetime
import fnmatch
import os
import platform
import shutil
from pprint import pprint
from obspy import read
import colors


# try:
#     import paramiko
#
#     PARAMIKOLOAD = True
# except:
#     print('Not import paramiko - SSH connection')
#     PARAMIKOLOAD = False

# try:
#     from clint.textui import progress, colored, puts
#
#     COLORED = True
# except:
#     print('Not from clint.textui import progress, colored, puts')
#     COLORED = False


# SABANCAYA = "Sabancaya/"
# MISTI = "Misti/"
# UBINAS = "Ubinas/"
#
# PATH_ORIGIN_DIARIOS = "/mnt/data/Reportes/"
# PATH_DESTINY_DIARIOS = "/var/www/html/panelview2/img/reporte_diario/"
#
# PATH_ORIGIN_CENIZAS = "/mnt/data/Cenizas/caida_de_cenizas/"
# PATH_DESTINY_CENIZAS = "/var/www/html/panelview2/img/cenizas/"
#
# FLUJOSO2_SABANCAYA = "D2J2833/"
# FLUJOSO2_UBINAS = "D2J2559/"
#
# PATH_ORIGIN_FLUJOSO2 = "/mnt/data/Geoquimica/1-EST-NOVAC/1_DOAS/"
# PATH_DESTINY_FLUJOSO2 = "/var/www/html/panelview2/img/flujoso2/"


class Station:
    def __init__(self):
        self.type = 'station'
        self.id = 0
        self.stationNameFrom = ''
        self.stationNameTo = ''
        self.pathFrom = ''
        self.pathToGCF = ''
        self.pathToSAC = ''
        self.volcano = ''
        self.enable = True
        self.today = None
        self.filename = ''
        self.isWorking = False
        self.date = None
        self.timer = 30
        self.timeout = 5
        self.SWITCH = True
        self.EXEC = [None, None]

    def setParametersToCopyGCF(self, params):
        # print('parameters')
        # print(params)

        self.type = params['type']

        self.id = params['id']

        self.stationNameFrom = params['stationNameFrom']
        self.stationNameTo = params['stationNameTo']

        self.volcano = params['volcano']

        self.pathFrom = params['pathFrom']

        self.pathToGCF = params['pathToGCF']
        self.pathToSAC = params['pathToSAC']

        self.timer = params['timer']

        self.enable = params['enable']

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

    def pathFileDestination(self, pathOrigin):
        allparts = []
        while 1:
            parts = os.path.split(pathOrigin)
            if parts[0] == pathOrigin:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == pathOrigin:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                pathOrigin = parts[0]
                allparts.insert(0, parts[1])

        date = allparts[-3] + '/' + allparts[-2] + '/' + allparts[-1] + '/'
        return date

    def creation_date(self, path_to_file):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        now = datetime.now().strftime('%Y-%m-%d %H')
        if platform.system() == 'Windows':
            createdHour = datetime.fromtimestamp(os.path.getctime(path_to_file)).strftime('%Y-%m-%d %H')

        else:
            stat = os.stat(path_to_file)
            try:
                createdHour = stat.st_birthtime.strftime('%Y-%m-%d %H')
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                createdHour = stat.st_mtime.strftime('%Y-%m-%d %H')

        if createdHour < now:
            return True
        else:
            return False

    def getNewFileName(self, file):
        changeName = file.split('.')
        if len(changeName) == 4:
            date, station, position, extencion = map(str, changeName)
            if station == "cf59":
                newStationName = "sab10"
            elif station == "9f59":
                newStationName = "ubn02"
            else:
                newStationName = station

            if len(position) == 1:
                newName = date + '.' + newStationName + '.' + position + '.' + extencion
            else:
                newPos = position[len(position) - 2]
                newName = date + '.' + newStationName + '.' + str(newPos) + '.' + extencion
        else:
            newName = file
        return newName

    def copyGCF(self):
        # verificamos q la camara este habilitado en el archivo INI
        if self.enable:
            self.isWorking = True
            # getDate = self.generateDatePath()
            remote_pathFrom = self.pathFrom + self.stationNameFrom + '/'

            originPathFiles = [os.path.join(dirpath, f)
                               for dirpath, dirnames, files in os.walk(remote_pathFrom)
                               for f in fnmatch.filter(files, '*.*')]
            for filesdir in originPathFiles:
                copying = self.creation_date(filesdir)
                if copying:
                    a = os.path.split(filesdir)
                    pathFileOrigin = a[0]
                    originalFileName = a[1]
                    pathFileDestiny = self.pathFileDestination(pathFileOrigin)
                    newfileName = self.getNewFileName(originalFileName)
                    remote_pathToSAC = self.pathToSAC + self.volcano + '/' + self.stationNameTo + '/' + pathFileDestiny
                    remote_pathToGCF = self.pathToGCF + self.volcano + '/' + self.stationNameTo + '/' + pathFileDestiny
                    # print('imprimiendo remote_pathFrom')
                    # print(remote_pathFrom)
                    # print('imprimiendo remote_pathToSAC')
                    # print(remote_pathToSAC)
                    # print('imprimiendo remote_pathToGCF')
                    # print(remote_pathToGCF)
                    try:

                        if fnmatch.fnmatch(newfileName, "*.gcf"):
                            # if self.file_exists(remote_path+'/') or retry == 0:

                            if not os.path.exists(remote_pathToSAC):
                                os.makedirs(remote_pathToSAC)
                                st = read(pathFileOrigin + '/' + originalFileName)
                                st.write(remote_pathToSAC + os.path.splitext(newfileName)[0] + '.sac', format='SAC')
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': GCF--TO--SAC from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToSAC +
                                                    os.path.splitext(newfileName)[0] + '.sac'), self.volcano)
                            else:
                                st = read(pathFileOrigin + '/' + originalFileName)
                                st.write(remote_pathToSAC + os.path.splitext(newfileName)[0] + '.sac', format='SAC')
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': GCF--TO--SAC from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToSAC +
                                                    os.path.splitext(newfileName)[0] + '.sac'), self.volcano)

                            if not os.path.exists(remote_pathToGCF):
                                os.makedirs(remote_pathToGCF)
                                shutil.move(pathFileOrigin + '/' + originalFileName,
                                            remote_pathToGCF + newfileName)
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': COPY--GCF from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToGCF + newfileName),
                                                self.volcano)
                            else:
                                shutil.move(pathFileOrigin + '/' + originalFileName,
                                            remote_pathToGCF + newfileName)
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': COPY--GCF from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToGCF + newfileName),
                                                self.volcano)
                        else:

                            if not os.path.exists(remote_pathToGCF):
                                os.makedirs(remote_pathToGCF)
                                shutil.move(pathFileOrigin + '/' + originalFileName,
                                            remote_pathToGCF + originalFileName)
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': COPY--TXT from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToGCF + originalFileName),
                                                self.volcano)
                            else:
                                shutil.move(pathFileOrigin + '/' + originalFileName,
                                            remote_pathToGCF + originalFileName)
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': COPY--TXT from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToGCF + originalFileName),
                                                self.volcano)
                    except WindowsError:
                        # self.printColor("No se puede realizar esta acción, debido a que el archivo esta siendo usado por otro proceso", "Inuse")
                        pass
                else:
                    self.printColor("No se puede realizar esta acción, debido a que el archivo esta siendo usado por otro proceso", "Inuse")
            # self.enable = False
            # print('Termino el Proceso?')
        else:
            self.isWorking = False
            self.printColor("No hay Archivos en este Directorio", "Inuse")

    def setParametersToConvertGCFtoSAC(self, params):

        self.type = params['type']

        self.id = params['id']

        self.stationNameFrom = params['stationNameFrom']
        self.stationNameTo = params['stationNameTo']

        self.volcano = params['volcano']

        self.pathFrom = params['pathFrom']

        self.pathTo = params['pathTo']

        self.timer = params['timer']

        self.enable = params['enable']

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

    def convertGCFtoSAC(self):
        pprint('to sac')
        if self.enable:
            self.isWorking = True
            getDate = self.generateDatePath()
            remote_pathFrom = self.pathFrom + self.volcano + '/' + self.stationNameFrom + '/' + getDate
            remote_pathTo = self.pathTo + self.volcano + '/' + self.stationNameTo + '/' + getDate
            print('imprimiento remote_path')
            print(remote_pathFrom)

            for filename in os.listdir(remote_pathFrom):
                print('filename')
                print(filename)
                if fnmatch.fnmatch(filename, "*.gcf"):
                    # if self.file_exists(remote_path+'/') or retry == 0:
                    if not os.path.exists(remote_pathTo):
                        os.makedirs(remote_pathTo)
                        st = read(remote_pathFrom + filename)
                        st.write(remote_pathTo + filename, format='SAC')
                    else:
                        st = read(remote_pathFrom + filename)
                        st.write(remote_pathTo + filename, format='SAC')
                else:
                    print('No hay archivos...')

    def generateDatePath(self):
        # GENERAMOS LA ESTRUCTURA DE CARPETAS ANIDADAS POR ANIO/MES/DIA/
        self.today = datetime.datetime.now()
        today = self.today
        if int(today.day) < 10:
            dia = '0' + str(today.day)
        else:
            dia = str(today.day)
        if int(today.month) < 10:
            mes = '0' + str(today.month)
        else:
            mes = str(today.month)

        year = today.year
        filenamePath = str(year) + '/' + str(mes) + '/' + str(dia) + '/'

        if not os.path.exists(filenamePath):
            os.makedirs(filenamePath)
        return filenamePath

    def printColor(self, msg, volcano):
        if volcano == "Misti":
            print(colors.blue(msg))

        elif volcano == "Sabancaya":
            print(colors.yellow(msg))

        elif volcano == "Ubinas":
            print(colors.cyan(msg))

        elif volcano == "Ticsani":
            print(colors.magenta(msg))

        elif volcano == "Inuse":
            print(colors.red(msg))
        else:
            print(msg)

    def printParams(self, params):
        pprint(params)
