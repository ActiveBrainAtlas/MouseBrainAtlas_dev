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

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

necessary_image_files_by_script_ntb = {}

necessary_image_files_by_script_ntb['a_script_preprocess_0_setup'] = {'image_set_1': {'prep_id':'None', 'version':'None', 'resol':'raw'}}

necessary_image_files_by_script_ntb['a_script_preprocess_1'] = {'image_set_1': {'prep_id':'None', 'version':'Ntb', 'resol':'raw'},
                                              'image_set_2': {'prep_id':'None', 'version':'Ntb', 'resol':'thumbnail'},
                                              'image_set_3': {'prep_id':'None', 'version':'NtbNormalized', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_2'] = {'image_set_1': {'prep_id':1, 'version':'NtbNormalized', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_3'] = {'image_set_1': 'autoSubmasks'}

necessary_image_files_by_script_ntb['a_script_preprocess_4'] = {'image_set_1': {'prep_id':'None', 'version':'mask', 'resol':'thumbnail'},
                                                               'image_set_2': 'floatHistogram',
                                                               'image_set_3': {'prep_id':'None', 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'raw'}}

necessary_image_files_by_script_ntb['a_script_preprocess_5'] = {'image_set_1': {'prep_id':5, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'raw'},
                                                               'image_set_2': {'prep_id':5, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_6'] = {'image_set_1': {'prep_id':2, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'raw'},
                                                               'image_set_2': {'prep_id':2, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'thumbnail'},
                                                               'image_set_3': {'prep_id':2, 'version':'mask', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_7'] = {'output_file_1': 'atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol',
                                                               'output_file_2': 'registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners'}

def all_img_files_valid( stack, prep_id='None', version='Ntb', resol='thumbnail' ):
    all_files_valid = True
    corrupted_files = []
    
    filenames_list = DataManager.load_sorted_filenames(stack)[0].keys()
    for img_name in filenames_list:
        img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=img_name)
        
        try:
            img = cv2.imread(img_fp)
            # If length of the image size is zero, it's corrupted
            if len(np.shape(img))==0:
                all_files_valid = False
                corrupted_files.append(img_name)
                continue
        except Exception as e:
            all_files_valid = False
            print(e)
            corrupted_files.append(img_name)
            
    return all_files_valid, corrupted_files

def all_img_files_present( stack, prep_id='None', version='Ntb', resol='thumbnail' ):
    all_files_present = True
    missing_files = []
    
    filenames_list = DataManager.load_sorted_filenames(stack)[0].keys()
    for img_name in filenames_list:
        img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=img_name)
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_name)
            
    return all_files_present, missing_files

def all_autoSubmasks_present( stack ):
    all_files_present = True
    missing_files = []
    for fn in metadata_cache['filenames_to_sections'][stack].keys():
        sec = metadata_cache['filenames_to_sections'][stack][fn]
        img_fp = DataManager.get_auto_submask_filepath(stack=stack, what='submask', submask_ind=0, 
                                                      fn=fn, sec=sec)
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_fp)
    return all_files_present, missing_files

def all_adaptive_intensity_floatHistograms_present( stack ):
    all_files_present = True
    missing_files = []
    for fn in metadata_cache['filenames_to_sections'][stack].keys():
        sec = metadata_cache['filenames_to_sections'][stack][fn]
        img_fp = DataManager.get_intensity_normalization_result_filepath(what='float_histogram_png', stack=stack, 
                                                                         fn=fn, section=sec)
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_fp)
    return all_files_present, missing_files

def get_text_of_pipeline_status( stack, stain ):
    text = ""
    all_correct = True
    
    for script_name in sorted(necessary_image_files_by_script_ntb.keys()):
        
        for image_set in necessary_image_files_by_script_ntb[script_name].keys():
            
            contents = necessary_image_files_by_script_ntb[script_name][image_set]
            if type(contents)==str:
                if contents=='autoSubmasks':
                    all_files_present, missing_files = all_autoSubmasks_present( stack )
                elif contents=='floatHistogram':
                    all_files_present, missing_files = all_adaptive_intensity_floatHistograms_present( stack )
            else:
                prep_id = contents['prep_id']
                version = contents['version']
                resol = contents['resol']
                if version=='None':
                    version = None
                all_files_present, missing_files = all_img_files_present( \
                                         stack, prep_id=prep_id, version=version, resol=resol )
                
            if all_files_present:
                #text += script_name + " " + image_set + " has been run successfully!\n"
                pass
            else:
                num_missing_files = len(missing_files)
                num_total_files = len(DataManager.load_sorted_filenames(stack)[0].keys())
                if num_missing_files == num_total_files:
                    text += "NO FILES HAVE FINISHED"
                
                for fn in missing_files[0]:
                    img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=fn)
                    img_root_fp = img_fp[0:img_fp.rfind('/')+1]
                #text += "\n"+script_name + " " + image_set + " is missing files:\n\n"
                text += "\n" + script_name + " did not run properly and has missing files:\n"
                text += "(" + str(num_missing_files) + " missing out of "+str(num_total_files)+")\n\n"
                text += "`" + img_root_fp + "` is the image directory in which there are the following missing files:\n\n"
                missing_files.sort()
                for fn in missing_files:
                    img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=fn)
                    text += fn+"\n"
                all_correct = False
                break
        if not all_correct:
            break
        elif all_correct:
            text += script_name + " has been run successfully!\n"
                    
    return text

class init_GUI(QWidget):
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font1 = QFont("Arial",16)
        self.font2 = QFont("Arial",12)
        
        self.stack = ""
        self.stain = ""
        
        self.initUI()
        self.updateFields()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        #layout = QHBoxLayout()
        self.grid1 = QGridLayout()
        self.grid2 = QGridLayout()
        #self.setGeometry(50, 50, 300, 300)
        #self.setFixedSize(500, 400)
        self.setFixedSize(900, 400)
        
        ### Grid 1 (1 row) ###
        # Static Text Field
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setMaxLength(6)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont( self.font1 )
        self.e1.setReadOnly( True )
        self.e1.setText( "Stack:" )
        self.e1.setFrame( False )
        self.grid1.addWidget( self.e1, 0, 0)
        # Dropbown Menu (ComboBox) for selecting Stack
        self.cb = QComboBox()
        self.cb.addItems( all_stacks )
        self.cb.setFont( self.font1 )
        self.cb.currentIndexChanged.connect( self.dropdownSelect )
        self.grid1.addWidget(self.cb, 0, 1)
        # Static Text Field
        self.e2 = QLineEdit()
        self.e2.setValidator( QIntValidator() )
        self.e2.setMaxLength(6)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont( self.font1 )
        self.e2.setReadOnly( True )
        self.e2.setText( "Stain:" )
        self.e2.setFrame( False )
        self.grid1.addWidget( self.e2, 0, 2)
        # Static Text Field
        self.e3 = QLineEdit()
        self.e3.setValidator( QIntValidator() )
        self.e3.setMaxLength(9)
        self.e3.setAlignment(Qt.AlignLeft)
        self.e3.setFont( self.font1 )
        self.e3.setReadOnly( True )
        self.e3.setText( "" )
        self.e3.setFrame( False )
        self.grid1.addWidget( self.e3, 0, 3)
        
        ### Grid 2 ###
        # Button
        self.b1 = QPushButton("Check pipeline status")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.buttonPress(self.b1))
        self.grid2.addWidget(self.b1, 0, 0)
        # Static Text Field
        self.e4 = QTextEdit()
        #self.e4.setValidator( QIntValidator() )
        #self.e4.setMaxLength(1000)
        self.e4.setAlignment(Qt.AlignLeft)
        self.e4.setFont( self.font2 )
        self.e4.setReadOnly( True )
        self.e4.setText( "" )
        #self.e4.setFrame( False )
        self.grid2.addWidget( self.e4, 1, 1)
        
        
        self.grid2.setColumnStretch(1, 3)
        self.grid2.setRowStretch(1, 2)
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid1, 0, 0)
        self.supergrid.addLayout( self.grid2, 1, 0)
        
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("combo box demo")
        
        # Update interactive windows
        self.updateFields()

    def dropdownSelect(self,i):
        #print "Items in the list are :"

        for count in range(self.cb.count()):
            selection = self.cb.currentText()
            selection_str = str(selection.toUtf8())
            #print type(selection)
            #print self.cb.itemText(count)
            #print "Current index",i,"selection changed ",selection_str
            self.stack = selection_str
            
            self.updateStainField( selection_str )
            
    def updateFields(self):
        self.updateStainField( str(self.cb.currentText().toUtf8()) )
        self.dropdownSelect(0)
        
    def updateStainField(self, stack):
        stain_from_stack = stack_metadata[stack]['stain']
        self.stain = stain_from_stack
        self.e3.setText( stain_from_stack )
        
    def updatePipelineStatusField(self):
        text = get_text_of_pipeline_status( self.stack, self.stain )
        
        self.e4.setText( text )
            
    def buttonPress(self, button):
        if button == self.b1:
            self.updatePipelineStatusField()
            #print "clicked button is "+button.text()
            

def main():
#     app = QApplication(sys.argv)
    app = QApplication( [] )
    
    ex = init_GUI()
    ex.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
