from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QVBoxLayout,
)
from settings import *
from models.FileUpload import FileUpload
from models.Button import Button


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
        draw_action_button = Button(parent=self, button_name="Open", on_click=self._draw_overlay_open)
        calibration_action_button = Button(parent=self, button_name="Configuration", on_click=self._draw_overlay_calibrate)
        toolbar.addWidget(draw_action_button)
        toolbar.addSeparator()
        toolbar.addWidget(calibration_action_button)
        self.addToolBar(toolbar)



        self.setStatusBar(QStatusBar(self))

    def onOverlayClicked(self):
        print("Overlay Clicked!")

    def _draw_overlay_open(self):
        dialog = FileUpload(self)
        dialog.exec()
        return

    def _draw_overlay_calibrate(self):
        return

    def _add_button(self, buttonName, onClick):
        button = QPushButton(text=buttonName, parent=self)
        button.setFixedSize(100, 32)
        button.clicked.connect(onClick)
        return button