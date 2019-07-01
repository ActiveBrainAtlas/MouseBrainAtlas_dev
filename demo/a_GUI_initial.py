import subprocess
#from a_driver_utilities import *
#sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
#from utilities2015 import *
#from registration_utilities import *
#from annotation_utilities import *
## from metadata import *
#from data_manager import DataManager
#from a_driver_utilities import *
subprocess.call( ['which', 'python'] )
import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    assert( os.environ['ROOT_DIR']!=None )
    assert( os.environ['REPO_DIR']!=None )
except KeyError:
    print('Please set up the virtual environment and try running this again')
    sys.exit()

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
            close_gui()
            subprocess.call( ['python', 'a_GUI_new_brain_metadata.py'] )
            
    def buttonPress_b2(self, button):
        if button == self.b2:
            close_gui()
            subprocess.call( ['python', 'a_GUI_continue_brain.py'] )
            
def close_gui():
    ex.hide()
    #sys.exit( app.exec_() )

def main():
    global app 
    app = QApplication( sys.argv )
    
    global ex
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )


if __name__ == '__main__':
    main()
