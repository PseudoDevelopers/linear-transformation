import sys

import numpy as np
from PIL import ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from linear_transform import linearTransform
from main_window import Ui_MainWindow


IMAGE_PATH = 'image.jpg'


class MyApp:
    def __init__(self):
        # Initializing the GUI
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self.transform = linearTransform(IMAGE_PATH)
        self.basisVectorChanged()
        self.setEventForSliders()

        self.updateBasisVectors_lbl(self.getBasisMatrix())
        self.ui.image_lbl.setText('Image is loading...')

        MainWindow.show()
        sys.exit(app.exec_())

    def basisVectorChanged(self):
        basisMatrix = self.getBasisMatrix()
        self.updateBasisVectors_lbl(basisMatrix)

        if self.transform.isRunning():
            self.transform.terminate()

        self.transform.setBasisMatrix(basisMatrix)
        self.transform.linearTransform.connect(self.updateImage)
        self.transform.start()


    def updateImage(self, image):
        QtImg = ImageQt.ImageQt(image)
        self.ui.image_lbl.setPixmap(QtGui.QPixmap.fromImage(QtImg))

    def getBasisMatrix(self):
        V1 = [ self.ui.firstVector_i_slider.value()/100, self.ui.firstVector_j_slider.value()/100 ]
        V2 = [ self.ui.secondVector_i_slider.value()/100, self.ui.secondVector_j_slider.value()/100 ]

        return np.array([V1, V2])

    def updateBasisVectors_lbl(self, basisMatrix):
        V1 = basisMatrix[0]
        V2 = basisMatrix[1]

        self.ui.firstUnitVector_value_lbl.setText(f'({V1[0]} î, {V1[1]} ĵ)')
        self.ui.secondUnitVector_value_lbl.setText(f'({V2[0]} î, {V2[1]} ĵ)')

    def setEventForSliders(self):
        """
        Set events for slider value change
        """
        self.ui.firstVector_i_slider.valueChanged.connect(self.basisVectorChanged)
        self.ui.firstVector_j_slider.valueChanged.connect(self.basisVectorChanged)
        self.ui.secondVector_i_slider.valueChanged.connect(self.basisVectorChanged)
        self.ui.secondVector_j_slider.valueChanged.connect(self.basisVectorChanged)


if __name__ == "__main__":
    MyApp()
