from components.interface import Ui_MainWindow
from screens.screens import Screen
from utils.cnf_utils import read_cnf_file
from utils.file_upload import open_dialog
from utils.processor import Processor
import shutil


class InitialMetrics:

    def __init__(self, ui: Ui_MainWindow, window):
        self.index = 2
        self.ui = ui
        self.window = window
        self.set_labels()
        self.set_actions()

    def set_labels(self):
        self.ui.text_u.setText(self.window.initial_processors["IAEA-U"].name.split("/")[-1])
        self.ui.text_th.setText(self.window.initial_processors["IAEA-Th"].name.split("/")[-1])
        self.ui.text_k.setText(self.window.initial_processors["IAEA-K"].name.split("/")[-1])

    def set_actions(self):
        self.ui.pushButton_10.clicked.connect(lambda: self.file_upload("IAEA-U"))
        self.ui.pushButton_11.clicked.connect(lambda: self.file_upload("IAEA-Th"))
        self.ui.pushButton_12.clicked.connect(lambda: self.file_upload("IAEA-K"))
        self.ui.update_calibration_button.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.energy_validation_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

    def file_upload(self, initial_file):
        try:
            file_name = open_dialog(self.window)
            self.window.initial_processors[initial_file] = Processor(*read_cnf_file(file_name))
            self.set_labels()
            shutil.copy(file_name, "config/calibration data/" + initial_file + ".CNF")

        except:
            pass

    def run_calibration(self):
        self.ui.stackedWidget.setCurrentIndex(3)
