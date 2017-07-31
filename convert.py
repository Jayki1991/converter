import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from pydub import AudioSegment
import list

X_GROESSE_FENSTER = 520
Y_GROESSE_FENSTER = 300
X_POS_FENSTER = 600
Y_POS_FENSTER = 300
MP3 = 'MP3'
MP4 = 'MP4'
WAVE = 'WAVE'
MOV = 'MOV'


class Fenster(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        # Initialisierung
        self.pfad = ' '
        self.area = list.List(self)
        self.area.setGeometry(10,40,255,190)
        self.vomTyp = WAVE
        self.zuTyp = MP3

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(300,150, 200,30)
        self.fromToText = QLabel("Konvertierung von WAVE zu MP3")

        fromText = QLabel("Von")
        zuText = QLabel(" => ")
        layout = QHBoxLayout()  # layout for the central widget
        layoutVertical = QVBoxLayout()
        layvfrom = QVBoxLayout()
        layvbetween = QVBoxLayout()
        layvto = QVBoxLayout()
        widget = QWidget(self)  # central widget
        widget.setLayout(layoutVertical)
        layout.addStretch(1)
        layoutVertical.addLayout(layout)

        fromGroup = QButtonGroup(widget)  # Gruppe von
        btnWave = QRadioButton(WAVE)
        btnWave.setChecked(True)
        fromGroup.addButton(btnWave)
        btnMov = QRadioButton(MOV)
        fromGroup.addButton(btnMov)
        #layvfrom.addWidget(fromText)
        layvfrom.addWidget(btnWave)
        layvfrom.addWidget(btnMov)
        layout.addLayout(layvfrom)

        layvbetween.addWidget(zuText)
        layout.addLayout(layvbetween)

        toGroup = QButtonGroup(widget)  # Gruppe zu
        btnMp3 = QRadioButton(MP3)
        btnMp3.setChecked(True)
        toGroup.addButton(btnMp3)
        btnMp4 = QRadioButton(MP4)
        toGroup.addButton(btnMp4)
        #layvto.addWidget(toText)
        layvto.addWidget(btnMp3)
        layvto.addWidget(btnMp4)
        layout.addLayout(layvto)
        layout.addSpacing(80)
        layoutVertical.addSpacing(110)
        layoutVertical.addWidget(self.fromToText)

        btnWave.setToolTip("Eine Wave-Datei konvertieren")
        btnMp4.setToolTip("Zu einer MP4-Datei konvertieren")
        btnMov.setToolTip("Eine MOV-Datei konvertieren")
        btnMp3.setToolTip("Zu einer MP3-Datei konvertieren")

        btnMp3.toggled.connect(lambda: self.toBtn("MP3"))
        btnMp4.toggled.connect(lambda: self.toBtn("MP4"))
        btnMov.toggled.connect(lambda: self.fromBtn("MOV"))
        btnWave.toggled.connect(lambda: self.fromBtn("WAVE"))



        # assign the widget to the main window+-
        self.setCentralWidget(widget)



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
        self.btnConvert = QPushButton('konvertieren', self) # Self damit der Button auf dem Fenster ist
        self.btnConvert.move(X_POS_FENSTER-300,Y_GROESSE_FENSTER-50)
        self.btnConvert.setToolTip('Konvertierung von WAVE zu MP3')
        self.btnConvert.clicked.connect(self.convert)

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

    def toBtn(self, _str):
        self.zuTyp = str(_str)
        self.textUpdate()

    def fromBtn(self, _str):
        self.vomTyp = str(_str)
        self.textUpdate()

    def textUpdate(self):
        stringText = 'Konvertierung von ' + str(self.vomTyp) + ' zu ' + str(self.zuTyp)
        self.fromToText.setText(stringText)
        if self.vomTyp == WAVE and self.zuTyp == MP3:
            self.btnConvert.setEnabled(True)
        elif self.vomTyp == MOV and self.zuTyp == MP4:
            self.btnConvert.setEnabled(False)
            self.btnConvert.setToolTip("Funktion noch nicht implementiert!")
        else:
            self.btnConvert.setEnabled(False)
            self.btnConvert.setToolTip("Keine Konvertierung von " + self.vomTyp + " zu " + self.zuTyp + "!")

    def speichernUnter(self):
        openData = QFileDialog.getExistingDirectory(self,"Open a folder","C://",QFileDialog.ShowDirsOnly)
        print(openData)
        self.textbox.setText(openData)
        self.pfad = openData

    def convert(self):
        # Funktionalitäten
        items = self.area.itemList.findItems('.', QtCore.Qt.MatchContains)
        von = ''
        zu =  ''
        if self.vomTyp == WAVE:
            von = '.wav'
        elif self.vomTyp == MOV:
            von = '.mov'
        else:
            print('error') # TODO error

        if self.zuTyp == MP3:
            zu = '.mp3'
        elif self.zuTyp == MP4:
            zu = '.mp4'
        else:
            print("error")
        print(von, zu)
        for i in items:
            self.area.itemList.setCurrentItem(i)
            j = i.text()
            toChange = j.split("///")
            z = toChange[1].split("/")
            ChangeName = z[len(z)-1]
            change = str(toChange[1])
            name = str(ChangeName).replace(von,zu)
            path = str(self.pfad)
            path += '/'
            print(change)
            print(path + name)
            if von == ".wav" and zu == ".mp3":
                AudioSegment.from_wav(change).export(path + name, format="mp3")
                self.area.itemList.currentItem().setCheckState(Qt.Checked)
            elif von == ".mov" and zu == ".mp4":
                print("TODO") # TODO Funktion finden

    def open(self):
        openData = QFileDialog.getOpenFileUrl(self, "Open a file", "C://")
        data = openData[0].toString()
        if self.area.drag(data):
            self.area.drop()

    def keyPressEvent(self, QKeyEvent): # Bei Tastendruck
        if QKeyEvent.key() == Qt.Key_E:
            self.close()

