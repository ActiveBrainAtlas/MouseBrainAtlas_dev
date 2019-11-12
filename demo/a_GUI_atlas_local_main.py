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

import argparse

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Atlas Local Fit GUI')
parser.add_argument("stack", type=str, help="stack name")
args = parser.parse_args()
stack = args.stack

class init_GUI(QWidget):
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font1 = QFont("Arial",16)
        self.font2 = QFont("Arial",12)

        # Stack specific info, determined from dropdown menu selection
        self.stack = stack
        self.stain = stack_metadata[stack]['stain']
        self.detector_id = ""
        self.img_version_1 = ""
        self.img_version_2 = ""
        
        self.curr_script_name = ""
        
        self.initUI()

    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_leftCol = QGridLayout()
        self.grid_rightCol = QGridLayout()
        self.grid_textField = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        #self.setFixedSize(1000, 500)
        self.resize(1000, 500)
        
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
        # Static Text Field
        self.e2 = QLineEdit()
        self.e2.setValidator( QIntValidator() )
        self.e2.setMaxLength(6)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont( self.font1 )
        self.e2.setReadOnly( True )
        self.e2.setText( self.stack )
        self.e2.setFrame( False )
        self.grid_top.addWidget( self.e2, 0, 1)
        # Static Text Field
        self.e3 = QLineEdit()
        self.e3.setValidator( QIntValidator() )
        self.e3.setAlignment(Qt.AlignRight)
        self.e3.setFont( self.font1 )
        self.e3.setReadOnly( True )
        self.e3.setText( "Stain:" )
        self.e3.setFrame( False )
        self.grid_top.addWidget( self.e3, 0, 2)
        # Static Text Field
        self.e4 = QLineEdit()
        self.e4.setValidator( QIntValidator() )
        self.e4.setMaxLength(9)
        self.e4.setAlignment(Qt.AlignLeft)
        self.e4.setFont( self.font1 )
        self.e4.setReadOnly( True )
        self.e4.setText( self.stain )
        self.e4.setFrame( False )
        self.grid_top.addWidget( self.e4, 0, 3)
        
        ### Grid Column Left ###
        # Static Text Field
        self.e5 = QLineEdit()
        self.e5.setValidator( QIntValidator() )
        self.e5.setAlignment(Qt.AlignLeft)
        self.e5.setFont( self.font1 )
        self.e5.setReadOnly( True )
        self.e5.setText( "Structure to run:" )
        self.e5.setFrame( False )
        self.grid_leftCol.addWidget( self.e5, 0, 0)
        # Static Text Field
        self.e6 = QLineEdit()
        self.e6.setValidator( QIntValidator() )
        self.e6.setAlignment(Qt.AlignLeft)
        self.e6.setFont( self.font1 )
        self.e6.setReadOnly( True )
        self.e6.setText( "Detector ID number:" )
        self.e6.setFrame( False )
        self.grid_leftCol.addWidget( self.e6, 1, 0)
        # Static Text Field
        self.e7 = QLineEdit()
        self.e7.setValidator( QIntValidator() )
        self.e7.setAlignment(Qt.AlignLeft)
        self.e7.setFont( self.font1 )
        self.e7.setReadOnly( True )
        self.e7.setText( "" )
        self.e7.setFrame( False )
        self.grid_leftCol.addWidget( self.e7, 2, 0)
        
        
        # Dropbown Menu (ComboBox) for selecting Structure
        self.dd1 = QComboBox()
        self.dd1.addItems( ['ALL'] + structures_sided_sorted_by_rostral_caudal_position )
        self.dd1.setFont( self.font1 )
        self.dd1.currentIndexChanged.connect( self.dd1_selection )
        self.dd1.setEnabled(False)
        self.grid_rightCol.addWidget(self.dd1, 0, 0)
        # Dropbown Menu (ComboBox) for selecting Detector ID
        self.dd2 = QComboBox()
        self.dd2.addItems( map(str, detector_settings.to_dict()['comments'].keys()) )
        self.dd2.setFont( self.font1 )
        self.dd2.currentIndexChanged.connect( self.dd2_selection )
        self.dd2.setEnabled(False)
        self.grid_rightCol.addWidget(self.dd2, 1, 0)
        
        ### Grid Bottom ###
        # Button Text Field
        self.bR = QPushButton("Run")
        self.bR.setDefault(True)
        self.bR.clicked.connect(lambda:self.buttonPressRunCommand(self.bR))
        self.grid_bottom.addWidget(self.bR, 0, 1)
        # Button Text Field
        self.bZ = QPushButton("Exit")
        self.bZ.setDefault(True)
        self.bZ.clicked.connect(lambda:self.buttonPressFinished(self.bZ))
        self.grid_bottom.addWidget(self.bZ, 0, 2)

        #self.grid_buttons.setColumnStretch(1, 3)
        #self.grid_buttons.setRowStretch(1, 2)

        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_leftCol, 1, 0)
        self.supergrid.addLayout( self.grid_rightCol, 1, 1)
        self.supergrid.addLayout( self.grid_bottom, 2, 0)

        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("Running Classifiers")

        # Update interactive windows
        self.updateFields()

    def updateFields(self):
        # Get dropdown selection
        selected_structure = str( self.dd1.currentText() )
        selected_detector = int( self.dd2.currentText() )
        #selected_detector = int( self.dd2.toUtf8() )
        print selected_structure
        print selected_detector
        
        # Set stack-specific variables
        #self.stack = dropdown_selection_str
        self.stain = stack_metadata[ self.stack ]['stain']
        self.detector_id = stain_to_metainfo[ self.stain.lower() ]['detector_id']
        self.img_version_1 = stain_to_metainfo[ self.stain.lower() ]['img_version_1']
        self.img_version_2 = stain_to_metainfo[ self.stain.lower() ]['img_version_1']
        
        self.updatePipelineStatus( )

    def updatePipelineStatus(self, initial_setup=False):
        text, script_name = get_text_of_pipeline_status( self.stack, self.stain )
        self.curr_script_name = script_name
                
    def dd1_selection( self ):
        dropdown_selection = self.dd1.currentText()
        dropdown_selection_str = str(dropdown_selection.toUtf8())
        self.updateFields()
        pass
    
    # Called when "Start pipeline from an earlier point" dropdown is used
    def dd2_selection( self ):
        selection_str = self.dd2.currentText()
        self.updateFields()
        pass
    
    def buttonPress(self, button):
        if button == self.bZ:
            close_gui()
            
    def closeEvent(self, event):
        close_gui()

def close_gui():
    sys.exit( app.exec_() )

def main():
    global app 
    app = QApplication( sys.argv )
    
    global ex
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
