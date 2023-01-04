import sys

import psutil
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QFont

from form import Form
from process_info import get_main_info


class GetProcess(QtCore.QThread):
    new_process = QtCore.pyqtSignal(dict)

    def run(self):
        for item in psutil.process_iter():
            proc = get_main_info(item)
            print(proc)
            self.new_process.emit(proc)
        print("End")


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Form()
        self.ui.setupUi(self)
        self.showAllRow()

        self.thread = GetProcess()
        self.thread.new_process.connect(self.add_row)
        self.run_thread()

    def showAllRow(self):
        self.ui.table.update()

    def add_row(self, item):
        font = QFont()
        font.setBold(True)

        i = self.ui.table.rowCount()
        self.ui.table.insertRow(i)
        cellinfo = QtWidgets.QTableWidgetItem(str(item["pid"]))
        self.ui.table.setItem(i, 0, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(item["name"])
        self.ui.table.setItem(i, 1, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(item["status"])
        cellinfo.setFont(font)
        match (item["status"]):
            case "running":
                cellinfo.setBackground(QColor(0, 255, 0))
            case "stopped":
                cellinfo.setBackground(QColor(255, 0, 0))
        self.ui.table.setItem(i, 2, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(item["parents"])
        cellinfo.setToolTip(item["parents"])
        self.ui.table.setItem(i, 3, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(item["exe"])
        cellinfo.setToolTip(item["exe"])
        self.ui.table.setItem(i, 4, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(str(item["dll"]))
        cellinfo.setToolTip(str(item["dll"]))
        self.ui.table.setItem(i, 5, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(item["owner"]["username"])
        cellinfo.setToolTip(item["owner"]["username"])
        self.ui.table.setItem(i, 6, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(item["owner"]["sid"])
        cellinfo.setToolTip(item["owner"]["sid"])
        self.ui.table.setItem(i, 7, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(str(item["bin"]))
        self.ui.table.setItem(i, 8, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(str(item["dep"]))
        self.ui.table.setItem(i, 9, cellinfo)

        cellinfo = QtWidgets.QTableWidgetItem(str(item["aslr"]))
        self.ui.table.setItem(i, 10, cellinfo)

    def run_thread(self):
        self.thread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec())
