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


app = QApplication(sys.argv)


def get_webchannel_source():
    file = QFile(":/qtwebchannel/qwebchannel.js")
    if not file.open(QIODevice.ReadOnly):
        return ""
    content = file.readAll()
    file.close()
    return content.data().decode()


class Backend(QObject):
    @pyqtSlot(str, name="handleClicked")
    def handle_clicked(self, output: str):
        print(output)


def executeCustomJavaScript():
    browser.page().runJavaScript(
        """       
        window.backend = null;
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.backend = channel.objects.backend;
        });

        var firstElement = null;
        var secondElement = null;

        document.body.addEventListener('click', (event) => {
                if (event.target.style.border != null && event.target.style.border == "2px solid red") {
                    event.target.style.border = null;
                    if (firstElement == event.target) {
                        firstElement = null;
                    }
                    else if (secondElement == event.target) {
                        secondElement = null;
                    }
                } else {
                    if (firstElement != null && secondElement != null) {
                        firstElement.style.border = null;
                        firstElement = event.target;
                    } else if (firstElement == null) {
                        firstElement = event.target;
                    } else if (secondElement == null) {
                        secondElement = event.target;
                    }

                    event.target.style.border = "2px solid red";
                }
                window.backend.handleClicked('hallo');

                event.preventDefault();
            });

        document.body.addEventListener('mouseover',
            function (event) {
                if (event.target.style.border != null && (event.target.style.border == "2px solid red"
                    || event.target.style.border == "2px solid green")) {
                    return;
                }

                event.target.style.border = "2px solid black";
            });

        document.body.addEventListener('mouseout',
            function (event) {
                if (event.target.style.border != null && (event.target.style.border == "2px solid red"
                    || event.target.style.border == "2px solid green")) {
                    return;
                }

                event.target.style.border = null;
            });

        window.addEventListener('beforeunload', (event) => {
            event.preventDefault();
            event.returnValue = '';
            });
        """
    )


grid = QGridLayout()

browser = QWebView()
browser.load(QUrl("http://www.youtube.com"))


backend = Backend()

script = QWebEngineScript()
script.setName("create_connection")
script.setSourceCode(get_webchannel_source())
script.setInjectionPoint(QWebEngineScript.DocumentReady)
script.setWorldId(QWebEngineScript.MainWorld)
script.setRunsOnSubFrames(False)
browser.page().profile().scripts().insert(script)

channel = QWebChannel(grid)
channel.registerObject("backend", backend)
browser.page().setWebChannel(channel)

browser.page().setAudioMuted(True)
browser.page().loadFinished.connect(executeCustomJavaScript)

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
