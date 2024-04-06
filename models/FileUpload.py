from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QDialog,
    QFileDialog
)
from models.Button import Button


class FileUpload(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setWindowTitle("Add file to Calibrate")
        self.setGeometry(100, 100, 300, 200)
        widget = Button(button_name="Upload", parent=self, on_click=self.show_file_dialog)
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

    def show_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File', '',
                                                   'All Files (*);;Text Files (*.txt);;Python Files (*.py)')

        if file_path:
            print(f'Selected File: {file_path}')

