import subprocess
from a_driver_utilities import *
#sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
#from utilities2015 import *
#from registration_utilities import *
#from annotation_utilities import *
## from metadata import *
from data_manager import DataManager
#from a_driver_utilities import *

from a_bioformats_utilities import *

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from tkinter import *
from tkinter import filedialog

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')
parser.add_argument("stack", type=str, help="The name of the stack")
args = parser.parse_args()
stack = args.stack
    
class init_GUI(QWidget):
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font_header = QFont("Arial",32)
        self.font_1 = QFont("Arial",16)
        
        self.default_textbox_val = ""
        
        self.tiff_destination = DataManager.get_czi_output_filepath_root( stack )
        self.channels_to_extract = []
        # czi_folder ignores the name of the selected czi file
        self.filepath_czi = ""
        self.filepath_czi_folder = ""
        
        self.czi_num_slices = None
        self.czi_num_channels = None
        self.fullres_series_indices = []
        
        self.initUI()
        #self.updateFields()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body_upper = QGridLayout()
        self.grid_body_mid = QGridLayout()
        self.grid_body_lower = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        self.setFixedSize(700, 450)
        
        ### Grid TOP (1 row) ###
        # Static Text Field
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setAlignment(Qt.AlignCenter)
        self.e1.setFont( self.font_header )
        self.e1.setReadOnly( True )
        self.e1.setText( "CZI to TIFF converter" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
        
        ### Grid BODY_UPPER (2 rows) ###
        # Button Text Field
        self.b1 = QPushButton("Select ~a~ CZI file")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.buttonPress(self.b1))
        self.b1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.grid_body_upper.addWidget(self.b1, 0, 0)
        # Checkbox
        self.cb1 = QCheckBox("Convert all CZI files in folder")
        self.cb1.setChecked(True)
        self.cb1.stateChanged.connect(lambda:self.checkboxPress(self.cb1))
        self.grid_body_upper.addWidget(self.cb1, 0, 1)
        # Static Text Field
        self.e4 = QLineEdit()
        self.e4.setValidator( QIntValidator() )
        self.e4.setAlignment(Qt.AlignRight)
        self.e4.setFont( self.font_1 )
        self.e4.setReadOnly( True )
        self.e4.setText( "Lorem Ipsum" )
        self.e4.setFrame( False )
        #self.grid_body_upper.addWidget( self.e4, 1, 1)
        
        ### Grid BODY_MID (X row) ###
        # Static Text Field
        self.t1 = QTextEdit()
        self.t1.setAlignment(Qt.AlignLeft)
        self.t1.setFont( self.font_1 )
        self.t1.setReadOnly( True )
        self.t1.setText( "Please select a czi file and an output folder using the blue buttons above.\n\n\
You can choose to convert just the selected file, or all files in its folder using the top-right checkbox." )
        self.grid_body_mid.addWidget( self.t1, 0, 0)
        
        ### Grid BODY_LOWER (X row) ###
        # Checkbox
        self.cb_c_all = QCheckBox("Convert all channels")
        self.cb_c_all.setChecked(True)
        self.cb_c_all.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_all))
        #self.grid_body_lower.addWidget(self.cb_c_all, 0, 0)
        # Checkbox
        self.cb_c_0 = QCheckBox("Convert channel 0")
        self.cb_c_0.setChecked(False)
        self.cb_c_0.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_0))
        #self.grid_body_lower.addWidget(self.cb_c_0, 1, 0)
        # Checkbox
        self.cb_c_1 = QCheckBox("Convert channel 1")
        self.cb_c_1.setChecked(False)
        self.cb_c_1.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_1))
        #self.grid_body_lower.addWidget(self.cb_c_1, 2, 0)
        # Checkbox
        self.cb_c_2 = QCheckBox("Convert channel 2")
        self.cb_c_2.setChecked(False)
        self.cb_c_2.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_2))
        #self.grid_body_lower.addWidget(self.cb_c_2, 3, 0)
        # Checkbox
        self.cb_c_3 = QCheckBox("Convert channel 3")
        self.cb_c_3.setChecked(False)
        self.cb_c_3.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_3))
        #self.grid_body_lower.addWidget(self.cb_c_3, 3, 0)
        
        
        ### Grid BODY_BOTTOM (X row) ###
        # Button Text Field
        self.b3 = QPushButton("Convert CZI File(s) to TIFF")
        self.b3.setDefault(True)
        self.b3.clicked.connect(lambda:self.buttonPress(self.b3))
        self.b3.setStyleSheet('QPushButton {background-color: #dfbb19; color: black;}')
        self.grid_bottom.addWidget(self.b3, 0, 0)
        
        # Stretch
        #self.grid_body_mid.setColumnStretch(1, 5)
        #self.grid_body_mid.setRowStretch(1, 5)
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_body_upper, 1, 0)
        self.supergrid.addLayout( self.grid_body_mid, 2, 0)
        self.supergrid.addLayout( self.grid_body_lower, 3, 0)
        self.supergrid.addLayout( self.grid_bottom, 4, 0)
        
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("combo box demo")
        
    def display_grid_body_lower(self):
        self.grid_body_lower.addWidget(self.cb_c_all, 0, 0)
        self.grid_body_lower.addWidget(self.cb_c_0, 1, 0)
        if self.czi_num_channels < 2:
            return
        self.grid_body_lower.addWidget(self.cb_c_1, 2, 0)
        if self.czi_num_channels < 3:
            return
        self.grid_body_lower.addWidget(self.cb_c_2, 3, 0)
        if self.czi_num_channels < 4:
            return
        self.grid_body_lower.addWidget(self.cb_c_3, 3, 0)

    def checkboxPress(self, checkbox):
        # "Convert all CZI files in folder"
        if checkbox == self.cb1:
            #print( self.cb1.isChecked() )
            pass
        
        elif checkbox == self.cb_c_all and self.cb_c_all.isChecked():
            for cb_to_disable in [self.cb_c_0, self.cb_c_1, self.cb_c_2, self.cb_c_3]:
                cb_to_disable.setChecked(False)
        
        elif checkbox in [self.cb_c_0, self.cb_c_1, self.cb_c_2, self.cb_c_3] :
            if checkbox.isChecked():
                self.cb_c_all.setChecked(False)
        
    def buttonPress(self, button):
        # Button: "select CZI file"
        if button == self.b1:
            fp = get_selected_file( initialdir='/',
                                   default_filetype=[("all files","*.*"),("czi files","*.czi"),("ndpi files","*.ndpi")] )
            self.filepath_czi = fp
            self.filepath_czi_folder = fp[0:max(loc for loc, val in enumerate(fp) if val == '/')]
            
            # Retrieve relevant metadata of the czi as a dictionary
            metadata_dict = get_czi_metadata( self.filepath_czi )
            # Retrieves indices of proper fullres tissue images
            self.fullres_series_indices = get_fullres_series_indices(metadata_dict)
            
            self.czi_num_slices = len( self.fullres_series_indices )
            self.czi_num_channels = metadata_dict[0]['channels']
            
            display_text = self.filepath_czi.replace(self.filepath_czi_folder, '').replace('/','')+"\n\n"+\
                            "Number of channels: "+str( self.czi_num_channels )+"\n"+\
                            "Detected number of slices: "+str( self.czi_num_slices )
            #self.t1.setText( str(metadata_dict) )
            self.t1.setText( display_text )
            
            self.display_grid_body_lower()
            self.b1.setStyleSheet('QPushButton {background-color: #cacaca; color: black;}')
            
        # Button: "Convert CZI File(s) to TIFF"
        if button == self.b3:
            validated = self.validate_selections()
            if not validated:
                self.t1.setText( "Either selections are incomplete or there is an internal error." )
                return
            else:
                import time
                t = time.time()
                # "convertFiles" will fully extract all specified channels/scenes/czis
                self.convertFiles()
                print('===================================================================')
                print 'Seconds taken to convert to TIFF: '+str(time.time()-t)
                print('===================================================================')
            
    def convertFiles(self):
        
        # If we are converting ALL files in the czi folder
        if self.cb1.isChecked():
            print('\n\n')
            print_stars()
            print('  Converting ALL CZI files in the folder to TIFFs')
            print_stars()
            print('\n')
            
            czi_file_list = get_list_of_czis_in_folder( self.filepath_czi_folder )
            
            for i, czi_file in enumerate(czi_file_list):
                full_czi_fn = os.path.join( self.filepath_czi_folder, czi_file)
                
                print_stars()
                print_stars()
                print('  Extracting czi file '+str(i+1)+' out of '+str(len(czi_file_list)) )
                print_stars()
                print_stars()
                print('\n')
                
                # Retrieve metadata of the czi as a dictionary of relevant values
                metadata_dict = get_czi_metadata( full_czi_fn )
                # Retrieves indices of proper fullres tissue images
                self.fullres_series_indices = get_fullres_series_indices(metadata_dict)
                del metadata_dict
                
                for ii, series_index in enumerate(self.fullres_series_indices):
                    print_stars()
                    print('  Extracting scene: '+str(ii+1)+' out of '+str(len(self.fullres_series_indices)) )
                    print_stars()
                    print('\n')
                    for channel in self.channels_to_extract:
                        print('Extracting channel: '+str(channel) )
                        
                        # Extract file by file, section by section, channel by channel
                        extract_tiff_from_czi( full_czi_fn, self.tiff_destination, series_index, channel )
                        
        # If we are converting ONLY 1 czi file
        else:
            print('\n\n')
            print_stars()
            print('  Converting just the selected CZI into TIFFs')
            print_stars()
            print('\n')
            
            # Each channel of each series takes 2min 7min 
            for series_index in self.fullres_series_indices:
                print_stars()
                print('Converting scene '+str(self.fullres_series_indices.index(series_index))+ \
                      ' out of '+str(len(self.fullres_series_indices)) )
                print_stars()
                print('\n')
                
                for channel in self.channels_to_extract:
                    extract_tiff_from_czi( self.filepath_czi, self.tiff_destination, series_index, channel )
        
    def validate_selections(self):
        # Check that CZI input folder and TIFF output folder are selected
        assert self.tiff_destination != ""
        assert self.filepath_czi != ""
        assert self.filepath_czi_folder != ""
        
        self.channels_to_extract = []
        if self.cb_c_all.isChecked():
            for i, cb in enumerate([self.cb_c_0, self.cb_c_1, self.cb_c_2, self.cb_c_3]):
                self.channels_to_extract.append( i )
                if i==self.czi_num_channels-1:
                    break
        else:
            for i, cb in enumerate([self.cb_c_0, self.cb_c_1, self.cb_c_2, self.cb_c_3]):
                if cb.isChecked():
                    self.channels_to_extract.append( i )
                    
        assert isinstance( self.channels_to_extract, list)
        assert len(self.channels_to_extract) > 0
                    
        return True
    
    def closeEvent(self, event):
        close_main_gui( ex )
        

def get_selected_file( initialdir='/', default_filetype=("jp2 files","*.jp2") ):
    # initialdir=os.environ['ROOT_DIR']
    # Use tkinter to ask user for filepath to jp2 images
    
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir = initialdir,\
                                                title = "Select file",\
                                                filetypes = default_filetype)
    fn = root.filename
    root.destroy()
    return fn

def get_selected_folder( initialdir='/' ):
    # initialdir=os.environ['ROOT_DIR'
    # Use tkinter to ask user for filepath to jp2 images
    
    root = Tk()
    root.filename = filedialog.askdirectory(initialdir = initialdir,\
                                                title = "Select folder")
    fp = root.filename
    root.destroy()
    return fp
                
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
    
    clean_up_tiff_directory2( '/media/alexn/Data_2/czi_convert_test/tiffs/fftest/' )

if __name__ == '__main__':
    main()