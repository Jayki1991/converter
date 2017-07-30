import sys
from PyQt5.QtWidgets import *
import convert

app = QApplication(sys.argv)
w = convert.Fenster()
sys.exit(app.exec_())