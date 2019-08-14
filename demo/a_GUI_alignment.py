import sys
from PyQt4 import QtGui, QtCore
import urllib

class myApplication(QtGui.QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        #---- Prepare a Pixmap ----

        url = ('https://www.techtrep.com/assets/uploads/2018/08/python-logo-450w.png')
        self.img = QtGui.QImage()
        self.img.loadFromData(urllib.urlopen(url).read())

        pixmap = QtGui.QPixmap(self.img)

        #---- Embed Pixmap in a QLabel ----

        diag = (pixmap.width()**2 + pixmap.height()**2)**0.5

        self.label = QtGui.QLabel()
        self.label.setMinimumSize(diag, diag)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(pixmap)

        #---- Prepare a Layout ----

        grid = QtGui.QGridLayout()

        button = QtGui.QPushButton('Rotate 15 degrees')
        button.clicked.connect(self.rotate_pixmap)

        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button, 1, 0)

        self.setLayout(grid)

        self.rotation = 0

    def rotate_pixmap(self):

        #---- rotate ----

        # Rotate from initial image to avoid cumulative deformation from
        # transformation

        pixmap = QtGui.QPixmap(self.img)
        self.rotation += 15

        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        #---- update label ----

        self.label.setPixmap(pixmap)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    instance = myApplication()  
    instance.show()    

    sys.exit(app.exec_())