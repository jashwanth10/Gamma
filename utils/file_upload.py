from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QFileDialog

from utils.cnf_utils import read_cnf_file
from utils.processor import Processor


@pyqtSlot()
def open_dialog(window):
    filter = "CNF (*.CNF)"
    fnames = QFileDialog.getOpenFileName(
        window,
        "Open File",
        "C\\Desktop",
        filter
    )
    file_name = fnames[0]
    assert file_name.lower().endswith(('.cnf'))
    return file_name


@pyqtSlot()
def open_dialog_dataset(window, label):
    filter = "CNF (*.CNF)"
    fnames = QFileDialog.getOpenFileName(
        window,
        "Open File",
        "C\\Desktop",
        filter
    )
    file_name = fnames[0]
    label.setText(file_name)
    try:
        assert file_name.lower().endswith(('.cnf'))
        file = read_cnf_file(fnames[0], write_output=True)
        print(file.keys())
        for k in file.keys():
            print(k, file[k])
        p = Processor(file)

        # Call a service to calculate initial metrics
    except AssertionError:
        print("Need another file")
    except:
        print("error!")