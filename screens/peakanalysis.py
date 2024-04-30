from components.interface import Ui_MainWindow
from config.isotopes import ISOTOPES
from screens.screens import Screen


class PeakAnalysis:

    def __init__(self, isotope_data, ui: Ui_MainWindow, window=None, processor=None, data=None):
        self.ui = ui
        self.isotope_data = isotope_data
        self.processor = processor
        self.window = window
        self.data = data
        self.populate_page()
        self.activate()

    def activate(self):
        self.ui.back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.pa_next.clicked.connect(lambda: self.transition_next())
        self.ui.pa_prev.clicked.connect(lambda: self.transition_previous())

    def transition_next(self):
        for i in reversed(range(self.ui.verticalLayout_2.count())):
            self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)
        values = self.processor.perform_peak_analysis(window=self.window, layout=self.ui.verticalLayout_2,
                                                      index=(self.data["index"] + 1) % len(
                                                          list(self.isotope_data.keys())),
                                                      isotope_data=self.isotope_data)

        self.data = values
        self.populate_page()
        pass

    def transition_previous(self):
        for i in reversed(range(self.ui.verticalLayout_2.count())):
            self.ui.verticalLayout_2.itemAt(i).widget().setParent(None)
        values = self.processor.perform_peak_analysis(window=self.window, layout=self.ui.verticalLayout_2,
                                                      index=(self.data["index"] - 1) % len(
                                                          list(self.isotope_data.keys())),
                                                      isotope_data=self.isotope_data)
        self.data = values
        self.populate_page()
        pass

    def populate_page(self):
        self.ui.total_hits_bfbe.setText(f'{self.data["BFBE"]["total_hits"]:.2f}')
        self.ui.hits_per_channel_bfbe.setText(f'{self.data["BFBE"]["hits_per_channel"]:.2f}')
        self.ui.total_hits_bfhe.setText(f'{self.data["BFHE"]["total_hits"]:.2f}')
        self.ui.hits_per_channel_bfhe.setText(f'{self.data["BFHE"]["hits_per_channel"]:.2f}')

        self.ui.total_hits_roi.setText(f'{self.data["region"]["total_hits"]:.2f}')
        self.ui.num_channels_peak.setText(f'{self.data["region"]["num_channels"]:.2f}')

        self.ui.total_hits_pic.setText(f'{self.data["pic"]["total_hits"]:.2f}')
        self.ui.num_channels_peak_2.setText(f'{self.data["pic"]["num_channels"]:.2f}')

        self.ui.channel_peak.setText(f'{self.data["results"]["peak_channel"]:.2f}')
        self.ui.energy_peak.setText(f'{self.data["results"]["peak_energy"]:.2f}')
        self.ui.fwhm.setText(f'{self.data["results"]["fwhm"]:.2f}')
