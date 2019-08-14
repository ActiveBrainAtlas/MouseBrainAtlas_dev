#! /usr/bin/env python

import sys, os
import argparse

#import matplotlib.pyplot as plt
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

#from PyQt4 import QtCore, QtGui

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


class init_GUI(QWidget):
    
    def __init__(self, parent = None):
        super(init_GUI, self).__init__(parent)
        self.font_h1 = QFont("Arial",32)
        self.font_p1 = QFont("Arial",16)
        
        self.valid_sections = metadata_cache['valid_sections_all'][stack]
        self.sections_to_filenames = metadata_cache['sections_to_filenames'][stack]
        self.curr_section = self.valid_sections[ len(self.valid_sections)/2 ]
        self.prev_section = self.getPrevValidSection( self.curr_section )
        self.next_section = self.getNextValidSection( self.curr_section )
        
        self.mode = 'view' 
                
        self.initUI()
        
    def initUI(self):
        # Set Layout and Geometry of Window
        self.grid_top = QGridLayout()
        self.grid_body_upper = QGridLayout()
        self.grid_body = QGridLayout()
        self.grid_bottom = QGridLayout()
        
        self.setFixedSize(1500, 1000)
        
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
        self.e1.setText( "Thumbnail Viewer" )
        self.e1.setFrame( False )
        self.grid_top.addWidget( self.e1, 0, 0)
        
        ### Grid BODY UPPER ###
        # Button Text Field
        self.b1 = QPushButton("Auto-Normalize")
        self.b1.setDefault(True)
        self.b1.clicked.connect(lambda:self.buttonPress(self.b1))
        self.grid_body_upper.addWidget( self.b1, 0, 1)
        # Static Text Field
        self.e4 = QLineEdit()
        self.e4.setAlignment(Qt.AlignCenter)
        self.e4.setFont( self.font_p1 )
        self.e4.setReadOnly( True )
        self.e4.setText( "Filename: " )
        self.e4.setStyleSheet("color: rgb(250,50,50); background-color: rgb(250,250,250);")
        self.grid_body_upper.addWidget( self.e4, 0, 2)
        # Static Text Field
        self.e5 = QLineEdit()
        self.e5.setAlignment(Qt.AlignCenter)
        self.e5.setFont( self.font_p1 )
        self.e5.setReadOnly( True )
        self.e5.setText( "Section: " )
        self.e5.setStyleSheet("color: rgb(250,50,50); background-color: rgb(250,250,250);")
        self.grid_body_upper.addWidget( self.e5, 0, 3)
                
        ### Grid BODY ###
        # Custom VIEWER
        self.grid_body.addWidget( self.viewer, 0, 0)
        
        ### Grid BOTTOM ###
        # Checkbox
        self.cb_1 = QCheckBox("Good Section")
        self.cb_1.setChecked(True)
        self.cb_1.stateChanged.connect(lambda:self.checkboxPress(self.cb_1))
        self.grid_bottom.addWidget(self.cb_1, 0, 0)
        # Checkbox
        self.cb_2 = QCheckBox("Blurry Section")
        self.cb_2.setChecked(False)
        self.cb_2.stateChanged.connect(lambda:self.checkboxPress(self.cb_2))
        self.grid_bottom.addWidget(self.cb_2, 0, 1)
        # Checkbox
        self.cb_3 = QCheckBox("Warped/Destroyed Section")
        self.cb_3.setChecked(False)
        self.cb_3.stateChanged.connect(lambda:self.checkboxPress(self.cb_3))
        self.grid_bottom.addWidget(self.cb_3, 0, 2)
        
        self.grid_body_upper.setColumnStretch(0, 2)
        self.grid_body_upper.setColumnStretch(2, 2)
        
        ### SUPERGRID ###
        self.supergrid = QGridLayout()
        self.supergrid.addLayout( self.grid_top, 0, 0)
        self.supergrid.addLayout( self.grid_body_upper, 1, 0)
        self.supergrid.addLayout( self.grid_body, 2, 0)
        #self.supergrid.addLayout( self.grid_bottom, 3, 0)
        
        # Set layout and window title
        self.setLayout( self.supergrid )
        self.setWindowTitle("Q")
        
        # Loads self.curr_section as the current image and sets all fields appropriatly
        self.setCurrSection( self.curr_section )
        
        #time.sleep(2)
        #self.keyPressEvent(91)
        
    def loadImage(self):
        # Get filepath of "curr_section" and set it as viewer's photo
        fp = get_fp( self.curr_section )
        self.viewer.setPhoto( QPixmap( fp ) )
        
    def loadImageThenNormalize(self):
        # Get filepath of "curr_section" and set it as viewer's photo
        fp = get_fp( self.curr_section )
        img = cv2.imread(fp) * 3
        
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        
        self.viewer.setPhoto( QPixmap( qImg ) )
        
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
        #print(key)
        
        if key==91: # [
            self.setCurrSection( self.getPrevValidSection( self.curr_section ) )
            
        elif key==93: # ]
            self.setCurrSection( self.getNextValidSection( self.curr_section ) )
            
        elif key==81: # Q
            self.pixInfo()
            
        elif key==77: # M
            self.toggleMode()
            
        else:
            print(key)
            
    def setCurrSection(self, section=-1):
        """
        Sets the current section to the section passed in.
        
        Will automatically update curr_section, prev_section, and next_section.
        Updates the header fields and loads the current section image.
        
        """
        # Update curr, prev, and next section
        self.curr_section = section
        self.prev_section = self.getPrevValidSection( self.curr_section )
        self.next_section = self.getNextValidSection( self.curr_section )
        # Update the section and filename at the top
        self.updateCurrHeaderFields()
            
        self.loadImage()
        
    def toggleMode(self):
        if self.mode=='view':
            self.mode = 'align'
        elif self.mode=='align':
            self.mode = 'view'
        self.setCurrSection()
            
    def buttonPress(self, button):
        if button == self.b1:
            self.loadImageThenNormalize()
        
    def checkboxPress(self, checkbox):
        if checkbox.isChecked():
            if checkbox == self.cb_1:
                self.cb_2.setChecked(False)
                self.cb_3.setChecked(False)
            elif checkbox == self.cb_2:
                self.cb_1.setChecked(False)
                self.cb_3.setChecked(False)
            elif checkbox == self.cb_3:
                self.cb_2.setChecked(False)
                self.cb_1.setChecked(False)
                
        elif not checkbox.isChecked():
            #checkbox.setChecked(True)
            pass
        
        
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
        #self.e2.setText( "Filename: "+str(self.sections_to_filenames[self.curr_section]) )
        #self.e3.setText( "Section: "+str(self.curr_section) )
        self.e4.setText( str(self.sections_to_filenames[self.curr_section]) )
        self.e5.setText( str(self.curr_section) )
        
        
                    
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
    # Simulate a user's keypress because otherwise the autozoom is weird
    ex.keyPressEvent(91)
    
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
