from components.interface import Ui_MainWindow


class Profile:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.index = 4
        pass

    def activate(self):
        self.ui.validation_isotope_dropdown.activated.connect(lambda x: print(x))
        pass