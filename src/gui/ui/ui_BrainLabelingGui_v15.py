# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/BrainLabelingGui_v15.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BrainLabelingGui(object):
    def setupUi(self, BrainLabelingGui):
        BrainLabelingGui.setObjectName(_fromUtf8("BrainLabelingGui"))
        BrainLabelingGui.resize(2280, 1113)
        self.centralwidget = QtGui.QWidget(BrainLabelingGui)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.main_sagittal_gview = QtGui.QGraphicsView(self.splitter_2)
        self.main_sagittal_gview.setObjectName(_fromUtf8("main_sagittal_gview"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tb_coronal_gview = QtGui.QGraphicsView(self.splitter)
        self.tb_coronal_gview.setObjectName(_fromUtf8("tb_coronal_gview"))
        self.tb_horizontal_gview = QtGui.QGraphicsView(self.splitter)
        self.tb_horizontal_gview.setObjectName(_fromUtf8("tb_horizontal_gview"))
        self.tb_sagittal_gview = QtGui.QGraphicsView(self.splitter)
        self.tb_sagittal_gview.setObjectName(_fromUtf8("tb_sagittal_gview"))
        self.verticalLayout.addWidget(self.splitter_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        self.lineEdit_username = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_username.setObjectName(_fromUtf8("lineEdit_username"))
        self.horizontalLayout.addWidget(self.lineEdit_username)
        self.button_reconstruct = QtGui.QPushButton(self.centralwidget)
        self.button_reconstruct.setObjectName(_fromUtf8("button_reconstruct"))
        self.horizontalLayout.addWidget(self.button_reconstruct)
        self.button_navigateToStructure = QtGui.QPushButton(self.centralwidget)
        self.button_navigateToStructure.setObjectName(_fromUtf8("button_navigateToStructure"))
        self.horizontalLayout.addWidget(self.button_navigateToStructure)
        self.button_displayStructures = QtGui.QPushButton(self.centralwidget)
        self.button_displayStructures.setObjectName(_fromUtf8("button_displayStructures"))
        self.horizontalLayout.addWidget(self.button_displayStructures)
        self.button_inferSide = QtGui.QPushButton(self.centralwidget)
        self.button_inferSide.setObjectName(_fromUtf8("button_inferSide"))
        self.horizontalLayout.addWidget(self.button_inferSide)
        self.button_clearSide = QtGui.QPushButton(self.centralwidget)
        self.button_clearSide.setObjectName(_fromUtf8("button_clearSide"))
        self.horizontalLayout.addWidget(self.button_clearSide)
        self.button_displayOptions = QtGui.QPushButton(self.centralwidget)
        self.button_displayOptions.setObjectName(_fromUtf8("button_displayOptions"))
        self.horizontalLayout.addWidget(self.button_displayOptions)
        self.button_saveHanddrawnStructures = QtGui.QPushButton(self.centralwidget)
        self.button_saveHanddrawnStructures.setObjectName(_fromUtf8("button_saveHanddrawnStructures"))
        self.horizontalLayout.addWidget(self.button_saveHanddrawnStructures)
        self.button_saveStructures = QtGui.QPushButton(self.centralwidget)
        self.button_saveStructures.setObjectName(_fromUtf8("button_saveStructures"))
        self.horizontalLayout.addWidget(self.button_saveStructures)
        self.button_save = QtGui.QPushButton(self.centralwidget)
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.horizontalLayout.addWidget(self.button_save)
        self.button_saveMarkers = QtGui.QPushButton(self.centralwidget)
        self.button_saveMarkers.setObjectName(_fromUtf8("button_saveMarkers"))
        self.horizontalLayout.addWidget(self.button_saveMarkers)
        self.button_loadStructures = QtGui.QPushButton(self.centralwidget)
        self.button_loadStructures.setObjectName(_fromUtf8("button_loadStructures"))
        self.horizontalLayout.addWidget(self.button_loadStructures)
        self.button_loadHanddrawnStructures = QtGui.QPushButton(self.centralwidget)
        self.button_loadHanddrawnStructures.setObjectName(_fromUtf8("button_loadHanddrawnStructures"))
        self.horizontalLayout.addWidget(self.button_loadHanddrawnStructures)
        self.button_loadWarpedAtlas = QtGui.QPushButton(self.centralwidget)
        self.button_loadWarpedAtlas.setObjectName(_fromUtf8("button_loadWarpedAtlas"))
        self.horizontalLayout.addWidget(self.button_loadWarpedAtlas)
        self.button_loadUnwarpedAtlas = QtGui.QPushButton(self.centralwidget)
        self.button_loadUnwarpedAtlas.setObjectName(_fromUtf8("button_loadUnwarpedAtlas"))
        self.horizontalLayout.addWidget(self.button_loadUnwarpedAtlas)
        self.button_load = QtGui.QPushButton(self.centralwidget)
        self.button_load.setObjectName(_fromUtf8("button_load"))
        self.horizontalLayout.addWidget(self.button_load)
        self.button_loadMarkers = QtGui.QPushButton(self.centralwidget)
        self.button_loadMarkers.setObjectName(_fromUtf8("button_loadMarkers"))
        self.horizontalLayout.addWidget(self.button_loadMarkers)
        self.verticalLayout.addLayout(self.horizontalLayout)
        BrainLabelingGui.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(BrainLabelingGui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2280, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        BrainLabelingGui.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(BrainLabelingGui)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        BrainLabelingGui.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(BrainLabelingGui)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        BrainLabelingGui.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(BrainLabelingGui)
        QtCore.QMetaObject.connectSlotsByName(BrainLabelingGui)

    def retranslateUi(self, BrainLabelingGui):
        BrainLabelingGui.setWindowTitle(_translate("BrainLabelingGui", "MainWindow", None))
        self.label_7.setText(_translate("BrainLabelingGui", "Username:", None))
        self.button_reconstruct.setText(_translate("BrainLabelingGui", "3D Reconstruct", None))
        self.button_navigateToStructure.setText(_translate("BrainLabelingGui", "Nagivate To Structure", None))
        self.button_displayStructures.setText(_translate("BrainLabelingGui", "Display Structures", None))
        self.button_inferSide.setText(_translate("BrainLabelingGui", "Infer Side", None))
        self.button_clearSide.setText(_translate("BrainLabelingGui", "Clear Side Assignment", None))
        self.button_displayOptions.setText(_translate("BrainLabelingGui", "Display Options", None))
        self.button_saveHanddrawnStructures.setText(_translate("BrainLabelingGui", "Save Handdrawn Structures", None))
        self.button_saveStructures.setText(_translate("BrainLabelingGui", "Save Atlas Structures", None))
        self.button_save.setText(_translate("BrainLabelingGui", "Save Contours", None))
        self.button_saveMarkers.setText(_translate("BrainLabelingGui", "Save Markers", None))
        self.button_loadStructures.setText(_translate("BrainLabelingGui", "Load Structures", None))
        self.button_loadHanddrawnStructures.setText(_translate("BrainLabelingGui", "Load Handdrawn Structures", None))
        self.button_loadWarpedAtlas.setText(_translate("BrainLabelingGui", "Load Warped Atlas", None))
        self.button_loadUnwarpedAtlas.setText(_translate("BrainLabelingGui", "Load Unwarped Atlas", None))
        self.button_load.setText(_translate("BrainLabelingGui", "Load Contours", None))
        self.button_loadMarkers.setText(_translate("BrainLabelingGui", "Load Markers", None))
        self.toolBar.setWindowTitle(_translate("BrainLabelingGui", "toolBar", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BrainLabelingGui = QtGui.QMainWindow()
    ui = Ui_BrainLabelingGui()
    ui.setupUi(BrainLabelingGui)
    BrainLabelingGui.show()
    sys.exit(app.exec_())

