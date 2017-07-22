import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *

X_GROESSE_FENSTER = 500
Y_GROESSE_FENSTER = 200
X_POS_FENSTER = 600
Y_POS_FENSTER = 300

class Fenster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        # Initialisierung
        # Menu Bar Elemente
        exitMe = QAction('&Exit',self)
        exitMe.setShortcut('Ctrl+E')
        exitMe.triggered.connect(self.close)
        #exitMe.setStatusTip('exit')

        convertMe = QAction(QIcon('Logo.png'), '&Convert',self)
        convertMe.setShortcut('Ctrl+C')
        convertMe.triggered.connect(self.convert)
        #convertMe.setStatusTip('convert')

        # Menu Bar
        menubar = self.menuBar()
        file = menubar.addMenu('&Datei') # Das und gibt die Moeglichkeit von Alt+D
        file.addAction(exitMe)
        file.addAction(convertMe)

        # Buttons
        #self.statusBar().showMessage('bereit')
        QToolTip.setFont(QFont('Arial', 8))
        button1 = QPushButton('konvertieren', self) # Self damit der Button auf dem Fenster ist
        button1.move(X_POS_FENSTER-300,Y_GROESSE_FENSTER-50)
        button1.setToolTip('Konvertierung von WAVE zu MP3')
        button1.clicked.connect(self.convert)

        button2 = QPushButton('Exit', self)  # Self damit der Button auf dem Fenster ist
        button2.move(X_POS_FENSTER-200,Y_GROESSE_FENSTER-50)
        button2.setToolTip('beende Programm')
        button2.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.setGeometry(X_POS_FENSTER, Y_POS_FENSTER, X_GROESSE_FENSTER, Y_GROESSE_FENSTER)
        self.setFixedSize(X_GROESSE_FENSTER, Y_GROESSE_FENSTER)
        self.setWindowTitle('Konverter Wave zu MP3')
        self.setWindowIcon(QIcon('Logo.png'))

        # anzeigen
        self.show()

    def convert(self):
        sender = self.sender()
        print("ok ")

    def keyPressEvent(self, QKeyEvent): # Bei Tastendruck
        if QKeyEvent.key() == Qt.Key_E:
            self.close()





app = QApplication(sys.argv)
w = Fenster()
sys.exit(app.exec_())

#datei = open(r'D:\test\vonKath.txt', "w")
#datei.write("hallo")
#datei.close()
#AudioSegment.from_wav(r'D:\test\vonKath.wav').export(r'D:\test\MP3vonKath.mp3', format="mp3")

