# Ricardo Coronado Perez
# rikardo.corp@gmail.com

import os
import datetime
import paramiko
import shutil
import urllib2
from bs4 import BeautifulSoup
# from createGif.createGif import CreateGif

# extensionesde imagen validas
VALID_EXTENSIONS = ('png', 'jpg')


class GetSenamhi():

    def __init__(self):
        self.PROXYURL = ''
        self.pathLocal = ''
        self.PORT_P = ''
        self.USER_P = ''
        self.PASS_P = ''
        self.ISPROXY = True

        self.PATH_SERVER_DEST = ''
        self.HOST_S = ''
        self.PORT_S = ''
        self.USER_S = ''
        self.PASS_S = ''

        self.directory = ''
        self.url = ''
        self.urlPath = ''
        self.attrImage = ''
        self.temporal = '_temp/'
        self.sendLocal = '/'

    def setParams(self, params):
        self.PROXYURL = params['PROXYURL']
        self.PORT_P = params['PORT_P']
        self.USER_P = params['USER_P']
        self.PASS_P = params['PASS_P']
        self.ISPROXY = params['ISPROXY']

        self.PATH_SERVER_DEST = params['PATH_SERVER_DEST']
        self.HOST_S = params['HOST_S']
        self.PORT_S = int(params['PORT_S'])
        self.USER_S = params['USER_S']
        self.PASS_S = params['PASS_S']

        self.pathLocal = params['pathLocal']
        self.directory = params['directory']
        self.url = params['url']
        self.urlPath = params['urlPath']
        self.attrImage = params['attrImage']
        self.sendLocal = params['sendLocal']

        # creamos una carpeta temporal para las imagenes optimizadas
        self.temporal = self.pathLocal + self.directory

    def setProxy(self):
        proxy = urllib2.ProxyHandler({'http': 'http://' + self.USER_P + ':' + self.PASS_P + '@' + self.PROXYURL + ':' + self.PORT_P,
                                      'https': 'https://' + self.USER_P + ':' + self.PASS_P + '@' + self.PROXYURL + ':' + self.PORT_P})
        auth = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def getImages(self):
        if self.ISPROXY:
            self.setProxy()

        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup(page, 'html.parser')

        self.count = 0
        fullPath = self.generateDatePath()
        for imgContent in soup.findAll('img'):
            # print imgContent
            self.count = self.count + 1
            # price = img.text.strip()
            # img = imgContent.find('img')
            img = imgContent
            src = img.get(self.attrImage)

            if src is not None and str(src[:1]) == "/":
                src = self.url + src
            elif src is not None and str(src[0:2]) == "..":
                src = self.urlPath + src

            if src is None:
                print img
            else:
                print src
                nameFile = 'img_' + str(self.count) + '.gif'
                imageFile = open(fullPath + nameFile, 'wb')
                # imageFile = open(self.temporal + 'img_' + self.generateNameHour() + '.gif', 'wb')
                imageFile.write(urllib2.urlopen(src).read())
                imageFile.close()
                self.updatedImagesToWeb(fullPath, nameFile)

        # self.listDirectory()
        # self.generateGif()
        if self.count == 0:
            shutil.rmtree(fullPath)

    def updatedImagesToWeb(self, path, nameFile):
        if self.sendLocal:
            print 'Local'
            try:
                if not os.path.exists(self.PATH_SERVER_DEST):
                    os.makedirs(self.PATH_SERVER_DEST)
                shutil.copy(path + nameFile, self.PATH_SERVER_DEST + nameFile)
                print ('- File Copied!!')
            except:
                print 'Erro Copy File!!'

        elif self.sendLocal is not None:
            self.uploadFile(path, self.PATH_SERVER_DEST + self.directory, nameFile)
        else:
            print 'No send'

    def uploadFile(self, src, dst, filename):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        print ("- Connecting to %s \n- with username=%s..." % (self.HOST_S, self.USER_S))
        try:
            t = paramiko.Transport((self.HOST_S, self.PORT_S))
            t.connect(username=self.USER_S, password=self.PASS_S)
        except:
            print ('- Error de conexion al servidor.')
            return

        try:
            sftp = paramiko.SFTPClient.from_transport(t)

            try:
                sftp.chdir(dst)  # Test if remote_path exists
            except IOError:
                sftp.mkdir(dst)  # Create remote_path
                sftp.chdir(dst)

            print ("- Copying file: %s to path: %s" % (src + filename, dst + filename))
            sftp.put(src + filename, dst + filename)
            print ('- File Copied!!')
            sftp.close()
            t.close()
        except:
            print ('- Error de envio de datos.')

    # def generateGif(self):
    #     gif = CreateGif()
    #     gif.path = self.temporal
    #     gif.gifPath = self.pathLocal + self.directory + self.gifName
    #     gif.noRequireValid = True
    #     gif.duration = 0.5
    #     gif.createGif()
    #     del gif

    def generateNameHour(self):
        DATE = datetime.datetime.now()
        H = DATE.hour
        H2 = H - 2
        if H <= 9:
            H = '0' + str(H)
        if H2 <= 9:
            H2 = '0' + str(H2)

        M = DATE.minute
        if M <= 9:
            M = '0' + str(M)

        S = DATE.second
        if S <= 9:
            S = '0' + str(S)

        return str(H) + '_' + str(M) + '_' + str(S) + '_' + str(DATE.microsecond)

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

        if os.path.exists(self.temporal + filenamePath):
            total = len(os.listdir(self.temporal + filenamePath))
        else:
            total = '0'

        pathFinal = self.temporal + filenamePath + 'm' + str(total) + '/'

        if not os.path.exists(pathFinal):
            os.makedirs(pathFinal)

        return pathFinal

    def listDirectory(self):
        filenames = sorted(os.listdir(self.temporal))
        print filenames
