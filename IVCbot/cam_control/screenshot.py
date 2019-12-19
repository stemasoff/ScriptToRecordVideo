import os
from time import sleep


def get_screen(cam, ip):
    ffmpegArgs = ['ffmpeg',
                  '-rtsp_transport tcp',
                  '-i', 'rtsp://admin:12345678@{}/mpeg4'.format(ip),
                  '-an -r 1',
                  '-vframes 1 -y -f',
                  'mjpeg {}.jpg'.format(cam)

    ]
    os.system(r' '.join(ffmpegArgs))
    return '{}.jpg'.format(cam)

def check_record(cam, path):
    camPath = path + cam + '/'
    i = 0
    sizeFolder = 0
    tempSizeFolder = 0
    while i < 2:
        tempSizeFolder = sizeFolder
        sizeFolder = 0
        for file in os.listdir(camPath):
            sizeFolder += os.path.getsize(camPath + file)
        sleep(2)
        i += 1
    return not tempSizeFolder == sizeFolder


def status():
    sleep(15)
    print('kek')

