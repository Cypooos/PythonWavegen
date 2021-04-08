import sys

from PyQt5.QtWidgets import (
    QApplication, QFileDialog , QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from ui.main_window_ui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, pm, parent=None):
        super().__init__(parent)
        self.pm = pm
        print("init done")
        self.old_ins = None
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

        self.actionNew_instrument.triggered.connect(self.ins_new)
        self.actionDelete_Instrument.triggered.connect(self.ins_del)
        self.actioncompile.triggered.connect(self.compile)
        self.actionCompile_And_Run.triggered.connect(self.compile_run)
        self.action_Stop.triggered.connect(self.stop_sound)

        self.ChooseIns.currentIndexChanged.connect(self.ins_change)

    def stop_sound(self):
        self.pm.stop_sound()

    def ins_change(self):

        print(self.pm.instruments)
        print(self.old_ins)

        if self.old_ins != None:
            self.pm.ins_update(self.old_ins,self.instrumentMain.toPlainText())
        
        self.reloadIns()

    def reloadIns(self):
        
        if self.ChooseIns.currentText() != "":
            self.instrumentMain.setText(self.pm.instruments[self.ChooseIns.currentText()])
            self.old_ins = self.ChooseIns.currentText()
        else:
            self.instrumentMain.setText("Veuillez selectionner un intrument !")
            self.old_ins = None

    def ins_new(self):
        t = self.pm.ins_new()
        self.ChooseIns.addItem(t)
        self.ChooseIns.setCurrentIndex(list(self.pm.instruments.keys()).index(t))
        self.reloadIns()
    
    def ins_del(self):
        self.pm.ins_del(str(self.ChooseIns.currentText()))
        self.ChooseIns.clear()
        self.ChooseIns.addItems(list(self.pm.instruments.keys()))
        self.ChooseIns.setCurrentIndex(0)
        self.instrumentMain.setText("")
        self.old_ins = None
        self.reloadIns()

    def getInfo(self): # a reload too of old_ins
        
        info = {}

        info["OUTFILE"] = self.OutFileName.text()
        info["SAMPLERATE"] = self.SampleRate.text()
        info["MAX_LEN"] = self.MaxLength.text()
        info["MAX_VOL"] = self.MaxVolume.text()
        info["NOTES"] = self.notesMain.toPlainText()
        info["INS_CODE"] = self.instrumentMain.toPlainText()
        info["INS_NAME"] = str(self.ChooseIns.currentText())

        self.old_ins = info["INS_NAME"]
        
        return info
    
    def reloadText(self,info):
        self.OutFileName.setText(info["OUTFILE"])
        self.SampleRate.setText(info["SAMPLERATE"])
        self.MaxLength.setText(info["MAX_LEN"])
        self.notesMain.setText(info["NOTES"])
        self.MaxVolume.setText(info["MAX_VOL"])
        self.instrumentMain.setText(info["INS_CODE"])

        self.ChooseIns.clear()
        self.ChooseIns.addItems(list(self.pm.instruments.keys()))
        self.ChooseIns.setCurrentIndex(list(self.pm.instruments.keys()).index(info["INS_NAME"]))
        self.reloadIns()

    def compile_run(self):
        self.compile()

    def compile(self):
        inf = self.getInfo()
        self.pm.ins_update(inf["INS_NAME"],inf["INS_CODE"])
        self.pm.compile(inf)

    def file_new(self):
        self.active_file_path = None
        self.pm.instruments = {"ins_0":"return math.sin(frequency*math.pi*2*i)"}
        self.notesMain.setText("(880,0,10,ins_0,1)")
        self.ChooseIns.clear()
        self.ChooseIns.addItem("ins_0")
        self.ChooseIns.setCurrentIndex(0)
        self.reloadIns()

    def file_open(self):
        
        file = QFileDialog.getOpenFileName(caption="Choose the file to open", filter="Python Files (*.py);;All Files (*)")
        
        print(file)
        file = file[0]
        
        try:
            self.reloadText(self.pm.load(file))
        except Exception as e:
            print("Error:",e);return

        self.active_file_path = file
        self.reloadIns()

    def file_saveas(self):
        self.active_file_path = QFileDialog.getSaveFileName(caption="Save as", filter="Python Files (*.py);;All Files (*)")[0]
        self.file_save()
        self.reloadIns()

    def file_save(self):
        if self.active_file_path == None:
            self.active_file_path = QFileDialog.getSaveFileName(caption="Save as", filter="Python Files (*.py);;All Files (*)")[0]
        
        inf = self.getInfo()
        self.pm.ins_update(inf["INS_NAME"],inf["INS_CODE"])
        try:
            self.pm.save(inf,self.active_file_path)
        except Exception as e:
            print("Error:",e);return

    def about(self):
        QMessageBox.about(
            self,
            "About WaveMaker",
            "<p>A simple wave maker tool to make sounds !</p>"
            "<p>Made using Python, Qt, by @Cypooos</p>"
        )


def setup(pm):
    app = QApplication(sys.argv)
    win = Window(pm)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    setup()

