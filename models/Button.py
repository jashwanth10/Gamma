from PyQt6.QtWidgets import (
    QPushButton
)

class Button(QPushButton):

    def __init__(self,  button_name, parent, on_click):
        super().__init__(text=button_name, parent=parent)
        self.setFixedSize(100, 32)
        self.clicked.connect(on_click)
