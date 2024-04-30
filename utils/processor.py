import math

import matplotlib
from PyQt6.QtGui import QPainterPath
from matplotlib.backends.backend_template import FigureCanvas

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import pyqtgraph as pg


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, x_label='energy(keV)',y_label='Count', dpi=100):
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        super(MplCanvas, self).__init__(fig)
        self.show()


def _max_index_less_than(arr, target):
    low, high = 0, len(arr)
    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid

    return low - 1 if low > 0 else -1


class Processor:

    def __init__(self, *args):
        self.data = args[0]
        self.name = args[1]
        self.channels = self.data['Channels']
        self.counts = self.data['Channels data']
        self.energies = self.data['Energy']
        self.peaks = {}
        self.fwhm = {}
        self.energy_portion = {}
        self.BFHE = {}
        self.BFBE = {}
        self.roi = {}
        self.roi_peak = {}
        self.bf_step = {}
        self.interest_region_counts = {}
        self.interest_region_energies = {}
        self.interest_region_indices = {}
        pass

    def analyze(self, isotope_data):
        self.calculate_interest_region(isotope_data)
        self.calculate_fwhm(isotope_data)
        self.calculate_peak_positions(isotope_data)
        self.calculate_narrow_peak_portion(isotope_data)

    def _peak_calibration(self, pos):
        return self.data["Energy coefficients"][0]*(pos**0) \
                + self.data["Energy coefficients"][1]*(pos**1)\
                + self.data["Energy coefficients"][2]*(pos**2)

    def _extract_portions(self, lower, upper):
        lower_ind = _max_index_less_than(self.energies, lower)
        upper_ind = _max_index_less_than(self.energies, upper)
        return lower_ind, upper_ind

    def _extract_index(self, energy):
        lower_ind = _max_index_less_than(self.energies, energy)
        return lower_ind

    def calculate_peak_positions(self, isotope_data):
        for key in isotope_data.keys():
            lower = isotope_data[key]["energy"] - isotope_data[key]["limit_BE_Rpic"][0]
            upper = isotope_data[key]["energy"] + isotope_data[key]["limit_HE_Rpic"][0]
            lower_ind, upper_ind = self._extract_portions(lower, upper)
            counts_portion = self.counts[lower_ind:upper_ind+1]
            channels_portion = self.channels[lower_ind:upper_ind+1]
            energy_portion = self.energies[lower_ind:upper_ind+1]
            self.roi[key] = {}
            self.roi[key]["total_hits"] = np.sum(np.array(counts_portion))
            self.roi[key]["num_channels"] = len(counts_portion)
            self.roi[key]["total_bf_under_peak"] = self.roi[key]["num_channels"] * ((self.BFBE[key]["hits_per_channel"] + self.BFHE[key]["hits_per_channel"])/2)
            self.roi[key]["net_hits"] = self.roi[key]["total_hits"] - self.roi[key]["total_bf_under_peak"]

            self.peaks[key] = channels_portion[np.argmax(counts_portion)]
            self.energy_portion[key] = energy_portion[np.argmax(counts_portion)]

    def calculate_interest_region(self, isotope_data):
        for key in isotope_data.keys():
            lower = isotope_data[key]["energy"] - isotope_data[key]["limit_BE_Rpic"][1]
            left_index = self._extract_index(lower) - 2*isotope_data[key]["nb_canaux_BFBE"]
            right_index = left_index + isotope_data[key]["range"]
            self.interest_region_energies[key] = self.energies[left_index:right_index+1]
            self.interest_region_indices[key] = list([left_index, right_index])
            self.interest_region_counts[key] = self.counts[left_index:right_index+1]

    def calculate_fwhm(self, isotope_data):
        for key in isotope_data.keys():
            lower = isotope_data[key]["energy"] - isotope_data[key]["limit_BE_Rpic"][0]
            upper = isotope_data[key]["energy"] + isotope_data[key]["limit_HE_Rpic"][0]
            lower_ind, upper_ind = self._extract_portions(lower, upper)

            energy_val_left = isotope_data[key]["energy"] - isotope_data[key]["limit_BE_Rpic"][1]
            left_index = self._extract_index(energy_val_left)
            left_count_portion = np.array(self.counts[left_index - isotope_data[key]["nb_canaux_BFBE"]:left_index+1])
            left_coups_total = np.sum(left_count_portion)
            left_coups_per_canal = left_coups_total/isotope_data[key]["nb_canaux_BFHE"]
            self.BFBE[key] = {}
            self.BFBE[key]["total_hits"] = left_coups_total
            self.BFBE[key]["hits_per_channel"] = left_coups_per_canal
            self.BFBE[key]["indices"] = (left_index - isotope_data[key]["nb_canaux_BFBE"], left_index+1)

            energy_val_right = isotope_data[key]["energy"] + isotope_data[key]["limit_HE_Rpic"][1]
            right_index = self._extract_index(energy_val_right)
            right_count_portion = np.array(self.counts[right_index:right_index+isotope_data[key]["nb_canaux_BFHE"]+1])
            right_coups_total = np.sum(right_count_portion)
            right_coups_per_canal = right_coups_total/isotope_data[key]["nb_canaux_BFHE"]
            self.BFHE[key] = {}
            self.BFHE[key]["total_hits"] = right_coups_total
            self.BFHE[key]["hits_per_channel"] = right_coups_per_canal
            self.BFHE[key]["indices"] = (right_index, right_index+isotope_data[key]["nb_canaux_BFHE"]+1)

            counts_portion = np.array(self.counts[lower_ind:upper_ind+1])

            self.bf_step[key] = []
            for i in range(len(counts_portion)):
                val = np.sum(counts_portion[0:i])/np.sum(counts_portion)
                self.bf_step[key].append(right_coups_per_canal + (left_coups_per_canal - right_coups_per_canal)*val)

            coups_nets = counts_portion - np.array(self.bf_step[key])
            energy_portion = np.array(self.energies[lower_ind:upper_ind+1])
            minus = np.sum(np.multiply(coups_nets, energy_portion))/np.sum(coups_nets)
            self.fwhm[key] = 2.36*np.sqrt((np.sum(np.multiply(coups_nets, np.multiply(energy_portion, energy_portion)))/np.sum(coups_nets)) - minus**2)

    def calculate_narrow_peak_portion(self, isotope_data):
        for key in isotope_data.keys():
            lower = isotope_data[key]["energy"] - isotope_data[key]["larger_region_pic"]/2
            upper = isotope_data[key]["energy"] + isotope_data[key]["larger_region_pic"]/2
            lower_ind, upper_ind = self._extract_portions(lower, upper)
            counts_portion = self.counts[lower_ind:upper_ind+1]
            print(key)
            self.roi_peak[key] = {}
            self.roi_peak[key]["total_hits"] = np.sum(np.array(counts_portion))
            self.roi_peak[key]["num_channels"] = len(counts_portion)
            self.roi_peak[key]["total_bf_under_peak"] = self.roi[key]["num_channels"] * ((self.BFBE[key]["hits_per_channel"] + self.BFHE[key]["hits_per_channel"])/2)
            self.roi_peak[key]["net_hits"] = self.roi[key]["total_hits"] - self.roi[key]["total_bf_under_peak"]

    def calculate_initial_metric(self, window, ui):
        total_counts = self.data['Channels data']
        energy = self.data['Energy']
        sc = MplCanvas(dpi=100)
        sc.axes.plot(energy, total_counts)
        sc.axes.set_title(self.name.split('/')[-1])
        toolbar = NavigationToolbar(sc, window)
        ui.verticalLayout.addWidget(toolbar)
        ui.verticalLayout.addWidget(sc)

    def display_residual_plot(self, window, layout, isotope_data):

        #y-axis
        residuals = [self._peak_calibration(self.peaks[key]) - isotope_data[key]["energy"] for key in isotope_data.keys()]

        #x-axis
        energies = [isotope_data[key]["energy"] for key in isotope_data.keys()]
        pos = [{'pos': (x, y)} for (x, y) in zip(energies, residuals)]
        view = pg.ViewBox()
        data = [isotope_data[key]["name"] for key in isotope_data.keys()]
        scatter = pg.ScatterPlotItem(pos, hoverable=True, data=data)
        view.addItem(scatter)
        plot_item = pg.PlotItem(labels={'left': "residual", 'bottom': "energy(keV)"}, title="Residual-Energy(keV) plot", viewBox=view)
        plot_widget = pg.PlotWidget(plotItem=plot_item)

        layout.addWidget(plot_widget)

    def display_fitting_curve(self, window, layout, isotope_data):

        # Generate residual plot
        x = np.array([self.peaks[key] for key in isotope_data.keys()])
        y = np.array([self._peak_calibration(self.peaks[key]) for key in isotope_data.keys()])
        plot_widget = pg.plot(x, y, symbol='+')
        layout.addWidget(plot_widget)

    def display_fwhm_plot(self, window, layout, isotope_data):

        sc = MplCanvas(width=4, height=4, x_label='energy(keV)', y_label='FWHM')

        x = [self.energy_portion[key] for key in isotope_data.keys()]
        y1 = [isotope_data[key]["ref"] for key in isotope_data.keys()]
        y2 = [self.fwhm[key] for key in isotope_data.keys()]
        print(y1, y2)
        sc.axes.plot(x, y1, color='r')
        sc.axes.scatter(x, y2)
        sc.axes.set_title("Reference Curve")
        toolbar = NavigationToolbar(sc, window)
        layout.addWidget(sc)
        layout.addWidget(toolbar)

    def perform_peak_analysis(self, window, layout, index, isotope_data):

        key = list(isotope_data.keys())[index]

        # Display plot
        x = self.interest_region_energies[key]

        # Just counts
        y1 = self.interest_region_counts[key]

        # Peak area
        a = np.zeros(len(self.energies))
        left = isotope_data[key]["energy"] - isotope_data[key]["limit_BE_Rpic"][0]
        right = isotope_data[key]["energy"] + isotope_data[key]["limit_HE_Rpic"][0]
        left_index, right_index = self._extract_portions(left, right)
        a[left_index:right_index+1] = self.counts[left_index:right_index+1]
        y2 = a[self.interest_region_indices[key][0]: self.interest_region_indices[key][1]+1]

        # BF Step
        a = np.zeros(len(self.energies))
        a[left_index:right_index + 1] = self.bf_step[key]
        y3 = a[self.interest_region_indices[key][0]: self.interest_region_indices[key][1] + 1]

        # Peak
        a = np.zeros(len(self.energies))
        a[left_index:right_index + 1] = self.counts[left_index:right_index+1] - self.bf_step[key]
        y4 = a[self.interest_region_indices[key][0]: self.interest_region_indices[key][1] + 1]
        #
        # # BFBE
        # a = np.zeros(len(self.energies))
        # a[left_index:right_index + 1] = self.counts[left_index:right_index + 1] - self.bf_step[key]
        # y5 = a[self.interest_region_indices[0]: self.interest_region_indices[1] + 1]


        sc = MplCanvas(width=4, height=4, x_label='energy(keV)', y_label='Counts')
        sc.axes.plot(x, y1, color='b')
        sc.axes.plot(x, y2, color='k')
        sc.axes.plot(x, y3, color='y')
        sc.axes.plot(x, y4, color='g')

        sc.axes.set_title("Peak: " + key)

        toolbar = NavigationToolbar(sc, window)
        layout.addWidget(sc)
        layout.addWidget(toolbar)

        # Return BFBE, BFHE, Region, Pic, results
        return {
            "BFBE": self.BFBE[key],
            "BFHE": self.BFHE[key],
            "region": self.roi[key],
            "pic": self.roi_peak[key],
            "results": {
                "fwhm": self.fwhm[key],
                "peak_channel": self.peaks[key],
                "peak_energy": self.energy_portion[key],
                "sigma": isotope_data[key]["larger_region_pic"] * 2.36 / self.fwhm[key]
            },
            "index": index
        }

        pass

