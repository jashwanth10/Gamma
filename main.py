import sys
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPainter, QColor, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QBoxLayout,
    QStackedWidget,
    QStackedLayout,
    QDialog
)
from settings import *

class Overlay(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(512, 256))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 255, 255, 128))

class OverlayDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setWindowTitle("Browse")
        self.setGeometry(100, 100, 300, 200)
        widget = QLabel("Click me!", self)
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget)
        self.setLayout(layout)

    def showEvent(self, event):
        # When the dialog is shown, disable the main window
        if self.parent():
            self.parent().setEnabled(False)
            main_window_rect = self.parent().geometry()
            self.move(main_window_rect.center() - self.rect().center())

    def hideEvent(self, event):
        # When the dialog is hidden, enable the main window
        if self.parent():
            self.parent().setEnabled(True)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gamma")
        self.setWindowIcon(QIcon('assets/download.png'))
        self.setFixedSize(QSize(SCREEN["WIDTH"], SCREEN["HEIGHT"]))
        with open("css/styles.css", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        layout = QVBoxLayout()

        # Main Widget
        bg = QLabel(self)
        layout.addWidget(bg)


        # Toolbar Widget
        toolbar = QToolBar("My main toolbar")
        toolbar.setFixedHeight(36)
        toolbar.setMovable(False)
        draw_action_button = self._add_button(buttonName="Open", onClick=self._draw_overlay_open)
        calibration_action_button = self._add_button(buttonName="Calibrate", onClick=self._draw_overlay_calibrate)
        toolbar.addWidget(draw_action_button)
        toolbar.addSeparator()
        toolbar.addWidget(calibration_action_button)
        self.addToolBar(toolbar)



        self.setStatusBar(QStatusBar(self))

    def onOverlayClicked(self):
        print("Overlay Clicked!")

    def _draw_overlay_open(self):
        dialog = OverlayDialog(self)
        dialog.exec()
        return

    def _draw_overlay_calibrate(self):
        return

    def _add_button(self, buttonName, onClick, status="Button"):
        button = QPushButton(text=buttonName, parent=self)
        button.setFixedSize(100, 32)
        button.clicked.connect(onClick)
        return button


if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()