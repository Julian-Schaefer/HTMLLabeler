from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt5.QtCore import Qt, pyqtSlot, QFile, QIODevice, QObject
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView as QWebView,
    QWebEnginePage as QWebPage,
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineSettings as QWebSettings,
    QWebEngineScript,
)
from PyQt5.QtWebChannel import QWebChannel
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtNetwork import *
import sys
from optparse import OptionParser
import json
from browser import get_browser


app = QApplication(sys.argv)

class Backend(QObject):
    @pyqtSlot(str, name="handleClicked")
    def handle_clicked(self, output: str):
        print(output)


grid = QGridLayout()

browser = get_browser(grid)

backend = Backend()

channel = QWebChannel(grid)
channel.registerObject("backend", backend)
browser.page().setWebChannel(channel)

button = QPushButton("Click me")


def load_url():
    browser.load(QUrl(url_input.text()))


button.clicked.connect(lambda: load_url())

# create grid layout
url_input = QLineEdit()
# url_input at row 1 column 0 of our grid
grid.addWidget(url_input, 1, 0)
# browser frame at row 2 column 0 of our grid
grid.addWidget(browser, 2, 0)

grid.addWidget(button, 1, 1)

# main app window
main_frame = QWidget()
main_frame.setLayout(grid)
main_frame.show()


app.exec_()
