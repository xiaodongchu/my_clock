# -*- encoding: utf-8 -*-
"""
@Modify Time          @Author      @Version    @Description
--------------      -----------    --------    ------------
2023/3/13 14:43     chuxiaodong      1.0           None
"""

from os import listdir, path
from sys import exit
from time import sleep
from random import choice
from traceback import print_exc
from win32con import MB_OK, MB_YESNO, IDNO, IDCLOSE
from win32api import MessageBox
from pygame import mixer

music_dir = "D:/programming/python/my_clock/music"  # 绝对路径
time_work = 30
time_break = 10
loop_play_max = 10
play = True
music_start_path = music_dir + "start/"
music_end_path = music_dir + "end/"
processes = []
mixer.init()


def show(show_s, start=True):
    while len(processes) > 0:
        processes.pop().terminate()
    if play:
        if start:
            file_list = listdir(music_start_path)
            file_list = music_start_path + choice(file_list)
        else:
            file_list = listdir(music_end_path)
            file_list = music_end_path + choice(file_list)
        mixer.music.load(file_list)
        mixer.music.play(loop_play_max)
        MessageBox(0, show_s, "提醒", MB_OK)
        mixer.music.stop()
    else:
        MessageBox(0, show_s, "提醒", MB_OK)


def choose_play():
    global play
    s = "是否播放音乐？\n将开始{}+{}循环计时。".format(time_work, time_break)
    i = MessageBox(0, s, "提醒", MB_YESNO)
    if i == IDNO:
        play = False
    elif i == IDCLOSE:
        exit(0)


if __name__ == '__main__':
    try:
        choose_play()
        loop_time = 0
        while True:
            sleep(time_work * 60)
            text = "休息{}分钟。".format(time_break)
            show(text, False)
            sleep(time_break * 60)
            loop_time += 1
            text = "休息结束，开始{}分钟工作。\n这是{}次循环。".format(time_work, loop_time)
            show(text, True)
    except:
        f = open(music_dir + "error.txt", "w")
        print_exc(file=f)
        f.close()
        MessageBox(0, "aclock程序出错，\n请查看error.txt。", "提醒", MB_OK)
    finally:
        exit(0)
