from pyqtgraph import QtWidgets

from components.interface import Ui_MainWindow
from screens.energyvalidation import EnergyValidation
from screens.screens import Screen
from utils.database import Database
from config.isotopes import ISOTOPES


class Profile:
    def __init__(self, ui: Ui_MainWindow, window=None):
        self.ui = ui
        self.index = 4
        self.window = window
        self.db = Database()
        self.activate()
        pass

    def activate(self):
        # TODO: Make this profile section dynamic

        # Show all the available profiles
        profiles = self.db.query("profiles")
        self.ui.profile_buttons = []
        for ind, profile in enumerate(profiles):
            self.create_profile(ind, profile)
            self.ui.profile_buttons[ind].clicked.connect(lambda: self.transition_to_energy_validation_page(profile))

        self.create_profile(len(profiles), "Add..")
        self.ui.profile_buttons[len(profiles)].clicked.connect(lambda: print("hello world"))

    def transition_to_energy_validation_page(self, profile):
        isotope_data = self.db.query(profile)
        self.window.screens[Screen.ENERGY_VALIDATION_PAGE] = EnergyValidation(
            profile={"name": profile, "isotopes": isotope_data}, ui=self.ui,
            window=self.window,
            processor=self.window.main_processor)

        print("Hmm")
        self.ui.stackedWidget.setCurrentIndex(4)

    def create_profile(self, index, profile_name):
        self.ui.profile_buttons.append(QtWidgets.QPushButton(parent=self.ui.layoutWidget2))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.profile_buttons[index].sizePolicy().hasHeightForWidth())
        self.ui.profile_buttons[index].setSizePolicy(sizePolicy)
        self.ui.profile_buttons[index].setStyleSheet("  background-color: #0095ff;\n"
                                                     "  border-radius: 3px;\n"
                                                     "color: #fff;")
        self.ui.profile_buttons[index].setText(profile_name)
        self.ui.gridLayout.addWidget(self.ui.profile_buttons[index], index // 3, index % 3, 1, 1)
