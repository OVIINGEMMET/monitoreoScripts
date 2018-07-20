import geopy.distance
import pandas as pd
import pprint
import csv

file = './stations.csv'

data = pd.read_csv(file, header=None)
# print data

result = {}
threshold = 20
for index, row in data.iterrows():
    id = row[0]
    volcan = row[1]
    codigo = row[2]
    latitude = row[3]
    longitude = row[4]
    altura = row[5]
    metodo = row[6]
    coordPrincipal = (latitude, longitude)
    result[id] = []
    print (id, volcan, codigo, latitude, longitude, altura, metodo)
    for _index, _row in data.iterrows():
        # if index != _index:
        _id = _row[0]
        _volcan = _row[1]
        _codigo = _row[2]
        _latitude = _row[3]
        _longitude = _row[4]
        _altura = _row[5]
        _metodo = _row[6]
        coordSecundaria = (_latitude, _longitude)
        distance = geopy.distance.vincenty(coordPrincipal, coordSecundaria).m
        if distance <= threshold:
            result[id].append([_id, _volcan, _codigo, _latitude, _longitude, _altura, _metodo, 0])

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(result)

with open('station_result.csv', 'w') as f:
    i = 0
    list = []
    print 'rick'
    for key in result:
        idx = key
        print key, idx, result[key]
        for (index, item) in enumerate(result[key]):
            idy = item[0]

            if int(idx) <= int(idy):
                state = int(item[7])
                try:
                    list.index(item[0])
                except:
                    # print list
                    list.append(item[0])
                    # print list
                    print item
                    cadena = ','.join(str(x) for x in item)
                    print '     ', cadena
                    f.write(cadena)
                    f.write('\n')
                # print '     ', item
    #
    #     if idx <= idy:
    #         i = i + 1
    #         print i, item[0]
    #     # f.write(line)

# coords_1 = (52.2296756, 21.0122287)
# coords_2 = (52.406374, 16.9251681)

# coords_1 = ('-15.80689', '-71.842637')
# coords_2 = (-15.824437,	-71.843211)
# coords_3 = ('-15.76404',	'-71.83165')
#
# print geopy.distance.vincenty(coords_1, coords_3).km
# print geopy.distance.vincenty(coords_1, coords_3).m