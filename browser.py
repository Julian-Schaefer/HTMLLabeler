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

def get_webchannel_source():
    file = QFile(":/qtwebchannel/qwebchannel.js")
    if not file.open(QIODevice.ReadOnly):
        return ""
    content = file.readAll()
    file.close()
    return content.data().decode()

def executeCustomJavaScript(browser):
        browser.page().runJavaScript(
            """             
            window.backend = null;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.backend = channel.objects.backend;
            });

            var selectedElements = [];

            document.body.addEventListener('click', (event) => {
                if (event.target.style.border === "2px solid red") {
                    event.target.style.border = null;
                    selectedElements = selectedElements.filter(el => el !== event.target);
                } else {
                    event.target.style.border = "2px solid red";
                    selectedElements.push(event.target);
                }
                
                if (window.backend) {
                    window.backend.handleSelection(
                        window.location.href,
                        window.currentLabel,
                        JSON.stringify(selectedElements.map(el => el.outerHTML))
                    );
                }

                event.preventDefault();
            });

            document.body.addEventListener('mouseover', function (event) {
                if (event.target.style.border !== "2px solid red") {
                    event.target.style.border = "2px solid black";
                }
            });

            document.body.addEventListener('mouseout', function (event) {
                if (event.target.style.border !== "2px solid red") {
                    event.target.style.border = null;
                }
            });
            """
        )

def get_browser(parent):
    browser = QWebView()
    browser.load(QUrl("http://www.youtube.com"))

    script = QWebEngineScript()
    script.setName("create_connection")
    script.setSourceCode(get_webchannel_source())
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setRunsOnSubFrames(False)
    browser.page().profile().scripts().insert(script)

    # channel = QWebChannel(parent)
    # channel.registerObject("backend", backend)
    # browser.page().setWebChannel(channel)

    browser.page().setAudioMuted(True)
    browser.page().loadFinished.connect(lambda: executeCustomJavaScript(browser))


    return browser
