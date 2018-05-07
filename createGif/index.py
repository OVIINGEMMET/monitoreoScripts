from createGif import CreateGif

params = {
    'path': '/home/pc17/Desktop/22/',
    'gifPath': 'output2.gif',
    'scale': 0.6,
    'isDirectory': True,
    'optimize': True,
    'quality': 50,
    'frecuency': 200,
    'duration': 0.07,
    'time': ['05:19:00', '14:25:00']
}

gif = CreateGif()
gif.setParams(params)
gif.createGif()
