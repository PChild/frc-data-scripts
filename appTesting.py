import sys
from PyQt5.QtWidgets import QDialog, QApplication
from dsLogWindow import DsLog

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = DsLog()
        self.ui.setupUi(self)
        self.show()  

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())