import sys
from functools import partial
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from timer_widget import PomodoroTimer


class PomodoroApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # 创建主窗口
        self.window = PomodoroTimer()
        self.window.setWindowTitle("番茄时钟")

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(QIcon("aclock.ico"), self)
        self.tray_icon.setToolTip("番茄时钟")

        # 创建系统托盘菜单
        self.menu = QMenu()

        self.start_short_break_action = QAction("开始短休息")
        self.start_short_break_action.triggered.connect(partial(self.window.start_timer, "short_break"))

        self.start_long_break_action = QAction("开始长休息")
        self.start_long_break_action.triggered.connect(partial(self.window.start_timer, "long_break"))

        self.start_work_action = QAction("开始工作")
        self.start_work_action.triggered.connect(partial(self.window.start_timer, "work"))

        self.reset_timer_action = QAction("重置计时")
        self.reset_timer_action.triggered.connect(self.window.reset_timer)

        self.stop_play_action = QAction("停止播放")
        self.stop_play_action.triggered.connect(self.window.stop_play)

        self.exit_action = QAction("退出")
        self.exit_action.triggered.connect(self.quit)

        self.menu.addAction(self.start_short_break_action)
        self.menu.addAction(self.start_long_break_action)
        self.menu.addAction(self.start_work_action)
        self.menu.addAction(self.reset_timer_action)
        self.menu.addAction(self.stop_play_action)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.toggle_window)
        self.tray_icon.show()

    def toggle_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.window.isVisible():
                self.window.hide()
            else:
                self.window.show()


if __name__ == '__main__':
    app = PomodoroApp(sys.argv)
    app.window.show()
    sys.exit(app.exec())
