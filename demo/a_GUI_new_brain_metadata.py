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
        self.font_left_col = QFont("Arial",16)
        
        self.default_textbox_val = ""
        
        self.stack = ""
        self.stain = ""
        #self.stain_2_if_alternating = ""
        self.planar_res = 0
        self.section_thickness = 0
        self.cutting_plane = ""
        
        self.stain_options = ['ntb', 'thionin']
        self.cutting_plane_options = ['sagittal', 'horozontal', 'coronal']
        self.cutting_planar_resolution_options = [0.46, 0.325]
        self.section_thickness_options = [20]
        
        self.initUI()
        #self.updateFields()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body = QGridLayout()
        
        self.setFixedSize(900, 350)
        
        ### Grid TOP (1 row) ###
        # Static Text Field
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setAlignment(Qt.AlignCenter)
        self.e1.setFont( self.font_header )
        self.e1.setReadOnly( True )
        self.e1.setText( "Enter Metadata" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
        
        ### Grid BODY (1 row) ###
        # Static Text Field
        self.e2 = QLineEdit()
        self.e2.setValidator( QIntValidator() )
        self.e2.setMaxLength(50)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont( self.font_left_col )
        self.e2.setReadOnly( True )
        self.e2.setText( "Stack name:" )
        self.e2.setFrame( False )
        self.grid_body.addWidget( self.e2, 0, 0)
        # Static Text Field
        self.e3 = QLineEdit()
        self.e3.setValidator( QIntValidator() )
        self.e3.setMaxLength(50)
        self.e3.setAlignment(Qt.AlignRight)
        self.e3.setFont( self.font_left_col )
        self.e3.setReadOnly( True )
        self.e3.setText( "Stain (ntb/thionin):" )
        self.e3.setFrame( False )
        self.grid_body.addWidget( self.e3, 1, 0)
        # Static Text Field
        self.e4 = QLineEdit()
        self.e4.setValidator( QIntValidator() )
        self.e4.setMaxLength(50)
        self.e4.setAlignment(Qt.AlignRight)
        self.e4.setFont( self.font_left_col )
        self.e4.setReadOnly( True )
        self.e4.setText( "Cutting plane (sagittal/horozontal/coronal):" )
        self.e4.setFrame( False )
        self.grid_body.addWidget( self.e4, 2, 0)
        # Static Text Field
        self.e5 = QLineEdit()
        self.e5.setValidator( QIntValidator() )
        self.e5.setMaxLength(50)
        self.e5.setAlignment(Qt.AlignRight)
        self.e5.setFont( self.font_left_col )
        self.e5.setReadOnly( True )
        self.e5.setText( "Slice thickness in um (usually 20):" )
        self.e5.setFrame( False )
        self.grid_body.addWidget( self.e5, 3, 0)
        # Static Text Field
        self.e6 = QLineEdit()
        self.e6.setValidator( QIntValidator() )
        self.e6.setMaxLength(50)
        self.e6.setAlignment(Qt.AlignRight)
        self.e6.setFont( self.font_left_col )
        self.e6.setReadOnly( True )
        self.e6.setText( "Planar resolution in um (0.46/0.325):" )
        self.e6.setFrame( False )
        self.grid_body.addWidget( self.e6, 4, 0)
        
        # Editable Text Field
        self.t1 = QLineEdit()
        self.t1.setMaxLength(50)
        self.t1.setAlignment(Qt.AlignLeft)
        self.t1.setFont( self.font_left_col )
        self.t1.setText( self.default_textbox_val )
        self.t1.setFrame( False )
        self.grid_body.addWidget( self.t1, 0, 1)
        # Editable Text Field
        self.t2 = QLineEdit()
        self.t2.setMaxLength(50)
        self.t2.setAlignment(Qt.AlignLeft)
        self.t2.setFont( self.font_left_col )
        self.t2.setText( self.default_textbox_val )
        self.t2.setFrame( False )
        self.grid_body.addWidget( self.t2, 1, 1)
        # Editable Text Field
        self.t3 = QLineEdit()
        self.t3.setMaxLength(50)
        self.t3.setAlignment(Qt.AlignLeft)
        self.t3.setFont( self.font_left_col )
        self.t3.setText( self.default_textbox_val )
        self.t3.setFrame( False )
        self.grid_body.addWidget( self.t3, 2, 1)
        # Editable Text Field
        self.t4 = QLineEdit()
        self.t4.setMaxLength(50)
        self.t4.setAlignment(Qt.AlignLeft)
        self.t4.setFont( self.font_left_col )
        self.t4.setText( self.default_textbox_val )
        self.t4.setFrame( False )
        self.grid_body.addWidget( self.t4, 3, 1)
        # Editable Text Field
        self.t5 = QLineEdit()
        self.t5.setMaxLength(50)
        self.t5.setAlignment(Qt.AlignLeft)
        self.t5.setFont( self.font_left_col )
        self.t5.setText( self.default_textbox_val )
        self.t5.setFrame( False )
        self.grid_body.addWidget( self.t5, 4, 1)
        
        # Static Text Field
        self.e7 = QLineEdit()
        self.e7.setValidator( QIntValidator() )
        self.e7.setMaxLength(50)
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
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_body, 1, 0)
        
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("combo box demo")
        
        # Update interactive windows
        #self.updateFields()
        
    def validateEntries(self):
        entered_stack = str( self.t1.text() )
        entered_stain = str( self.t2.text() )
        entered_plane = str( self.t3.text() )
        entered_thickness = str( self.t4.text() )
        entered_resolution = str( self.t5.text() )
        
        if self.default_textbox_val!='' and self.default_textbox_val in \
        entered_stack+entered_stain+entered_plane+entered_thickness+entered_resolution:
            self.e7.setText( 'All fields must be filled out' ) 
            return False
        if ' ' in entered_stack+entered_stain+entered_plane+entered_thickness+entered_resolution:
            self.e7.setText( 'There should not be any spaces' ) 
            return False
                
        if not is_number(entered_thickness):
            self.e7.setText( 'Thickness is not a number' ) 
            return False
        if not is_number(entered_resolution):
            self.e7.setText( 'Resolution is not a number' ) 
            return False
            
        if entered_stain.lower() not in self.stain_options:
            self.e7.setText( 'Stain not valid' ) 
            return False
        if entered_plane.lower() not in self.cutting_plane_options:
            self.e7.setText( 'Cutting plane not valid' ) 
            return False
        if float(entered_thickness) not in self.section_thickness_options:
            self.e7.setText( 'Thickness not valid' ) 
            return False
        if float(entered_resolution) not in self.cutting_planar_resolution_options:
            self.e7.setText( 'Resolution not valid' ) 
            return False
            
        self.e7.setText( 'Logging brain metadata!' )
        return True
            
    def buttonPressSubmit(self, button):
        if button == self.b1:
            validated = self.validateEntries()
            if validated:
                entered_stack = str( self.t1.text() )
                entered_stain = str( self.t2.text() ).lower()
                entered_plane = str( self.t3.text() ).lower()
                entered_thickness = float( str( self.t4.text() ) )
                entered_resolution = float( str( self.t5.text() ) )
                
                set_stack_metadata( entered_stack, entered_stain, entered_plane, entered_thickness, entered_resolution )
                
                close_gui()
                subprocess.call( ['python', 'a_GUI_select_file_locations.py', entered_stack] )
                
    
# Records a stack's metadata after it is validated
def set_stack_metadata( stack, stain, plane, thickness, resolution):
    if stain=='ntb':
        stain_capitalized = 'NTB'
    if stain=='thionin':
        stain_capitalized = 'Thionin'
    
    input_dict = {}
    input_dict['DEFAULT'] = {'stack_name': stack, \
                             'cutting_plane': plane,\
                             'planar_resolution_um': resolution,\
                             'section_thickness_um': thickness,\
                             'stain': stain_capitalized,\
                             'stain_2_if_alternating': ""}
    
    fp = os.path.join( os.environ['ROOT_DIR'], 'brains_info', stack+'.ini' )
    try:
        os.makedirs( os.path.join( os.environ['ROOT_DIR'], 'brains_info' ) )
    except:
        pass
    
    save_dict_as_ini( input_dict, fp )
    save_metadata_in_shell_script( stack, stain, plane, thickness, resolution )
    
# Save the STACK.ini file
def save_dict_as_ini( input_dict, fp ):
    import configparser
    assert 'DEFAULT' in input_dict.keys()

    config = configparser.ConfigParser()

    for key in input_dict.keys():
        config[key] = input_dict[key]
        
    with open(fp, 'w') as configfile:
        config.write(configfile)

# Save the brain_metadata.sh file
def save_metadata_in_shell_script( stack, stain, plane, thickness, resolution ):
    fp = os.path.join( os.environ['PROJECT_DIR'], 'setup', 'set_'+stack+'_metadata.sh' )
    
    # Change ntb->NTB and thionin->Thionin
    if stain=='ntb':
        stain='NTB'
        detector_id=799
        img_version_1 = 'NtbNormalized'
        img_version_2 = 'NtbNormalizedAdaptiveInvertedGamma'
    elif stain=='thionin':
        stain='Thionin'
        detector_id=19
        img_version_1 = 'gray'
        img_version_2 = 'gray'
    
    data = 'export stack='+stack+'\n'+\
            'export stain='+stain+'\n'+\
            'export detector_id='+str(detector_id)+'\n'+\
            'export img_version_1='+img_version_1+'\n'+\
            'export img_version_2='+img_version_2+'\n'
            
    with open( fp, 'w' ) as file:
        file.write( data )

def close_gui():
    ex.hide()
    # We manually kill this operation by getting a list of p_ids running this process 
    #  (in case there are multiple hanging instances)
    ps = subprocess.Popen(('ps','aux'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'python a_GUI_initial.py'), stdin=ps.stdout)
    python_GUI_initial_processes = output.split('\n')
    
    for process_str in python_GUI_initial_processes:
        # We are currently running a grep command that we should not kill
        if 'grep' in process_str or process_str == '':
            continue
        # Get the p-id of every a_GUI_initial.py process and kill it in cold blood
        else:
            p_id = process_str.split()[1]
            subprocess.call(['kill','-9',p_id])
            
    print('\n\n***********************')
    print('\n\nGUI closed down successfully!\n\n')
    print('***********************\n\n')
    
    sys.exit( app.exec_() )
    sys.exit()
    
def main():
    global app 
    app = QApplication( sys.argv )
    
    global ex
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
