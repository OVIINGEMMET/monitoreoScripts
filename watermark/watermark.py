#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import os
from PIL import Image, ImageDraw, ImageFont


class Watermark():
    # DEFINICION DE VARIABLES
    def __init__(self):
        self.logoPath = None
        self.imagePath = None
        self.output = None
        self.sourceImage = None
        self.width = 0
        self.height = 0
        self.title = ''
        self.style = 1

        plataforma = sys.platform
        if plataforma == 'win32':
            FILEFULLPATH = os.path.abspath('')
            self.FONT = 'arial.ttf'
        else:
            FILEPATHNAME = os.path.dirname(sys.argv[0])
            FILEFULLPATH = os.path.abspath(FILEPATHNAME)
            self.FONT = 'Pillow/Tests/fonts/DejaVuSans.ttf'

    def __del__(self):
        print ("del Watermark")

    # INICIALIZACION DE VARIABLES
    def setParams(self, params):
        self.logoPath = params['logoPath']
        self.imagePath = params['imagePath']
        self.output = params['output']
        self.title = params['title']
        self.style = params['style']

    # INICIALIZACION LINEAL DE VARIABLES
    def setParamsLineal(self, logoPath, imagePath, output, title, style):
        self.logoPath = logoPath
        self.imagePath = imagePath
        self.output = output
        self.title = title
        self.style = style

    def makereactangule(self, rheight, typePos=1):
        width = self.width
        height = self.height

        # LIENZO EN BLANCO PARA EL RECTANGULO
        rectangle = Image.new('RGBA', (width, rheight))
        draw = ImageDraw.Draw(rectangle)
        # SE PINTA EL RECTANGULO CON UNA OPACIDAD
        draw.rectangle(((0, 0), (width, rheight)), fill=(0, 0, 0, 120))

        # POSICIONAMIENTO DEL LIENZO
        if typePos == 1:
            posRect = (0, height - rheight)
        else:
            posRect = (0, 0)

        # UNIMOS LAS PARTES AL LIENZO PRINCIPAL
        self.sourceImage.paste(rectangle, posRect, rectangle)

    def maketitle(self,  date='', typePos=1):
        width = self.width
        height = self.height
        title = self.title
        FONT = self.FONT
        sourceImage = self.sourceImage

        # POSICIONAMOS EL TITULO POR COORDENADAS
        if typePos == 1:
            posText1 = (10, height - 45)
            posText2 = (10, height - 25)
        elif typePos == 2:
            posText1 = (10, height - 20)
            posText2 = (width - 150, height - 20)
        else:
            posText1 = (10, 4)
            posText2 = (width - 150, 4)
        # ---------------------------------------

        # CREAMOS UN LIENZO EN BLANCO PARA AGREGAR EL TEXTO
        txt = Image.new('RGBA', sourceImage.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype(FONT, 12, encoding='utf-8')
        d = ImageDraw.Draw(txt)
        # -------------------------------------------------

        # CREAMOS LA FECHA DE REGISTRO
        format = "%d/%m/%Y %H:%M:%S"
        if date != '':
            msg = date.strftime(format)
        else:
            msg = datetime.datetime.now().strftime(format)
        # ----------------------------

        # UNIMOS LAS PARTES AL LIENZO PRINCIPAL
        d.text(posText1, title.decode('utf-8'), font=fnt, fill=(255, 255, 255, 255))
        d.text(posText2, msg, font=fnt, fill=(255, 255, 255, 190))
        self.sourceImage.paste(txt, None, txt)

    def makelogo(self, sizeLogo, typePos=1):
        width = self.width
        height = self.height

        # CARGAMOS EL LOGO
        logo = Image.open(self.logoPath)
        lw = logo.size[0]
        lh = logo.size[1]

        # REDIMESIONAMOS EL LOGO AL TAMANIO DESEADO
        realH = sizeLogo
        percent = float(realH) / lh
        realW = int(lw * percent)
        simage = logo.resize((realW, realH))
        # -----------------------------------------

        # POSICIONAMOS EL LOGO POR COORDENADAS
        if typePos == 1:
            posLogo = (width - realW - 10, height - realH - 5)
        elif typePos == 2:
            posLogo = (int(float(width) / 2 - float(realW) / 2), 5)
        else:
            posLogo = (int(width - float(realW)) - 10, int(height - float(realH)) - 5)
        # ------------------------------------

        # UNIMOS LAS PARTES AL LIENZO PRINCIPAL
        self.sourceImage.paste(simage, posLogo, simage)

    def showImage(self):
        self.sourceImage.show()

    def makeWatermark(self, date=''):
        base = Image.open(self.imagePath)
        self.width = base.size[0]
        self.height = base.size[1]
        self.sourceImage = base

        if self.style == 1:
            self.makereactangule(rheight=55, typePos=1)
            self.maketitle(date=date, typePos=1)
            self.makelogo(sizeLogo=45, typePos=1)
        elif self.style == 2:
            self.makereactangule(rheight=25, typePos=1)
            self.maketitle(date=date, typePos=2)
            self.makelogo(sizeLogo=75, typePos=2)
        elif self.style == 3:
            self.makereactangule(rheight=20, typePos=2)
            self.maketitle(date=date, typePos=3)
            self.makelogo(sizeLogo=70, typePos=3)

        self.sourceImage.save(self.output, "JPEG")

