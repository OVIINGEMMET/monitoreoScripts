import os
import requests

pathSource = '/home/pc17/Desktop/getImage/rikardocorp.jpg'
urlUp = 'http://ovi.ingemmet.gob.pe/visual/misti/upload_simulacro.php'

files = {'file': open(pathSource, 'rb')}
response = requests.post(urlUp, files=files)
if response.status_code == 200:
    print '-> uploaded image[' + pathSource + ']!!'
else:
    print response.content
    print '-> upload Server Error!!'

