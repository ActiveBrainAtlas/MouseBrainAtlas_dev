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

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')
parser.add_argument("stack", type=str, help="The name of the stack")
args = parser.parse_args()
stack = args.stack

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class init_GUI(QWidget):
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font_header = QFont("Arial",32)
        self.font_sub_header = QFont("Arial",16)
        self.font_left_col = QFont("Arial",16)
        
        self.default_textbox_val = "-"
        
        self.stack = stack
        #self.stain = ""
        #self.stain_2_if_alternating = ""
        #self.planar_res = 0
        #self.section_thickness = 0
        #self.cutting_plane = ""
        
        self.initUI()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body = QGridLayout()
        
        self.setFixedSize(800, 350)
        
        ### Grid TOP (1 row) ###
        # Static Text Field
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setAlignment(Qt.AlignCenter)
        self.e1.setFont( self.font_header )
        self.e1.setReadOnly( True )
        self.e1.setText( "Select File Locations" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
        # Static Text Field
        self.e1 = QTextEdit()
        #self.e1.setValidator( QIntValidator() )
        #self.e1.setAlignment(Qt.AlignCenter)
        self.e1.setFont( self.font_sub_header )
        self.e1.setReadOnly( True )
        self.e1.setText( "You must select your sorted filenames (.txt) file created for "+self.stack+
                        ". This must be a text file formatted as described in the github page.\n"+
                       "Your raw image files must be in either *.jp2 or *.tif format and must all be "+
                       "located inside the same directory. Each filename in the sorted filenames must "+
                       "appear in the filename of a raw image file.")
        #self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 1, 0)
        
        ### Grid BODY (1 row) ###
        # Static Text Field
        self.e2 = QLineEdit()
        self.e2.setValidator( QIntValidator() )
        #self.e2.setMaxLength(50)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont( self.font_left_col )
        self.e2.setReadOnly( True )
        self.e2.setText( "Select sorted_filenames.txt file:" )
        self.e2.setFrame( False )
        self.grid_body.addWidget( self.e2, 0, 0)
        # Static Text Field
        self.e3 = QLineEdit()
        self.e3.setValidator( QIntValidator() )
        #self.e3.setMaxLength(50)
        self.e3.setAlignment(Qt.AlignRight)
        self.e3.setFont( self.font_left_col )
        self.e3.setReadOnly( True )
        self.e3.setText( "Select raw jp2 or tiff files:" )
        self.e3.setFrame( False )
        self.grid_body.addWidget( self.e3, 1, 0)
        
        # Button Text Field
        self.b2 = QPushButton("Select sorted filenames")
        self.b2.setDefault(True)
        self.b2.clicked.connect(lambda:self.buttonPress_selectSFS(self.b2))
        self.b2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.grid_body.addWidget(self.b2, 0, 1)
        # Button Text Field
        self.b3 = QPushButton("Select image files")
        self.b3.setDefault(True)
        self.b3.clicked.connect(lambda:self.buttonPress_selectIMG(self.b3))
        self.b3.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.grid_body.addWidget(self.b3, 1, 1)
        
        # Static Text Field
        self.e7 = QLineEdit()
        self.e7.setValidator( QIntValidator() )
        #self.e7.setMaxLength(50)
        self.e7.setAlignment(Qt.AlignRight)
        self.e7.setFont( self.font_left_col )
        self.e7.setReadOnly( True )
        self.e7.setText( "Push `Submit` when finished" )
        self.e7.setFrame( False )
        self.grid_body.addWidget( self.e7, 6, 0)
        # Button Text Field
        self.b1 = QPushButton("Submit")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.buttonPressSubmit(self.b1))
        self.grid_body.addWidget(self.b1, 6, 1)
        
        #self.grid_top.setColumnStretch(1, 3)
        #self.grid_top.setRowStretch(1, 3)
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_body, 1, 0)
        
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("combo box demo")
        
    def validateEntries(self):
        #entered_stack = str( self.t1.text() )
        
        #if float(entered_resolution) not in self.cutting_planar_resolution_options:
        #    self.e7.setText( 'Resolution not valid' ) 
        #    return False
            
        #self.e7.setText( 'Logging brain metadata!' ) 
        
        return True
        
    def buttonPressSubmit(self, button):
        if button == self.b1:
            validated = self.validateEntries()
            if validated:
                subprocess.call( ['python', 'a_test.py'] )
                close_gui()
                
    def buttonPress_selectSFS(self, button):
        if button == self.b2:
            fp = get_selected_fp( default_filetype=[("text files","*.txt"),("all files","*.*")] )
            validate_sorted_filenames()
            self.e2.setText( fp ) 
                
    def buttonPress_selectIMG(self, button):
        if button == self.b3:
            fp = get_selected_fp( default_filetype=[("tiff files","*.tif"), ("jp2 files","*.jp2"), ("all files","*.*")] )
            #validate_chosen_images()
            self.e3.setText( fp ) 
                
def get_selected_fp( initialdir=os.environ['ROOT_DIR'], default_filetype=("jp2 files","*.jp2") ):
    # Use tkinter to ask user for filepath to jp2 images
    from tkinter import filedialog
    from tkinter import *
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = initialdir,\
                                                title = "Select file",\
                                                filetypes = default_filetype)
    fn = root.filename
    root.destroy()
    return fn
    
def close_gui():
    sys.exit( app.exec_() )
    
def main():
#     app = QApplication(sys.argv)
    app = QApplication( [] )
    
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
