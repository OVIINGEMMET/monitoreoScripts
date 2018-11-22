#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import datetime
import os
import sys
from pprint import pprint
import ftplib
import stat
# from collections import defaultdict
# from PIL import Image
import watermark
import requests
import time
import shutil
from requests.auth import HTTPDigestAuth

try:
    import paramiko
    PARAMIKOLOAD = True
except:
    print 'Not import paramiko - SSH connection'
    PARAMIKOLOAD = False

try:
    from clint.textui import progress, colored, puts
    COLORED = True
except:
    print 'Not from clint.textui import progress, colored, puts'
    COLORED = False
# from config import *

SYNC = False
VALID_EXTENSIONS = ('png', 'jpg')


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

        self.remoteConnect = ''
        self.remotePathUp = ''
        self.remoteHost = ''
        self.remotePort = ''
        self.remoteUser = ''
        self.remotePass = ''
        self.destroyImageOriginal = False

        self.fontSize = 12
        self.sizeLogo = 100
        self.SWITCH = True
        self.EXEC = [None, None]

        self.watermarkScale = False
        self.pathScale = ''
        self.axisX = 0
        self.axisY = 0
        self.filenameUp = None

        self.sourcePath = ''
        self.outcomePath = ''
        self.frequency = None
        self.copySpecial = ''
        self.delay = 1
        self.analysis = True
        self.rebootError = None

        self.isRange = False
        self.days = 1
        self.dateTimeFrom = ''
        self.dateTimeTo = ''
        self.timeFrom = ''
        self.timeTo = ''
        self.lapseTime = 0
        self.exit = False

        self.countErrors = 0
        self.totalCountErrors = 0
        self.errorTraverseSSH = 0
        self.errorTraverseFTP = 0
        self.postName = ''

        # def __del__(self):
    #     print ("del Camera")

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
        self.remoteConnect = params['remoteConnect']
        self.remotePathUp = params['remotePathUp']
        self.remoteHost = params['remoteHost']
        self.remotePort = int(params['remotePort'])
        self.remoteUser = params['remoteUser']
        self.remotePass = params['remotePass']

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
        try:
            self.rebootError = int(params['rebootError'])
        except:
            self.rebootError = None

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

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
        self.remoteConnect = params['remoteConnect']
        self.remotePathUp = params['remotePathUp']
        self.remoteHost = params['remoteHost']
        self.remotePort = int(params['remotePort'])
        self.remoteUser = params['remoteUser']
        self.remotePass = params['remotePass']
        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        self.delay = params['delay']
        self.analysis = params['analysis']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        self.restrict = params['restrict']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE PETICION HTTPS POST
        self.urlUp = params['urlUp']
        self.destroyImageOriginal = params['destroyImageOriginal']

        try:
            self.rebootError = int(params['rebootError'])
        except:
            self.rebootError = None

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

    def setSynchronizerServerToLocal(self, params):
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
        self.remoteConnect = params['remoteConnect']
        self.remotePathUp = params['remotePathUp']
        self.remoteHost = params['remoteHost']
        self.remotePort = int(params['remotePort'])
        self.remoteUser = params['remoteUser']
        self.remotePass = params['remotePass']
        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        # self.delay = params['delay']
        # self.analysis = params['analysis']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        self.restrict = params['restrict']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE PETICION HTTPS POST
        self.urlUp = params['urlUp']
        self.destroyImageOriginal = params['destroyImageOriginal']
        try:
            self.rebootError = int(params['rebootError'])
        except:
            self.rebootError = None

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

    def setSyncronizerWEB(self, params):
        self.type = params['type']
        # [STRING] ID DE LA CAMARA
        self.id = params['id']
        # [STRING] PATH O RUTA ABSOLUTA DONDE SE ALMACENARA LA CARPETA DE IMAGENES, EJEMPLO home/user1/imagenes/
        self.GLOBALPATH = params['GLOBALPATH']
        # [STRING] NOMBRE IDENTIFICADOR DE LA CAMARA
        self.cameraName = params['cameraName']
        # [BOOL] HABILITA O DESHABILITA UNA CAMARA
        self.enable = params['enable']
        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        self.restrict = params['restrict']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE PETICION HTTPS POST
        self.urlUp = params['urlUp']
        self.directory = params['directory']
        self.SWITCH = params['SWITCH']

        self.watermarkScale = params['watermarkScale']
        self.pathScale = params['pathScale']
        self.axisX = params['axisX']
        self.axisY = params['axisY']
        self.filenameUp = params['filenameUp']
        try:
            self.rebootError = int(params['rebootError'])
        except:
            self.rebootError = None

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

    def setSyncronizerLocalToServer(self, params):
        self.type = params['type']
        # [STRING] ID DE LA CAMARA
        self.id = params['id']
        # [STRING] PATH O RUTA ABSOLUTA DONDE SE ALMACENARA LA CARPETA DE IMAGENES, EJEMPLO home/user1/imagenes/
        self.GLOBALPATH = params['GLOBALPATH']
        # [STRING] NOMBRE IDENTIFICADOR DE LA CAMARA
        self.cameraName = params['cameraName']
        # [BOOL] HABILITA O DESHABILITA UNA CAMARA
        self.enable = params['enable']
        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        self.restrict = params['restrict']
        # [STRING] URL O SERVICIO PARA SUBIR LA IMAGEN A UN SERVIDOR EXTERNO MEDIANTE FTP
        self.remoteConnect = params['remoteConnect']
        self.remotePathUp = params['remotePathUp']
        self.remoteHost = params['remoteHost']
        self.remotePort = int(params['remotePort'])
        self.remoteUser = params['remoteUser']
        self.remotePass = params['remotePass']
        self.watermarkScale = params['watermarkScale']
        self.pathScale = params['pathScale']
        self.axisX = params['axisX']
        self.axisY = params['axisY']
        self.filenameUp = params['filenameUp']

        self.directory = params['directory']
        try:
            self.rebootError = int(params['rebootError'])
        except:
            self.rebootError = None

        self.SWITCH = params['SWITCH']
        self.EXEC = params['EXEC']

    def setGenerateScale(self, params):
        self.type = params['type']
        # [STRING] ID DE LA CAMARA
        self.id = params['id']
        # [STRING] PATH O RUTA ABSOLUTA DONDE SE ALMACENARA LA CARPETA DE IMAGENES, EJEMPLO home/user1/imagenes/
        self.GLOBALPATH = params['GLOBALPATH']
        # [STRING] NOMBRE IDENTIFICADOR DE LA CAMARA
        self.cameraName = params['cameraName']
        # [BOOL] HABILITA O DESHABILITA UNA CAMARA
        self.enable = params['enable']
        # [INT] PERIODO DE TIEMPO PARA VOLVER A HACER LA PETICION DE UNA IMAGEN
        self.timer = params['timer']
        # [ARRAY] RESTRICIONES DE HORA, LOS RANGOS DENTRO DE ESTE ARRAY NO DESCARGARAN IMAGENES
        # EJEMPLO: [[00:00:00, 04:00:12],[07:51:19, 09:40:41]]
        # self.restrict = params['restrict']

        # self.watermarkScale = params['watermarkScale']
        self.pathScale = params['pathScale']
        self.axisX = params['axisX']
        self.axisY = params['axisY']

        self.sourcePath = params['sourcePath']
        self.outcomePath = params['outcomePath']
        self.postName = params['postName']
        self.isRange = params['isRange']
        self.days = params['days']
        self.dateTimeFrom = params['dateTimeFrom']
        self.dateTimeTo = params['dateTimeTo']
        self.SWITCH = params['SWITCH']

        self.frequency = params['frequency']
        if self.frequency is not None:
            self.frequency = int(self.frequency)

    def printParams(self, params):
        pprint(params)

    def printColor(self, msg, index=0):
        if COLORED:
            idx = int(int(self.id) % 7)
        else:
            idx = None
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
        else:
            print (preText + msg + postText)

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
                    try:
                        os.makedirs(toPath)
                    except:
                        self.printColor(str(self.date) + '->' + str(
                            self.cameraName) + '-> LOCAL Create Directory Error [' + dest + ']!!', self.id)
                        return False
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
                if cen and self.urlUp is not None:
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
                if cen and self.remoteConnect is not None:
                    origin = self.GLOBALPATH + str(self.directory) + self.filenamePath
                    dest = self.remotePathUp + str(self.directory) + self.filenamePath
                    if self.remoteConnect == 'FTP':
                        self.sendFTP(origin, dest, self.filename)
                    else:
                        self.sendSSH(origin, dest, self.filename)

            # -----------------------------------------------------------------------------------
        else:
            self.isWorking = False

    def sendWEB(self, path, filename):
        try:
            files = {'file': open(path + filename, 'rb')}
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploading image web...', self.id)
            response = requests.post(self.urlUp, files=files)
            if response.status_code == 200:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> uploaded image[' + filename + ']!!', self.id)
            else:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> upload Server Error!!', self.id)
        except:
            self.countErrors = self.countErrors + 1
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> upload Error!!', self.id)

    def connectFTP(self):
        self.printColor(
            str(self.date) + '->' + str(self.cameraName) + '-> FTP Connect:' + self.remoteUser + '@' + self.remoteHost,
            self.id)
        try:
            FTP = ftplib.FTP(self.remoteHost)
            FTP.login(self.remoteUser, self.remotePass)
            plataforma = sys.platform
            if plataforma != 'win32':
                FTP.set_pasv(False)

            FTP.cwd('/')
            return True, FTP
        except:
            self.countErrors = self.countErrors + 1
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> FTP Error Connection!!', self.id)
            return False, None

    def sendFTP(self, source, dest, fileSource, fileDest=None, FTP=None):
        localClose = False
        if FTP is None:
            state, FTP = self.connectFTP()
            if state is False:
                return False
            localClose = True

        fnameSource = fileSource
        if fileDest is None:
            fnameDest = fileSource
        else:
            fnameDest = fileDest

        try:
            FTP.cwd(dest)
        except:

            try:
                FTP.mkd(dest)
                FTP.cwd(dest)
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> FTP uploading Create Directory! ' + dest, self.id)
            except:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> FTP You need permission to create folders!' + dest, self.id)
                return False

        try:
            uploadfile = open(source + fnameSource, 'rb')
            FTP.storbinary('STOR ' + fnameDest, uploadfile)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> FTP uploaded Image[' + fileSource + ']!!',self.id)
        except:
            self.countErrors = self.countErrors + 1
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> FTP uploading Error Saving[' + fileSource + ']!!', self.id)
            return False

        if self.destroyImageOriginal:
            try:
                os.remove(source + fileSource)
            except:
                pass

        if localClose:
            FTP.quit()

        return True

    def connectSSH(self):

        if PARAMIKOLOAD is False:
            self.printColor(str(self.date) + '->' + str(
                self.cameraName) + '-> SSH Connect: ERROR no IMPORT PARAMIKO', self.id)
            sys.exit(0)

        self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> SSH Connect:' + self.remoteUser + '@' + self.remoteHost + ':' + str(self.remotePort), self.id)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        try:
            t = paramiko.Transport((self.remoteHost, self.remotePort))
            t.connect(username=self.remoteUser, password=self.remotePass)
            sftp = paramiko.SFTPClient.from_transport(t)
            return True, sftp, t
        except:
            self.countErrors = self.countErrors + 1
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> SSH Error Connection!!', self.id)
            return False, None, None

    def sendSSH(self, source, dest, fileSource, fileDest=None, sftp=None, t=None):
        localClose = False
        if sftp is None:
            state, sftp, t = self.connectSSH()
            if state is False:
                return False
            localClose = True

        try:
            sftp.chdir(dest)  # Test if remote_path exists
        except IOError:
            self.mkdir_p(sftp, dest)
            # sftp.mkdir(dest)  # Create remote_path
            sftp.chdir(dest)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> SSH uploading Create Directory!', self.id)

        fnameSource = fileSource
        if fileDest is None:
            fnameDest = fileSource
        else:
            fnameDest = fileDest

        try:
            sftp.put(source + fnameSource, fnameDest)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> SSH uploaded Image[' + fnameSource + ']!!',self.id)
        except:
            self.countErrors = self.countErrors + 1
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> SSH uploading Error Saving[' + fnameSource + ']!!', self.id)
            return False

        if self.destroyImageOriginal:
            try:
                os.remove(source + fnameSource)
            except:
                pass

        if localClose:
            sftp.close()
            t.close()

        return True

    def sendLOCAL(self, source, dest, filename):

        if self.evaluateFile(source + filename):
            if not os.path.exists(dest):
                try:
                    os.makedirs(dest)
                except:
                    self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> LOCAL Create Directory Error [' + dest + ']!!', self.id)
                    return False
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> LOCAL Create Directory! ' + dest, self.id)
            try:
                if sys.platform == 'win32':
                    shutil.copy2(source + filename, dest + filename)
                else:
                    os.popen(self.copySpecial + ' ' + source + filename + ' ' + dest + filename)

                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> LOCAL copied Image[' + filename + ']!!', self.id)
            except:
                self.countErrors = self.countErrors + 1
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> LOCAL Copying Error Saving[' + filename + ']!!', self.id)
                return False

            if self.destroyImageOriginal:
                try:
                    os.remove(source + filename)
                except:
                    pass

        return True

    def mkdir_p(self, sftp, remote_directory):
        """Change to this directory, recursively making new folders if needed.
        Returns True if any folders were created."""
        if remote_directory == '/':
            # absolute path so change directory to root
            sftp.chdir('/')
            return
        if remote_directory == '':
            # top-level relative directory must exist
            return
        try:
            sftp.chdir(remote_directory)  # sub-directory exists
        except IOError:
            dirname, basename = os.path.split(remote_directory.rstrip('/'))
            self.mkdir_p(sftp, dirname)  # make parent directories
            sftp.mkdir(basename)  # sub-directory missing, so created it
            sftp.chdir(basename)
            return True

    # SINCRONIZA TODOS LOS ARCHIVOS DE DIRECTORIOS Y SUBDIRECTORIOS DE LOCAL A UN SERVIDOR
    def synchronizeLocal(self):
        self.countErrors = 0
        self.date = datetime.datetime.now()
        self.printColor(str(self.date) + '->' + str(self.cameraName), self.id)
        # CONTRASTAMOS QUE LA HORA ACTUAL NO SE ENCUENTRE EN EL RANGO DE LAS RESTRICCIONES
        isRestrict, hourRestrict = self.restrictHour()
        if isRestrict:
            self.isWorking = False
            self.printColor(str(self.date) + '-> Hora restringida ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1]), self.id)
        else:
            self.traverseLocal()
        self.rebootByError()

    def traverseLocal(self):
        FTP = None
        sftp = None
        t = None

        if self.remoteConnect == 'FTP':
            state, FTP = self.connectFTP()
        elif self.remoteConnect == 'SSH':
            state, sftp, t = self.connectSSH()
        elif self.remoteConnect == 'LOCAL':
            plataforma = sys.platform
            if plataforma == 'win32':
                self.copySpecial = 'copy'
            else:
                self.copySpecial = 'cp'
            state = True
        else:
            self.printColor(str(self.date) + '-> Elija un protocolo de conexion permitido [FTP, SSH, LOCAL]', self.id)
            return

        if state is False:
            return

        if self.analysis:
            sources = self.analysisFilesInPath(self.GLOBALPATH)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Delay ' + str(self.delay) + ' seconds', self.id)
            time.sleep(float(self.delay))
            for dir in sources:
                origin = self.GLOBALPATH + dir['path']
                dest = self.remotePathUp + dir['path']
                for item in dir['files']:
                    if self.urlUp is not None:
                        self.sendWEB(origin, item)

                    # print origin, dest, item
                    if self.remoteConnect == 'FTP':
                        self.sendFTP(origin, dest, item, FTP=FTP)
                    elif self.remoteConnect == 'SSH':
                        self.sendSSH(origin, dest, item, sftp=sftp, t=t)
                    elif self.remoteConnect == 'LOCAL':
                        self.sendLOCAL(origin, dest, item)
                    else:
                        return
        else:

            sources = os.walk(self.GLOBALPATH)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Delay ' + str(self.delay) + ' seconds', self.id)
            time.sleep(float(self.delay))
            for root, subFolder, files in sources:
                for item in files:
                    if item.lower().endswith(VALID_EXTENSIONS):
                        origin = (root + '/').replace('\\', "/")
                        if self.urlUp is not None:
                            self.sendWEB(origin, item)

                        dest = self.remotePathUp + origin.replace(self.GLOBALPATH, '')

                        if self.remoteConnect == 'FTP':
                            self.sendFTP(origin, dest, item, FTP=FTP)
                        elif self.remoteConnect == 'SSH':
                            self.sendSSH(origin, dest, item, sftp=sftp, t=t)
                        elif self.remoteConnect == 'LOCAL':
                            self.sendLOCAL(origin, dest, item)
                        else:
                            return

        if self.remoteConnect == 'FTP':
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> FTP Disconnected!!', self.id)
            FTP.quit()
        elif self.remoteConnect == 'SSH':
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> SSH Disconnected!!', self.id)
            sftp.close()
            t.close()

    def analysisFilesInPath(self, PATH):
        routes = []
        total = 0
        self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Analyzing [' + PATH + ']... ', self.id)
        for root, subFolder, files in os.walk(PATH):
            # print root, subFolder
            origin = (root + '/').replace('\\', "/")
            directories = origin.replace(PATH, '')
            listFiles = []
            for item in sorted(files):
                if item.lower().endswith(VALID_EXTENSIONS):
                    listFiles.append(item)
                    total = total + 1
                    # print directories, item

            if len(listFiles) > 0:
                routes.append({
                    'path': directories,
                    'files': listFiles
                })
        self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Analyzed! [' + str(total) + ' images]', self.id)
        return routes

    # SINCRONIZA TODOS LOS ARCHIVOS DE DIRECTORIOS Y SUBDIRECTORIOS DE UN SERVIDOR AL LOCAL
    def synchronizeServerToLocal(self):
        self.countErrors = 0
        self.date = datetime.datetime.now()
        self.printColor(str(self.date) + '->' + str(self.cameraName), self.id)

        isRestrict, hourRestrict = self.restrictHour()
        if isRestrict:
            self.isWorking = False
            self.printColor(str(self.date) + '-> Hora restringida ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1]), self.id)
        else:

            if self.remoteConnect == 'FTP':
                state, FTP = self.connectFTP()
                if state is False:
                    self.rebootByError()
                    return
                self.traverseFTP(FTP, self.remotePathUp)
                FTP.quit()
                self.countErrors = self.countErrors + self.errorTraverseFTP
            else:
                state, sftp, t = self.connectSSH()
                if state is False:
                    self.rebootByError()
                    return
                self.traverseSSH(sftp, self.remotePathUp)
                sftp.close()
                t.close()
                self.countErrors = self.countErrors + self.errorTraverseSSH
        self.rebootByError()

    def rebootByError(self):
        self.totalCountErrors = self.totalCountErrors + self.countErrors
        if self.rebootError and self.totalCountErrors >= self.rebootError:
            self.printColor(str(self.date) + '-> [TOTAL ERRORS: ' + str(self.totalCountErrors) + ' REBOOT NOW!!!] ', self.id)
            print
            os.execv(self.EXEC[0], self.EXEC[1])
        else:
            self.printColor(str(self.date) + '-> Count bugs: ' + str(self.totalCountErrors), self.id)

    def traverseSSH(self, sftp, path='.', files=None):
        if files is None:
            files = []
            path = path[:-1]
            self.errorTraverseSSH = 0

        a = sftp.listdir_attr(path)
        for attr in a:
            if stat.S_ISDIR(attr.st_mode):
                self.traverseSSH(sftp, path + '/' + attr.filename, files)
            else:
                filename = attr.filename
                sourcePath = path + '/'
                destPath = self.GLOBALPATH + sourcePath.replace(self.remotePathUp, '')

                try:
                    if not os.path.exists(destPath):
                        os.makedirs(destPath)
                    # self.errorTraverseSSH = 1
                    sftp.get(sourcePath + filename, destPath + filename)
                    self.printColor(str(self.date) + '-> [' + filename + ']:: ' + sourcePath + ' >> ' + destPath, self.id)
                    if self.destroyImageOriginal and self.evaluateFile(destPath + filename):
                        try:
                            sftp.remove(sourcePath + filename)
                        except:
                            self.printColor(str(self.date) + '-> ERROR Remove ::The directory require PERMISSION ', self.id)
                except:
                    self.errorTraverseSSH = 1
                    self.printColor(str(self.date) + '-> [' + filename + ']:: ERROR Download ' + sourcePath, self.id)
        return files

    def traverseFTP(self, ftp, path='.', pathTemp='', files=None):
        if files is None:
            files = []
            self.errorTraverseFTP = 0
            try:
                ftp.cwd(path)
            except:
                self.printColor(str(self.date) + '-> the directory ' + path + ' not found.', self.id)
                return False

        for attr in ftp.nlst():
            try:
                ftp.cwd(attr)
                self.traverseFTP(ftp, attr, pathTemp + attr + '/', files)
                ftp.cwd('../')
            except:
                filename = attr
                sourcePath = self.remotePathUp + pathTemp
                destPath = self.GLOBALPATH + pathTemp

                try:
                    if not os.path.exists(destPath):
                        os.makedirs(destPath)

                    with open(destPath + filename, "wb") as f:
                        ftp.retrbinary("RETR " + filename, f.write)
                    self.printColor(str(self.date) + '-> [' + filename + ']:: ' + sourcePath + ' >> ' + destPath, self.id)

                    if self.destroyImageOriginal and self.evaluateFile(destPath + filename):
                        ftp.delete(filename)
                except:
                    self.errorTraverseFTP = 1
                    if os.path.exists(destPath + filename):
                        os.remove(destPath + filename)
                    self.printColor(str(self.date) + '-> [' + filename + ']:: ERROR Download ' + sourcePath, self.id)

        return files

    def traverseFTP2(self, ftp, depth=0):
        # RECORRE TODO EL ARBOL DE CARPETAS DE UNA HOST FTP
        if depth > 4:
            return ['depth > 10']
        level = {}
        for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
            try:
                ftp.cwd(entry)
                level[entry] = self.traverseFTP2(ftp, depth + 1)
                ftp.cwd('..')
            except ftplib.error_perm:
                level[entry] = None
        return level

    # SINCRONIZA LA ULTIMA IMAGEN OBTENIDA A UN SERVIDOR WEB POR CONEXION HTTP
    def syncUpdateImageWeb(self):
        self.countErrors = 0
        self.date = datetime.datetime.now()
        self.printColor(str(self.date) + '->' + str(self.cameraName), self.id)
        isRestrict, hourRestrict = self.restrictHour()
        if isRestrict:
            self.isWorking = False
            self.printColor(str(self.date) + '-> Hora restringida ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1]), self.id)
        else:
            self.generateDatePath()
            pathImages = self.GLOBALPATH + self.directory + self.filenamePath

            if os.path.exists(pathImages):
                listImages = os.listdir(pathImages)
                if len(listImages) > 0:
                    filename = sorted(listImages)[-1]

                    if self.watermarkScale:
                        statePaste, pathUpLocal, filenameLocal = self.pasteScale(pathImages, self.GLOBALPATH + self.directory, filename, (self.axisX, self.axisY))

                    else:
                        statePaste = None
                        pathUpLocal = pathImages
                        filenameLocal = filename

                    if self.watermarkScale is False or statePaste is True:
                        self.sendWEB(pathUpLocal, filenameLocal)

                    if statePaste is True:
                        try:
                            os.remove(pathUpLocal + filenameLocal)
                        except:
                            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, Not found [' + self.directory + filename + ']', self.id)
                else:
                    self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, vacio [' + pathImages + ']', self.id)
            else:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, no existe [' + pathImages + ']', self.id)
        self.rebootByError()

    # SINCRONIZA LA ULTIMA IMAGEN OBTENIDA A UN SERVIDOR POR CONEXION SSH O FTP
    def syncUpdateImageLocalToServer(self):
        self.countErrors = 0
        self.date = datetime.datetime.now()
        self.printColor(str(self.date) + '->' + str(self.cameraName), self.id)
        isRestrict, hourRestrict = self.restrictHour()
        if isRestrict:
            self.isWorking = False
            self.printColor(str(self.date) + '-> Hora restringida ' + str(hourRestrict[0]) + ' - ' + str(hourRestrict[1]), self.id)
        else:
            self.generateDatePath()
            pathImages = self.GLOBALPATH + self.directory + self.filenamePath
            if os.path.exists(pathImages):
                listImages = os.listdir(pathImages)
                if len(listImages) > 0:
                    filename = sorted(listImages)[-1]

                    if self.watermarkScale:
                        statePaste, pathUpLocal, filenameLocal = self.pasteScale(pathImages, self.GLOBALPATH + self.directory, filename, (self.axisX, self.axisY))
                        filenameRemote = filenameLocal
                    else:
                        statePaste = None
                        pathUpLocal = pathImages
                        filenameLocal = filename
                        if self.filenameUp is None or not self.filenameUp.lower().endswith(VALID_EXTENSIONS):
                            filenameRemote = filename
                        else:
                            filenameRemote = self.filenameUp

                    if self.watermarkScale is False or statePaste is True:
                        if self.remoteConnect == 'FTP':
                            self.sendFTP(pathUpLocal, self.remotePathUp, filenameLocal, filenameRemote)
                        else:
                            self.sendSSH(pathUpLocal, self.remotePathUp, filenameLocal, filenameRemote)

                    if statePaste is True:
                        try:
                            os.remove(pathUpLocal + filenameLocal)
                        except:
                            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, Not found [' + self.directory + filename + ']', self.id)

                else:
                    self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, vacio [' + pathImages + ']', self.id)
            else:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, no existe [' + pathImages + ']', self.id)
        self.rebootByError()

    def generetaScale (self):
        self.date = datetime.datetime.now()
        try:
            if self.isRange:
                # if int(self.days) < 0:
                #     self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Mode isRange TRUE require DAYS >=0', self.id)
                #     return False

                dFrom = datetime.datetime.strptime(self.dateTimeFrom, '%Y-%m-%dT%H:%M:%S')
                dTo = datetime.datetime.strptime(self.dateTimeTo, '%Y-%m-%dT%H:%M:%S')
            else:
                d1 = datetime.datetime.strptime(self.dateTimeFrom, '%Y-%m-%dT%H:%M:%S')
                d2 = datetime.datetime.strptime(self.dateTimeTo, '%Y-%m-%dT%H:%M:%S')

                dTo = datetime.datetime.now().replace(hour=d2.hour, minute=d2.minute, second=d2.second)
                dFrom = dTo - datetime.timedelta(days=abs(int(self.days)))
                dFrom = dFrom.replace(hour=d1.hour, minute=d1.minute, second=d1.second)
                # dFrom = datetime.datetime.strptime(self.dateTimeFrom, '%Y-%m-%dT%H:%M:%S')
                # dTo = datetime.datetime.strptime(self.dateTimeTo, '%Y-%m-%dT%H:%M:%S')
        except:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, se debe respetar el formato de tiempo [YYYY-MM-DDTHH:MM:SS]', self.id)
            return False

        if not os.path.exists(self.pathScale):
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> la ruta de pathScale ['+ self.pathScale +'] no existe', self.id)
            return False

        if self.sourcePath == self.outcomePath:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> El directorio surcePath debe ser distinto al outcomePath', self.id)
            return False

        # definimos los rangos de hora permitidos
        self.timeFrom = datetime.time(dFrom.hour, dFrom.minute, dFrom.second)
        self.timeTo = datetime.time(dTo.hour, dTo.minute, dTo.second)

        if dFrom > dTo:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error, DatetimeFrom debe ser un fecha anterior DatetimeTo', self.id)
            return False

        if self.isRange is False and int(self.days) < 0:
            diffDays = 0
        else:
            diffDays = (dTo - dFrom).days

        for i in range(diffDays + 1):
            self.exit = False
            self.lapseTime = 0
            pickDate = dFrom + datetime.timedelta(days=i)
            self.generateDatePath(pickDate)
            temporalPath = self.sourcePath + self.filenamePath
            # print temporalPath
            if os.path.exists(temporalPath):
                listImages = sorted(os.listdir(temporalPath))
                if len(listImages) > 0:
                    self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Read ' + temporalPath, self.id)
                    temporalOutPath = self.outcomePath + self.filenamePath
                    if not os.path.exists(temporalOutPath):
                        os.makedirs(temporalOutPath)

                    for image in listImages:
                        if not self.exit:
                            if self.validateHour(image):
                                self.filenameUp = self.generateNewName(image, self.postName)
                                self.pasteScale(temporalPath, temporalOutPath, image, (self.axisX, self.axisY))
                        else:
                            break

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

    def generateDatePath(self, date=None):

        # GENERAMOS LA ESTRUCTURA DE CARPETAS ANIDADAS POR ANIO/MES/DIA/
        if date is None:
            self.today = datetime.datetime.now()
            today = self.today
        else:
            today = date

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

            if thread:
                self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> edited image!!', self.id)
            else:
                puts(colored.green('     - edited image!!'))
        except:
            if thread:
                self.printColor(str(self.date) + '-> Error editting: la imagen incompleta!', self.id)
            else:
                puts(colored.red('     - Error editting: la imagen podria estar dañada.'))

    def pasteScale(self, source, dest, filename, axis=(0, 0)):

        if self.filenameUp is None or not self.filenameUp.lower().endswith(VALID_EXTENSIONS):
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> filenameUp['+ str(self.filenameUp) +'] extension invalida', self.id)
            toFilename = filename
        else:
            toFilename = self.filenameUp

        try:
            water = watermark.Watermark()
            water.makePasteScale(originalPath=source + filename, outPath=dest + toFilename, scalePath=self.pathScale, axis=axis)
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Edited imagen escala['+ filename +']!!', self.id)
            return True, dest, toFilename
        except:
            self.printColor(str(self.date) + '->' + str(self.cameraName) + '-> Error paste escala!!', self.id)
            return False, source, filename

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

    def evaluateFile(self, filename):

        try:
            size = os.path.getsize(filename)
            return size > 0
        except:
            return False

    def validateHour(self, filename):
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
        if difflapse < self.frequency:
            # si no transcurrido el tiempo minimo para registrar otra imagen se inavalida la imagen evaluada
            return False
        else:
            # caso contrario se actualiza tiempo de la ultima imagen registrada
            self.lapseTime = newlapseTime

        # verificamos que la imagen este entre el rango de tiempo permitido
        return self.timeFrom <= fileTime <= self.timeTo

    def generateNewName(self, filename, postName):

        year = filename[-18:-16]
        month = filename[-15:-13]
        day = filename[-13:-11]

        try:
            hour = filename[-10:-8]
            minute = filename[-8:-6]
            second = filename[-6:-4]
        except:
            return filename

        return '20' + year + month + day + '_' + hour + minute + second + '.' + postName + '.jpg'

