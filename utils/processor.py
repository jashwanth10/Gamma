import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel('energy(keV)')
        self.axes.set_ylabel('Count')
        super(MplCanvas, self).__init__(fig)
        self.show()

class Processor:

    def __init__(self, *args):
        self.data = args[0]
        self.name = args[1]
        pass

    def calculate_initial_metric(self, window, ui):
        '''
        :return: Plot of the count rate
        '''

        total_counts = self.data['Channels data']
        energy = self.data['Energy']
        sc = MplCanvas(width=5, height=5, dpi=100)
        sc.axes.plot(energy, total_counts)
        sc.axes.set_title(self.name.split('/')[-1])
        toolbar = NavigationToolbar(sc, window)
        ui.verticalLayout.addWidget(toolbar)
        ui.verticalLayout.addWidget(sc)

        pass

    def display_residual_plot(self, window, layout):

        # Calculate Peak positions

        # Optimize energy coefficients on click



        total_counts = self.data['Channels data']
        energy = self.data['Energy']
        sc = MplCanvas(width=5, height=5, dpi=100)
        sc.axes.plot(energy, total_counts)
        sc.axes.set_title(self.name.split('/')[-1])
        toolbar = NavigationToolbar(sc, window)
        layout.addWidget(toolbar)
        layout.addWidget(sc)
