import moviepy.editor as mpy

path = '/home/pc17/Desktop/getImage/sabancaya9.avi'
myclip = mpy.VideoFileClip(path)
myclip.write_videofile('/home/pc17/Desktop/getImage/rick.webm', audio=False)
