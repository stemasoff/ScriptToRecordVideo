
from camera import Camera

cam1 = Camera('cam1/', '192.168.XX.XX', '554', '/mpeg4', 'admin:12345678')
cam2 = Camera('cam2/', '192.168.XX.XX', '554', '/mpeg4', 'admin:12345678')

cam1.thread.start()
cam2.thread.start()

print('Идет запись.')
print('Работают {} камеры'.format(Camera.countCam))
print('Press <Ctrl> + <Z> to stop.')