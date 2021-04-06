import sys

from PyQt5.QtWidgets import (
    QApplication, QFileDialog , QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from main_window_ui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.file_new()

    def connectSignalsSlots(self):
        self.actionQuit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.actionSave_as.triggered.connect(self.file_saveas)
        self.actionSave.triggered.connect(self.file_save)
        self.actionOpen.triggered.connect(self.file_open)
        self.actionNew.triggered.connect(self.file_new)


    def file_new(self):
        self.active_file_path = None
        self.instrumentMain.setText("")


    def file_open(self):
        file = QFileDialog.getOpenFileName(caption="Choose the file to open", filter="Python Files (*.py);;All Files (*)")
        print(file)
        file = file[0]
        
        try:
            f = open(file,"r")
            content = f.read()
            f.close()
        except Exception as e:
            print("Error:",e);return
        
        self.instrumentMain.setText(content)
        self.active_file_path = file

    def file_saveas(self):
        self.active_file_path = QFileDialog.getSaveFileName(caption="Save as", filter="Python Files (*.py);;All Files (*)")[0]
        self.file_save()

    def file_save(self):
        if self.active_file_path == None:
            self.active_file_path = QFileDialog.getSaveFileName(caption="Save as", filter="Python Files (*.py);;All Files (*)")[0]
        
        try:
            file = open(self.active_file_path,"w")
        except Exception as e:
            print(e)
            self.active_file_path = None
            return
        
        file.write(self.instrumentMain.toPlainText())
        file.close()

    def about(self):
        QMessageBox.about(
            self,
            "About WaveMaker",
            "<p>A simple wave maker tool to make sounds !</p>"
            "<p>Made using Python, Qt, by @Cypooos</p>"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

