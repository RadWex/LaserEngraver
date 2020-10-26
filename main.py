from PyQt5 import QtWidgets
import sys
from centralWidget import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 450)
    window.initialize_3d_widget()
    window.show()
    sys.exit(app.exec_())