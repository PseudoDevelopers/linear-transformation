import numpy as np
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal


class linearTransform(QThread):
    def __init__(self, imgPath):
        super().__init__()
        self.image = np.array(Image.open(imgPath))

    def setBasisMatrix(self, basisMatrix):
        self.basisMatrix = basisMatrix

    linearTransform = pyqtSignal(Image.Image)
    def run(self):
        imageHeight = self.image.shape[1]

        transformedImage = np.full(shape=(600, 500, 4), fill_value=255, dtype=np.uint8)
        transformedImageWidth = transformedImage.shape[0]
        transformedImageHeight = transformedImage.shape[1]

        for rowNo, row in enumerate(self.image):
            rowNo = (imageHeight - 1) - rowNo

            for colNo, pixel in enumerate(row):
                transformedVector = np.matmul(self.basisMatrix, np.array([rowNo, colNo])).astype(int)

                x = (imageHeight - 1) - transformedVector[0]
                y = transformedVector[1]

                if (0 <= x < transformedImageWidth) and (0 <= y < transformedImageHeight):
                    transformedImage[x, y] = np.append(pixel, 255)

        self.linearTransform.emit(Image.fromarray(transformedImage, mode='RGBA'))
