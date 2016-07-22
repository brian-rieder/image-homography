__author__ = 'ee364e02'

import sys, os
from scipy.misc import *
from PySide.QtCore import *
from PySide.QtGui import *

from Homography import *
from HomographyGUI import *

class HomographyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(HomographyApp, self).__init__(parent)
        self.setupUi(self)

        self.loading_buttons = [self.sourceButton, self.targetButton]
        self.graphs = [self.sourceGraph, self.targetGraph]
        self.point_fields = [self.point1Edit, self.point2Edit, self.point3Edit, self.point4Edit]
        self.action_buttons = [self.transformButton, self.resetButton, self.saveButton]

        self.source_selected = False
        self.target_selected = False

        self.pixel_map_item = None
        self.pointIndex = 0

        self.keyPressEvent = self.remove_point
        self.state_string = ""
        self.source_image = None
        self.target_image = None
        self.target_backup = None

        self.transformButton.clicked.connect(self.apply_homography)
        self.saveButton.clicked.connect(self.save_dialog)

        self.initialState()

    def initialState(self):
        self.state_string = "Initial"
        # all widgets but loading buttons start disabled
        self.acquireButton.setEnabled(False)
        for graph in self.graphs:
            graph.setEnabled(False)
        for point_field in self.point_fields:
            point_field.setEnabled(False)
        for button in self.action_buttons:
            button.setEnabled(False)
        self.effectLbl.setEnabled(False)
        self.effectCombo.setEnabled(False)

        self.sourceButton.clicked.connect(self.loadImage)
        self.targetButton.clicked.connect(self.loadImage)
        self.resetButton.clicked.connect(self.reset_target)

    def loadImage(self):
        button_pressed = self.sender().text().split()[1]
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open Image file ...', filter="Image Files (*.png)")
        if not filePath:
            return
        self.loadFromImageFile(filePath, button_pressed)

    def loadFromImageFile(self, filePath, button_pressed):
        write_location = None
        if button_pressed == "Source":
            write_location = self.sourceGraph
            self.source_selected = True
        elif button_pressed == "Target":
            write_location = self.targetGraph
            self.target_selected = True
        for graph in self.graphs:
            graph.setEnabled(True)
        scn = QtGui.QGraphicsScene()
        pixel_map = QtGui.QPixmap(filePath)
        pixel_map_item = QtGui.QGraphicsPixmapItem(pixel_map)
        scn.addItem(pixel_map_item)
        if button_pressed == "Target":
            self.pixel_map_item = pixel_map_item
        write_location.setScene(scn)
        write_location.fitInView(scn.sceneRect(), QtCore.Qt.KeepAspectRatio)
        if button_pressed == "Source":
            self.source_image = imread(filePath)
        elif button_pressed == "Target":
            self.target_image = imread(filePath)
            self.target_backup = filePath
        if self.state_string == "Ready":
            self.loadedState()
        elif self.source_selected and self.target_selected:
            self.acquireButton.setEnabled(True)
            self.state_string = "Loaded"
            self.acquireButton.clicked.connect(self.acquire_button_clicked)

    def pointSelectionState(self):
        self.state_string = "Point Selection"
        for button in self.loading_buttons:
            button.setEnabled(False)
        for field in self.point_fields:
            field.setEnabled(True)
        self.pixel_map_item.mousePressEvent = self.assign_point

    def assign_point(self, event):
        point_list = event.pos()
        if self.pointIndex < 4:
            self.point_fields[self.pointIndex].setText("{0:.0f}.0, {1:.0f}.0".format(point_list.x(), point_list.y()))
            self.pointIndex += 1

    def remove_point(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            if self.pointIndex > 0:
                self.pointIndex -= 1
                self.point_fields[self.pointIndex].setText("")

    def acquire_button_clicked(self):
        if self.pointIndex == 4:
            self.readyState()
        elif self.state_string == "Loaded":
            self.pointSelectionState()
        else:
            self.loadedState()

    def loadedState(self):
        self.state_string = "Loaded"
        for field in self.point_fields:
            field.setText("")
            field.setEnabled(False)
        for button in self.loading_buttons:
            button.setEnabled(True)
        for button in self.action_buttons:
            button.setEnabled(False)
        self.effectLbl.setEnabled(False)
        self.effectCombo.setEnabled(False)
        self.pointIndex = 0

    def readyState(self):
        self.state_string = "Ready"
        # enable all widgets
        for button in self.loading_buttons:
            button.setEnabled(True)
        for button in self.action_buttons:
            button.setEnabled(True)
        for field in self.point_fields:
            field.setEnabled(True)
        self.effectLbl.setEnabled(True)
        self.effectCombo.setEnabled(True)


    def apply_homography(self):
        if self.source_image.ndim == 2:
            gui_transformation = Transformation(self.source_image)
        else:
            gui_transformation = ColorTransformation(self.source_image)
        target_points = []
        for field in self.point_fields:
            target_points.append(tuple([float(num) for num in field.text().split(', ')]))
        effect = None
        effect_ind = self.effectCombo.currentIndex()
        if effect_ind == 1:
            effect = Effect.rotate90
        elif effect_ind == 2:
            effect = Effect.rotate180
        elif effect_ind == 3:
            effect = Effect.rotate270
        elif effect_ind == 4:
            effect = Effect.flipHorizontally
        elif effect_ind == 5:
            effect = Effect.flipVertically
        elif effect_ind == 6:
            effect = Effect.transpose
        gui_transformation.setupTransformation(target_points, effect=effect)
        transformed_image = gui_transformation.transformImage(self.target_image)
        imsave("TMP_IMG.png", transformed_image)
        scn = QtGui.QGraphicsScene()
        pixel_map = QtGui.QPixmap("TMP_IMG.png")
        pixel_map_item = QtGui.QGraphicsPixmapItem(pixel_map)
        scn.addItem(pixel_map_item)
        self.pixel_map_item = pixel_map_item
        self.targetGraph.setScene(scn)
        self.targetGraph.fitInView(scn.sceneRect(), QtCore.Qt.KeepAspectRatio)
        os.remove("TMP_IMG.png")
        self.transformedState()

    def transformedState(self):
        self.state_string = "Transformed"
        self.acquireButton.setEnabled(False)
        for field in self.point_fields:
            field.setEnabled(False)

    def save_dialog(self):
        filePath, _ = QFileDialog.getSaveFileName(self, caption='Save Target to ...')
        if not filePath:
            return
        imsave(filePath, self.target_image, "png")

    def reset_target(self):
        self.loadFromImageFile(self.target_backup, "Target")
        self.readyState()

if __name__ == '__main__':
    currentApp = QApplication([])
    currentForm = HomographyApp()

    currentForm.show()
    currentApp.exec_()