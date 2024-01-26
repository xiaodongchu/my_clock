from os import listdir
from time import sleep
from random import choice
from traceback import print_exc
from multiprocessing import Process as process

from win32con import MB_OK, MB_YESNOCANCEL, IDYES, IDNO
from win32api import MessageBox
from pygame import mixer

music_dir = "D:/programming/python/my_clock/music/"  # 绝对路径
time_work = 30  # 单位：分钟
time_break = 10  # 单位：分钟
loop_play_max = 3
play = True
music_start_path = music_dir + "start/"
music_end_path = music_dir + "end/"
error_path = music_dir + "error.txt"
process_list = []
mixer.init()


def show(show_s, start=True):
    while len(process_list) > 0 and start:
        process1 = process_list.pop()
        if process1 is not None and process1.is_alive():
            process1.terminate()
    if play:
        if start:
            file_list = listdir(music_start_path)
            file_list = [i for i in file_list if i.endswith(".mp3")]
            file_list = music_start_path + choice(file_list)
        else:
            file_list = listdir(music_end_path)
            file_list = [i for i in file_list if i.endswith(".mp3")]
            file_list = music_end_path + choice(file_list)
        mixer.music.load(file_list)
        mixer.music.play(loop_play_max)
        MessageBox(0, show_s, "提醒", MB_OK)
        mixer.music.stop()
    else:
        MessageBox(0, show_s, "提醒", MB_OK)


def choose_play():
    global play
    s = "是否播放音乐？\n将开始{}+{}循环计时。\n单击取消推出计时".format(time_work, time_break)
    i = MessageBox(0, s, "提醒", MB_YESNOCANCEL)
    if i == IDNO:
        play = False
    elif i == IDYES:
        play = True
    else:
        return 0
    loop_run()


def loop_run():
    try:
        loop_time = 0
        while True:
            sleep(time_work * 60)
            text = "休息{}分钟。".format(time_break)
            process1 = process(target=show, args=(text, False))
            process1.start()
            process_list.append(process1)
            sleep(time_break * 60)
            loop_time += 1
            text = "休息结束，开始{}分钟工作。\n这是{}次循环。".format(time_work, loop_time)
            show(text, True)
    except:
        f = open(error_path, "w", encoding="utf-8")
        print_exc(file=f)
        f.close()
        MessageBox(0, "aclock程序出错，\n请查看error.txt。", "提醒", MB_OK)


if __name__ == '__main__':
    choose_play()
