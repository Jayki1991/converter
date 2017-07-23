import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from pydub import AudioSegment

X_GROESSE_FENSTER = 520
Y_GROESSE_FENSTER = 300
X_POS_FENSTER = 600
Y_POS_FENSTER = 300

class List(QScrollArea):

    def __init__(self, parent):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptDrops(True)
        self.itemList = QListWidget()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidget(self.itemList)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            data = e.mimeData().text()
            if self.drag(data):
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def drag(self, data):
        self.nameOfItem = data
        print(data)
        x = self.nameOfItem.split(".")
        print("hier")
        if x[len(x) - 1] == 'wav':
            return True
        else:
            return False

    def drop(self):
        it = QListWidgetItem(self.nameOfItem)
        it.setFlags(Qt.ItemIsUserCheckable)
        it.setCheckState(Qt.Unchecked)
        self.itemList.addItem(it)

    def dropEvent(self, e):
        self.drop()

    def getItemList(self):
        return self.itemList


class Fenster(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        # Initialisierung
        self.pfad = ' '
        self.area = List(self)
        self.area.setGeometry(10,40,255,190)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(300,150, 200,30)

        # Menu Bar Elemente
        exitMe = QAction('&Exit',self)
        exitMe.setShortcut('Ctrl+E')
        exitMe.triggered.connect(self.close)
        #exitMe.setStatusTip('exit')

        convertMe = QAction(QIcon('Logo.png'), '&Convert',self)
        convertMe.setShortcut('Ctrl+C')
        convertMe.triggered.connect(self.convert)
        #convertMe.setStatusTip('convert')

        openMe = QAction('&Open',self)
        openMe.setShortcut('CTRL-O')
        openMe.triggered.connect(self.open)

        # Menu Bar
        menubar = self.menuBar()
        file = menubar.addMenu('&Datei') # Das und gibt die Moeglichkeit von Alt+D
        file.addAction(exitMe)
        file.addAction(convertMe)
        file.addAction(openMe)

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

        saveBtn = QPushButton('Speichern unter', self)
        saveBtn.move(300, 190)
        saveBtn.clicked.connect(self.speichernUnter)

        self.setGeometry(X_POS_FENSTER, Y_POS_FENSTER, X_GROESSE_FENSTER, Y_GROESSE_FENSTER)
        self.setFixedSize(X_GROESSE_FENSTER, Y_GROESSE_FENSTER)
        self.setWindowTitle('Konverter Wave zu MP3')
        self.setWindowIcon(QIcon('Logo.png'))

        # anzeigen
        self.show()

    def speichernUnter(self):
        openData = QFileDialog.getExistingDirectory(self,"Open a folder","C://",QFileDialog.ShowDirsOnly)
        print(openData)
        self.textbox.setText(openData)
        self.pfad = openData

    def convert(self):
        # Funktionalität
        items = self.area.itemList.findItems('.', QtCore.Qt.MatchContains)
        for i in items:
            self.area.itemList.setCurrentItem(i)
            j = i.text()
            toChange = j.split("///")
            z = toChange[1].split("/")
            ChangeName = z[len(z)-1]
            change = str(toChange[1])
            name = str(ChangeName).replace(".wav",".mp3")
            path = str(self.pfad)
            path += '/'
            print(change)
            print(path + name)
            AudioSegment.from_wav(change).export(path + name, format="mp3")
            self.area.itemList.currentItem().setCheckState(Qt.Checked)

    def open(self):
        openData = QFileDialog.getOpenFileUrl(self, "Open a file", "C://")
        data = openData[0].toString()
        if self.area.drag(data):
            self.area.drop()

    def keyPressEvent(self, QKeyEvent): # Bei Tastendruck
        if QKeyEvent.key() == Qt.Key_E:
            self.close()

app = QApplication(sys.argv)
w = Fenster()
sys.exit(app.exec_())

