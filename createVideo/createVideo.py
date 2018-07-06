import cv2
import numpy as np
import os

from os.path import isfile, join
VALID_EXTENSIONS = ('png', 'jpg')


def convert_frames_to_video(pathIn, pathOut, fps):
    frame_array = []
    # files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    files = sorted(os.listdir(pathIn))
    # for sorting the file names properly
    # files.sort(key=lambda x: int(x[5:-4]))

    for i in range(0,5500):
        print 'item ' + str(i)
        filename = pathIn + files[i]
        # reading each files
        if filename.lower().endswith(VALID_EXTENSIONS):
            try:
                img = cv2.imread(filename)
                height, width, layers = img.shape
                size = (width, height)
                print(filename)
                # inserting the frames into an image array
                frame_array.append(img)
            except:
                print 'ERROR: ' + filename
        else:
            print 'NO FORMATO: ' + filename

    # print frame_array
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()


def main():
    # pathIn = '/home/pc17/Desktop/getImage/sabancaya/2018/05/30/'
    pathIn = '/run/user/1000/gvfs/smb-share:server=10.102.131.46,share=monitoreo/Visual/original/sabancaya/2018/07/03/'
    pathOut = 'sabancaya_18_07_03-ALL.avi'
    fps = 10.0
    convert_frames_to_video(pathIn, pathOut, fps)


if __name__ == "__main__":
    main()