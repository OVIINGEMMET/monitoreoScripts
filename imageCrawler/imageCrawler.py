import urllib2
import urllib
from bs4 import BeautifulSoup

# PRINCIPAL
ISPROXY = True
PROXYURL = '10.102.0.253'
PORT = '8080'
USERNAME = 'autonomoosi10'
PASSWORD = 'autonomo'
PATH_IMAGES = 'images/'
# IMAGES
URL = 'https://www.senamhi.gob.pe/site/volcan/?p=Sabancaya'
ATTR_IMAGE = 'src'
VALUES = {
    'v_time': 'loop',
    'v_var': '_espe',
    'v_ini': '_1_f',
    'v_mod': 'Fall3d',
    'v_volc': '_Ubinas_',
    'v_altu': 2000
}

VALUES = {
    'v_time': 'loop',
    'v_var': '_Ubinas_3000_espe_f',
    'v_mod': 'Fall3d'
}
# ----------------------------------------------------

if ISPROXY:
    proxy = urllib2.ProxyHandler({'http': 'http://' + USERNAME + ':' + PASSWORD + '@' + PROXYURL + ':' + PORT,
                                  'https': 'https://' + USERNAME + ':' + PASSWORD + '@' + PROXYURL + ':' + PORT})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

URL_PATH = 'https://www.senamhi.gob.pe/site/volcan/'
# URL = 'https://www.senamhi.gob.pe/site/volcan/ver_mapas_img_volcanes_final.php?v_time=loop&v_var=_espe&v_ini=_1_f&v_mod=Fall3d&v_volc=_Sabancaya_&v_altu=2000'
URL = 'https://www.senamhi.gob.pe/site/volcan/ver_mapas_img_volcanes.php?v_time=loop&v_var=_Ubinas_3000_espe_f&v_mod=Fall3d&v_volc=_Ubinas_'
# data = urllib.urlencode(VALUES)
# req = urllib2.Request(URL, data)
page = urllib2.urlopen(URL)
soup = BeautifulSoup(page, 'html.parser')
print soup

i = 0
for imgContent in soup.findAll('img'):
    # print imgContent
    i = i + 1
    # price = img.text.strip()
    # img = imgContent.find('img')
    img = imgContent
    src = img.get(ATTR_IMAGE)
#
    if src is not None and str(src[:1]) == "/":
        src = URL + src
    elif src is not None and str(src[0:2]) == "..":
        src = URL_PATH + src
    print src
    if src is None:
        print img
    else:
        print src
        imageFile = open(PATH_IMAGES + 'image' + str(i) + '.jpg', 'wb')
        imageFile.write(urllib2.urlopen(src).read())
        imageFile.close()
