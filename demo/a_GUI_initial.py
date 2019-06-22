import subprocess
#from a_driver_utilities import *
#sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
#from utilities2015 import *
#from registration_utilities import *
#from annotation_utilities import *
## from metadata import *
#from data_manager import DataManager
#from a_driver_utilities import *

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class init_GUI(QWidget):
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.button_font = QFont("Arial",26)
        
        self.initUI()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid1 = QGridLayout()
        self.setFixedSize(900, 400)
        
        ### Grid 1 (1 row) ###
        # Button
        self.b1 = QPushButton("Setup a new brain")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.buttonPress_b1(self.b1))
        self.b1.setMinimumSize(QSize(300, 250))
        self.b1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font-size: 36px;}')
        self.grid1.addWidget(self.b1, 0, 0)
        # Button
        self.b2 = QPushButton("Continue running a brain")
        self.b2.setDefault(True)
        self.b2.clicked.connect(lambda:self.buttonPress_b2(self.b2))
        self.b2.setMinimumSize(QSize(300, 250))
        self.b2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font-size: 36px;}')
        self.grid1.addWidget(self.b2, 0, 1)
        
        # Set layout and window title
        self.setLayout( self.grid1 )
        self.setWindowTitle("combo box demo")
            
    def buttonPress_b1(self, button):
        if button == self.b1:
            #print "clicked button is "+button.text()
            subprocess.call( ['python', 'a_GUI_new_brain_metadata.py'] )
            close_gui()
            
    def buttonPress_b2(self, button):
        if button == self.b2:
            #print "clicked button is "+button.text()
            subprocess.call( ['python', 'a_test.py'] )
            close_gui()
            
def close_gui():
    sys.exit( app.exec_() )
            

def main():
#     app = QApplication(sys.argv)
    app = QApplication( [] )
    
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )

app = None
if __name__ == '__main__':
    main()
