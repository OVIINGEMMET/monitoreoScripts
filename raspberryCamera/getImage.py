#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import datetime
import os
from pprint import pprint
import ftplib
from PIL import Image
import watermark
import requests
from requests.auth import HTTPDigestAuth
from clint.textui import progress, colored, puts
# from config import *

SYNC = False

class Camera():
    # DEFINICION DE VARIABLES
    def __init__(self):
        self.type = 'camera'
        self.id = 0
        self.cameraName = ''
        self.title = ''
        self.url = ''
        self.auth = True
        self.timer = 60
        self.user = ''
        self.password = ''
        self.directory = ''
        self.prenameFile = ''
        self.enable = True
        self.restrict = None
        self.today = None
        self.filename = ''
        self.filenamePath = ''
        self.watermark = False
        self.GLOBALPATH = ''
        self.PATH_LOGO = ''
        self.FONT = None
        self.isWorking = False
        self.date = None
        self.timeout = 5
        self.urlUp = ''
        self.ftpPathUp = ''
        self.ftpHost = ''
        self.ftpUser = ''
        self.ftpPass = ''
        self.destroyImageOriginal = False

        self.fontSize = 12
        self.sizeLogo = 100

    def __del__(self):
        print ("del Camera")

    # INICIALIZACION DE VARIABLES
    def setParameters(self, params):
        self.type = params['type']
        # [STRING] ID DE LA CAMARA
        self.id = params['id']
        # [STRING] NOMBRE IDENTIFICADOR DE LA CAMARA
        self.cameraName = params['cameraName']
        # [STRING] TITULO QUE IRA IMPRESO EN LA IMAGEN
        self.title = params['title']
        # [STRING] TAMAÑO DE LA FUENTE
        self.fontSize = int(params['fontSize'])
        # [STRING] TAMAÑO DE LA FUENTE
        self.sizeLogo = int(params['sizeLogo'])
        # [STRING] IP O URL DEL ORIGEN DE LA IMAGEN A DESCARGAR
        self.url = params['url']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE PETICION HTTPS POST
        self.urlUp = params['urlUp']

        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE FTP
        self.ftpPathUp = params['ftpPathUp']
        self.ftpHost = params['ftpHost']
        self.ftpUser = params['ftpUser']
        self.ftpPass = params['ftpPass']

        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        # [BOOL] SI LA CONEXON REQUIERE AUTENTICACION
        self.auth = params['auth']
        # [STRING] USERNAME AUTENTICACION
        self.user = params['user']
        # [STRING] PASSWORD AUTENTICACION
        self.password = params['password']
        # [STRING] CARPETA DONDE SE ALMACENARAN LAS IMAGENES, EJEMPLO misImagenes/
        self.directory = params['directory']
        # [STRING] PREFIJO PARA NOMBRE DEL ARCHIVO
        self.prenameFile = params['prenameFile']
        # [BOOL] HABILITA O DESHABILITA UNA CAMARA
        self.enable = params['enable']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        self.restrict = params['restrict']
        # [BOOL] PARA AGREGAR MARCA DE AGUA A LA IMAGEN
        self.watermark = params['watermark']
        # [STRING] PATH O RUTA ABSOLUTA DONDE SE ALMACENARA LA CARPETA DE IMAGENES, EJEMPLO home/user1/imagenes/
        self.GLOBALPATH = params['GLOBALPATH']
        # [STRING] PATH O RUTA ABSOLUTA DEL LOGO
        self.PATH_LOGO = params['PATH_LOGO']
        # [STRING/NULL] PATH O RUTA DE LA FUENTE DE LETRA PARA LOS TITULOS
        self.FONT = params['FONT']
        # [INT] TIMEPO MAXIMO DE ESPERA PARA SOLICITAR UNA IMAGEN
        self.timeout = params['timeout']
        self.destroyImageOriginal = params['destroyImageOriginal']

    def setSynchronizer(self, params):
        self.type = params['type']
        # [STRING] ID DE LA CAMARA
        self.id = params['id']
        # [STRING] PATH O RUTA ABSOLUTA DONDE SE ALMACENARA LA CARPETA DE IMAGENES, EJEMPLO home/user1/imagenes/
        self.GLOBALPATH = params['GLOBALPATH']
        # [STRING] NOMBRE IDENTIFICADOR DE LA CAMARA
        self.cameraName = params['cameraName']
        # [BOOL] HABILITA O DESHABILITA UNA CAMARA
        self.enable = params['enable']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE FTP
        self.ftpPathUp = params['ftpPathUp']
        self.ftpHost = params['ftpHost']
        self.ftpUser = params['ftpUser']
        self.ftpPass = params['ftpPass']
        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        self.restrict = params['restrict']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE PETICION HTTPS POST
        self.urlUp = params['urlUp']
        self.destroyImageOriginal = params['destroyImageOriginal']

    def printParams(self, params):
        pprint(params)

    def printColor(self, msg, index=0):
        idx = int(int(self.id) % 7)
        preText = '   -[' + str(self.id) + ']'
        postText = ''
        colors = ['magenta', 'cyan', 'green', 'yellow', 'blue', 'red', 'white']

        if idx == 0:
            print(colored.magenta(preText + msg + postText))
        elif idx == 1:
            print(colored.cyan(preText + msg + postText))

        elif idx == 2:
            print(colored.green(preText + msg + postText))

        elif idx == 3:
            print(colored.yellow(preText + msg + postText))

        elif idx == 4:
            print(colored.blue(preText + msg + postText))

        elif idx == 5:
            print(colored.red(preText + msg + postText))

        elif idx == 6:
            print(colored.white(preText + msg + postText))

    def getImage(self):

        # VERIFICAMOS SI LA CAMARA ESTA HABILITADA EN LA CONFIGURACION DEL ARCHIVO config.ini
        if self.enable:
            self.isWorking = True
            puts(colored.cyan('[GET IMAGE: ' + str(self.cameraName) + ' >> ' + str(self.url)))

            # CONTRASTAMOS QUE LA HORA ACTUAL NO SE ENCUENTRE EN EL RANGO DE LAS RESTRICCIONES
            isRestrict, hourRestrict = self.restrictHour()
            if isRestrict:
                self.isWorking = False
                puts(colored.yellow('     - Hora restringida -> ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1])))
            else:

                # GENERAMOS EL PATH DE SALIDA PARA LA NUEVA IMAGEN
                self.generateDatePath()
                toPath = self.GLOBALPATH + str(self.directory) + self.filenamePath
                if not os.path.exists(toPath):
                    os.makedirs(toPath)
                toPathFilename = toPath + str(self.filename)
                puts(colored.yellow('     - to path >> ' + toPathFilename))
                # ------------------------------------------------

                # VALIDAMOS QUE LA CONEXION CON EL SERVICIO REQUIERE AUTENTICACION
                if self.auth:
                    cen = self.saveImage(toPathFilename)
                else:
                    cen = self.saveImage_urllib2(toPathFilename)
                # ----------------------------------------------------------------

                self.isWorking = False

                # CONDICIONAL PARA AGREGAR MARCA DE AGUA CON LOGOTIPO INSTITUCIONAL Y CABECERA
                if cen and self.watermark:
                    self.pasteLogo(toPathFilename)
                # -----------------------------------------------------------------------------

                # CONDICIONAL: SI CONFIGURAMOS UN URLUP SUBIREMOS LA IMAGEN MEDIANTE UN SERVICIO WEB
                if cen and self.urlUp is not False:
                    try:
                        files = {'file': open(toPathFilename, 'rb')}
                        puts(colored.cyan('     - uploading image...'))
                        puts(colored.yellow('         [' + self.urlUp + ']'))
                        response = requests.post(self.urlUp, files=files)
                        puts(colored.green('     - uploaded image!! ' + str(response.status_code)))
                    except:
                        puts(colored.green('     - upload Error!! '))
                # -----------------------------------------------------------------------------

            puts(colored.cyan(' END]'))
            print
        else:
            self.isWorking = False

    def getImageThread(self):

        # VERIFICAMOS SI LA CAMARA ESTA HABILITADA EN LA CONFIGURACION DEL ARCHIVO config.ini
        if self.enable:
            self.isWorking = True
            self.date = datetime.datetime.now()
            self.printColor(str(self.date) + '->' + str(self.cameraName) + ' > ' + str(self.url), self.id)

            # CONTRASTAMOS QUE LA HORA ACTUAL NO SE ENCUENTRE EN EL RANGO DE LAS RESTRICCIONES
            isRestrict, hourRestrict = self.restrictHour()
            if isRestrict:
                self.isWorking = False
                self.printColor(str(self.date) + '-> Hora restringida ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1]), self.id)
            else:
                # GENERAMOS EL PATH DE SALIDA PARA LA NUEVA IMAGEN
                self.generateDatePath()
                toPath = self.GLOBALPATH + str(self.directory) + self.filenamePath
                if not os.path.exists(toPath):
                    os.makedirs(toPath)
                toPathFilename = toPath + str(self.filename)
                # ------------------------------------------------

                # OBTENEMOS EL ESTADO DE L DESCARGA
                cen = self.saveImageSimple(toPathFilename, thread=True)
                self.isWorking = False
                # SI LA DESCARGA SE REALIZA CON EXITO SE EVALUA SI REQUIERE MARCA DE AGUA
                if cen and self.watermark:
                    self.pasteLogo(toPathFilename, thread=True)

                # CONDICIONAL: SI CONFIGURAMOS UN URLUP SUBIREMOS LA IMAGEN MEDIANTE UN SERVICIO WEB
                if cen and self.urlUp is not None:
                    self.sendWEB(toPath, str(self.filename))

                # CONDICIONAL: SI SE DESEA ENVIAR LA IMAGEN POR FTP
                if cen and self.ftpPathUp is not None:
                    origin = self.GLOBALPATH + str(self.directory) + self.filenamePath
                    dest = self.ftpPathUp + str(self.directory) + self.filenamePath
                    self.sendFTP(origin, dest, self.filename)


            # -----------------------------------------------------------------------------------
        else:
            self.isWorking = False

    def sendWEB(self, path, filename):
        try:
            files = {'file': open(path + filename, 'rb')}
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploading image web...', self.id)
            requests.post(self.urlUp, files=files)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploaded image[' + filename + ']!!', self.id)
        except:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> upload Error!!', self.id)

    def sendFTP(self, source, dest, filename):
        self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploading image FTP:'+ self.ftpUser + '@' + self.ftpHost, self.id)
        try:
            FTP = ftplib.FTP(self.ftpHost)
            FTP.login(self.ftpUser, self.ftpPass)
            FTP.cwd('/')
        except:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploading Error Connection!!', self.id)
            return False
        try:
            FTP.cwd(dest)
        except:
            FTP.mkd(dest)
            FTP.cwd(dest)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploading Create Directory!', self.id)

        try:
            uploadfile = open(source + filename, 'rb')
            FTP.storbinary('STOR ' + filename, uploadfile)
        except:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploading Error Saving!!', self.id)
            return False

        if self.destroyImageOriginal:
            os.remove(source + filename)

        self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploaded Image!!', self.id)
        return True

    def synchronizeLocal(self):
        self.date = datetime.datetime.now()
        # CONTRASTAMOS QUE LA HORA ACTUAL NO SE ENCUENTRE EN EL RANGO DE LAS RESTRICCIONES
        isRestrict, hourRestrict = self.restrictHour()
        if isRestrict:
            self.isWorking = False
            self.printColor(str(self.date) + '-> Hora restringida ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1]), self.id)
        else:
            self.taverseLocal()

    def taverseLocal(self):
        for root, subFolder, files in os.walk(self.GLOBALPATH):
            # print root, subFolder
            for item in files:
                if item.endswith('.jpg'):
                    origin = root + '/'
                    dest = self.ftpPathUp + origin.replace(self.GLOBALPATH, '')
                    if self.urlUp is not None:
                        self.sendWEB(origin, item)

                    self.sendFTP(origin, dest, item)

                    # print origin
                    # print dest
                    # print item
                    # print '------------------------------------'
                # if item.endswith(".jpg"):
                #     fileNamePath = str(os.path.join(root, subFolder, item))
                #     print fileNamePath

    def traverseFTP(self, ftp, depth=0):
        # RECORRE TODO EL ARBOL DE CARPETAS DE UNA HOST FTP
        if depth > 4:
            return ['depth > 10']
        level = {}
        for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
            try:
                ftp.cwd(entry)
                level[entry] = self.traverse(ftp, depth + 1)
                ftp.cwd('..')
            except ftplib.error_perm:
                level[entry] = None
        return level

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

    def authenticated(self):
        # Create a password manager
        manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        manager.add_password(None, self.url, self.user, self.password)
        # Create an authentication handler using the password manager
        authlocal = urllib2.HTTPBasicAuthHandler(manager)
        # Create an opener that will replace the default urlopen method on further calls
        opener = urllib2.build_opener(authlocal)
        urllib2.install_opener(opener)

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
        self.filenamePath = str(year) + '/' + str(mes) + '/' + str(dia) + '/'
        # ---------------------------------------------------------------

        # GENERAMOS EL NOMBRE DEL ARCHIVO DE SALIDA
        format = "%y-%m%d-%H%M%S"
        nameFile = datetime.datetime.now().strftime(format)
        self.filename = str(self.prenameFile) + nameFile + '.jpg'
        # ---------------------------------------------------------------

    def pasteLogo(self, toPath, thread=False):

        if self.today is None:
            # FECHA DE REGISTRO DE LA IMAGEN
            self.today = datetime.datetime.strptime(toPath.split('/')[-1][3:17], "%y-%m%d-%H%M%S")

        try:
            water = watermark.Watermark()
            water.setParamsLineal(logoPath=self.PATH_LOGO, imagePath=toPath, output=toPath, title=self.title, style=4,
                                  font=self.FONT, fontsize=self.fontSize, sizeLogo=self.sizeLogo)
            water.makeWatermark(date=self.today)
            # watermark.showImage()

            if not thread:
                puts(colored.green('     - edit image!!'))
        except:
            if thread:
                self.printColor(str(self.date) + '-> Error editting: la imagen incompleta!', self.id)
            else:
                puts(colored.red('     - Error editting: la imagen podria estar dañada.'))

    def saveImage_urllib2(self, toPathFilename, thread=False):
        if not thread:
            puts(colored.cyan('     - saving image...'))

        try:
            # PETICION AL SERVIDOR PARA DESCARGAR IMAGEN SIN AUTENTICACION
            response = urllib2.urlopen(self.url)
            localFile = open(toPathFilename, 'wb')
            localFile.write(response.read())
            localFile.close()
            if thread:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> saved image!', self.id)
            else:
                puts(colored.green('     - saved image!'))
            return True
            # -------------------------------------------------------------

        except IOError as e:
            if thread:
                self.printColor(str(self.date) + '-> Error saving: el servidor esta desconectado!', self.id)
            else:
                puts(colored.red('     - Error saving: el servidor esta desconectado'))
            return False

    def saveImage(self, toPathFilename, thread=False):
        if not thread:
            puts(colored.cyan('     - saving image...'))

        try:
            # PETICION AL SERVIDOR PARA DESCARGAR IMAGEN CON DOWNLOAD BAR
            r = requests.get(self.url, stream=True,  auth=HTTPDigestAuth(self.user, self.password), timeout=int(self.timeout))
            with open(toPathFilename, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1, label="       Downloading "):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            puts(colored.green('     - saved image!'))
            return True
            # ------------------------------------------------------------
        except:
            puts(colored.red('     - Error saving: el servidor esta desconectado'))
            return False

    def saveImageSimple(self, toPathFilename, thread=False):
        if not thread:
            puts(colored.cyan('     - saving image...'))

        try:
            # CONDICIONAL PARA PETICIONES CON Y SIN AUTENTICACION
            if self.auth:
                r = requests.get(self.url, auth=HTTPDigestAuth(self.user, self.password), timeout=int(self.timeout))
            else:
                r = requests.get(self.url, timeout=int(self.timeout))

            # EVALUAMOS SI LA IMAGEN SE DESCARGO CON EXITO
            if r.status_code == 200:
                localFile = open(toPathFilename, 'wb')
                localFile.write(r.content)
                localFile.close()
                if thread:
                    self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> saved image!', self.id)
                else:
                    puts(colored.green('     - saved image!'))
                return True
            else:
                if thread:
                    self.printColor(str(self.date) + '-> Error saving: el servidor esta desconectado!!', self.id)
                else:
                    puts(colored.red('     - Error saving: el servidor esta desconectado!!'))
                return False
            # ---------------------------------------------

        except:
            if thread:
                self.printColor(str(self.date) + '-> Error saving: el servidor esta desconectado!', self.id)
            else:
                puts(colored.red('     - Error saving: el servidor esta desconectado'))
            return False
