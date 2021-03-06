
from threading import Thread, Lock
import threading
from modules.utility import print_debug
from modules import interface
from copy import copy
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np
import seaborn as sn

plt.rcParams['axes.facecolor'] = 'black'
plt.rc('axes', edgecolor='w')
plt.rc('xtick', color='w')
plt.rc('ytick', color='w')
plt.rcParams['axes.titlecolor'] = "white"
plt.rcParams['axes.labelcolor'] = "white"
plt.rcParams["figure.autolayout"] = True


def values(self, type):
    # whether what the user chose it will still be the same no. for both axes
    # TODO: should be more flexible and dependent on parameter and interpolation type
    vals = []
    if type == "No. Of Chunks":
        vals = np.arange(1, 8)
    elif type == "Poly. Order":
        vals = np.arange(1, 6)
    elif type == "% Overlap":
        vals = np.arange(0, 13)
    return vals


def select_error_x(self, x_type="No. Of Chunks"):
    self.x_type = x_type


def select_error_y(self, y_type="Poly. Order"):
    self.y_type = y_type


def normalization(self):
    self.normalized_error = []
    min = np.amin(self.percentage_error)
    max = np.amax(self.percentage_error)

    for i in self.percentage_error:
        self.normalized_error_temp = []
        for j in i:
            value = (j - min) / (max - min)
            self.normalized_error_temp.append(value)
        self.normalized_error.append(self.normalized_error_temp)


def enter(self, order=3, chunks=10, overlap=9):
    # gets user defaults from original signal processor object
    if order == 3:
        order = self.signal_processor.interpolation_order
    if chunks == 10:
        chunks = self.signal_processor.max_chunks
    if overlap == 9:
        overlap = self.signal_processor.overlap_percent

    # sets user input

    self.signal_processor_error.interpolation_order = order
    self.signal_processor_error.max_chunks = chunks
    self.signal_processor_error.overlap_percent = overlap


def type_selection(self, x_type, y_type, i, j):
    # order,chunks,overlap
    self.y_type == y_type
    self.x_type == x_type
    if (self.y_type == "No. Of Chunks" and self.x_type == "Poly. Order"):
        enter(self, order=i, chunks=j)
    elif(self.y_type == "Poly. Order" and self.x_type == "No. Of Chunks"):
        enter(self, order=j, chunks=i)
    elif (self.y_type == "No. Of Chunks" and self.x_type == "% Overlap"):
        enter(self, chunks=j, overlap=i)
    elif (self.y_type == "% Overlap" and self.x_type == "No. Of Chunks"):
        enter(self, chunks=i, overlap=j)
    elif(self.y_type == "% Overlap" and self.x_type == "Poly. Order"):
        enter(self, order=i, overlap=j)
    elif (self.y_type == "Poly. Order" and self.x_type == "% Overlap"):
        enter(self, order=j, overlap=i)
    else:
        raise Exception("Invalid Selection")


def error_map(self):
    if(len(self.signal_processor.original_signal)==0):
        QtWidgets.QMessageBox.warning(
            self, 'NO SIGNAL ', 'You have to enter a signal first')
    else:
        print_debug("error map assigned to thread: {}".format(
            threading.current_thread().name))
        lock = Lock()

        t1 = Thread(target=calculate_error, args=(
            self,), name='error map thread')
        # start threads
        t1.start()
        # wait until threads finish their job
        # t1.join()


def calculate_error(self, loading_counter: int = 0):
    self.toggle_progressBar = 0

    # progress bar
    # TODO: both axis should be same size
    # values  and type of axis
    # for loop to get interpolated
    # put in array
    # compare original and interpolated
    self.signal_processor_error = copy(self.signal_processor)

    interface.progressBar_update(self, 1)

    self.x_values = values(self, self.x_type)

    self.y_values = values(self, self.y_type)

    print_debug("calculate error assigned to thread: {}".format(
        threading.current_thread().name))

    x = self.x_values
    y = self.y_values

    self.percentage_error = []
    for j in y:
        # to iterate on the y ranges
        self.percentage_error_temp = []
        for i in x:
            # intrapolate according to the 2 numbers and add to the matrix

            # order,chunks,overlap
            type_selection(self, self.x_type, self.y_type, i, j)

            self.signal_processor_error.interpolate()

            self.percentage_error_temp.append(
                self.signal_processor_error.percentage_error())

            print_debug("Error Calculated: " + "x =" + str(i) + " y=" + str(j))
        self.percentage_error.append(self.percentage_error_temp)

    interface.progressBar_update(self, 2)
    if self.toggle_progressBar == 1:
        return

    normalization(self)

    interface.progressBar_update(self, 3)
    if self.toggle_progressBar == 1:
        return
    plot_error_map(self, self.normalized_error, self.x_type, self.y_type)
    # multithreading
    # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
    pass


def create_error_map_figure(self):
    self.figure = plt.figure()
    self.figure.patch.set_facecolor('black')
    self.axes = self.figure.add_subplot()
    self.ErrorMap = Canvas(self.figure)
    self.error_plot_box.addWidget(self.ErrorMap)
    # plot_error_map(self) # CALL WHEN ERROR_BUTTON IS CLICKED INSTEAD


def plot_error_map(self, data=[], xlabel='', ylabel=''):

    self.axes.clear()
    plt.clf()


# plotting the heatmap
    erorr_map = sn.heatmap(data=data)

# displaying the plotted heatmap
    # plt.show()

    plt.title('Error Map')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    self.ErrorMap.draw()
    self.figure.canvas.draw()
