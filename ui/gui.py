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
        self.selected = None
        self.innerReload = True
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

        self.RenameBtn.clicked.connect(self.ins_rename)

        self.actionNew_instrument.triggered.connect(self.ins_new)
        self.actionDelete_Instrument.triggered.connect(self.ins_del)
        self.actioncompile.triggered.connect(self.compile)
        self.actionCompile_And_Run.triggered.connect(self.compile_run)
        self.action_Stop.triggered.connect(self.stop_sound)

        self.ChooseIns.currentIndexChanged.connect(self.select)

    def stop_sound(self):
        self.pm.stop_sound()

    def ins_rename(self):
        print("Renaming")
        new_name = self.RenameTxt.text()
        if new_name != "" and new_name != self.pm.instruments.keys() and self.selected != None:
            self.pm.instruments[new_name] = self.pm.instruments.pop(self.selected)
            self.selected = new_name
            self.reloadUI()


    def select(self):
        self.selected = self.ChooseIns.currentText()
        self.reloadUI()

    def reloadUI(self):
        print("Reloading the UI")
        print("ins:",self.pm.instruments)
        print("selected:",self.selected)
        
        if not self.innerReload: return
        self.innerReload = False
        
        self.ChooseIns.clear()
        self.ChooseIns.addItems(list(self.pm.instruments.keys()))
        
        if self.selected in self.pm.instruments.keys():
            self.instrumentMain.setText(self.pm.instruments[self.selected])
            self.ChooseIns.setCurrentIndex(list(self.pm.instruments.keys()).index(self.selected))
        else:
            self.instrumentMain.setText("Veuillez selectionner un intrument !")
            self.ChooseIns.setCurrentIndex(-1)
            self.selected = None
        self.innerReload = True

    def ins_new(self):
        print("ins_new")
        self.selected = self.pm.ins_new()
        self.reloadUI()
    
    def ins_del(self):
        print("ins_del")
        self.pm.ins_del(self.selected)
        self.selected = None
        self.reloadUI()

    def getInfo(self): # a reload too of selected
        print("getInfo")
        
        info = {}

        info["OUTFILE"] = self.OutFileName.text()
        info["SAMPLERATE"] = self.SampleRate.text()
        info["MAX_LEN"] = self.MaxLength.text()
        info["MAX_VOL"] = self.MaxVolume.text()
        info["NOTES"] = self.notesMain.toPlainText()
        info["INS_CODE"] = self.instrumentMain.toPlainText()
        info["INS_NAME"] = str(self.ChooseIns.currentText())

        self.selected = info["INS_NAME"]
        
        return info
    
    def reloadText(self,info):
        print("reloadText")
        self.OutFileName.setText(info["OUTFILE"])
        self.SampleRate.setText(info["SAMPLERATE"])
        self.MaxLength.setText(info["MAX_LEN"])
        self.notesMain.setText(info["NOTES"])
        self.MaxVolume.setText(info["MAX_VOL"])
        self.instrumentMain.setText(info["INS_CODE"])

        self.reloadUI()

    def compile_run(self):
        print("compile_run")
        self.compile()

    def compile(self):
        print("compile")
        inf = self.getInfo()
        self.pm.ins_update(inf["INS_NAME"],inf["INS_CODE"])
        self.pm.compile(inf)

    def file_new(self):
        print("file_new")
        self.active_file_path = None
        self.pm.instruments = {"ins_0":"return math.sin(frequency*math.pi*2*i)"}
        self.selected = "ins_0"
        self.notesMain.setText("(880,0,10,ins_0,1)")
        self.reloadUI()

    def file_open(self):
        print("file_open")
        
        file = QFileDialog.getOpenFileName(caption="Choose the file to open", filter="Python Files (*.py);;All Files (*)")
        
        print(file)
        file = file[0]
        
        try:
            self.reloadText(self.pm.load(file))
        except Exception as e:
            print("Error:",e);return

        self.active_file_path = file
        self.reloadUI()

    def file_saveas(self):
        self.active_file_path = QFileDialog.getSaveFileName(caption="Save as", filter="Python Files (*.py);;All Files (*)")[0]
        self.file_save()
        self.reloadUI()

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

