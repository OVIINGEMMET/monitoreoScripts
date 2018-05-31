#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os, sys
from PIL import Image, ImageDraw, ImageFont

plataforma = sys.platform
if plataforma == 'win32':
    FILEFULLPATH = os.path.abspath('')
    FONT = 'arial.ttf'
else:
    FILEPATHNAME = os.path.dirname(sys.argv[0])
    FILEFULLPATH = os.path.abspath(FILEPATHNAME)
    FONT = 'Pillow/Tests/fonts/DejaVuSans.ttf'


def makecross(sourceImage):
    draw = ImageDraw.Draw(sourceImage)
    draw.line((0, 0) + sourceImage.size, fill=128)
    draw.line((0, sourceImage.size[1], sourceImage.size[0], 0), fill=128)


def maketitle (sourceImage, title='Titulo por default', typePos=1, date='', fontSize=12, font=None):
    height = sourceImage.size[1]
    weight = sourceImage.size[0]

    if font is None:
        font = FONT

    # Position
    if typePos == 1:
        posText1 = (10, height - 45)
        posText2 = (10, height - 25)
    elif typePos == 2:
        posText1 = (10, height - 20)
        posText2 = (weight - 150, height - 20)
    else:
        posText1 = (10, 1)
        posText2 = (weight - (fontSize * 10 + 40), 1)

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', sourceImage.size, (255, 255, 255, 0))
    # get a font
    fnt = ImageFont.truetype(font, fontSize, encoding='utf-8')
    d = ImageDraw.Draw(txt)
    format = "%d/%m/%Y %H:%M:%S"
    if date != '':
        msg = date.strftime(format)
    else:
        msg = datetime.datetime.now().strftime(format)

    d.text(posText1, title.decode('utf-8'), font=fnt, fill=(255, 255, 255, 255))
    d.text(posText2, msg, font=fnt, fill=(255, 255, 255, 190))
    sourceImage.paste(txt, None, txt)


def makereactangule (sourceImage, rheight, typePos=1):
    width = sourceImage.size[0]
    height = sourceImage.size[1]
    rectangle = Image.new('RGBA', (width, rheight))
    draw = ImageDraw.Draw(rectangle)
    draw.rectangle(((0, 0), (width, rheight)), fill=(0, 0, 0, 100))

    # Position
    if typePos == 1:
        posRect = (0, height - rheight)
    else:
        posRect = (0, 0)

    sourceImage.paste(rectangle, posRect, rectangle)


def makelogo (sourceImage, pathLogo, sizeLogo, typePos=1):
    width = sourceImage.size[0]
    height = sourceImage.size[1]

    logo = Image.open(pathLogo)
    lw = logo.size[0]
    lh = logo.size[1]

    realH = sizeLogo
    percent = float(realH) / lh
    realW = int(lw * percent)
    simage = logo.resize((realW, realH))
    # simage.putalpha(100)

    # Position
    if typePos == 1:
        posLogo = (width - realW - 10, height - realH - 5)
    elif typePos == 2:
        posLogo = (int(float(width) / 2 - float(realW)/2), 5)
    else:
        posLogo = (int(width - float(realW)) - 10, int(height - float(realH)) - 5)

    sourceImage.paste(simage, posLogo, simage)


def watermark1(imageSource, title='Volcán', date=''):
    makereactangule(imageSource, 55, typePos=1)
    maketitle(imageSource, title, typePos=1, date=date)
    makelogo(imageSource, FILEFULLPATH + '/sources/ovi-logo.png', sizeLogo=45, typePos=1)


def watermark2(imageSource, title='Volcán', date=''):
    makereactangule(imageSource, 25, typePos=1)
    maketitle(imageSource, title, typePos=2, date=date)
    makelogo(imageSource, FILEFULLPATH + '/sources/logoCircle2.png', sizeLogo=75, typePos=2)


def watermark3(imageSource, title='Volcán', date=''):
    makereactangule(imageSource, 20, typePos=2)
    maketitle(imageSource, title, typePos=3, date=date)
    makelogo(imageSource, FILEFULLPATH + '/sources/logoCircle2.png', sizeLogo=70, typePos=3)


def watermark4(imageSource, title='Volcán', date='', font=None):
    makereactangule(imageSource, 22, typePos=2)
    maketitle(imageSource, title, typePos=3, date=date, fontSize=18, font=font)
    makelogo(imageSource, FILEFULLPATH + '/sources/ovi-logo-azul.png', sizeLogo=90, typePos=3)


# def main():
#
#     # get an image
#     base = Image.open('sources/test.jpg')
#     Ht = base.size[1]
#     Wt = base.size[0]
#
#     watermark3(base)
#
#     base.show()
#     base.save("12volt.jpg", "JPEG")
#
#
# if __name__ == '__main__':
#     main()