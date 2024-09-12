from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt5.QtCore import Qt, pyqtSlot, QObject, QFile, QIODevice
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView as QWebView,
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineScript,
)
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import *


def get_browser(parent):
    browser = QWebView()
    browser.load(QUrl("http://google.com"))

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
                alert('Connected to backend');
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

    def get_webchannel_source():
        file = QFile(":/qtwebchannel/qwebchannel.js")
        if not file.open(QIODevice.ReadOnly):
            return ""
        content = file.readAll()
        file.close()
        return content.data().decode()

    backend = Backend()

    channel = QWebChannel(parent)
    channel.registerObject("backend", backend)
    browser.page().setWebChannel(channel)

    script = QWebEngineScript()
    script.setName("create_connection")
    script.setSourceCode(get_webchannel_source())
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setRunsOnSubFrames(False)
    browser.page().profile().scripts().insert(script)

    browser.page().setAudioMuted(True)
    browser.page().loadFinished.connect(executeCustomJavaScript)

    return browser
