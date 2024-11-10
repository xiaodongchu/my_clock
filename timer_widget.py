import json
import os
from random import choice

import pygame
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

base_path = os.path.dirname(__file__) + '/'
start_sound_path = base_path + 'start/'
end_sound_path = base_path + 'end/'
config_path = base_path + 'config.json'
with open(config_path, 'r') as f:
    config = json.load(f)


class PomodoroTimer(QWidget):

    def __init__(self):
        super().__init__()
        self.work_duration = config["work_time"] * 60  # 工作时间
        self.break_duration = config["break_time"] * 60  # 休息时间
        self.long_break_duration = config["long_break_time"] * 60  # 长休息时间
        self.long_break_interval = config["long_break_interval"]  # 长休息间隔
        self.long_break_interval_helper = 0  # 长休息间隔计数器
        self.tag = "工作"  # 当前状态 工作/休息/长休息
        self.time_left = self.work_duration

        # 初始化音频
        pygame.mixer.init()

        # 设置布局和控件
        self.layout = QVBoxLayout()
        self.label = QLabel("启动中...")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 设置计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.timer.start(1000)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label.setText(self.tag + '：' + self.format_time(self.time_left))
        else:
            self.switch_mode()

    def switch_mode(self, swich_mode=""):
        self.timer.stop()
        self.stop_play()
        if swich_mode:
            if self.tag == "工作":
                self.long_break_interval_helper += 1
            if swich_mode == "工作":
                self.time_left = self.work_duration
                self.tag = "工作"
            elif swich_mode == "休息":
                self.time_left = self.break_duration
                self.tag = "休息"
            else:
                self.time_left = self.long_break_duration
                self.long_break_interval_helper = 0
                self.tag = "长休息"
        else:
            if self.tag == "工作":
                self.play_sound(False)
                self.long_break_interval_helper += 1
                if self.long_break_interval_helper == self.long_break_interval:
                    self.time_left = self.long_break_duration
                    self.long_break_interval_helper = 0
                    self.tag = "长休息"
                else:
                    self.time_left = self.break_duration
                    self.tag = "休息"
            else:
                self.play_sound(True)
                self.time_left = self.work_duration
                self.tag = "工作"
        self.timer.start()

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def play_sound(self, is_start=True):
        if is_start:
            file_list = os.listdir(start_sound_path)
            file_list = [i for i in file_list if i.endswith(".mp3")]
            file_list = start_sound_path + choice(file_list)
        else:
            file_list = os.listdir(end_sound_path)
            file_list = [i for i in file_list if i.endswith(".mp3")]
            file_list = end_sound_path + choice(file_list)
        pygame.mixer.music.load(file_list)
        pygame.mixer.music.play()
        self.show()

    @staticmethod
    def stop_play():
        pygame.mixer.music.stop()

    def reset_timer(self):
        if self.tag == "工作":
            self.time_left = self.work_duration
        elif self.tag == "长休息":
            self.time_left = self.long_break_duration
        else:
            self.tag = "休息"
            self.time_left = self.break_duration

    def closeEvent(self, event):
        # 关闭界面时停止音效
        pygame.mixer.music.stop()
        event.accept()

    def showEvent(self, event):
        # 设置标签文本居中
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        event.accept()

    def play_random_sound(self):
        file_list = os.listdir(start_sound_path)
        file_list = [start_sound_path + i for i in file_list if i.endswith(".mp3")]
        end_list = os.listdir(end_sound_path)
        end_list = [end_sound_path + i for i in end_list if i.endswith(".mp3")]
        music_path = choice(file_list + end_list)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
