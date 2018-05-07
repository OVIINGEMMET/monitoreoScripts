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

# extensionesde imagen validas
VALID_EXTENSIONS = ('png', 'jpg')


class CreateGif():

    def __init__(self):
        self.oWidth = 0
        self.oHeight = 0
        self.width = 0
        self.height = 0
        self.scale = 0.5
        self.quality = 80
        self.duration = 0.5
        self.path = ''
        self.gifPath = ''
        self.optimize = False
        self.isDirectory = False
        self.temporal = '_temp/'
        self.images = []
        self.time = []
        self.count = 0
        self.timeFrom = None
        self.timeTo = None
        self.exit = False
        self.lapseTime = 0
        self.frecuency = 0.3

    def setParams(self, params):
        self.scale = params['scale']
        self.path = params['path']
        self.gifPath = params['gifPath']
        self.optimize = params['optimize']
        self.isDirectory = params['isDirectory']
        self.quality = params['quality']
        self.duration = params['duration']
        self.time = params['time']
        self.frecuency = params['frecuency']

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

    # Genera el tamanio a escala de la imagen en base al dato de entrada 'scale'
    def getResizeParams(self):
        newW = int(self.oWidth * self.scale)
        newH = int(self.oHeight * self.scale)
        self.width = newW
        self.height = newH

    # Abre la imagen original y la redimensiona segun el tamaio escalado self.width y self.height
    def openResizeImage(self, pathImage):
        original_image = Image.open(pathImage)
        self.oWidth, self.oHeight = original_image.size
        self.getResizeParams()
        resized_image = original_image.resize([self.width, self.height], Image.ANTIALIAS)
        return resized_image

    # Agrega una imagen de manera manual a la lista de imagenes que conformaran el gif
    def addImage(self, pathImage):
        # Validamos si la imagen esta dentro del rango de tiempo permitido
        if self.validHour(pathImage):
            image = self.openResizeImage(self.path + pathImage)
            # Verifica si se desea optimizar la imagen
            if self.optimize:
                image.save(self.temporal + str(self.count) + '.jpg', optimize=True, quality=self.quality)
                localImage = imageio.imread(self.temporal + str(self.count) + '.jpg')
                self.count = self.count + 1
            else:
                localImage = np.asarray(image)

            self.images.append(np.asarray(localImage))
            print pathImage

    def createGif(self):

        # si las imagenes estan dentro de un difrectorio listamos todo el contenido, y filtramos las imagenes permitidas
        if self.isDirectory:
            filenames = sorted(os.listdir(self.path))
            for filename in filenames:
                if filename.lower().endswith(VALID_EXTENSIONS):
                    # en caso de querer escapar del bucle
                    if not self.exit:
                        self.addImage(filename)
                    else:
                        break

        # grabamos las lista de imagenes en un archivo de salida con extension .gif
        imageio.mimsave(self.gifPath, self.images, duration=self.duration)
        # removemos la carpeta temporal
        shutil.rmtree(self.temporal)
        print 'Tiempo de duracion: ' + str(float(self.count * self.duration)) + ' seg.'

    def validHour(self, filename):
        year = filename[-18:-16]
        month = filename[-15:-13]
        day = filename[-13:-11]
        hour = int(filename[-10:-8])
        minute = int(filename[-8:-6])
        second = int(filename[-6:-4])

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
        if difflapse < self.frecuency:
            # si no transcurrido el tiempo minimo para registrar otra imagen se inavalida la imagen evaluada
            return False
        else:
            # caso contrario se actualiza tiempo de la ultima imagen registrada
            self.lapseTime = newlapseTime

        # verificamos que la imagen este entre el rango de tiempo permitido
        return self.timeFrom <= fileTime <= self.timeTo

    def listDirectory(self):
        filenames = sorted(os.listdir(self.path))
        print filenames
