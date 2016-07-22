# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './HomographyGUI.ui'
#
# Created: Tue Dec  1 16:56:09 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sourceGraph = QtGui.QGraphicsView(self.centralwidget)
        self.sourceGraph.setGeometry(QtCore.QRect(10, 40, 381, 281))
        self.sourceGraph.setObjectName("sourceGraph")
        self.targetGraph = QtGui.QGraphicsView(self.centralwidget)
        self.targetGraph.setGeometry(QtCore.QRect(410, 40, 381, 281))
        self.targetGraph.setObjectName("targetGraph")
        self.sourceButton = QtGui.QPushButton(self.centralwidget)
        self.sourceButton.setGeometry(QtCore.QRect(10, 10, 131, 27))
        self.sourceButton.setObjectName("sourceButton")
        self.targetButton = QtGui.QPushButton(self.centralwidget)
        self.targetButton.setGeometry(QtCore.QRect(410, 10, 131, 27))
        self.targetButton.setObjectName("targetButton")
        self.acquireButton = QtGui.QPushButton(self.centralwidget)
        self.acquireButton.setGeometry(QtCore.QRect(411, 330, 131, 27))
        self.acquireButton.setCheckable(True)
        self.acquireButton.setObjectName("acquireButton")
        self.transformButton = QtGui.QPushButton(self.centralwidget)
        self.transformButton.setGeometry(QtCore.QRect(411, 471, 121, 27))
        self.transformButton.setObjectName("transformButton")
        self.resetButton = QtGui.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(539, 471, 121, 27))
        self.resetButton.setObjectName("resetButton")
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(668, 471, 121, 27))
        self.saveButton.setObjectName("saveButton")
        self.point1Edit = QtGui.QLineEdit(self.centralwidget)
        self.point1Edit.setGeometry(QtCore.QRect(551, 331, 116, 27))
        self.point1Edit.setReadOnly(True)
        self.point1Edit.setObjectName("point1Edit")
        self.point2Edit = QtGui.QLineEdit(self.centralwidget)
        self.point2Edit.setGeometry(QtCore.QRect(673, 331, 117, 27))
        self.point2Edit.setReadOnly(True)
        self.point2Edit.setObjectName("point2Edit")
        self.point3Edit = QtGui.QLineEdit(self.centralwidget)
        self.point3Edit.setGeometry(QtCore.QRect(551, 364, 116, 27))
        self.point3Edit.setReadOnly(True)
        self.point3Edit.setObjectName("point3Edit")
        self.point4Edit = QtGui.QLineEdit(self.centralwidget)
        self.point4Edit.setGeometry(QtCore.QRect(673, 364, 117, 27))
        self.point4Edit.setReadOnly(True)
        self.point4Edit.setObjectName("point4Edit")
        self.effectCombo = QtGui.QComboBox(self.centralwidget)
        self.effectCombo.setGeometry(QtCore.QRect(540, 420, 251, 27))
        self.effectCombo.setObjectName("effectCombo")
        self.effectCombo.addItem("")
        self.effectCombo.addItem("")
        self.effectCombo.addItem("")
        self.effectCombo.addItem("")
        self.effectCombo.addItem("")
        self.effectCombo.addItem("")
        self.effectCombo.addItem("")
        self.effectLbl = QtGui.QLabel(self.centralwidget)
        self.effectLbl.setGeometry(QtCore.QRect(480, 420, 51, 27))
        self.effectLbl.setObjectName("effectLbl")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.sourceButton.setText(QtGui.QApplication.translate("MainWindow", "Load Source ...", None, QtGui.QApplication.UnicodeUTF8))
        self.targetButton.setText(QtGui.QApplication.translate("MainWindow", "Load Target ...", None, QtGui.QApplication.UnicodeUTF8))
        self.acquireButton.setText(QtGui.QApplication.translate("MainWindow", "Acquire Points", None, QtGui.QApplication.UnicodeUTF8))
        self.transformButton.setText(QtGui.QApplication.translate("MainWindow", "Transform", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(0, QtGui.QApplication.translate("MainWindow", "Nothing", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(1, QtGui.QApplication.translate("MainWindow", "Rotate 90°", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(2, QtGui.QApplication.translate("MainWindow", "Rotate 180°", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(3, QtGui.QApplication.translate("MainWindow", "Rotate 270°", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(4, QtGui.QApplication.translate("MainWindow", "Flip Horizontally", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(5, QtGui.QApplication.translate("MainWindow", "Flip Vertically", None, QtGui.QApplication.UnicodeUTF8))
        self.effectCombo.setItemText(6, QtGui.QApplication.translate("MainWindow", "Transpose", None, QtGui.QApplication.UnicodeUTF8))
        self.effectLbl.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Effect</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

