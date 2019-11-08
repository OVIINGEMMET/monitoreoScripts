from obspy import read, UTCDateTime
from colorama import Fore
from PIL import Image, ImageDraw, ImageOps, ImageMath
from past.builtins import xrange

original = 'C:\WorkSpace\Sismologia\Procesados\Ticsani_tic02_2019-11-07.png'
imgPath = 'C:\WorkSpace\Sismologia\Procesados\Ticsani_tic02_08-11-20194.pdf'
pathToHelli = 'C:/WorkSpace/Sismologia/Procesados/'
originalImg = Image.open(original, 'r')


# gcfPart = Image.open(img, 'r')



# a = remove_transparency(img)
# a.save(pathToHelli + 'alpha.png')

# newImg = Image.new('RGBA', originalImg.size, (0, 0, 0, 0))
# newImg.paste(originalImg, (0, 0))
# newImg.paste(originalImg, (0, 0), mask=gcfPart)
# # newImgJPG = newImg.convert('RGB')
# # newImgJPG.save(img)
# newImg.save(pathToHelli + 'm.png')

def convertToTransparent():
    img = Image.open(imgPath)  # image path and name
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for i, item in datas:
        avg = int(sum(item[:3]) / 3.0)
        newData[i] = (item[0], item[1], item[2], 0 + avg)
        # if item[0] == 0 and item[1] == 0 and item[2] == 0:
        #     newData.append((0, 0, 0, 0))
        # else:
        #     newData.append(item)
    img.putdata(newData)
    return img


#
# im = Image.open(imgPath)
#
# mask = Image.new('L', im.size, color = 255)
# draw=ImageDraw.Draw(mask)
# transparent_area = (0, 0, 900, 800)
#
# draw.rectangle(transparent_area, fill = 0)
# im.putalpha(mask)
# im.save(pathToHelli + 'alpha.png')

def distance2(a, b):
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2])


def makeColorTransparent(image, color, thresh2=0):
    image = image.convert("RGBA")
    red, green, blue, alpha = image.split()
    image.putalpha(ImageMath.eval("""convert(((((t - d(c, (r, g, b))) >> 31) + 1) ^ 1) * a, 'L')""",
                                  t=thresh2, d=distance2, c=color, r=red, g=green, b=blue, a=alpha))
    return image


import os
from wand.image import Image
from wand.color import Color


def convert_pdf(filename, output_path, resolution=150):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    all_pages = Image(filename=filename, resolution=resolution)
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('#000000')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}-{}.png'.format(image_filename, i)
            image_filename = os.path.join(output_path, image_filename)

            img.save(filename=image_filename)

convert_pdf(imgPath,pathToHelli)