import sys
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from dsLogWindow import Ui_dsLog as DsLog
from logClassifier import Ui_logClassifier as LogClassifier
import qdarkgraystyle

class ClassifierScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = LogClassifier()
        self.ui.setupUi(self)
        
    #Signal packet should be:: [confirmed, type, SPECIFICS ]
    #comp specifics: key, type, number
    #prac speficis: str (send empty string and 0 for last fields)
    classifierData = pyqtSignal(bool, str, str, str, int, name='classifierData')

class MainScreen(QDialog):        
    def __init__(self):
        super().__init__()
        self.ui = DsLog()
        self.ui.setupUi(self)
        
        self.ui.addButton.clicked.connect(self.selectFile)
        self.ui.outButton.clicked.connect(self.close)
        self.fileListings = []
        self.classifierWindow = ClassifierScreen()

    def openClassifier(self):
        self.classifierWindow.exec_()
        
    def selectFile(self):
        logFolder = "C:/Users/Public/Documents/FRC/Log Files"
        dsFiles = "DS Logs (*.dslog)"
        fileName = QFileDialog.getOpenFileName(directory = logFolder, filter = dsFiles)[0]
        
        if len(fileName) > 0:
            shortName = fileName.split('/')[-1]
            
            if not fileName in self.fileListings:
                self.openClassifier()
                
                
                self.fileListings.append(fileName)
                self.ui.inputList.addItem(shortName)
                
                


def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    
    main = MainScreen()
    main.show()
    app.exec_()
    
if __name__ == '__main__':
    main()