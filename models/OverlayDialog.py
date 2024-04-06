from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QDialog
)


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

