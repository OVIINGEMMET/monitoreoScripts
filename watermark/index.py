from watermark import Watermark

# params = {
#     'logoPath': 'logoCircle.png',
#     'imagePath': 'test.jpg',
#     'output': 'output.jpg',
#     'title': 'Titulo de Prueba',
#     'style': 3
# }

watermark = Watermark()
# INICIAR PARAMETROS METODO 1
# watermark.setParams(params)
# INICIAR PARAMETROS METODO 2
watermark.setParamsLineal(logoPath='sources/logoCircle.png', imagePath='sources/test.jpg', output='output.jpg', title='OVI Ingemmet', style=3)
watermark.makeWatermark()
watermark.showImage()
