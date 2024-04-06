from components.interface import Ui_MainWindow
from utils.file_upload import open_dialog


class Toolbar:

    def  __init__(self, ui: Ui_MainWindow):

        self.ui = ui
        self.ui.actionOpen.setEnabled(True)
        self.ui.actionSave.setEnabled(False)
        self.ui.actionPrint.setEnabled(False)
        self.ui.actionClose.setEnabled(False)
        self.ui.menuChart_Design.setEnabled(False)
        self.ui.menuCalibration.setEnabled(False)

        self.initiate_actions()
        pass

    def initiate_actions(self):
        self.ui.actionPrint.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.actionOpen.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.actionRun.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.actionRun.triggered.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))

    def file_uploaded_state(self):
        self.ui.actionSave.setEnabled(True)
        self.ui.actionPrint.setEnabled(True)
        self.ui.actionClose.setEnabled(True)
        self.ui.menuChart_Design.setEnabled(True)
        self.ui.menuCalibration.setEnabled(True)


