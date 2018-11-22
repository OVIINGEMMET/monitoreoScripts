import os
import sys
import datetime
import shutil
YEAR = '2017'
METHOD = 'SO2_DOAS_ESCANER'
PATH = '/home/pc17/monitoreo/Geoquimica/1-EST-NOVAC/1_DOAS/' + YEAR + '/'
OUTCOME = '/home/pc17/monitoreo2/01_ORIGINAL/'

STATION = {
    'D2J2559': {'volcan': 'UBINAS', 'pre': 'UBD1'},
    'D2J2809': {'volcan': 'SABANCAYA', 'pre': 'SAD3'},
    'D2J2816': {'volcan': 'UBINAS', 'pre': 'UBD2'},
    'D2J2824': {'volcan': 'SABANCAYA', 'pre': 'SAD5.1'},
    'D2J2833': {'volcan': 'SABANCAYA', 'pre': 'SAD1'},
}

# name = '2018'
# try:
#     fecha = datetime.datetime.strptime(name, '%Y-%m-%d')
# except:
#     fecha = None
#
# print fecha

# a = '/home/pc17/monitoreo/Geoquimica/1-EST-NOVAC/1_DOAS/2014/2014.12.30/D2J2559/'
# b = '/home/pc17/Desktop/DOAS/aa/aa/'
#
# if not os.path.exists(b):
#     os.makedirs(b)

# shutil.copytree(a, b)

Error = []
if os.path.exists(PATH):
    listImages = os.listdir(PATH)
    for directory in listImages:
        try:
            fecha = datetime.datetime.strptime(directory, '%Y.%m.%d')
            pathStations = PATH + directory + '/'

            stations = os.listdir(pathStations)
            for dir in stations:
                if os.path.isdir(pathStations + dir + '/'):
                    volcan = STATION[dir]['volcan']
                    prename = STATION[dir]['pre'] + '_'

                    print
                    source = PATH + directory + '/' + dir + '/'
                    dest = OUTCOME + volcan + '/GEOQUIMICA/' + METHOD + '/' + prename + dir + '/' + YEAR + '/' + directory + '/'

                    print source
                    print dest
                    try:
                        shutil.copytree(source, dest)
                        print 'Copied!!'
                    except:
                        Error.append(source)
                        print 'Error!!'
        except:
            print directory, False


print
print 'Error LIST:'
print Error
