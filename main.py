import sys
import psutil
import cpuinfo

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QFrame
from gui import Ui_Frame

class Window(QFrame, Ui_Frame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.CloseButton.clicked.connect(self.close)
        self.MinButton.clicked.connect(self.showMinimized)

        self.old_pos = None
        self.last_update_pos = None
        self.mouse_move_timer = QTimer(self)
        self.mouse_move_timer.timeout.connect(self.update_window_position)

        self.Title_Bar.mousePressEvent = self.mouse_press_event
        self.Title_Bar.mouseMoveEvent = self.mouse_move_event
        self.Title_Bar.mouseReleaseEvent = self.mouse_release_event

        self.cpu_usage_timer = QTimer(self)
        self.cpu_usage_timer.timeout.connect(self.update_cpu_usage)
        self.cpu_usage_timer.start(1000)

        self.ram_timer = QTimer(self)
        self.ram_timer.timeout.connect(self.update_ram_info)
        self.ram_timer.start(1000)

        self.cpu_info = cpuinfo.get_cpu_info()
        self.cpu_name = self.cpu_info['brand_raw']
        model_name = self.cpu_name.split('@')[0].strip()
        self.CpuNameLabel.setText(model_name)

    def update_window_position(self):
        if self.old_pos and self.old_pos != self.last_update_pos:
            self.move(self.mapToGlobal(self.pos()) + self.old_pos - self.last_update_pos)
            self.last_update_pos = self.old_pos

    def update_cpu_usage(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        self.label_cpu.setText(f"{cpu_usage:.2f}%")

    def update_ram_info(self):
        ram_info = psutil.virtual_memory()
        ram_used = ram_info.used / (1024 ** 3)  # Convert to gigabytes
        ram_total = ram_info.total / (1024 ** 3)  # Convert to gigabytes
        ram_percentage = ram_info.percent
        self.RamUsed.setText(f"Ram Used: {ram_used:.1f} GB")
        self.RamTotal.setText(f"Ram Total: {ram_total:.1f} GB")
        self.label_ram.setText(f"{ram_percentage}%")

    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.old_pos = event.position()
            self.last_update_pos = event.position()
            self.mouse_move_timer.start(50)  # Throttle mouse move events

    def mouse_move_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            self.old_pos = event.position()

    def mouse_release_event(self, event):
        self.old_pos = None
        self.mouse_move_timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
