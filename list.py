from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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