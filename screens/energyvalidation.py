from components.interface import Ui_MainWindow


class EnergyValidation:

    def __init__(self, ui: Ui_MainWindow, processor=None):
        self.ui = ui
        self.processor = processor
        self.activate()
        pass


    def show_plots(self):
        self.processor.display_residual_plot(self.ui.residual_layout)
        pass
    def activate(self):

        pass
