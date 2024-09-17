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
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog, QMenuBar
from PyQt5.QtWidgets import QMenu, QAction, QFileDialog
from dataset import dataset

app = QApplication(sys.argv)

class Backend(QObject):
    @pyqtSlot(str, name="handleClicked")
    def handle_clicked(self, output: str):
        print(output)

    @pyqtSlot(str, str, str, name="handleSelection")
    def handle_selection(self, url: str, label: str, elements: str):
        dataset.add_selection(url, label, json.loads(elements))
        print(f"Selection added for {url}: {label}")

main_layout = QHBoxLayout()
sidebar_layout = QVBoxLayout()
browser_layout = QGridLayout()

browser = get_browser(browser_layout)

backend = Backend()

channel = QWebChannel(browser_layout)
channel.registerObject("backend", backend)
browser.page().setWebChannel(channel)

button = QPushButton("Load")

def load_url():
    browser.load(QUrl(url_input.text()))

button.clicked.connect(lambda: load_url())

def load_dataset():
    filename, _ = QFileDialog.getOpenFileName(main_frame, "Load Dataset", "", "JSON Files (*.json)")
    if filename:
        dataset.load_from_file(filename)
        label_list.clear()
        label_list.addItems(dataset.labels)

def save_dataset():
    filename, _ = QFileDialog.getSaveFileName(main_frame, "Save Dataset", "", "JSON Files (*.json)")
    if filename:
        dataset.save_to_file(filename)

# Create and set up sidebar
url_input = QLineEdit()
label_list = QListWidget()
add_label_button = QPushButton("Add Label")

sidebar_layout.addWidget(label_list)
sidebar_layout.addWidget(add_label_button)

main_layout.addLayout(sidebar_layout)
main_layout.addLayout(browser_layout, 1)

# Modify widget placements
browser_layout.addWidget(url_input, 0, 0)
browser_layout.addWidget(button, 0, 1)
browser_layout.addWidget(browser, 1, 0, 1, 2)

# Add label functionality
def add_label():
    label, ok = QInputDialog.getText(main_frame, "Add Label", "Enter label name:")
    if ok and label:
        label_list.addItem(label)
        dataset.add_label(label)

add_label_button.clicked.connect(add_label)

def set_current_label(item):
    label = item.text()
    browser.page().runJavaScript(f"window.currentLabel = '{label}';")

label_list.itemClicked.connect(set_current_label)

# Update main frame setup
main_frame = QWidget()
main_frame.setLayout(main_layout)
main_frame.setWindowTitle("HTML Labeler")

# Create menubar
menubar = QMenuBar(main_frame)
file_menu = menubar.addMenu('File')

load_action = file_menu.addAction('Load Dataset')
save_action = file_menu.addAction('Save Dataset')

load_action.triggered.connect(load_dataset)
save_action.triggered.connect(save_dataset)

# Update main layout to include menubar
main_layout.setMenuBar(menubar)

main_frame.show()

app.exec_()
