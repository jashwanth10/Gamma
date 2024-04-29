from components.interface import Ui_MainWindow
from screens.energyvalidation import EnergyValidation
from screens.screens import Screen


class Profile:
    def __init__(self, ui: Ui_MainWindow, window=None):
        self.ui = ui
        self.index = 4
        self.window = window
        self.activate()
        pass

    def activate(self):
        # TODO: Make this profile section dynamic
        self.ui.profile_1_button.clicked.connect(lambda: self.transition_to_energy_validation_page())

    def transition_to_energy_validation_page(self):
        self.window.screens[Screen.ENERGY_VALIDATION_PAGE] = EnergyValidation(self.ui, self.window, self.window.main_processor)

        print("Hmm")
        self.ui.stackedWidget.setCurrentIndex(4)
