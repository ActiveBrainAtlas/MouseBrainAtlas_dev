import os, sys
import subprocess
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
from metadata import *
from data_manager import DataManager
from a_driver_utilities import *

from a_GUI_utilities_pipeline_status import *

import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def format_grid_buttons_initial( button ):
    button.setDefault( True )
    button.setEnabled(True)
    button.setStyleSheet('QPushButton { \
                          background-color: #FDB0B0; \
                          color: black; \
                          border-radius: 15px; \
                          font-size: 26px;}')
    button.setMinimumSize(QSize(150, 150))
    
def format_grid_buttons_completed( button ):
    button.setEnabled(False)
    button.setStyleSheet('QPushButton { \
                          background-color: #868686; \
                          color: black; \
                          border-radius: 15px; \
                          font-size: 26px;}')


class init_GUI(QWidget):
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font1 = QFont("Arial",16)
        self.font2 = QFont("Arial",12)

        # Stack specific info, determined from dropdown menu selection
        self.stack = ""
        self.stain = ""
        self.detector_id = ""
        self.img_version_1 = ""
        self.img_version_2 = ""
        
        self.curr_script_name = ""
        
        self.initial_bottom_text = "Push `Finished` to exit the GUI"

        self.initUI()

    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_buttons = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        self.setFixedSize(1000, 450)

        ### Grid Top (1 row) ###
        # Static Text Field
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setMaxLength(6)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont( self.font1 )
        self.e1.setReadOnly( True )
        self.e1.setText( "Stack:" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
        # Dropbown Menu (ComboBox) for selecting Stack
        self.cb = QComboBox()
        self.cb.addItems( all_stacks )
        self.cb.setFont( self.font1 )
        self.cb.currentIndexChanged.connect( self.updateFields )
        self.grid_top.addWidget(self.cb, 0, 1)
        # Static Text Field
        self.e2 = QLineEdit()
        self.e2.setValidator( QIntValidator() )
        self.e2.setMaxLength(6)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont( self.font1 )
        self.e2.setReadOnly( True )
        self.e2.setText( "Stain:" )
        self.e2.setFrame( False )
        self.grid_top.addWidget( self.e2, 0, 2)
        # Static Text Field
        self.e3 = QLineEdit()
        self.e3.setValidator( QIntValidator() )
        self.e3.setMaxLength(9)
        self.e3.setAlignment(Qt.AlignLeft)
        self.e3.setFont( self.font1 )
        self.e3.setReadOnly( True )
        self.e3.setText( "" )
        self.e3.setFrame( False )
        self.grid_top.addWidget( self.e3, 0, 3)

        ### Grid Buttons ###
        # Button
        self.b_setup = QPushButton("Setup")
        format_grid_buttons_initial( self.b_setup )
        self.b_setup.clicked.connect( lambda:self.button_grid_push(self.b_setup) )
        self.grid_buttons.addWidget( self.b_setup, 0, 0)
        # Button
        self.b_align = QPushButton("Align")
        format_grid_buttons_initial( self.b_align )
        self.b_align.clicked.connect( lambda:self.button_grid_push(self.b_align) )
        self.grid_buttons.addWidget( self.b_align, 0, 1)
        # Button
        self.b_mask = QPushButton("Mask")
        format_grid_buttons_initial( self.b_mask )
        self.b_mask.clicked.connect( lambda:self.button_grid_push(self.b_mask) )
        self.grid_buttons.addWidget( self.b_mask, 0, 2)
        # Button
        self.b_crop = QPushButton("Crop")
        format_grid_buttons_initial( self.b_crop )
        self.b_crop.clicked.connect( lambda:self.button_grid_push(self.b_crop) )
        self.grid_buttons.addWidget( self.b_crop, 1, 0)
        # Button
        self.b_globalFit = QPushButton("Global Atlas Fit")
        format_grid_buttons_initial( self.b_globalFit )
        self.b_globalFit.clicked.connect( lambda:self.button_grid_push(self.b_globalFit) )
        self.grid_buttons.addWidget( self.b_globalFit, 1, 1)
        # Button
        self.b_localFit = QPushButton("Local Atlas Fit")
        format_grid_buttons_initial( self.b_localFit )
        self.b_localFit.clicked.connect( lambda:self.button_grid_push(self.b_localFit) )
        self.grid_buttons.addWidget( self.b_localFit, 1, 2)
        
        ### Grid Bottom ###
        # Button Text Field
        self.b_newBrain = QPushButton("New Brain")
        self.b_newBrain.setDefault(True)
        self.b_newBrain.clicked.connect(lambda:self.button_push(self.b_newBrain))
        self.grid_bottom.addWidget(self.b_newBrain, 0, 1)
        # Button Text Field
        self.b_neuroglancer = QPushButton("Neuroglancer Utilities")
        self.b_neuroglancer.setDefault(True)
        self.b_neuroglancer.clicked.connect(lambda:self.button_push(self.b_neuroglancer))
        self.grid_bottom.addWidget(self.b_neuroglancer, 0, 2)
        # Button Text Field
        self.b_datajoint = QPushButton("Datajoint Utilities")
        self.b_datajoint.setDefault(True)
        self.b_datajoint.clicked.connect(lambda:self.button_push(self.b_datajoint))
        self.grid_bottom.addWidget(self.b_datajoint, 0, 3)
        # Button Text Field
        self.b_exit = QPushButton("Finished")
        self.b_exit.setDefault(True)
        self.b_exit.clicked.connect(lambda:self.button_push(self.b_exit))
        self.grid_bottom.addWidget(self.b_exit, 0, 4)

        #self.grid_buttons.setColumnStretch(1, 3)
        #self.grid_buttons.setRowStretch(1, 2)

        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_buttons, 1, 0)
        self.supergrid.addLayout( self.grid_bottom, 2, 0)

        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("Align to Active Brainstem Atlas - Main Page")

        # Update interactive windows
        self.updateFields()
        
        # Center the GUI
        self.center()
    
    def updateFields(self):
        # Get dropdown selection
        dropdown_selection = self.cb.currentText()
        dropdown_selection_str = str(dropdown_selection.toUtf8())
        
        # Set stack-specific variables
        self.stack = dropdown_selection_str
        self.stain = stack_metadata[ self.stack ]['stain']
        self.detector_id = stain_to_metainfo[ self.stain.lower() ]['detector_id']
        self.img_version_1 = stain_to_metainfo[ self.stain.lower() ]['img_version_1']
        self.img_version_2 = stain_to_metainfo[ self.stain.lower() ]['img_version_1']
        # Update "stain" field to self.stack's stain
        self.e3.setText( self.stain )
        
                
    def button_grid_push(self, button):
        if button == self.b_setup:
            subprocess.call(['python','a_GUI_setup_p1.py'])
        elif button == self.b_align:
            pass
        elif button == self.b_mask:
            pass
        elif button == self.b_crop:
            pass
        elif button == self.b_globalFit:
            pass
        elif button == self.b_localFit:
            pass
            
    def button_push(self, button):
        if button == self.b_exit:
            close_gui()
        elif button == self.b_neuroglancer:
            pass
        elif button == self.b_datajoint:
            pass
        elif button == self.b_newBrain:
            pass
     
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber( QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
            
    def closeEvent(self, event):
        close_main_gui( ex, reopen=False )
        
def main():
    global app 
    app = QApplication( sys.argv )
    
    global ex
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
