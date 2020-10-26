import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtWidgets as qWidget
from PyQt5 import QtGui as qGui
from PyQt5 import QtCore as qCore
from PyQt5 import uic, QtOpenGL
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore
import sys
import os
from PIL import Image as Image
import numpy
from os import listdir
from os.path import isfile, join
import os
from PIL import Image as Image
import numpy
import operator
from sceneView import GLWidget
import interface

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open("style.qss", 'r').read())
        self.initialize_menu_bar()
        self.initialize_tool_bar()
        self.setWindowTitle("Laser Engraver")

    def initialize_menu_bar(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        view_menu = menu_bar.addMenu("&View")

    def initialize_tool_bar(self):
        tool_menu = QToolBar()
        self.addToolBar(tool_menu)
        action = QAction("Tak")
        #action.setIcon(QIcon("images/2.png"))
        tool_menu.addAction(action)
        
    def initialize_3d_widget(self):
        ogl = GLWidget()
        self.setCentralWidget(ogl)

class MainWindowInterface(interface.Interface):
    def __init__(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())