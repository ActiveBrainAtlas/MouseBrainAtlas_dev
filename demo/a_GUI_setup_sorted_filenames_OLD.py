#! /usr/bin/env python

import sys, os
import argparse
import math

#import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from multiprocess import Pool

sys.path.append( os.path.join(os.environ['REPO_DIR'] , 'utilities') )
sys.path.append( os.path.join(os.environ['REPO_DIR'] , 'gui', 'widgets') )
sys.path.append( os.path.join(os.environ['REPO_DIR'] , 'gui') )

from utilities2015 import *
from metadata import *
from data_manager_v2 import *
from registration_utilities import find_contour_points
from gui_utilities import *
from qt_utilities import *
from preprocess_utilities import *
from a_driver_utilities import *
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'web_services'))

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Mask Editing GUI')
parser.add_argument("stack", type=str, help="stack name")
args = parser.parse_args()
stack = args.stack

# Check if a sorted_filenames already exists
sfns_fp = DataManager.get_sorted_filenames_filename( stack=stack )
sfns_already_exists = os.path.exists(sfns_fp)


# Defining possible quality options for each slice
quality_options = ['unusable', 'blurry', 'good']

# Cannot assume we have the sorted_filenames file. Load images a different way
thumbnail_folder = DataManager.setup_get_thumbnail_fp(stack)
#section_to_fn = {}
valid_sections = []
fn_to_data = {}
for i, img_name in enumerate(os.listdir( thumbnail_folder )):
    #section_to_fn[i] = img_name
    fn_to_data[img_name] = {
        'section': i,
        'quality': 'good'}
    valid_sections.append(i)

def section_to_fn(section):
    for fn in fn_to_data.keys():
        if section == int(fn_to_data[fn]['section']):
            return fn
        
def get_grayscale_thumbnail_img( section ):
    fn = section_to_fn( int(section) )
    img_fp = os.path.join( DataManager.setup_get_thumbnail_fp(stack), fn)
    img = cv2.imread(img_fp, -1)
    img = img_as_ubyte(rgb2gray(img))
    return img

class ImageViewer( QGraphicsView):
    photoClicked = pyqtSignal( QPoint )

    def __init__(self, parent):
        super(ImageViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor( QGraphicsView.AnchorUnderMouse )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setBackgroundBrush( QBrush( QColor(30, 30, 30) ))
        self.setFrameShape( QFrame.NoFrame )

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect( QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0
        else:
            print 'RECT IS NULL'

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode( QGraphicsView.ScrollHandDrag )
            self._photo.setPixmap( pixmap )
        else:
            self._empty = True
            self.setDragMode( QGraphicsView.NoDrag )
            self._photo.setPixmap( QPixmap() )
        self.fitInView()
        
    def paintOverlayImage(self, pixmap=None):
        painter = QPainter()
        painter.begin(image)
        painter.drawImage(0, 0, overlay)
        painter.end()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.delta() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode( QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode( QGraphicsView.ScrollHandDrag )

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit( QPoint(event.pos()) )
        super(ImageViewer, self).mousePressEvent(event)
        
class QHLine(QFrame):
    def __init__(self):
        # https://doc.qt.io/qt-5/qframe.html
        # https://stackoverflow.com/questions/5671354/how-to-programmatically-make-a-horizontal-line-in-qt
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(5)
        
class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(5)
        
class init_GUI(QWidget):
    
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font_h1 = QFont("Arial",32)
        self.font_p1 = QFont("Arial",16)
        
        #self.valid_sections = metadata_cache['valid_sections_all'][stack]
        self.valid_sections = valid_sections
        #self.sections_to_filenames = metadata_cache['sections_to_filenames'][stack]
        self.sections_to_filenames = section_to_fn
        self.curr_section = self.valid_sections[ len(self.valid_sections)/2 ]
        self.prev_section = self.getPrevValidSection( self.curr_section )
        self.next_section = self.getNextValidSection( self.curr_section )
                
        self.initUI()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body_upper = QGridLayout()
        self.grid_body = QGridLayout()
        self.grid_body_lower = QGridLayout()
        self.grid_bottom = QGridLayout()
        self.grid_blank = QGridLayout()
        
        self.setFixedSize(1600, 1100)
        
        ### VIEWER ### (Grid Body)
        self.viewer = ImageViewer(self)
        self.viewer.photoClicked.connect( self.photoClicked )
        
        ### Grid TOP ###
        # Static Text Field (Title)
        self.e1 = QLineEdit()
        self.e1.setValidator( QIntValidator() )
        self.e1.setAlignment(Qt.AlignCenter)
        self.e1.setFont( self.font_h1 )
        self.e1.setReadOnly( True )
        self.e1.setText( "Setup Sorted Filenames" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
        # Button Text Field
        self.b_help = QPushButton("HELP")
        self.b_help.setDefault(True)
        self.b_help.setEnabled(True)
        self.b_help.clicked.connect(lambda:self.help_button_press(self.b_help))
        self.b_help.setStyleSheet("color: rgb(0,0,0); background-color: rgb(250,250,250);")
        self.grid_top.addWidget(self.b_help, 0, 1)
        
        ### Grid BODY UPPER ###
        # Static Text Field
        self.e4 = QLineEdit()
        self.e4.setAlignment(Qt.AlignCenter)
        self.e4.setFont( self.font_p1 )
        self.e4.setReadOnly( True )
        self.e4.setText( "Filename: " )
        #self.e4.setStyleSheet("color: rgb(250,50,50); background-color: rgb(250,250,250);")
        self.grid_body_upper.addWidget( self.e4, 0, 2)
        # Static Text Field
        self.e5 = QLineEdit()
        self.e5.setAlignment(Qt.AlignCenter)
        self.e5.setFont( self.font_p1 )
        self.e5.setReadOnly( True )
        self.e5.setText( "Section: " )
        #self.e5.setStyleSheet("color: rgb(250,50,50); background-color: rgb(250,250,250);")
        self.grid_body_upper.addWidget( self.e5, 0, 3)
                
        ### Grid BODY ###
        # Custom VIEWER
        self.grid_body.addWidget( self.viewer, 0, 0)
        
        ### Grid BODY LOWER ###
        # Static Text Field
        self.e7 = QLineEdit()
        self.e7.setMaximumWidth(250)
        self.e7.setAlignment(Qt.AlignRight)
        self.e7.setReadOnly( True )
        self.e7.setText( "Select section quality:" )
        self.grid_body_lower.addWidget( self.e7, 0, 0)
        # Vertical line
        self.grid_body_lower.addWidget(QVLine(), 0, 1, 1, 1)
        
        # Checkbox
        self.cb_good = QCheckBox("Good Quality")
        self.cb_good.setMaximumWidth(140)
        self.cb_good.setChecked(False)
        #self.cb_good.setStyleSheet("border: 2px solid black;")
        #self.grid_body_lower.addWidget(self.cb_good, 0, 2)
        # Checkbox
        self.cb_blurry = QCheckBox("Intact + Blurry")
        self.cb_blurry.setMaximumWidth(150)
        self.cb_blurry.setChecked(False)
        #self.grid_body_lower.addWidget(self.cb_blurry, 0, 3)
        # Checkbox
        self.cb_unusable = QCheckBox("Unuseably Blurry/Torn")
        self.cb_unusable.setMaximumWidth(190)
        self.cb_unusable.setChecked(False)
        #self.grid_body_lower.addWidget(self.cb_unusable, 0, 4)
        
        # Dropbown Menu (ComboBox) for selecting Stack
        self.cb = QComboBox()
        self.cb.addItems( quality_options )
        self.grid_body_lower.addWidget( self.cb, 0, 2)
        
        # Vertical line
        self.grid_body_lower.addWidget(QVLine(), 0, 5, 1, 1)
        # Button Text Field
        self.b_left = QPushButton("<--   Move Section Left   <--")
        self.b_left.setDefault(True)
        self.b_left.setEnabled(True)
        self.b_left.clicked.connect(lambda:self.buttonPress(self.b_left))
        self.b_left.setStyleSheet("color: rgb(0,0,0); background-color: rgb(200,250,250);")
        self.grid_body_lower.addWidget(self.b_left, 0, 6)
        # Button Text Field
        self.b_right = QPushButton("-->   Move Section Right   -->")
        self.b_right.setDefault(True)
        self.b_right.setEnabled(True)
        self.b_right.clicked.connect(lambda:self.buttonPress(self.b_right))
        self.b_right.setStyleSheet("color: rgb(0,0,0); background-color: rgb(200,250,250);")
        self.grid_body_lower.addWidget(self.b_right, 0, 7)
        # Horozontal Line
        self.grid_body_lower.addWidget(QHLine(), 1, 0, 1, 8)
        # Button Text Field
        self.b_done = QPushButton("Finished")
        self.b_done.setDefault(True)
        self.b_done.setEnabled(True)
        self.b_done.clicked.connect(lambda:self.buttonPress(self.b_done))
        self.b_done.setStyleSheet("color: rgb(0,0,0); background-color: #dfbb19;")
        self.grid_body_lower.addWidget(self.b_done, 2, 7)
        
        ### GRID BOTOM ###
        
        
        # Grid stretching
        #self.grid_body_upper.setColumnStretch(0, 2)
        self.grid_body_upper.setColumnStretch(2, 2)
        #self.grid_body_lower.setColumnStretch(3, 1)
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_body_upper, 1, 0)
        self.supergrid.addLayout( self.grid_body, 2, 0)
        #self.supergrid.addLayout( self.grid_body_lower, 4, 0)
        self.supergrid.addWidget(QHLine(), 6, 0, 1, 2)
        #self.supergrid.addLayout( self.grid_bottom, 6, 0)
        self.supergrid.addLayout( self.grid_body_lower, 7, 0)
        self.supergrid.addWidget(QHLine(), 8, 0, 1, 2)
                
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("Q")
        
        self.update_fields()
        
        # Loads self.curr_section as the current image and sets all fields appropriatly
        #self.setCurrSection( self.curr_section )
        
        
        
    def help_button_press(self, button):
        info_text = "This GUI is used to align slices to each other. The shortcut commands are as follows: \n\n\
    -  `[`: Go back one section. \n\
    -  `]`: Go forward one section."
        
        QMessageBox.information( self, "Empty Field",
                    info_text)
        
    def update_fields(self):
        self.setCurrSection( self.curr_section )
        pass
    
    def load_sorted_filenames(self):
        self.valid_sections = metadata_cache['valid_sections_all'][stack]
        self.sections_to_filenames = metadata_cache['sections_to_filenames'][stack]
        self.curr_section = self.valid_sections[ len(self.valid_sections)/2 ]
        self.prev_section = self.getPrevValidSection( self.curr_section )
        self.next_section = self.getNextValidSection( self.curr_section )
        
    def loadImage(self):
        # Get filepath of "curr_section" and set it as viewer's photo
        fn = section_to_fn( int(self.curr_section) )
        img_fp = os.path.join( DataManager.setup_get_thumbnail_fp(stack), fn)
        self.viewer.setPhoto( QPixmap( img_fp ) )
        
    def photoClicked(self, pos):
        if self.viewer.dragMode() == QGraphicsView.NoDrag:
            print('%d, %d' % (pos.x(), pos.y()))
            
    def pixInfo(self):
        self.viewer.toggleDragMode()
        
    def keyPressEvent(self, event):
        try:
            key = event.key()
        except AttributeError:
            key = event
        
        if key==91: # [
            self.setCurrSection( self.getPrevValidSection( self.curr_section ) )
        elif key==93: # ]
            self.setCurrSection( self.getNextValidSection( self.curr_section ) )            
        else:
            print(key)
            
    def setCurrSection(self, section=-1):
        """
        Sets the current section to the section passed in.
        
        Will automatically update curr_section, prev_section, and next_section.
        Updates the header fields and loads the current section image.
        
        """
        if section==-1:
            section = self.curr_section
        
        # Update curr, prev, and next section
        self.curr_section = section
        self.prev_section = self.getPrevValidSection( self.curr_section )
        self.next_section = self.getNextValidSection( self.curr_section )
        # Update the section and filename at the top
        self.updateCurrHeaderFields()
                    
        self.loadImage()
            
    def buttonPress(self, button):
        # Brighten an image
        if button in [self.b1, self.b2, self.b3]:
            # Check whether to apply transform to ALL images according to checkbox value
            if self.cb_1.isChecked():
                only_on_current_img = False
            else:
                only_on_current_img = True
            
            # "Flip image(s) across central vertical line"
            if button==self.b1:
                self.transform_images( 'flip', 
                                               only_on_current_img=only_on_current_img)
            # "Flop image(s) across central horozontal line"
            elif button==self.b2:
                self.transform_images( 'flop', 
                                               only_on_current_img=only_on_current_img)
            # "Rotate Image(s)"
            elif button==self.b3:
                self.transform_images( 'rotate', 
                                               degrees=str(self.cb.currentText()), 
                                               only_on_current_img=only_on_current_img)
            # Update the Viewer info and displayed image
            self.setCurrSection(self.curr_section)
        elif button == self.b_done:
            #QMessageBox.about(self, "Popup Message", "Done.")
            
            self.finished()
        
    def getNextValidSection(self, section):
        section_index = self.valid_sections.index( section )
        next_section_index = section_index + 1
        if next_section_index > len(self.valid_sections)-1:
            next_section_index = 0
        next_section = self.valid_sections[ next_section_index ]
        return next_section
    
    def getPrevValidSection(self, section):
        section_index = self.valid_sections.index( section )
        prev_section_index = section_index - 1
        if prev_section_index < 0:
            prev_section_index = len(self.valid_sections)-1
        prev_section = self.valid_sections[ prev_section_index ]
        return prev_section
        
    def updateCurrHeaderFields(self):
        #self.e4.setText( str(self.sections_to_filenames[self.curr_section]) )
        self.e5.setText( str(self.curr_section) )
                
    def finished(self):
        set_step_completed_in_progress_ini( stack, '1-5_setup_orientations')
        
        #close_main_gui( ex )
        sys.exit( app.exec_() )
            
def close_gui():
    #ex.hide()
    sys.exit( app.exec_() )

def main():
    global app 
    app = QApplication( sys.argv )
    
    global ex
    ex = init_GUI()

    if sfns_already_exists:
        msgBox = QMessageBox()
        text = 'Sorted_filenames already exists, Do you want to load it?\n\n'
        text += 'Warning: If you select no, it will be overwritten!'
        msgBox.setText( text )
        msgBox.addButton( QPushButton('Cancel'), QMessageBox.RejectRole)
        msgBox.addButton( QPushButton('No'), QMessageBox.NoRole)
        msgBox.addButton( QPushButton('Yes'), QMessageBox.YesRole)
        ret = msgBox.exec_()
        # Cancel
        if ret==0:
            #sys.exit( app.exec_() )
            return None
        # No
        elif ret==1:
            ex.show()
        # Yes
        elif ret==2:
            ex.load_sorted_filenames()
            ex.show()
            #Simulate a user's keypress because otherwise the autozoom is weird
            ex.keyPressEvent(91)
            sys.exit( app.exec_() )
    # If sorted_filenames does NOT exist, we must make a new one
    else:
        ex.show()
        # Simulate a user's keypress because otherwise the autozoom is weird
        ex.keyPressEvent(91)
        sys.exit( app.exec_() )

if __name__ == '__main__':
    main()