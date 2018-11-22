# Ricardo Coronado Perez
# rikardo.corp@gmail.com

# #####################    PARAMS    ##############################
# 'path'   : path of the directory of images
#            (the name of the images must be the following format 'Name[year]-[month][day]- [hour][minute][seconds]')
#             for example if the image was taken at 2018-12-24 12:01:00 -> FSB18-1224-120100.jpg
# 'gifPath': path of the output (format .gif)
# 'scale'  : scale [0-1]
# 'isDirectory': True/False,
#                True :if the images are inside a folder
#                False: if we are going to add each image manually with addImage(PathImage)
# 'optimize': True/False,
# 'quality' : [0-100],
# 'frecuency': in seconds,
# 'duration' : [0.01-inf] is the time between each slide,
# 'time'     : ['05:19:00', '14:25:00'] range of time
# ##################################################################

import os
import datetime
import imageio
from PIL import Image
import numpy as np
import shutil
import paramiko
import sys
import cv2

# extensionesde imagen validas
VALID_EXTENSIONS = ('png', 'jpg')
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class CreateGif():

    def __init__(self):
        self.oWidth = 0
        self.oHeight = 0
        self.width = 0
        self.height = 0
        self.scale = 0.5
        self.quality = 80
        self.duration = 0.5
        self.today = ''
        self.automatic = True
        self.path = ''
        self.gifPath = ''
        self.optimize = False
        self.isDirectory = False
        self.temporal = '_temp/'
        self.images = []
        self.totalImages = 0
        self.date = ''
        self.time = []
        self.count = 0
        self.timeFrom = None
        self.timeTo = None
        self.exit = False
        self.lapseTime = 0
        self.frecuency = 0.3
        self.id = 0
        self.cameraName = 'Default'
        self.hostname = None
        self.port = 22
        self.username = ''
        self.password = ''
        self.pathImagesSource = ''
        self.minImagesByWork = 10
        self.gifName = 'default.gif'
        self.gifNameBySend = 'default.gif'
        self.restrict = None
        self.uploadImage = False
        self.deleteOriginalGif = True
        self.isPathDate=True
        self.PATH_DEST_GIF_SERVER = ''
        self.typeOutFile = ''
        self.fps = ''

    def setParams(self, params):
        self.id = params['id']
        self.path = params['path']
        self.automatic = params['automatic']
        self.date = params['date']
        self.time = params['time']
        self.cameraName = params['cameraName']
        self.hostname = params['hostname']
        self.port = int(params['port'])
        self.username = params['username']
        self.password = params['password']
        self.pathImagesSource = params['pathImagesSource']
        self.isDirectory = params['isDirectory']
        self.minImagesByWork = int(params['minImagesByWork'])
        self.gifName = params['gifName']
        self.scale = float(params['scale'])
        self.optimize = params['optimize']
        self.quality = int(params['quality'])
        self.frecuency = int(params['frecuency'])
        self.duration = float(params['duration'])
        self.gifNameBySend = params['gifNameBySend'] + '.' + params['typeOutFile']
        self.gifPath = params['path'] + params['gifName'] + '.' + params['typeOutFile']
        self.restrict = params['restrict']
        self.uploadImage = params['uploadImage']
        self.deleteOriginalGif = params['deleteOriginalGif']
        self.isPathDate = params['isPathDate']
        self.PATH_DEST_GIF_SERVER = params['PATH_DEST_GIF_SERVER']

        self.typeOutFile = params['typeOutFile']
        self.fps = float(params['fps'])

        # definimos los rangos de hora permitidos
        h = self.time[0].split(':')
        self.timeFrom = datetime.time(int(h[0]), int(h[1]), int(h[2]))
        h = self.time[1].split(':')
        self.timeTo = datetime.time(int(h[0]), int(h[1]), int(h[2]))

        # creamos una carpeta temporal para las imagenes optimizadas
        self.temporal = self.path + '_temp/'
        if os.path.exists(self.temporal):
            shutil.rmtree(self.temporal)
        os.makedirs(self.temporal)

        # COMPLETAMOS EL PATH DE RECURSOS SI LAS CARPETAS SON TIPO DATE
        if self.isPathDate:
            self.pathImagesSource = self.pathImagesSource + self.generateDatePath()

    def generateDatePath(self):

        # GENERAMOS LA ESTRUCTURA DE CARPETAS ANIDADAS POR ANIO/MES/DIA/
        self.today = datetime.datetime.now()
        if self.automatic:
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
            return str(year) + '/' + str(mes) + '/' + str(dia) + '/'
        else:
            date = self.date.split('/')
            return date[2] + '/' + date[1] + '/' + date[0] + '/'

    # Genera el tamanio a escala de la imagen en base al dato de entrada 'scale'
    def getResizeParams(self):
        newW = int(self.oWidth * self.scale)
        newH = int(self.oHeight * self.scale)
        self.width = newW
        self.height = newH

    # Abre la imagen original y la redimensiona segun el tamaio escalado self.width y self.height
    def openResizeImage(self, pathImage):

        if self.typeOutFile == 'gif':
            original_image = Image.open(pathImage)
            self.oWidth, self.oHeight = original_image.size
            self.getResizeParams()
            if self.scale < 1:
                original_image = original_image.resize([self.width, self.height], Image.ANTIALIAS)
        else:
            original_image = cv2.imread(pathImage)
            self.oWidth, self.oHeight, layers = original_image.shape
            self.getResizeParams()
            if self.scale < 1:
                original_image = cv2.resize(original_image, (int(self.height), int(self.width)))

        return original_image

    # Agrega una imagen de manera manual a la lista de imagenes que conformaran el gif
    def addImage(self, pathImage):
        # Validamos si la imagen esta dentro del rango de tiempo permitido
        if self.validHour(pathImage):
            image = self.openResizeImage(self.pathImagesSource + pathImage)
            # Verifica si se desea optimizar la imagen
            if self.optimize and self.typeOutFile == 'gif':
                image.save(self.temporal + str(self.count) + '.jpg', optimize=True, quality=self.quality)
                localImage = imageio.imread(self.temporal + str(self.count) + '.jpg')
            else:
                localImage = np.asarray(image)

            strMsg = '- Image #' + str(self.count) + ' ' + pathImage

            self.count = self.count + 1
            self.images.append(np.asarray(localImage))
            plataforma = sys.platform

            if plataforma != 'win32':
                sys.stdout.write(CURSOR_UP_ONE)
                sys.stdout.write(ERASE_LINE)
                print strMsg
            else:
                sys.stdout.write('\r' + strMsg)

    def createGif(self):
        print
        # CONTRASTAMOS QUE LA HORA ACTUAL NO SE ENCUENTRE EN EL RANGO DE LAS RESTRICCIONES
        isRestrict, hourRestrict = self.restrictHour()
        if isRestrict:
            print '- Hora restringida -> ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1])
            return

        # si las imagenes estan dentro de un difrectorio listamos todo el contenido, y filtramos las imagenes permitidas
        if self.isDirectory:
            if not os.path.exists(self.pathImagesSource):
                print '- La ruta de recursos "' + self.pathImagesSource + '" no existe'
                return

            filenames = sorted(os.listdir(self.pathImagesSource))
            for filename in filenames:
                if filename.lower().endswith(VALID_EXTENSIONS):
                    # print filename
                    # en caso de querer escapar del bucle
                    if not self.exit:
                        self.addImage(filename)
                    else:
                        break

        # VERIFICAMOS QUE EXISTAN IMAGENES PARA CREAR EL GIF
        self.totalImages = len(self.images)
        if self.totalImages == 0:
            print '- Las imagenes no cuplen las condicones o el [pathImagesSource] esta vacio'
            return

        # grabamos las lista de imagenes en un archivo de salida con extension .gif
        if self.typeOutFile == 'gif':
            imageio.mimsave(self.gifPath, self.images, duration=self.duration)
            print '- Tiempo de duracion del GIF: ' + str(float(self.totalImages * self.duration)) + ' seg. [' + str(self.totalImages) + ' imagenes]'

        elif self.typeOutFile == 'avi':
            out = cv2.VideoWriter(self.gifPath, cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (self.height, self.width))
            for i in range(self.totalImages):
                # writing to a image array
                out.write(self.images[i])
            out.release()
            print '- Tiempo de duracion del VIDEO[avi]: ' + str(float(self.totalImages / self.fps)) + ' seg. [' + str(self.totalImages) + ' imagenes]'
        elif self.typeOutFile == 'mp4':
            out = cv2.VideoWriter(self.gifPath, cv2.VideoWriter_fourcc(*'MP4V'), self.fps, (self.height, self.width))
            for i in range(self.totalImages):
                # writing to a image array
                out.write(self.images[i])
            out.release()
            print '- Tiempo de duracion del VIDEO[mp4]: ' + str(float(self.totalImages / self.fps)) + ' seg. [' + str(self.totalImages) + ' imagenes]'
        elif self.typeOutFile == 'ogg':
            out = cv2.VideoWriter(self.gifPath, cv2.VideoWriter_fourcc(*'THEO'), self.fps, (self.height, self.width))
            for i in range(self.totalImages):
                # writing to a image array
                out.write(self.images[i])
            out.release()
            print '- Tiempo de duracion del VIDEO[ogg]: ' + str(float(self.totalImages / self.fps)) + ' seg. [' + str(self.totalImages) + ' imagenes]'
        else:
            print '- El typeOutFile no es un valor valido, utilizar solo [gif or avi]'
            return

        # removemos la carpeta temporal
        if os.path.exists(self.temporal):
            shutil.rmtree(self.temporal)

        # UPLOAD IMAGE TO SERVER
        if self.totalImages >= self.minImagesByWork and self.uploadImage:
            self.uploadFile(self.gifPath, self.PATH_DEST_GIF_SERVER + self.gifNameBySend)

        # DELETE ORIGINAL GIF
        if self.deleteOriginalGif:
            os.remove(self.gifPath)
            print('- Original GIF deleted!')

    def validHour(self, filename):
        year = filename[-18:-16]
        month = filename[-15:-13]
        day = filename[-13:-11]

        try:
            hour = int(filename[-10:-8])
            minute = int(filename[-8:-6])
            second = int(filename[-6:-4])
        except:
            return False

        # obtenemos la hora de la imagen por el nombre del archivo
        fileTime = datetime.time(hour, minute, second)
        # validamos que la hora de la imagen sea menor que maximo rango permitido en caso de ser mayor
        # activamos la opcion para escapar del bucle de lectura del directorio
        if fileTime > self.timeTo:
            self.exit = True

        # obtenemos el hora en segundos de la imagen
        newlapseTime = hour * 60 * 60 + minute * 60 + second
        difflapse = newlapseTime - self.lapseTime

        # la frecuencia es el tiempo que debe de transcurrir para agregar otras imagen a la secuencia
        # la difflapse es el tiempo transcurrido en segundos desde la ultima imagen registrada
        if difflapse <= self.frecuency:
            # si no transcurrido el tiempo minimo para registrar otra imagen se inavalida la imagen evaluada
            return False
        else:
            # caso contrario se actualiza tiempo de la ultima imagen registrada
            self.lapseTime = newlapseTime

        # verificamos que la imagen este entre el rango de tiempo permitido
        return self.timeFrom <= fileTime <= self.timeTo

    def restrictHour(self):
        if self.restrict is None:
            return False, []

        # VARIABLE DE ESCAPE DEL BUCLE
        centinel = False
        hourRestrict = []
        localtime = datetime.datetime.now().time()

        # BUCLE PARA LEER EL ARRAY DE RESTRICCIONES
        for r in self.restrict:
            # DESDE
            h = r[0].split(':')
            rtimeFrom = datetime.time(int(h[0]), int(h[1]), int(h[2]))
            # HASTA
            h = r[1].split(':')
            rtimeTo = datetime.time(int(h[0]), int(h[1]), int(h[2]))

            # EVALUAMOS SI LA HORA LOCAL ESTA DENTRO DEL RANGO DE RESTRICCION
            if rtimeFrom < localtime < rtimeTo:
                hourRestrict = r
                centinel = True
                break

        return centinel, hourRestrict

    def uploadFile(self, src, dst):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        print ("- Connecting to %s \n- with username=%s..." % (self.hostname, self.username))
        try:
            t = paramiko.Transport((self.hostname, self.port))
            t.connect(username=self.username, password=self.password)
        except:
            print ('- Error de conexion al servidor.')
            return

        try:
            sftp = paramiko.SFTPClient.from_transport(t)
            print ("- Copying file: %s to path: %s" % (src, dst))
            sftp.put(src, dst)
            print ('- File Copied!!')
            sftp.close()
            t.close()
        except:
            print ('- Error de envio de datos.')

    def listDirectory(self):
        filenames = sorted(os.listdir(self.pathImagesSource))
        print filenames
