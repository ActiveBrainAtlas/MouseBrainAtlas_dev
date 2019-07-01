import os
import subprocess
from a_driver_utilities import *
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
# from metadata import *
from data_manager import DataManager
from a_driver_utilities import *

from a_GUI_utilities_pipeline_status import *

import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        # set to "script" to display command to run the next script
        # set to "manual" to display manual user step preceding next command
        self.curr_script_or_manual_step = "manual"
        
        self.initial_bottom_text = "Push `Finished` to exit the GUI"

        self.initUI()

    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_buttons = QGridLayout()
        self.grid_dropdowns = QGridLayout()
        self.grid_textField = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        self.setFixedSize(1000, 500)

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
        self.b1 = QPushButton("Check pipeline status")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.button_grid_push(self.b1))
        self.grid_buttons.addWidget(self.b1, 0, 0)
        # Button
        self.b2 = QPushButton("Prepare to run the next script")
        self.b2.setDefault(True)
        self.b2.clicked.connect(lambda:self.button_grid_push(self.b2))
        self.grid_buttons.addWidget(self.b2, 0, 1)
        # Button
        self.b3 = QPushButton("Where are my files?")
        self.b3.setDefault(True)
        self.b3.clicked.connect(lambda:self.button_grid_push(self.b3))
        self.grid_buttons.addWidget(self.b3, 0, 2)
        
        ### Grid Dropdowns ###
        # Dropbown Menu (ComboBox) for selecting Stack
        self.dd1 = QComboBox()
        self.dd1.addItems( ['Manual user step (1)','Script (2)'] )
        self.dd1.setFont( self.font1 )
        self.dd1.currentIndexChanged.connect( self.dd1_selection )
        self.dd1.setEnabled(False)
        self.grid_dropdowns.addWidget(self.dd1, 0, 1)
        # Dropbown Menu (ComboBox) for selecting Stack
        self.dd2 = QComboBox()
        self.dd2.addItems( ['Run next script', 'script 1...'] )
        self.dd2.setFont( self.font1 )
        self.dd2.currentIndexChanged.connect( self.dd2_selection )
        self.dd2.setEnabled(False)
        self.grid_dropdowns.addWidget(self.dd2, 0, 2)
        # Dropbown Menu (ComboBox) for selecting Stack
        self.dd3 = QComboBox()
        self.dd3.addItems( ['all structures']+all_known_structures_sided )
        self.dd3.setFont( self.font1 )
        self.dd3.currentIndexChanged.connect( self.dd3_selection )
        self.dd3.setEnabled(False)
        self.grid_dropdowns.addWidget(self.dd3, 0, 3)
        # Dropbown Menu (ComboBox) for selecting Stack
        self.dd4 = QComboBox()
        self.dd4.addItems( ['Best detector', 'Detector 15 (Thionin)', 'Detector 19 (Thionin)', 
                            'Detector 799 (NTB)', 'Detector 998 (normalized_-1_5)', 'Detector 999 (normalized_-1_5)'] )
        self.dd4.setFont( self.font1 )
        self.dd4.currentIndexChanged.connect( self.dd4_selection )
        self.dd4.setEnabled(False)
        self.grid_dropdowns.addWidget(self.dd4, 0, 4)
        
        ### Grid Text Field ###
        # Static Text Field
        self.e4 = QTextEdit()
        self.e4.setAlignment(Qt.AlignLeft)
        self.e4.setFont( self.font2 )
        self.e4.setReadOnly( True )
        self.e4.setText( "" )
        self.grid_textField.addWidget( self.e4, 1, 1)
        
        ### Grid Bottom ###
        # Static Text Field
        self.e5 = QLineEdit()
        self.e5.setValidator( QIntValidator() )
        #self.e7.setMaxLength(50)
        self.e5.setAlignment(Qt.AlignRight)
        self.e5.setFont( self.font2 )
        self.e5.setReadOnly( True )
        self.e5.setText( self.initial_bottom_text )
        self.e5.setFrame( False )
        self.grid_bottom.addWidget( self.e5, 0, 0)
        # Button Text Field
        self.bR = QPushButton("Run")
        self.bR.setDefault(True)
        self.bR.clicked.connect(lambda:self.buttonPressRunCommand(self.bR))
        self.grid_bottom.addWidget(self.bR, 0, 1)
        # Button Text Field
        self.bZ = QPushButton("Finished")
        self.bZ.setDefault(True)
        self.bZ.clicked.connect(lambda:self.buttonPressFinished(self.bZ))
        self.grid_bottom.addWidget(self.bZ, 0, 2)

        #self.grid_buttons.setColumnStretch(1, 3)
        #self.grid_buttons.setRowStretch(1, 2)

        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_buttons, 1, 0)
        self.supergrid.addLayout( self.grid_dropdowns, 2, 0)
        self.supergrid.addLayout( self.grid_textField, 3, 0)
        self.supergrid.addLayout( self.grid_bottom, 4, 0)

        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("Atlas Pipeline GUI")

        # Update interactive windows
        self.updateFields()
        self.update_large_text_field( "Please choose the stack you would like to run, "+
                                         "and select an option from above." )

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
        
        # Update "stain" field
        self.e3.setText( self.stain )
        
        self.e5.setText( self.initial_bottom_text )
        self.e5.setReadOnly( True )
        
        self.updatePipelineStatusField( )
        self.toggle_scriptRunningMode( False )

    def updatePipelineStatusField(self, initial_setup=False):
        text, script_name = get_text_of_pipeline_status( self.stack, self.stain )
        self.curr_script_name = script_name
        
        self.update_large_text_field( text )
        
    def button_grid_push(self, button):
        if button == self.b1:
            self.updatePipelineStatusField()
            self.toggle_scriptRunningMode( False )
        if button == self.b2: # "prepare to run next script"
            self.update_large_text_field( "** RUN THE MANUAL STEP **\n\n"+
                 "Use the dropdown menu on the top left to choose whether to display the manual user "+
                 "step command, or whether to display the command to run the script. The order is ALWAYS: manual step "+
                 "followed by script. \n\nIf the manual step is in parenthesis then there is no python command to run. "+
                 "The third preprocessing script has two commands to run for the manual user step, you must remove "+
                 "all extraneous characters.\n\n\n"+
                 "** RUN THE SCRIPT **\n\n"+
                 "Please verify that you have successfully completed the manual step required for "+
                 "this script or you will encounter an error. This may require opening a new terminal "+
                 "window to run an additional command for the time being.\n\n"+
                 "If the command below has a dollarsign (`$`) preceding any variable, then it must be "+
                 "manually entered by you according to the pipeline intructions on Github.")
            self.toggle_scriptRunningMode( True )
        if button == self.b3:
            self.update_large_text_field( "** YOUR ROOT DIRECTORY **\n\n"+os.environ['ROOT_DIR']+"\n\n"+
                            "As you run the pipeline, various files will be generated and organized "+
                            "according to a strict file management system. You should not delete any files "+
                            "inside of your ROOT_DIR while you are still running the pipeline.\n\n"+
                            "** WHERE IMAGES ARE LOCATED **\n\n"+
                            os.path.join(os.environ['ROOT_DIR'],'CSHL_data_processed',self.stack)+"/\n\n"
                            "The preprocessing pipeline (all scripts with \"preprocessing\" in the name) "+
                            "will generate a variety of image files that use a file naming scheme as described here: \n"+
                            "https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/doc/Filename_Breakdown.md" )
            self.toggle_scriptRunningMode( False )
            
    def toggle_scriptRunningMode(self, turn_on):
        if turn_on:
            script_command = get_script_command( self.curr_script_name, self.stack, self.stain, str(self.detector_id),
                                              self.curr_script_or_manual_step )
            self.e5.setText( script_command )
            self.e5.setReadOnly( False )
            self.e5.setStyleSheet('QLineEdit {background-color: #f0f8fc; border: 1px solid black;}')
            
            self.bR.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
            self.bR.setEnabled(True)
            
            self.dd1.setEnabled(True)
        else:
            self.e5.setText( self.initial_bottom_text )
            self.e5.setReadOnly( True )
            self.e5.setStyleSheet('QLineEdit {background-color: #FFFFFF;}')
            
            self.bR.setStyleSheet('QPushButton {background-color: #444444; color: black;}')
            self.bR.setEnabled(False)
            
            self.dd1.setEnabled(False)
            
    def buttonPressRunCommand(self, button):
        if button == self.bR:
            self.update_large_text_field( "Running the script, output will be displayed on the Terminal." )
            command = str( self.e5.text() )
            if command == self.initial_bottom_text:
                return None
            else:
                if '$' in command:
                    self.update_large_text_field( "\'$\' symbol has been detected in the command. All variables with "+
                                    "this symbol prepended to their name should be replaced with the proper "+
                                    "value as described on the Github." )
                    return
                else:
                    pass
                
                try:
                    start_time_gui_script = time.time()
                    subprocess.call( command.split() )
                    end_time_gui_script = time.time()
                    text = "Script has finished! Took "+str(round(float(end_time_gui_script-start_time_gui_script)/60.0,1))+" minutes"
                    self.update_large_text_field( text )

                except Exception as e:
                    self.update_large_text_field( str(e) )
                
    def dd1_selection( self ):
        dropdown_selection = self.dd1.currentText()
        dropdown_selection_str = str(dropdown_selection.toUtf8())
                
        if dropdown_selection_str=='Manual user step (1)':
            self.curr_script_or_manual_step = "manual"
            print self.curr_script_or_manual_step
        elif dropdown_selection_str=='Script (2)':
            self.curr_script_or_manual_step = "script"
            print self.curr_script_or_manual_step
        else:
            sys.exit()
            
        self.toggle_scriptRunningMode( True )
    
    def dd2_selection( self ):
        pass
    
    def dd3_selection( self ):
        pass
    
    def dd4_selection( self ):
        pass
            
    def update_large_text_field(self, text):
        self.e4.setText( text )
        self.e4.repaint()
    
    def buttonPressFinished(self, button):
        if button == self.bZ:
            close_gui()
            
    def closeEvent(self, event):
        close_gui()

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
