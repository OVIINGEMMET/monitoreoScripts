from datetime import datetime, timedelta
import fnmatch
import os, glob, time, configparser, ast, sys, getopt
import platform
import shutil
from pprint import pprint
from obspy import read, UTCDateTime
from colorama import Fore
from PIL import Image, ImageMath


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

        self.logoPath = ''
        self.component = ''
        self.pathFrom = ''
        self.pathToHelli = ''
        self.pathToWeb = ''
        self.pathToPanel = ''

        self.remoteConnect = ''
        self.remoteHost = ''
        self.remotePort = ''
        self.remoteUser = ''
        self.remotePass = ''

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

    def setParametersToHellicorder(self, params):
        # print('parameters')
        # print(params)

        self.type = params['type']
        self.id = params['id']
        self.stationNameFrom = params['stationNameFrom']
        self.stationNameTo = params['stationNameTo']
        self.volcano = params['volcano']

        self.logoPath = params['logoPath']
        self.component = params['component']
        self.pathFrom = params['pathFrom']
        self.pathToHelli = params['pathToHelli']
        self.pathToWeb = params['pathToWeb']

        self.pathToPanel = params['pathToPanel']
        self.remoteConnect = params['remoteConnect']
        self.remoteHost = params['remoteHost']
        self.remotePort = int(params['remotePort'])
        self.remoteUser = params['remoteUser']
        self.remotePass = params['remotePass']

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
        now = datetime.now()  # .strftime('%Y-%m-%d %H')
        if platform.system() == 'Windows':
            createdHour = datetime.fromtimestamp(os.path.getctime(path_to_file))  # .strftime('%Y-%m-%d %H')
            print(createdHour, path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                createdHour = stat.st_birthtime  # .strftime('%Y-%m-%d %H')
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                createdHour = stat.st_mtime  # .strftime('%Y-%m-%d %H')

        ago = now - timedelta(hours=1, minutes=20)

        if createdHour < ago:
            print('createdHour', 'ago')
            print(createdHour, ago)

            return True
        else:
            print('createdHour', 'ago')
            print(createdHour, ago)
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
                print(copying)
                if copying:
                    a = os.path.split(filesdir)
                    pathFileOrigin = a[0]
                    originalFileName = a[1]
                    pathFileDestiny = self.pathFileDestination(pathFileOrigin)
                    newfileName = self.getNewFileName(originalFileName)
                    remote_pathToSAC = self.pathToSAC + self.volcano + '/' + self.stationNameTo + '/' + pathFileDestiny
                    remote_pathToGCF = self.pathToGCF + self.volcano + '/' + self.stationNameTo + '/' + pathFileDestiny

                    try:

                        if fnmatch.fnmatch(newfileName, "*.gcf"):
                            # if self.file_exists(remote_path+'/') or retry == 0:

                            if not os.path.exists(remote_pathToSAC):
                                os.makedirs(remote_pathToSAC)
                            if not os.path.exists(remote_pathToGCF):
                                os.makedirs(remote_pathToGCF)
                            try:
                                st = read(pathFileOrigin + '/' + originalFileName)
                                st.write(remote_pathToSAC + os.path.splitext(newfileName)[0] + '.sac', format='SAC')
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': GCF--TO--SAC from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToSAC +
                                                    os.path.splitext(newfileName)[0] + '.sac'), self.volcano)

                                shutil.move(pathFileOrigin + '/' + originalFileName,
                                            remote_pathToGCF + newfileName)
                                self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                    ': COPY--GCF from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToGCF + newfileName),
                                                self.volcano)
                            except:
                                self.printColor(
                                    self.volcano + '-' + self.stationNameFrom + ": Archivo corrompido: " + originalFileName,
                                    'Inuse')
                                pass

                        else:

                            if not os.path.exists(remote_pathToGCF):
                                os.makedirs(remote_pathToGCF)
                            shutil.move(pathFileOrigin + '/' + originalFileName,
                                        remote_pathToGCF + originalFileName)
                            self.printColor(str(self.volcano + '-' + self.stationNameFrom +
                                                ': COPY--TXT from: ' + pathFileOrigin + '/' + originalFileName + ' --->>> To: ' + remote_pathToGCF + originalFileName),
                                            self.volcano)

                    except WindowsError:
                        pass
                else:
                    self.printColor(
                        self.volcano + '-' + self.stationNameFrom + ": No se puede realizar esta acción, el archivo esta siendo usado",
                        "Inuse")
        else:
            self.isWorking = False
            self.printColor("No hay Archivos en este Directorio", "Inuse")

    def generateDatePath(self):
        # GENERAMOS LA ESTRUCTURA DE CARPETAS ANIDADAS POR ANIO/MES/DIA/
        self.today = datetime.now()
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

    def convertToTransparent(self, img):
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        return img

    def distance2(self, a, b):
        return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2])

    def makeColorTransparent(self, image, color, thresh2=0):
        image = image.convert("RGBA")
        red, green, blue, alpha = image.split()
        image.putalpha(ImageMath.eval("""convert(((((t - d(c, (r, g, b))) >> 31) + 1) ^ 1) * a, 'L')""",
                                      t=thresh2, d=self.distance2, c=color, r=red, g=green, b=blue, a=alpha))
        return image
    def putLogo(self, img,date):

        originalImg = Image.open(img, 'r')
        logoImg = Image.open(self.logoPath, 'r')
        logoW = logoImg.size[0]
        logoH = logoImg.size[1]
        # REDIMENCIONAMOS IMAGEN
        imgH = 40
        percent = float(imgH)/logoH
        imgW = int(logoW*percent)
        newLogo = logoImg.resize((imgW, imgH), Image.ANTIALIAS)
        posLogo = (originalImg.size[0] - imgW - 20, 0)

        newImg = Image.new('RGBA', originalImg.size, (0, 0, 0, 0))
        newImg.paste(originalImg, (0, 0))
        newImg.paste(newLogo, posLogo, mask=newLogo)
        newImgJPG = newImg.convert('RGB')
        newImgJPG.save(img)

    def joinImages(self,img):
        original = img[:-5]
        print(original)
        originalImg = Image.open(original+'.png', 'r')
        gcfPart = Image.open(img, 'r')
        gcfPartTransparent = self.makeColorTransparent(gcfPart, (0,0,0))
        gcfPartTransparent = gcfPartTransparent.resize((900, 800), Image.ANTIALIAS)
        newImg = Image.new('RGBA', originalImg.size, (0, 0, 0, 0))
        newImg.paste(originalImg, (0, 0))
        newImg.paste(gcfPartTransparent, (0, 0), mask=gcfPartTransparent)
        # newImgJPG = newImg.convert('RGB')
        # newImgJPG.save(img)
        newImg.save(self.pathToHelli +'m.png')

    def plotHellicorder(self):
        pathDate = self.generateDatePath()
        path = self.pathFrom + self.stationNameFrom + '/' + pathDate
        print(path)
        filename = [os.path.join(dirpath, f)
                    for dirpath, dirnames, files in os.walk(path)
                    for f in fnmatch.filter(files, '*.z.gcf')]
        # filename = sorted(glob.glob(path[:-10] + 'z'))
        print(filename)
        st = read(filename[0])
        for i in range(1, len(filename)):
            st += read(filename[i])
        st.merge(method=1, fill_value='latest')
        st.filter('bandpass', freqmin=0.5, freqmax=20.0, corners=2, zerophase=False)
        now = UTCDateTime.now()
        startT = UTCDateTime(year=now.year,month=now.month,day=now.day,hour=0)
        endT = startT + timedelta(hours=24)
        # print(startT, endT)
        if int(now.day) < 10:
            dia = '0' + str(now.day)
        else:
            dia = str(now.day)
        if int(now.month) < 10:
            mes = '0' + str(now.month)
        else:
            mes = str(now.month)
        date = str(dia) + '-' + str(mes) + '-' + str(now.year)
        # st.plot(type='dayplot', interval=15, vertical_scaling_range=5000, one_tick_per_line=False, starttime=startT,
        #         endtime=endT, grid='True', subplots_adjust_left=0.09, subplots_adjust_right=0.98,
        #         subplots_adjust_bottom=0.05,tick_format='%H:00h',
        #         color=['#385970', 'r', 'g', 'b'], show_y_UTC_label=True, size=(900, 800), dpi=100,
        #         title='Volcán: '+ self.volcano + ' Estación: ' + self.stationNameTo+'-' + self.component + '  ' + date,
        #         outfile=self.pathToHelli + self.volcano + '_' +self.stationNameTo + '_' + date + '.svg', format='SVG')
        # self.putLogo(self.pathToHelli + self.volcano + '_' + self.stationNameTo + '_' + date + '.svg', date)
        st.plot(type='dayplot', interval=15, vertical_scaling_range=5000, one_tick_per_line=False, starttime=startT,
                endtime=endT, grid_color='#000000', subplots_adjust_left=0.09, subplots_adjust_right=0.98,
                subplots_adjust_bottom=0.05, tick_format='%H:00h',
                color=['#385970', 'r', 'g', 'b'], show_y_UTC_label=False, size=(900, 800),
                title='', transparent=True,
                outfile=self.pathToHelli + self.volcano + '_' + self.stationNameTo + '_' + date + '4.tiff', format='Tas')
        # self.joinImages(self.pathToHelli + self.volcano + '_' + self.stationNameTo + '_' + date + '1.png')

    def printColor(self, msg, volcano):
        preText = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - [' + str(self.id) + '] '
        postText = ''
        colors = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'RESET']

        if volcano == "Misti":
            print(Fore.BLUE + (preText + msg + postText))

        elif volcano == "Sabancaya":
            print(Fore.YELLOW + (preText + msg + postText))

        elif volcano == "Ubinas":
            print(Fore.CYAN + (preText + msg + postText))

        elif volcano == "Ticsani":
            print(Fore.MAGENTA + (preText + msg + postText))

        elif volcano == "Inuse":
            print(Fore.RED + (preText + msg + postText))
        else:
            print(msg)

    def printParams(self, params):
        pprint(params)
