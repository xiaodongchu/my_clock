import sys
import traceback
from functools import partial

from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from timer_widget import PomodoroTimer, icon_path, error_path


class PomodoroApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # 创建主窗口
        self.window = PomodoroTimer()
        self.window.setWindowTitle("番茄时钟")

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.setToolTip("番茄时钟")

        # 创建系统托盘菜单
        self.menu = QMenu()

        self.start_short_break_action = QAction("开始短休息")
        self.start_short_break_action.triggered.connect(partial(self.window.switch_mode, "休息"))

        self.start_long_break_action = QAction("开始长休息")
        self.start_long_break_action.triggered.connect(partial(self.window.switch_mode, "长休息"))

        self.start_work_action = QAction("开始工作")
        self.start_work_action.triggered.connect(partial(self.window.switch_mode, "工作"))

        self.reset_timer_action = QAction("重置计时")
        self.reset_timer_action.triggered.connect(self.window.reset_timer)

        self.stop_play_action = QAction("停止播放")
        self.stop_play_action.triggered.connect(self.window.stop_play)

        self.play_random_action = QAction("随机一曲")
        self.play_random_action.triggered.connect(self.window.play_random_sound)

        self.mute_action = QAction("静音")
        self.mute_action.setCheckable(True)
        self.mute_action.setChecked(self.window.is_muted)
        self.mute_action.triggered.connect(self.window.toggle_mute)

        self.exit_action = QAction("退出")
        self.exit_action.triggered.connect(self.quit)

        self.menu.addAction(self.start_short_break_action)
        self.menu.addAction(self.start_long_break_action)
        self.menu.addAction(self.start_work_action)
        self.menu.addAction(self.reset_timer_action)
        self.menu.addAction(self.stop_play_action)
        self.menu.addAction(self.play_random_action)
        self.menu.addAction(self.mute_action)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.toggle_window)
        self.tray_icon.show()

    def toggle_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.window.isVisible():
                self.window.close()
            else:
                self.window.show()


if __name__ == '__main__':
    try:
        app = PomodoroApp(sys.argv)
        app.window.show()
        sys.exit(app.exec())
    except Exception as e:
        f = open(error_path, 'a', encoding='utf-8')
        f.write(traceback.format_exc())
        f.write('\n' + str(e) + '\n')
        f.close()
        sys.exit(1)
