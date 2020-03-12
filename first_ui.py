import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from Ui_movie import Ui_MainWindow

app=QApplication(sys.argv)
w=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(w)
w.show()
sys.exit(app.exec_())
