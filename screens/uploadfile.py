from components.interface import Ui_MainWindow
from utils.cnf_utils import read_cnf_file
from utils.file_upload import open_dialog, open_dialog_dataset
from utils.processor import Processor


class UploadFile:

    def __init__(self, ui: Ui_MainWindow, main_window, toolbar):
        self.index = 1
        self.ui = ui
        self.main_window = main_window
        self.toolbar = toolbar
        self.activate()

    def activate(self):
        self.ui.pushButton.clicked.connect(lambda: self.file_upload())

    def file_upload(self):
        try:
            file_name = open_dialog(self.main_window)
            p = Processor(*read_cnf_file(file_name))
            self.main_window.main_processor = p
            p.calculate_initial_metric(self.main_window, self.ui)
            self.ui.stackedWidget.setCurrentIndex(2)
            self.toolbar.file_uploaded_state()

        except:
            print("File Upload failed")

        pass