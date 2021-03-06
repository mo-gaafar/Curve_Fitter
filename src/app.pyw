# https://namingconvention.org/python/ use the pythonic naming convention here (friendly reminder)

from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTabWidget
from modules import interface, errormap
from modules import resources
from modules.curvefit import *
from modules import errormap
import numpy as np
from modules.utility import print_debug
import sys


class MainWindow(QtWidgets.QMainWindow):
    ''' This is the PyQt5 GUI Main Window'''
    progressChanged = QtCore.pyqtSignal(int)
    endLoading = QtCore.pyqtSignal()
    startLoading = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        ''' Main window constructor'''

        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./resources/curvefittingwindow.ui', self)

        # set the title and icon
        self.setWindowIcon(QtGui.QIcon('./resources/icons/icon.png'))
        self.setWindowTitle("Curve Fitter")

        print_debug("Connectors Initialized")
        # initialize arrays and variables
        self.signal = Signal()
        self.signal_processor = SignalProcessor()
        self.hidden_row = 0
        self.toggle_progressBar = 0

        self.x_type = "No. Of Chunks"
        self.y_type = "Poly. Order"
        # initialize interface components
        interface.init_plots(self)
        interface.init_connectors(self)
        create_latex_figure(self)
        errormap.create_error_map_figure(self)


def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
