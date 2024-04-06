import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)
from components.interface import Ui_MainWindow
from screens.initialmetrics import InitialMetrics
from screens.profile import Profile
from utils.cnf_utils import read_cnf_file
from screens.home import Home
from screens.toolbar import Toolbar
from screens.uploadfile import UploadFile
from utils.processor import Processor
from screens.screens import Screen



class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.screens = {}
        self.initial_processors = {}
        self.main_processor = None

        # self.initiate_actions()
        self.initiate_processors()


    def initiate_processors(self):
        file_u = "./config/calibration data/IAEA-U.CNF"
        file_k = "./config/calibration data/IAEA-K.CNF"
        file_th = "./config/calibration data/IAEA-Th.CNF"

        self.initial_processors["IAEA-U"] = Processor(*read_cnf_file(file_u))
        self.initial_processors["IAEA-K"] = Processor(*read_cnf_file(file_k))
        self.initial_processors["IAEA-Th"] = Processor(*read_cnf_file(file_th))

    def initiate_screens(self, ui):
        self.screens[Screen.TOOLBAR] = Toolbar(ui)
        self.screens[Screen.HOME] = Home(ui)
        self.screens[Screen.UPLOAD_FILE] = UploadFile(ui, main_window=self, toolbar=self.screens[Screen.TOOLBAR])
        self.screens[Screen.INITIAL_METRICS] = InitialMetrics(ui, self)
        self.screens[Screen.PROFILE_PAGE] = Profile(ui)

        pass

    def switch_page(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.initiate_screens(ui)
    window.show()
    sys.exit(app.exec())