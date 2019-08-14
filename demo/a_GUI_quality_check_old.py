#! /usr/bin/env python

import sys, os
import argparse

import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from multiprocess import Pool

sys.path.append( os.path.join(os.environ['REPO_DIR'] , 'utilities') )
sys.path.append( os.path.join(os.environ['REPO_DIR'] , 'gui', 'widgets') )
sys.path.append( os.path.join(os.environ['REPO_DIR'] , 'gui') )

from utilities2015 import *
from metadata import *
from data_manager import *
from registration_utilities import find_contour_points
from gui_utilities import *
from qt_utilities import *
from preprocess_utilities import *
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'web_services'))


def get_img( section, prep_id='None', resol='thumbnail', version='NtbNormalized' ):
    return DataManager.load_image_v2(stack=stack, 
                          section=section, prep_id=prep_id,
                          resol=resol, version=version)

def get_fp( section, prep_id='None', resol='thumbnail', version='NtbNormalized' ):
    return DataManager.get_image_filepath_v2(stack=stack, 
                          section=section, prep_id=prep_id,
                          resol=resol, version=version)

class init_GUI(QWidget):
    
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font_h1 = QFont("Arial",32)
        self.font_p1 = QFont("Arial",16)
        
        self.valid_sections = metadata_cache['valid_sections_all'][stack]
        self.sections_to_filenames = metadata_cache['sections_to_filenames'][stack]
        self.curr_section = self.valid_sections[len(self.valid_sections)/2]
        
        self.i = 10
        
        self.initUI()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        self.setFixedSize(1400, 1000)
        
        ### Grid TOP (1 row) ###
        # Static Text Field
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setAlignment(Qt.AlignCenter)
        self.e1.setFont( self.font_h1 )
        self.e1.setReadOnly( True )
        self.e1.setText( "Select File Locations" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
                
        ### Grid BODY ###
        self.label = QLabel()
        self.loadSection()
        #this.pixmap = QPixmap(fn)
        #this.label.setPixmap( this.pixmap )
        self.grid_body.addWidget( self.label, 0, 0)
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_body, 1, 0)
        self.supergrid.addLayout( self.grid_bottom, 2, 0)
        
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("Q")
        

    def keyPressEvent(self, event):
        key = event.key()
        #print(key)
        
        if key==91: # [
            curr_section_index = self.valid_sections.index( self.curr_section )
            new_section_index = curr_section_index - 1
            if new_section_index<0:
                new_section_index = self.valid_sections[ len(self.valid_sections) ]
            self.curr_section = self.valid_sections[ new_section_index ]
            
            self.loadSection()
            
        elif key==93: # ]
            curr_section_index = self.valid_sections.index( self.curr_section )
            new_section_index = curr_section_index + 1
            if new_section_index>len(self.valid_sections):
                new_section_index = 0
            self.curr_section = self.valid_sections[ new_section_index ]
            
            self.loadSection()
            
        else:
            print(key)
        
    #def mousePressEvent(self, event):
    #    print event.source()
    #    print "clicked"
        
    def wheelEvent(self,event):
        # delta equals plus or minus 1
        delta = event.delta() / 120
        
        self.i += delta
        print self.i
        
        self.pixmap.scaledToWidth( self.i)
        self.label.setPixmap( self.pixmap )
            
    def buttonPress(self, button):
        if button == self.b1:
            close_gui()
            subprocess.call( ['python', 'a_GUI_new_brain_metadata.py'] )
            
    def loadSection( self ):
        fp = get_fp( self.curr_section )
        self.pixmap = QPixmap( fp )
        
        
        
        self.label.setPixmap( self.pixmap )
            
def close_gui():
    ex.hide()
    #sys.exit( app.exec_() )

def main():
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Mask Editing GUI')
    parser.add_argument("stack", type=str, help="stack name")
    args = parser.parse_args()
    global stack
    stack = args.stack
    
    global app 
    app = QApplication( sys.argv )
    
    global ex
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )


if __name__ == '__main__':
    main()
