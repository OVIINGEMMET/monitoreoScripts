from createGif import CreateGif

params = {
    'path': '/home/pc17/Desktop/getImage/05/',
    'gifPath': 'output3.gif',
    'scale': 0.8,
    'isDirectory': True,
    'optimize': True,
    'quality': 60,
    'frecuency': 30,
    'duration': 0.25,
    'time': ['10:00:00', '12:00:00']
}

gif = CreateGif()
gif.setParams(params)
gif.createGif()
