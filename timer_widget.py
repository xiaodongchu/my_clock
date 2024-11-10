import json
import os
from random import choice

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QTimer, Qt
import pygame

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
        self.is_working = True  # 是否在工作状态
        self.time_left = self.work_duration

        # 初始化音频
        pygame.mixer.init()

        # 设置布局和控件
        self.layout = QVBoxLayout()
        self.label = QLabel(self.format_time(self.time_left))
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 设置计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.start_timer()

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)  # 每秒更新一次
            self.play_sound(True)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.play_sound(False)
            self.switch_mode()

    def switch_mode(self, swich_mode=""):
        if swich_mode:
            if self.is_working:
                self.long_break_interval_helper += 1
            if swich_mode == "work":
                self.time_left = self.work_duration
                self.is_working = True
                self.label.setText("工作时间！")
            elif swich_mode == "break":
                self.time_left = self.break_duration
                self.is_working = False
                self.label.setText("休息时间！")
            elif swich_mode == "long_break":
                self.time_left = self.long_break_duration
                self.long_break_interval_helper = 0
                self.is_working = False
                self.label.setText("长休息时间！")
        else:
            if self.is_working:
                self.long_break_interval_helper += 1
                self.is_working = False
                if self.long_break_interval_helper == self.long_break_interval:
                    self.time_left = self.long_break_duration
                    self.long_break_interval_helper = 0
                    self.label.setText("长休息时间！")
                else:
                    self.time_left = self.break_duration
                    self.label.setText("休息时间！")
            else:
                self.time_left = self.work_duration
                self.is_working = True
                self.label.setText("工作时间！")

    def format_time(self, seconds):
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

    def stop_play(self):
        pygame.mixer.music.stop()

    def reset_timer(self):
        if self.is_working:
            self.time_left = self.work_duration
        elif self.long_break_interval_helper == 0:
            self.time_left = self.long_break_duration
        else:
            self.time_left = self.break_duration

    def closeEvent(self, event):
        # 关闭界面时停止音效
        pygame.mixer.music.stop()
        event.accept()

    def showEvent(self, event):
        # 设置标签文本居中
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        event.accept()
