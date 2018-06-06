from createGif import CreateGif
# import ftplib
import datetime
import paramiko

H = '10.102.131.52'
U = 'root'
P = 'rootubinas2016'

local = '/media/pc17/DATOS/project/monitoreoScripts/createGif/'
remote = '/var/www/html/panelview/img/'
RESTRICT = [['00:00:00', '07:59:00'], ['17:00:00', '23:59:59']]


def restrictHour():
    if RESTRICT is None:
        return False, []

    # VARIABLE DE ESCAPE DEL BUCLE
    centinel = False
    hourRestrict = []
    localtime = datetime.datetime.now().time()

    # BUCLE PARA LEER EL ARRAY DE RESTRICCIONES
    for r in RESTRICT:
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


def copy_file(hostname, port, username, password, src, dst):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    print (" Connecting to %s \n with username=%s... \n" %(hostname,username))
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    print ("Copying file: %s to path: %s" %(src, dst))
    sftp.put(src, dst)
    sftp.close()
    t.close()


def generateDateRange():
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

    timeTo = str(H) + ':' + str(M) + ':00'
    timeFrom = str(H2) + ':' + str(M) + ':00'
    return timeFrom, timeTo


def createGif(params):
    gif = CreateGif()
    gif.setParams(params)
    gif.createGif()
    total = gif.totalImages
    return total


TimeFrom, TimeTo = generateDateRange()
sources = [{
            'path': '/home/pc17/Desktop/getImage/05/',
            'gifPath': local + 'sabancaya.gif',
            'scale': 0.8,
            'isDirectory': True,
            'optimize': True,
            'quality': 60,
            'frecuency': 30,
            'duration': 0.25,
            'time': [TimeFrom, TimeTo],
            'auxName': 'sabancaya.gif'
            },{
            'path': '/home/pc17/Desktop/getImage/05/',
            'gifPath': local + 'ubinas.gif',
            'scale': 0.8,
            'isDirectory': True,
            'optimize': True,
            'quality': 60,
            'frecuency': 30,
            'duration': 0.25,
            'time': [TimeFrom, TimeTo],
            'auxName': 'ubinas.gif'
            }]


for src in sources:

    isRestrict, hours = restrictHour()

    if not isRestrict:
        totalImages = createGif(src)

        if totalImages > 150:
            copy_file(H, 22, U, P, src['gifPath'], remote + src['auxName'])
        else:
            print 'La cantidad de imagenes es insuficiente [' + str(totalImages) + ']'
    else:
        print 'Hora restringida '+ str(hours[0]) + '-' + str(hours[1])
