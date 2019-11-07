import subprocess
from a_driver_utilities import *
#sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
#from utilities2015 import *
#from registration_utilities import *
#from annotation_utilities import *
## from metadata import *
from data_manager_v2 import DataManager
#from a_driver_utilities import *

from a_bioformats_utilities import *

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Tkinter import *
#from Tkinter import *
#from Tkinter import filedialog

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
        
        self.metadata_dict = {}
        self.main_channel = 0
        
        self.initUI()
        #self.updateFields()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body_upper = QGridLayout()
        self.grid_body_mid = QGridLayout()
        self.grid_body_lower = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        #self.setFixedSize(700, 500)
        self.resize(700, 500)
        
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
        self.b1 = QPushButton("Select a CZI file")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.buttonPress(self.b1))
        self.b1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.grid_body_upper.addWidget(self.b1, 0, 0)
        # Checkbox
        self.cb1 = QCheckBox("Convert all CZI files in folder")
        self.cb1.setChecked(True)
        self.cb1.stateChanged.connect(lambda:self.checkboxPress(self.cb1))
        self.grid_body_upper.addWidget(self.cb1, 0, 1)
        # Button Text Field
        self.b2 = QPushButton("Select \"Sorted Filenames\" TXT file (Optional)")
        self.b2.setDefault(True)
        self.b2.clicked.connect(lambda:self.buttonPress(self.b2))
        self.b2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.grid_body_upper.addWidget(self.b2, 1, 0)
        
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
        
        # Static Text Field
        self.e5 = QLineEdit()
        self.e5.setValidator( QIntValidator() )
        self.e5.setAlignment(Qt.AlignLeft)
        self.e5.setFont( QFont("Arial",12) )
        self.e5.setReadOnly( True )
        self.e5.setText( "Select the main channel (the nissl/nuclear stain):" )
        self.e5.setFrame( False )
        #self.grid_body_lower.addWidget( self.e5, 0, 1)
        # Checkbox
        self.cb_c_0_main = QCheckBox("Channel 0 is Main")
        self.cb_c_0_main.setChecked(False)
        self.cb_c_0_main.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_0_main))
        #self.grid_body_lower.addWidget(self.cb_c_0_main, 1, 1)
        # Checkbox
        self.cb_c_1_main = QCheckBox("Channel 1 is Main")
        self.cb_c_1_main.setChecked(False)
        self.cb_c_1_main.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_1_main))
        #self.grid_body_lower.addWidget(self.cb_c_1_main, 2, 1)
        # Checkbox
        self.cb_c_2_main = QCheckBox("Channel 2 is Main")
        self.cb_c_2_main.setChecked(False)
        self.cb_c_2_main.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_2_main))
        #self.grid_body_lower.addWidget(self.cb_c_2_main, 3, 1)
        # Checkbox
        self.cb_c_3_main = QCheckBox("Channel 3 is Main")
        self.cb_c_3_main.setChecked(False)
        self.cb_c_3_main.stateChanged.connect(lambda:self.checkboxPress(self.cb_c_3_main))
        #self.grid_body_lower.addWidget(self.cb_c_3_main, 3, 1)
        
        
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
        self.setWindowTitle("Extract tiffs using bioformats tools")
        
    def display_grid_body_lower(self):
        # Add left column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_all, 0, 0)
        self.grid_body_lower.addWidget(self.cb_c_0, 1, 0)
        # Add right column checkboxes
        self.grid_body_lower.addWidget( self.e5, 0, 1)
        self.grid_body_lower.addWidget(self.cb_c_0_main, 1, 1)
        self.cb_c_0_main.setText( self.metadata_dict['channel_0_name']+' (channel 0)' )
        self.cb_c_0_main.setChecked(True)
        
        if self.czi_num_channels < 2:
            return
        # Add left column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_1, 2, 0)
        # Add right column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_1_main, 2, 1)
        self.cb_c_1_main.setText( self.metadata_dict['channel_1_name']+' (channel 1)' )
        
        if self.czi_num_channels < 3:
            return
        # Add left column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_2, 3, 0)
        # Add right column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_2_main, 3, 1)
        self.cb_c_2_main.setText( self.metadata_dict['channel_2_name']+' (channel 2)' )
        
        if self.czi_num_channels < 4:
            return
        # Add left column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_3, 4, 0)
        # Add right column checkboxes
        self.grid_body_lower.addWidget(self.cb_c_3_main, 4, 1)
        self.cb_c_3_main.setText( self.metadata_dict['channel_3_name']+' (channel 3)' )

    def checkboxPress(self, checkbox):
        # "Convert all CZI files in folder"
        if checkbox == self.cb1:
            #print( self.cb1.isChecked() )
            pass
        # If "Convert all channels" is selected, remove all other selections
        elif checkbox == self.cb_c_all and self.cb_c_all.isChecked():
            for cb_to_disable in [self.cb_c_0, self.cb_c_1, self.cb_c_2, self.cb_c_3]:
                cb_to_disable.setChecked(False)
        # If A single channel is selected, deselect the "Convert all channels" option
        elif checkbox in [self.cb_c_0, self.cb_c_1, self.cb_c_2, self.cb_c_3] :
            if checkbox.isChecked():
                self.cb_c_all.setChecked(False)
                
        # For selecting the "main" channel, disable all other options when one is selected
        cbox_list = [self.cb_c_0_main, self.cb_c_1_main, self.cb_c_2_main, self.cb_c_3_main]
        if checkbox in cbox_list:
            if checkbox.isChecked():
                for cbox_to_disable in cbox_list:
                    # If the checkbox we're cycling through is the selected checkbox, ignore
                    if checkbox==cbox_to_disable: # Don't disable the active checkbox
                        # Set the "main_channel" equal to the selected checkbox
                        if checkbox==self.cb_c_0_main:
                            self.main_channel = 0
                        if checkbox==self.cb_c_1_main:
                            self.main_channel = 1
                        if checkbox==self.cb_c_2_main:
                            self.main_channel = 2
                        if checkbox==self.cb_c_3_main:
                            self.main_channel = 3
                        continue

                    if cbox_to_disable.isChecked():
                        cbox_to_disable.setChecked(False)
            else:
                pass
                #checkbox.setChecked(True)
        
    def buttonPress(self, button):
        # Button: "select CZI file"
        if button == self.b1:
            fp = get_selected_file( initialdir='/',
                                   default_filetype=[("all files","*.*"),("czi files","*.czi"),("ndpi files","*.ndpi")] )
            self.filepath_czi = fp
            self.filepath_czi_folder = fp[0:max(loc for loc, val in enumerate(fp) if val == '/')]
            
            # Retrieve relevant metadata of the czi as a dictionary
            metadata_dict = get_czi_metadata( self.filepath_czi )
            self.metadata_dict = metadata_dict.copy()
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
            
        # Button: "select TXT Sorted Filenames file"
        if button == self.b2:
            fp = get_selected_file( initialdir='/',
                                   default_filetype=[("text files","*.txt"),("all files","*.*")] )
            destination_fp = DataManager.get_sorted_filenames_filename(stack)
            
            # Create destination folder if does not exist
            destination_folder = os.path.split( destination_fp )[0]
            try:
                if not os.path.exists( destination_folder ):
                    os.makedirs( destination_folder )
            except:
                pass
            
            subprocess.call(['cp', fp, destination_fp])
            #set_step_completed_in_progress_ini( stack, '1-4_setup_sorted_filenames')
            
            
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
            print(czi_file_list)
            
            for i, czi_file in enumerate(czi_file_list):
                full_czi_fn = os.path.join( self.filepath_czi_folder, czi_file)
                
                print_stars()
                print_stars()
                print('  Extracting czi file '+str(i+1)+' out of '+str(len(czi_file_list)) )
                print_stars()
                print_stars()
                #print('\n')
                
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
                        print('\nExtracting channel: '+str(channel) )
                        
                        # Extract file by file, section by section, channel by channel
                        extract_tiff_from_czi( full_czi_fn, self.tiff_destination, series_index, channel )
                        if ii==0 and channel==0:
                            extract_tiff_from_czi( full_czi_fn, self.tiff_destination, series_index, channel )
            # Copy all files into the proper location
            copy_extracted_tiffs_to_proper_locations( stack, self.tiff_destination, self.main_channel )
            self.finished()
                
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
        #assert self.filepath_czi != ""
        assert self.filepath_czi_folder != "", "No CZI file selected!"
        
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
        #close_main_gui( ex )
        sys.exit( app.exec_() )
        
    def finished(self):
        set_step_completed_in_progress_ini( stack, '1-2_setup_images')
        
        #subprocess.call( ['python', 'a_script_preprocess_setup.py', stack, 'unknown'] )
        
        #close_main_gui( ex )
        sys.exit( app.exec_() )
        

def get_selected_file( initialdir='/', default_filetype=("jp2 files","*.jp2") ):
    # initialdir=os.environ['ROOT_DIR']
    # Use tkinter to ask user for filepath to jp2 images
    import tkFileDialog as filedialog
    
    if ON_DOCKER:
        initialdir = '/mnt/computer_root/'
    
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
    import tkFileDialog as filedialog
    
    if ON_DOCKER:
        initialdir = '/mnt/computer_root/'
    
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
    
    #clean_up_tiff_directory2( '/media/alexn/Data_2/czi_convert_test/tiffs/fftest/' )

if __name__ == '__main__':
    main()