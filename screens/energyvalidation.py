from components.interface import Ui_MainWindow
from config.isotopes import ISOTOPES
from screens.peakanalysis import PeakAnalysis
from screens.screens import Screen


class EnergyValidation:

    def __init__(self, ui: Ui_MainWindow, window=None, processor=None):
        self.ui = ui
        self.processor = processor
        self.window = window
        self.selected_item = None
        self.show_plots()
        self.activate()

    def show_plots(self):
        if self.processor is not None:
            self.processor.display_residual_plot(window=self.window, layout=self.ui.residual_layout)
            self.processor.display_fitting_curve(window=self.window, layout=self.ui.energyVchannel_layout)
            self.processor.display_fwhm_plot(window=self.window, layout=self.ui.fwhm_layout)

    def activate(self):
        self.ui.validation_isotope_dropdown.activated.connect(self.index_changed)
        self.ui.analyze_button.clicked.connect(lambda: self.transition_to_peak_analysis_page())
        self.ui.del_peak_button.clicked.connect(lambda: self.delete_peak())

    # def delete_peak(self):

    def transition_to_peak_analysis_page(self):
        for i in reversed(range(self.ui.verticalLayout_2.count())):
            self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)
        values = self.processor.perform_peak_analysis(window=self.window, layout=self.ui.verticalLayout_2,
                                                      index=self.selected_item)
        self.window.screens[Screen.PEAK_ANALYSIS_PAGE] = PeakAnalysis(self.ui, self.window, self.window.main_processor,
                                                                      data=values)
        self.ui.stackedWidget.setCurrentIndex(5)

    def index_changed(self, ind):
        self.selected_item = ind - 1
        if (ind == 0):
            self.selected_item = None
