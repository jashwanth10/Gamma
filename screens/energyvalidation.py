from components.interface import Ui_MainWindow
from config.isotopes import ISOTOPES
from screens.peakanalysis import PeakAnalysis
from screens.screens import Screen
from utils.database import Database


class EnergyValidation:

    def __init__(self, profile, ui: Ui_MainWindow, window=None, processor=None):
        self.ui = ui
        self.profile_name = profile["name"]
        self.isotope_data = profile["isotopes"]
        self.db = Database()
        self.processor = processor
        self.window = window
        self.selected_item = None
        self.partially_deleted = []
        self.populate_dropdown()
        self.show_plots()
        self.activate()

    def populate_dropdown(self):
        keys = self.isotope_data.keys()
        print(keys)
        self.ui.validation_isotope_dropdown.clear()
        self.ui.validation_isotope_dropdown.addItems(["Choose.."])
        self.ui.validation_isotope_dropdown.addItems(keys)

    def show_plots(self):
        self.processor.analyze(isotope_data=self.isotope_data)
        for i in reversed(range(self.ui.residual_layout.count())):
            if self.ui.residual_layout.itemAt(i).widget():
                self.ui.residual_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.ui.fwhm_layout.count())):
            if self.ui.fwhm_layout.itemAt(i).widget():
                self.ui.fwhm_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.ui.energyVchannel_layout.count())):
            if self.ui.energyVchannel_layout.itemAt(i).widget():
                self.ui.energyVchannel_layout.itemAt(i).widget().setParent(None)


        if self.processor is not None:
            self.processor.display_residual_plot(window=self.window, layout=self.ui.residual_layout,
                                                 isotope_data=self.isotope_data)
            self.processor.display_fitting_curve(window=self.window, layout=self.ui.energyVchannel_layout,
                                                 isotope_data=self.isotope_data)
            self.processor.display_fwhm_plot(window=self.window, layout=self.ui.fwhm_layout,
                                             isotope_data=self.isotope_data)

    def activate(self):
        self.ui.validation_isotope_dropdown.activated.connect(self.index_changed)
        self.ui.analyze_button.clicked.connect(lambda: self.transition_to_peak_analysis_page())
        self.ui.del_peak_button.clicked.connect(lambda: self.delete_peak())
        self.ui.add_peak_button.clicked.connect(lambda: self.add_peak())
        self.ui.save_profile_button.clicked.connect(lambda: self.save_profile())

    def save_profile(self):
        self.db.insert(self.profile_name, self.isotope_data)

    def add_peak(self):
        isotope_name = self.ui.isotope_name.text()
        self.isotope_data[isotope_name] = {}
        self.isotope_data[isotope_name]["name"] = isotope_name
        self.isotope_data[isotope_name]["energy"] = float(self.ui.energy_value.text())
        self.isotope_data[isotope_name]["ref"] = float(self.ui.reference_width.text())
        self.isotope_data[isotope_name]["limit_HE_Rpic"] = [float(self.ui.he_rpic_left.text()), float(self.ui.he_rpic_right.text())]
        self.isotope_data[isotope_name]["limit_BE_Rpic"] = [float(self.ui.be_rpic_left.text()), float(self.ui.be_rpic_right.text())]
        self.isotope_data[isotope_name]["nb_canaux_BFBE"] = int(self.ui.nb_canaux_bfbe.text())
        self.isotope_data[isotope_name]["nb_canaux_BFHE"] = int(self.ui.nb_canaux_bfhe.text())
        self.isotope_data[isotope_name]["larger_region_pic"] = int(self.ui.larger_region_peak.text())
        self.isotope_data[isotope_name]["range"] = int(self.ui.range_value.text())

        self.populate_dropdown()
        self.show_plots()
        self.ui.tabWidget.setCurrentIndex(0)

    def delete_peak(self):
        selected_peak = self.ui.validation_isotope_dropdown.currentText().split(' ')[0]
        self.partially_deleted.append(selected_peak)
        self.isotope_data.pop(selected_peak)
        self.populate_dropdown()
        self.show_plots()
        pass

    def transition_to_peak_analysis_page(self):
        for i in reversed(range(self.ui.verticalLayout_2.count())):
            self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)
        values = self.processor.perform_peak_analysis(window=self.window, layout=self.ui.verticalLayout_2,
                                                      index=self.selected_item, isotope_data=self.isotope_data)
        self.window.screens[Screen.PEAK_ANALYSIS_PAGE] = PeakAnalysis(isotope_data=self.isotope_data, ui=self.ui,
                                                                      window=self.window,
                                                                      processor=self.window.main_processor,
                                                                      data=values)
        self.ui.stackedWidget.setCurrentIndex(5)

    def index_changed(self, ind):
        self.selected_item = ind - 1
        if (ind == 0):
            self.selected_item = None
