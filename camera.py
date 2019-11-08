import os
from threading import Thread
from config import Config


class Camera(Config):
    def __init__(self, camFolder, ip, port, dir, logPass):
        self.folder = Camera.mainVideoFolder + camFolder                        # Папка с видео для камеры
        self.ip = ip                                                            # Ip камеры
        self.thread = Thread(target=self.record)                                # Создаем новый поток для записи
        self.logPass = logPass
        self.port = port
        self.dir = dir

        # В этой переменной храним атрибуты вызова программы ffmpeg
        self.ffmpegArgs = ['ffmpeg',                                                    # Название программы
                           f'-t 00:{Camera.time_record}:00',                            # Время записи
                           '-i',
                           f'rtsp://{self.logPass}@{self.ip}:{self.port}{self.dir}',    # Путь к камере
                           '-loglevel quiet',                                           # Отключаем вывод в консоль
                           '-copyts', '-start_at_zero',
                           '-rtsp_transport tcp', '-r 25', '-vcodec copy',              # Выбор протокола tcp и fps
                           f'{self.folder}$(date +%Y-%m-%d+%H-%M-%S).avi']              # Путь к папке и название файла
        Camera._countCam += 1                                                            # Считаем кол-во камер

    def delete_old_files(self):

        videoFolderSize = 0     # Обнуляем счетчик
        timeLiveFiles = list()  # Список, с временем жизни каждого файла в папке
        dictFiles = dict()      # Словарь, в котором ключ - это вес файла, а значение - его имя

        for file in os.listdir(self.folder):
            fileName = self.folder + file                           # Полное имя файла, с указанием пути к нему
            fileTime = os.path.getmtime(fileName)                   # Получаем дату редактирования(создания файла)
            videoFolderSize += os.path.getsize(self.folder + file)  # Счетчик размера папки

            # Словарь, где время создания файла является ключем, а значение это полное имя файла
            dictFiles[fileTime] = fileName

            # Добавляем время создания файла в массив и сортируем его, чтобы потом брать из него значения для
            # удаления самых старых видео
            timeLiveFiles = sorted(dictFiles)

        if videoFolderSize > Camera.maxSizeFolder / Camera._countCam:
            # Удаляем самый старый файл
            os.remove(dictFiles[timeLiveFiles.pop(0)])

    def record(self):
        if not os.path.exists(self.folder):
            # Проверяем, существует ли папка для записи, если нет, то создаем её
            os.mkdir(self.folder)
        while True:
            # Цикл, в котором мы запускаем функцию, для удаления старых файлов и запуска записи
            self.delete_old_files()
            os.system(r' '.join(self.ffmpegArgs))
